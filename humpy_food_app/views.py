from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from .models import SetProfile, Menu, Contact, Cart, Order, Feedback
from .form import CartForm, MenuForm, OrderForm
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})
        else:
            try:
                password = request.POST.get('password')
                password_c = request.POST.get('re_password')
                if password == password_c:
                    user = User.objects.create_user(
                        username=name, email=email, password=password)
                    user.save()
                    login(request, user)
                    return render(request, 'setprofile.html', {'name': name, 'email': email})
                else:
                    return render(request, 'register.html', {'error': 'Incorrect Password'})
            except IntegrityError:
                return render(request, 'register.html', {'error': 'Username already exists'})
    return render(request, 'register.html')


def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Invalid Username or Password'})
    return render(request, 'login.html')


def logoutuser(request):
    logout(request)
    return redirect('index')

def thank(request):
    item = Cart.objects.filter(user__id=request.user.id, status=False)
    price = 0
    total = 0
    for i in item:
        price = i.product.price*i.quantity
        total += price
    context = {
        'items': item,
        'total': total
    }
    return render(request, 'thank.html', context)


def index(request):
    menus = Menu.objects.filter(cate="Pizza")
    item = Cart.objects.filter(user__id=request.user.id, status=False)
    price = 0
    total = 0
    for i in item:
        price = i.product.price*i.quantity
        total += price
    context = {
        'items': item,
        'total': total,
        'menus':menus
    }
    return render(request, 'index.html', context)

def setprofile(request):
    if request.method == 'POST':
        username = request.user.username
        user = User.objects.get(username=username)
        if user is not None:
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            image = request.FILES.get('image')
            profile = SetProfile(user=user, email=email, fname=fname,
                                 lname=lname, address=address, phone=phone, image=image)
            profile.save()
            return redirect('index')
        else:
            return render(request, 'setprofile.html')
    setprofile = SetProfile.objects.filter(user=request.user)
    return render(request, 'setprofile.html', {'setprofile': setprofile})

@login_required(login_url='login')
def profile(request):
    item = Cart.objects.filter(user__id=request.user.id, status=False)
    price = 0
    total = 0
    for i in item:
        price = i.product.price*i.quantity
        total += price
    context = {
        'items': item,
        'total': total
    }

    check = SetProfile.objects.filter(user__id=request.user.id)
    if len(check) > 0:
        data = SetProfile.objects.get(user__id=request.user.id)
        context["data"] = data
    if request.method == "POST":
        # print(request.POST)
        fn = request.POST["fname"]
        ln = request.POST["lname"]
        ur = request.POST["username"]
        em = request.POST["email"]
        con = request.POST["phone"]
        add = request.POST["address"]
        # set updated data
        usr = User.objects.get(id=request.user.id)
        usr.username = ur
        usr.save()
        data.email = em
        data.fname = fn
        data.lname = ln
        data.address = add
        data.phone = con
        data.save()
        if "image" in request.FILES:
            img = request.FILES["image"]
            data.image = img
            data.save()
    return render(request, 'profile.html', context)


