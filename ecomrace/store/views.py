from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *
import datetime

# Create your views here.
def store(request):
    products = Product.objects.all()
    
    if request.user.is_authenticated:
        customer = request.user.customer
        oreder, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = oreder.orderitem_set.all()
        cartItem = oreder.get_cart_items
    else:
        items = []
        oreder = {'get_cart_items':0, 'get_cart_total':0}
        cartItem = order['get_cart_items']

    context = {'items': items, 'order': oreder, 'cartItem':cartItem, 'products': products}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        oreder, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = oreder.orderitem_set.all()
        cartItem = oreder.get_cart_items
    else:
        items = []
        oreder = {'get_cart_items':0, 'get_cart_total':0}
        cartItem = order['get_cart_items']

    context = {'items': items, 'order': oreder, 'cartItem':cartItem}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        oreder, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = oreder.orderitem_set.all()
        cartItem = oreder.get_cart_items
    else:
        items = []
        oreder = {'get_cart_items':0, 'get_cart_total':0}
        cartItem = order['get_cart_items']

    context = {'items': items, 'order': oreder, 'cartItem':cartItem}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    productId = request.GET.get('productId')
    action = request.GET.get('action')
    print(action)
    print(productId)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('item was updated', safe=False)


def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)