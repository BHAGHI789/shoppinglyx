from audioop import reverse
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Customer,
    Product,
    Cart,
    OrderPlaced
)

class CustomerModeladmin(admin.ModelAdmin):
    list_display=['id','user','name','locality','city','zipcode','state']
admin.site.register(Customer,CustomerModeladmin)

class ProductModeladmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discounted_price','description','brand','category','product_image']
admin.site.register(Product,ProductModeladmin)

class ChartModeladmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']
admin.site.register(Cart,ChartModeladmin)
class OrderPlaceModeladmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity','ordered_date','status']
admin.site.register(OrderPlaced,OrderPlaceModeladmin)

