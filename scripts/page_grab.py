import requests
import sys
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# Repetative removal of blank entries in a list
def rm_whitespace(l):
    while '' in l:
        l.remove('')
    return l

# Getting build lists for individual builds
# Itterates over and grabs data for each
def copy_build_list(loc):

    builds = pd.read_parquet(loc, engine='pyarrow')
    builds_list = builds["build_list_link"].tolist()
    #print(len(builds_list))
    #sys.exit(1)
    #temp_stop = 0
    final_list = pd.DataFrame(columns=["build_list_id", "component_type", "component_name", "component_price"])

    for entry in builds_list:
        url = entry
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')

        entry_data = get_build_data(soup, url)
        print(url)
        final_list = final_list.append(entry_data)
        print(len(final_list["build_list_id"].unique()))

    print(final_list)
        #temp_stop += 1
        #if temp_stop == 2:
            #sys.exit(1)


# Getting an individual builds table data from the specific parts list page
def get_build_data(soup, url):
    # getting individual id out from url
    inv_id = url.split("/")[-1]
    inv_id = inv_id.replace("\n","")

    # recreating a condensed table with the planned stats for the build_list db
    individual_df = pd.DataFrame(columns=["build_list_id", "component_type", "component_name", "component_price"])

    # Iterrate through each tr-table_row element to find info
    for link in soup.find_all('tr'):
        
        # Getting text data out of the entry
        link = link.text.split("\n")
        link = rm_whitespace(link)

        # default row entry
        comp_row = ['NA', 'NA', 'NA', 'NA']

        # Missing or weird price information
        if len(link) == 9:
            comp_row = [inv_id, link[0], link[1], 'NA']

        # Regular format with all information provided
        if len(link) == 10:
            comp_row= [inv_id, link[0], link[1], link[-3].replace('$','')]
        
        # slate to list
        if comp_row != ['NA', 'NA', 'NA', 'NA']:
            individual_df.loc[len(individual_df.index)] = comp_row 

    return individual_df

if __name__ == "__main__":
    #static data source
    build_details_link = './clean_data/build_details_all.parquet'
    copy_build_list(build_details_link)
