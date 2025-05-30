from django.shortcuts import render,redirect
from .models import Carousel
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .models import Category,Product
from django.contrib.auth.models import User  # For User model  # If UserProfile is in models, add it here too
from .models import UserProfile 
from django.contrib.auth.decorators import login_required



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