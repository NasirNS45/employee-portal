from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartDetail.as_view(), name='cart_detail'),
    path('add/<int:product_id>/', views.AddtoCartView.as_view(), name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]

