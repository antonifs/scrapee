from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import truncatechars

MONITORING_STATUS_CHOICES = (
    (1, 'Draft'),
    (2, 'Scraped'),
    (3, 'Ignore'),
)

CATEGORY_STATUS_CHOICES = (
    (1, 'Draft'),
    (2, 'Scraped'),
    (3, 'Ignore'),
)

URL_STATUS_CHOICES = (
    (1, 'Draft'),
    (2, 'Scraped'),
    (3, 'Ignore'),
)

ITEM_STATUS_CHOICES = (
    (1, 'Draft'),
    (2, 'Scraped'),
    (3, 'Ignore'),
)


class Monitoring(models.Model):
    store_name = models.CharField(max_length=100)
    status = models.IntegerField(choices=MONITORING_STATUS_CHOICES)
    domain = models.CharField(max_length=200)
    monitoring_url = models.CharField(max_length=200)
    tag = models.CharField(max_length=100, default=None, null=True)
    attr = models.CharField(max_length=100, default=None, null=True)
    attr_val = models.CharField(max_length=100, default=None, null=True)
    tag_child = models.CharField(max_length=100, default=None, null=True)
    attr_child = models.CharField(max_length=100, default=None, null=True)
    attr_val_child = models.CharField(max_length=100, default=None, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.store_name

class Category(models.Model):

    category = models.CharField(max_length=100)
    cat_url = models.CharField(max_length=1000)
    status = models.IntegerField(choices=URL_STATUS_CHOICES)
    monitoring = models.ForeignKey(Monitoring, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    @property
    def short_url(self):
        return truncatechars(self.url, 50)

    def __unicode__(self):
        return self.category

class Url(models.Model):

    url = models.CharField(max_length=1000)
    status = models.IntegerField(choices=URL_STATUS_CHOICES)
    category = models.ForeignKey(Category, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    @property
    def short_url(self):
        return truncatechars(self.url, 50)

    def __unicode__(self):
        return self.url


class Item(models.Model):

    title = models.CharField(max_length=255)
    url = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    category = models.ForeignKey(Category, blank=True, null=True)
    category_raw = models.CharField(max_length=100, blank=True, null=True)
    sub_category_raw = models.CharField(max_length=100, blank=True, null=True)
    condition = models.CharField(max_length=255, blank=True, null=True)
    image_1 = models.CharField(max_length=255)
    image_2 = models.CharField(max_length=255)
    image_3 = models.CharField(max_length=255)
    image_4 = models.CharField(max_length=255, blank=True, null=True)
    image_5 = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    fabric = models.CharField(max_length=255, blank=True, null=True)
    currency = models.IntegerField()
    is_scrapped = models.IntegerField(blank=True, null=True)
    is_sold = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(choices=ITEM_STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    @property
    def short_url(self):
        return truncatechars(self.url, 50)

    def __unicode__(self):
        return self.title