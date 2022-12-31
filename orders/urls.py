from django.urls import path
from . import views

app_name="orders"


urlpatterns = [
    path('place-order', views.placeorder, name="placeorder"),
    path('my-order', views.my_orders, name="my_orders"),

    # razorpay
    path('proceed-to-pay', views.razorcheck, name="razorcheck"),
]
