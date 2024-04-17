#!/usr/bin/env python

"""Tests for `djsurfer` package."""
import pytest
import numpy as np
import pandas as pd

from pathlib import Path

#%%
@pytest.fixture
def dir_data():
    
    dir = Path(__file__).parent / 'demo_data'
    dir.mkdir(exist_ok=True)
    
    arr0 = np.random.rand(100, 10)
    columns = [f'col_{i}' for i in range(10)]    
    df = pd.DataFrame(np.round(arr0, 4), columns=columns)   
    df.to_csv(dir / 'data0.txt', index=False)
    
    arr1 = np.random.rand(100, 7)
    columns = [f'col_{i}' for i in range(5, 12)]    
    df = pd.DataFrame(np.round(arr1, 4), columns=columns)   
    df.to_csv(dir / 'data1.txt', index=False)    

    return str(dir)

#%%
def test_textobject(dir_data):
    
    from djsurfer.lib_interface.text_object import TEXT_OBJECT
    
    path = Path(dir_data) / 'data0.txt'
    obj = TEXT_OBJECT(path)

    assert isinstance(obj.dataframe, pd.DataFrame)
    
#%%   
def test_datapool(dir_data):
    
    from djsurfer.datapool import DataPool
    from djsurfer.lib_interface.text_object import TEXT_OBJECT
    
    dp = DataPool(dir_data, TEXT_OBJECT)
    
    assert len(dp.objs) == 2  
    