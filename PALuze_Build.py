
from sqlalchemy import create_engine, select, MetaData, Table
from db_functions import *
import time
import datetime
import random
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import urllib3
urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}


main = 'PALuze'
temp = temp_table_create(main)



#Find scrape_num, add 1 and go next range
# Need to alter build query to select by date yet convert scrape_num to int
def db_build_query_key_2(main,column_sort,column_int,count):
    import pymysql
    import datetime
    
    conn = pymysql.connect(db='cocrscom_cocrs', user='cocrscom', passwd='bA3sbSHIc3', host='qsoftserver1.qsoftdesigns.com', port=3306)
    cur = conn.cursor()
    cur.execute('''SELECT {2} FROM {0} ORDER BY {0}.{1} DESC'''.format(main,column_sort,column_int))
    go = int(cur.fetchone()[0])
    sql_sel = range(go + 1, go + count)
        
    cur.close()
    #print('Updating')
    return(sql_sel)

scrape_range = db_build_query_key_2(main,'lastUpdatedDate','scrape_num',500)
result_list = []
start_time = time.time()

try:
    for blah in scrape_range:
        url = 'https://gis.luzernecounty.org/arcgis/rest/services/PublicMap/MapServer/1/{}?f=pjson'.format(blah)
        result = requests.get(url, headers=headers).json()

        result['feature']
        parcel = result['feature']['attributes']['PIN']
        x = parcel
        assrparcel = result['feature']['attributes']['PIN']
        owner = result['feature']['attributes']['OWNER']
        if not owner:
            continue
        scrape_num = result['feature']['attributes']['OBJECTID']

        ### Manipulate the URL to pull address from elite revenue site####

        #x = '50G11S1 001012000'
        #x = '50F10SE4004123000'
        #x = '35E8S4  011011000'
        muni = x[:2]
        mapp = x[2:8]
        block = x[8:11]
        lot = x[11:14]
        improve = x[14:]
        mapp2 = mapp.strip()
        map_space = 6 - len(mapp2)
        plusses = '++++++'
        plus_fill = plusses[:map_space]
        url_fill = muni + '-' + mapp2 + plus_fill + '-' + block + '-' + lot + '-' + improve


        detail_url = 'https://eliterevenue.rba.com/taxes/luzerne/trirsp2pp.asp?parcel={}&currentlist=0&'.format(url_fill)
        detail_response = requests.get(detail_url, headers=headers, verify=False)
        detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
        situsstreet = detail_soup.find(text=" LOCATION: ").findNext('td').contents[0].strip()
        mailstreet = detail_soup.find(text=" ADDRESS: ").findNext('td').contents[0].strip()
        legal = detail_soup.find(text=" DISTRICT: ").findNext('td').contents[0].strip()
        totalassessedvalue = detail_soup.find(text=" ASSESSED VALUE:").findNext('td').contents[0].strip()

    
        result_list.append(scrape_dict(parcel=parcel, resv1=detail_url, assrparcel=assrparcel, owner=owner, legal=legal,situsstreet=situsstreet, mailstreet=mailstreet,scrape_num=scrape_num,totalassessedvalue=totalassessedvalue, active=1))

    #print(result_list)
    if result_list:
        result_list_df = pd.DataFrame(result_list)
        upsert_max(main,temp,result_list_df,'scrape_num',1)
        #upsert_load(result_list_df, main, temp)# regular upsert

    result_log_2(main, temp, 'Building', start_time)


except:
    #error_catch(main)
    print(result_list)

 
exit()
