
import pandas as pd
from djsurfer.datainterface import DataInterface

#%%
class TEXT_OBJECT(DataInterface):
    
    def __init__(self, path, name=None, comment=None):
        
        super().__init__(path, name, comment)
        
    def get_df(self):
        
        # Read the text file
        with open(self.path, 'r') as f:
            data = f.readlines()
        
        # Create a dataframe
        df = pd.DataFrame([l.strip().split(',') for l in data[1:]], columns=data[0].strip().split(','))
        
        return df
        

if __name__ == '__main__':
    
    obj = TEXT_OBJECT('text.txt')

