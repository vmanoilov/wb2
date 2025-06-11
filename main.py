# EcoDispose - A Practical Tool for E-Waste Compliance
# This script is a command-line implementation of the EcoDispose prototype.

import time
import os
from datetime import date

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen for a cleaner interface."""
    # Works for Mac/Linux (os.name == 'posix') and Windows (os.name == 'nt')
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Prints a consistent header for each section."""
    print("==================================================")
    print(f"       EcoDispose - {title}")
    print("==================================================")
    print() # Add a little space

def ask_question(prompt, options):
    """
    A reusable function to ask a multiple-choice question and get valid input.
    This function demonstrates loops and conditional statements.
    """
    print(f"-> {prompt}")
    # Display options in a more readable format if the list is long
    if len(options) > 10:
        # Display in columns for better readability
        col_width = max(len(option) for option in options) + 4
        num_cols = 3
        cols = [options[i::num_cols] for i in range(num_cols)]
        max_rows = max(len(col) for col in cols)
        for i in range(max_rows):
            row_str = ""
            for col in cols:
                if i < len(col):
                    row_str += f"{i * num_cols + (cols.index(col) + 1):>2}) {col[i]:<{col_width}}"
            print(row_str)
    else:
        for i, option in enumerate(options, 1):
            print(f"   {i}) {option}")

    while True: # This is a 'while' loop to keep asking until we get a valid answer.
        try:
            choice = int(input("\n   Your choice: "))
            if 1 <= choice <= len(options): # This is an 'if' statement to check the input.
                return options[choice - 1] # Return the chosen text
            else:
                print("   ! That's not a valid option, please try again.")
        except ValueError:
            print("   ! Please enter a number.")

# --- Wizard & Results Functions ---

def run_personal_wizard():
    """Guides the user through the personal disposal questions."""
    clear_screen()
    print_header("Personal Disposal Guidance")

    # This dictionary will store the user's answers. It's a variable.
    selections = {}

    # List of London Councils for tailored advice
    london_councils = [
        "Barking and Dagenham", "Barnet", "Bexley", "Brent", "Bromley", "Camden",
        "City of London", "Croydon", "Ealing", "Enfield", "Greenwich", "Hackney",
        "Hammersmith and Fulham", "Haringey", "Harrow", "Havering", "Hillingdon",
        "Hounslow", "Islington", "Kensington and Chelsea", "Kingston upon Thames",
        "Lambeth", "Lewisham", "Merton", "Newham", "Redbridge", "Richmond upon Thames",
        "Southwark", "Sutton", "Tower Hamlets", "Waltham Forest", "Wandsworth", "Westminster"
    ]

    selections['location'] = ask_question(
        "To give you tailored advice, please select your London council:",
        london_councils
    )
    print("\n" + "-" * 50 + "\n")


    selections['item_type'] = ask_question(
        "What type of item do you want to dispose of?",
        ["Computer/Laptop", "Phone/Tablet", "TV/Monitor", "Small Appliance", "Batteries", "Other"]
    )
    print("\n" + "-" * 50 + "\n")

    selections['condition'] = ask_question(
        "What is the item's condition?",
        ["Working / Repairable", "Broken / Not Working"]
    )
    print("\n" + "-" * 50 + "\n")

    selections['data'] = ask_question(
        "Does the item contain personal or sensitive data?",
        ["Yes, and I need to wipe it", "Yes, but it has been wiped", "No / Not applicable"]
    )
    print("-" * 50)

    display_personal_results(selections)


def run_business_wizard():
    """Guides the user through the business disposal questions."""
    clear_screen()
    print_header("Business Compliance Reporting")

    selections = {}

    selections['item_type'] = ask_question(
        "What type of item are you disposing of?",
        ["Computer/Laptop", "Phone/Tablet", "Server", "Printer/Scanner", "Office Phone System"]
    )
    print("\n" + "-" * 50 + "\n")

    selections['condition'] = ask_question(
        "What is the item's condition?",
        ["Working / Refurbishable", "End of Life / For Recycling"]
    )
    print("\n" + "-" * 50 + "\n")

    selections['data'] = ask_question(
        "What is the status of the data on the device(s)?",
        ["Data has been securely erased", "Data erasure is still required", "No sensitive data on device"]
    )
    print("\n" + "-" * 50 + "\n")

    # Getting quantity for the business report
    while True:
        try:
            quantity = int(input("-> How many of these items are you disposing of?: "))
            if quantity > 0:
                selections['quantity'] = quantity
                break
            else:
                print("   ! Please enter a number greater than zero.")
        except ValueError:
            print("   ! Please enter a valid number.")

    print("-" * 50)
    display_business_report(selections)


