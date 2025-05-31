from django.shortcuts import render,redirect
from .models import Carousel,Cart,Booking
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .models import Category,Product,ORDERSTATUS
from django.contrib.auth.models import User  # For User model  # If UserProfile is in models, add it here too
from .models import UserProfile 
from django.contrib.auth.decorators import login_required
import json



from django.shortcuts import render, redirect 

# Create your views here.

def home(request):
    return render(request,'home.html')


@login_required
def user_dashboard(request):
    # This is your user dashboard
    return render(request, 'user_dashboard.html')

def index(request):
    return render(request,'navigation.html')

def about(request):
    return render(request,'about.html')

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
    return render(request, 'admin_dashboard.html')


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
                return redirect('user_dashboard')
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

def booking(request):
    user = UserProfile.objects.get(user=request.user)
    cart = Cart.objects.get(user=request.user)
    total = 0
    product_data = (cart.product).replace("'", '"')
    product_data = json.loads(str(product_data))

    # Check if cart is empty BEFORE accessing [0]
    if not product_data.get('objects') or not product_data['objects'][0]:
        messages.error(request, "Cart is empty, Please add product in cart.")
        return redirect('cart')

    productid = product_data['objects'][0]

    for i, j in productid.items():
        product = Product.objects.get(id=i)
        price_str = str(product.price).replace('$', '').replace('Ghc.', '').replace('Rs.', '').replace('€', '').strip()
        total += float(j) * float(price_str)

    if request.method == "POST":
        # Double-check cart is not empty before booking
        if not productid:
            messages.error(request, "Cart is empty, Please add product in cart.")
            return redirect('cart')
        book = Booking.objects.create(user=request.user, product=cart.product, total=total)
        cart.product = json.dumps({'objects': []})  # Clear cart after booking
        cart.save()
        messages.success(request, "Book Order Successfully")
        return redirect('main')
    return render(request, "booking.html", locals())

def myOrder(request):
    order = Booking.objects.filter(user=request.user)
    return render(request, "my-order.html", locals())

def user_order_track(request, pid):
    order = Booking.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    order_status_int = int(order.status) 
    return render(request, "user-order-track.html", locals())