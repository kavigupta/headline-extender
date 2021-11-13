import requests

from permacache import permacache

from .secret import deepai_api_key

# try to keep the stories light. Obviously not perfect but at least an attempt
BAN_LIST = [
    "murder",
    "kill",
    "ra" + "pe",
    "torture",
    "assault",
    "genocide",
    "atrocit",
    "homocide",
    "gun",
    "gang",
]


def check_output(output):
    lines = [x for x in output.split("\n") if x]
    while lines:
        if lines[-1].endswith("."):
            break
        lines.pop()
    if not all(x[0].isalpha() or x[0] == '"' for x in lines):
        return False
    if len(lines) <= 4:
        return False
    if lines[0][0] == lines[1][0]:
        return False
    if not all(len(line.split()) > 10 for line in lines[1:]):
        return False
    if sum(":" in line for line in lines) > len(lines) / 2:
        return False
    if any(word in output for word in BAN_LIST):
        return False
    text = "\n\n".join(lines)
    words = set(text.split())
    all_uppercase = [x for x in words if x.isupper() and len(x) > 4]
    if all_uppercase:
        return False
    return text


@permacache("headline_extender/sample_article/sample_5")
def sample(prompt, tries=5):
    for _ in range(tries):
        r = requests.post(
            "https://api.deepai.org/api/text-generator",
            data={
                "text": prompt,
            },
            headers={"api-key": deepai_api_key},
        )
        output = r.json()["output"]
        output = check_output(output)
        if output:
            return output


def locate_article(context, base_account, tl):
    for tweet in tl[::-1]:
        *first, _ = tweet.text.split(" ")
        if context.has_used(tweet.id):
            continue
        prompt = " ".join(first) + ".\n"
        if "\n" in prompt[:-1]:
            continue
        if prompt.startswith("RT @"):
            continue
        output = sample(prompt)
        url = f"https://twitter.com/{base_account[1:]}/status/{tweet.id}"
        if output is not None:
            return output, tweet.id, url
    return None, None, None
