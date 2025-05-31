from django import template
from groceryapp.models import Product
register = template.Library()

@register.filter()
def applydiscount(pid):
    data = Product.objects.get(id=pid)
    # Remove any currency symbols and convert to float
    price_str = str(data.price).replace('$', '').replace('Ghc.', '').replace('Rs.', '').strip()
    discount_str = str(data.discount).replace('%', '').strip()
    try:
        price = float(price_str)
        discount = float(discount_str)
    except ValueError:
        return data.price  # fallback to original price if conversion fails
    discounted_price = price * (100 - discount) / 100
    # Optionally, round to 2 decimal places
    return round(discounted_price, 2)

@register.filter()
def productimage(pid):
    data = Product.objects.get(id=pid)
    return data.image.url

@register.filter()
def productname(pid):
    data = Product.objects.get(id=pid)
    return data.name

@register.filter()
def productprice(pid):
    data = Product.objects.get(id=pid)
    return data.price

@register.simple_tag()
def producttotalprice(pid, qty):
    data = Product.objects.get(id=pid)
    # Remove any currency symbols and convert to float
    price_str = str(data.price).replace('$', '').replace('Ghc.', '').replace('Rs.', '').replace('€', '').strip()
    try:
        price = float(price_str)
        qty = int(qty)
    except ValueError:
        return data.price  # fallback to original price if conversion fails
    return round(price * qty, 2)