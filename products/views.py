from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt,csrf_protect #Add this



csv_filepathname="txt/matching_score.csv"
# csv_filepathname="txt/names_and_img2.csv"

import re
import csv
import datetime
import random
from django.db.models import Q
# Create your views here.

# import pycmf
import pandas as pd
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
    # a = User.objects.get(id = 5)
    # b = User.objects.get(id = 6)
    # Offer_a = Offer.objects.get(id = 1)
    # Offer_b = Offer.objects.get(id = 3)
    # c = ExchangeRequest()
    # c.user_from = a
    # c.user_to = b
    # c.Offer_requestfor = Offer_b
    # c.Offer_provide = Offer_a
    # c.status = 0
    # c.save()
    # d = ExchangeRequest()
    # d.user_from = b
    # d.user_to = a
    # d.Offer_requestfor = Offer_a
    # d.Offer_provide = Offer_b
    # d.status = 0
    # d.save()
    return render(request,'start.html')

def SearchPage(request):
    if request.method == "POST":
        print('POST got',request.POST['result'])
        try:
            product = ProductInfo.objects.get(Product_asin=request.POST['result'])
            # print('get product')
            us = User.objects.get(id = request.POST['user_object'])
            # print('get us')
            offer = Offer.objects.get(Offer_key=product,user =us)
            # print('get offer')
            like = Likes.objects.get(Offer=offer,User=request.user)
            # print('get like')
            if like.Like == 0:
                like.Like = 1
            else:
                like.Like = 0
            like.save()
        except:
            like = Likes()
            like.User = request.user
            like.Like = 1
            like.Offer = Offer.objects.get(Offer_asin = request.POST['result'],user=request.POST['user_object'])
            like.save()
    srh = request.GET['query']
    products = ProductInfo.objects.filter(Product_title__icontains=srh).values_list('Product_asin', flat=True)
    # for each in products:
    #     print(each)
    offer = Offer.objects.filter(Offer_asin__in = products)
    # like  = Likes.objects.filter(User = request.user).values_list('Offer',flat=True)

    # for each in offer:
    #     print('============',each.Offer_key.Product_title, each.Offer_asin)
    # print('===================================================================')
    location_sort = Fares.objects.filter(src_station_id=request.user.profileuser.location_station.station_id).order_by('oct_adt_fare')

    print(location_sort)
    like_ = Likes.objects.filter(User=request.user,Like=1).values_list('Offer',flat = True)
    like_list = list(like_)
    # print('=============like list:',like_list)


    params = {'products':offer, 'search':srh, 'sorted_location':location_sort,'like_list':like_list}

    return render(request,'search.html', params)


def ManageView(request):
    myOffer = Offer.objects.filter(user=request.user)
    params = {'Offer':myOffer}
    return render(request, 'manage.html',params)

def RequestView(request):
    received = ExchangeRequest.objects.filter(user_to=request.user)
    sent = ExchangeRequest.objects.filter(user_from=request.user)
    params = {'received':received, 'sent':sent}
    return render(request, 'request.html',params)

@csrf_exempt 
def ExchangeView(request):
    products = []
    count = 0
    value = request.GET['price'] #price

    current_user = request.user
    user_location = current_user.profileuser.location_station.station_id #location
    user_item = Offer.objects.filter(user=current_user).values_list('Offer_asin', flat=True)

    matching_score_sort = MatchingScore.objects.filter(user=current_user).order_by('-value')[:4]
    stations = Fares.objects.filter(oct_adt_fare__lte=10, src_station_id=user_location).exclude(dest_station_id=user_location).values_list('dest_station_id', flat=True)

    owners = UserProfile.objects.filter(location__in=stations).values_list('user', flat=True)
    for each in matching_score_sort:
        category = ProductCategory.objects.get(id=each.ProductCategory.id)
        asin = ProductInfo.objects.filter(Product_category_name=category, value__lte=float(value)*1.1, value__gte=float(value)*0.9).exclude(Product_asin__in=user_item).values_list('Product_asin', flat=True)
        products.append(Offer.objects.filter(Offer_asin__in = asin, user__in=owners)[:3])
    #owner = Offer.objects.filter(Offer_asin__in = asin).values_list('user', flat=True)

    # for o in owner:
    #    x = User.objects.get(id=o)
        # if (x.profileuser.location in stations):
        #    products.append(Offer.objects.filter(user=x).values_list('Offer_asin', flat=True))
    
    #params = {'destinations': stations, 'matching_score': matching_score_sort, 'products':products}
    '''
    df = pd.DataFrame(products)
    df = df.drop_duplicates(keep='first')
    res = []
    for column in df.columns:
        li = df[column].tolist()
        res.append(li)
    '''
    params = {'price': value, 'matching_score': matching_score_sort, 'products': products}
    return render(request, 'exchange.html', params)