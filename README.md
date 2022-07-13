# Pioneer_Git

Example codes of python, SQL and webscraping algorythms. 

PALuze_Build.py is a program that updates ownership records nightly.  First, it uses an id from a SQL database that needs to manipulate into the proper URL pattern in order to webscrape.  Reverse engineering was done to determine the correct URL pattern in order scrape.  Records are recorded and then flipped into Pandas DataFrame to upload back to server. 

PIO_Webscrape_Ex.py is an example script for Pioneer Consulting that shows an example how using Python and webdriver to search a form in Texas counties to build multiple databases.  It uses the address field and searches on address numbers while looking at the maximum search results by page and determining when and where to end the search.  

In typical webscraping the python extension, REQUESTS, can be used to do most work.  Texas has javascript based search so an alternative method needed to be used.  

This code uses alpha characters to exhaust a search on property owner names.  And because the search is limited to finite amount of records, we add additional letters as needed. 
