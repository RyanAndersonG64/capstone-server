import os
import django
from django.conf import settings
# Use this by running:
# python standalone_script.py
os.environ["DJANGO_SETTINGS_MODULE"] = "cycling_store_project.settings"
django.setup()

print('SCRIPT START *************************')
# Now you have django, so you can import models and do stuff as normal
### NOTE
# DO NOT CHANGE CODE ABOVE THIS LINE
# WORK BELOW

from cycling_store_app.models import *

# Add entries to vehicle table

# object_list = Vehicle.objects.bulk_create([
#     Vehicle(type='Bicycle', number_in_stock = 100),
#     Vehicle(type='Unicycle', number_in_stock = 50),
#     Vehicle(type='Tricycle', number_in_stock = 50),
#     Vehicle(type='Mountain Bike', number_in_stock = 50),
#     Vehicle(type='BMX Bike', number_in_stock = 50)
# ])



# Add entries to customer table

# object_list = Customer.objects.bulk_create([
#     Customer(name='Bob'),
#     Customer(name='Evel Knievel'),
#     Customer(name='Freddie Mercury'),
#     Customer(name='Customer 79084'),
#     Customer(name='Ryan Nyquist')
# ])



# This was necessary because I accidentally added vehicles twice

# Vehicle.objects.filter(type='Bicycle').first().delete()
# Vehicle.objects.filter(type='Unicycle').first().delete()
# Vehicle.objects.filter(type='Tricycle').first().delete()
# Vehicle.objects.filter(type='Mountain Bike').first().delete()
# Vehicle.objects.filter(type='BMX Bike').first().delete()



# bikes = Vehicle.objects.all()
# for bike in bikes:
#     print(bike)

# customers = Customer.objects.all()
# for customer in customers:
#     print(customer)



# Handles non-integer inputs

def int_inputs(input_str):
    int_input_str = 'Initializer string'
    while type(int_input_str) != int:
        try:
            int_input_str=int(input(input_str))
            if type(int_input_str) == int:
                return int_input_str
        except ValueError:
            print('please enter an integer')
            continue
        except TypeError:
            print('please enter an integer')
            continue



# Opens main menu

def operate_store():
    action = input('What would you like to do? \n 1: Manage inventory \n 2: Manage Customers \n 3: Create or modify an order \n 4: Cancel or complete an order \n 5: Exit \n')
    if action == '1':
        inventory_function()
    elif action == '2':
        customer_function()
    elif action == '3':
        order_function()
    elif action == '4':
        delete_order_function()
    elif action == '5':
        print('Exiting store')
    else:
        print('Invalid input')
        operate_store()



# Displays inventory and provides options for ordering more vehicles for store

def inventory_function():
    print('Current inventory:')
    bikes = Vehicle.objects.all()
    for bike in bikes:
        print(bike)

    order_or_not = input('Would you like to order more vehicles?  Y/N \n') # Y brings up menu to order more inventory, N goes back to main menu

    if order_or_not == 'Y' or order_or_not == 'y':
        order_choice = input('Which vehicle would you like to order? Enter 1 for bicycle, 2 for unicycle, 3 for tricycle, 4 for mountain bike, 5 for BMX bike \n')



    # Prompts user to choose a number of the selected vehicle to order, and displays how many are now in stock
    # If the user decides not to order, they can enter 0
    # Negative integers are allowed, which would represent selling/removing inventory

        if order_choice == '1':
            bicycles = Vehicle.objects.filter(type='Bicycle')
            for bicycle in bicycles:
                bicycle.number_in_stock += int_inputs('How many would you like to order? \n')
                if bicycle.number_in_stock < 0:
                    print('You cannot remove more inventory than you have')
                else: 
                    bicycle.save()
                    print(f'You now have {bicycle.number_in_stock} bicycles')

        elif order_choice == '2':
            unicycles = Vehicle.objects.filter(type='Unicycle')
            for unicycle in unicycles:
                unicycle.number_in_stock += int_inputs('How many would you like to order? \n') 
                if unicycle.number_in_stock < 0:
                    print('You cannot remove more inventory than you have')
                else: 
                    unicycle.save()
                    print(f'You now have {unicycle.number_in_stock} bicycles')

        elif order_choice == '3':
            tricycles = Vehicle.objects.filter(type='Tricycle')
            for tricycle in tricycles:
                tricycle.number_in_stock += int_inputs('How many would you like to order? \n') 
                if tricycle.number_in_stock < 0:
                    print('You cannot remove more inventory than you have')
                else: 
                    tricycle.save()
                    print(f'You now have {tricycle.number_in_stock} bicycles')

        elif order_choice == '4':
            mountain_bikes = Vehicle.objects.filter(type='Mountain Bike')
            for mountain_bike in mountain_bikes:
                mountain_bike.number_in_stock += int_inputs('How many would you like to order? \n') 
                if mountain_bike.number_in_stock < 0:
                    print('You cannot remove more inventory than you have')
                else: 
                    mountain_bike.save()
                    print(f'You now have {mountain_bike.number_in_stock} bicycles')

        elif order_choice == '5':
            bmx_bikes = Vehicle.objects.filter(type='BMX Bike')
            for bmx_bike in bmx_bikes:
                bmx_bike.number_in_stock += int_inputs('How many would you like to order? \n') 
                if bmx_bike.number_in_stock < 0:
                    print('You cannot remove more inventory than you have')
                else: 
                    bmx_bike.save()
                    print(f'You now have {bmx_bike.number_in_stock} bicycles')


        else:   #Returns to inventory prompt if invalid order number
            print('Invalid input')

        inventory_function()    #Allows user to continue managing inventory after ordering stock
    elif order_or_not == 'N' or order_or_not == 'n':
        operate_store()
    else:
        print('Invalid input \n')
        inventory_function()



