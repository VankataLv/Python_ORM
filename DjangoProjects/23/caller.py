import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Order, Product
from django.db.models import Q, Count, F
from decimal import Decimal

# Create queries within functions


def get_profiles(search_string=None) -> str:
    if search_string is None:
        return ""

    query = Q(full_name__icontains=search_string) |\
    Q(email__icontains=search_string) |\
    Q(phone_number__icontains=search_string)

    profiles = Profile.objects.filter(query).order_by('full_name')

    if not profiles.exists():
        return ""

    result = []
    for profile in profiles:
        result.append(f"Profile: {profile.full_name}, email: {profile.email}, phone number: {profile.phone_number}, "
                      f"orders: {profile.orders.count()}")

    return '\n'.join(result)


def get_loyal_profiles() -> str:
    profiles = Profile.objects.get_regular_customers()

    if not profiles.exists():
        return ""

    result = []
    for profile in profiles:
        result.append(f"Profile: {profile.full_name}, orders: {profile.orders.count()}")

    return '\n'.join(result)


def get_last_sold_products() -> str:
    last_order = Order.objects.prefetch_related('products').last()

    if last_order is None or not last_order.products.exists():
        return ""

    products = [p.name for p in last_order.products.order_by('name')]
    return f"Last sold products: {', '.join(products)}"


#  --------------------------------------------------------------------------------------------------------------------
def get_top_products()-> str:
    products = Product.objects\
        .annotate(orders_count=Count('orders_products'))\
        .filter(orders_count__gt=0)\
        .order_by('-orders_count', 'name')[0:5]

    if not products.exists():
        return ""

    result = ["Top products:"]
    for product in products:
        result.append(f"{product.name}, sold {product.orders_count} times")

    return '\n'.join(result)


def apply_discounts() -> str:
    orders = Order.objects\
        .annotate(products_count=Count('products'))\
        .filter(products_count__gt=2, is_completed=False)\
        .update(total_price=F('total_price') * 0.90)

    return f"Discount applied to {orders} orders."


def complete_order() -> str:
    first_order = Order.objects.filter(is_completed=False).first()

    if not first_order:
        return ""

    first_order.is_completed=True
    for product in first_order.products.all():
        product.in_stock -= 1

        if product.in_stock == 0:
            product.is_available = False

    return "Order has been completed!"

