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


# Loops to make testing faster
for item in range(0, 6):
    want_help = yes_no("Do you want to read the instructions? ")
    print(f"You said '{want_help}'\n")
