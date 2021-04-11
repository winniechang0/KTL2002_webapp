from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView
from django.contrib.auth import logout as auth_logout

csv_filepathname="txt/Product_association_matrix.csv"
# csv_filepathname="txt/names_and_img2.csv"

import re
import csv
import datetime
import random
from django.db.models import Q
# Create your views here.


        
    


class ProductListView(ListView):
    model = ProductInfo
    template_name = 'start.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
        result = super(ProductListView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            print('==============the user searched', query)
            postresults = ProductInfo.objects.filter(Product_title__contains=query)
            # results_list = list(postresults)
            result = postresults
        else :
            result = None
        return result
    

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

def AddOfferView(request):
    # for i in range(4122, 4149):
    #     cat = ProductCategory.objects.get(id = i)
    #     # li = []
    #     # for i in range(1,45972):
    #     a = Offer.objects.filter(Offer_cat=cat)
    #     tmp = ProductInfo.objects.get(id = 1)
    #     for each in a:
    #         try:
    #             b = ProductInfo.objects.get(Product_asin__contains=each.Offer_asin)
    #             each.Offer_key = b
    #         except ProductInfo.DoesNotExist:
    #             print("each.offer key =",each.Offer_asin)
    #             each.Offer_key = tmp
    #         each.save()
    #     print("finish, ",cat.product_category_name)
        
        # print(b.Product_title)
        # a.Offer_key = b
        # a.save()
    # with open('Video_Games.txt', 'w') as f:
    #     for item in li:
    #         f.write("%s\n" % item)
                


    # text_file = open("Video_Games.txt","w")
    # cat = ProductCategory.objects.get(product_category_name="Video_Games")
    # filtered = Offer.objects.filter(Offer_cat=cat)
    # for each in filtered:
    #     text_file.write(each.Offer_asin)
    #     text_file.write("\n")
    # print("filtered=============", filtered)
    # for i in range(1,)

    # dataReader = csv.reader(open(csv_filepathname, encoding='utf-8'), delimiter=',', quotechar='"')

    
    # for row in dataReader:
    #     a = Offer()
    #     a.Offer_asin =row[1]
    #     a.Offer_cat = ProductCategory.objects.get(product_category_name=row[2])
    #     a.user = User.objects.get(username = row[0])
    #     a.save()
    #     print('hi')

        
    # print('finished')
    # i = 1
    # for row in dataReader:
    #     a = ProductInfo.objects.get(Product_asin=row[0])
    #     a.Product_category_name = ProductCategory.objects.get(product_category_name=row[3])
    #     a.save()
    dataReader = csv.reader(open(csv_filepathname, encoding='utf-8'), delimiter=',', quotechar='"')
    i= 4122
    for row in dataReader:
        for j in range(4122,4149):
            print('hihihi', row[j-4122])
            a = ProductAssociation_matrix()
            a.Src_Product_Cat = ProductCategory.objects.get(id=i)
            a.Dest_Product_Cat = ProductCategory.objects.get(id=j)
            a.value = row[j-4122]
            a.save()
        i+=1


    print('finish')


    return render(request, 'add_offer.html')


def LoginView(request):
    return render(request, 'login.html')

def SignUpView(request):
    return render(request, 'signup.html')

def LogoutView(request):
    auth_logout(request)
    return render(request, "logout.html")

def HomeView(request):
    return render(request,'start.html')

def SearchPage(request):
    srh = request.GET['query']
    products = ProductInfo.objects.filter(Product_title__icontains=srh).values_list('Product_asin', flat=True)
    for each in products:
        print(each)
    offer = Offer.objects.filter(Offer_asin__in = products)
    # like  = Likes.objects.filter(User = request.user).values_list('Offer',flat=True)

    for each in offer:
        print('============',each.Offer_key.Product_title, each.Offer_asin)
    print('===================================================================')
    params = {'products':offer, 'search':srh}
    return render(request,'search.html', params)