from abc import ABC, abstractmethod


class Action(ABC):
    def __init__(self):
        self._done = False
    @abstractmethod
    def do(self):
        if self._done:
            raise Exception("Operation cannot be done twice.")
        self._done = True

    def undo(self):
        if not self._done:
            raise Exception("Operation cannot be undone twice.")
        self._done = False