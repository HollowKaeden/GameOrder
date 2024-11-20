from django.urls import path

from . import views


app_name = 'orders'


urlpatterns = [
    path('order', views.order, name='order'),
    path('my_orders', views.my_orders, name='my_orders'),
]
