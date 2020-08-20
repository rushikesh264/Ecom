from django.shortcuts import render,redirect 
from . models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart,cartData

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm

from django.contrib.auth import authenticate,login,logout

def index(request):
    context = {}
    return render(request,'store/index.html',context)

def store(request):
    data = cartData(request)
    
    loginflag = data['loginflag']
    cartItems = data['cartItems']  
    products = Product.objects.all()    
    context={'products':products,'cartItems':cartItems,'loginflag':loginflag}
    return render(request,'store/store1.html',context)
def cart(request):
    data = cartData(request)
    loginflag = data['loginflag']
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']   
        
    #sending context dictionary to cart.html
    context={'items':items,'order':order,'cartItems':cartItems,'loginflag':loginflag}
    return render(request,'store/cart.html',context)
def checkout(request):
    data = cartData(request)
    loginflag = data['loginflag']
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context={'items':items,'order':order,'cartItems':cartItems,'loginflag':loginflag}
    return render(request,'store/checkout.html',context)
def aboutus(request):
    data = cartData(request)
    cartItems = data['cartItems']
    context={'cartItems':cartItems}
    return render(request,'store/about.html',context)

def viewdetails(request,id):
    data = cartData(request)
    cartItems = data['cartItems']
    product = Product.objects.get(id=id)
    context={'product':product,'cartItems':cartItems}
    # context={}
    return render(request,'store/prodview.html',context)

def userregister(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Account created successfull for ' + user +'..')
            return redirect('userlogin')
        else:
            print("error")
    context = {'form':form,'cartItems':0}
    return render(request,'store/register.html',context)
    
def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.info(request,'Invalid Credentials!!!')
    context={'cartItems':0}
    return render(request,'store/login.html',context)

def logoutuser(request):
    logout(request)
    return redirect('userlogin')

def userorder(request):
    return render(request,'store/orders.html')
#receive data from additem() from cart.js
def updateitem(request):
    #loading data from javascript
     
    data= json.loads(request.body)
    productID=data['productID']
    action=data['Action']

    #getting customer
    customer=request.user.customer

    #retriving selected product
    product=Product.objects.get(id=productID)

    #creating order of recent customer
    order,created=Order.objects.get_or_create(customer=customer,complete=False)

    #creating orderitem with above order and product
    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)

    #updating quantity 
    if(action=='add'):
        orderItem.quantity+=1
    elif action=='remove':
        orderItem.quantity-=1
    orderItem.save()

    if orderItem.quantity<=0:
        orderItem.delete()
    return JsonResponse('added',safe=False)

def processorder(request):
    data= json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()        
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        order.transaction_id = transaction_id
       

        #below part also exist in else also....
        total = float(data['userformdata']['total'])
        
        if total == float(order.get_cart_total) :
            #float(order.get_cart_total)
            #print("aaaaaaaaaaahe ali total",total,"result ala ha",(order.get_cart_total))
            order.complete = True
        order.save()
        #print("caaaaaaaaaaaaaart",order.get_cart_items)

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['usershippingdata']['address'],
                city = data['usershippingdata']['city'],
                state = data['usershippingdata']['state'],
                zipcode = data['usershippingdata']['zipcode']
            )
    else:
        print("User not logged in")
        name = data['userformdata']['name']
        email = data['userformdata']['email']

        cookieData = cookieCart(request)
        items = cookieData['items']

        customer,created = Customer.objects.get_or_create(email=email)
        customer.name = name
        customer.email = email
        
        customer.save()

        order = Order.objects.create(customer = customer,complete = False)
        order.transaction_id = transaction_id

        for item in items:
            product = Product.objects.get(id=item['product']['id'])
            orderItem = OrderItem.objects.create(product = product,order = order,quantity = item['quantity'])
        
        #same part from above if block
        total = float(data['userformdata']['total'])
        
        if total == float(order.get_cart_total) :
            #float(order.get_cart_total)
            #print("aaaaaaaaaaahe ali total",total,"result ala ha",(order.get_cart_total))
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['usershippingdata']['address'],
                city = data['usershippingdata']['city'],
                state = data['usershippingdata']['state'],
                zipcode = data['usershippingdata']['zipcode']
            )


        
    return JsonResponse('payment complete',safe=False)

