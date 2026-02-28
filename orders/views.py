from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from products.models import Product
from .cart import Cart
from .models import Order, OrderItem
from customers.models import Customer
from django.core.paginator import Paginator


@login_required
def cart_partial(request):
    cart = Cart(request)
    return render(
        request,
        "tenant/orders/partials/cart_items.html",
        {
            "cart_items": cart.get_items(),
            "total": cart.get_total_price(),
        },
    )


@require_POST
@login_required
def htmx_cart_add(request, product_id):
    cart = Cart(request)
    quantity = int(request.POST.get("quantity", 1))
    cart.add(product_id, quantity)
    return cart_partial(request)


@require_POST
@login_required
def htmx_cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return cart_partial(request)


@require_POST
@login_required
def htmx_cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return cart_partial(request)


@login_required
def checkout(request):
    cart = Cart(request)

    if not cart.cart:
        return redirect("cart_detail")

    customer, _ = Customer.objects.get_or_create(user_id=request.user.id)
    order = Order.objects.create(
        customer=customer, status="pending", total_amount=cart.get_total_price()
    )

    for item in cart.get_items():
        OrderItem.objects.create(
            order=order,
            product_id=item["product_id"],
            product_name=item["name"],
            unit_price=item["price"],
            quantity=item["quantity"],
        )

    cart.clear()

    return redirect("orders:order_success", order_id=order.id)


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "tenant/orders/success.html", {"order": order})


@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "tenant/orders/order_details.html", {"order": order})


@login_required
def order_list(request):

    # Get customer for current user
    try:
        customer = Customer.objects.get(user_id=request.user.id)
        orders = (
            Order.objects.filter(customer=customer)
            .prefetch_related("items")
            .order_by("-created_at")
        )
    except Customer.DoesNotExist:
        orders = Order.objects.none()

    # Pagination
    paginator = Paginator(orders, 10)
    page = request.GET.get("page")
    orders_page = paginator.get_page(page)

    context = {
        "orders": orders_page,
    }
    return render(request, "tenant/orders/orders.html", context)
