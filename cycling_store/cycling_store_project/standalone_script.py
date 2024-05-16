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

def inventory_function():
    print('Current inventory:')
    bikes = Vehicle.objects.all()
    for bike in bikes:
        print(bike)

    order_or_not = input('Would you like to order more vehicles?  Y/N \n')

    if order_or_not == 'N' or order_or_not == 'n':
        operate_store()

    elif order_or_not == 'Y' or order_or_not == 'y':
        order_choice = input('Which vehicle would you like to order? Enter 1 for bicycle, 2 for unicycle, 3 for tricycle, 4 for mountain bike, 5 for BMX bike \n')

        if order_choice == '1':
            bicycles = Vehicle.objects.filter(type='Bicycle')
            for bicycle in bicycles:
                bicycle.number_in_stock += int(input('How many would you like to order? \n')) #need to deal with non-int edge cases
                bicycle.save()
                print(f'You now have {bicycle.number_in_stock} bicycles')

        elif order_choice == '2':
            unicycles = Vehicle.objects.filter(type='Unicycle')
            for unicycle in unicycles:
                unicycle.number_in_stock += int(input('How many would you like to order? \n')) #need to deal with non-int edge cases
                unicycle.save()
                print(f'You now have {unicycle.number_in_stock} unicycles')

        elif order_choice == '3':
            tricycles = Vehicle.objects.filter(type='Tricycle')
            for tricycle in tricycles:
                tricycle.number_in_stock += int(input('How many would you like to order? \n')) #need to deal with non-int edge cases
                tricycle.save()
                print(f'You now have {tricycle.number_in_stock} tricycles')

        elif order_choice == '4':
            mountain_bikes = Vehicle.objects.filter(type='Mountain Bike')
            for mountain_bike in mountain_bikes:
                mountain_bike.number_in_stock += int(input('How many would you like to order? \n')) #need to deal with non-int edge cases
                mountain_bike.save()
                print(f'You now have {mountain_bike.number_in_stock} mountain bikes')

        elif order_choice == '5':
            bmx_bikes = Vehicle.objects.filter(type='BMX Bike')
            for bmx_bike in bmx_bikes:
                bmx_bike.number_in_stock += int(input('How many would you like to order? \n')) #need to deal with non-int edge cases
                bmx_bike.save()
                print(f'You now have {bmx_bike.number_in_stock} BMX Bikes')

        else:   #Returns to inventory prompt if invalid order number
            print('Invalid input')
            inventory_function()

    else:
        print('Invalid input')
    operate_store()



def customer_function():
    print('Current customers:')
    customers = Customer.objects.all()
    for customer in customers:
        print(f'{customer} - currently owns {customer.bicycles_owned} bicycles, {customer.unicycles_owned} unicycles, {customer.tricycles_owned} tricycles, {customer.mountain_bikes_owned} mountain bikes, and {customer.bmx_bikes_owned} BMX bikes')

    customer_action = input('What would you like to do? \n 1: Add a new customer \n 2: Modify a customer \n 3: Terminate a customer \n 4: Exit \n')

    if customer_action == '1':
        new_name = input("Enter the new customer's name:  ")
        new_cust = Customer(name = new_name)
        new_cust.save()
        customer_function()

    elif customer_action == '2':
        mod_choice = input('Which customer do you want to modify?  ')
        if Customer.objects.filter(name = mod_choice).exists():
            mod_name = input("Enter the customer's new name:  ")
            mod_cust = Customer.objects.filter(name = mod_choice).first()
            mod_cust.name = mod_name
            mod_cust.save()
            customer_function()
        else:
            print('That customer does not exist')
            customer_function()

    elif customer_action == '3':
        del_choice = input('Which customer do you want to terminate?  ')
        if Customer.objects.filter(name = del_choice).exists():
            Customer.objects.filter(name = del_choice).first().delete()
            customer_function()
        else:
            print('That customer does not exist')
            customer_function()

    elif customer_action == '4':
        operate_store()
    else:
        print('Invalid input')
        customer_function()

def order_function():
    print('\n Current orders: \n')
    orders = CustomerOrder.objects.all()
    for order in orders:
        print(order)
    add_or_mod = input('\n What would you like to do? \n 1: Add a new order \n 2: Modify an order \n 3: Exit \n')
    if add_or_mod == '1':
        new_order_cust = input('Which customer is this order for?  ')
        if Customer.objects.filter(name = new_order_cust).exists():
            new_order_cust = Customer.objects.filter(name = new_order_cust).first()
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
            number_ordered = int(input('How many are they ordering?  ')) # Handle non-integer inputs
            paid_yet = False
            if input("Enter 'Y' if the customer has already paid for the order  ") == 'Y' or 'y':
                paid_yet = True
            new_order = CustomerOrder(customer = new_order_cust, order = order_vehicle, number = number_ordered ,paid = paid_yet)
            new_order.save()
            order_vehicle.number_in_stock -= number_ordered
            order_vehicle.save()
            print(f'{new_order_cust} has ordered {number_ordered} {order_vehicle.type}s.  There are {order_vehicle.number_in_stock} {order_vehicle.type}s left in stock.')
            order_function()
        else:
            print('That customer does not exist')
            order_function()
    elif add_or_mod == '2':
        mod_id = int(input('Enter the ID of the order you want to modify:  '))
        mod_order = CustomerOrder.objects.filter(id = mod_id).first() # Handle non-integer inputs
        if CustomerOrder.objects.filter(id = mod_id).exists():
            num_or_pay = input('Enter 1 to change the number of vehicles ordered or 2 to mark the order as paid  ')
            if num_or_pay == '1':
                old_num = mod_order.number
                mod_order.number = int(input('Enter the updated number being ordered  '))
                print(mod_order.number)
                print(old_num)
                mod_order.save()
                stock_diff = mod_order.number - old_num
                mod_order.order.number_in_stock -= stock_diff
                mod_order.order.save()
                print(f"{mod_order.customer}'s order has been modified to {mod_order.number}.  There are now {mod_order.order.number_in_stock} {mod_order.order}s in stock.")
            elif num_or_pay == '2':
                mod_order.paid = True
                mod_order.save()
                print(f'Order {mod_id} has been paid')
            else:
                print('Invalid input')
                order_function()
        else:
            print('No order with that ID exists')
            order_function()
    elif add_or_mod == '3': 
        operate_store()
    else:
        print('invalid input')
        order_function()

def delete_order_function():
    print('\n Current orders: \n')
    orders = CustomerOrder.objects.all()
    for order in orders:
        print(order)

    delete_id = input('Enter the ID of the order you want to complete or cancel:  ')
    delete_order = CustomerOrder.objects.filter(id = delete_id).first()
    if CustomerOrder.objects.filter(id = delete_id).exists():
        complete_or_cancel = input('\n What would you like to do? \n 1: Cancel the order \n 2: Mark the order complete \n 3: Exit \n')
        if complete_or_cancel == '1':
                delete_order.order.number_in_stock += delete_order.number
                delete_order.order.save()
                print (f'Order {delete_id} has been cancelled and the ordered vehicle(s) have been returned to stock.  There are now {delete_order.order.number_in_stock} {delete_order.order}s in stock.')
                delete_order.delete()
                delete_order_function()
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
        elif complete_or_cancel == '3':
            print (delete_order.order)
            operate_store()
        else:
            print('Invalid input')
            delete_order_function()
    else:
        print('No order with that ID exists')
        delete_order_function()


operate_store()