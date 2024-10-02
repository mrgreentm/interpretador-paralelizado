from abc import ABC, abstractmethod

class IComponent(ABC):
    @abstractmethod
    def processar(self):
        pass