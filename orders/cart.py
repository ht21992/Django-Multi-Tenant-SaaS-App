# orders/cart.py
from decimal import Decimal
from products.models import Product

CART_SESSION_ID = "cart"


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)

        if not cart:
            cart = self.session[CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product_id, quantity=1):
        print("here: ", product_id)
        product_id = str(product_id)

        if product_id not in self.cart:
            product = Product.objects.get(id=product_id)
            self.cart[product_id] = {
                "name": product.name,
                "price": str(product.price),
                "quantity": 0,
            }

        self.cart[product_id]["quantity"] += quantity
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session[CART_SESSION_ID] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def get_items(self):
        items = []
        for product_id, item in self.cart.items():
            items.append(
                {
                    "product_id": product_id,
                    "name": item["name"],
                    "price": Decimal(item["price"]),
                    "quantity": item["quantity"],
                    "subtotal": Decimal(item["price"]) * item["quantity"],
                }
            )
        return items

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )
