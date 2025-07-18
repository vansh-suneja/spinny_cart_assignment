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

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cart, Coupon

@api_view(['POST'])
def apply_coupon(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=404)

    # Get coupon code from request body
    coupon_code = request.data.get('coupon_code')
    if not coupon_code:
        return Response({"error": "Coupon code is required"}, status=400)

    try:
        coupon = Coupon.objects.get(code=coupon_code)
    except Coupon.DoesNotExist:
        return Response({"error": "Invalid coupon code"}, status=400)

    cart.coupon = coupon
    cart.save()

    return Response({"message": "Coupon applied successfully", "coupon": coupon.code})

@api_view(['GET'])
def get_total_price(request):
    user_id = request.query_params.get('user_id')

    try:
        user = User.objects.get(id=user_id)
        cart = Cart.objects.get(user=user)
        cart_items = cart.cartitem_set.all()
        total = sum(item.product.price * item.quantity for item in cart_items)

        discount = 0
        if cart.coupon:
            discount = (cart.coupon.discount / 100) * total
            total -= discount

        return Response({
            'total_price': round(total, 2),
            'discount_applied': round(discount, 2),
            'coupon': cart.coupon.code if cart.coupon else None
        })

    except User.DoesNotExist:
        return Response({'error': 'User not found'})
    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'})


@api_view(['GET'])
def get_user_address(request, user_id):
    try:
        address = Address.objects.get(user_id=user_id)
        serializer = AddressSerializer(address)
        return Response(serializer.data)
    except Address.DoesNotExist:
        return Response({"error": "Address not found"}, status=404)
