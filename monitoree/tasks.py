from celery.task.schedules import crontab
from celery.decorators import periodic_task
from scrapee.utils import scrapers
from celery.utils.log import get_task_logger

import helpers

from .models import Monitoring, Category, Item, Url

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
                url = url.url,
                price = helpers.convert_money(object["price"]),
                image_1 = object['image_1'],
                image_2 = object['image_2'],
                image_3 = object['image_3'],
                image_4 = object['image_4'],
                image_5 = object['image_5'],
                category_raw = "".join(category).replace("-", " "),
                sub_category_raw = "".join(sub_category).replace("-", " "),
                is_sold = 1,
                status = 1,
                brand = object['brand'],
                condition = object["condition"],
                currency = 1,
                is_scrapped = True,

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
        url = "http://tnklst.click/internalapi/scraper/searchbrand?brand="+ item.brand +"&access_token="+ access_token
        brand_obj = requests.get(url)
        brand = brand_obj.json()
        brand_id = brand[item.brand]

        # Rsync the product
        os.system('rsync -avz -e "ssh -o StrictHostKeyChecking=no \ -o UserKnownHostsFile=/dev/null" --progress /var/www/html/magento/media/import/' + item.directory +' root@tinkerlust.com:/var/www/html/magento/media/import/' + item.directory)

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
