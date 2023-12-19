from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    
    path('anime_collection/', anime_collection,name='anime_collection'),
    path('hand_designs/',hand_designs,name='hand_designs'),
    path('hoodies/',hoodies,name='hoodies'),
    path('get_product/<slug>',get_product,name='get_product'),
    path('get_info',get_info,name='get_info'),
    path('add_to_wishlist_or_bag/<uid>',add_to_wishlist_or_bag,name='add_to_wishlist_or_bag'),
    path('embroidery_collection',embroidery_collection,name='embroidery_collection'),
    path('casual-collection',casual_collection,name='casual_collection'),
    path('wishlist/delete/<str:wishlist_item_id>/', remove_wishlist_item, name='remove_wishlist_item'),
    path('bag/delete/<str:bag_item_id>/', remove_bag_item, name='remove_bag_item'),
    path('add_item_of_wishlist_in_cart/<str:wishlist_item_id>',add_item_of_wishlist_in_cart,name='add_item_of_wishlist_in_cart'),
    path('update_quantity/<str:bag_item_id>',update_quantity,name='update_quantity'),
    path('search/', search_view, name='search'),

 
   
]

