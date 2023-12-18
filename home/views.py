from django.shortcuts import render,redirect,HttpResponseRedirect,get_object_or_404
from products.models import *
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from products.models import Product
from django.contrib.auth.decorators import login_required
from products.models import WishlistItem,Product,Bag,BagItems
import razorpay
from django.conf import settings
# Create your views here.
def home(request):
    categories = Category.objects.all().order_by('-created_at')
    category_obj = Category.objects.get(slug='casual-collection')
    products = Product.objects.all()

    return render(request, 'home/home.html',{'categories':categories ,'products':products})


def wishlist(request):
    if request.user.is_authenticated:
        wishlist_items = WishlistItem.objects.filter(user=request.user).prefetch_related('product__product_images').all()
  

        return render(request, 'home/wishlist.html',{'wishlist_items':wishlist_items })
    else:
        return render(request,'accounts/login.html') # Or any appropriate response for a successful POST request.
    
    # Handle GET requests (initial page load) here.
    # Render the wishlist page or provide a response for GET requests.
    
    
    # You can add code to process the selected size for the wishlist functionality.
    



        
def call_us(request):
    return render(request,'contect.html')
def bag(request):
    
    user = request.user
    if user.is_authenticated:
        try:
            bag_obj = Bag.objects.get(user=user,is_paid=False)
            bag_items = BagItems.objects.filter(bag=bag_obj).prefetch_related('product__product_images').all()
            item_count =  bag_items.count()
            item_cost_sum = 0
            for item in bag_items:
                item_cost_sum += item.total_price
            print(bag_obj)
            return render(request,'home/bag.html',{'bag_items':bag_items,'bag_obj':bag_obj,'item_count':item_count ,'item_cost_sum':item_cost_sum})
        except:
            bag_obj = None
            print(bag_obj)
            return render(request,'home/bag.html',{'bag_obj':bag_obj})
            


        
    else:
        return redirect('user_login')

    
    


def address(request):
    user=request.user
    if user.is_authenticated:

        bag_obj = Bag.objects.all().get(user=user)
        print(bag_obj)
    

        return render(request,'accounts/address.html',{'bag_obj':bag_obj})

    