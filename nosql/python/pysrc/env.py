""" module env.py, Chris Joakim, Microsoft, 2023 """

import os
import sys
import time

class Env():
    """
    This class is used to read the host environment, such as username and
    environment variables.  It also has methods for command-line flag
    argument processing.
    """

    @classmethod
    def var(cls, name: str, default=None) -> str | None:
        """ Return the value of the given environment variable name, or None. """
        if name in os.environ:
            return os.environ[name]
        return default

    @classmethod
    def username(cls) -> str | None:
        """ Return the USERNAME (Windows) or USER (macOS/Linux) value. """
        usr = cls.var('USERNAME')
        if usr is None:
            usr = cls.var('USER')
        return usr

    @classmethod
    def epoch(cls) -> float:
        """ Return the current epoch time, as time.time() """
        return time.time()

    @classmethod
    def verbose(cls) -> bool:
        """ Return a boolean indicating if --verbose or -v is in the command-line. """
        flags = [ '--verbose', '-v' ]
        for arg in sys.argv:
            for flag in flags:
                if arg == flag:
                    return True
        return False

    @classmethod
    def boolean_arg(cls, flag: str) -> bool:
        """ Return a boolean indicating if the given arg is in the command-line. """
        for arg in sys.argv:
            if arg == flag:
                return True
        return False
