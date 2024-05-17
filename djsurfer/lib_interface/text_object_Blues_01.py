
import pandas as pd
from djsurfer.datainterface import DataInterface

#%%
class Data(DataInterface):
    """
    A class representing a text object to access data in a text file.

    Args:
        path (str): The path to the text file.
        name (str, optional): The name of the text object. Defaults to None.
        comment (str, optional): Any additional comment about the text object. Defaults to None.
    """

    def __init__(self, path, name=None, comment=None, delimiter='r\t'):
        
        self.path = path
        #self.name = name
        #self.comment = comment
        #super().__init__(path=path, name=name, comment=comment)
        
        self.delimiter = delimiter
        
    def get_df(self):
        """
        Read the text file and return its contents as a pandas DataFrame.

        Returns:
            pandas.DataFrame: The contents of the text file as a DataFrame.
        """
        with open(self.path,"r") as f:
            table1 = f.read()
        
        #split the data into lines
        lines = table1.strip().split("\n")
        
        #extract the column names from the first line
        column_names = lines[0].split("\t")
        
        data = []
        for line in lines[1:]:
            values = line.split("\t")
            data.append({column_names[i]: value for i, value in enumerate(values)})
        
        df = pd.DataFrame(data)
      
        #print(table1)
        return df
    
    #def to_excel(self, path):
        """
        Save the text object to an Excel file.

        Args:
            path (str): The path to save the Excel file.
        """
        #self.df.to_excel(path, index=False)
        

if __name__ == '__main__':
    
    from pathlib import Path
    obj = Data(Path(__file__).parent / r"C:\TEST\PLKO.txt")