# Displays customers and allows user to add or delete a customer, or change a customer's name

def customer_function():
    print('Current customers:')
    customers = Customer.objects.all()
    for customer in customers:
        print(f'{customer} - currently owns {customer.bicycles_owned} bicycles, {customer.unicycles_owned} unicycles, {customer.tricycles_owned} tricycles, {customer.mountain_bikes_owned} mountain bikes, and {customer.bmx_bikes_owned} BMX bikes')

    customer_action = input('What would you like to do? \n 1: Add a new customer \n 2: Modify a customer \n 3: Terminate a customer \n 4: Exit \n')


    # Entering 1 allows adding a new customer and entering their name

    if customer_action == '1':
        new_name = input("Enter the new customer's name:  ")
        new_cust = Customer(name = new_name)
        new_cust.save()
        customer_function()


    # Entering 2 allows changing a customer's name

    elif customer_action == '2':
        mod_choice = input('Enter the ID of the customer you want to modify:  ')
        if Customer.objects.filter(id = mod_choice).exists():
            mod_name = input("Enter the customer's new name:  ")
            mod_cust = Customer.objects.filter(id = mod_choice).first()
            mod_cust.name = mod_name
            mod_cust.save()
            customer_function()
        else:
            print('No customer has that ID')
            customer_function()


    # Entering 3 allows deleting a customer by entering their ID

    elif customer_action == '3':
        del_choice = input('Enter the ID of the customer you want to terminate:  ')
        if Customer.objects.filter(id = del_choice).exists():
            Customer.objects.filter(id = del_choice).first().delete()
            customer_function()
        else:
            print('No customer has that ID')
            customer_function()


    # Entering 4 returns to main menu

    elif customer_action == '4':
        operate_store()


    # Invalid input brings up customer menu again  

    else:
        print('Invalid input')
        customer_function()


    # Displays current orders and allows user to create an order or update an existing one

def order_function():
    print('\n Current orders: \n')
    orders = CustomerOrder.objects.all()
    for order in orders:
        print(order)

    add_or_mod = input('\n What would you like to do? \n 1: Add a new order \n 2: Modify an order \n 3: Exit \n')


    # Entering 1 allows user to create a new order by specifying customer, vehicle and number of vehicles

    if add_or_mod == '1':
        new_order_cust = input('Enter the ID of the customer placing the order:  ')
        if Customer.objects.filter(id = new_order_cust).exists():
            new_order_cust = Customer.objects.filter(id = new_order_cust).first()
            order_vehicle = input('Which vehicle are they ordering?  Enter 1 for bicycle, 2 for unicycle, 3 for tricycle, 4 for mountain bike, 5 for BMX bike \n')
            if order_vehicle == '1':
                order_vehicle = Vehicle.objects.filter(type='Bicycle').first()
            elif order_vehicle == '2':
                order_vehicle = Vehicle.objects.filter(type='Unicycle').first()
            elif order_vehicle == '3':
                order_vehicle = Vehicle.objects.filter(type='Tricycle').first()
            elif order_vehicle == '4':
                order_vehicle = Vehicle.objects.filter(type='Mountain Bike').first()
            elif order_vehicle == '5':
                order_vehicle = Vehicle.objects.filter(type='BMX Bike').first()
            else:
                print('Invalid input')
                order_function()


            # Prevents ordering more vehicles than are available

            number_ordered = int_inputs('How many are they ordering?  ') 
            if number_ordered > order_vehicle.number_in_stock:
                print('There are not enough vehicles in stock for this order')
            else:
                paid_yet = False
                if input("Enter 'Y' if the customer has already paid for the order  ") == 'Y' or 'y':
                    paid_yet = True
                new_order = CustomerOrder(customer = new_order_cust, order = order_vehicle, number = number_ordered ,paid = paid_yet)
                new_order.save()
                order_vehicle.number_in_stock -= number_ordered
                order_vehicle.save()
                print(f'{new_order_cust.name} has ordered {number_ordered} {order_vehicle.type}s.  There are {order_vehicle.number_in_stock} {order_vehicle.type}s left in stock.')

            order_function() # Allows user to continue managing orders

        else:
            print('No customer has that ID')
            order_function() #Brings up orde prompt again after entering non-existent ID


    # Entering 2 allows user to change the number of vehicles being ordered or mark an unpaid order as paid

    elif add_or_mod == '2':
        mod_id = int_inputs('Enter the ID of the order you want to modify:  ')
        mod_order = CustomerOrder.objects.filter(id = mod_id).first()
        if CustomerOrder.objects.filter(id = mod_id).exists():
            num_or_pay = input('Enter 1 to change the number of vehicles ordered or 2 to mark the order as paid  ')
            if num_or_pay == '1':
                old_num = mod_order.number
                mod_order.number = int_inputs('Enter the updated number being ordered:  ')
                mod_order.save()
                stock_diff = mod_order.number - old_num
                mod_order.order.number_in_stock -= stock_diff


                # Prevents changing an order to more vehicles than are in stock

                if mod_order.number > mod_order.order.number_in_stock:
                    print(f'There are not enough {mod_order.order.type}s for this order')
                else:
                    mod_order.order.save()
                    print(f"{mod_order.customer.name}'s order has been modified to {mod_order.number}.  There are now {mod_order.order.number_in_stock} {mod_order.order.type}s in stock.")

            elif num_or_pay == '2':
                mod_order.paid = True
                mod_order.save()
                print(f'Order {mod_id} has been paid')
            else:
                print('Invalid input')

        else:
            print('No order with that ID exists')

        order_function() # Allows user to continue managing orders

    elif add_or_mod == '3': # Exits back to main menu
        operate_store()
    else:
        print('invalid input')
        order_function() # Returns to order prompt on invalid input


    # Allows an order to be completed (which deletes it and updated number of vehicles owned by customer)
    # or cancelled (which deletes it and returns ordered vehicles to stock)

