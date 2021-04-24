from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
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
    if request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html',{'form':form})

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
    liked = False
    unliked = False

    wished = False
    unwished = False
    if request.method == "POST":
        if request.POST.get("form_type") == 'like_form':
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
                    liked = True

                else:
                    like.Like = 0
                    unliked = True

                like.save()
            except:
                like = Likes()
                like.User = request.user
                like.Like = 1
                like.Offer = Offer.objects.get(Offer_asin = request.POST['result'],user=request.POST['user_object'])
                like.save()
                liked = True

        elif request.POST.get("form_type") == 'wishlist_form':
            print('POST got',request.POST['result'])
            print('POST got', request.POST['user_object'])
            try:
                product = ProductInfo.objects.get(Product_asin=request.POST['result'])
                # print('get product')
                us = User.objects.get(id = request.POST['user_object'])
                # print('get us')
                offer = Offer.objects.get(Offer_key=product,user =us)
                # print('get offer')
                wish = Wish.objects.get(Offer=offer,User=request.user)
                if wish.Wish == 0:
                    wish.Wish = 1
                    wished = True
                else:
                    wish.Wish = 0
                    unwished = True
                wish.save()
            except:
                wish = Wish()
                wish.User = request.user
                wish.Wish = 1
                wish.Offer = Offer.objects.get(Offer_asin = request.POST['result'],user=request.POST['user_object'])
                wish.save()
                wished = True
    if liked:
        try:
            like_pref = LikePreference.objects.get(User=request.user, Category=product.Product_category_name)
            # print("get like_pref")
            like_pref.Count += 1
            like_pref.save()
        except:
            like_pref = LikePreference()
            like_pref.User = request.user
            like_pref.Category = product.Product_category_name
            like_pref.Count = 1
            like_pref.save()
        finally:
            print("Error")
    elif unliked:
        try:
            like_pref = LikePreference.objects.get(User=request.user, Category=product.Product_category_name)
            # print("get like_pref")
            like_pref.Count -= 1
            like_pref.save()
        except:
            like_pref = LikePreference()
            like_pref.User = request.user
            like_pref.Category = product.Product_category_name
            like_pref.Count = 0
            like_pref.save()
    
    if wished:
        try:
            wish_pref = WishPreference.objects.get(User=request.user, Category=product.Product_category_name)
            wish_pref += 1
            wish_pref.save()
        except:
            wish_pref = WishPreference()
            wish_pref.User = request.user
            wish_pref.Category = product.Product_category_name
            wish_pref.Wish = 1
            wish_pref.save()
    elif unwished:
        try:
            wish_pref = WishPreference.objects.get(User=request.user, Category=product.Product_category_name)
            wish_pref -= 1
            wish_pref.save()
        except:
            wish_pref = WishPreference()
            wish_pref.User = request.user
            wish_pref.Category = product.Product_category_name
            wish_pref.Wish = 0
            wish_pref.save()
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

    #print(location_sort)
    like_ = Likes.objects.filter(User=request.user,Like=1).values_list('Offer',flat = True)
    like_list = list(like_)
    # print('=============like list:',like_list)
    wish_ = Wish.objects.filter(User=request.user, Wish=1).values_list('Offer', flat = True)
    wish_list = list(wish_)

    params = {'products':offer, 'search':srh, 'sorted_location':location_sort,'like_list':like_list, 'wish_list': wish_list}

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
    if request.method =="POST":
        print("==========================")
        print(request.POST['offer_provide'])
        print(request.POST['offer_request'])
        a = ExchangeRequest()
        offer_request = Offer.objects.get(id=request.POST['offer_request'])
        offer_provide = Offer.objects.get(id=request.POST['offer_provide'])
        
        a.status = 0
        a.Offer_provide = offer_provide
        a.Offer_requestfor = offer_request
        a.user_from = request.user
        a.user_to = offer_request.user
        a.save()

        try:
            exchange_pref = ExchangePreference.objects.get(User=request.user, Category=product.Product_category_name)
            # print("get like_pref")
            exchange_pref.Exchange += 1
            exchange_pref.save()
        except:
            exchange_pref = ExchangePreference()
            exchange_pref.User = request.user
            exchange_pref.Category = offer_request.Offer_key.Product_category_name
            exchange_pref.Exchange = 1
            exchange_pref.save()

        return redirect('request')

    products = []
    count = 0
    value = request.GET['price'] #price
    offer_id = request.GET['offer_id']

    current_user = request.user
    user_location = current_user.profileuser.location_station.station_id #location
    user_item = Offer.objects.filter(user=current_user).values_list('Offer_asin', flat=True)
    # user_item_offer = Offer.objects.get(user=current_user,Offer_asin=)

    matching_score_sort = MatchingScore.objects.filter(user=current_user).order_by('-value')[:4]
    stations = Fares.objects.filter(oct_adt_fare__lte=10, src_station_id=user_location).exclude(dest_station_id=user_location).values_list('dest_station_id', flat=True)

    owners = UserProfile.objects.filter(location__in=stations).values_list('user', flat=True)
    for each in matching_score_sort:
        category = ProductCategory.objects.get(id=each.ProductCategory.id)
        asin = ProductInfo.objects.filter(Product_category_name=category, value__lte=float(value)*1.1, value__gte=float(value)*0.9).exclude(Product_asin__in=user_item).values_list('Product_asin', flat=True)
        products.append(Offer.objects.filter(Offer_asin__in = asin, user__in=owners)[:3])
    # owner = Offer.objects.filter(Offer_asin__in = asin).values_list('user', flat=True)

    #  for o in owner:
    #     x = User.objects.get(id=o)
    #      if (x.profileuser.location in stations):
    #         products.append(Offer.objects.filter(user=x).values_list('Offer_asin', flat=True))
    
    # params = {'destinations': stations, 'matching_score': matching_score_sort, 'products':products}
    
    # df = pd.DataFrame(products)
    # df = df.drop_duplicates(keep='first')
    # res = []
    # for column in df.columns:
    #     li = df[column].tolist()
    #     res.append(li)
    
    params = {'price': value, 'matching_score': matching_score_sort, 'products': products, 'offer_id':offer_id}
    return render(request, 'exchange.html', params)

