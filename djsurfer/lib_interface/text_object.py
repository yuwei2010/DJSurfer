
import pandas as pd
from djsurfer.datainterface import DataInterface

#%%
class TEXT_OBJECT(DataInterface):
    """
    A class representing a text object to access data in a text file.

    Args:
        path (str): The path to the text file.
        name (str, optional): The name of the text object. Defaults to None.
        comment (str, optional): Any additional comment about the text object. Defaults to None.
    """

    def __init__(self, path, name=None, comment=None, delimiter=','):
        
        super().__init__(path=path, name=name, comment=comment)
        
        self.delimiter = delimiter


        
    def get_df(self):
        """
        Read the text file and return its contents as a pandas DataFrame.

        Returns:
            pandas.DataFrame: The contents of the text file as a DataFrame.
        """
        with open(self.path, 'r') as f:
            lines = f.readlines()
       
        df = pd.DataFrame([l.strip().split(self.delimiter) for l in lines[1:]], 
                          columns=lines[0].strip().split(self.delimiter))
        
        return df
        

if __name__ == '__main__':
    
    from pathlib import Path
    obj = TEXT_OBJECT(Path(__file__).parent / r'..\..\tests\demo_data\data0.txt')

