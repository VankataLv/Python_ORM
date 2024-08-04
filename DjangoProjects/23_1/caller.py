import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Product, Order
from django.db.models import Q, Count, F


# Create queries within functions


def get_profiles(search_string=None):
    if search_string is None:
        return ""

    query = Q(full_name__icontains=search_string) |\
    Q(email__icontains=search_string) |\
    Q(phone_number__icontains=search_string)

    profiles = (Profile.objects.prefetch_related('profile_orders')
                .annotate(order_count=Count('profile_orders'))
                .filter(query)
                .order_by('full_name'))

    if not profiles:
        return ""

    result = []
    for pro in profiles:
        result.append(f"Profile: {pro.full_name}, email: {pro.email}, phone number: {pro.phone_number}, "
                      f"orders: {pro.order_count}")

    return '\n'.join(result)

# print(get_profiles(search_string='a'))


def get_loyal_profiles():
    profiles = Profile.objects.get_regular_customers()

    if not profiles:
        return ""

    result = []
    for pro in profiles:
        result.append(f"Profile: {pro.full_name}, orders: {pro.order_count}")

    return '\n'.join(result)


def get_last_sold_products():
    last_order = Order.objects.prefetch_related('products').order_by('creation_date').last()

    if not last_order:
        return ""

    return f"Last sold products: {', '.join([product.name for product in last_order.products.all()])}"


# __________________________________________________________
def get_top_products():
    top_products = (Product.objects
                    .annotate(order_count=Count('orders_products'))
                    .filter(order_count__gt=0)
                    .order_by('-order_count', 'name'))[0:5]

    if not top_products.exists():
        return ""

    result = ["Top products:"]
    for product in top_products:
        result.append(f'{product.name}, sold {product.order_count} times')

    return '\n'.join(result)


def apply_discounts():
    big_orders = (Order.objects
                  .annotate(product_count=Count('products'))
                  .filter(product_count__gt=2, is_completed=False)
                  .update(total_price=F('total_price') * 0.9))

    if not big_orders:
        return f"Discount applied to 0 orders."

    return f"Discount applied to {big_orders} orders."


def complete_order():
    first_order = Order.objects.filter(is_completed=False).order_by('creation_date').first()

    if not first_order:
        return ""
    first_order.is_completed = True
    first_order.save()

    for product in first_order.products.all():
        if product.in_stock > 0:
            product.in_stock -= 1
            if product.in_stock == 0:
                product.is_available=False
        product.save()
    return "Order has been completed!"

# print(complete_order())