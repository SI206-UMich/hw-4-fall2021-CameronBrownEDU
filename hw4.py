# -*- coding: utf-8 -*-
import unittest
import random
import math

# The Customer class
# The Customer class represents a customer who will order from the stalls.
class Customer: 
    # Constructor
    def __init__(self, name, wallet = 100):
        self.name = name
        self.wallet = wallet

    # Reload some deposit into the customer's wallet.
    def reload_money(self,deposit):
        self.wallet += deposit

    # The customer orders the food and there could be different cases   
    def validate_order(self, cashier, stall, item_name, quantity):
        success = False
        if not(cashier.has_stall(stall)):
            print("Sorry, we don't have that vendor stall. Please try a different one.")
        elif not(stall.has_item(item_name, quantity)):  
            print("Our stall has run out of " + item_name + " :( Please try a different stall!")
        elif self.wallet < stall.compute_cost(quantity): 
            print("Don't have enough money for that :( Please reload more money!")
        else:
            success = True
            bill = cashier.place_order(stall, item_name, quantity) 
            self.submit_order(cashier, stall, bill) 
            print("Great buy! You've purchased " + str(quantity) + " " + item_name + "!")
           
            #extra credit
            cashier.orders += 1
            if cashier.orders % 10 == 0:
                print("Congratulations, you've been entered to win $10!")
                five_percent = random.randrange(1, 100)
                if five_percent <= 5:
                    print("You've won $10! Congratulations")
                    self.reload_money(10)
                    cashier.earnings -= 10
                else:
                    print("Aww, you didn't win. Better luck next time!")


        return success
    
    # Submit_order takes a cashier, a stall and an amount as parameters, it deducts the amount from the customer’s wallet and calls the receive_payment method on the cashier object
    def submit_order(self, cashier, stall, amount): 
        self.wallet -= amount
        cashier.receive_payment(stall,amount)
        pass

    # The __str__ method prints the customer's information.    
    def __str__(self):
        return "Hello! My name is " + self.name + ". I have $" + str(self.wallet) + " in my payment card."


# The Cashier class
# The Cashier class represents a cashier at the market. 
class Cashier:

    # Constructor
    def __init__(self, name, directory =[]):
        self.name = name
        self.directory = directory # make a copy of the directory
        self.orders = 0

    # Whether the stall is in the cashier's directory
    def has_stall(self, stall):
        return stall in self.directory

    # Adds a stall to the directory of the cashier.
    def add_stall(self, new_stall):
        self.directory.append(new_stall)

    # Receives payment from customer, and adds the money to the stall's earnings.
    def receive_payment(self, stall, money):
        stall.earnings += money

    # Places an order at the stall.
	# The cashier pays the stall the cost.
	# The stall processes the order
	# Function returns cost of the order, using compute_cost method
    def place_order(self, stall, item, quantity):
        stall.process_order(item, quantity)
        return stall.compute_cost(quantity) 
    
    # string function.
    def __str__(self):
        return "Hello, this is the " + self.name + " cashier. We take preloaded market payment cards only. We have " + str(sum([len(category) for category in self.directory.values()])) + " vendors in the farmers' market."

## Complete the Stall class here following the instructions in HW_4_instructions_rubric
class Stall:
    def __init__(self, name, inventory, cost = 7, earnings = 0):
        self.name = name
        self.inventory = dict(inventory)
        self.cost = cost
        self.earnings = earnings
    
    def process_order(self, name, quantity):
        current_inv = self.inventory.get(name)
        if current_inv >= quantity:
            self.inventory[name] = current_inv - quantity 
        else:
            print("Order could not be processed.")

    def has_item(self, name, quantity):
        current_inv = self.inventory.get(name)
        if current_inv >= quantity:
            return True 
        else:
            return False

    def stock_up(self, name, quantity):
        current_inv = self.inventory.get(name)
        self.inventory[name] = current_inv + quantity

    def compute_cost(self, quantity):
        total_cost = self.cost * quantity
        return total_cost

    def __str__(self):
        current_items = list(self.inventory.keys)
        out = "Hello, we are " + self.name + ". This is our current menu " + current_items + ". We charge $" + str(self.cost) + " per item. We have " + str(self.earnings) + "in total."
        print(out)

