import requests
from bs4 import BeautifulSoup
from scrapee import settings

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


# this tool will replace all formated-money with type string into a proper decimal
def convert_money(money):
    from re import sub
    from decimal import Decimal
    return Decimal(sub(r'[^\d.]', '', money))

def get_token():
    url = settings.API_DOMAIN + settings.API_GET_TOKEN + '?' \
            'client_id=' + settings.CLIENT_ID + '' \
            '&client_secret=' + settings.CLIENT_SECRET
    r = requests.get(url)
    return r.json()

def get_all_attributeset(token):
    url = settings.API_DOMAIN + settings.API_GET_ATTRIBUTESET + '?access_token=' + token
    r = requests.get(url)
    return r.json()

def upload_product(data):
    url = settings.API_DOMAIN + settings.API_CREATE_ITEM
    r = requests.post(url, data=data)
    return r.json()

def get_category_id(category, token):
    url = settings.API_DOMAIN + settings.API_GET_CATEGORY + '?category_name=' + category + '' \
            '&access_token=' + token
    r = requests.get(url)
    return r.json()

def get_brand_id(brand, token):
    url = settings.API_DOMAIN + settings.API_GET_BRAND + '?brand=' + brand + '' \
            '&access_token=' + token
    r = requests.get(url)
    return r.json()

def get_category_id(category_name, token):
    url = settings.API_DOMAIN + settings.API_GET_CATEGORY + '?category_name=' + category_name + '' \
            '&access_token=' + token
    r = requests.get(url)
    return r.json()

def upload_images(data):
    url = settings.API_DOMAIN + settings.API_ADD_IMAGE
    r = requests.post(url, data=data)
    return r.json()

# get the extension of a path
def get_image_extention(original_path):
    return str(original_path.split("/")[-1]).split(".")[-1]

# source of website scraped
def get_source(url):
    return url.split("/")[2]

def get_brand_id(brand, token):
    url = settings.API_DOMAIN + settings.API_GET_BRAND  +"?brand="+ brand +"&access_token="+ token
    r = requests.get(url)
    return r.json()

# the name consists of SKU_number.extension, extension taken from original extension file
def get_new_name(sku, original_path, number):
    return sku.replace(" ", "_") + "_" + number + "." + get_image_extention(original_path)

def get_domain(url):
    return url.split('/')[0] + '//' + url.split('/')[2]