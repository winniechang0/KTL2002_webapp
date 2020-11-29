from django.contrib import admin
from .models import Product
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'value')
    search_fields = ('title', 'value')
    
admin.site.register(Product, ProductAdmin)