def delete_order_function():
    print('\n Current orders: \n')
    orders = CustomerOrder.objects.all()
    for order in orders:
        print(order)

    delete_id = input('Enter the ID of the order you want to complete or cancel:  ')
    delete_order = CustomerOrder.objects.filter(id = delete_id).first()
    if CustomerOrder.objects.filter(id = delete_id).exists():
        complete_or_cancel = input('\n What would you like to do? \n 1: Cancel the order \n 2: Mark the order complete \n 3: Exit \n')

        
        # Cancelling an order returns vehicles to stocks

        if complete_or_cancel == '1':
                delete_order.order.number_in_stock += delete_order.number
                delete_order.order.save()
                print (f'Order {delete_id} has been cancelled and the ordered vehicle(s) have been returned to stock.  There are now {delete_order.order.number_in_stock} {delete_order.order.type}s in stock.')
                delete_order.delete()
                delete_order_function()


        # Completing an order updates vehicles owned by customer

        elif complete_or_cancel == '2':
                if delete_order.order.type =='Bicycle':
                    delete_order.customer.bicycles_owned += delete_order.number
                    print(f'{delete_order.customer} has recieved their {delete_order.number} {delete_order.order.type}s.  They now own {delete_order.customer.bicycles_owned} bicycles.')
                elif delete_order.order.type =='Unicycle':
                    delete_order.customer.unicycles_owned += delete_order.number
                    print(f'{delete_order.customer} has recieved their {delete_order.number} {delete_order.order.type}s.  They now own {delete_order.customer.unicycles_owned} unicycles.')
                elif delete_order.order.type =='Tricycle':
                    delete_order.customer.tricycles_owned += delete_order.number
                    print(f'{delete_order.customer} has recieved their {delete_order.number} {delete_order.order.type}s.  They now own {delete_order.customer.tricycles_owned} tricycles.')
                elif delete_order.order.type =='Mountain Bike':
                    delete_order.customer.mountain_bikes_owned += delete_order.number
                    print(f'{delete_order.customer} has recieved their {delete_order.number} {delete_order.order.type}s.  They now own {delete_order.customer.mountain_bikes_owned} mountain bikes.')
                elif delete_order.order.type =='BMX Bike':
                    delete_order.customer.bmx_bikes_owned += delete_order.number
                    print(f'{delete_order.customer} has recieved their {delete_order.number} {delete_order.order}s.  They now own {delete_order.customer.bmx_bikes_owned} BMX bikes.')
                delete_order.customer.save()
                delete_order.delete()
                delete_order_function()

        elif complete_or_cancel == '3': # Exits to main menu
            operate_store()
        else:
            print('Invalid input')
            delete_order_function() # Returns to ccomplete/cancel prompt on invalid input
    else:
        print('No order with that ID exists')
        delete_order_function() # Returns to ccomplete/cancel prompt if non-exisxted ID is entered


operate_store()