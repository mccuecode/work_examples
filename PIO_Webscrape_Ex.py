#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Load dependences 

import time
import bs4, selenium, smtplib, time
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from sqlalchemy import create_engine, select, MetaData, Table
import pandas as pd
from datetime import date
import string
import random
import re
import pickle
from db_functions import *


# In[4]:


import pymysql

# Establish connections to SQL databases 
conn = pymysql.connect(db='cocrs', user='user', passwd='xxxxxx', host='qsoftserver1.com', port=3306)
cur = conn.cursor()
engine = create_engine("mysql+pymysql://cocrscom:xxxxxxz@cocrs.com/")
table_schema = scrape_schema()


# In[3]:





# In[5]:


#Load the Texas CID and full county names. this list was made from Requests Scrape looking for CID matches
cleantex = pickle.load(open('cleantex', 'rb'))
print(cleantex)


# In[7]:


#Seperate the lists based on CID and County
cid = []
county = []

for x, y in cleantex:
    cid.append(x)
    county.append(y)

#Create Database Shortnames for COCRS DB's
texdb_name = []
for x,y in cleantex:
    texdb_name.append('TX' + str(y)[:4])

#Account for duplicates in the event of database shortname
dups = {}

for i, val in enumerate(texdb_name):
    if val not in dups:
        # Store index of first occurrence and occurrence value
        dups[val] = [i, 1]
    else:
        # Special case for first occurrence
        if dups[val][1] == 1:
            texdb_name[dups[val][0]] += str(dups[val][1])

        # Increment occurrence value, index value doesn't matter anymore
        dups[val][1] += 1

        # Use stored occurrence value
        texdb_name[i] += str(dups[val][1])
    
# Clean up the County names to eliminate spaces 
texdb_name = [x.strip()for x in texdb_name]    
    
#Zip the lists
texas = list(zip(cid, county, texdb_name))
print(texas)


# In[2]:


# WEBSCRAPE Function FOR TRUEAUTOMATION 
def true_auto():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    table_body = soup.find('table', {'id':'propertySearchResults_resultsTable'})
    rows = table_body.find_all('tr')
    data_rows = rows[1:-1]
    
    for x in data_rows:
        data = x.find_all('td')
        parcel = data[1].get_text()
        resv6 = data[3].get_text()
        legal = data[5].get_text()#owner
        situsstreet = data[4].get_text().replace('\n', '')#situsstreet
        schedule = data[2].get_text()
        owner = data[6].get_text()
        props.append(scrape_dict(resv6=resv6,treasacct=parcel, scrape_num=parcel, parcel=parcel,owner=owner,schedule=schedule,situsstreet=situsstreet,legal=legal))


# In[38]:


# FOR ADVANCED SEARCH TEST TO NOT TIMEOUT

# #Click button to Advanced Search
# driver.find_element_by_xpath('//*[@id="propertySearchOptions_advanced"]').click()

# #Insert Street number
# street_num = driver.find_element_by_xpath('//*[@id="propertySearchOptions_streetNumber"]')
# street_num.send_keys('1')

# #Select by REAL
# driver.find_element_by_xpath("//*[@id='propertySearchOptions_propertyType']/option[text()='Real']").click()

# # Click Search Button
# driver.find_element_by_xpath('//*[@id="propertySearchOptions_searchAdv"]').click()


for a, b, c in testtex:
    cid = a
    dbname = c
    
    props = []
    url = 'https://propaccess.trueautomation.com/clientdb/Property.aspx?cid={}'.format(cid)

    #LOADS TRUEAUTO
    options = Options()
    options.add_argument("start-maximized")
    #options.headless = True
    #driver = webdriver.Chrome(options=options, executable_path='/Users/markmccue/Desktop/chromedriver')
    driver = webdriver.Chrome(options=options, executable_path='C:/Users/markm/Desktop/chromedriver')
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(ec.element_to_be_clickable((By.ID, 'header_PropertySearch')))
    #Click button to Advanced Search
    driver.find_element_by_xpath('//*[@id="propertySearchOptions_advanced"]').click()
    wait.until(ec.element_to_be_clickable((By.ID, 'header_PropertySearch')))

    # SEARCH ON DIGIT IN RANGE
    for y in range(9):
        numbersearch = driver.find_element_by_xpath('//*[@id="propertySearchOptions_streetNumber"]')
        numbersearch.send_keys(y)
        #Select by REAL
        driver.find_element_by_xpath("//*[@id='propertySearchOptions_propertyType']/option[text()='Real']").click()
        # Click Search Button
        driver.find_element_by_xpath('//*[@id="propertySearchOptions_searchAdv"]').click()
    
        wait.until(ec.element_to_be_clickable((By.ID, 'header_PropertySearch')))

        soup = BeautifulSoup(driver.page_source, "html.parser")
        try:
            paging = soup.find('td',{'class':'paging'})
            page_len = len(paging)
            true_auto()
        except:
            continue 

        if page_len == 1:
            true_auto()

        if page_len > 1 and page_len < 22:
            wait.until(ec.element_to_be_clickable((By.ID, 'header_PropertySearch')))
            page_total = page_len -1
            click_range = range(2, page_total)
            
            for pagey in click_range:
                driver.get('https://propaccess.trueautomation.com/clientdb/SearchResults.aspx?cid={0}&rtype=address&page={1}'.format(cid,pagey))
                wait.until(ec.element_to_be_clickable((By.ID, 'header_PropertySearch')))
                soup = BeautifulSoup(driver.page_source, "html.parser")
                true_auto()
                time.sleep(.2)

        if page_len == 22:
            wait.until(ec.element_to_be_clickable((By.ID, 'header_PropertySearch')))
            # TXColo when it looked for 7 in search, it lost a normal tr, so im subtracting it down to 26 instead of 27
            try:
                page_total = driver.find_element_by_xpath('//*[@id="propertySearchResults_resultsTable"]/tbody/tr[27]/td/a[11]')
            except:
                page_total = driver.find_element_by_xpath('//*[@id="propertySearchResults_resultsTable"]/tbody/tr[26]/td/a[11]')
            
            click_range = range(2, int(page_total.text) + 1)

            for pagey in click_range:
                driver.get('https://propaccess.trueautomation.com/clientdb/SearchResults.aspx?cid={0}&rtype=address&page={1}'.format(cid,pagey))
                wait.until(ec.element_to_be_clickable((By.ID, 'header_PropertySearch')))
                soup = BeautifulSoup(driver.page_source, "html.parser")
                true_auto()
                time.sleep(.2)
        
        wait.until(ec.element_to_be_clickable((By.ID, 'header_PropertySearch')))
        
        driver.get(url)
        
        wait.until(ec.element_to_be_clickable((By.ID, 'header_PropertySearch')))

        driver.find_element_by_xpath('//*[@id="propertySearchOptions_advanced"]').click()


    
    df = pd.DataFrame(props)

    df2 = df.drop_duplicates(subset=['treasacct'], keep='last')

    
    
    time.sleep(2)
    cur.execute('''CREATE TABLE {} LIKE AA_scrapeDBtemplate'''.format(dbname))
    
    time.sleep(2)
    
    df2.to_sql(dbname, con=engine, if_exists = 'append', chunksize = 1000, method='multi', index=False, dtype=table_schema)

driver.close()




######### END THE EXAMPLE CODE#######

