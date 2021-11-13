import os
import re
import tempfile
import subprocess

from PIL import Image

ROOT_DIRECTORY = os.path.dirname(os.path.dirname(__file__))


def render_text(software_tool, base_account, output):
    output = output.replace("\u200b", "")
    output = dumb_to_smart_quotes(output)
    header, *rest = output.split("\n")
    assert header.endswith(".")
    header = header[:-1]
    rest = "\n".join(rest)
    with open(f"{ROOT_DIRECTORY}/template/template.tex") as f:
        code = f.read()
    code = (
        code.replace("TITLE", header)
        .replace("BASEACCOUNT", base_account)
        .replace("TEXT", rest)
        .replace("SOFTWARETOOL", software_tool)
    )
    root = tempfile.mkdtemp() + "/"
    with open(root + "file.tex", "w") as f:
        f.write(code)
    subprocess.check_call(["pdflatex", "-output-directory=" + root, root + "file.tex"])
    subprocess.check_call(
        [
            "convert",
            "-background",
            "#FFF1E5",
            "-alpha",
            "remove",
            "-density",
            "300",
            root + "file.pdf",
            "-quality",
            "400",
            root + "file.png",
        ]
    )
    return Image.open(root + "file.png")


def dumb_to_smart_quotes(string):
    """Takes a string and returns it with dumb quotes, single and double,
    replaced by smart quotes. Accounts for the possibility of HTML tags
    within the string.
    
    Based on https://gist.github.com/davidtheclark/5521432
    """

    # Find dumb double quotes coming directly after letters or punctuation,
    # and replace them with right double quotes.
    string = re.sub(r'([a-zA-Z0-9.,?!;:\'\"])"', r"\1''", string)
    # Find any remaining dumb double quotes and replace them with
    # left double quotes.
    string = string.replace('"', "``")
    return string