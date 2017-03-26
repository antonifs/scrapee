from django.contrib import admin
from .models import Category, Item, Monitoring, Url

from .helpers import crawl

def fetch_categories(self, request, queryset):
    monitoring = queryset.first()
    categories = crawl(monitoring.monitoring_url, monitoring.tag, monitoring.attr, monitoring.attr_val)

    total = 0
    for category in categories:
        href = monitoring.domain + category['href']
        sc = Category.objects.filter(cat_url = category['href'])
        if sc.count() < 1:
            cat = Category(category = category.text, cat_url = href, status = 1, monitoring=monitoring)
            cat.save()
            total += 1

    mon = Monitoring.objects.get(id=monitoring.id)
    mon.status = 2
    mon.save()

    self.message_user(request, "%s successfully fetched." % total)

def fetch_url_item(self, request, queryset):
    category = queryset.first()
    monitoring = Monitoring.objects.get(id=category.monitoring_id)
    item_urls = crawl(category.cat_url, monitoring.tag_child, monitoring.attr_child, monitoring.attr_val_child)

    for item_url in item_urls:
        href = monitoring.domain + item_url['href']
        sc = Url.objects.filter(url = href)
        if sc.count() < 1:
            u = Url(url = href, status = 1, category_id=category.id)
            u.save()

    c = Category.objects.get(id=category.id)
    c.status = 2
    c.save()

    total = 1

    self.message_user(request, "%s successfully fetched." % total)

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ["id", "category", "cat_url", "status", "created"]
    list_display_links = ["category"]
    list_filter = ["updated"]
    search_fields = ["category"]
    actions = [fetch_url_item]
    class Meta:
        ordering = ['pk']
        model = Category

@admin.register(Url)
class UrlModelAdmin(admin.ModelAdmin):
    list_display = ["id", "short_url", "status", "created"]
    list_display_links = ["short_url"]
    list_filter = ["updated", "created"]
    search_fields = ["short_url", "status"]
    class Meta:
        model = Url

@admin.register(Item)
class ItemModelAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "status", "condition", "created"]
    list_display_links = ["title"]
    list_filter = ["updated", "created"]
    search_fields = ["title", "status"]
    class Meta:
        model = Item

@admin.register(Monitoring)
class MonitoringModelAdmin(admin.ModelAdmin):
    list_display = ["id", "store_name", "status", "domain", "created"]
    list_display_links = ["store_name"]
    list_filter = ["updated", "created"]
    search_fields = ["store_name"]
    actions = [fetch_categories]
    class Meta:
        model = Monitoring
