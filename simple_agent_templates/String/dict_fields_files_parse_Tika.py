#start_of_parameters
#key=fields_source;  type=constant;  value=['dict_field|dict_field.csv']
#key=col_max_length;  type=constant;  value=200
#key=new_field_prefix;  type=constant;  value=files_parsed_Tika_
#key=field_prefix_use_source_names;  type=constant;  value=True
#key=include_columns_type;  type=constant;  value=is_dict_only
#key=include_columns_containing;  type=constant;  value=
#key=ignore_columns_containing;  type=constant;  value='%ev_field%' and '%onehe_%'
#end_of_parameters

# AICHOO OS Simple Agent
# Documentation about AI OS and how to create Simple Agents can be found on our WiKi
# https://github.com/eghamtech/AIOS/wiki/Simple-Agents
# https://github.com/eghamtech/AIOS/wiki/AI-OS-Introduction
#
# this agent creates new column from given field by reading its text content
# and assuming each row is a path to a file,
# it then parses such file using Tika and parsed text is saved as new dict column
#

import warnings
warnings.filterwarnings("ignore")
import gc
gc.collect()

import pandas as pd
import numpy  as np
import os.path, bz2, pickle, re
import tika

from datetime import datetime

class cls_agent_{id}:
    data_defs = {fields_source}

    # obtain a unique ID for the current instance
    result_id         = {id}
    # create new field name based on "new_field_prefix" with unique instance ID
    # and filename to save new field data
    new_field_prefix              = "{new_field_prefix}"
    field_prefix_use_source_names = {field_prefix_use_source_names}

    col_max_length    = {col_max_length}
    agent_name        = 'agent_' + str(result_id)    
 
    def is_set(self, s):
        return len(s)>0 and s!="0"

    def make_dict(self, col):
        a1 = col.unique()
        a1 = [x for x in a1 if str(x) != 'nan']
        keys1 = range(1, len(a1)+1)
        return dict(zip(a1, keys1))

    def __init__(self):
        #if not self.is_set(self.data_defs):
        #    self.data_defs = ["{_random_dict_distinct}", "{_random_dict_distinct}"]
        tika.initVM()

        if self.field_prefix_use_source_names:                   
            # concatenate all source column names into new field prefix
            col_max_length = int(200 / len(self.data_defs))            # allow 200 characters max combined col name length
            for i in range(0,len(self.data_defs)):
                col_name = self.data_defs[i].split("|")[0]
                col_name = col_name[:col_max_length]                   # only take first col_max_length chars from each column
                self.new_field_prefix = self.new_field_prefix + '_' + col_name

        self.new_col_name = self.new_field_prefix + '_' + str(self.result_id)


    def run_on(self, df_run, apply_fun=False):        
        df_new         = []
        block_progress = 0
        total          = len(df_run)
        block          = int(total/50)

        col_name  = self.data_defs[0].split("|")[0]

        for i, rowTuple in enumerate(df_run[[col_name]].itertuples(index=False)):
            sfile = rowTuple[0]

            parsed_file = {}
            if os.path.isfile(sfile):
                parsed_file = tika.parser.from_file(sfile)            # read the file and parse it  
            else:
                parsed_file = tika.parser.from_buffer(sfile)          # parse the given string, if it is not a file reference
            
            df_new.append(parsed_file.get('content',''))

            block_progress += 1
            if (block_progress >= block):
                block_progress = 0
                print (str(datetime.now()), " rows processed: ", round((i+1)/total*100,0), "%")

        df_run[self.new_col_name] = df_new

                    

    def run(self, mode):
        print ("enter run mode " + str(mode))

        for i in range(0,len(self.data_defs)):
            col_name  = self.data_defs[i].split("|")[0]
            file_name = self.data_defs[i].split("|")[1]

            if i==0:
                self.df = pd.read_csv(workdir+file_name)[[col_name]]
            else:
                self.df = self.df.merge(pd.read_csv(workdir+file_name)[[col_name]], left_index=True, right_index=True)

            if os.path.isfile(workdir + 'dict_' + file_name):
                # load dictionary if it exists
                dict_temp = pd.read_csv(workdir + 'dict_' + file_name, dtype={'value': object}).set_index('key')["value"].to_dict()

                self.df[col_name] = self.df[col_name].map(dict_temp)


        self.run_on(self.df)
        nrow = len(self.df)

        # save and register each new column    
        fld   = self.new_col_name
        fname = fld + '.csv'

        fld_dict     = self.make_dict(self.df[fld].fillna(''))         # create dictionary of given text column  
        self.df[fld] = self.df[fld].fillna('').map(fld_dict)           # replace column values with corresponding values from dictionary

        # save dictionary for each text column into separate file
        pd.DataFrame(list(fld_dict.items()), columns=['value', 'key'])[['key','value']].to_csv(workdir+'dict_'+fld+'.csv', encoding='utf-8')

        self.df[[fld]].to_csv(workdir+fname)
        print ("#add_field:"+fld+",Y,"+fname+","+str(nrow))


    def apply(self, df_add):
        self.run_on(df_add, apply_fun=True)

agent_{id} = cls_agent_{id}()