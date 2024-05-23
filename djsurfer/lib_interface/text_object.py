
import pandas as pd
from djsurfer.datainterface import DataInterface

#%%
class TextObject(DataInterface):
    """
    A class representing a text object to access data in a text file.

    Args:
        path (str): The path to the text file.
        name (str, optional): The name of the text object. Defaults to None.
        comment (str, optional): Any additional comment about the text object. Defaults to None.
    """

    def __init__(self, path, name=None, comment=None, delimiter=','):
        
        # Initialize the text interface object, passing the path, name, and comment to the base class.
        super().__init__(path=path, name=name, comment=comment)
        
        # Default delimiter is a comma.
        self.delimiter = delimiter
        
        
    def __repr__(self):
        
        return f'"{self.name}"@{self.__class__.__name__}'
    
    def __str__(self):
        
        return f'{self.name}'
        
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

