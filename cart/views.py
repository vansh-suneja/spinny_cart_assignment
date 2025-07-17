from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Cart, CartItem, Coupon, Address
from .serializers import ProductSerializer, CartItemSerializer, CartSerializer, CouponSerializer, AddressSerializer

@api_view(['POST'])
def add_to_cart(request):
    serializer = CartItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def update_cart_item(request, item_id):
    try:
        item = CartItem.objects.get(id=item_id)
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)

    serializer = CartItemSerializer(item, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def remove_cart_item(request, item_id):
    try:
        item = CartItem.objects.get(id=item_id)
        item.delete()
        return Response(status=204)
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)

@api_view(['POST'])
def apply_coupon(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
        coupon = Coupon.objects.get(code=request.data['code'])
        cart.coupon = coupon
        cart.save()
        return Response({"success": "Coupon applied!"})
    except (Cart.DoesNotExist, Coupon.DoesNotExist):
        return Response({"error": "Cart or coupon not found"}, status=404)

@api_view(['GET'])
def get_total_price(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
        total = sum(item.product.price * item.quantity for item in cart.items.all())
        if cart.coupon:
            total *= (1 - cart.coupon.discount / 100)
        return Response({"total_price": total})
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=404)

@api_view(['GET'])
def get_user_address(request, user_id):
    try:
        address = Address.objects.get(user_id=user_id)
        serializer = AddressSerializer(address)
        return Response(serializer.data)
    except Address.DoesNotExist:
        return Response({"error": "Address not found"}, status=404)
