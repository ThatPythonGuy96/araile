from django.db import models
from product.models import Product
from account.models import Account

STATUS = (
    ("Pending", "Pending"),
    ("Processing", "Processing"),
    ("Shipped", "Shipped"),
    ("Delivered", "Delivered"),
)

def generate_order_id():
    last_order = Order.objects.order_by('-order_id').first()
    if last_order and last_order.order_id.startswith('ORD'):
        number = int(last_order.order_id[3:]) + 1
    else:
        number = 1
    return f"ORD{number:05d}"

class Order(models.Model):
    order_id = models.CharField(max_length=10, primary_key=True, default=generate_order_id, editable=False)
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="customer_order")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_product")
    status = models.CharField(max_length=40, choices=STATUS, default="Pending")
    total = models.DecimalField(max_digits=9, decimal_places=2)
    order_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
    #     if not self.order_id:
    #         for _ in range(5):
    #             self.order_id = generate_order_id()
    #             try:
    #                 return super().save(*args, **kwargs)
    #             except IntegrityError:
    #                 time.sleep(0.1)
    #         raise IntegrityError("Failed to generate unique order ID after multiple attempts.")
        price = self.product.price
        self.total = price
        return super().save(*args, **kwargs)