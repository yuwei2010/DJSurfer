
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
        files = Path(input_item).rglob('*')
        self.objs = [interface(file) for file in files]
        
    def get_signal(self, name):
        dats = []
        
        for obj in self.objs:
            df = obj.get_df()
            
            if name in obj.columns:
                dats.append(df[name])
                
            else:
                dats.append(pd.Series(np.nan*np.ones(len(self.index)), index=df.index))

        out = pd.concat(dats, axis=1)
        
        return  out

            
        
        
        
        
        
        