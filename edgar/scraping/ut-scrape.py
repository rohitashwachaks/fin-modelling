# !pip install git+https://github.com/sec-edgar/sec-edgar.git
# ! pip install -i https://test.pypi.org/simple/ ut-msba-edgar-scraper

import os

from ut_msba_edgar_scraper import Downloader
import ut_msba_edgar_scraper

import argparse
import datetime


if __name__ == "__main__":
    file_list = []
    failed = dict()

    ## Command Line Arguments

    parser=argparse.ArgumentParser()

    parser.add_argument('-t', '--tickers', type = str, default= None,
                    help='space separated tickers')
    parser.add_argument('-e', '--end_date', type = str, 
                    help='End Date YYYMMDD', default= datetime.datetime.now().strftime('%Y%m%D'))
    parser.add_argument("-o", '--output', type=str, default= 'temp',
                    help="output folder path")
    args=parser.parse_args()

    ## -------------------
    # datetime.datetime.fromisoformat(args.end_date).strftime('%Y-%d-%m')
    # print(datetime.datetime.fromisoformat(args.end_date).strftime('%Y-%d-%m'))

    if args.tickers:
        tic_list = args.tickers.split(' ')
        company_filings = CompanyFilings(cik_lookup= tic_list,
                                            filing_type= FilingType.FILING_10K,
                                            count=5,
                                            rate_limit=1,
                                            end_date = args.end_date,
                                            user_agent='Rohitashwa Chakraborty (rohitashwa.chakraborty@austin.utexas.edu')
        company_filings.save(args.output)
        company_filings = CompanyFilings(cik_lookup= tic_list,
                                            filing_type= FilingType.FILING_10Q,
                                            count=5,
                                            rate_limit=1,
                                            user_agent='Rohitashwa Chakraborty (rohitashwa.chakraborty@austin.utexas.edu')
        company_filings.save(args.output)
        

# # start_date = '1999-01-01'