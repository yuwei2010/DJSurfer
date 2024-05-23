#%%
import unittest

from djsurfer.lib_interface.d97_object import D97_Object
from djsurfer.datapool import DataPool
class Test_DataPool(unittest.TestCase):

    def test_datapool_with_D97_Object(self):
        # Create a D97_Object instance
        TestPath = 'C:/project/PS_Sensor/measure/20240426'

        # Add test data to the datapool
        #dp = DataPool(TestPath, interface= D97_Object,ftype='zip')
        dp = DataPool(TestPath, interface= D97_Object,ftype='.zip')
        print(f'{len(dp.objs)} Dataframe are existed in the Data pool')
      
        
        P_ref = dp.get_signal('p_MC_Model')
        print(P_ref.head(20))

        assert len(dp.objs) == 2
        # Assert that the retrieved data is the same as the original D97_Object instance
      

if __name__ == '__main__':
    unittest.main()
# %%
