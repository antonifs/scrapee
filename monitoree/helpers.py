import requests
from bs4 import BeautifulSoup

def crawl(domain, tag, attr, attr_val):
    r = requests.get(domain)
    soup = BeautifulSoup(r.content, "html.parser")
    res = soup.find_all(tag, {attr : attr_val})
    return res

def crawl2(domain,
            block_tag,
            block_attribute,
            block_value,
            item_tag,
            item_attribute,
            item_value
           ):
    r = requests.get(domain)
    soup = BeautifulSoup(r.content, "html.parser")
    res = soup.find_all(block_tag, {block_attribute : block_value})
    result = res[0].find_all(item_tag, {item_attribute : item_value})
    return result


def download_image(src):
    pass


def download_content(url):
    pass

def convert_money(money):
    from re import sub
    from decimal import Decimal
    return Decimal(sub(r'[^\d.]', '', money))

def get_token():
    url = 'http://tnklst.click/internalapi/oauth2/punten?client_id=87e7fd65fe9d937690b78da26971914a&client_secret=ccc7eab1a464cec1cb8658adb883df31'
    r = requests.get(url)
    return r.json()

def get_all_attributeset(token):
    url = 'http://tnklst.click/internalapi/scraper/attributeset'
    payload = {'access_token': token}
    r = requests.get(url, params=payload)
    return r.json()

def upload_product(data):
    url = 'http://tnklst.click/internalapi/scraper/createitem'
    r = requests.post(url, data=data)
    return r.json()

def get_brand_id(brand):
    url = 'http://tnklst.click/internalapi/oauth2/punten?brand_name=' + brand
    r = requests.get(url)
    return r.json()
