import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from accounts.models import Account
from cart.models import CartItem
from store.models import Product

from .models import Order, OrderItems, ProfileAddress


@login_required(login_url='accounts:login_page')
def placeorder(request, total=0, quantity=0):
    if request.method == 'POST':
        currentuser = Account.objects.filter(id=request.user.id).first()
        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('first_name')
            currentuser.last_name = request.POST.get('last_name')
            currentuser.save()

        if not ProfileAddress.objects.filter(user=request.user):
            addressProfile = ProfileAddress()
            addressProfile.user = request.user
            addressProfile.address_line_1 = request.POST.get('address_line_1')
            addressProfile.address_line_2 = request.POST.get('address_line_2')
            addressProfile.phone = request.POST.get('phone_number')
            addressProfile.city = request.POST.get('city')
            addressProfile.state = request.POST.get('state')
            addressProfile.country = request.POST.get('country')
            addressProfile.pincode = request.POST.get('pincode')

            addressProfile.save()

        neworder = Order()
        neworder.user = request.user
        neworder.first_name = request.POST.get('first_name')
        neworder.last_name = request.POST.get('last_name')
        neworder.phone = request.POST.get('phone_number')
        neworder.email = request.POST.get('email')
        neworder.address_line_1 = request.POST.get('address_line_1')
        neworder.address_line_2 = request.POST.get('address_line_2')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')

        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')
        cart_items = CartItem.objects.filter(user=request.user)

        for cart_item in cart_items:
            total += ((cart_item.product.price-(cart_item.product.category.offer *
                                                cart_item.product.price)/100)*cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
        neworder.total_price = grand_total
        trno = 'khadi'+str(random.randint(11111111, 99999999))

        while Order.objects.filter(tracking_no=trno) is None:
            trno = 'khadi'+str(random.randint(11111111, 99999999))
        neworder.tracking_no = trno
        neworder.save()

        neworderitems = CartItem.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItems.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
            pr = item.product
            product = Product.objects.get(id=pr.id)
            product.stock -= item.quantity
            product.save()
        CartItem.objects.filter(user=request.user).delete()
        messages.success(request, 'Your order have been placed successfully')
        paymod = request.POST.get('payment_mode')
        if paymod == 'paid by razorpay' or paymod == 'paid by PayPal':
            print('hello razorpay gfjsdfjgjsdfjgdfgposjdfpg99999')
            #JsonResponse({'status':'Your order have been placed successfully'})
            JsonResponse({'status': 'false', 'message': 'ddddd'}, status=200)
            # HttpResponse("Request method is not a GET")
        return redirect('store:storehome')
    else:
        return redirect('cart:checkout')


@login_required(login_url='accounts:login_page')
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'accounts/my_orders.html', context)


@login_required(login_url='accounts:login_page')
def razorcheck(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = 0
    for cart_item in cart_items:
        total_price += ((cart_item.product.price-(cart_item.product.category.offer *
                                                  cart_item.product.price)/100)*cart_item.quantity)
    tax = (2 * total_price)/100
    grand_total = total_price + tax
    print(total_price)
    return JsonResponse({
        'total_price': round(grand_total)
    })
