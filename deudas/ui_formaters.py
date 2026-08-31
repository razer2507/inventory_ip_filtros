from abc import ABC, abstractmethod


class UiFormatter(ABC):
    pass
    @abstractmethod
    def obtain(self):
        pass
