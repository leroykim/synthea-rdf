from abc import ABC, abstractmethod
from pandas import DataFrame


class Resource(ABC):
    @abstractmethod
    def __init__(self, df: DataFrame):
        self.__resource_df = df

    @property
    @abstractmethod
    def resource_df(self):
        pass

    @resource_df.setter
    @abstractmethod
    def resource_df(self, value):
        pass

    @abstractmethod
    def convert(self, graph):
        pass
