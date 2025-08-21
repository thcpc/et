import abc


class Assignee(abc.ABC):
    @abc.abstractmethod
    def handle(self, task): ...
