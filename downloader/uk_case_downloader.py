import os.path
import sys
import time

import requests as requests
from tqdm import tqdm

import util.download_helper

from bs4 import BeautifulSoup
from pathlib import Path

base_path = 'https://caselaw.nationalarchives.gov.uk'

court_links = util.download_helper.national_archives_court_links
tribunal_links = util.download_helper.national_archives_tribunal_links
links = [court_links, tribunal_links]


def extract_judgments(html_page):
    judgments = html_page.find_all("span", attrs={"class": "judgment-listing__title"})
    for judgment in judgments:
        judgment_link = judgment.findNext('a')
        href = judgment_link['href'].split("?")[0]  # take the first part of the link without params
        xml_url = f'{base_path}{href}/data.xml'
        xml = requests.get(xml_url, allow_redirects=True, headers={"User-Agent": "Chrome/102.0.0.0"})
        xml_page = BeautifulSoup(xml.content, "xml")
        link_split = href.split('/')
        doc_name = f'{link_split[-1]}.xml'  # document name
        folder_path = '/'.join(link_split[:len(link_split) - 1])  # folder path

        if not os.path.exists(f'data/uk{folder_path}'):
            path = Path(f'data/uk{folder_path}')
            path.mkdir(parents=True, exist_ok=True)
        with open(f'data/uk{folder_path}/{doc_name}', "w", encoding="utf-8") as file:
            file.write(xml_page.prettify())
        time.sleep(0.2)


def run():
    for down_links in links:
        for key, link in down_links.items():
            URL = f'{base_path}{link}'
            payload = requests.get(URL, allow_redirects=True, headers={"User-Agent": "Chrome/102.0.0.0"})
            html_page = BeautifulSoup(payload.content, "html.parser")
            print(f'download started for {key}')
            extract_judgments(html_page)
            pagination_links = html_page.find_all('a', attrs={'class': 'pagination__page-link'})
            if len(pagination_links) > 0:
                last_page = int(pagination_links[-1]['href'].split('page=')[1])
            else:
                last_page = 1
            if last_page > 1:
                for i in tqdm(range(2, last_page + 1)):
                    URL = f'{URL}&page={i}'
                    payload = requests.get(URL, allow_redirects=True, headers={"User-Agent": "Chrome/102.0.0.0"})
                    html_page = BeautifulSoup(payload.content, "html.parser")
                    extract_judgments(html_page)
            print(f'download ended for {key}')

if __name__ == '__main__':
    run()
