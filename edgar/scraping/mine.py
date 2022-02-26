import xml.etree.ElementTree as ET
import sys
from bs4 import BeautifulSoup


def parse_file(xmlfile: str):
    # create element tree object
    with open(xmlfile) as fp:
        soup = BeautifulSoup(fp, "html.parser")
    # tree = ET.parse(xmlfile)
    print(len([x for x in soup.children]))
    # [print(index, x,"\n") for index, x in enumerate(soup.children) if index < 1]
    return type(soup)

if __name__ == '__main__':
    print('command line arguments are:',sys.argv[1:])
    print(parse_file('./temp/testing/aapl/10-K/0000320193-20-000096.txt'))