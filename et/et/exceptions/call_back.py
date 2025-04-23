import abc
from abc import ABC


class CallBack(ABC):
    @abc.abstractmethod
    def invoke(self): ...