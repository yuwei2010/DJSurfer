
from abc import ABC, abstractmethod

#%%
class DataInterface(ABC):
    
    def __init__(self, path, name=None, comment=None, config=None):
        
        self.path = path
        self.name = name
        self.comment = comment
        self.config = config
        self.df = self.get_df()
        
        
    @abstractmethod
    def get_df(self):
        pass