def WishListView(request):
    mWishList = Wish.objects.filter(User=request.user)
    params = {'wishlist': mWishList}
    return render(request, 'wishlist.html', params)

def get_p(p, max_p, min_p):
    return (p - min_p) / (max_p - min_p)

def DemoView(request):

    customer_preference = []

    like_p = LikePreference()
    wish_p = WishPreference()
    exchange_p = ExchangePreference()

    p_like = 0
    p_wish = 0
    p_exchange = 0

    mLikePref = LikePreference.objects.filter(User=request.user).order_by('-Count')
    mWishPref = WishPreference.objects.filter(User=request.user).order_by('-Wish')
    mExchangePref = ExchangePreference.objects.filter(User=request.user).order_by('-Exchange')
    
    max_like = mLikePref[0].Count
    min_like = mLikePref[28].Count if len(mLikePref) == 29 else 0

    max_wish = mWishPref[0].Wish
    min_wish = mWishPref[28].Wish if len(mWishPref) == 29 else 0

    max_exchange = mExchangePref[0].Exchange
    min_exchange = mExchangePref[28].Exchange if len(mExchangePref) == 29 else 0

    for i in range(4122,4149):
        category = ProductCategory.objects.get(id=i)
        try:
            like_p = LikePreference.objects.get(User=request.user, Category_id=category)
            p_like = like_p.Count
        except:
            p_like = 0
        
        try:
            wish_p  = WishPreference.objects.get(User=request.user, Category_id=category)
            p_wish = wish_p.Wish
        except:
            p_wish = 0

        try:
            exchange_p = ExchangePreference.objects.get(User=request.user, Category_id=category)
            p_exchange = exchange_p.Exchange
        except:
            p_exchange = 0

        customer_preference.append(get_p(p_like, max_like, min_like) + get_p(p_wish, max_wish, min_wish) + get_p(p_exchange, max_exchange, min_exchange))

    params = {'max_like': max_like, 'min_like': min_like, 
                'max_wish': max_wish, 'min_wish': min_wish, 
                'max_exchange': max_exchange, 'min_exchange': min_exchange,
                'customer_preference': customer_preference}
    
    return render(request, 'demo.html', params)