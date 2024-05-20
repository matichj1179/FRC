# import libraries
import pandas
import math


# *** Functions go here ***

# checks that input is either a float or an
# integer that is more than zero. Takes in custom error message
def num_check(question, error, num_type):
    while True:

        try:
            response = num_type(input(question))

            if response <= 0:
                print(error)
            else:
                return response

        except ValueError:
            print(error)


# checks that user has entered yes/ no to a question
def yes_no(question):
    to_check = ["yes", "no"]

    while True:

        response = input(question).lower()

        for var_item in to_check:
            if response == var_item:
                return response
            elif response == var_item[0]:
                return var_item

        print("please enter enter either yes or no....\n")


def not_blank(question, error):
    while True:
        response = input(question)

        if response == "":
            print(f"{error}. \nPlease try again. \n")
            continue

        return response


# currency formatting functionS
def currency(x):
    return f"${x:.2f}"


def get_expenses(var_fixed):
    # set up dictionaries

    item_list = []
    quantity_list = []
    price_list = []

    variable_dict = {
        "Item": item_list,
        "Quantity": quantity_list,
        "Price": price_list
    }
    # loop to get component, quantity and price
    item_name = ""
    while item_name.lower() != "xxx":

        print()
        # get name, quantity and item
        item_name = not_blank("item name: ",
                              "The product name can't be blank.")
        if item_name.lower() == "xxx":
            break

        if var_fixed == "variable":

            quantity = num_check("Quantity:",
                                 "The amount must be a whole number "
                                 "more than zero",
                                 int)
        else:
            quantity = 1

        price = num_check("How much for a single item? $",
                          "The price must be a number <more "
                          "than 0>",
                          float)

        # add item, quantity and price to lists
        item_list.append(item_name)
        quantity_list.append(quantity)
        price_list.append(price)

    expense_frame = pandas.DataFrame(variable_dict)
    expense_frame = expense_frame.set_index('Item')

    # Calculate cost of each component
    expense_frame['Cost'] = expense_frame['Quantity'] \
                            * expense_frame['Price']

    # Find sub total
    sub_total = expense_frame['Cost'].sum()

    # currency Formatting (uses currency function)
    add_dollars = ['Price', 'Cost']
    for item in add_dollars:
        expense_frame[item] = expense_frame[item].apply(currency)

    return [expense_frame, sub_total]


# Prints expense frame
def expense_print(heading, frame, subtotal):
    print()
    print(f"**** {heading} ****")
    print(frame)
    print()
    print(f"{heading} Costs: ${subtotal:.2f}")
    return ""


def profit_goal(total_costs):
    # Initialise variables and error message
    error = "Please enter a valid profit goal\n"

    while True:

        # ask for profit goal
        response = input("What is your profit goal (eg $500 or 50%)")

        # check if first character is $
        if response[0] == "$":
            profit_type = "$"
            # Get amount (everything after the $)

            amount = response[1:]

        # check if last character is %
        elif response[-1] == "%":
            profit_type = "%"
            # get amount (everything before the %)
            amount = response[:-1]

        else:
            # set response to amount for now
            profit_type = "unknown"
            amount = response

        try:
            # check amount is a number more than zero
            amount = float(amount)
            if amount <= 0:
                print(error)
                continue

        except ValueError:
            print(error)
            continue

        if profit_type == "unknown" and amount >= 100:
            dollar_type = yes_no(f"Do you mean ${amount:.2f}. ie {amount:.2f} dollars?, y/n")

            # set profit type based on user answer above
            if dollar_type == "yes":
                profit_type = "$"
            else:
                profit_type = "%"

        elif profit_type == "unknown" and amount < 100:
            percent_type = yes_no(f"Do you mean {amount}%?, y / n")
            if percent_type == "yes":
                profit_type = "%"
            else:
                profit_type = "$"

            # return profit goal to main routine
            if profit_type == "$":
                return amount
            else:
                goal = (amount / 100) * total_costs
                return goal


def round_up(amount, var_round_to):
    return int(math.ceil(amount / var_round_to)) * var_round_to


# **** Main Routine goes here ****

# Get product name

product_name = not_blank("Product name: ", "")

how_many = num_check("How many items will you be producing? ",
                     "The number of items must be a whole number more than zero", int)

print("Please enter your costs below...")
variable_expenses = get_expenses("variable")
variable_frame = variable_expenses[0]
variable_sub = variable_expenses[1]

print()
have_fixed = yes_no("Do you have costs (y /n)? ")

if have_fixed == "yes":
    # get fixed costs
    fixed_expenses = get_expenses("fixed")
    fixed_frame = fixed_expenses[0]
    fixed_sub = fixed_expenses[1]
else:
    fixed_frame = ""
    fixed_sub = 0

# work out total costs and profit target
all_costs = variable_sub + fixed_sub
profit_target = profit_goal(all_costs)

# Calculate total sales needed to reach goal
sales_needed = all_costs + profit_target

# Ask user for rounding
round_to = num_check("round to nearest...? $",
                     "cant be 0", int)

# calculate recommended price
selling_price = sales_needed / how_many
print(f"Selling Price (unrounded): ${selling_price:.2f}")

recommended_price = round_up(selling_price, round_to)



# *** Printing Area ***

print()
print(f"**** Fund Raising - {product_name} ****")
print()
expense_print("Variable", variable_frame, variable_sub)

if have_fixed == "yes":
    expense_print("Fixed", fixed_frame[['Cost']], fixed_sub)

print()
print(f"**** Total costs: ${all_costs:.2f} ****")
print()

print()
print("**** Profit & Sales Targets ****")
print(f"Profit Target: ${profit_target:.2f}")
print(f"Total Sales: ${all_costs + profit_target:.2f}")

print()
print("**** Pricing ****")
print(f"Minimum Price: ${selling_price:.2f}")
print(f"**** Recommended Selling Price:"
      f" ${recommended_price:.2f}")
