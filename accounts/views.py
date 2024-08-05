from django.shortcuts import render,HttpResponse
from django.contrib import messages
from base.emails import send_account_activation_email,send_invoice
# Create your views here.
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout

from .models import UserProfile,UserAdd
from .models import UserAdd
from django.contrib.auth.models import User
from products.models import BagItems,Bag
import razorpay
from django.conf import settings
import uuid
import datetime
from base.helpers import save_pdf
def register(request):
    if request.method == 'POST':
    
        email = request.POST.get('email')
        raw_password = request.POST.get('password')
        gender = request.POST.get('gender')
        mobile = request.POST.get('mobile')
        username = email.split('@')[0]
        email_token = str(uuid.uuid4())
        user = User.objects.create_user(username=username,email=email)
        user.set_password(raw_password=raw_password)
        user.save()
        user_profile_item = UserProfile.objects.get_or_create(user=user,mobile=mobile,gender=gender,email_token=email_token)
        
        
        if user_profile_item:
            send_account_activation_email(email,email_token)


  
        return redirect('user_login')  # Redirect to your home page
    else:
        
        return render(request, 'accounts/register.html')


def activate_email(request,email_token):
    try:
        user = UserProfile.objects.get(email_token = email_token)
        user.is_email_verified =True

        user.save()

    except Exception as e:
        return HttpResponse('invalid email token ')
    return redirect('/')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            print(user)
            user = authenticate(request,username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')

        except Exception as e:
            print(e)
          
            # Redirect to your home page
       
    return render(request, 'accounts/login.html')
    
def user_logout(request):
    logout(request)
    return redirect('/')# Redirect to your home page
def add_address(request):
    return render(request,'accounts/add_address.html')

def user_address(request,uid=None):
    addresses = UserAdd.objects.all().filter(user = request.user)
    if addresses:
        bag_obj = Bag.objects.get(user=request.user,is_paid=False)
        client = razorpay.Client(auth = (settings.RAZOR_PAY_KEY,settings.RAZOR_PAY_SECRET))
        payment = client.order.create({'amount':bag_obj.get_bag_total() * 100,'currency':'INR','payment_capture':1})
        bag_obj.razor_pay_order_id = payment['id']
        bag_obj.save()
        print('******')
        print(payment)
        print('*****')

        return render(request, 'accounts/address.html',{'addresses':addresses,'bag_obj':bag_obj ,'payment':payment})
    else:
        if uid:
            edit_address_obj = UserAdd.objects.get(uid=uid)
            return render(request,'accounts/add_address.html',{'edit_address':edit_address_obj})
    return render(request,'accounts/add_address.html')
    #add save address functionality


def save_address(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        user_address_item = UserAdd.objects.create(

            user = request.user,
            full_name = full_name,
            addressline1 = address1,
            addressline2 = address2,
            pincode = pincode,
            city = city,
            state = state
            )
        user_address_item.save()
        return redirect('address')
def edit_address_page(request,uid):
    item = UserAdd.objects.get(uid=uid)
    return render(request,'accounts/edit_address.html',{'item':item})
    
def edit_address(request,uid):

    
    item = UserAdd.objects.get(uid=uid)
    item.full_name = request.POST.get('full_name')
    item.addressline1 = request.POST.get('address1')
    item.addressline2 = request.POST.get('address2')
    item.city = request.POST.get('city')
    item.pincode = request.POST.get('pincode')
    item.state = request.POST.get('state')
    item.save()
    return redirect('address')


def payment_success(request):
    order_id = request.GET.get('razorpay_order_id')
    bag = Bag.objects.get(razor_pay_order_id = order_id)
    bag.is_paid = True
    bag.razor_pay_payment_id = request.GET.get('razorpay_payment_id')
    bag.razor_pay_payment_signature = request.GET.get('razorpay_signature')
    bag.save()
    ordered_items = BagItems.objects.filter(bag=bag)
    addresses = UserAdd.objects.all().filter(user = request.user)

    


    context = {
        'order_id':request.GET.get('razorpay_order_id'),
        'payment_id':request.GET.get('razorpay_payment_id'),
        'ordered_items':ordered_items,
        'bag_total':bag.get_bag_total,
        'time':datetime.datetime.now(),
        'address':addresses[0]
        
      
    }
    invoice = save_pdf(context)
    send_invoice(request.user.email,invoice)
    return render(request,'payments/payment_successfull.html',context)
    

    
