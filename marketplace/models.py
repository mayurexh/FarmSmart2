from django.db import models
from django.contrib.auth.models import User

# Seller model
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.username

# Product model
class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Order model
class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')],
        default='Pending'
    )

    def __str__(self):
        return f"Order {self.id} by {self.buyer.username}"


#Cart model

# For Logged-in Users: Store cart items in a Cart model linked to the user.
# For Guests (Not Logged In): Use sessions to temporarily store cart items.

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Stores the user
    session_key = models.CharField(max_length=40, null=True, blank=True)  # For guests
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # The product in the cart
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product

    def total_price(self):
        return self.quantity * self.product.price  # Calculate total price of this item

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"