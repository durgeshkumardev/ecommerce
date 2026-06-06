from django.shortcuts import redirect, render
from django.http import HttpResponse

from django.contrib import messages

# import for the logn 

from django.contrib.auth import authenticate, login


# Create your views here.

from .models import Role, User, Category, Product, ProductImage

def home(request):
    return render(request, 'home.html')

def electronics(request):
    return render(request,'electronic.html')


def admin_dashboard(request):
    return render(request,'dashboard.html')


# this is have add product business logic
def add_product(request):

    return render(request, 'addProduct.html')


def  add_category(request):
    if request.method == 'POST':
        try:
            category_name = request.POST.get('category_name')
            description = request.POST.get('description')

            # form validation
            if not category_name:
                messages.error(request, 'Category name is required!')
                return render(request, 'addCategory.html')

            # check unique category name validation database
            if Category.objects.filter(category_name=category_name).exists():
                messages.error(request, 'Category name already exists!')
                return render(request, 'addCategory.html')

        # Create and save the new category
            category = Category(category_name=category_name, description=description)
            category.save()

            messages.success(request, 'Category added successfully!')

        except Exception as e:
            messages.error(request, f'Error adding category: {str(e)}')
        

    return render(request, 'addCategory.html')


# show category list

def category_list(request):
    categories=Category.objects.all()
    return render(request,'categoryList.html',{'categories':categories})



# add UserRole

def add_user_role(request):
    if request.method=="POST":
        try:
            role_name=request.POST.get('role_name')

            # form validation
            if not role_name:
                messages.error(request, 'Role name is required!')
                return render(request, 'addUserRole.html')
            
            # check unique role name validation database
            if Role.objects.filter(role_name=role_name).exists():
                messages.error(request, 'Role name already exists!')
                return render(request, 'addUserRole.html')

            # Create and save the new role
            role = Role(role_name=role_name)
            role.save()
            messages.success(request, 'Role added successfully!')
        except Exception as e:
            messages.error(request, f'Error adding role: {str(e)}')
    return render(request, 'addUserRole.html')



# Add Product 

def add_product(request):
    categories = Category.objects.filter(is_active=True)

    if request.method == 'POST':
        try:
            product_name = request.POST.get('product_name')
            short_description = request.POST.get('short_description')
            long_description = request.POST.get('long_description')
            price = request.POST.get('price')
            stock_quantity = request.POST.get('stock_quantity')
            category_id = request.POST.get('category_id')

            # get Image from form
            product_image = request.FILES.get('product_image')

            # form validation
            if not product_name or not price or not stock_quantity or not category_id:
                messages.error(request, 'All fields are required!')
                return render(request, 'addProduct.html', {'categories': categories})

            # check unique product name validation database
            if Product.objects.filter(product_name=product_name).exists():
                messages.error(request, 'Product name already exists!')
                return render(request, 'addProduct.html', {'categories': categories})

            # Create and save the new product
            category = Category.objects.get(id=category_id)
            product = Product(
                product_name=product_name,
                short_description=short_description,
                long_description=long_description,
                price=price,
                stock_quantity=stock_quantity,
                category=category
            )
            product.save()

            if product_image:
                
                product_image_instance = ProductImage(product=product, image=product_image)
                product_image_instance.save()

            messages.success(request, 'Product added successfully!')

        except Exception as e:
            messages.error(request, f'Error adding product: {str(e)}')

    return render(request, 'addProduct.html', {'categories': categories})



# user registration view find the  role from the database user and that id add in the user table and save the user data in database

def user_registration(request):
    roles = Role.objects.filter()

    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            mobile_no = request.POST.get('mobile_no')
            profile_image = request.FILES.get('profile_image')
          

            # form validation
            if not first_name or not last_name or not email or not password:
                messages.error(request, 'All fields are required!')
                return render(request, 'register.html', {'roles': roles})

            # check unique username and email validation database
     

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists!')
                return render(request, 'register.html', {'roles': roles})
            
            username = email.split('@')[0]  # Generate username from email

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return render(request, 'register.html', {'roles': roles})

            # Create and save the new user
            role = Role.objects.get(role_name="user")

            user=User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
                role=role,
            )
            if user.mobile_no:
                user.mobile_no = mobile_no

            if profile_image:
                user.profile_image = profile_image
            user.save()

            messages.success(request, 'User registered successfully!')

        except Exception as e:
            print(e)
            messages.error(request, f'Error registering user: {str(e)}')

    return render(request, 'register.html')


# user login 
def user_login(request):

    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')

            # form validation
            if not email or not password:
                messages.error(request, 'Email and password are required!')
                return render(request, 'login.html')

            # check user authentication
            user = User.objects.filter(email=email).first()

            if user and user.check_password(password):
                messages.success(request, 'Login successful!')
                return redirect(request, 'home.html')
            else:
                messages.error(request, 'Invalid email or password!')
                return render(request, 'login.html')

        except Exception as e:
            messages.error(request, f'Error during login: {str(e)}')
            return render(request, 'login.html')



    return render(request, 'login.html')
