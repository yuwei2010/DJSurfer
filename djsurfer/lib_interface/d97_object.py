import pandas as pd
import numpy as np
from djsurfer.datainterface import DataInterface


class D97_Object(DataInterface):
    """
    A class representing a *.D97 object to access data in a D97 file.

    Args:
        path (str): The path to the D97 file.
        name (str, optional): The name of the D97 object. Defaults to None.
        comment (str, optional): Any additional comment about the text object. Defaults to None.
    """

    def __init__(self, path, name=None, comment=None,relevant_signals=[]):

        # relevant_signals is the list of the Signal names that will be readed from D97 file
        from d97parser import d97parser 
  
        self.d97parser = d97parser 
        # Initialize the text interface object, passing the path, name, and comment to the base class.
        super().__init__(path=path, name=name, comment=comment)
        
        # Define the Default relevant Signals
        if relevant_signals == []:
           self.relevant_signals = ['p_MC_Model','RBMESG_RB_VirtualPressureSensor']

        
    def get_df(self): 

    # 
        """
        Read the d97 file and return its contents as a pandas DataFrame. (D97 has .zip)

        Returns:
            pandas.DataFrame: The contents of the D97 file as a DataFrame.
        """
          # Load data using d97parser package
        loaded_data = self.d97parser.load_signals(measurement_filepath=self.path,
                                         add_signal_names=self.relevant_signals)

    # Convert TimeSeries object from d97parser to pandas dataframe
        if loaded_data ==None: 
            pass

        signalDf = pd.DataFrame()

               
        for tsSignal in self.relevant_signals:
        
            # Create temporary dataframe with TimeSeries information
            tempDf = pd.DataFrame(data=loaded_data[tsSignal].values,
                                index=np.round(loaded_data[tsSignal].timestamps, decimals=3),
                                columns=[tsSignal])
            
            # Insert extracted information into pre-initialized dataframe
            if len(signalDf) == 0:
                # Initialize signal dataframe with temp dataframe
                signalDf = tempDf
            else:
                # Outer join of new content with signal dataframe
                signalDf = signalDf.join(tempDf, how='outer', lsuffix='', rsuffix='')
        
            # Forward-fill & back-fill the dataframe to deal with different sampling rates
            signalDf.ffill(inplace=True)  
            signalDf.bfill(inplace=True) 

        # reindex of signalDf 
    
        signalDf['time'] = signalDf.index.values  # Convert index to column named 'time'
        signalDf.reset_index(drop=True, inplace=True) # Reset index to integer values
        
        
        self.signalDf = signalDf

        # Output summary of pandas dataframe
        signalDf.describe()

        return self.signalDf


    def to_excel(self, path):
        """
        Save the text object to an Excel file.

        Args:
            path (str): The path to save the Excel file.
        """
        self.signalDf.to_excel(path, index=True)

    def to_csv(self, path):
        """
        Save the text object to a CSV file.

        Args:
            path (str): The path to save the CSV file.
        """
        self.signalDf.to_csv(path, index=False)    

 #%%   

if __name__ == '__main__':
    
    from pathlib import Path
    
    obj = D97_Object('C:/project/PS_Sensor/measure/20240426/bl10inc3loc_pmc_ai_v3_V223_1690_240428_00.zip')
    mydf= obj.get_df()
    print(mydf.head(10))
    obj.to_csv('C:/project/PS_Sensor/measure/20240426/bl10inc3loc_pmc_ai_v3_V223_1690_240428_00.csv')

    print('Unit Test successful')
 #%%   