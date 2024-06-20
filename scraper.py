# Web scraping logic

import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    image = soup.find('img')
    image_url = image['src'] if image else 'default_image_url'
    title = soup.find('title').text
    summary = soup.find('meta', attrs={'name': 'description'})['content']

    return {
        'image_url': image_url,
        'title': title,
        'summary': summary
    }
