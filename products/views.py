from django.shortcuts import render
from .models import Product
from django.views.generic import ListView, DetailView
# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
