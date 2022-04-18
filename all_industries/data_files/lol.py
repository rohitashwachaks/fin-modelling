import pandas as pd
import numpy as np
from tqdm import tqdm
import os
import sys
from multiprocessing import Pool

import warnings
warnings.filterwarnings("ignore")

tqdm.pandas()
import re
import multiprocessing as mp

def get_mdna(s: str) -> str:
    if pd.isna(s):
        return None
        
    matches = re.findall(r'(?i)MANAGEMENT\'?S? DISCUSSION(?i).*(?i)ITEM[ ]{0,2}\d(?i)', s, re.DOTALL)
    if len(matches) == 1:
        s = matches[0]
    # take the last set of discusion text
    elif len(matches) > 1:
        s = matches[-1]
    return s


def process_text(df: pd.DataFrame) -> pd.DataFrame:
    # print(mp.current_process().name, 'starting')
    df['text'] = df['text'].apply(get_mdna)
    # df.dropna(subset=['text'], inplace=True).reset_index(drop=True)
    return df
    
if __name__ == '__main__':
    text_reader = pd.read_csv('all_text.csv', 
                    chunksize=1000,
                    index_col= 'Unnamed: 0'
                )

    if os.path.exists('all_text_mdna.csv'):
        os.remove('all_text_mdna.csv')
        print('removed all_text_mdna.csv')


    with tqdm() as pbar:
        with Pool(os.cpu_count()) as p:
            for index, chunk in enumerate(p.imap(process_text, text_reader),1):
                pbar.update()
                if os.path.exists('all_text_mdna.csv'):
                    pbar.set_description(f'Appending chunk {index} to \'all_text_mdna.csv\'')
                    chunk.to_csv('all_text_mdna.csv', mode='a', header=False, index=False)
                else:
                    pbar.set_description(f'Creating file \'all_text_mdna.csv\' with chunk {index}')
                    chunk.to_csv('all_text_mdna.csv', index=False, header=True)
    print('done')