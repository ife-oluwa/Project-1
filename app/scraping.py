from bs4 import BeautifulSoup as Soup
import requests
import re
import pandas as pd
from datetime import date, datetime
import lxml


class scraping():

    def __init__(self, total, size_page=48):
        self.lowest = True
        self.total = total
        self.size_page = size_page
        self.min_pages = self.total//self.size_page
        self.remainder = self.total
        self.data = []

        if self.total > self.size_page:
            self.remainder = self.total - (self.size_page * self.min_pages)
            self.lowest = False

        print(
            f"Pages detected: {self.size_page}\nRemainder detected: {self.remainder}")

    def __set_df_data(self, dd):
        self.data.append(dd)

    def __set_data_page(self, soup, remainder):
        first_pictures = soup.select('img.ui-search-result-image__element')
        fp = [first_pictures[i]['data-src'] for i in range(0, remainder)]
        property_names = soup.select('h2.ui-search-item__title')
        pn = [property_names[i].text for i in range(0, remainder)]
        urls = soup.select('a.ui-search-result__content')
        url = [urls[i]['href'] for i in range(0, remainder)]
        prices = soup.select('span.price-tag-text-sr-only')
        prc = [prices[i].text for i in range(0, remainder)]
        addresses = soup.select('span.ui-search-item__location')
        adr = [addresses[i].text for i in range(0, remainder)]
        sizes = soup.select('li.ui-search-card-attributes__attribute')
        sz = [re.findall("\d+", sizes[i].text)[0]
              for i in range(0, remainder*2) if i % 2 == 0]
        ame = [sizes[i].text for i in range(0, (remainder*2)) if i % 2 != 0]
        desc = []
        for ur in url:
            descriptions_response = requests.get(ur)
            descriptions_soup = Soup(descriptions_response.content, 'lxml')
            descriptions = descriptions_soup.select(
                'p.ui-pdp-description__content')
            desc.append(descriptions[0].text)

        dict_data = {
            'property_name': pn,
            'url': url,
            'price': prc,
            'address': adr,
            'size': sz,
            'street': adr,
            'number': adr,
            'settlement': adr,
            'town': adr,
            'state': adr,
            'county': adr,
            'description': ame,
            'first_picture': fp
        }

        self.__set_df_data(dict_data)

    def __get_soup(self, n):
        url = f'https://inmuebles.metroscubicos.com/casas/venta/quintana-roo/_Desde_{n}_NoIndex_True'
        response = requests.get(url)
        return Soup(response.content, 'lxml')

    def get_data(self):
        c = 0
        if self.lowest:
            print(
                f"Scraping data from the first page, total elements {self.remainder}")
            soup = self.__get_soup(0)
            self.__set_data_page(soup, self.remainder)

        else:
            for p in range(0, self.min_pages, 1):
                print(f"Scraping data from page: {p+1}")
                if p > 0:
                    c = (p * self.size_page) + 1
                soup = self.__get_soup(c)
                self.__set_data_page(soup, self.size_page)

            if self.remainder > 0:
                print(f"Scraping data from remainder: {self.remainder}")
                c += self.size_page
                soup = self.__get_soup(c + 1)
                self.__set_data_page(soup, self.remainder)

        print("Joining all the scraped pages and remainders...")
        return pd.concat([pd.DataFrame(self.data[i], columns=self.data[i].keys()) for i in range(0, len(self.data))], axis=0).reset_index()
