import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def get_soup_by_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.content.read()
            return BeautifulSoup(content, 'html.parser')

async def extract_image_urls(artsy_url: str, max_page: int=None, delay: float=0):
    soup = await get_soup_by_url(artsy_url)
    if type(max_page) != int:
        max_page_data = soup.select_one('nav[aria-label="Pagination"]')
        max_page = int(max_page_data.select('a')[-2].contents[0])

    img_data = dict()
    for page_idx in range(1, max_page+1):
        page_url = f'{artsy_url}?page={page_idx}'
        await asyncio.sleep(delay)  # Add delay to avoid overwhelming the server
        page_soup = await get_soup_by_url(page_url)
        div_tags = page_soup.select('div[data-test="artworkGrid"]')[0]

        for img in div_tags.find_all('img'):
            img_data[img['src']] = img['alt']

    return img_data

if __name__ == '__main__':
    MONET_URL = 'https://www.artsy.net/artist/claude-monet'

    # Set the maximum number of concurrent requests and the delay between requests
    max_concurrent_requests = 5
    delay_between_requests = 0.5

    async def main():
        image_urls = await extract_image_urls(MONET_URL, max_page=5, delay=delay_between_requests)

        print(image_urls)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
