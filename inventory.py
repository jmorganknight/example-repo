
# Libraries to be imported
import os
import csv
from tabulate import tabulate


#========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = float(cost)
        self.quantity = int(quantity)
        
    def get_cost(self):
        '''
        Add the code to return the cost of the shoe in this method.

        Note: this is not necessary as a function provided below does the same.
        '''
        return self.cost
        

    def get_quantity(self):
        '''
        Add the code to return the quantity of the shoes.

        Note: this is not necessary as a function provided below does the same.
        '''
        return self.quantity
            
    def __str__(self):
        '''
        Add a code to returns a string representation of a class.
        '''
        return f"Shoe: {self.product} (Code: {self.code}), Country: {self.country}, Cost: ${self.cost}, Quantity: {self.quantity}"       



#=============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''

filename = "inventory.txt" 


#==========Functions outside the class==============
def read_shoes_data():
    '''
    Reads the shoes data from the inventory.txt file
    and returns a list of Shoe objects.
    '''
    shoe_list = []
    with open(("./" + filename), "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            shoe = Shoe(
                row["Country"],
                row["Code"],
                row["Product"],
                row["Cost"],
                row["Quantity"]
            )
            shoe_list.append(shoe)

    return shoe_list


def capture_shoes(shoe_list):
    '''
    This function will allow a user to capture data
    about a shoe and use this data to create a shoe object
    and append this object inside the shoe list.
    '''
    country = input("Enter Country: ")
    code = input("Enter Code: ")
    product = input("Enter Product: ")
    
    while True:
        try:
            cost = float(input("Enter shoe cost: "))
            break
        except ValueError:
            print("Please enter a valid number for cost.")

    while True:
        try:
            quantity = int(input("Enter shoe quantity: "))
            break
        except ValueError:
            print("Please enter a valid integer for quantity.")
    
    new_shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(new_shoe)


def view_all():
    '''
    This function will iterate over the shoes list and
    print the details of the shoes returned from the __str__
    function. Optional: you can organise your data in a table format
    by using Python’s tabulate module.
    '''
    table_of_shoes = [[shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity] for shoe in shoe_list]
    headers = ["Country", "Code", "Product", "Cost", "Quantity"]

    print(tabulate(table_of_shoes, headers, tablefmt="grid"))


    

def re_stock(shoe_list):
    '''
    This function will find the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked. Ask the user if they
    want to add this quantity of shoes and then update it.
    This quantity should be updated on the file for this shoe.
    '''
    if not shoe_list:
        print("No shoes available.")
        return

    # find minimum quantity and all shoes with that quantity
    min_qty = min(shoe_list, key=lambda s: s.quantity).quantity
    tied = [s for s in shoe_list if s.quantity == min_qty]

    print(f"\nLowest quantity = {min_qty}. Found {len(tied)} item(s) with that quantity.\n")

    # show tied items with indices
    table = [[idx + 1, s.country, s.code, s.product, s.cost, s.quantity] for idx, s in enumerate(tied)]
    headers = ["#","Country", "Code", "Product", "Cost", "Quantity"]
    print(tabulate(table, headers, tablefmt="grid"))

    # prompt user for action
    prompt = ("Enter item number to restock that shoe, "
              "'A' to restock ALL listed items, or 'Q' to cancel: ")

    while True:
        choice = input(prompt).strip()
        if not choice:
            continue

        if choice.lower() == 'q':
            print("Restock cancelled.")
            return

        if choice.lower() == 'a':
            # restock all tied items
            while True:
                amount_in = input("Enter quantity to add to EACH tied item (or 'q' to cancel): ").strip()
                if amount_in.lower() == 'q':
                    print("Restock cancelled.")
                    return
                try:
                    add_amount = int(amount_in)
                    if add_amount < 0:
                        print("Please enter a non-negative integer.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid integer or 'q' to cancel.")
            for s in tied:
                s.quantity += add_amount
            print(f"Added {add_amount} to each of the {len(tied)} item(s).")
            break

        # try to parse numeric selection
        try:
            idx = int(choice) - 1
            if idx < 0 or idx >= len(tied):
                print("Selection out of range; try again.")
                continue
        except ValueError:
            print("Invalid input; enter number, 'A' or 'Q'.")
            continue

        # ask how many to add for the chosen item
        target = tied[idx]
        while True:
            amount_in = input(f"Enter how many new '{target.product}' ({target.code}) were received (or 'q' to cancel): ").strip()
            if amount_in.lower() == 'q':
                print("Restock cancelled.")
                return
            try:
                add_amount = int(amount_in)
                if add_amount < 0:
                    print("Please enter a non-negative integer.")
                    continue
                break
            except ValueError:
                print("Please enter a valid integer or 'q' to cancel.")

        target.quantity += add_amount
        print(f"Updated {target.product} ({target.code}) quantity -> {target.quantity}")
        break

    # write updated inventory back to file (use script dir to be safe)
    try:
        filepath = os.path.join(os.path.dirname(__file__), filename)
    except NameError:
        # fallback if __file__ not available (e.g., interactive REPL)
        filepath = filename

    with open(filepath, "w", newline="") as f:
        f.write("Country,Code,Product,Cost,Quantity\n")
        for s in shoe_list:
            f.write(f"{s.country},{s.code},{s.product},{s.cost},{s.quantity}\n")

    print("\nStock successfully updated in inventory.txt")

