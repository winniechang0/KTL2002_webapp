from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    location = models.IntegerField()


class Product(models.Model):
    title = models.CharField(max_length=50)
    value = models.IntegerField()

class Wish(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Fares(models.Model):
    src_station_id = models.IntegerField()
    dest_station_id = models.IntegerField()
    oct_adt_fare = models.FloatField()

class Station(models.Model):
    station_name = models.CharField(max_length=50)
    station_id = models.IntegerField()

class ProductCategory(models.Model):
    product_category_name = models.CharField(max_length=100)
    # product_category_name_english = models.CharField(max_length=100)

class ProductInfo(models.Model):
    Product_title = models.CharField(max_length = 300)
    Product_asin = models.CharField(max_length=50)
    Product_category_name = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    Product_image = models.CharField(max_length = 500)

class Offer(models.Model):
    Offer_asin = models.CharField(max_length = 50)
    Offer_key = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Offer_date = models.DateField()
    Offer_cat = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

class Likes(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    Like = models.IntegerField(default=0)
    Like_date = models.DateField()
    Offer = models.ForeignKey(Offer, on_delete=models.CASCADE)

class ProductAssociation_matrix(models.Model):
    Src_Product_Cat = models.ForeignKey(ProductCategory,on_delete=models.CASCADE , related_name="Src_Product_Cat")
    Dest_Product_Cat = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="Dest_Product_Cat")
    value = models.FloatField(default=0)

class CustomerPreference_model(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    ProductCategory = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    value = models.FloatField(default=0)




