
import pandas as pd
from djsurfer.datainterface import DataInterface

#%%
class XmlObject(DataInterface):
    """
    A class representing a XML object to access data in a XML file.

    Args:
        path (str): The path to the XML file.
        name (str, optional): The name of the XML object. Defaults to None.
        comment (str, optional): Any additional comment about the XML object. Defaults to None.
    """

    def __init__(self, path, name=None, comment=None, prop_name = 'property', attr_name = 'name', 
                 attr_text = ['item_id', 'item_revision_id', 'object_name', 'rb6_regulation_long_title']):
        
        # Initialize the text interface object, passing the path, name, and comment to the base class.
        super().__init__(path=path, name=name, comment=comment)
        
        # Default prop_name is string 'property'.
        self.prop_name = prop_name
        # Default attr_name is string 'name'.
        self.attr_name = attr_name
        # Default attr_text is a list of four major attribute names.
        self.attr_text = attr_text

        
    def get_df(self):
        """
        Read the XML file, parse the structure, and return the specific contents as a pandas DataFrame.

        Returns:
            pandas.DataFrame: The contents which are extracted by defined attributes as a DataFrame.
        """
        import xml.etree.ElementTree as ET
        
        # Read the XML file and parse the structure.
        tree = ET.parse(self.path)
        root = tree.getroot()

        # Create a DataFrame to store the parsed and extracted contents.
        df = pd.DataFrame()

        for i in self.attr_text:
            # create a list for each attribute
            globals()[f'data_{i}'] = []

            # Extract the contents by defined attributes.
            for obj in root.iter(self.prop_name):
                attr = obj.find(self.attr_name)
                if attr.text == i:
                    value = obj.find('value').find('key').text
                    globals()[f'data_{i}'].append(value)

            # Store the extracted contents in the DataFrame.
            df[i] = globals()[f'data_{i}']
       
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
    obj = XmlObject(Path(__file__).parent / r'..\..\tests\demo_data\data0.txt')

