#start_of_parameters
#key=field_source;  type=constant;  value=enter_source_field_name_with_csv_file_name
#key=field_filter;  type=constant;  value=enter_field_to_filter_by_with_csv_file_name
#key=condition;  type=constant;  value=enter_condition e.g. ==0
#key=set_value;  type=constant;  value=enter_value_to_set
#key=condition_1;  type=constant;  value=enter_condition e.g. >=1
#key=set_value_1;  type=constant;  value=enter_value_to_set
#key=set_value_2;  type=constant;  value=enter_value_to_set
#end_of_parameters

# AICHOO OS Simple Agent 
# Documentation about AI OS and how to create Simple Agents can be found on our WiKi
# https://github.com/eghamtech/AIOS/wiki/Simple-Agents
# https://github.com/eghamtech/AIOS/wiki/AI-OS-Introduction
#
# this agent creates new column which is a derivative of "field_source" but with some rows: 
# set to "set_value" where those rows in "field_filter" match "condition" 
# set to "set_value_1" where those rows in "field_filter" match "condition_1"
# set to "set_value_2" where those rows in "field_filter" match neither "condition" nor "condition_1"

class cls_agent_{id}:
    import warnings
    warnings.filterwarnings("ignore")
    
    import pandas as pd
    import numpy as np
    
    data_defs = ["{field_source}","{field_filter}"]
    new_value = {set_value}

    new_value_1 = {set_value_1}
    new_value_2 = {set_value_2}
    
    # obtain a unique ID for the current instance
    result_id = {id}
    # create new field name based on "new_field_prefix" with unique instance ID
    # and filename to save new field data
    new_field_prefix = "filter_"
    output_column = new_field_prefix + data_defs[0].split("|")[0] + "_" + str(result_id)
    output_filename = output_column + ".csv"
   
    def run(self, mode):
        print ("enter run mode " + str(mode))
        
        for i in range(0,len(self.data_defs)):
             col_name = self.data_defs[i].split("|")[0]
             file_name = self.data_defs[i].split("|")[1]
    
             if i==0:
                self.df = self.pd.read_csv(workdir+file_name)[[col_name]]
             else:
                self.df = self.df.merge(self.pd.read_csv(workdir+file_name)[[col_name]], left_index=True, right_index=True)
        
        nrow = len(self.df)
        
        #col_source = self.data_defs[0].split("|")[0]
        #col_filter = self.data_defs[1].split("|")[0]
        # in case when both "field_source" and "field_filter" are the same, column names changed in df
        col_source = self.df.columns[0]
        col_filter = self.df.columns[1]
        
        # initialise all rows with default "new_value_2"
        self.df[self.output_column] = self.new_value_2
        
        # find all rows matching "condition" and set new column for such rows to "new_value"
        self.df.loc[self.df[col_filter]{condition}, self.output_column] = self.new_value
        # find all rows matching "condition_1" and set new column for such rows to "new_value_1"
        self.df.loc[self.df[col_filter]{condition_1}, self.output_column] = self.new_value_1
       
        self.df[[self.output_column]].to_csv(workdir+self.output_filename)
        print ("#add_field:"+self.output_column+",N,"+self.output_filename+","+str(nrow)+",N")

        
    def apply(self, df_add):
        col_source = self.data_defs[0].split("|")[0]
        col_filter = self.data_defs[1].split("|")[0]
        
        df_add[self.output_column] = self.new_value_2
        df_add.loc[df_add[col_filter]{condition}, self.output_column] = self.new_value
        df_add.loc[df_add[col_filter]{condition_1}, self.output_column] = self.new_value_1
       

agent_{id} = cls_agent_{id}()
