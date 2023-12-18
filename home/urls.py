from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    
    path('',home,name='home'),
    path('wishlist',wishlist,name='wishlist'),
    path('call_us',call_us,name='call_us'),
    path('bag',bag,name='bag'),
    path('address',address,name='address'),
   
]
