#start_of_parameters
#key=input_json;  type=constant;  value=enter_input_json
#key=meta_json;  type=constant;  value=enter_meta
#key=predictor_agent;  type=constant;  value=ev_agent_11111
#key=debug_out;  type=constant;  value=0
#end_of_parameters

global DEBUG
DEBUG     = {debug_out}
res_agent = {predictor_agent}
    
import pandas as pd
import json

import gc
gc.collect()

def printlog(mesg):
    from datetime import datetime
    global DEBUG
    if DEBUG == 1:
        print (str(datetime.now()), mesg)

try:    
    json_data = json.loads("""{input_json}""")
    printlog ('Data JSON received')

    meta_data    = json.loads("""{meta_json}""")
    printlog ('Meta Data JSON received')

    scoring_meta = meta_data["scoring_meta"]

    df_add = pd.DataFrame().from_dict(json_data["training_data"])
    printlog (df_add)
    if DEBUG == 1:
        df_add.to_csv(workdir + str(res_agent) + '_debug.csv')
        printlog ('live debug data file saved')
    
    i = 0
    # apply each required agent on df_add which will be extended by each agent until it reaches return_column
    for agent in agents:
        i+=1
        printlog ("applying agent " + str(i) + " " + str(agent))    
        agent.apply(df_add)
        printlog (df_add)
        # convert all spurious text into numeric as after the 1st agent all fields should be numeric or NaN
        # this should be applied after the 1st agent i.e., after all dictionaries have been created
        if i==1:
            df_add = df_add.apply(pd.to_numeric, errors='coerce')

    # select the app id and score
    output_columns = [scoring_meta["output_primary_field"]]
    output_columns.extend(scoring_meta["return_columns"])
    out_df = df_add[output_columns]
    printlog ( "Output columns:" )
    printlog ( output_columns )
    
    out_json = out_df.to_json(orient='records')
    print('#result1=', out_json)
except Exception as e:
    print('#result1={"error":"'+str(e)+'"}')
