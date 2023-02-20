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

# Connection Handling
# Description: Error case if the site is down for maintenence
def details_request(main_site):
    try:
        # Selenium webdriver options
        
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("--disable-extensions")
        
        options.add_argument("--profile-directory=Default")
        options.add_argument("--user-data-dir=C:/Users/INSERT_YOUR_USER_NAME/AppData/Local/Google/Chrome/User Data")
        options.add_argument("--disable-blink-features")
        options.add_argument('--disable-blink-features=AutomationControlled')
        #options.add_argument("window-size=1920,1000")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Rand user agent
        ua = UserAgent()
        userAgent = ua.random
        print(userAgent)
        options.add_argument(f'user-agent={userAgent}')
        options.headless = True
        
        # Use driver to get webpage
        driver = webdriver.Chrome(options=options, executable_path=r'C:/Users/Taterthot/Desktop/de_project/nft_scraper/chrome_driver/win32/chromedriver.exe')
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # undectected way
        #driver = uc.Chrome()
        #options = uc.ChromeOptions()
        #options = webdriver.ChromeOptions() 
        #options.headless = True
        #driver = uc.Chrome(options=options)
        
        #options.user_data_dir = "/Users/Taterthot/Desktop/de_project/nft_scraper/profile"
        #driver = uc.Chrome(options=options, version_main=94)
        driver.get(main_site)

        random_sleep = random.randint(1,15)
        print(f'sleeping for {random_sleep} seconds')
        #time.sleep(random_sleep)
        
    except NoSuchElementException:
        logging.error('No connection established on {select}')
        sys.exit(1)
    else:
        logging.info("Connection Established.")
    
    return driver

def details_scraper(driver, build_link):

    random_sleep = random.randint(1,15)
    print(f'sleeping for {random_sleep} seconds')
    #time.sleep(random_sleep)
    try:
        driver.find_element(By.CLASS_NAME,'user')

    except NoSuchElementException:
        try:
            driver.find_element(By.CLASS_NAME,'g-recaptcha')
        except NoSuchElementException:
            print("captcha reached")
            sys.exit(1) 
        return ['NA', 'NA', 'NA', 'NA', 'NA', 'NA']
            
    table_id = build_link.split("/")[-1]
    details_entry = {}
    
    # build_id
    # Class: user
    # Tag: div, a, href
    element_id = driver.find_element(By.CLASS_NAME,'user')
    username = element_id.find_elements(By.TAG_NAME, 'a')
    
    for link in username:
        temp_id = link.get_attribute('href').split("/")
        while '' in temp_id:
            temp_id.remove('')
            
        details_entry.update({'build_id':f'{temp_id[-1]}_{table_id}'})
    
    # build_list_link
    # Class: header-actions
    # Tag: a, href
    
     # build_list_id
    # Make id from last few + author
    element_id = driver.find_element(By.CLASS_NAME,'header-actions')
    list_link = element_id.find_elements(By.TAG_NAME, 'a')
   
    for link in list_link:
            temp = link.get_attribute('href')
            details_entry.update({'build_list_link':f'{temp}'})
            temp_list_id = temp.split("/")[-1]
            details_entry.update({'build_list_id':f'{temp_id[-1]}_{temp_list_id}'})


    # build_date
    # Class order: group, group__title, group__content
    # Tag order: div h4 div
    # Have to look for date published, since the other one is too similar
    element_id = driver.find_elements(By.CLASS_NAME,'group__content')

    for field in element_id:
        
        if '.' in field.text and ',' in field.text and '20' in field.text:
            
            if 'build_date' not in details_entry.keys():
                temp_field = field.text
                temp_field = temp_field.replace("Sept", "sep")
                temp_date = datetime.strptime(temp_field, "%b. %d, %Y")
                
                details_entry.update({'build_date':temp_date})

    # description
    # Class order: description block, markdown
    # Tag order: div, div
    # Get this as one long string
    element_id = driver.find_elements(By.CLASS_NAME,'description')
    total_descript = ''
    for text in element_id:
        total_descript += text.text
        
    details_entry.update({'description':total_descript.replace("\n", " ")})
    
    # build_cost
    # Price Class: tr__total tr__total--grandtotal
    # Tag: td_price
    element_id = driver.find_elements(By.CLASS_NAME,'tr__total')

    for price in element_id:
        if 'build_cost' not in details_entry.keys():

            build_price = price.text.replace('$', '')
            build_price = build_price.replace("TOTAL: ", '')
            build_price = build_price.replace("Subtotal: ", '')
            build_price = build_price.replace(' ', '')
            
            details_entry.update({'build_cost':float(build_price)})
            
    if 'build_date' not in details_entry.keys():
        details_entry.update({'build_date':datetime(2022, random.randint(1,12), random.randint(1,28))})
        
    return [details_entry['build_id'], details_entry['build_list_id'], details_entry['build_list_link'] , details_entry['build_date']\
         , details_entry['build_cost'], details_entry['description']]
    
def details_operator():
    # Get list of build links
    f = './clean_data/build_summary.parquet'
    
    print("Gathering build link list...")
    print("")
    
    build_summary = pd.read_parquet(f, engine='pyarrow')
    
    build_list = build_summary.build_link.tolist()
    details_df = pd.DataFrame(columns = ['build_id','build_list_id', 'build_list_link', 'build_date', 'build_cost', 'description'])
    
    # curr
    #entry_start = 1851
    entry_start = 2201    
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
            driver = details_request(link)
            
            # Scrape Details
            details_row = details_scraper(driver, link)
            
            print(details_row)
            details_df.loc[len(details_df)]= details_row
            random_sleep = random.randint(1,15)
            print(f'sleeping for {random_sleep} seconds')
            #time.sleep(random_sleep)
            if counter % 50 == 0:
                details_df.to_csv(f'./clean_data/build_details_{counter}.csv')
        

            driver.quit()
        counter +=1
        
    
    details_df.to_parquet(f'./clean_data/build_details_total.parquet')
    
        