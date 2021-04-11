from django.contrib import admin
from .models import *
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'value')
    search_fields = ('title', 'value')

class StationAdmin(admin.ModelAdmin):
    list_display = ('id','station_name','station_id')
    search_fields = ('station_name','station_id')    

class FaresAdmin(admin.ModelAdmin):
    list_display = ('src_station_id','dest_station_id','oct_adt_fare')
    search_fields = ('src_station_id','dest_station_id','oct_adl_fare')

admin.site.register(Product, ProductAdmin)
admin.site.register(Station, StationAdmin)
admin.site.register(Fares, FaresAdmin)
