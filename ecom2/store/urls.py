from django.urls import path
from . import views
urlpatterns=[
   
    path('',views.store,name="index"),
    path('store/',views.store,name="store"),
    path('checkout/',views.checkout,name="checkout"),
    path('cart/',views.cart,name="cart"),
    path('update_item/',views.updateitem,name="update_item"),
    path('process_order/',views.processorder,name="process_order"),
    path('view_details/<int:id>/',views.viewdetails,name='view_details'),
    path('aboutus/',views.aboutus,name='aboutus'),
    path('userlogin/',views.userlogin,name='userlogin'),
    path('userregister/',views.userregister,name='userregister'),
    path('logoutuser/',views.logoutuser,name='logoutuser'),
    path('userorder/',views.userorder,name='userorder')
]