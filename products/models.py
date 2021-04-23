from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Station(models.Model):
    station_name = models.CharField(max_length=50)
    station_id = models.IntegerField()
    
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    location = models.IntegerField()

class UserProfile2(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="profileuser")
    location_station = models.ForeignKey(Station, on_delete=models.CASCADE)

class Product(models.Model):
    title = models.CharField(max_length=50)
    value = models.IntegerField()


class Fares(models.Model):
    src_station_id = models.IntegerField()
    dest_station_id = models.IntegerField()
    oct_adt_fare = models.FloatField()



class ProductCategory(models.Model):
    product_category_name = models.CharField(max_length=100)
    # product_category_name_english = models.CharField(max_length=100)

class ProductInfo(models.Model):
    Product_title = models.CharField(max_length = 300)
    Product_asin = models.CharField(max_length=50)
    Product_category_name = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    Product_image = models.CharField(max_length = 500)
    value = models.FloatField()

class Offer(models.Model):
    Offer_asin = models.CharField(max_length = 50)
    Offer_key = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Offer_date = models.DateField()
    Offer_cat = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

class Likes(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    Like = models.IntegerField(default=0)
    # Like_date = models.DateField()
    Offer = models.ForeignKey(Offer, on_delete=models.CASCADE)

class ProductAssociation_matrix(models.Model):
    Src_Product_Cat = models.ForeignKey(ProductCategory,on_delete=models.CASCADE , related_name="Src_Product_Cat")
    Dest_Product_Cat = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="Dest_Product_Cat")
    value = models.FloatField(default=0)

class CustomerPreference_model(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    ProductCategory = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    value = models.FloatField(default=0)

class MatchingScore(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ProductCategory = models.ForeignKey(ProductCategory,on_delete=models.CASCADE)
    value = models.FloatField()

class ExchangeRequest(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user_from")
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_to")
    # 0 = sent but not yet ans/ 1 = finished(accept) / 2= declined
    Offer_requestfor = models.ForeignKey(Offer,on_delete=models.CASCADE,related_name="Offer_requestfor")
    Offer_provide = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="Offer_provide")
    status = models.IntegerField()

class Wish(models.Model):
    #title = models.CharField(max_length=50)
    # date = models.DateTimeField()
    Wish = models.IntegerField(default=0)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Offer = models.ForeignKey(Offer, on_delete=models.CASCADE)

class LikePreference(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    Count = models.IntegerField(default=0)




