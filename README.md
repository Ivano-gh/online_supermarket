# Centralized Online Shopping Supermarket

**Users**
1.Admin
2.Buyer/Customers

**Admin Features**
1. Add categories and perform other crud operations on them 
2. Can also perform crud operations on products
3. Can perform crud operations on orders recieved.
4. Can relay an order status to a customer.
5. Can read and delete customers recieved feedback
6. Can change(update) password and can also login and logout

One can create or register an admin using the default django admin panel
python manage.py changepassword <username>
u can replace the username with a desired username or overwrite an existing django admin using  python manage.py shell

**Customer Features**
1. Add product to cart and peform crud opeartions on the cart
2. SignUp,Login and Change password
3.  Can write a feedback about the shops services to the suoeramrket and that will be seen by the admin
4. Can view and edit profile information
5. Can view or order and cancel an order
6. Can pay to the supermarket and view the order staus of his or her product
7.Can also view extra details about a product

**TO RUN THE PROGRAM**
navigate to the online_shopping_supermarket (cd online_shopping_supermarket)
and then run python manage.py runserver. Also u may need to install other dependencies and also for the paystack keys you would have to use your own API trial test keys.
so that payment can be made.

# Install dependencies
pip install -r requirements.txt
   






