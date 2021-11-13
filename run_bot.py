import ast
import sys

sys.path.insert(0, ".")

from headline_extender.context import Context

context = Context()
starting = context.new_index()
while True:
    if context.run_for_index(
        starting,
        "@BBCNorthAmerica",
        tweet=ast.literal_eval(sys.argv[1]) if len(sys.argv) > 1 else True,
    ):
        break
    starting += 1