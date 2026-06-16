from abc import ABC, abstractmethod


class Action(ABC):
    @abstractmethod
    def do(self):
        pass

    def undo(self):
        pass

