# Register your models here.

from django.contrib import admin
from .models import Product, Cart, CartItem, Coupon, Address

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Coupon)
admin.site.register(Address)

