from django.urls import path
from . import views

urlpatterns = [
    path('', views.market_index, name='market_index'),
    path('item/<int:item_id>/', views.item_sellers, name='item_sellers'),
    path('create/', views.product_create, name='product_create'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('search/', views.search_products, name='market_search'),
    path('order/create/<int:product_id>/', views.order_create, name='order_create'),
    path('orders/', views.order_list, name='order_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/cancel/', views.order_cancel, name='order_cancel'),
    path('payment/<int:order_id>/', views.payment_process, name='payment_process'),
    path('payment/success/<int:order_id>/', views.payment_success, name='payment_success'),
]