class TestAllMethods(unittest.TestCase):
    
    def setUp(self):
        inventory = {"Burger":40, "Taco":50}
        self.f1 = Customer("Ted")
        self.f2 = Customer("Morgan", 150)
        self.s1 = Stall("The Grill Queen", inventory, cost = 10)
        self.s2 = Stall("Tamale Train", inventory, cost = 9)
        self.s3 = Stall("The Streatery", inventory)
        #the following codes show that the two cashiers have the same directory
        stall_list = [self.s1, self.s2, self.s3]
        self.c1 = Cashier("West", stall_list)
        self.c2 = Cashier("East", stall_list)

	## Check to see whether constructors work
    def test_customer_constructor(self):
        self.assertEqual(self.f1.name, "Ted")
        self.assertEqual(self.f2.name, "Morgan")
        self.assertEqual(self.f1.wallet, 100)
        self.assertEqual(self.f2.wallet, 150)

	## Check to see whether constructors work
    def test_cashier_constructor(self):
        self.assertEqual(self.c1.name, "West")
        #cashier holds the directory - within the directory there are three stalls
        self.assertEqual(len(self.c1.directory), 3) 

	## Check to see whether constructors work
    def test_stall_constructor(self):
        self.assertEqual(self.s1.name, "The Grill Queen")
        self.assertEqual(self.s1.inventory, {"Burger":40, "Taco":50})
        self.assertEqual(self.s3.earnings, 0)
        self.assertEqual(self.s2.cost, 9)

	# Check that the stall can stock up properly.
    def test_stocking(self):
        inventory = {"Burger": 10}
        s4 = Stall("Misc Stall", inventory)

		# Testing whether stall can stock up on items
        self.assertEqual(s4.inventory, {"Burger": 10})
        s4.stock_up("Burger", 30)
        self.assertEqual(s4.inventory, {"Burger": 40})
        
    def test_make_payment(self):
		# Check to see how much money there is prior to a payment
        previous_custormer_wallet = self.f2.wallet
        previous_earnings_stall = self.s2.earnings
        
        self.f2.submit_order(self.c1, self.s2, 30)

		# See if money has changed hands
        self.assertEqual(self.f2.wallet, previous_custormer_wallet - 30)
        self.assertEqual(self.s2.earnings, previous_earnings_stall + 30)


	# Check to see that the server can serve from the different stalls
    def test_adding_and_serving_stall(self):
        c3 = Cashier("North", directory = [self.s1, self.s2])
        self.assertTrue(c3.has_stall(self.s1))
        self.assertFalse(c3.has_stall(self.s3)) 
        c3.add_stall(self.s3)
        self.assertTrue(c3.has_stall(self.s3))
        self.assertEqual(len(c3.directory), 3)


	# Test that computed cost works properly.
    def test_compute_cost(self):
        #what's wrong with the following statements?
        #can you correct them?
        self.assertEqual(self.s1.compute_cost(5), 50)
        self.assertEqual(self.s3.compute_cost(6), 42)

	# Check that the stall can properly see when it is empty
    def test_has_item(self):
        # Set up to run test cases

        # Test to see if has_item returns True when a stall has enough items left
        # Please follow the instructions below to create three different kinds of test cases 
        # Test case 1: the stall does not have this food item: 
        self.assertFalse(self.s1.has_item("Steak", 1))
        
        # Test case 2: the stall does not have enough food item: 
        self.assertFalse(self.s1.has_item("Burger", 80))

        # Test case 3: the stall has the food item of the certain quantity: 
        self.assertTrue(self.s1.has_item("Burger", 40))

        pass

	# Test validate order
    def test_validate_order(self):
		# case 1: test if a customer doesn't have enough money in their wallet to order
        self.assertFalse(self.f1.validate_order(self.c1, self.s1, "Burger", 11))
		# case 2: test if the stall doesn't have enough food left in stock
        self.f1.reload_money(400)
        self.assertFalse(self.f1.validate_order(self.c1, self.s1, "Burger", 50))
		# case 3: check if the cashier can order item from an unknown stall
        new_stall = Stall("Just Ketchup", {"Ketchup" : 10000}, 1)
        self.assertFalse(self.f1.validate_order(self.c1, new_stall, "Ketchup", 1))
        # personal case: test success
        self.assertTrue(self.f1.validate_order(self.c1, self.s1, "Burger", 40))
        pass

    # Test if a customer can add money to their wallet
    def test_reload_money(self):
        self.assertEqual(self.f1.wallet, 100)
        self.f1.reload_money(50)
        self.assertEqual(self.f1.wallet, 150)
        pass
    
### Write main function
def main():
    #Create different objects 

    inv_dict1 = {"Potato" : 40, "Beet" : 20, "Cabbage" : 30}
    inv_dict2 = {"Pork" : 12, "Beef" : 43, "Chicken" : 30}
    inv_dict3 = {"Soda" : 200, "Beer" : 150, "Liquor" : 100}
    inv_dict4 = {"Toy" : 50, "Game" : 100}

    stall1 = Stall("Veggies", inv_dict1, 4)
    stall2 = Stall("Meats", inv_dict2, 8)
    stall3 = Stall("Drinks", inv_dict3, 3)
    stall4 = Stall("Fun Stuff", inv_dict4, 12)

    food_list = (stall1, stall2, stall3)
    nonfood_list = []
    nonfood_list.append(stall4)

    cashier1 = Cashier("Food", food_list)
    cashier2 = Cashier("Nonfood", nonfood_list)

    cust1 = Customer("Cameron", 250)
    cust2 = Customer("Sabine", 300)
    cust3 = Customer("Steve", 50)

    #Try all cases in the validate_order function
    #Below you need to have *each customer instance* try the four cases

    cust_list = (cust1, cust2, cust3)

    for cust in cust_list:
         #case 1: the cashier does not have the stall 
         cust.validate_order(cashier1, "Garden Supplies", "Shovel", 1)
         #case 2: the casher has the stall, but not enough ordered food or the ordered food item
         cust.validate_order(cashier1, stall1, "Rutabega", 10)
         #case 3: the customer does not have enough money to pay for the order: 
         cust.validate_order(cashier2, stall4, "Game", 40)
         #case 4: the customer successfully places an order
         cust.validate_order(cashier1, stall2, "Beef", 5)

    pass

if __name__ == "__main__":
	main()
	print("\n")
	unittest.main(verbosity = 2)
