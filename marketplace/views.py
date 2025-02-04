from django.shortcuts import render,redirect, get_object_or_404
from .models import Seller, Product, CartItem
from .forms import SellerRegistrationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
def market_home(request):
    products = Product.objects.all()
    return render(request, "marketplace/market_home.html", {"products":products})


#Register as a Seller

@login_required
def become_seller(request):
    if request.method == "POST":
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        if address and phone:
            Seller.objects.create(user=request.user, address=address, phone=phone)
            return redirect("market_home")  # Redirect to marketplace homepage

    return render(request, "marketplace/become_seller.html")


@login_required
def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        image = request.FILES.get("image")

        if name and description and price and stock:
            Product.objects.create(
                seller=request.user.seller,  # Link product to the logged-in seller
                name=name,
                description=description,
                price=price,
                stock=stock,
                image=image,
            )
            return redirect("market_home")  # Redirect after adding product

    return render(request, "marketplace/add_product.html")


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "marketplace/product_detail.html", {"product": product})


#Cart functionality 
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        # User is logged in, store in database
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
    else:
        # Guest User: Use session-based cart
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        cart_item, created = CartItem.objects.get_or_create(session_key=session_key, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()

    # return JsonResponse({"success": True, "message": "Item added to cart"})
    return redirect("cart")


#Cart view
def cart_view(request):
    if request.user.is_authenticated:
        cart_items  = CartItem.objects.filter(user = request.user)
        
    else:
        session_key = request.session.session_key
        cart_items  = CartItem.objects.filter(session_key = session_key)
        
    total = sum(item.total_price() for item in cart_items)
    
    return render(request, "marketplace/cart.html", {"cart_items": cart_items, "total": total})

#Update cart
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user = request.user)

    action = request.GET.get("action")
    if action == "increase":
        if cart_item.quantity == cart_item.product.stock:
            pass
        else:
            cart_item.quantity += 1
    elif action == "decrease" and cart_item.quantity > 1:
        cart_item.quantity -= 1

    cart_item.save()
    return redirect("cart")


#Remove cart item
def remove_cart_item(request, item_id):
    session_key = request.session.session_key

    if not session_key:  # Ensure session key exists for guests
        request.session.create()
        session_key = request.session.session_key
    
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(id= item_id, user = request.user)
        
    else:
        cart_item = get_object_or_404(CartItem, id = item_id, session_key = session_key)
        
    cart_item.delete()
    
    
    return redirect("cart")