
# version 1.0

import bs4
import requests


list_url_temp = {
    'https://www.21vek.by/jewelry_boxes/all/belbohemia/',
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
    'https://www.21vek.by/bags_refrigerators/all/belbohemia/'
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

    def price_vdom (self, article):
        vdom_text = url_vdom_search+article
        soup = bs4.BeautifulSoup(self.get_page(vdom_text), 'lxml')
        try:
            r = soup.find("p", class_ = "price").find("span").text
            if article == soup.find("table", class_="shop_attributes").find("td").text:
                price_vdom = int(r.split('.')[0])+0.01*int(r.split('.')[1][0:2])
            else:
                price_vdom = "N/D"
        except:
            price_vdom = "N/D"
        return price_vdom

class Parser_21:
    def __init__(self):
        # init parser
        self.session = requests.Session()
        self.session.headers = {
            'User - Agent': 'Mozilla 5.0 (Windows NT 10.0; Win64; x64) AppleWebKit \
            537.36(KHTML, like Gecko) Chrome / 78.0.3904.108 Safari / 537.36',
            'Accept-Language': 'ru',
        }

    def get_page(self, page_url):
        # text of page
        r = self.session.get(page_url)
        r.encoding = 'utf-8'
        return r.text

    def get_final_page (self, page_url):
        # definition number of final page
        soup = bs4.BeautifulSoup(self.get_page(page_url), 'lxml')
        try:
            final_page_soup = soup.find("div", class_ ="cr-paginator_page_list").text
            final_page_str = final_page_soup.strip().split(' ')[-1]
            final_page = round(int(final_page_str)/60+0.5)
            #print (final_page)

        except Exception as E:
            print ('Страниц нет')
            final_page = 0

        return final_page


    def get_blocks(self, html):
        # blocks with products
        soup = bs4.BeautifulSoup(html, 'lxml')
        container = soup.select('li.result__item')
        return container

    def get_article (self, name):
        # article for vdom.by
        #TODO функция на справляется со строкой "в ассортимеенте", исправть
        str = name.split(' ')
        if ')' in str[-1]:
            if '(' in str[-2]:
                return str[-3]
            else:
                return str[-2]
        else:
            return str[-1]

    def parse_block(self, item):
        # definition name and price 21vek.by
        try:
            # имени может не быть
            name_product = item.find("span", class_ = 'result__name')
        except Exception as E:
            print (E)
            name_product = ''
        try:
            #цены может не быть
            price_product = item.find('span', class_ = "g-price__unit result__priceunit").find_previous("span").text

            #price = price_product.find("span")
        except:
            price_product = ''
        return name_product.text, price_product, self.get_article(name_product.text)

def main():
    p21 = Parser_21()
    vdom = ParserVdom()

    for url in list_url_temp:
        cont = p21.get_blocks(p21.get_page(url))
        for i in cont:
            #print ('article vdom: ', p21.parse_block(i)[2])

            print(p21.parse_block(i))
            print (vdom.price_vdom(p21.parse_block(i)[2]))
        fp = p21.get_final_page(url)
        if fp > 0:
            for page in range(1, fp):
                print ('Page: ', page+1)
                url_count = url + 'page:' + str(page+1)
                print (url_count)
                cont = p21.get_blocks(p21.get_page(url_count))
                for i in cont:
                    print (p21.parse_block(i))
                    print(vdom.price_vdom(p21.parse_block(i)[2]))

if __name__ == '__main__':
    main()


