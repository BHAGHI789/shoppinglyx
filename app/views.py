from itertools import product
from unicodedata import category
from django.shortcuts import render,redirect
from app.models import Cart,Customer,Product,OrderPlaced
from django.views import View
from app.forms import CustomerRegistationForm,CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class Productview(View):
    def get(self,request):
        topwear=Product.objects.filter(category='TW')
        bottomwear=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        laptop=Product.objects.filter(category='L')
        return render(request, 'app/home.html',{'topwear':topwear,'bottomwear':bottomwear,'mobiles':mobiles,'laptop':laptop})









class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:

            item_already_in_cart=Cart.objects.filter(Q(product=product) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})
def mobile(request,data=None):
    if data==None:
        mobiles=Product.objects.filter(category='M')
    elif data=='iphone' or data=='realme':
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data=='below':
        mobiles=Product.objects.filter(category='M').filter(discounted_price__lt=1000)
    elif data=='above':
        mobiles=Product.objects.filter(category='M').filter(discounted_price__gt=1000)
    return render(request, 'app/mobile.html',{'mobiles':mobiles})

class CustomerRegistationView(View):
    def get(self,request):
        form=CustomerRegistationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self,request):
        form=CustomerRegistationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congralations   ! successfully')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congralations !! Profile Update Successfully')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
@login_required
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
     if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        print(cart)
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p  for p in Cart.objects.all() if p.user ==user]
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity*p.product.discounted_price)
                amount +=tempamount
                totalamount=amount+shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})
        else:
            return render(request,'app/emptycart.html')

def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p  for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount +=tempamount
        data={
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':amount+shipping_amount
            }
        return JsonResponse(data)

def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p  for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount +=tempamount
        data={
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':amount+shipping_amount
            }
        return JsonResponse(data)

def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p  for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount +=tempamount
            totalamount=amount
        data={
                'amount':amount,
                'totalamount':amount+shipping_amount
            }
        return JsonResponse(data)
@login_required
def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    total_amount=0.0
    cart_product=[p  for p in Cart.objects.all() if p.user ==request.user]
    if cart_product:
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount +=tempamount
        total_amount=amount+shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'totalamount':total_amount,'cart_items':cart_items})
@login_required
def paymentdone(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")
@login_required
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})



def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')






 #def home(request):((!1))
 #return render(request, 'app/home.html')
 #def product_detail(request):
 #return render(request, 'app/productdetail.html')
 #def mobile(request):
 #return render(request, 'app/mobile.html')
 #def customerregistration(request):
 #return render(request, 'app/customerregistration.html')
 #def login(request):
 #return render(request, 'app/login.html')
 #def change_password(request):(delete)
 #return render(request, 'app/changepassword.html')
