# !pip install git+https://github.com/sec-edgar/sec-edgar.git
from typing import Text
from bs4 import BeautifulSoup
import bs4
from bs4.element import Comment
from selenium import webdriver
import time
import pandas as pd
import requests


# from secedgar import CompanyFilings, FilingType


from secedgar import CompanyFilings, FilingType

my_filings = CompanyFilings(cik_lookup=['aapl','xom'],
                            filing_type=FilingType.FILING_10K,
                            count=2,
                            rate_limit=1,
                            user_agent='Rohitashwa Chakraborty (rohitashwa.chakraborty@austin.utexas.edu')

my_filings.save('temp/testing')     


# tickers = ['aapl']

# start_date = '1999-01-01'
# for ticker in tickers:



print('hahah')