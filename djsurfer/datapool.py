
import pandas as pd
import numpy as np
from pathlib import Path

#%%
class DataPool(object):
       
    def __init__(self, path, interface, **kwargs):
        """
        Initializes a DataPool object.

        Args:
            input_item (str): The input item to search for files.
            interface (class): The interface class to create objects from files.

        Attributes:
            objs (list): A list of objects created from the files found.

        """
        pattern = kwargs.pop('pattern', None) or '*'
        files = list(Path(path).rglob(pattern)) # find all files in directory

        self.objs = [interface(file, name=file.stem) for file in files] # create objects from files
        
    def get_signal(self, key):
        """
        Retrieve a signal from the datapool.

        Parameters:
        - name (str): The name of the signal to retrieve.

        Returns:
        - out (pd.DataFrame): A DataFrame containing the signal data.
        """
        dats = []
        
        for obj in self.objs:
            df = obj.dataframe
                      
            if key in obj.dataframe.columns:
                dats.append(df[key])           
            else:
                dats.append(pd.Series(np.nan*np.ones(len(df.index)), index=df.index))

        out = pd.concat(dats, axis=1)
        out.columns = [obj.name for obj in self.objs]
        
        return out
    
    def to_excel(self, path, key, **kwargs):
        """
        Write the data to an Excel file.

        Parameters:
        - path (str): The path to the Excel file.
        - key (str): The key to use for the data.
        """
        
        df = self.get_signal(key)           
        df.to_excel(path, **kwargs)     
          
        return self
        

#%%            
        
        
        
        
        
        