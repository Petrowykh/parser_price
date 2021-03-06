
# version 1.2

import bs4
import requests
import csv
import logging


logging.basicConfig(filename="parse.log", level=logging.INFO, filemode="w")


list_url_temp = {  # for testing
    'https://www.21vek.by/ny_decorations/all/belbohemia/',
}

url_vdom_search = 'https://vdom.by/?post_type=product&s='  # for search in vdom.by

url_oz_main = 'https://oz.by/producer/more120300.html'

# list_url_21vek = {
#
#     'https://www.21vek.by/vacuum_packing/all/belbohemia/',
#     'https://www.21vek.by/clothes_hangers/all/belbohemia/',
#
#     # 'https://www.21vek.by/ny_decorations/all/belbohemia/',
#     # 'https://www.21vek.by/led_decorations/all/belbohemia/',
#     # 'https://www.21vek.by/christmas_led_figures/all/belbohemia/',
#     # 'https://www.21vek.by/christmas_trees/all/belbohemia/',
#     # 'https://www.21vek.by/party_goods/all/belbohemia/',
#     # 'https://www.21vek.by/food_containers/all/belbohemia/',
#     # 'https://www.21vek.by/spice_organizers/all/belbohemia/',
#     # 'https://www.21vek.by/kitchen_organizers/all/belbohemia/',
#     # 'https://www.21vek.by/drinkware/all/belbohemia/',
#     # 'https://www.21vek.by/dishes/all/belbohemia/',
#     # 'https://www.21vek.by/tableware/all/belbohemia/',
#     # 'https://www.21vek.by/cutlery/all/belbohemia/',
#     # 'https://www.21vek.by/bar_accessories/all/belbohemia/',
#     # 'https://www.21vek.by/candles_candleholders/all/belbohemia/',
#     # 'https://www.21vek.by/statuettes/all/belbohemia/',
#     # 'https://www.21vek.by/flowerpots/all/belbohemia/',
#     # 'https://www.21vek.by/vases/all/belbohemia/',
#     # 'https://www.21vek.by/jewelry_boxes/all/belbohemia/',
#     # 'https://www.21vek.by/artificial_flowers_plants/all/belbohemia/',
#     # 'https://www.21vek.by/furnishings/all/belbohemia/',
#     # 'https://www.21vek.by/interior_watches/all/belbohemia/',
#     # 'https://www.21vek.by/thermoses/all/belbohemia/',
#     # 'https://www.21vek.by/bags_refrigerators/all/belbohemia/',
#     # 'https://www.21vek.by/cezves/all/belbohemia/',
#     # 'https://www.21vek.by/coffee_teapots/all/belbohemia/',
#     # 'https://www.21vek.by/bathroom_furniture/all/belbohemia/',
#     # 'https://www.21vek.by/bathroom_apps/all/belbohemia/',
#     # 'https://www.21vek.by/storage_organizers/all/belbohemia/',
#     # 'https://www.21vek.by/bins/all/belbohemia/',
#     # 'https://www.21vek.by/cleaning_implements/all/belbohemia/',
#     # 'https://www.21vek.by/drying_racks/all/belbohemia/',
#     # 'https://www.21vek.by/towels/all/belbohemia/',
#     # 'https://www.21vek.by/washing_tools/all/belbohemia/',
#     # 'https://www.21vek.by/makeup_storage/all/belbohemia/',
#     # # 'https://www.21vek.by/vacuum_packing/all/belbohemia/',
#     # 'https://www.21vek.by/clothes_hangers/all/belbohemia/',
#     # 'https://www.21vek.by/face_apps/all/belbohemia/',
#     # 'https://www.21vek.by/bathtub_enclosures/all/belbohemia/',
#     # 'https://www.21vek.by/toilet_accessories/all/belbohemia/',
#     # 'https://www.21vek.by/bathroom_sets/all/belbohemia/',
#     # 'https://www.21vek.by/aprons_potholders/all/belbohemia/',
#     # 'https://www.21vek.by/watering/all/belbohemia/',
#     # 'https://www.21vek.by/gift_sets/all/belbohemia/',
#     # 'https://www.21vek.by/cutting_boards/all/belbohemia/',
#     # 'https://www.21vek.by/kitchen_apps/all/belbohemia/',
#     # 'https://www.21vek.by/bowls_feeders/all/belbohemia/',
#     # 'https://www.21vek.by/animal_furniture/all/belbohemia/',
#     # 'https://www.21vek.by/cat_scratchers/all/belbohemia/',
#     # 'https://www.21vek.by/aerobics_yoga/all/belbohemia/',
#     # 'https://www.21vek.by/sport_expanders/all/belbohemia/',
#     # 'https://www.21vek.by/weights/all/belbohemia/',
#     # 'https://www.21vek.by/hair_accessories/all/belbohemia/',
#     # 'https://www.21vek.by/hair_colors/all/belbohemia/',
#     # 'https://www.21vek.by/massagers/all/belbohemia/',
#     # 'https://www.21vek.by/sports_bottles/all/belbohemia/',
#     # 'https://www.21vek.by/frying_pans/all/belbohemia/',
#     # 'https://www.21vek.by/parasols/all/belbohemia/'
# }


class Parser:

    def __init__(self):
        # init parser
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    def get_page(self, page_url):
        # text of page
        # print('GET')
        try:
            r = self.session.get(page_url)
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


class Parser21Vek(Parser):

    def get_links(self):
        list_urls_21vek = []
        soup = bs4.BeautifulSoup(self.get_page('https://www.21vek.by/info/brands/belbohemia.html'), 'lxml')
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

            # final_page = final_page_soup.strip().split(' ')[-1]
            # final_page = round(int(final_page_str)/60+0.5)
        except:
            final_page = 1
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
        except:
            article_product = ''

        return name_product, price_product, article_product


def main():
    oz = ParserOz()
    vdom = ParserVdom()
    p21 = Parser21Vek()
    my_list = []

    # fp = oz.get_final_page()  # define pages
    # for page in range(0, fp):
    #     url_count = url_oz_main + 'page%3A2=&page=3?page=' + str(page+1)  # format url
    #     print(url_count)
    #     links = oz.get_links(oz.get_page(url_count))
    #
    #     for i in links:
    #         parse_product_temp = oz.parse_product(i)
    #         if parse_product_temp[1] != '' and parse_product_temp[2] != '':
    #
    #             short = [(parse_product_temp[2], parse_product_temp[0],
    #                       parse_product_temp[1], vdom.price_vdom(parse_product_temp[2]))]
    #             if short[0][3] != '':
    #                 print(page, short)
    #             my_list.append(short)

    list_url_21vek = p21.get_links()

    for url in list_url_21vek:
        fp = p21.get_final_page(url)  # define pages
        for page in range(0, fp):
            url_count = url + 'page:' + str(page+1)  # format url
            print(url_count)
            cont = p21.get_blocks(p21.get_page(url_count))
            for i in cont:
                if p21.parse_block(i)[1] != '':
                    parse_block_temp = p21.parse_block(i)
                    short = [(parse_block_temp[2], parse_block_temp[0],
                             parse_block_temp[1], vdom.price_vdom(p21.parse_block(i)[2]))]
                    if short[0][3] != '':
                        print(page, short)
                    my_list.append(short)
    return my_list


if __name__ == '__main__':
    list_csv = main()
    with open('out.csv', "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for line in list_csv:
            writer.writerow(line[0])
