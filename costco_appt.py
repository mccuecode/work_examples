#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import smtplib
import re
from bs4 import BeautifulSoup
import time


# In[2]:


#COSTCO SHERIDAN LOCATION
bad_vodoo = 'The site is temporarily disabled. Please check back at a later time.'
url = 'https://booknow.appointment-plus.com/d0p3q2rc'
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
vodoo = soup.find_all('td')[-1].text.strip()


# In[2]:


if bad_vodoo != vodoo: 
    username = 'mccue'
    password = 'xxxxxx'
    subject = 'check your email'
    to_addr = 'markcmccue@gmail.com'
    from_addr = 'mccuepython@gmail.com' 
    message = 'https://booknow.appointment-plus.com/d0p3q2rc/appointments'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(username,password)
    newmessage = '\r\n'.join([
              'To: %s' % to_addr,
               'From: %s' % from_addr,
                'Subject: %s' %subject,
                '',
                message
                ])

    server.sendmail(from_addr, to_addr,newmessage)
    server.quit()


# In[1]:


file = open('/home/ec2-user/cron_check.txt', 'a+')
file.write("\n")
file.write("Date: {} | Time: {} | Where: {}".format(time.strftime('%x'), time.strftime('%X'), 'Costco'))
file.close()


# In[7]:


#PEPSI CENTER
url = 'https://www.primarybio.com/r/truecare24-cdphe'
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
pepsi_center = soup.find('strong').text
string_pep = 'As of now, all available appointments have been taken.'


# In[9]:


if pepsi_center != string_pep:
    username = 'mccue'
    password = 'xxxxxx'
    subject = 'check your email'
    to_addr = 'markcmccue@gmail.com'
    from_addr = 'mccuepython@gmail.com' 
    message = 'https://www.primarybio.com/r/truecare24-cdphe'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(username,password)
    newmessage = '\r\n'.join([
              'To: %s' % to_addr,
               'From: %s' % from_addr,
                'Subject: %s' %subject,
                '',
                message
                ])

    server.sendmail(from_addr, to_addr,newmessage)
    server.quit()


# In[ ]:


file = open('/home/ec2-user/cron_check.txt', 'a+')
file.write("\n")
file.write("Date: {} | Time: {} | Where: {}".format(time.strftime('%x'), time.strftime('%X'), 'Pepsi Center'))
file.close()


# In[ ]:




