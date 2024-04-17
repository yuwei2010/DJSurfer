
import pandas as pd
from djsurfer.datainterface import DataInterface

#%%
class TEXT_OBJECT(DataInterface):
    """
    A class representing a text object.

    Args:
        path (str): The path to the text file.
        name (str, optional): The name of the text object. Defaults to None.
        comment (str, optional): Any additional comment about the text object. Defaults to None.
    """

    def __init__(self, path, name=None, comment=None):
        super().__init__(path, name, comment)
        
    def get_df(self):
        """
        Read the text file and return its contents as a pandas DataFrame.

        Returns:
            pandas.DataFrame: The contents of the text file as a DataFrame.
        """
        with open(self.path, 'r') as f:
            data = f.readlines()
        
        df = pd.DataFrame([l.strip().split(',') for l in data[1:]], columns=data[0].strip().split(','))
        
        return df
        

if __name__ == '__main__':
    
    obj = TEXT_OBJECT('text.txt')

