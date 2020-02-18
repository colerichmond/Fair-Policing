import json
import pandas as pd
import os

def get_data(outpath, years):
    """
    This function creates a new directory at the location depicted
    
    by `outpath`. It also seperates the new data from the old by calling
    
    `get_table` using the `ripa` and `year`.
    
    """
    
    path = outpath

    # check if new directory already exists
    if not os.path.exists(path):
        
        os.mkdir(path)
        
    for year in years:
        
        ripa = False
                
        if year == '2019':

            ripa = True
            
        table = get_table(ripa, year)
            
        table.to_csv('data/vehicle_stops%s.csv' %(year))
            
def get_table(ripa, year):
    """
    This function creates a new directory at the location depicted
    
    by `outpath`. It also seperates the new data from the old by calling
    
    `get_table` using the `ripa` and `year`.
    
    """
    
    # check if data falls under new format
    if ripa:
        
        dfs = pd.read_csv('http://seshat.datasd.org/pd/ripa_stops_datasd_v1.csv')
        
        # get rid of irrelevant columns in the newer version of police stops data
        dfs = dfs.drop(columns=['ori', 'exp_years', 'stopduration', 'stop_in_response_to_cfs', 
                    'officer_assignment_key', 'assignment', 'intersection', 'address_block', 'land_mark', 
                    'address_street', 'highway_exit', 'isschool', 'school_name', 'address_city', 
                    'beat_name', 'pid', 'isstudent', 'perceived_limited_english', 
                    'perceived_gender', 'gender_nonconforming', 'gend_nc', 'perceived_lgbt', 'agency'])
        
        dfs = dfs.rename(columns={"beat": "service_area", 
                                  "gend": "subject_sex", 
                                  "perceived_age" : "subject_age"})
        
    else:
        
        dfs = pd.read_csv('http://seshat.datasd.org/pd/vehicle_stops_%s_datasd_v1.csv' %(year))
        
        # get rid of irrelevant columns in the older version of police stops data
        dfs = dfs.drop(columns=['stop_cause', 'subject_race', 'date_time', "sd_resident", "arrested", 
                                "searched", "obtained_consent", "contraband_found", "property_seized"])
        
    return dfs


def percent_missing(df):
    """
    This function computes the missingness by column for 
    
    the dataframe that is passed in as an argument.
    
    """
    df1 = df.drop(['obtained_consent', 'property_seized', 'contraband_found'], axis=1)
    
    missing_value_df = (df1.isnull().sum() * 100 / len(df1)).sort_values(ascending=False)
    
    return missing_value_df
