
import pandas as pd
from asammdf import MDF
from djsurfer.datainterface import DataInterface

#%%
class Mf4Object(DataInterface):
    """
    A class representing a mf4 object to access data in a mf4 file.

    Args:
        path (str): The path to the mf4 file.
        name (str, optional): The name of the mf4 object. Defaults to None.
        comment (str, optional): Any additional comment about the mf4 object. Defaults to None.
    """

    def __init__(self, path, name=None, comment=None):
        
        # Initialize the text interface object, passing the path, name, and comment to the base class.
        super().__init__(path=path, name=name, comment=comment)

        
    def get_df(self):
        """
        Read the mf4 file and return its contents as a pandas DataFrame.

        Returns:
            pandas.DataFrame: The contents of the text file as a DataFrame.
        """
        # Read the mf4 file and return its contents as a DataFrame.
        mdf = MDF(self.path)
        df = mdf.to_dataframe()
        
        return df
    
    def to_excel(self, path):
        """
        Save the text object to an Excel file.

        Args:
            path (str): The path to save the Excel file.
        """
        self.df.to_excel(path, index=False)
        

if __name__ == '__main__':
    
    from pathlib import Path
    obj = TextObject(Path(__file__).parent / r'..\..\tests\demo_data\data0.txt')

