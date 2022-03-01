#%% Import Libraries

from email import message
from importlib.metadata import files
from time import time
from numpy import character
import pandas as pd
import sys
import os
from bs4 import BeautifulSoup
from tqdm import tqdm
from multiprocessing import Pool
import argparse
import re
import time

#%% Parse Function

def parse_file(args_list: str):
    xmlfile, mode = args_list
    company, date, form, doc_id, _ = xmlfile.split('/')[-1].split('_')
    flag = True
    response_message = None
    try:
        with open(xmlfile, 'r', encoding= 'utf-8') as fp:
            soup = BeautifulSoup(fp, "html.parser")
        
        # Text Data
        if mode != 't':
            text = soup.find_all(name= 'p')
            text = [x.get_text() for x in text]
            
            text = '\r'.join([x for x in text if not str.isspace(x)])
            text = re.sub('[ \n\t                ]+', ' ', text)

            with open(f'''output_data/txt/{xmlfile.split('/')[-1][:-5]}.txt''', 'w') as f:
                f.write(text)
        
        # Tabular Data
        if mode != 'x':
            table = soup.find_all(name= 'table')[0]
            table = table.find_all(name = 'th')
            table = [str(x)+"\n\n" for x in table if not str.isspace(str(x))]

            with open(f'''output_data/table/{xmlfile.split('/')[-1][:-5]}.xml''', 'w') as f:
                f.write('\r'.join(table))

    except Exception as e:
        response_message = str(e)
        flag = False

    return company, date, form, doc_id, flag, response_message

#%% Main Function

if __name__ == '__main__':
    file_list = []
    failed = dict()

    ## Command Line Arguments

    parser=argparse.ArgumentParser()

    parser.add_argument('-m', '--mode', type = str, default= 'x',
                    help='(t) tables; (x) text; (b) both [default = "x"]')
    parser.add_argument('-c', '--cores', type = int, 
                    help='Number of cores to use', default= os.cpu_count())
    parser.add_argument("-f", '--files', type=str, nargs='+',
                    help="space separated files/folders")
    args=parser.parse_args()

    ## -------------------

    ## Fetch files to parse

    for path in (pbar:= tqdm(args.files)):
        pbar.set_description(path)
        if os.path.isdir(path):
            file_list.extend(['/'.join([path, f]) for f in os.listdir(path) 
                        if (os.path.isfile('/'.join([path, f])) and f.endswith('.html'))])

        elif os.path.isfile(path):
            file_list.append(path)
    
    file_list = list(zip(file_list , [args.mode]*len(file_list) ))
    
    ## ----------------------

    print(f'\n\nNumber of cores used: {args.cores}\n')
    print(f'Number of files found: {len(file_list)}\n')
    
    ## Parse Files

    with Pool(args.cores) as proc_pool:
        with tqdm(total=len(file_list)) as pbar:
            for details in proc_pool.imap_unordered(parse_file, file_list):
                company, date, form, doc_id, flag, response_message = details
                pbar.set_description(f'Processing form:{form}, Ticker:{company}; dated: {date}')
                pbar.update()
                if not flag:
                    failed['_'.join([company, date, form, doc_id])] = response_message
    if len(failed) > 0:
        print("Unable to Parse the following docs:")
        [print(key,":", failed[key]) for key in failed]
    with open('failed_docs.txt','w') as f:
        f.write('\r'.join(failed))

    ## ----------------------

    print("\n")
    