def display_personal_results(selections):
    """Displays the final guidance for a personal user."""
    clear_screen()

    # Check for specific conditions to suggest donation
    is_donatable = selections['item_type'] in ["Computer/Laptop", "Phone/Tablet"]
    is_working = selections['condition'] == "Working / Repairable"

    if is_donatable and is_working:
        print_header("Donation Recommendation")
        print("RECOMMENDED ACTION: DONATE FOR REUSE\n")
        print("Since your device is in working order, the most sustainable option is to donate it.")
        print("This extends its life and helps someone in your community.\n")
        print("Consider donating to a local UK charity that tackles digital exclusion.")
        print("Search online for 'local computer donation' or check with community libraries.\n")

        # A conditional message based on their answer about data.
        if "Yes" in selections['data']:
            print("DATA SECURITY REMINDER:")
            print("Before donating, please ensure all your personal data is securely erased.\n")
    else:
        # Display the standard recycling guidance
        print_header("Your Disposal Guidance")
        print("RECOMMENDED ACTION:")
        print("Based on your answers, this item should be taken to a certified WEEE recycling facility.")
        print("Please do not place it in your household bin.\n")

        if "Yes" in selections['data']:
            print("DATA SECURITY REMINDER:")
            print("Please ensure all personal data is securely erased before disposal.\n")

        print("RESOURCE LOCATOR:")
        print(f"For tailored advice in {selections['location']}, search for your nearest Household Waste Recycling Centre (HWRC) on your council's website.")
        print("Look for the 'WEEE' or 'Small Electricals' section for specific local instructions.")


def display_business_report(selections):
    """Displays a simulated compliance certificate or donation advice for a business user."""
    clear_screen()

    # Check for the specific conditions to suggest donation
    is_donatable_item = selections['item_type'] == "Computer/Laptop"
    is_working = selections['condition'] == "Working / Refurbishable"

    if is_donatable_item and is_working:
        print_header("Donation Recommendation")
        print("RECOMMENDED ACTION: DONATE FOR REUSE\n")
        print("Since the equipment is in working order, the most sustainable and socially")
        print("responsible option is to donate it to a charity tackling digital exclusion.\n")

        # Add a specific data wipe warning if needed
        if selections['data'] == "Data erasure is still required":
            print("!! IMPORTANT DATA SECURITY NOTICE !!")
            print("You MUST ensure all sensitive company data is securely and professionally")
            print("erased from all devices before they are donated.\n")

        print("This extends the life of the hardware and helps bridge the digital divide.")
        print("Consider donating to a local UK charity.\n")
        print("SUGGESTED CHARITIES:")
        print("- The Turing Trust")
        print("- Get Well Gamers")
        print("- Local community centres or schools in your area\n")
        print("A WEEE-compliant disposal certificate can still be provided by the charity")
        print("or a registered IT Asset Disposition (ITAD) company upon request.")

    else:
        # Display the standard compliance report
        print_header("Compliance Report Ready")
        print("------------------------------------------")
        print("      CERTIFICATE OF DISPOSAL (DRAFT)")
        print("------------------------------------------")
        print(f"  Company:          GreenTech Solutions Client")
        print(f"  Date:             {date.today().strftime('%d/%m/%Y')}")
        print(f"  Item Type:        {selections['item_type']}")
        print(f"  Quantity:         {selections['quantity']}")
        print(f"  Condition:        {selections['condition']}")
        print(f"  Data Protocol:    {selections['data']}")
        print(f"  Disposal Method:  Secure WEEE Recycling")
        print("------------------------------------------")
        print("\nThis document certifies that the items listed have been processed")
        print("for disposal in accordance with the WEEE Directive.")
        print("\nNOTE: This is a draft. A final PDF would be generated in a full application.")


# --- Main Application Logic ---

def main():
    """The main function that runs the application loop."""
    while True:
        clear_screen()
        print_header("Main Menu")

        # This is our top-level function call
        path = ask_question(
            "How are you disposing of electronics today?",
            ["Personal Use", "Business Use", "Exit Program"]
        )

        if path == "Personal Use":
            run_personal_wizard()
        elif path == "Business Use":
            run_business_wizard()
        elif path == "Exit Program":
            print("\nThank you for using EcoDispose. Exiting now.")
            break # Exit the 'while' loop

        print("\n" + "="*50)
        input("Press Enter to return to the Main Menu...")

# This is a standard Python practice to make the script runnable.
if __name__ == "__main__":
    main()
