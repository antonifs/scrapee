from celery.task.schedules import crontab
from celery.decorators import periodic_task
from scrapee.utils import scrapers
from celery.utils.log import get_task_logger
from scrapee import settings

import requests
import helpers

from models import Monitoring, Category, Item, Url

logger = get_task_logger(__name__)

# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def scraper_content():

    '''
    :Flow
    - Read Url table
    - Scrap object based on given url
    - Write the result to Item table
    - Update url object status to scraped (2)
    '''
    url = Url.objects.filter(status=1).order_by('-id').first()

    if url:
        logger.info("Scraper is started.")
        object = scrapers.scraper_content(url.url)

        try:

            category = url.url.split("/")[-3:-2]
            sub_category = url.url.split("/")[-2:-1]

            # Save the content
            Item(title = object['product_name'],
                url = str(url.url),
                price = helpers.convert_money(object["price"]),
                status = 1,
                currency = 1,
                image_1 = object['image_1'],
                image_2 = object['image_2'],
                image_3 = object['image_3'],
                image_4 = object['image_4'],
                image_5 = object['image_5'],
                category_raw = "".join(category).replace("-", " "),
                sub_category_raw = "".join(sub_category).replace("-", " "),
                is_sold = 1,
                brand = object['brand'],
                condition = object["condition"],
                is_scraped = True,
                is_image_scraped = False,
            ).save()

            logger.info("%s scraped and was saved" % url.id)
        except:
            pass

        # update the status to scraped
        obj_url = Url.objects.get(id=url.id)
        obj_url.status = 2
        obj_url.save()
    else:
        logger.info("Nothing can be scraped")

@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def scraper_image_download():
    import urllib
    import os

    # Get item target, sort item ascending (oldest) then get the top one
    item = Item.objects.filter(is_image_scraped=False, is_scraped=True).order_by('id').first()

    if item:

        # number image(s) want to download
        img_num = 0

        media_root = settings.MEDIA_ROOT + '/import/'
        dir = str(item.title.replace(" ", "_").encode('utf-8'))
        directory = media_root + dir

        # create directory to store the images
        if not os.path.exists(directory):
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
        else:
            img_name_1 = ""

        if not img_url_2 == "":
            img_name_2 = item.title.replace(" ", "_") + "_2" + "." + str(item.image_2.split("/")[-1]).split(".")[-1]
            img_num += 1
            try:
                urllib.urlretrieve(img_url_2, directory + '/' + img_name_2)
            except:
                pass
        else:
            img_name_2 = ""

        if not img_url_3 == "":
            img_name_3 = item.title.replace(" ", "_") + "_3" + "." + str(item.image_3.split("/")[-1]).split(".")[-1]
            img_num += 1
            try:
                urllib.urlretrieve(img_url_3, directory + '/' + img_name_3)
            except:
                pass
        else:
            img_name_3 = ""

        if not img_url_4 == "":
            img_name_4 = item.title.replace(" ", "_") + "_4" + "." + str(item.image_4.split("/")[-1]).split(".")[-1]
            img_num += 1
            try:
                urllib.urlretrieve(img_url_4, directory + '/' + img_name_4)
            except:
                pass
        else:
            img_name_4 = ""

        if not img_url_5 == "":
            img_name_5 = item.title.replace(" ", "_") + "_5" + "." + str(item.image_5.split("/")[-1]).split(".")[-1]
            img_num += 1
            try:
                urllib.urlretrieve(img_url_5, directory + '/' + img_name_5)
            except:
                pass
        else:
            img_name_5 = ""

        item.image_name_1 = img_name_1
        item.image_name_2 = img_name_2
        item.image_name_3 = img_name_3
        item.image_name_4 = img_name_4
        item.image_name_5 = img_name_5
        item.directory = dir
        item.is_image_scraped = True
        item.save()


@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def scraper_mage_upload():

    import os

    item = Item.objects.filter(status=1).order_by('id').first()

    if item:

        token = helpers.get_token()

        access_token = token['access_token']

        # Converter
        attribute_set = {
            'bags' : 'Tas',
            'accessories' : 'Aksesoris',
            'shoes' : 'Sepatu',
        }

        att_set = attribute_set[str(item.category_raw)]
        attributeset = helpers.get_all_attributeset(token['access_token'])
        att_set_id = attributeset['data'][att_set]

        item = Item.objects.filter(is_image_scraped=True, is_scraped=True).order_by('id').first()
        url_search_brand =  settings.API_DOMAIN + "internalapi/scraper/searchbrand?brand="+ str(item.brand) +"&access_token="+ access_token
        logger.info("URL Brand: %s" % url_search_brand)
        brand_obj = requests.get(url_search_brand)
        brand = brand_obj.json()
        logger.info("Brand: %s" % brand)
        brand_id = brand['data'][str(item.brand)]

        # Rsync the product
        staging_src = '/var/www/html/magento/media/import/'
        server_src = '/var/www/html/magento/media/import/'

        # Production server
        # os.system('rsync -avz -e "ssh -o StrictHostKeyChecking=no \ -o UserKnownHostsFile=/dev/null" --progress ' + staging_src + item.directory +' root@tinkerlust.com:' + server_src + item.directory)

        # Staging server

        logger.info("Rsyncing ... ")
        local_src = '/Users/antonifs/Documents/tinkerlust/store_scraper/media/import/'
        os.system('rsync -avz -e "ssh -o StrictHostKeyChecking=no \ -o UserKnownHostsFile=/dev/null" --progress ' + local_src + item.directory +' root@tnklst.click:' + staging_src + item.directory)
        logger.info("Done Rsyncing")

        params = {
            'access_token': access_token,
        }
        data = {
                'name'              : item.title,
                'attribute_set_id'  : att_set_id,
                'weight'            : 3,
                'color'             : [9,7],
                'price'             : item.price,
                'description'       : '-',
                'short_description' : '-',
                'vendor_attribute'  : 298,
                'vendor_category'   : 2667,
                'fabric'            : 3,
                'condition'         : 2,
                'category_1'        : att_set_id,
                'category_2'        : 5,
                'brand_id'          : brand_id,
                'source'            : 'bobobobo',
                'access_token'      : access_token,
        }

        res = helpers.upload_product(data);

        logger.info("Upload to Mage: %s " % res)

        item.status = 2
        item.save()
    else:
        logger.info("Nothing can be uploaded")
