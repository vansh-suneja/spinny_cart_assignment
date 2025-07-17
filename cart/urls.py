from django.urls import path
from . import views

urlpatterns = [
    path('add-to-cart/', views.add_to_cart),
    path('update-cart/<int:item_id>/', views.update_cart_item),
    path('remove-cart/<int:item_id>/', views.remove_cart_item),
    path('apply-coupon/<int:cart_id>/', views.apply_coupon),
    path('total-price/<int:cart_id>/', views.get_total_price),
    path('address/<int:user_id>/', views.get_user_address),
]
