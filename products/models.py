from django.db import models
from base.models import BaseModel
from django.utils.text import slugify 
from django.contrib.auth.models import User
from django.urls import reverse

from uuid import uuid4

class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slogen = models.TextField(null=True,blank=True)
    background_image = models.ImageField(upload_to='images/categories',null=True,blank=True)
    second_image = models.ImageField(upload_to='images/second_background',null=True,blank=True)
    
    slug = models.SlugField(unique=True,null=True,blank=True)
    
    link_path = models.CharField(max_length=100,null=True,blank=True)
    def save(self, *args, **kwargs):
        self.slug= slugify(self.category_name)
        super(Category,self).save(*args,**kwargs)
    def __str__(self) -> str:
        return self.category_name
    


class ColorVariant(BaseModel):
    color_code = models.CharField(max_length=6, default='ffffff', blank=True, null=True)
    color_name = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid4, unique=True)  # Add a UUID field

    def __str__(self):
        return self.color_name

class SizeVariant(BaseModel):
    size_name = models.CharField(max_length=10)
    price = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid4, unique=True)  # Add a UUID field

    def __str__(self):
        return self.size_name

    


class Product(BaseModel):
    
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    original_price = models.IntegerField()
    discounted_price = models.IntegerField()
    product_description = models.TextField()
    color_variant = models.ManyToManyField(ColorVariant,blank=True)
    size_variant = models.ManyToManyField(SizeVariant,blank=True)
    def get_absolute_url(self):
        # Define the URL for viewing the product detail
        return reverse('home', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.slug= slugify(self.product_name)
        super(Product,self).save(*args,**kwargs)
    def __str__(self) -> str:
        return self.product_name


class ProductImage(BaseModel):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_images")
    image = models.ImageField(upload_to='images/products')



class WishlistItem(BaseModel):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size =  models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    added_at = models.DateTimeField(auto_now_add=True)

class Bag(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    is_paid = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)
    razor_pay_order_id = models.CharField(max_length=100,null=True,blank=True)
    razor_pay_payment_id = models.CharField(max_length=100,null=True,blank=True)
    razor_pay_payment_signature= models.CharField(max_length=100,null=True,blank=True)
    shipping_cost = models.IntegerField(default=0)
    
    def get_bag_total(self):
        bag_items = self.bag_items.all()
        price = []
        for bag_item in bag_items:
            price.append(bag_item.total_price)
            total = sum(price)     
        return total







    



class BagItems(BaseModel):
    bag = models.ForeignKey(Bag,on_delete=models.CASCADE,related_name='bag_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        # Calculate the discounted price based on the associated product
        return self.product.discounted_price * self.quantity
    def __str__(self):
        return f"{self.bag.user.username}'s Bag - {self.product.product_name}"


