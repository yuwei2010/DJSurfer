# Welcome to Datasurfer

In this chapter, you'll gain a rapid insight of Datasurfer, covering installation, building your initial data pool, searching for certain data, and visualizing it.

## Install Datasurfer

To initiate the installation of Datasurfer, execute the following command:

> pip install datasurfer

## Create Data Files

Before diving into data harnessing with Datasurfer, let's first create some data files in various formats.

```python
import numpy as np
import pandas as pd
import json
from pathlib import Path

np.random.seed()

# Create a directory to store the data.
dir_data = Path('demo_data')
dir_data.mkdir(exist_ok=True)

# Create a csv file.
data1 = pd.DataFrame(np.random.rand(4, 5), columns=list('abcde'))
data1.to_csv(dir_data / 'data1.csv', index=False)

# Create an excel file
data2 = pd.DataFrame(np.random.rand(6, 4), columns=list('bcde'))
data2.to_excel(dir_data / 'data2.xlsx', index=False)

# Create a json file
data3 = pd.DataFrame(np.random.rand(5, 3), index=list('cdefg'))
json.dump(data3.to_dict(), open(dir_data / 'data3.json', 'w'),  indent=4)
```

## Data Pool

### Create a Data Pool Object by Path
We've now generated three files within the "demo_data" directory, each has different file types, varying data sizes, and unequal column names.

In the next step, We will create a data pool object to organize and contain these files.

```python
import datasurfer as ds

# Create a DataSurfer object by giving the path of the data files
dp = ds.Data_Pool("demo_data")

# display all information of the data pool 
dp.describe(verbose=True)
```

### List Signal Names in the Pool
The data pool description provides details on the three files we've created, including signals, file types, sizes, and more. Using the following command, you can view all the signal names stored in the data pool:

```python
# list all pool signals

dp.list_signals()
```

### Retrieve Single Signal from Pool

The Pool returns values from files within the pool, presenting them as a pandas DataFrame. To achieve data length alignment, empty spaces will be filled with 'NaN'.

```python
# Obtain signal "c" from pool files
df = dp['c']

df
```

### Retrieve multiple signals from Pool

The Pool can also return multiple signals at once. The signals can be specified by a list of signal names:

```python

# Depresse warning messages
import warnings
warnings.filterwarnings("ignore")

# Return a DataFrame containing signals 'b' and 'c'; non-existent values will be filled with NaN.
df = dp[['b', 'c']]
df
```

### Visualize data in the pool

You can also plot the data in the pool directly. The following code will satter pool signals:

```python
# Scatter signal "c" and "d" and set the axis labels
dp.plot.scatter('c', 'd', setax=True);
```

