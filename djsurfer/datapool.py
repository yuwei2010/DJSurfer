
import pandas as pd
import numpy as np
from pathlib import Path
import re
import os

#%%
class DataPool(object):
       
    def __init__(self, input_item, interface, **kwargs):
        """
        Initializes a DataPool object.

        Args:
            input_item (str): The input item to search for files.
            interface (class): The interface class to create objects from files.

        Attributes:
            objs (list): A list of objects created from the files found.

        """
        pattern = kwargs.pop('pattern', None)
        file_extension = kwargs.pop('ftype', None)
        if file_extension is None:        
            files = Path(input_item).rglob('*') # find all files in directory
        else:
            files = []
            if pattern is not None:
                regex = re.compile(pattern)
            else:
                regex = re.compile('.*')
            for root, _, filenames in os.walk(input_item):
                for filename in filenames:
                    if filename.endswith(file_extension) and regex.search(filename):
                        files.append(os.path.join(root, filename))

        if len(files) != 0:
            self.objs = [interface(file) for file in files] # create objects from files
        else:
            print("No specific file found.")
        
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

            
        
        
        
        
        
        