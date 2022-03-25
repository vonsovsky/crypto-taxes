from abc import ABC, abstractmethod
import pickle


class Reader(ABC):

    def save(self, records):
        with open(self.get_pickle_filename(), "wb") as fw:
            pickle.dump(records, fw)

    def load(self):
        with open(self.get_pickle_filename(), "rb") as fr:
            return pickle.load(fr)

    @abstractmethod
    def get_pickle_filename(self):
        pass

    @abstractmethod
    def read_file(self, filename):
        pass
