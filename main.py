
# version 1.2

import bs4
import requests
import csv
import logging
import urllib3
from progress.bar import IncrementalBar

urllib3.disable_warnings()

logging.basicConfig(filename="parse.log", level=logging.INFO, filemode="w")

url_21vek = 'https://www.21vek.by/info/brands/belbohemia.html'

url_vdom_search = 'https://vdom.by/?post_type=product&s='  # for search in vdom.by

url_oz_main = 'https://oz.by/producer/more120300.html'

url_oki = "https://oki.by/search?q=%D0%B1%D0%B5%D0%BB%D0%B1%D0%BE%D0%B3%D0%B5%D0%BC%D0%B8%D1%8F"

my_list = []


class Parser:

    def __init__(self):
        # init parser
        self.session = requests.Session()
        self.session.headers = {'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.9 (KHTML, like Gecko) \
         Chrome/5.0.307.11 Safari/532.9'}

    def get_page(self, page_url):
        # text of page
        try:
            r = self.session.get(page_url, verify=False)
            r.encoding = 'utf-8'
            html_page = r.text
        except Exception as E:
            html_page = ""
            logging.exception(E)
        return html_page


class ParserOz(Parser):

    def get_final_page(self):
        soup = bs4.BeautifulSoup(self.get_page(url_oz_main), 'lxml')
        r = soup.find("li", class_="g-pagination__list__li pg-link pg-last").find("a").text
        final_page = int(r)
        return final_page

    @staticmethod
    def get_links(html):
        links = []
        soup = bs4.BeautifulSoup(html, 'lxml')
        container = soup.find_all("div", class_="item-type-card__content")
        for cont in container:
            links.append(cont.find("a").get("href"))
        return links

    def parse_product(self, link):
        cod_link = self.get_page("https://oz.by" + link)
        soup = bs4.BeautifulSoup(cod_link, 'lxml')
        name = soup.find("div", class_="b-product-title__heading").find("h1").text
        price = soup.find("div", class_="b-product-control__row").find("span").text.strip().split("\xa0")[0]
        articles = soup.find("div", class_="b-description__container-col").find_all("td")
        i = 0
        sa = ''
        for article in articles:
            i = i+1
            if article.text == 'Артикул':
                sa = articles[i].text
                break
        return name, price, sa


class ParserVdom(Parser):

    def price_vdom(self, article):
        vdom_text = url_vdom_search+article
        soup = bs4.BeautifulSoup(self.get_page(vdom_text), 'lxml')
        try:
            r = soup.find("p", class_="price").find("span").text

            if article == soup.find("table", class_="shop_attributes").find("td").text:
                price_vdom = str(int(r.split('.')[0])+0.01*int(r.split('.')[1][0:2])).replace('.', ',')
            else:
                price_vdom = ''
        except Exception as E:
            logging.exception(E)
            price_vdom = ''
        return price_vdom


class ParserOki(Parser):

    def get_final_page(self):
        soup = bs4.BeautifulSoup(self.get_page(url_oki), 'lxml')
        r = soup.find("ul", class_="pagination").find_all("li")
        r = r[-1].find("a").get("href").split("=")[-1]
        return int(r)

    @staticmethod
    def get_links(html):
        links = []
        soup = bs4.BeautifulSoup(html, 'lxml')
        container = soup.find_all("div", class_="col-sm-6 col-md-4 item")
        for cont in container:
            links.append(cont.find("div", class_='prod-img').find("a").get("href"))
        return links

    def parse_product(self, link):
        cod_link = self.get_page("https://oki.by" + link)
        soup = bs4.BeautifulSoup(cod_link, 'lxml')
        name = soup.find("div", class_="col-md-12 title-name").find("h1").find("span").text
        price = soup.find("div", class_="price").find("p").text.strip().split(" ")[0]
        articles = soup.find("table", class_="table table-condensed").find_all("td")
        sa = articles[1].text

        return name, price.replace(".", ","), sa


