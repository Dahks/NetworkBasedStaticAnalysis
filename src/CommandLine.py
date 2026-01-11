import os
import sys
class CommandLineOptions():
    """
    `Singleton` maintaining commandline arguments (if applicable)
    """
    flags: dict = {}

    def __init__(self):
        raise Exception("Not an instantiable class")

    @classmethod
    def load(cls):
        if len(args := sys.argv) < 2:
            raise Exception("args must include filename")

        cls.flags["filename"] = (filename := args[1])
        if not (os.path.exists(filename)):
            raise Exception("First arg must be a valid filename / path")
