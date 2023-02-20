"""Module providing yes"""
import pandas as pd
import os
import sys

pd.set_option('display.max_rows', 500)
page_num = 600

#test = pd.read_parquet(f'./summary_build_data_curr_progress/build_catalog_{page_num}.parquet', engine='pyarrow')
#print(test.head(50))
#print(test.shape[0])

# navigate each dir
'''
data_dir = './summary_build_data_curr_progress'
sum_df = pd.DataFrame()

for f in os.listdir(data_dir):
    f = os.path.join(data_dir, f)
    
    if os.path.isfile(f):
        temp_df = pd.read_parquet(f, engine='pyarrow')
        sum_df = sum_df.append(temp_df)
        
sum_df.to_parquet(f'./clean_data/build_summary.parquet')
'''
'''
data_dir = './summary_build_data_curr_progress'
sum_df = pd.DataFrame()

for f in os.listdir(data_dir):
    f = os.path.join(data_dir, f)
    
    if os.path.isfile(f) and 'parquet' in f and 'build_details' in f:
        temp_df = pd.read_parquet(f, engine='pyarrow')
        sum_df = sum_df.append(temp_df)
        
sum_df.to_parquet(f'./clean_data/build_details_808.csv')

'''
'''
data_dir = './clean_data'
sum_df = pd.DataFrame()

for f in os.listdir(data_dir):
    if 'build_details' in f and 'csv' in f:
        f = os.path.join(data_dir, f)
        
        if os.path.isfile(f):
            print(f)
            temp_df = pd.read_csv(f,encoding='latin-1')
            sum_df = sum_df.append(temp_df)
        
sum_df.to_parquet(f'./clean_data/build_details_all.parquet')
'''
test = pd.read_parquet(f'./clean_data/build_details_all.parquet', engine='pyarrow')
test = test.iloc[:,[1,2,3,4,5,6]]
test = test.drop_duplicates(subset='build_id', keep="first")
test = test.reset_index(drop=True)
print(test.tail(50))
print(test.shape[0])
print(test.columns)
test.to_parquet(f'./clean_data/build_details_cleaned.parquet')
        
    # open up with pandas and append to a full table
    
    
# output catalog in parquet / json

