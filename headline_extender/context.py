import os
import json

from .tweet import get_api
from .sample_article import locate_article
from .render import render_text

context_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "context.json")


class Context:
    def __init__(self):
        with open(context_file) as f:
            result = json.load(f)
        self.result = result

    def new_index(self):
        id = get_api().user_timeline("@bot_guesses")[0].id
        matching = [x for x in self.result if x["new_tweet"] == id]
        if matching:
            return matching[0]["index"] + 1
        return 1

    def dump(self):
        with open(context_file, "w") as f:
            json.dump(self.result, f, indent=2)

    def has_used(self, original_tweet):
        return any(original_tweet == tweet["original_tweet"] for tweet in self.result)

    def make_for_index(self, index, base_account):
        matching_index = [tweet for tweet in self.result if tweet["index"] == index]
        if len(matching_index) == 1:
            return matching_index[0]
        api = get_api()
        tl = api.user_timeline(base_account)
        text, tweet_id, link = locate_article(self, base_account, tl)
        if text is None:
            return None
        image = render_text("DeepAI's GPT2 text generation model", base_account, text)
        path = f"outputs/{index}.png"
        image.save(path)
        self.result.append(
            dict(
                original_tweet=tweet_id,
                new_tweet=None,
                index=index,
                image_path=path,
                link=link,
                text=text,
            )
        )
        self.dump()
        return self.make_for_index(index, base_account)

    def run_for_index(self, index, base_account, tweet):
        item = self.make_for_index(index, base_account)

        if item is None:
            return True

        if tweet:
            api = get_api()
            result = api.update_with_media(
                item["image_path"], status=item["text"].split("\n")[0]
            )
            api.update_status(status=item["link"], in_reply_to_status_id=result.id)

            item["new_tweet"] = result.id

        return False
