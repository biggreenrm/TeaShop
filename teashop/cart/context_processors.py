from .cart import Cart


# context processors always takes request as argument
# and returns dictionary
def cart(request):
    return {'cart': Cart(request)}