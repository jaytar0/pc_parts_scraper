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

# Connection Handling
# Description: Error case if the site is down for maintenence
def conn_request(main_site, select, proxy_dict):

    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--profile-directory=Default")
        options.add_argument("--user-data-dir=C:/Users/INSERT_YOUR_USER_NAME/AppData/Local/Google/Chrome/User Data")
        options.add_argument("--disable-blink-features")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("window-size=1920,1000")
        # Rand user agent
        ua = UserAgent()
        userAgent = ua.random
        print(userAgent)
        options.add_argument(f'user-agent={userAgent}')
        #options.add_argument("--user-data-dir=chrome-data")
        
        # Bypass CAPTCHA V3
        # Obtain a random single proxy from the list of proxy addresses
        #print(proxy_dict[0]["IP Address"])
        #random_proxy = proxy_dict[random.randint(0, len(proxy_dict))]
        
        # Checking Proxy Used
        #print("Using random proxy:")
        #print(f"IP: {random_proxy['IP Address']}")
        #print(f"Port: {random_proxy['Port']}")
        #print(f"Country: {random_proxy['Country']}")
        
        #full_proxy = f"{random_proxy['IP Address']}:{random_proxy['Port']}"
        #print(full_proxy)
        
        # add in proxy
        #options.add_argument('--proxy-server={}'.format(full_proxy))

        driver = webdriver.Chrome(options=options, executable_path=r'C:/Users/Taterthot/Desktop/de_project/nft_scraper/chrome_driver/win32/chromedriver.exe')
        #driver= webdriver.Chrome(options=options, executable_path='C:/Program Files (x86)/Google/Chrome/Application/chrome.exe')
        driver.get(f'{main_site}#page={select}')
        #WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
        random_sleep = random.randint(1,20)
        print(f'sleeping for {random_sleep} seconds')
        time.sleep(random_sleep)
        
    except NoSuchElementException:
        logging.error('No connection established on {select}')
        sys.exit(1)
    else:
        logging.info("Connection Established to {main_site}stats?tab={select}")
    
    return driver

# Tabling case for GME NFT Stats Page
# Description: Finds th,tr,td elements and packages them to pandas df
def table_finder(driver):
    table = pd.DataFrame()
    
    search = driver.find_elements(By.CLASS_NAME,'logGrid')
    random_sleep = random.randint(1,20)
    print(f'sleeping for {random_sleep} seconds')
    time.sleep(random_sleep)
    
    build_entries = []

    for row in search:
        
        # Get individual builds
        row_child= row.find_elements(By.CLASS_NAME, 'logGroup')

        for child in row_child:
            prop_dict = {}
            
            # splicing individual build data
            gen_row = child.text.split("\n")
            
            # get post and comment counts out
            gen_row[-2] = gen_row[-2].strip("$").replace("+",'')
            gen_row[-1] = gen_row[-1].replace(" ", "#")
            data_row = []
            [data_row.extend(delim.split("#")) for delim in gen_row]
            
            gen_row = data_row
            
            prop_dict.update({'comments':gen_row[-1]})
            prop_dict.update({'likes':gen_row[-2]})
            
            # get general properties
            prop_dict.update({'user':gen_row[0]})
            prop_dict.update({'name':gen_row[1]})
            
            build_entries.append([prop_dict['user'],prop_dict['name'],prop_dict['likes'],prop_dict['comments']])
        
        
    # make frame
    col_names = ['user','build_name', 'post_likes_count', 'post_comments_count']
    builds_df = pd.DataFrame(data= build_entries, columns = col_names)
    
    row_link = row.find_elements(By.CLASS_NAME,'logGroup__target')
    
    entry_link = []
    for link in row_link:
        entry_link.append(link.get_attribute('href'))
        
    builds_df["build_link"] = entry_link
    builds_df["build_id"] = builds_df["user"] + '_' + builds_df["build_link"].str.split("/", n = -1, expand = False).str[-1]
    
    random_sleep = random.randint(1,20)
    print(f'sleeping for {random_sleep} seconds')
    time.sleep(random_sleep)
    
    driver.quit()
    return builds_df

# Proxy random
def get_free_proxies():
    driver = webdriver.Chrome(executable_path=r'C:/Users/Taterthot/Desktop/de_project/ppc_scraper/chrome_driver/win32/chromedriver.exe')
    
    #driver.get('https://sslproxies.org')
    driver.get('https://hidemy.name/en/proxy-list/')
    table = driver.find_element(By.TAG_NAME, 'table')
    thead = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')
    tbody = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

    headers = []
    for th in thead:
        headers.append(th.text.strip())
    print(headers)

    proxies = []
    for tr in tbody:
        proxy_data = {}
        tds = tr.text.split("\n")
        prox_main = tds[0].split(" ")

        proxy_data.update({'IP Address':prox_main[0]})
        proxy_data.update({'Port':prox_main[1]})
        
        if len(prox_main) <= 2:
            proxy_data.update({'Country':'NA'})
        else:
            proxy_data.update({'Country':prox_main[2]})
        proxies.append(proxy_data)

    return proxies

