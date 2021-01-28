from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, CreateView
from mobilestore.forms import SignUpForm, ShippingAddressForm, UserAccountUpdateForm
from mobilestore.models import ProductCategory, Product, User, Address, Order
from cart.cart import Cart


class BaseView(View):

    def get(self, request):
        products = Product.objects.filter(is_booked=False)
        return render(request, 'base.html', {'products': products})


class HomePageView(View):

    def get(self, request, slug=None):
        category = None
        count = Product.objects.filter(is_booked=False).count()
        categories = ProductCategory.objects.filter(parent=None)
        sub_categories = ProductCategory.objects.filter(parent__in=categories)
        products = Product.objects.filter(is_booked=False)
        template = 'index.html'
        if slug:
            category = get_object_or_404(ProductCategory, slug=slug)
            products = Product.objects.filter(category=category, is_booked=False)
            template = 'mobilestore/search_product.html'
        context = {
            'count': count,
            'category': category,
            'products': products,
            'categories': categories,
            'sub_categories': sub_categories
                    }
        return render(request, template, context)


class SearchResultView(View):

    def get(self, request):
        return render(request, 'mobilestore/search_results.html', {})


class ProductView(View):

    def get(self, request, slug=None):
        category = None
        count = Product.objects.filter(is_booked=False).count()
        categories = ProductCategory.objects.filter(parent=None)
        sub_categories = ProductCategory.objects.filter(parent__in=categories)
        products = Product.objects.filter(is_booked=False)
        template = 'mobilestore/products.html'
        if slug:
            category = get_object_or_404(ProductCategory, slug=slug)
            products = Product.objects.filter(category=category, is_booked=False)
            template = 'mobilestore/search_product.html'
        context = {
            'count': count,
            'category': category,
            'products': products,
            'categories': categories,
            'sub_categories': sub_categories
                    }
        return render(request, template, context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'mobilestore/product_detail.html'


class CheckoutInfoView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        form = ShippingAddressForm()
        return render(request, 'mobilestore/checkout_info.html', {'form': form})

    def post(self, request):
        form = ShippingAddressForm(request.POST, request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('checkout-payment')
        else:
            return render(request, 'mobilestore/checkout_info.html', {'form': form})


class CheckoutCompleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'mobilestore/checkout_complete.html', {})


class MyAccountView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        user = request.user
        return render(request, 'mobilestore/my_account.html', {'user': user})


class ContactUsView(View):

    def get(self, request):
        return render(request, 'mobilestore/contact_us.html', {})

    def post(self, request):
        user_email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        if user_email:
            send_mail(subject, message, user_email, (settings.EMAIL_HOST_USER,), fail_silently=False)
            return HttpResponse('mail sent successfully')
        return redirect('contact-us')


class AboutUsView(View):

    def get(self, request):
        return render(request, 'mobilestore/about_us.html', {})


class FaqView(View):

    def get(self, request):
        return render(request, 'mobilestore/faq.html', {})


class SignUpView(View):

    def get(self, request):
        form = SignUpForm
        return render(request, 'mobilestore/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'mobilestore/signup.html', {'form': form})


class UserAccountUpdateView(View):

    def get(self, request, pk):
        form = UserAccountUpdateForm()
        return render(request, 'mobilestore/account_update.html', {'form': form})

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        update_form = UserAccountUpdateForm(request.POST, instance=user)
        if update_form.is_valid():
            update_form.save()
            return redirect('account')
        else:
            return render(request, 'mobilestore/account_update.html', {'form': update_form})


class AddAccountInfoView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Address
    fields = ['address', 'zip_code']
    context_object_name = 'form'
    template_name = 'mobilestore/add-info.html'
    success_url = reverse_lazy('account')

    def form_valid(self, form):
        return super().form_valid(form)


def order_create(request):
    cart = Cart(request)
    if not cart:
        return render(request, 'mobilestore/checkout_complete.html', {})
    else:
        return redirect('cart:cart_detail')


class OrderRecord(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        orders = Order.objects.filter(customer=request.user)
        total_items = Order.objects.filter(customer=request.user).count()
        # total_items = 0
        total_price = 0
        for order in orders:
            # total_items = total_items + order.quantity
            total_price = total_price + order.product_price
        context = {
            'orders': orders,
            'total_price': total_price,
            'total_items': total_items
        }
        return render(request, 'mobilestore/order_record.html', context)