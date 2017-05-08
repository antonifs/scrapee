from celery.task.schedules import crontab
from celery.decorators import periodic_task
from scrapee.utils import scrapers
from celery.utils.log import get_task_logger
from scrapee import settings


import requests
from helpers import *
import os
import urllib, json

from models import Monitoring, Category, Item, Url

logger = get_task_logger(__name__)

# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def scraper_url():

    '''
    :Flow
    - Scrap object based on given url
    - Write the result to Item table url
    import monitoree.tasks as tasks
    category = Category.objects.filter(status=1).order_by('id').first()
    from monitoree.models import Monitoring, Category, Item, Url
    '''
    category = Category.objects.filter(status=1).order_by('id').first()

    if category:

        monitoring = Monitoring.objects.get(id=category.monitoring_id)

        if category.current_pagination == 0:
            page = 1
        else:
            page = category.current_pagination

        url = str(category.cat_url) + str(category.query_string) + str(page)

        logger.info("Start scrapping %s" % url)
        item_urls = crawl(url,
                          monitoring.tag_child,
                          monitoring.attr_child,
                          monitoring.attr_val_child
                          )

        total = 0
        for item_url in item_urls:
            href = monitoring.domain + item_url['href']
            sc = Url.objects.filter(url = href)
            if sc.count() < 1:
                u = Url(url = href, status = 1, category_id=category.id)
                u.save()
                total += 1

        # increase the current pagination by 1
        obj = Category.objects.get(id=category.id)
        if obj.current_pagination == obj.total_pagination:
            obj.status = 2
            obj.save()
        else:
            obj.current_pagination = obj.current_pagination + 1
            obj.save()

        logger.info("End scrapping %s" % str(obj.current_pagination) )
    else:
        logger.info("No item could be scraped")


# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def scraper_url_styletribute():

    '''
    :Flow
    - Scrap object based on given url
    - Write the result to Item table url
    import monitoree.tasks as tasks
    category = Category.objects.filter(status=1).order_by('id').first()
    from monitoree.models import Monitoring, Category, Item, Url
    '''
    category = Category.objects.filter(status=1).filter(monitoring_id=2).filter(level=2).order_by('id').first()

    total = 0
    if category:

        monitoring = Monitoring.objects.get(id=category.monitoring_id)

        if category.current_pagination == 0:
            page = 1
        else:
            page = category.current_pagination

        # depends on the URL patern of the website target
        url = str(category.cat_url)

        # get item URL Only
        response = urllib.urlopen(url)
        data = json.loads(response.read())

        for object in data['products']:
            href = 'https://styletribute.com/product/' + object['urlpath']

            sc = Url.objects.filter(url = href)
            if sc.count() < 1:
                u = Url(url = href, status = 1, category_id=category.id)
                u.save()
                total += 1

        # increase the current pagination by 1
        obj = Category.objects.get(id=category.id)
        if obj.current_pagination == obj.total_pagination:
            obj.status = 2
            obj.save()
        else:
            obj.current_pagination = obj.current_pagination + 1
            obj.save()

        logger.info("End scrapping %s" % str(obj.current_pagination) )
    else:
        logger.info("No item could be scraped")

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
        try:
            # scrap the html content
            object = scrapers.scraper_content(url.url)

            category = url.url.split("/")[-3:-2]
            sub_category = url.url.split("/")[-2:-1]

            size = scrapers.get_size(str(url.url))

            if not Item.objects.filter(url=str(url.url)).exists():

                if not "bobobobo.com" in  url.url:

                    Item(title = object['product_name'],
                        url = str(url.url),
                        price = convert_money(object["price"]),
                        status = 1,
                        currency = 1,
                        size = size,
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

                # Khusus bobobo hanya simpan item yg discountnya > 40%
                else:
                    discount = scrapers.get_discount(str(url.url))
                    logger.info("BOBO: Discount %s " % discount)

                    if int(discount) > 40:
                        logger.info("BOBO: Discount greater than > 40 ")
                        # Save the content
                        Item(title = object['product_name'],
                            url = str(url.url),
                            price = convert_money(object["price"]),
                            discount = discount,
                            status = 1,
                            currency = 1,
                            size = size,
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
                    else:
                        pass

                logger.info("%s scraped and was saved" % url.id)
            else:
                logger.info("Item is existed")
        except:
            logger.info("Exception error")

        # update the status to
        obj_url = Url.objects.get(id=url.id)
        obj_url.status = 2
        obj_url.save()
    else:
        logger.info("No content can be scraped")

    logger.info("Scraping content end")

# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def scraper_content_styletributes():

    '''
    :Flow
    - Read Url table
    - Scrap object based on given url
    - Write the result to Item table
    - Update url object status to scraped (2)
    '''

    import urllib, json

    url = Url.objects.filter(status=1).filter(url__startswith='https://styletribute.com/').first()

    logger.info("URL: %s", str(url.url))

    if url:
        try:
            response = urllib.urlopen(str(url.url))
            data = json.loads(response.read())

            if not Item.objects.filter(url=str(url.url)).exists():

                domain = 'https://styletribute.com/media/'

                image_1 = domain + data['largeImages'][0]
                image_2 = domain + data['largeImages'][1]
                image_3 = domain + data['largeImages'][2]
                image_4 = domain + data['largeImages'][3]
                image_5 = domain + data['largeImages'][4]

                # Save the content
                Item(title = str(data['name']),
                    url = str(url.url),
                    price = convert_money(object["price"]),
                    discount = discount,
                    status = 1,
                    currency = 1,
                    size = data['shortDescription'],
                    image_1 = image_1,
                    image_2 = image_2,
                    image_3 = image_3,
                    image_4 = image_4,
                    image_5 = image_5,
                    category_raw = str(url.category),
                    sub_category_raw = str(url.category),
                    is_sold = 1,
                    brand = data['designer'],
                    condition = data["condition"],
                    is_scraped = True,
                    is_image_scraped = False,
                ).save()

                logger.info("%s scraped and was saved" % url.id)

            else:
                logger.info("Item is existed")
        except:
            logger.info("Exception error")

        # update the status to
        obj_url = Url.objects.get(id=url.id)
        obj_url.status = 2
        obj_url.save()
    else:
        logger.info("No content can be scraped")

    logger.info("Scraping content end")


@periodic_task(run_every=(crontab(hour="*", minute="3", day_of_week="*")))
def scraper_mage_upload():

    import os

    item = Item.objects.filter(status=1).order_by('id').first()
    att_set = u'Default'

    if item:
        logger.info("Uploading is started %s " % (item.title) )

        token = get_token()

        logger.info("token: %s" % token)

        access_token = token['access_token']

        # Convert attributeset from target standard to tinkerlust standard
        attribute_set = {
            'bags' : 'Tas',
            'accessories' : 'Aksesoris',
            'shoes' : 'Sepatu',
            'clothing': 'Pakaian (atasan)',
        }

        try:
            att_set = attribute_set[str(item.category_raw)]
        except:
            pass

        if att_set == u'Default':
            try:
                att_set = attribute_set[str(item.sub_category_raw)]
            except:
                pass

        attributeset = get_all_attributeset(access_token)
        att_set_id = attributeset['data'][att_set]

        brand_id = str([val for key, val in get_brand_id(item.brand, access_token)['data'].iteritems()][0])

        domain = get_domain(item.url)

        source = Monitoring.objects.filter(domain=domain).first()

        category_id = str(get_category_id(att_set, access_token)['data'][0])

        # get random vendor
        from random import randint
        attribute = source.attribute_ids.split(",")[randint(0,4)].split('#')

        data = {
                'name'              : str(item.title),
                'attribute_set_id'  : str(att_set_id),
                'weight'            : 3,
                'color'             : [9,7],
                'price'             : item.price,
                'description'       : '-',
                'short_description' : '-',
                'vendor_attribute'  : str(attribute[1]),
                'vendor_category'   : str(attribute[0]),
                'fabric'            : 3,
                'condition'         : 2,
                'category'          : category_id,
                'brand_id'          : brand_id,
                'source'            : str(source.domain),
                'access_token'      : str(access_token),
        }

        logger.info("Data: %s " % data)

        res = upload_product(data)

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
            img_name_1 = get_new_name(item.sku, item.image_1, '1')
            img_num += 1
            try:
                urllib.urlretrieve(img_url_1, directory + '/' + img_name_1)
            except:
                pass
        else:
            img_name_1 = ""

        if not img_url_2 == "":
            img_name_2 = get_new_name(item.sku, item.image_2, '2')
            img_num += 1
            try:
                urllib.urlretrieve(img_url_2, directory + '/' + img_name_2)
            except:
                pass
        else:
            img_name_2 = ""

        if not img_url_3 == "":
            img_name_3 = get_new_name(item.sku, item.image_3, '3')
            img_num += 1
            try:
                urllib.urlretrieve(img_url_3, directory + '/' + img_name_3)
            except:
                pass
        else:
            img_name_3 = ""

        if not img_url_4 == "":
            img_name_4 = get_new_name(item.sku, item.image_4, '4')
            img_num += 1
            try:
                urllib.urlretrieve(img_url_4, directory + '/' + img_name_4)
            except:
                pass
        else:
            img_name_4 = ""

        if not img_url_5 == "":
            img_name_5 = get_new_name(item.sku, item.image_5, '5')
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

        token = get_token()
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

        res = upload_images(data_image)

        logger.info("%s uploaded to Magento media" % res)

        item.status = 5
        item.save()

    else:
        logger.info("No item is uploaded")

@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def scraper_item_update():

    from datetime import datetime, timedelta

    # Update the item in Magento
    token = get_token()
    access_token = token['access_token']

    time_threshold = datetime.now() - timedelta(hours=2)

    # Get item which the item is created in Magento, and the updated-date is less than today
    item = Item.objects.filter(updated__lt=time_threshold).filter(status__gte=2).order_by('id').first()

    if item:

        title = item.title.replace(" ", "+")
        url = "http://www.bobobobo.com/page/women?q=" + title

        # get the sub category
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        cat = str(item.sub_category_raw)
        product = soup.find_all("div", {"id" : "collapse" + cat})
        category = product[0].find_all("a", {"class": "showUrl"})[0].text

        categories = get_category_id(category, access_token)['data']

        if len(categories) > 1:
            category_id = str(categories[0])
            sub_category_id = str(categories[1])
        else:
            category_id = str(categories[0])
            sub_category_id = str(categories[0])

        logger.info("Scrape the new properties updated of %s " % item.url)

        try:
            # scrap the html content
            object = scrapers.scraper_content(item.url)
            stock = scrapers.is_sold(item.url)

            if not "bobobobo.com" in str(item.url):

                # Update the content in local DB
                obj_url = Item.objects.get(id=item.id)
                obj_url.price = convert_money(object["price"])
                obj_url.new_category = category
                obj_url.stock = stock
                obj_url.save()

                data = {
                    'sku' : item.sku,
                    'price' : convert_money(object["price"]),
                    'qty' : stock,
                    'category': category_id,
                    'subcategory': sub_category_id,
                    'short_description':str(item.size),
                    'status': 'true',
                    'access_token' : str(access_token),
                }

                logger.info("The data: %s " % data)

                res = update_product(data)

                logger.info("The data: %s has been saved. %s and it's noy bobobobo" % (str(data), str(res)) )
            else:
                discount = get_discount(item.url)

                if discount > 40:
                    # Update the content in local DB
                    obj_url = Item.objects.get(id=item.id)
                    obj_url.price = convert_money(object["price"])
                    obj_url.stock = stock
                    obj_url.save()

                    # Update the item in Magento
                    token = get_token()
                    access_token = token['access_token']

                    data = {
                        'sku' : item.sku,
                        'price' : convert_money(object["price"]),
                        'qty' : stock,
                        'access_token' : str(access_token),
                    }

                    logger.info("The data: %s " % data)

                    res = update_product(data)
                    logger.info("The data: %s has been saved. %s. It have > 40 discount." % (str(data), str(res)) )
                else:
                    logger.info("Item %s discount is no longer > 40 percent" % str(data) )

        except:
            logger.info("Exception error")

            # Update the content in local DB
            obj_url = Item.objects.get(id=item.id)
            obj_url.stock = 0
            obj_url.save()

            logger.info("%s stock has been updated" % item.url)

            data = {
                'sku' : str(item.sku),
                'category': str(category),
                'subcategory': str(category),
                'short_description':str(item.size),
                'status': 'true',
                'access_token' : str(access_token),
            }

            logger.info("The data: %s " % data)
            res = update_product(data)

            logger.info("The data: %s has been saved. %s and it's no bobobobo" % (str(data), str(res)) )

    else:
        logger.info("No item updated")