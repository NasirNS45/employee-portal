from django.urls import path
from . import views
urlpatterns = [
    path('', views.HomePageView.as_view(), name='homepage'),
    path('search/results/', views.SearchResultView.as_view(), name='search-result'),
    path('products/', views.ProductView.as_view(), name='products'),
    path('products/<slug:slug>/', views.ProductView.as_view(), name='products-by-category'),
    path('product/detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    # path('checkout/cart/', views.CheckoutCartView.as_view(), name='checkout-cart'),
    path('checkout/info/', views.CheckoutInfoView.as_view(), name='checkout-info'),
    # path('checkout/payment/', views.CheckoutPaymentView.as_view(), name='checkout-payment'),
    path('checkout/complete/', views.CheckoutCompleteView.as_view(), name='checkout-complete'),
    path('account/', views.MyAccountView.as_view(), name='account'),
    path('account/add/info/', views.AddAccountInfoView.as_view(), name='add-info'),
    path('contact-us/', views.ContactUsView.as_view(), name='contact-us'),
    path('about-us/', views.AboutUsView.as_view(), name='about-us'),
    path('faq/', views.FaqView.as_view(), name='faq'),
    path('signup/', views.SignUpView.as_view(), name='register'),
    path('order/done/', views.order_create, name='order'),
    path('order/record/', views.OrderRecord.as_view(), name='order-record'),
    # path('add/<int:pk>/cart', views.AddToCartView.as_view(), name='add-to-cart'),
    # path('cart/items/', views.ItemListCartView.as_view(), name='cart-items'),
    # path('cart/item/<int:pk>/remove/', views.RemoveCartItemView.as_view(), name='remove-from-cart')
    path('account/<int:pk>/update/', views.UserAccountUpdateView.as_view(), name='update-account')
]

