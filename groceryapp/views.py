from django.shortcuts import render,redirect
from .models import Carousel,Cart,Booking
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .models import Category,Product,ORDERSTATUS,Feedback
from django.contrib.auth.models import User  # For User model  # If UserProfile is in models, add it here too
from .models import UserProfile 
from django.contrib.auth.decorators import login_required
import json



from django.shortcuts import render, redirect 

# Create your views here.

def home(request):
    data = Carousel.objects.all()
    dic = {'data': data}
    return render(request, 'index.html', dic)


@login_required
def user_dashboard(request):
    # This is your user dashboard
    return render(request, 'user_dashboard.html')

def index(request):
    return render(request,'navigation.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request, 'contact.html')

def main(request):
    data = Carousel.objects.all()
    dic = {'data':data}
    return render(request, 'index.html', dic)

def adminLogin(request):
    msg = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(request, user)
                messages.success(request, "You have successfully logged in")
                return redirect('admindashboard')
            else:
                messages.success(request, "Invalid Credentials")
        except:
            messages.success(request, "Invalid Credentials")
    
    return render(request, 'admin_login.html')

def adminHome(request):
    return render(request, 'admin_base.html')

def admin_dashboard(request):
    user = UserProfile.objects.filter()
    category = Category.objects.filter()
    product = Product.objects.filter()
    new_order = Booking.objects.filter(status=1)
    dispatch_order = Booking.objects.filter(status=2)
    way_order = Booking.objects.filter(status=3)
    deliver_order = Booking.objects.filter(status=4)
    cancel_order = Booking.objects.filter(status=5)
    return_order = Booking.objects.filter(status=6)
    order = Booking.objects.filter()
    read_feedback = Feedback.objects.filter(status=1)
    unread_feedback = Feedback.objects.filter(status=2)
    return render(request, 'admin_dashboard.html', locals())

def add_category(request):
    if request.method == "POST":
        name = request.POST['name']
        Category.objects.create(name=name)
        messages.success(request, "Category added")
        return redirect('view_category')
    return render(request, 'add_category.html', locals())
 
def view_category(request):
    category = Category.objects.all()
    return render(request, 'view_category.html', locals())

def edit_category(request, pid):
    category = Category.objects.get(id=pid)
    if request.method == "POST":
        name = request.POST['name']
        category.name = name
        category.save()
        messages.success(request, "Category updated")
        return redirect('view_category')
    return render(request, 'edit_category.html', locals())

def delete_category(request, pid):
    category = Category.objects.get(id=pid)
    category.delete()
    messages.success(request, "Category deleted")
    return redirect('view_category')


def add_product(request):
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        discount = request.POST['discount']
        desc = request.POST['desc']
        image = request.FILES['image']
        catobj = Category.objects.get(id=cat)
        Product.objects.create(name=name, price=price, discount=discount, category=catobj, description=desc, image=image)
        messages.success(request, "Product added")
    return render(request, 'add_product.html', locals())

def view_product(request):
    product = Product.objects.all()
    return render(request, 'view_product.html', locals())

def edit_product(request, pid):
    product = Product.objects.get(id=pid)
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        discount = request.POST['discount']
        desc = request.POST['desc']
        try:
            image = request.FILES['image']
            product.image = image
            product.save()
        except:
            pass
        catobj = Category.objects.get(id=cat)
        Product.objects.filter(id=pid).update(name=name, price=price, discount=discount, category=catobj, description=desc)
        messages.success(request, "Product Updated")
        return redirect('view_product')
    return render(request, 'edit_product.html', locals())

def delete_product(request, pid):
    product = Product.objects.get(id=pid)
    product.delete()
    messages.success(request, "Product Deleted")
    return redirect('view_product')

from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile

def registration(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        image = request.FILES.get('image')  # Safely get the image
        
        # Create user and profile
        user = User.objects.create_user(
            username=email, 
            first_name=fname, 
            last_name=lname, 
            email=email, 
            password=password
        )

        # If image is provided, use it; otherwise, create the profile without it
        UserProfile.objects.create(
            user=user, 
            mobile=mobile, 
            address=address, 
            image=image if image else None
        )

        messages.success(request, "Registration Successful")
        return redirect('userlogin')
    return render(request, 'registration.html', locals())

def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "User login successfully")
            return redirect('user_dashboard')  # Redirect to dashboard, not main
        else:
            messages.error(request, "Invalid Credentials")
    return render(request, 'login.html')

@login_required
def profile(request):
    # Always get or create the profile for the user
    data, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        address = request.POST['address']
        mobile = request.POST['mobile']
        try:
            image = request.FILES['image']
            data.image = image
            data.save()
        except:
            pass
        user = User.objects.filter(id=request.user.id).update(first_name=fname, last_name=lname, email=email)
        UserProfile.objects.filter(id=data.id).update(mobile=mobile, address=address)
        messages.success(request, "Profile updated")
        return redirect('user_dashboard')
    return render(request, 'profile.html', {'data': data})


def logoutuser(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('main')

from django.contrib.auth import authenticate, login

def change_password(request):
    if request.method == 'POST':
        o = request.POST.get('currentpassword')
        n = request.POST.get('newpassword')
        c = request.POST.get('confirmpassword')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                # Re-authenticate and log the user in again
                user = authenticate(username=request.user.username, password=n)
                if user:
                    login(request, user)
                messages.success(request, "Password Changed")
                return redirect('userlogin')
            else:
                messages.error(request, "Password not matching")
                return redirect('change_password')
        else:
            
            messages.error(request, "Invalid Password")
            return redirect('change_password')
    return render(request, 'change_password.html')

def user_product(request,pid):
    if pid == 0:
        product = Product.objects.all()
    else:
        category = Category.objects.get(id=pid)
        product = Product.objects.filter(category=category)
    allcategory = Category.objects.all()
    return render(request, "user-product.html", locals())

def product_detail(request, pid):
    product = Product.objects.get(id=pid)
    latest_product = Product.objects.filter().exclude(id=pid).order_by('-id')[:10]
    return render(request, "product_detail.html", locals())


def addToCart(request, pid):
    myli = {"objects": []}
    try:
        cart = Cart.objects.get(user=request.user)
        myli = json.loads((str(cart.product)).replace("'", '"'))
        # Try to update the quantity for this pid
        if myli['objects']:
            if str(pid) in myli['objects'][0]:
                myli['objects'][0][str(pid)] += 1
            else:
                myli['objects'][0][str(pid)] = 1
        else:
            myli['objects'].append({str(pid): 1})
        cart.product = json.dumps(myli)
        cart.save()
    except Cart.DoesNotExist:
        myli['objects'].append({str(pid): 1})
        cart = Cart.objects.create(user=request.user, product=json.dumps(myli))
    return redirect('cart')

def incredecre(request, pid):
    cart = Cart.objects.get(user=request.user)
    if request.GET.get('action') == "incre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
    if request.GET.get('action') == "decre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        if myli['objects'][0][str(pid)] == 1:
            del myli['objects'][0][str(pid)]
        else:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) - 1
    cart.product = myli
    cart.save()
    return redirect('cart')

def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        product = (cart.product).replace("'", '"')
        myli = json.loads(str(product))
        product = myli['objects'][0]
    except:
        product = []
    lengthpro = len(product)
    return render(request, 'cart.html', locals())

def deletecart(request, pid):
    cart = Cart.objects.get(user=request.user)
    product = (cart.product).replace("'", '"')
    myli = json.loads(str(product))
    del myli['objects'][0][str(pid)]
    cart.product = myli
    cart.save()
    messages.success(request, "Delete Successfully")
    return redirect('cart')

@login_required
def booking(request):
    try:
        user = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('main')

    try:
        cart = Cart.objects.get(user=request.user)
        product_data = (cart.product).replace("'", '"')
        product_data = json.loads(str(product_data))
        productid = product_data.get('objects', [{}])[0]
    except (Cart.DoesNotExist, IndexError, KeyError, ValueError, TypeError):
        messages.error(request, "Cart is empty, Please add product in cart.")
        return redirect('cart')

    if not productid:
        messages.error(request, "Cart is empty, Please add product in cart.")
        return redirect('cart')

    total = 0
    discounted = 0
    deduction = 0

    for i, j in productid.items():
        try:
            product = Product.objects.get(id=i)
            # Clean price and discount
            price_str = str(product.price).replace('$', '').replace('Ghc.', '').replace('Rs.', '').replace('€', '').strip()
            discount_str = str(product.discount).replace('%', '').strip()
            price = float(price_str)
            discount = float(discount_str)
            qty = int(j)
            total += qty * price
            discounted_price = price * (100 - discount) / 100
            discounted += qty * discounted_price
        except (Product.DoesNotExist, ValueError, TypeError):
            continue

    deduction = total - discounted

    if request.method == "POST":
        return redirect(f'/payment/?total={total}&discounted={discounted}&deduction={deduction}')

    return render(request, "booking.html", {
        "user": user,
        "cart": cart,
        "total": total,
        "discounted": discounted,
        "deduction": deduction,
        "productid": productid,
    })


def myOrder(request):
    order = Booking.objects.filter(user=request.user)
    return render(request, "my-order.html", locals())

def user_order_track(request, pid):
    order = Booking.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    order_status_int = int(order.status) 
    return render(request, "user-order-track.html", locals())

def change_order_status(request, pid):
    order = Booking.objects.get(id=pid)
    status = request.GET.get('status')
    if status:
        order.status = status
        order.save()
        messages.success(request, "Order status changed.")
    return redirect('myorder')

def user_feedback(request):
    user = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        Feedback.objects.create(user=request.user, message=request.POST['feedback'])
        messages.success(request, "Feedback sent successfully")
    return render(request, "feedback-form.html", locals())

def manage_feedback(request):
    action = request.GET.get('action', 0)
    feedback = Feedback.objects.filter(status=int(action))
    return render(request, 'manage_feedback.html', locals())

def delete_feedback(request, pid):
    feedback = Feedback.objects.get(id=pid)
    feedback.delete()
    messages.success(request, "Deleted successfully")
    return redirect('manage_feedback')


def mark_feedback_read(request, pid):
    feedback = Feedback.objects.get(id=pid)
    feedback.status = 1  # 1 means "Read"
    feedback.save()
    return redirect('manage_feedback')


from django.conf import settings

def payment(request):
    total = request.GET.get('total')
    user = UserProfile.objects.get(user=request.user)
    from django.conf import settings
    context = {
        'total': total,
        'user': user,  
        'PAYSTACK_PUBLIC_KEY': settings.PAYSTACK_PUBLIC_KEY,
    }
    return render(request, "payment.html", context)
import requests
from django.conf import settings
from django.http import HttpResponse

def verify_payment(request):
    reference = request.GET.get('reference')
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    resp = requests.get(url, headers=headers)
    result = resp.json()
    if result['data']['status'] == 'success':
        user = request.user
        cart = Cart.objects.get(user=user)
        total = request.GET.get('total')
        Booking.objects.create(user=user, product=cart.product, total=total)
        cart.product = {'objects': []}
        cart.save()
        messages.success(request, "Payment successful! Order booked.")
        return redirect('myorder')  # Redirect to your order page
    else:
        messages.error(request, "Payment failed or not verified.")
        return redirect('cart') 
    
def manage_order(request):
    action = request.GET.get('action', 0)
    order = Booking.objects.filter(status=int(action))
    order_status = ORDERSTATUS[int(action)-1][1]
    if int(action) == 0:
        order = Booking.objects.filter()
        order_status = 'All'
    return render(request, 'manage_order.html', locals()) 

def delete_order(request, pid):
    order = Booking.objects.get(id=pid)
    order.delete()
    messages.success(request, 'Order Deleted')
    return redirect('/manage-order/?action='+request.GET.get('action'))

def admin_order_track(request, pid):
    order = Booking.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    status = int(request.GET.get('status',0))
    if status:
        order.status = status
        order.save()
        return redirect('admin_order_track', pid)
    return render(request, 'admin-order-track.html', locals())

def manage_user(request):
    user = UserProfile.objects.all()
    return render(request, 'manage_user.html', locals()) 

def delete_user(request, pid):
    try:
        user = User.objects.get(id=pid)
        try:
            userprofile = UserProfile.objects.get(user=user)
            userprofile.delete()
        except UserProfile.DoesNotExist:
            pass  # It's ok if the profile is already gone
        user.delete()
        messages.success(request, "User deleted successfully")
    except User.DoesNotExist:
        messages.error(request, "User does not exist or was already deleted.")
    return redirect('manage_user')

def admin_change_password(request):
    if request.method == 'POST':
        o = request.POST.get('currentpassword')
        n = request.POST.get('newpassword')
        c = request.POST.get('confirmpassword')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('admin_login')
            else:
                messages.success(request, "Password not matching")
                return redirect('admin_change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('admin_change_password')
    return render(request, 'admin_change_password.html')

def home_products(request):
    products = Product.objects.all()
    return render(request, 'home_products.html', {'products': products})