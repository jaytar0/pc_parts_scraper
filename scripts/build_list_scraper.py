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
import os
import sys
import time
from fake_useragent import UserAgent
from datetime import datetime
import undetected_chromedriver.v2 as uc


# Creation and Option tuning for selenium web driver for build list scraping
def list_request(main_site):
    
    try:
        # Selenium webdriver options
        options = webdriver.ChromeOptions()
        
        options.add_argument("start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--profile-directory=Default")
        options.add_argument("--user-data-dir=C:/Users/INSERT_YOUR_USER_NAME/AppData/Local/Google/Chrome/User Data")
        options.add_argument("--disable-blink-features")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Random User Agent to mimic first time user
        ua = UserAgent()
        userAgent = ua.random
        options.add_argument(f'user-agent={userAgent}')
        options.headless = True
        
        # Use driver to get webpage
        driver = webdriver.Chrome(options=options, executable_path=r'C:/Users/Taterthot/Desktop/de_project/nft_scraper/chrome_driver/win32/chromedriver.exe')
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Get site
        driver.get(main_site)

        # Random sleep to mimic human activity
        #random_sleep = random.randint(1,15)
        #print(f'sleeping for {random_sleep} seconds')
        #time.sleep(random_sleep)
        
    except NoSuchElementException:
        # Logging Error if link is broken
        logging.error('No connection established on {main_site}')
        sys.exit(1)
        
    else:
        # Logging if driver get succeeds
        logging.info("Connection Established.")
    
    # Returns selenium web driver for further usage
    return driver


# Main scraper and formatting for the lists page of pc builds
def list_scraper(driver, build_link):
    print("Yes")

      
# Operator that performs all processes for list page gathering     
def list_operator():
    # Get list of build links
    f = './clean_data/details_summary.parquet'
    
    print("Gathering build link list...")
    print("")
    
    build_summary = pd.read_parquet(f, engine='pyarrow')
    
    build_list = build_summary.build_link.tolist()
    list_df = pd.DataFrame(columns = ['build_list_id', 'component_type', 'component_name', 'component_price', 'vendor', 'watage_est'])
    
    # curr
    #entry_start = 1851
    entry_start = 0    
    # next
    #entry_start = 901co
    counter = 0
    entry_end = 100
    
    for link in build_list:
        if counter >= entry_start:
            print(f"Gathering information from: {link}")
            print(f"Counter: {counter}")
            print("")
            # Getting connection driver
            driver = list_request(link)
            
            # Scrape Details
            list_row = list_scraper(driver, link)
            print(list_row)
            list_df.loc[len(list_df)]= list_row

            if counter % 50 == 0:
                list_df.to_csv(f'./clean_data/build_list_{counter}.csv')
        
            driver.quit()
            
        counter +=1
        
    
    list_df.to_parquet(f'./clean_data/build_list_total.parquet')


