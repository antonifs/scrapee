import requests
from bs4 import BeautifulSoup

def crawl(domain, tag, attr, attr_val):
    r = requests.get(domain)
    soup = BeautifulSoup(r.content, "html.parser")
    res = soup.find_all(tag, {attr : attr_val})
    return res

def download_image(src):
    pass


def download_content(url):
    pass

def convert_money(money):
    from re import sub
    from decimal import Decimal
    return Decimal(sub(r'[^\d.]', '', money))