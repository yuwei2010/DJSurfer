
from abc import ABC, abstractmethod
from pathlib import Path

#%%
class DataInterface(ABC):
    """
    Abstract base class for data interfaces.
    """

    def __init__(self, path, name=None, comment=None, config=None):
        """
        Initializes a DataInterface object.

        Parameters:
        - path (str): The path to the data.
        - name (str, optional): The name of the data interface. Defaults to None.
        - comment (str, optional): Any additional comment or description. Defaults to None.
        - config (dict, optional): Configuration parameters for the data interface. Defaults to None.
        """
        self.path = Path(path)
        self.__name = name
        self.comment = comment
        self.config = config

        
    @property
    def name(self):
        
        if self.__name is None:
            self.__name = self.path.stem
        
        return self.__name

    @property
    def dataframe(self):
        """
        Returns the dataframe associated with the data interface.
        
        Returns:
            pandas.DataFrame: The dataframe associated with the data interface.
        """
        return self.get_df()
    
    df = dataframe

    @abstractmethod
    def get_df(self):
        
        """
        Abstract method to get the data as a pandas DataFrame.

        Returns:
        - df (pandas.DataFrame): The data as a pandas DataFrame.
        """

