#news_crawler.py
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from api.utils.config import news_kor

class NewsCrawler:
    def __init__(self, urls):
        self.urls = urls
        self.results = {'title': [], 'content': []}

    def fetch(self, url):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse(self, html, url):
        if html is None:
            return None

        parser = BeautifulSoup(html, 'xml')
        items = parser.find_all('item')

        for item in items:
            self.results['title'].append(item.find('title').text)
            self.results['content'].append(item.find('description').text)


    def crawl_single_url(self, url):
        html = self.fetch(url)
        self.parse(html, url)

    def crawl_all(self, max_workers=5):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(self.crawl_single_url, self.urls)

    def get_results(self):
        return self.results
    
def get_korean_news():
    urls_kor = news_kor

    crawler = NewsCrawler(urls_kor)
    crawler.crawl_all(max_workers=5)

    results = crawler.get_results()

    return results