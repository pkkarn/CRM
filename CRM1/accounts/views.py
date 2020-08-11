from django.shortcuts import render, redirect
from .models import *
from django.db.models import Count
from .forms import *
from .filters import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group


# Create your views here.
@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            form = CreateUserForm(request.POST)
            user = User.objects.create_user(username=request.POST['username'],
                                            email=request.POST['email'],
                                            password=request.POST['password1'])
            group = Group.objects.get(name="customer")
            user.groups.add(group)
            user.save()
            Customer.objects.create(
                user=user,
            )
            messages.success(request, 'Account Was Created ' + user.username + " Please Log In...")
            return redirect('login')

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginuser(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, "User Name Or Password Didn't match")
            return redirect('login')
        else:
            login(request, user)
            return redirect('home')
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, "Logged out successfully!")
        return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects
    total_orders = orders.all().count()
    pending_orders = orders.filter(status="Pending").count()
    delievered_orders = orders.filter(status="Delieverd").count()
    orders = Order.objects.all().order_by('-created')[0:5]
    context = {
        'pending_orders': pending_orders,
        'delievered_orders': delievered_orders,
        'total_orders': total_orders,
        'customers': customers,
        'orders': orders
    }
    return render(request, 'accounts\dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts\products.html', {'products': products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request, pk):
    customers = Customer.objects.get(id=pk)
    customerorders = customers.order_set.all()
    totalorders = customerorders.count()
    myfilter = OrderFilter(request.GET, queryset=customerorders)
    customerorders = myfilter.qs
    context = {
        'customers': customers,
        'customerorders': customerorders,
        'totalorders': totalorders,
        'myfilter': myfilter
    }
    return render(request, 'accounts\customers.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    customerOrder = Order.objects.get(id=pk)
    form = OrderForm(instance=customerOrder)
    context = {
        'form': form
    }
    if request.method == 'GET':
        return render(request, 'accounts/crud/order_form.html', context)
    else:
        form = OrderForm(request.POST, instance=customerOrder)
        if form.is_valid():
            form.save()
        return redirect('home')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    customer = Customer.objects.get(id=pk)
    form = OrderForm(initial={'customer': customer})  # initial of customers
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        return render(request, 'accounts/crud/order_form.html', {'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(reuqest, pk):
    order = Order.objects.get(id=pk)
    if reuqest.method == 'POST':
        order.delete()
        return redirect('home')
    return render(reuqest, 'accounts/crud/delete.html', {'order': order})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createCustomer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('home')
    return render(request, 'accounts/createCustomer.html', {'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
        return redirect('home')
    return render(request, 'accounts/createCustomer.html', {'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.all().count()
    pending_orders = orders.filter(status="Pending").count()
    delievered_orders = orders.filter(status="Delieverd").count()
    context = {
        'orders': orders,
        'pending_orders': pending_orders,
        'delievered_orders': delievered_orders,
        'total_orders': total_orders,
    }

    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userSetting(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
        return redirect('user-page')
    return render(request, 'accounts/settings.html', {'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userProfile(request):
    customer = request.user.customer
    context = {
        'customer': customer
    }
    return render(request, 'accounts/profile.html', context)
