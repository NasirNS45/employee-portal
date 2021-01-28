import stripe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View

from mobilestore.models import Product, PaymentInfo, Order
from myproject import settings
from .cart import Cart
from .forms import CartAddProductForm


class AddtoCartView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, product_id):
        cart = Cart(request)  # create a new cart object passing it the request object
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product)
        return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


class CartDetail(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
        return render(request, 'cart/detail.html', {'cart': cart, "key": settings.STRIPE_PUBLISHABLE_KEY})

    def post(self, request):
        cart = Cart(request)
        amount = int(cart.get_total_price())
        charge = stripe.Charge.create(amount=amount,
                                      currency='usd',
                                      description='Payment of ' + str(request.user.email),
                                      source='tok_visa')
        PaymentInfo.objects.create(user=request.user,
                                   stripe_payment_id=charge.stripe_id,
                                   stripe_payment_status=charge.status,
                                   stripe_paid_amount=amount)
        for item in cart:
            Order.objects.create(
                customer=request.user,
                product_name=item['product'],
                product_price=item['price'],
                quantity=item['quantity']
            )
        cart.clear()
        return redirect('order')