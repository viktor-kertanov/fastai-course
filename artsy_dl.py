from bs4 import BeautifulSoup
import requests
from time import sleep
from backoff import on_exception, expo
import os
from random import random, randint
import re
on_exception(expo, requests.exceptions.RequestException, max_time=60, max_tries=3)
def get_soup_by_url(url):
    req = requests.get(url)
    content = req.content
    return BeautifulSoup(content, 'html.parser')

on_exception(expo, requests.exceptions.RequestException, max_time=60, max_tries=3)
def extract_image_urls(artsy_url: str, max_page: int=None) -> dict[str]:
    soup = get_soup_by_url(artsy_url)
    if type(max_page) != int:
        max_page_data = soup.select_one('nav[aria-label="Pagination"]')
        max_page = int(max_page_data.select('a')[-2].contents[0])
    
    img_data = dict()
    for page_idx in range(1, max_page+1):
        print(f'Working on page_idx {page_idx}')
        page_url = f'{artsy_url}?page={page_idx}'
        page_soup = get_soup_by_url(page_url)
        div_tags = page_soup.select('div[data-test="artworkGrid"]')[0]

        for img in div_tags.find_all('img'):
            img_data[img['src']] = img['alt']
        sleep(3)

    return img_data

import re

def sanitize_filename(filename):
    # Define the pattern for problematic characters
    pattern = r'[<>:"/\\|?*\x00-\x1F]'

    # Replace problematic characters with an underscore
    sanitized_filename = re.sub(pattern, '_', filename)

    return sanitized_filename


on_exception(expo, requests.exceptions.RequestException, max_time=60, max_tries=3)
def download_url(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded successfully to {save_path}")
        sleep(randint(1,3)+random())
    else:
        print(f"Failed to download {url}")

def save_imgs_on_local_machine(image_urls: dict[str]):
    for img in image_urls:
        metadata = image_urls[img].lower().strip()
        splitted = metadata.split(',')
        artist = splitted[0].replace(' ', '_')
        title = splitted[1].replace(' ', '_').replace('’','').replace('‘', '')[:min(20, len(splitted[1]))]
        year = splitted[-1].replace(' ', '_')

        os.makedirs(f'{SAVE_PATH_MAIN}{artist}', exist_ok=True)
        
        filename = sanitize_filename(f'{artist}{title}{year}')
        savepath = f'{SAVE_PATH_MAIN}{artist}/{filename}.jpg'
        
        if not os.path.exists(savepath):
            download_url(img, savepath)
        else:
            print(f'File already exists: {savepath}')

if __name__ == '__main__':
    MONET_URL = 'https://www.artsy.net/artist/paul-cezanne'
    SAVE_PATH_MAIN = 'datasets/painters/'
    
    image_urls = extract_image_urls(MONET_URL, max_page=None)
    save_imgs_on_local_machine(image_urls)
