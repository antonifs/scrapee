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
            # Save the content
            Item(title = object['product_name'],
                url = url.url,
                price = helpers.convert_money(object["price"]),
                image_1 = object['image_1'],
                image_2 = object['image_2'],
                image_3 = object['image_3'],
                image_4 = object['image_4'],
                image_5 = object['image_5'],
                is_sold = 1,
                status = 1,
                condition = object["condition"],
                currency = 1,
                is_scrapped = 1,

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
    item = Item.objects.filter(status=1).order_by('id').first()
    if item:

        token = helpers.get_token()

        # attributeset = helpers.get_all_attributeset(token)

        logger.info("Token: %s " % token)

        item.status = 2
        item.save()
    else:
        logger.info("Nothing can be uploaded")