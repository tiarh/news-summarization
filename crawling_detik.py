# crawling_detik.py
import requests
from bs4 import BeautifulSoup
import pandas as pd

class DetikCrawler:
    def __init__(self, topic):
        self.topic = topic
        self.df = None  # Inisialisasi DataFrame sebagai None

    def get_urls(self):
        news_links = []
        # get news URL from page 1
        page = 1
        url = f"https://www.detik.com/search/searchall?query={self.topic}&siteid=2&sortby=time&page={page}"
        html_page = requests.get(url).content
        soup = BeautifulSoup(html_page, 'lxml')
        articles = soup.find_all('article')

        # Ambil hanya satu URL berita, jika ada
        if articles:
            url = articles[0].find('a')['href']
            news_links.append(url)

        return news_links

    def has_link(self, text):
        # Fungsi untuk memeriksa apakah teks mengandung tautan
        return 'href=' in text

    def extract_news(self):
        # get news article details from scraped URLs
        scraped_info = []
        for news in self.get_urls():
            source = news
            html_page = requests.get(news).content
            soup = BeautifulSoup(html_page, 'lxml')
            # check if title, author, date, news div, is not None type
            title = soup.find('h1', class_='detail__title')
            if title is not None:
                title = title.text
                title = title.replace('\n', '')
                title = title.strip()

            author = soup.find('div', class_='detail__author')
            if author is not None:
                author = author.text

            date = soup.find('div', class_='detail__date')
            if date is not None:
                date = date.text

            # Ambil isi berita dari div dengan class 'detail__body-text itp_bodycontent'
            content_div = soup.find("div", {"class": "detail__body-text itp_bodycontent"})
            if content_div:
                # Hilangkan elemen-elemen <a> yang merupakan tautan
                for a_tag in content_div.find_all(self.has_link):
                    a_tag.decompose()

                # Ambil teks dari div
                news_content = ' '.join(content_div.stripped_strings)

                # convert scraped data into a dictionary
                news_data = {
                    "url": source,
                    "judul": title,
                    "penulis": author,
                    "tanggal": date,
                    "isi": news_content
                }
                # add dictionaries to a list
                scraped_info.append(news_data)

        self.df = pd.DataFrame.from_dict(scraped_info)
        return self.df