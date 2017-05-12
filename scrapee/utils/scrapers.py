import requests
from bs4 import BeautifulSoup
import re
from scrapee import settings
import urllib, json

def convert_money(money):
    from re import sub
    from decimal import Decimal
    return Decimal(sub(r'[^\d.]', '', money))

def get_content(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    product = soup.find_all("div", {"class" : "product-detail-img-row"})

    return product

def get_color(url):

    color = 'Not specified'

    content = get_content(url)
    try:
        p = content[0].find_all("p", {"class": "property-content"})
        if len(p) > 0:
            color = str(p[1].find_all("option", {"selected":"selected"})[0].text)
    except:
        passexit

    return color

def get_size(url):

    size = ''
    content = get_content(url)
    string = content[0].find_all("div", {"id": "size"})
    try:
        size = string[0].find_all("table")
        size = str(size[0]).replace("\n", "").replace(" ", "")
    except:
        match = re.findall(r'[\\n]*(\w+)\s*:\s*(\d+\s+\w+)', str(string[0]))
        res = [m[0] + " " + m[1] for m in match]
        size = str(", ".join(res))
    return size

def get_discount(url):
    discount = 0
    content = get_content(url)

    try:
        data = content[0].find_all("span", {"class":"specials"})
        disc = re.findall(r"\d+", str(data[1].text))
        discount = disc[0]
    except:
        pass

    return discount

def get_price(url):
    price = 0
    content = get_content(url)

    try:
        data = content[0].find_all("span", {"class":"specials"})
        price = str(data[0].text).split(" ")[1]
    except:
        pass

    return convert_money(price)

def get_fabric(url):
    fabric = ""
    content = get_content(url)

    try:
        data = content[0].find_all("span", {"class":"specials"})
        disc = re.findall(r"\d+", str(data[1].text))
        discount = disc[0]
    except:
        pass

    return discount

def is_sold(url):
    stock = 1
    content = get_content(url)

    try:
        data = content[0].find_all("button", {"disabled": "disabled"})

        if "out of Stock" in data[0].text:
            stock = 0
        else:
            stock = 1
    except:
        pass

    return stock

def get_subcategory(url, tag):
    content = get_content(url)

    try:
        data = content[0].find_all("", {"disabled": "disabled"})

        if "out of Stock" in data[0].text:
            stock = 0
        else:
            stock = 1
    except:
        pass

    return stock



def scraper_content(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    product = soup.find_all("div", {"class" : "product-detail-img-row"})

    condition = "Brand New"
    product_name = product[0].find_all("span", {"class": "product-name"})[0].text
    brand = product[0].find_all("h1", {"class": "content-title-text"})[0].find_all("a")[0].text
    image_1 = product[0].find_all("li", {"data-class": "product-thumb-1"})[0].find_all("img")[0]['src']

    try:
        image_2 = product[0].find_all("li", {"data-class": "product-thumb-2"})[0].find_all("img")[0]['src']
    except:
        image_2 = ""

    try:
        image_3 = product[0].find_all("li", {"data-class": "product-thumb-3"})[0].find_all("img")[0]['src']
    except:
        image_3 = ""

    try:
        image_4 = product[0].find_all("li", {"data-class": "product-thumb-4"})[0].find_all("img")[0]['src']
    except:
        image_4 = ""

    try:
        image_5 = product[0].find_all("li", {"data-class": "product-thumb-5"})[0].find_all("img")[0]['src']
    except:
        image_5 = ""

    try:
        price = product[0].find_all("span", {"class": "specials"})
    except:
        pass

    return {
            "condition": condition,
            "product_name": product_name,
            "brand": brand,
            "price": price,
            "url": url,
            "image_1": image_1,
            "image_2": image_2,
            "image_3": image_3,
            "image_4": image_4,
            "image_5": image_5,
    }

def scraper_mage_download():
    import urllib
    import os

    # Get item target, sort item ascending (oldest) then get the top one
    item = Item.objects.filter(is_image_scraped=False, is_scraped=True).order_by('id').first()

    if item:

        # number image(s) want to download
        img_num = 0

        media_root = settings.MEDIA_ROOT + '/import/'
        dir = str(item.title.replace(" ", "_"))
        directory = media_root + dir

        # create directory to store the images
        is_directory = os.path.exists(directory)
        if not os.path.exists(is_directory):
            os.makedirs(directory)

        # image collections
        img_url_1 = item.image_1
        img_url_2 = item.image_2
        img_url_3 = item.image_3
        img_url_4 = item.image_4
        img_url_5 = item.image_5

        if not img_url_1 == "":
            img_name_1 = item.title.replace(" ", "_") + "_1" + "." + str(item.image_1.split("/")[-1]).split(".")[-1]
            img_num += 1
            try:
                urllib.urlretrieve(img_url_1, directory + '/' + img_name_1)
            except:
                pass

        if not img_url_2 == "":
            img_name_2 = item.title.replace(" ", "_") + "_2" + "." + str(item.image_2.split("/")[-1]).split(".")[-1]
            img_num += 1
            try:
                urllib.urlretrieve(img_url_2, directory + '/' + img_name_2)
            except:
                pass

        if not img_url_3 == "":
            img_name_3 = item.title.replace(" ", "_") + "_3" + "." + str(item.image_3.split("/")[-1]).split(".")[-1]
            img_num += 1
            try:
                urllib.urlretrieve(img_url_3, directory + '/' + img_name_3)
            except:
                pass

        if not img_url_4 == "":
            img_name_4 = item.title.replace(" ", "_") + "_4" + "." + str(item.image_4.split("/")[-1]).split(".")[-1]
            img_num += 1
            try:
                urllib.urlretrieve(img_url_4, directory + '/' + img_name_4)
            except:
                pass

        if not img_url_5 == "":
            img_name_5 = item.title.replace(" ", "_") + "_5" + "." + str(item.image_5.split("/")[-1]).split(".")[-1]
            img_num += 1
            try:
                urllib.urlretrieve(img_url_5, directory + '/' + img_name_5)
            except:
                pass

        item.image_name_1 = img_name_1
        item.image_name_2 = img_name_2
        item.image_name_3 = img_name_3
        item.image_name_4 = img_name_4
        item.image_name_5 = img_name_5
        item.directory = dir
        item.is_image_scraped = True
        item.save()

# added today
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

def update_product(data):
    url = settings.API_DOMAIN + settings.API_UPDATE_ITEM
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

def get_material_id(material_name, token):
    url = settings.API_DOMAIN + settings.API_GET_MATERIAL + '?material=' + material_name + '' \
            '&access_token=' + token
    r = requests.get(url)
    return r.json()

def get_fabric_id(fabric_name, token):
    url = settings.API_DOMAIN + settings.API_GET_FABRIC + '?fabric=' + fabric_name + '' \
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


# Styletribute helper
def get_conversion_rate(url="https://api.styletribute.com/currencies"):
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return [i['rate'] for i in data if i['code'] == 'IDR'][0]