def search_shoe(search_code):
    '''
    This function will search for a shoe from the list
    using the shoe code and return this object so that it will be printed.
    '''

    for shoe in shoe_list:
        if shoe.code == search_code:
            return shoe
    return None
    

def value_per_item(search_code):
    '''
    This function will calculate the total value for each item.
    Please keep the formula for value in mind: value = cost * quantity.
    Print this information on the console for all the shoes.
    '''
    for shoe in shoe_list:
        if shoe.code == search_code:
            value = shoe.cost * shoe.quantity
            table = [[shoe.code, shoe.product, shoe.cost, shoe.quantity, value]]
            headers = ["Code", "Product", "Cost", "Quantity", "Value"]
            print(tabulate(table, headers, tablefmt="grid"))
            return
    print("Error: Code not found.")
        

def highest_qty():
    '''
    Write code to determine the product with the highest quantity and
    print this shoe as being for sale.
    '''
    
    # Find the shoe with the largest quantity
    max_qty = max(shoe_list, key=lambda shoe: int(shoe.quantity)).quantity

    # Collect all shoes with that same max quantity
    highest_shoes = [s for s in shoe_list if int(s.quantity) == int(max_qty)]

    print(f"\nHighest quantity = {max_qty}. Items on sale:\n")

    for shoe in highest_shoes:
        print(shoe)


#==========Main Menu=============

# Populate the shoe_list at the start
shoe_list = read_shoes_data()

'''
Create a menu that executes each function above.
This menu should be inside the while loop. Be creative!
'''
def main_menu():
    while True:
        print("""
╔══════════════════════════════════════╗
║           INVENTORY SYSTEM           ║
╠══════════════════════════════════════╣
║  1. Current inventory                ║
║  2. Add a new shoes                  ║
║  3. Restock                          ║
║  4. Search                           ║
║  5. Lookup value                     ║
║  6. On sale shoes                    ║
║  7. Exit                             ║
╚══════════════════════════════════════╝
""")

        choice = input("Enter selection: ")

        if choice == '1':
            view_all() 
        elif choice == '2':
            capture_shoes(shoe_list)
        elif choice == '3':
            re_stock(shoe_list)
        elif choice == '4':
            code = input("Enter shoe code to search: ")
            shoe = search_shoe(code)
            if shoe:
                print(shoe)
            else:
                print("Shoe code not found.")
        elif choice == '5':
            code = input("Enter shoe code to search: ")
            value_per_item(code)   
        elif choice == '6':
            highest_qty()
        elif choice == '7':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Start the program
main_menu()
        