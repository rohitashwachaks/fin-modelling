from time import time
import pandas as pd
import sys
import os
from bs4 import BeautifulSoup
from tqdm import tqdm
from multiprocessing import Pool

import re
import time

def parse_file(xmlfile: str):
    company, date, form, doc_id, _ = xmlfile.split('/')[-1].split('_')
    flag = True
    try:
        with open(xmlfile, 'r', encoding= 'utf-8') as fp:
            soup = BeautifulSoup(fp, "html.parser")
        
        # Text Data
        text = soup.find_all(name= 'p')
        text = [x.get_text() for x in text]
        text = '\r'.join([x for x in text if not str.isspace(x)])
        text = re.sub('[ \n\t                ]+', ' ', text)

        with open(f'''output_data/txt/{xmlfile.split('/')[-1][:-5]}.txt''', 'w') as f:
            f.write(text)
        
        # Tabular Data
        # table = soup.find_all(name= 'table')
        # table = [x.get_text() for x in table]

        # with open(f'''output_data/table/{xmlfile.split('/')[-1][:-5]}.txt''', 'w') as f:
        #     f.write('\r'.join(table))
    except:
        flag = False

    return company, date, form, doc_id, flag

if __name__ == '__main__':
    file_list = []
    failed = []

    for path in (pbar:= tqdm(sys.argv[1:])):
        pbar.set_description(path)
        if os.path.isdir(path):
            file_list.extend(['/'.join([path, f]) for f in os.listdir(path) if (os.path.isfile('/'.join([path, f])) and f.endswith('.html'))])
        elif os.path.isfile(path):
            file_list.append(path)
    
    cores = os.cpu_count()
    print(f'\n\nNumber of cores used: {cores}\n')
    
    with Pool(cores) as proc_pool:
        with tqdm(total=len(file_list)) as pbar:
            for details in proc_pool.imap_unordered(parse_file, file_list):
                company, date, form, doc_id, flag = details
                pbar.set_description(f'Processing form:{form}, Ticker:{company}; dated: {date}')
                pbar.update()
                if not flag:
                    failed.append('_'.join([company, date, form, doc_id]))
    print("Unable to Parse the following docs:")
    [print(t) for t in failed]
    with open('failed_docs.txt','w') as f:
        f.write('\r'.join(failed))
    