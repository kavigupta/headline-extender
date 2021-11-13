import os
import json

context_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "context.json")


class Context:
    def __init__(self):
        with open(context_file) as f:
            result = json.load(f)
        self.result = result

    def dump(self):
        with open(context_file, "w") as f:
            json.dump(self.result, f)

    def has_used(self, tweet):
        return tweet in self.result.get("used_tweets", [])

    def use_tweet(self, tweet):
        self.result["used_tweets"] = self.result.get("used_tweets", []) + [tweet]
        self.dump()
