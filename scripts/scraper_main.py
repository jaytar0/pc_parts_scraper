# Selenium Packages
from matplotlib import test
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy


# Typical Packages
import random
import requests
import argparse
import logging
import pandas as pd
import numpy as np
import datetime
import os
import sys
import time
from fake_useragent import UserAgent

# custom packages
from build_summary_scraper import *
from build_details_scraper import *
from build_list_scraper import *

# User Arguments and Scraper Options
# Description: To be added to in future projects
def user_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--time', type=str, required=False, help='Use 24hr, 7d, 30d data options')
    parser.add_argument('-o', '--option', type=int, required=False, help='1 = build parser, 2 = details parser, 3 = list parser')
    return parser.parse_args()


# Default Web Parser
# Description: Using bs4, and parsing on top 50 collections per time frame
def web_parser(main_site, u_input):
    
    # Get list of random proxies usable for scraping
    # Notes: Unused in testing phase
    #proxy_dict = get_free_proxies()
    
    # Scrape builds off the main page
    if u_input.option == 1:
        
        # Required vars
        summary_table = pd.DataFrame()  # Temporary dataframe for storage
        page_start = 1                  # Custom variable for start page
        page_end = 600                  # Custom variable for end page
        proxy_dict = {}                 # Dictionary of proxies
        
        # Grab data from each page
        for page_num in range(page_start, page_end + 1):
            
            logging.info(f"Processing page: {page_num}")
            
            # Requesting connection via selenium
            build_conn = conn_request(main_site, str(page_num), proxy_dict)
            
            # Parsing Elements out into table
            build_data = table_finder(build_conn)
            summary_table = summary_table.append(build_data)
            logging.info(f"Page progress {page_num} : complete.")
            
            # Partition to 50 pages per file incase captcha stops the script
            if page_num % 50 == 0:
                logging.info(f"Sending build_catalog_{page_num}.parquet to build catalog")
                summary_table.to_parquet(f'./summary_build_data/build_catalog_{page_num}.parquet')
                summary_table = pd.DataFrame()
                
                
    # Scraping general details of individual builds
    # Description: Scraping general details of the build and the link to the parts list
    elif u_input.option == 2:
        details_operator()
    
    # Scraping list data of components from builds
    # Description: All component details, price, vendor are grabbed from the table on this page
    elif u_input.option == 3:
        list_operator()
        
        
    # List Scraper
    # Description: Scraping individual components of the build and their details
    elif u_input.option == 3:
        
        build_list = pd.DataFrame()
        
        

    # Temp Exit Clause
    sys.exit(1)
     
    
# Main Parser Call
def main(u_input):
    main_site = "https://pcpartpicker.com/builds/"
    
    # Creating logging in debug folder

    if os.path.exists("./debug"):
        os.system("rm -rf debug")    
           
    os.mkdir('debug')

    logging.basicConfig(level=logging.INFO, filename='./debug/parser.log')
    logging.info(f'Parsing data from {main_site}')
    
    # Creating parquet file storage per build summary table
    if u_input.option == 1:
        if os.path.exists("./summary_build_data"):
            os.system("rm -rf summary_build_data")
            
        os.mkdir('summary_build_data')   
        
    # Start the parsing process
    web_parser(main_site, u_input)

    
    
if __name__ == '__main__':
    u_input = user_args()
    main(u_input)