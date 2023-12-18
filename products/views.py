from django.shortcuts import render,get_object_or_404,redirect,HttpResponse,HttpResponseRedirect
from django.contrib import messages 
from django.http import JsonResponse
import razorpay

from .models import *
# Create your views here.
def anime_collection(request):

    category_obj = Category.objects.get(slug='anime-collection')
    print(category_obj)
    context={
        'background_image_url':'http://192.168.101.40:8000/{}'.format(category_obj.background_image),
        'slogen':category_obj.slogen
        
    }

    products = Product.objects.filter(category=category_obj)
    product_count = products.count()

    
    return render(request,'products/anime_collection.html',{'context':context,'products':products,'product_count':product_count})



def hand_designs(request):
    category_obj = Category.objects.get(category_name='Hand Designs Collection')
     
    context={   
        'background_image_url':'http://192.168.101.40:8000/{}'.format(category_obj.background_image),
        'slogen':category_obj.slogen
        
    }

    products = Product.objects.filter(category=category_obj)

    
    return render(request,'products/hand_made_collection.html',{'context':context,'products':products})


def get_product(request,slug):
    product_obj = Product.objects.get(slug=slug)
    product = Product.objects.filter(category=product_obj.category).exclude(slug=product_obj.slug)
    product_images = ProductImage.objects.filter(product__slug=slug)
    return render(request,'products/product.html',{'product_images':product_images,'product_obj':product_obj,'product':product})


def get_info(request):
    if request.method == "POST":
        selected_color = request.POST.get("selected_color")
        # Process the selected color, e.g., save it to the database, perform an action, etc.

        return JsonResponse({"message": "Color data received and processed."})
    
from django.http import HttpResponse



def add_to_wishlist_or_bag(request,uid):
    if request.method == 'POST':
        button_value = request.POST.get('action', None)
        print(button_value)
        if button_value =='add to wishlist':
            product = get_object_or_404(Product,uid=uid)
            wishlist_item, created = WishlistItem.objects.get_or_create(
            user=request.user,
            product=product,
            size = request.POST.get('size_name'),
            color = 'ffffff'
            )
            if created:

                print('wishlist')
                return redirect('wishlist')
        if button_value == 'add to bag':
            product = get_object_or_404(Product,uid=uid)
            bag = Bag.objects.get_or_create(user=request.user,is_paid=False)
            bag_item, created = BagItems.objects.get_or_create(
            bag = Bag.objects.get(user=request.user,is_paid=False),
            product=product,
            size = request.POST.get('size_name'),
            color = 'ffffff',
            quantity = request.POST.get('quantity')
            )
            bag_item.save()
            print('cart')
            return redirect('bag')
        


    
    # You might want to add a default response for other cases
    return HttpResponse('Invalid request')

def add_item_of_wishlist_in_cart(request,wishlist_item_id):
    if request.method=='POST':
        bag_id = Bag.objects.get_or_create(user=request.user,is_paid=False)
        wishlist_item = WishlistItem.objects.get(uid=wishlist_item_id)
        bag_item,created = BagItems.objects.get_or_create(
            bag = Bag.objects.get(user=request.user,is_paid=False),
            product=wishlist_item.product,
            size = wishlist_item.size,
            color = wishlist_item.color,
        )
        if created:
            wishlist_item.delete()
            
            return redirect('bag')
    return HttpResponse('Invalid request')
    
        


    


def remove_wishlist_item(request,wishlist_item_id):
    wishlist_item = get_object_or_404(WishlistItem, uid=wishlist_item_id, user=request.user)
    
    wishlist_item.delete()
    return redirect('wishlist')

def remove_bag_item(request,bag_item_id):
   

    bag_item = get_object_or_404(BagItems,uid=bag_item_id)
    bag_item.delete()
    return redirect('bag')

def embroidery_collection(request):

    category_obj = Category.objects.get(slug='embroidery-collection')
    print(category_obj)
    context={
        'background_image_url':'http://192.168.101.40:8000/{}'.format(category_obj.background_image),
        'slogen':category_obj.slogen
        
    }

    products = Product.objects.filter(category=category_obj)

    
    return render(request,'products/embroidery_collection.html',{'context':context,'products':products})

def casual_collection(request):

    category_obj = Category.objects.get(category_name='Casual Collection')
    print(category_obj)
  
    

    products = Product.objects.filter(category=category_obj)
    product_count = products.count()

    
    return render(request,'products/casual_collection.html',{'products':products,'product_count':product_count,'category_obj':category_obj})

# This will print the name of each field

def update_quantity(request,bag_item_id):
    if request.method=='POST':
        quantity = int(request.POST.get('quantity'))
        bag_obj = get_object_or_404(BagItems,uid=bag_item_id)
        bag_obj.quantity = quantity
        bag_obj.save()
    return redirect('bag')


    

from django.db.models import Q
from django.shortcuts import render
from .models import Product

def search_view(request):
    query = request.GET.get('q')
    if query:
        results = Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(product_description__icontains=query) |
            Q(category__category_name__icontains=query)
        )
    else:
        results = Product.objects.all()

    return render(request, 'products/search_results.html', {'results': results, 'query': query})