@staff_member_required(login_url='login')
def addmenu(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        desc = request.POST.get('desc')
        cate = request.POST.get('cate')
        types = request.POST.get('types')
        image = request.FILES.get('image')
        menu = Menu(name=name, desc=desc, cate=cate,
                    price=price, types=types, image=image)
        menu.save()
    return render(request, 'addmenu.html')


@staff_member_required(login_url='login')
def editmenu(request):
    menu = Menu.objects.all()
    id = request.GET.get('id')
    if request.method == "POST":
        menus = Menu.objects.get(id=id)
        edit = MenuForm(request.POST, request.FILES, instance=menus)
        if edit.is_valid():
            edit.save()
    return render(request, "editmenu.html", {'menus': menu})


@staff_member_required(login_url='login')
def deletemenu(request):
    id = request.GET.get('id')
    Menu.objects.filter(id=id).delete()
    return redirect('editmenu')


def contact(request):
    item = Cart.objects.filter(user__id=request.user.id, status=False)
    price = 0
    total = 0
    for i in item:
        price = i.product.price*i.quantity
        total += price
    context = {
        'items': item,
        'total': total
    }
    if request.method == 'POST':
        f_name = request.POST.get('name')
        email = request.POST.get('email')
        msg = request.POST.get('message')
        contact = Contact(name=f_name, email=email, message=msg)
        contact.save()
        return render(request, 'thank.html')
    return render(request, 'contact.html', context)


def about(request):
    item = Cart.objects.filter(user__id=request.user.id, status=False)
    price = 0
    total = 0
    for i in item:
        price = i.product.price*i.quantity
        total += price
    context = {
        'items': item,
        'total': total
    }
    return render(request, 'about.html', context)


def faq(request):
    item = Cart.objects.filter(user__id=request.user.id, status=False)
    price = 0
    total = 0
    for i in item:
        price = i.product.price*i.quantity
        total += price
    context = {
        'items': item,
        'total': total
    }
    return render(request, 'faq.html', context)


def tc(request):
    item = Cart.objects.filter(user__id=request.user.id, status=False)
    price = 0
    total = 0
    for i in item:
        price = i.product.price*i.quantity
        total += price
    context = {
        'items': item,
        'total': total
    }
    return render(request, 'terms_conditions.html', context)


def menu(request):
    item = Cart.objects.filter(user__id=request.user.id, status=False)
    price = 0
    total = 0
    for i in item:
        price = i.product.price*i.quantity
        total += price
    context = {
        'items': item,
        'total': total
    }

    category = request.GET.get('category')
    types = request.GET.get('types')
    if category:
        menus = Menu.get_menu_by_cate(category)
    elif types:
        menus = Menu.get_menu_by_type(types)
    elif request.method == 'POST':
        name = request.POST.get('search')
        menus = Menu.objects.filter(name__icontains=name)
    else:
        menus = Menu.objects.all()
    context['menus']=menus
    return render(request, 'menu.html', context)


@login_required(login_url='login')
def cart(request):
    # directory
    context = {}
    items = Cart.objects.filter(user__id=request.user.id, status=False)
    price = 0
    total = 0
    for i in items:
        price = i.product.price*i.quantity
        total += price 
    context = {
        'items': items,
        'total': total
    }
    if request.user.is_authenticated:
        if request.method == "POST":
            p_id = request.POST.get("p_id")
            qty = request.POST.get("qty")
            is_exist = Cart.objects.filter(
                product_id=p_id, user_id=request.user.id, status=False)
            if len(is_exist) > 0:
                context["msg"] = "Item Allready Exist in Cart"
                context["cls"] = "alert alert-warning"
            else:
                product = get_object_or_404(Menu, id=p_id)
                usr = get_object_or_404(User, id=request.user.id)
                c = Cart(user=usr, product=product, quantity=qty)
            c.save()
            return redirect('menu')
    else:
        context["error"] = "Login to View Your Cart"
    return render(request, 'cart.html', context)


@login_required(login_url='login')
def editcart(request, id):
    if request.method == "POST":
        cart = Cart.objects.get(id=id, status=False)
        edit = CartForm(request.POST, instance=cart)
        if edit.is_valid():
            Edit = edit.save(commit=False)
            Edit.user = request.user
            Edit.save()
        return redirect('cart')


@login_required(login_url='login')
def deletecart(request):
    id = request.GET.get("id")
    Cart.objects.filter(id=id, status=False).delete()
    return redirect('cart')


@login_required(login_url='login')
def payment(request):
    item=Cart.objects.filter(user__id=request.user.id,status=False)
    price=0
    total=0
    menu=[]
    inv=""
    for i in item:
        price=i.product.price*i.quantity
        total+=float(price)
        menu=str(i.product.name)
        inv+=str(i.id)
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(total),
        'item_name': menu,
        'invoice': inv,
        'currency_code': 'INR',
        'notify_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format('127.0.0.1:8000',
                                          reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format('127.0.0.1:8000',
                                              reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment.html', {'form': form, 'total':total, 'items':item})
    #return render(request, 'payment.html',{'total':total})

@csrf_exempt
def payment_done(request):
    item=Cart.objects.filter(user__id=request.user.id,status=False)
    user=request.user
    price=0
    total=0
    menu=""
    for i in item:
        price=i.product.price*i.quantity
        total+=float(price)
        menu+=i.product.name+", "
    order=Order(user=user,menu=menu,total_price=total)
    order.save()
    for j in item:
        j.status = True
        j.save()
    return render(request, 'thank.html')


@csrf_exempt
def payment_cancelled(request):
    item=Cart.objects.filter(user__id=request.user.id,status=False)
    price=0
    total=0
    for i in item:
        price=i.product.price*i.quantity
        total += price
    context={
        'items': item,
        'total': total,
        'msg': "Payment Cancelled",
        'cls': "alert alert-warning"
    }
    return render(request, 'cart.html', context)

@login_required(login_url='login')
def tracking(request):
    # your cart
    items = Cart.objects.filter(user__id=request.user.id, status=True)
    track = Order.objects.filter(user__id=request.user.id)
    price = 0
    total = 0
    for i in items:
        price = i.product.price*i.quantity
        total += price
    context = {
        'items': items,
        'total': total,
        'track': track
    #     html   view
    }
    return render(request, 'tracking.html', context)

@staff_member_required(login_url='login')
def edittrack(request):
    orders=Order.objects.order_by('-added_on')
    if request.method=="POST":
        id=request.GET.get("id")
        order=Order.objects.get(id=id, status=False)
        edit=OrderForm(request.POST, instance=order)
        if edit.is_valid():
            if order.track=='Your Order has been Delivered':
                Edit=edit.save(commit=False)
                Edit.status=True
                Edit.save()
                Cart.objects.filter(status=True).delete()
                return render(request, "edittrack.html",{"orders":orders})
            edit.save()
    return render(request, "edittrack.html",{"orders":orders})

@login_required(login_url='login')
def feedback(request):
    context={}
    menus = Menu.objects.all()
    context['menus']=menus
    if request.method == 'POST':
        review = request.POST.get('reviews')
        name=request.POST.get('name')
        rate=request.POST.get('rate')
        order=Menu.objects.get(name=name)
        fd = Feedback(review=review, user=request.user, order=order, rate=rate)
        fd.save()
        return render(request, 'thank.html')
    return render(request, 'feedback.html', context)