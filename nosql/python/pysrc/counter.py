""" module counter.py, Chris Joakim, Microsoft, 2023 """

class Counter():
    """
    This class implements a simple int counter with an underlying dict object.
    """
    def __init__(self):
        self.data = {}

    def increment(self, key: str) -> None:
        """ Increment the given key by 1. """
        keys = self.data.keys()
        if key in keys:
            self.data[key] = self.data[key] + 1
        else:
            self.data[key] = 1

    def decrement(self, key: str) -> None:
        """ Decrement the given key by 1. """
        keys = self.data.keys()
        if key in keys:
            self.data[key] = self.data[key] - 1
        else:
            self.data[key] = -1

    def get_value(self, key: str) -> int:
        """ Get the int value of the given key. """
        keys = self.data.keys()
        if key in keys:
            return self.data[key]
        return 0

    def get_data(self) -> dict:
        """ Return the underlying dict object. """
        return self.data
