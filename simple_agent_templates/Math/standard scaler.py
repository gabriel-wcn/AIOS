# AICHOO OS Simple Agent 
# Documentation about AI OS and how to create Simple Agents can be found on our WiKi
# https://github.com/eghamtech/AIOS/wiki/Simple-Agents
# https://github.com/eghamtech/AIOS/wiki/AI-OS-Introduction
#
# this agent creates 3 new columns by applying 3 methods of scaling to a selected field

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import QuantileTransformer
from sklearn.preprocessing import Imputer
from numpy import inf

# obtain random field of numerical type
# restrict selection to those that not already used and not created by the agent
col_definition1 = "{random_field_numeric_distinct}"
# field definition received from the kernel contains two parts: name of the field and CSV filename that holds the actual data
# load these two parts into variables
col1 = col_definition1.split("|")[0]
file1 = col_definition1.split("|")[1]

# "workdir" must be specified in Constants - it is a global setting where all CSV files are stored on Jupyter server
# read the data for selected column
df = pd.read_csv(workdir+file1)[[col1]]

#print( np.argwhere(np.isnan(np.array(df))) )
#print( np.argwhere(np.isinf(np.array(df))) )

# convert selected field to Numpy Array first and reshape as required by sklearn
np_column = np.array(df[col1]).reshape(-1, 1)
# find max and min values ignoring NaN and INF values
np_column_max = np.ma.masked_invalid(np_column).max()
np_column_min = np.ma.masked_invalid(np_column).min() 
# replace INF and -INF with above
np_column[np_column == inf] = np_column_max
np_column[np_column == -inf] = np_column_min

# replace NaN with mean values
np_column = Imputer().fit_transform(np_column)

# obtain a unique ID for the current instance
result_id = {id}

# create new field name with unique instance ID
# and filename to save new field data
output_column = "scaled_" + col1 + "_ss_" + str(result_id)
output_filename = output_column + ".csv"
# use sklearn library to scale col1 in df, pre-processed as np_column
scaler = StandardScaler()
df[output_column] = scaler.fit_transform(np_column)
df[[output_column]].to_csv(workdir+output_filename)
print ("StandardScaler("+col1+")")
print ("#add_field:"+output_column+",N,"+output_filename)

# create new field name with unique instance ID
# and filename to save new field data
output_column = "scaled_" + col1 + "_mm_" + str(result_id)
output_filename = output_column + ".csv"
# use sklearn library to scale col1 in df, pre-processed as np_column
scaler = MinMaxScaler()
df[output_column] = scaler.fit_transform(np_column)
df[[output_column]].to_csv(workdir+output_filename)
print ("MinMaxScaler("+col1+")")
print ("#add_field:"+output_column+",N,"+output_filename)

# create new field name with unique instance ID
# and filename to save new field data
output_column = "scaled_" + col1 + "_qt_" + str(result_id)
output_filename = output_column + ".csv"
# use sklearn library to scale col1 in df, pre-processed as np_column
scaler = QuantileTransformer(n_quantiles=100)
df[output_column] = scaler.fit_transform(np_column)
df[[output_column]].to_csv(workdir+output_filename)
print ("QuantileTransformer("+col1+")")
print ("#add_field:"+output_column+",N,"+output_filename)