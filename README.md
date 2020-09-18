# SEC Scraper  
Python repo to scrape data from the SEC's [EDGAR database]()(https://www.sec.gov/edgar.shtml). Currently configured to pull Form 3 and Form 4 (changes in beneficial ownership of securities), but can be changed to pull arbitrary forms and data. 

# Dependencies 
* BeautifulSoup4 
* Pandas / Numpy 

# Rate-Limiting 
The SEC asks that developers restrict their web crawling to 10 requests a second. While this can slow down the scraper, not doing so will get you temporarily blocked from the site. The code for this is in https://github.com/hmcguinn/secScraper/blob/a40ec6b4d088f6ab6279b545cc42b34ec9683478/multiThreading/opensPerSecond.py
