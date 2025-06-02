from django import template
from groceryapp.models import Product, Booking
import json

register = template.Library()

@register.filter()
def applydiscount(pid):
    try:
        data = Product.objects.get(id=pid)
        price_str = str(data.price).replace('$', '').replace('Ghc.', '').replace('Rs.', '').strip()
        discount_str = str(data.discount).replace('%', '').strip()
        price = float(price_str)
        discount = float(discount_str)
        discounted_price = price * (100 - discount) / 100
        return round(discounted_price, 2)
    except (Product.DoesNotExist, ValueError):
        return 0

@register.filter()
def productimage(pid):
    try:
        data = Product.objects.get(id=pid)
        return data.image.url
    except Product.DoesNotExist:
        return ""

@register.filter()
def productname(pid):
    try:
        data = Product.objects.get(id=pid)
        return data.name
    except Product.DoesNotExist:
        return ""

@register.filter()
def productprice(pid):
    try:
        data = Product.objects.get(id=pid)
        return data.price
    except Product.DoesNotExist:
        return 0

@register.simple_tag()
def producttotalprice(pid, qty):
    try:
        data = Product.objects.get(id=pid)
        price_str = str(data.price).replace('$', '').replace('Ghc.', '').replace('Rs.', '').replace('€', '').strip()
        price = float(price_str)
        qty = int(qty)
        return round(price * qty, 2)
    except (Product.DoesNotExist, ValueError):
        return 0

@register.filter()
def get_product(productli):
    try:
        productli = productli.replace("'", '"')
        myli = json.loads(str(productli))['objects'][0]
        pro_li = [int(i) for i in myli.keys()]
        product = Product.objects.filter(id__in=pro_li)
        return product
    except (json.JSONDecodeError, KeyError, ValueError, TypeError):
        return None

@register.simple_tag
def get_qty(pro, bookid):
    try:
        book = Booking.objects.get(id=bookid)
        productli = book.product.replace("'", '"')
        myli = json.loads(str(productli))['objects'][0]
        return myli.get(str(pro), 0)
    except (Booking.DoesNotExist, json.JSONDecodeError, KeyError, ValueError, TypeError):
        return 0