class Parser21Vek(Parser):

    def get_links(self, html):
        list_urls_21vek = []
        soup = bs4.BeautifulSoup(self.get_page(html), 'lxml')
        try:
            links = soup.find("ul", class_="b-categories-full brand-categories__list")\
                        .find_all("li", class_="brand-subcategories__item")
            for url in links:
                list_url_21vek = url.find("a", class_='brand-subcategories__link').get("href")
                list_urls_21vek.append(list_url_21vek)
            links = list_urls_21vek
        except Exception as E:
            logging.exception('Страниц нет', E)
            links = []
        return links

    def get_final_page(self, page_url):
        # definition number of final page
        soup = bs4.BeautifulSoup(self.get_page(page_url), 'lxml')
        try:
            final_page_soup = soup.find("span", class_="cr-curent cr-paging_link").text
            final_page = int(final_page_soup.strip())
        except Exception as E:
            logging.exception(E)
            return 1
        return final_page

    @staticmethod
    def get_blocks(html):
        # blocks with products
        soup = bs4.BeautifulSoup(html, 'lxml')
        container = soup.select('li.result__item')
        return container

    @staticmethod
    def get_article(name):
        # article for vdom.by
        str_article = name.split(' ')
        result = ''
        for i in str_article:
            if len(i) == 5 and i.isnumeric():
                result = i
        return result

    def parse_block(self, item):
        # definition name and price 21vek.by
        try:
            # name is found
            name_product = item.find("span", class_="result__name").text
        except Exception as E:
            logging.exception(E)
            name_product = ''
        try:
            # price is found
            price_product = item.find('span', class_="g-price__unit result__priceunit").find_previous("span").text
        except Exception as E:
            logging.exception(E)
            price_product = ''
        try:
            article_product = self.get_article(name_product)
        except Exception as E:
            logging.exception(E)
            article_product = ''
        return name_product, price_product, article_product


def parse_oki():
    vdom = ParserVdom()
    print("Парсим Oki.by")
    oki = ParserOki()
    fp = oki.get_final_page()  # define pages
    for page in range(0, fp):
        url_count = url_oki + '&sort=1&page=' + str(page + 1)  # format url
        links = oki.get_links(oki.get_page(url_count))
        bar = IncrementalBar('  Links#' + str(page), max=len(links))
        for i in links:
            bar.next()
            parse_product_temp = oki.parse_product(i)
            if parse_product_temp[1] != '' and parse_product_temp[2] != '':
                short = [(parse_product_temp[2], parse_product_temp[0],
                          parse_product_temp[1], vdom.price_vdom(parse_product_temp[2]))]
                # if short[0][3] != '':
                #     print(page, short)
                my_list.append(short)
        bar.finish()
    return my_list


def parse_21vek():
    vdom = ParserVdom()
    print("Парсим 21 век")
    p21 = Parser21Vek()
    list_url_21vek = p21.get_links(url_21vek)
    for url in list_url_21vek:
        fp = p21.get_final_page(url)  # define pages
        for page in range(0, fp):
            url_count = url + 'page:' + str(page + 1)  # format url
            cont = p21.get_blocks(p21.get_page(url_count))
            bar = IncrementalBar('Page #' + str(url), max=len(cont))
            for i in cont:
                bar.next()
                if p21.parse_block(i)[1] != '':
                    parse_block_temp = p21.parse_block(i)
                    short = [(parse_block_temp[2], parse_block_temp[0],
                              parse_block_temp[1], vdom.price_vdom(p21.parse_block(i)[2]))]
                    # if short[0][3] != '':
                    #     print(page, short)
                    my_list.append(short)
            bar.finish()
    return my_list


def parse_oz():
    vdom = ParserVdom()
    print("Парсим oz.by")
    oz = ParserOz()
    fp = oz.get_final_page()  # define pages
    for page in range(0, fp):
        url_count = url_oz_main + 'page%3A2=&page=3?page=' + str(page+1)  # format url
        links = oz.get_links(oz.get_page(url_count))
        bar = IncrementalBar('  Links#' + str(page), max=len(links))
        for i in links:
            bar.next()
            parse_product_temp = oz.parse_product(i)
            if parse_product_temp[1] != '' and parse_product_temp[2] != '':
                short = [(parse_product_temp[2], parse_product_temp[0],
                          parse_product_temp[1], vdom.price_vdom(parse_product_temp[2]))]
                my_list.append(short)
        bar.finish()
    return my_list


def main():
    name = ''
    print("1 - 21 Век, 2 - Oki.by, 3 - oz.by")
    parsing_type = input()
    if parsing_type == '1':
        parse_21vek()
        name = '21vek.csv'
    elif parsing_type == '2':
        parse_oki()
        name = "oki.csv"
    elif parsing_type == '3':
        parse_oz()
        name = "oz.csv"
    else:
        print("Выходим")
    return my_list, name


if __name__ == '__main__':

    list_csv, name_file = main()
    if list_csv:
        with open(name_file, "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            for line in list_csv:
                writer.writerow(line[0])
    else:
        print("Thanks")
