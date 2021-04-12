from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, login

csv_filepathname="txt/preference_matrix.csv"
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
    # for i in range(1,12088):
    #     try :
    #         user = User.objects.get(id = i)
    #         Profile = UserProfile2()
    #         Profile.user = user
    #         Profile.location_station = Station.objects.get(station_id = user.last_name)
    #         Profile.save()
    #     except user.DoesNotExist:
    #         print('User Does Not Exist')
    # print('finish')


    return render(request, 'add_offer.html')


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