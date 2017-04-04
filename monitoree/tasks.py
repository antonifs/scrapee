from celery.task.schedules import crontab
from celery.decorators import periodic_task
from scrapee.utils import scrapers
from celery.utils.log import get_task_logger
from scrapee import settings

import requests
import helpers
import os

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
    url = Url.objects.filter(status=1).order_by('id').first()

    if url:
        logger.info("Scraper is started.")

        # scrap the html content
        object = scrapers.scraper_content(url.url)

        try:

            category = url.url.split("/")[-3:-2]
            sub_category = url.url.split("/")[-2:-1]

            if not Item.objects.filter(url=str(url.url)).exists():

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
            else:
                logger.info("Item is existed")
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

        url = settings.API_DOMAIN + settings.API_GET_TOKEN + '?' \
            'client_id=' + settings.CLIENT_ID + '' \
            '&client_secret=' + settings.CLIENT_SECRET

        logger.info("reg: %s" % url)

        token = helpers.get_token()

        logger.info("token: %s" % token)


        access_token = token['access_token']

        # Convert attributeset from target standard to tinkerlust standard
        attribute_set = {
            'bags' : 'Tas',
            'accessories' : 'Aksesoris',
            'shoes' : 'Sepatu',
        }

        att_set = attribute_set[str(item.category_raw)]
        attributeset = helpers.get_all_attributeset(access_token)
        att_set_id = attributeset['data'][att_set]

        brand_id = str([val for key, val in helpers.get_brand_id(str(item.brand), access_token)['data'].iteritems()][0])

        domain = helpers.get_domain(item.url)

        source = Monitoring.objects.filter(domain=domain).first()

        category_id = str(helpers.get_category_id(str(item.category_raw), access_token)['data'][0])
        if len(helpers.get_category_id(str(item.sub_category_raw), access_token)['data']) > 0:
            sub_category_id = str(helpers.get_category_id(str(item.sub_category_raw), access_token)['data'][0])
        else:
            sub_category_id = 0

        data = {
                'name'              : str(item.title),
                'attribute_set_id'  : str(att_set_id),
                'weight'            : 3,
                'color'             : [9,7],
                'price'             : item.price,
                'description'       : '-',
                'short_description' : '-',
                'vendor_attribute'  : str(source.vendor_attribute),
                'vendor_category'   : str(source.vendor_category),
                'fabric'            : 3,
                'condition'         : 2,
                'category_1'        : category_id,
                'category_2'        : sub_category_id,
                'brand_id'          : brand_id,
                'source'            : str(source.domain),
                'access_token'      : str(access_token),
        }

        logger.info("Data: %s " % data)

        res = helpers.upload_product(data)

        logger.info("%s has been upload to Magento" % res)

        item.sku = str(res['data'][u'sku'])
        item.status = 2
        item.save()
    else:
        logger.info("Nothing can be uploaded")

@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def scraper_image_download():
    import urllib
    import os

    # Get item target, sort item ascending (oldest) then get the top one
    item = Item.objects.filter(status=2).order_by('id').first()

    if item:

        # number image(s) want to download
        img_num = 0

        media_root = settings.MEDIA_ROOT + '/import/'
        dir = str(item.sku.replace(" ", "_").encode('utf-8'))
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
            img_name_1 = helpers.get_new_name(item.sku, item.image_1, '1')
            img_num += 1
            try:
                urllib.urlretrieve(img_url_1, directory + '/' + img_name_1)
            except:
                pass
        else:
            img_name_1 = ""

        if not img_url_2 == "":
            img_name_2 = helpers.get_new_name(item.sku, item.image_2, '2')
            img_num += 1
            try:
                urllib.urlretrieve(img_url_2, directory + '/' + img_name_2)
            except:
                pass
        else:
            img_name_2 = ""

        if not img_url_3 == "":
            img_name_3 = helpers.get_new_name(item.sku, item.image_3, '3')
            img_num += 1
            try:
                urllib.urlretrieve(img_url_3, directory + '/' + img_name_3)
            except:
                pass
        else:
            img_name_3 = ""

        if not img_url_4 == "":
            img_name_4 = helpers.get_new_name(item.sku, item.image_4, '4')
            img_num += 1
            try:
                urllib.urlretrieve(img_url_4, directory + '/' + img_name_4)
            except:
                pass
        else:
            img_name_4 = ""

        if not img_url_5 == "":
            img_name_5 = helpers.get_new_name(item.sku, item.image_5, '5')
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
        item.status = 3
        item.save()

        logger.info("%s is downloaded." % item)


@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def scraper_upload_images():

    # Get item which the images have been scraped
    item = Item.objects.filter(status=3).order_by('id').first()

    if item:

        token = helpers.get_token()
        access_token = token['access_token']

        logger.info("Token: %s access token: %s" % (token, access_token))

        logger.info("Rsyncing ... ")

        '''
        --------------------------------------------------------------------------------------------------
        Production server: vendor upload to tinkerlust.com
        --------------------------------------------------------------------------------------------------
        '''
        # staging_src = '/var/www/html/magento/media/import/'
        # server_src = '/var/www/html/magento/media/import/'

        # origin = staging_src
        # target = server_src + item.directory

        # origin = local_src + item.directory
        # target = staging_src + item.directory
        # os.system('rsync -r -v -e "ssh -i $HOME/.ssh/tinkerlust" '+ str(origin) +' root@tinkerlust.com:' + str(target) + '/')

        '''
        --------------------------------------------------------------------------------------------------
        Staging server: local upload to tnklst.click
        --------------------------------------------------------------------------------------------------
        '''
        # local_src = '/Users/antonifs/Documents/tinkerlust/store_scraper/media/import/'
        # origin = local_src + item.directory
        # target = staging_src
        # os.system('rsync -r -v -e "ssh -i $HOME/tinkerstaging" '+ str(origin) +' root@tnklst.click:' + str(target) + '/')
        # logger.info("Done Rsyncing")

        '''
        --------------------------------------------------------------------------------------------------
        Staging server: local upload to tinkerlust.com
        --------------------------------------------------------------------------------------------------
        '''
        local_src = '/Users/antonifs/Documents/tinkerlust/store_scraper/media/import/'
        origin = local_src + item.directory
        target = '/var/www/html/magento/media/import/'
        os.system('rsync -r -v -e "ssh -i $HOME/tinkerlust" '+ str(origin) +' root@tinkerlust.com:' + str(target) + '/')
        logger.info("Done Rsyncing")

        d = str(origin)
        lsdir = os.listdir(d)
        image_count = len(lsdir)

        data_image = {
            'access_token': str(access_token),
            'sku': str(item.sku),
            'image_count': image_count
        }

        logger.info("Data: %s" % data_image)

        res = helpers.upload_images(data_image)

        logger.info("%s uploaded to Magento media" % res)

        item.status = 5
        item.save()

    else:
        logger.info("No item is uploaded")