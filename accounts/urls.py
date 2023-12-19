# urls.py
from django.urls import path
from .views import register, user_login,user_logout,user_address,save_address,edit_address,edit_address_page,add_address,payment_success,activate_email

urlpatterns = [
    path('register/', register, name='register'),
    path('user_login/', user_login, name='user_login'),
    path('logout/',user_logout,name='logout'),
    path('address/',user_address,name='address'),
    path('add_address/',add_address,name='add_address'),
    path('save_address/',save_address,name='save_address'),
    path('edit_address_page/<str:uid>',edit_address_page,name='edit_address_page'),
    path('edit_address/<str:uid>',edit_address,name='edit_address'),
    path('payment_success/',payment_success,name='payment_success'),
    path('activate/<email_token>',activate_email,name='activate')

]
