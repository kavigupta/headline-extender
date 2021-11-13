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
        return max([x["index"] for x in self.result] + [0]) + 1

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
            return True
        image = render_text("DeepAI's GPT2 text generation model", base_account, text)
        path = f"outputs/{index}.png"
        image.save(path)
        result = api.update_with_media(path, status=text.split("\n")[0])
        api.update_status(status=link, in_reply_to_status_id=result.id)
        self.use_tweet(
            original_tweet=tweet_id,
            new_tweet=result.id,
            index=index,
            image_path=path,
            text=text,
        )
        return False

    def use_tweet(self, original_tweet, new_tweet, index, image_path, text):
        self.result.append(
            dict(
                original_tweet=original_tweet,
                new_tweet=new_tweet,
                index=index,
                image_path=image_path,
                text=text,
            )
        )
        self.dump()
