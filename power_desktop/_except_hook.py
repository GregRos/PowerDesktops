import pdb, threading
from typing import Any


def pm(args: Any):
    pdb.post_mortem(args.exc_traceback)  # stops at the raise site


threading.excepthook = pm
