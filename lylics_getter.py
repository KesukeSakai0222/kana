import requests
from bs4 import BeautifulSoup
import bs4
import pandas as pd
import time
import re
from datetime import datetime
from typing import List, Any
from logging import getLogger

# consts
COLUMNS = ['曲名', '歌詞', '作曲者', '作詞者','発売日', 'URL']
ROOT_URL = 'https://www.uta-net.com/artist/9639/'
BASE_URL = 'https://www.uta-net.com'

# logger
logger = getLogger(__name__)

def get_urls() -> List[str]:
    logger.info('start getting urls')
    html = requests.get(ROOT_URL)
    soup = BeautifulSoup(html.text, 'html.parser')

    urls = []
    list = soup.find_all('tr', attrs={'class', 'border-bottom'})
    for line in list:
        if line.a == None:
            continue
        urls.append(BASE_URL + line.a.get('href'))
    time.sleep(1)

    logger.info('end getting urls')
    return urls

def get_data(urls: List[str]) -> List[List[Any]]:
    logger.info('start getting data')
    data = []
    for u in urls:
        html = requests.get(u)
        soup = BeautifulSoup(html.text, 'html.parser')

        title = soup.h2.contents[0]
        lylics = []
        for lylic in soup.select('#kashi_area')[0].contents:
            if type(lylic) is bs4.element.Tag:
                continue
            lylics.append(lylic.replace('\u3000', ' '))
        detail = soup.find_all('p', class_='detail')[0]
        lyricist = detail.find_all('a')[0].contents[0]
        composer = detail.find_all('a')[1].contents[0]
        release = datetime.strptime(re.search(r'\d{4}/\d{2}/\d{2}', detail.text).group(), '%Y/%m/%d').date()
        data.append([title, ' '.join(lylics), lyricist, composer, release, u])
        time.sleep(1)

    logger.info('end getting data')
    return data

def output(data: List[List[Any]]):
    logger.info('start output data')
    df = pd.DataFrame(data, columns = COLUMNS)
    df.to_csv('./data/lylics.csv', index=False)
    logger.info('end output data')

def main():
    logger.info('start main')

    urls = get_urls()
    data = get_data(urls)
    output(data)

    logger.info('end main')

if __name__ == "__main__":
    main()
