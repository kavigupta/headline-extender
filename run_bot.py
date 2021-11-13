import sys

sys.path.insert(0, ".")

from headline_extender.context import Context

context = Context()
while True:
    if context.make_for_index(context.new_index(), "@BBCNorthAmerica"):
        break