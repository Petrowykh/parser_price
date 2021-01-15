
# version 1.0

import bs4
import requests
import csv
import logging


logging.basicConfig(filename="parse.log", level=logging.INFO)


list_url_temp = {
    'https://www.21vek.by/ny_decorations/all/belbohemia/',
}

url_vdom_search = 'https://vdom.by/?post_type=product&s='

list_url = {
    'https://www.21vek.by/ny_decorations/all/belbohemia/',
    'https://www.21vek.by/led_decorations/all/belbohemia/',
    'https://www.21vek.by/christmas_led_figures/all/belbohemia/',
    'https://www.21vek.by/christmas_trees/all/belbohemia/',
    'https://www.21vek.by/party_goods/all/belbohemia/',
    'https://www.21vek.by/food_containers/all/belbohemia/',
    'https://www.21vek.by/spice_organizers/all/belbohemia/',
    'https://www.21vek.by/kitchen_organizers/all/belbohemia/',
    'https://www.21vek.by/drinkware/all/belbohemia/',
    'https://www.21vek.by/dishes/all/belbohemia/',
    'https://www.21vek.by/tableware/all/belbohemia/',
    'https://www.21vek.by/cutlery/all/belbohemia/',
    'https://www.21vek.by/bar_accessories/all/belbohemia/',
    'https://www.21vek.by/candles_candleholders/all/belbohemia/',
    'https://www.21vek.by/statuettes/all/belbohemia/',
    'https://www.21vek.by/flowerpots/all/belbohemia/',
    'https://www.21vek.by/vases/all/belbohemia/',
    'https://www.21vek.by/jewelry_boxes/all/belbohemia/',
    'https://www.21vek.by/artificial_flowers_plants/all/belbohemia/',
    'https://www.21vek.by/furnishings/all/belbohemia/',
    'https://www.21vek.by/interior_watches/all/belbohemia/',
    'https://www.21vek.by/thermoses/all/belbohemia/',  
    'https://www.21vek.by/bags_refrigerators/all/belbohemia/',
    'https://www.21vek.by/cezves/all/belbohemia/',
    'https://www.21vek.by/coffee_teapots/all/belbohemia/',
    'https://www.21vek.by/bathroom_furniture/all/belbohemia/',
    'https://www.21vek.by/bathroom_apps/all/belbohemia/',
    'https://www.21vek.by/storage_organizers/all/belbohemia/',
    'https://www.21vek.by/bins/all/belbohemia/',
    'https://www.21vek.by/cleaning_implements/all/belbohemia/',
    'https://www.21vek.by/drying_racks/all/belbohemia/',
    'https://www.21vek.by/towels/all/belbohemia/',
    'https://www.21vek.by/washing_tools/all/belbohemia/',
    'https://www.21vek.by/makeup_storage/all/belbohemia/',
    # 'https://www.21vek.by/vacuum_packing/all/belbohemia/',
    'https://www.21vek.by/clothes_hangers/all/belbohemia/',
    'https://www.21vek.by/face_apps/all/belbohemia/',
    'https://www.21vek.by/bathtub_enclosures/all/belbohemia/',
    'https://www.21vek.by/toilet_accessories/all/belbohemia/',
    'https://www.21vek.by/bathroom_sets/all/belbohemia/',
    'https://www.21vek.by/aprons_potholders/all/belbohemia/',
    'https://www.21vek.by/watering/all/belbohemia/',
    'https://www.21vek.by/gift_sets/all/belbohemia/',
    'https://www.21vek.by/cutting_boards/all/belbohemia/',
    'https://www.21vek.by/kitchen_apps/all/belbohemia/',
    'https://www.21vek.by/bowls_feeders/all/belbohemia/',
    'https://www.21vek.by/animal_furniture/all/belbohemia/',
    'https://www.21vek.by/cat_scratchers/all/belbohemia/',
    'https://www.21vek.by/aerobics_yoga/all/belbohemia/',
    'https://www.21vek.by/sport_expanders/all/belbohemia/',
    'https://www.21vek.by/weights/all/belbohemia/',
    'https://www.21vek.by/hair_accessories/all/belbohemia/',
    'https://www.21vek.by/hair_colors/all/belbohemia/',
    'https://www.21vek.by/massagers/all/belbohemia/',
    'https://www.21vek.by/sports_bottles/all/belbohemia/',
    'https://www.21vek.by/frying_pans/all/belbohemia/',
    'https://www.21vek.by/parasols/all/belbohemia/'

}


class ParserVdom:
    def __init__(self):
        # init parser
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    def get_page(self, page_url):
        # text of page
        r = self.session.get(page_url)
        r.encoding = 'utf-8'
        return r.text

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


class Parser21Vek:
    def __init__(self):
        # init parser
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    def get_page(self, page_url):
        # text of page
        try:
            r = self.session.get(page_url)
            r.encoding = 'utf-8'
            html_page = r.text
        except Exception as E:
            html_page = ""
            logging.exception(E)
        return html_page

    def get_final_page(self, page_url):
        # definition number of final page
        soup = bs4.BeautifulSoup(self.get_page(page_url), 'lxml')
        try:
            final_page_soup = soup.find("div", class_="cr-paginator_page_list").text
            final_page_str = final_page_soup.strip().split(' ')[-1]
            final_page = round(int(final_page_str)/60+0.5)
        except Exception as E:
            logging.exception('Страниц нет', E)
            final_page = 0
        return final_page

    def get_blocks(self, html):
        # blocks with products
        soup = bs4.BeautifulSoup(html, 'lxml')
        container = soup.select('li.result__item')
        return container

    def get_article(self, name):
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
            # имени может не быть
            name_product = item.find("span", class_="result__name")
        except Exception as E:
            logging.exception(E)
            name_product = ''
        try:
            # цены может не быть
            price_product = item.find('span', class_="g-price__unit result__priceunit").find_previous("span").text
        except Exception as E:
            logging.exception(E)
            price_product = ''
        return name_product.text, price_product, self.get_article(name_product.text)


def main():
    p21 = Parser21Vek()
    vdom = ParserVdom()

    my_list = []

    for url in list_url:
        fp = p21.get_final_page(url)  # define pages
        for page in range(0, fp):
            url_count = url + 'page:' + str(page+1)  # format url
            print(url_count)
            cont = p21.get_blocks(p21.get_page(url_count))
            for i in cont:
                if p21.parse_block(i)[1] != '':
                    short = [(p21.parse_block(i)[2], p21.parse_block(i)[0],
                             p21.parse_block(i)[1], vdom.price_vdom(p21.parse_block(i)[2]))]
                    my_list.append(short)
    return my_list


if __name__ == '__main__':
    list_csv = main()
    with open('out.csv', "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for line in list_csv:
            writer.writerow(line[0])
