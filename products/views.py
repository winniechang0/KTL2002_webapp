from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

csv_filepathname="txt/matching_score.csv"
# csv_filepathname="txt/names_and_img2.csv"

import re
import csv
import datetime
import random
from django.db.models import Q
# Create your views here.

# import pycmf
# import pandas as pd
# import numpy as numpyfrom pathlib import Path        
    


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
    cat = ProductCategory.objects.all()
    params = {'ProductCat': cat}
    addoffer = Offer()
    if request.method == 'POST':
        if request.POST.get('offername'):
            try: 
                offerkey = ProductInfo.objects.get(Product_title=request.POST.get('offername'))
                addoffer.Offer_key = offerkey
                addoffer.Offer_asin = offerkey.Product_asin
                addoffer.Offer_cat = offerkey.Product_category_name
                addoffer.user = request.user
                addoffer.save()
                print('=============================created')
            except:
                offerkey = ProductInfo()
                offerkey.Product_title = request.POST.get('offername')
                offerkey.Product_asin = random.randint(1000000,9999999)
                offerkey.Product_category_name = ProductCategory.objects.get(id = request.POST.get('cat'))
                offerkey.value = request.POST.get('value')
                offerkey.save()
                addoffer.Offer_key = offerkey
                addoffer.Offer_asin = offerkey.Product_asin
                addoffer.Offer_cat = offerkey.Product_category_name
                addoffer.user = request.user
                addoffer.save()
                print('=============================created2')

            

    return render(request, 'add_offer.html',params)


def LoginView(request):
    try:
        print('------------------------------------------------------')
        username=request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('HomeView')
        else:
            print('fail')
            return render(request, 'login.html')
    except:
        print('123------------------------------------------------------')
        return render(request, 'login.html')

def SignUpView(request):
    return render(request, 'signup.html')

def LogoutView(request):
    auth_logout(request)
    return render(request, "logout.html")

def HomeView(request):
    # dataReader = csv.reader(open(csv_filepathname,encoding='utf-8'),delimiter=',', quotechar='"')
    # for row in dataReader:
    #     user = User.objects.get(username=row[0])
    #     for i in range(4122,4149):
    #         cat = ProductCategory.objects.get(id = i)
    #         a = MatchingScore()
    #         a.user = user
    #         a.ProductCategory = cat
    #         a.value = row[i-4121]
    #         a.save()
    #         print('saved',user.username)
        
        

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
    location_sort = Fares.objects.filter(src_station_id=request.user.profileuser.location_station.station_id).order_by('oct_adt_fare')

    print(location_sort)

    params = {'products':offer, 'search':srh, 'sorted_location':location_sort}
    return render(request,'search.html', params)


def ManageView(request):
    myOffer = Offer.objects.filter(user=request.user)
    params = {'Offer':myOffer}
    return render(request, 'manage.html',params)

def ExchangeView(request):
    return render(request, 'exchange.html')