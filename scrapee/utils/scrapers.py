import requests
from bs4 import BeautifulSoup

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
    else:
        p = product[0].find_all("p", {"class": "attribute-content"})
        price = p[0].find_all("span")[0].text

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


def scraper_mage_upload():
    return "image yay"