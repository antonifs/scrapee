from django.contrib import admin
from .models import Category, Item, Monitoring, Url, ParentCategory, Subcategory
from django.utils.translation import ugettext_lazy as _
from django.contrib.humanize.templatetags.humanize import intcomma
import urllib, json

from scrapee.utils.scrapers import *

def fetch_categories(self, request, queryset):
    monitoring = queryset.first()
    categories = crawl(monitoring.monitoring_url,
                       monitoring.tag,
                       monitoring.attr,
                       monitoring.attr_val
                       )

    total = 0
    for category in categories:
        href = monitoring.domain + category['href']
        sc = Category.objects.filter(cat_url = href)

        if sc.count() < 1:
            cat = Category(category = category.text.strip(),
                           cat_url = href,
                           status = 1,
                           level = 1,
                           monitoring=monitoring
                           )
            cat.save()
            total += 1

    mon = Monitoring.objects.get(id=monitoring.id)
    mon.status = 2
    mon.save()

    self.message_user(request, "%s successfully fetched." % total)

def fetch_styletribute_categories(self, request, queryset):

    monitoring = queryset.first()

    ids = [5, 428, 4, 63, 6]

    response = urllib.urlopen(monitoring.domain)

    data = json.loads(response.read())

    total = 0
    for object in data[0]['children']:
        if object['id'] in ids:
            href = monitoring.monitoring_url + 'category=' + str(object['id']) + '&category_id=1225'
            sc = Category.objects.filter(cat_url = href)

            if sc.count() < 1:
                cat = Category(category = object['name'],
                               cat_url = href,
                               status = 1,
                               level = 1,
                               monitoring=monitoring
                               )
                cat.save()
                total += 1

                for o in object['children']:
                    href2 = monitoring.monitoring_url + 'category=' + str(o['id']) + '&category_id=1225'
                    sc = Category.objects.filter(cat_url = href2)

                    if sc.count() < 1:
                        cat = Category(category = o['name'],
                                       cat_url = href2,
                                       status = 1,
                                       level = 2,
                                       monitoring=monitoring
                                       )
                        cat.save()
                        total += 1

    mon = Monitoring.objects.get(id=monitoring.id)
    mon.status = 2
    mon.save()

    self.message_user(request, "%s successfully fetched." % total)



def fetch_sub_category(self, request, queryset):
    cat = queryset.first()

    if cat.status == 1 and cat.item_tag != None and cat.item_attribute != None:

        categories = crawl(cat.cat_url,
                           cat.item_tag,
                           cat.item_attribute,
                           cat.item_value
                           )
        total = 0
        for category in categories:
            domain = "http://www.bobobobo.com"
            href = domain + category['href']
            sc = Category.objects.filter(category = category.text)



            if sc.count() < 1:
                sub_category = Category(category = category.text.strip(),
                               category_parent = cat.category,
                               cat_url = href,
                               status = 1,
                               level = 2,
                               monitoring=cat.monitoring
                               )
                sub_category.save()
                total += 1

        mon = Category.objects.get(id=cat.id)
        mon.status = 2
        mon.save()

        self.message_user(request, "%s successfully fetched." % total)
    else:
        self.message_user(request, "Couldn't be fetched. Ensure the status is draft, with tag and attributes has a proper value")

def stop_fetch_url(self, request, queryset):
    for q in queryset:
        if Category.objects.filter(id=q.id).exists():
            obj = Category.objects.filter(id=q.id).first()
            obj.status = 3
            obj.save()
    self.message_user(request, "%s successfully stopped.")

def set_to_draft(self, request, queryset):
    for q in queryset:
        if Url.objects.filter(id=q.id).exists():
            obj = Url.objects.filter(id=q.id).first()
            obj.status = 1
            obj.save()

def set_to_scraped(self, request, queryset):
    for q in queryset:
        if Url.objects.filter(id=q.id).exists():
            obj = Url.objects.filter(id=q.id).first()
            obj.status = 2
            obj.save()

def set_to_item_created(self, request, queryset):
    for q in queryset:
        if Item.objects.filter(id=q.id).exists():
            obj = Item.objects.filter(id=q.id).first()
            obj.status = 2
            obj.save()

def set_to_item_scraped(self, request, queryset):
    for q in queryset:
        if Item.objects.filter(id=q.id).exists():
            obj = Item.objects.filter(id=q.id).first()
            obj.status = 1
            obj.save()

# def button(self, obj):
#     return mark_safe('<input type="button">')
# title.short_description = 'Action'
# title.allow_tags = True

@admin.register(ParentCategory)
class ParentCategoryModelAdmin(admin.ModelAdmin):
    list_display = ["id", "monitoring", "category", "cat_url", "status", "created"]
    list_display_links = ["category"]
    list_filter = ["monitoring", "updated"]
    search_fields = ["category"]
    actions = [fetch_sub_category]
    class Meta:
        ordering = ['pk']
        model = Category

@admin.register(Subcategory)
class SubcategoryModelAdmin(admin.ModelAdmin):
    list_display = ["id", "monitoring", "category", "category_parent", "cat_url", "status", "created"]
    list_display_links = ["category"]
    list_filter = ["monitoring", "updated"]
    search_fields = ["category"]
    actions = [stop_fetch_url]
    class Meta:
        ordering = ['pk']
        model = Category

@admin.register(Url)
class UrlModelAdmin(admin.ModelAdmin):
    list_display = ["id", "short_url", "status", "created"]
    list_display_links = ["short_url"]
    list_filter = ["status", "updated", "created"]
    search_fields = ["url", "status"]
    actions = [set_to_draft, set_to_scraped]
    class Meta:
        model = Url

@admin.register(Item)
class ItemModelAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "status", "sku", "discount", "formatted_amount", "condition", "updated", "created"]
    list_display_links = ["title"]
    list_filter = [ "sub_category_raw", "status", "created"]
    search_fields = ["title", "status", "category_raw", "sku", "sub_category_raw"]
    actions = [set_to_item_created, set_to_item_scraped]

    def formatted_amount(self, obj):
        return "IDR. %s%s" % (intcomma(int(obj.price)), ("%0.2f" % obj.price)[-3:])

    class Meta:
        model = Item

@admin.register(Monitoring)
class MonitoringModelAdmin(admin.ModelAdmin):
    list_display = ["id", "store_name", "status", "domain", "created"]
    list_display_links = ["store_name"]
    list_filter = ["updated", "created"]
    search_fields = ["store_name"]
    actions = [fetch_categories, fetch_styletribute_categories]
    class Meta:
        model = Monitoring
