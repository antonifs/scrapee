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
    (0, 'New'),
    (1, 'Scraped'),
    (2, 'Item Created'),
    (3, 'Image Downloaded'),
    (4, 'Image Uploaded'),
    (5, 'Completed'),
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
    vendor_attribute = models.IntegerField(null=True, blank=True)
    vendor_category = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.store_name

class Category(models.Model):
    category = models.CharField(max_length=100)
    category_parent = models.CharField(max_length=100, null=True)
    level = models.IntegerField(default=1)
    cat_url = models.CharField(max_length=1000)
    status = models.IntegerField(choices=URL_STATUS_CHOICES)
    monitoring = models.ForeignKey(Monitoring, blank=True, null=True)
    block_tag = models.CharField(max_length=100, null=True)
    block_attribute = models.CharField(max_length=100, null=True)
    block_value = models.CharField(max_length=100, null=True)
    item_tag = models.CharField(max_length=100, null=True)
    item_attribute = models.CharField(max_length=100, null=True)
    item_value = models.CharField(max_length=100, null=True)
    total_pagination = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    @property
    def short_url(self):
        return truncatechars(self.url, 50)

    def __unicode__(self):
        return self.category

class ParentCategoryManager(models.Manager):
    def get_queryset(self):
        return super(ParentCategoryManager, self).get_queryset().filter(level=1)

class ParentCategory(Category):
    class Meta:
        proxy = True

    objects = ParentCategoryManager()

class SubcategoryManager(models.Manager):
    def get_queryset(self):
        return super(SubcategoryManager, self).get_queryset().filter(level=2)

class Subcategory(Category):
    class Meta:
        proxy = True

    objects = SubcategoryManager()

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
    url = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sku = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True)
    category_raw = models.CharField(max_length=255, blank=True, null=True)
    sub_category_raw = models.CharField(max_length=255, blank=True, null=True)
    condition = models.CharField(max_length=255, blank=True, null=True)
    image_1 = models.CharField(max_length=255)
    image_2 = models.CharField(max_length=255)
    image_3 = models.CharField(max_length=255)
    image_4 = models.CharField(max_length=255, blank=True, null=True)
    image_5 = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    fabric = models.CharField(max_length=255, blank=True, null=True)
    currency = models.IntegerField()
    is_scraped = models.BooleanField()
    is_sold = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(choices=ITEM_STATUS_CHOICES)
    brand = models.CharField(max_length=100, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_image_scraped = models.BooleanField()
    directory = models.CharField(max_length=255, null=True, blank=True)
    image_name_1 = models.CharField(max_length=255, blank=True, null=True)
    image_name_2 = models.CharField(max_length=255, blank=True, null=True)
    image_name_3 = models.CharField(max_length=255, blank=True, null=True)
    image_name_4 = models.CharField(max_length=255, blank=True, null=True)
    image_name_5 = models.CharField(max_length=255, blank=True, null=True)

    @property
    def short_url(self):
        return truncatechars(self.url, 50)

    def __unicode__(self):
        return self.title