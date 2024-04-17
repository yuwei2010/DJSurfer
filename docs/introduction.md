# Welcome to the Datasurfer Tutorial

In this tutorial, you'll gain a rapid insight of Datasurfer, covering installation, building your initial data pool, searching for certain data, and visualizing it.

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