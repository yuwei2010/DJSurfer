
import pandas as pd
import numpy as np
from pathlib import Path

#%%
class DataPool(object):
       
    def __init__(self, input_item, interface):
        """
        Initializes a DataPool object.

        Args:
            input_item (str): The input item to search for files.
            interface (class): The interface class to create objects from files.

        Attributes:
            objs (list): A list of objects created from the files found.

        """
        files = Path(input_item).rglob('*') # find all files in directory
        self.objs = [interface(file) for file in files] # create objects from files
        
    def get_signal(self, name):
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
            
            if name in obj.dataframe.columns:
                dats.append(df[name])
                
            else:
                dats.append(pd.Series(np.nan*np.ones(len(self.index)), index=df.index))

        out = pd.concat(dats, axis=1)
        out.columns = [obj.name for obj in self.objs]
        
        return out

            
        
        
        
        
        
        