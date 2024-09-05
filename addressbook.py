'''


    @Author: Shivraj Yelave
    @Date: 05-09-24
    @Last modified by: Shivraj Yelave
    @Last modified time: 05-09-24
    @Title: Address Book Program


'''

# Import required modules/files
import re
from logger import get_info_logger

# Regex patterns for validation
EMAIL_REGEX = r'^[\w]+([._%+-][\w]+)*@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(\.[a-zA-Z]{2,})?$'
PHONE_REGEX = r'^\d{10}$'
ZIP_REGEX = r'^\d{6}$'

# Setup logger
logger = get_info_logger('AddressBook')

class Contact:
    def __init__(self, first_name, last_name, address, city, state, zip_code, phone_number, email):
        
        """
        
        Description:
        Initializes a Contact instance with the given details.
        
        Parameters:
        first_name (str): First name of the contact.
        last_name (str): Last name of the contact.
        address (str): Address of the contact.
        city (str): City of the contact.
        state (str): State of the contact.
        zip_code (str): Zip code of the contact.
        phone_number (str): Phone number of the contact.
        email (str): Email address of the contact.
        
        """
        
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone_number = phone_number
        self.email = email

    def __str__(self):
        return (f"{self.first_name} {self.last_name}, {self.address}, {self.city}, "
                f"{self.state}, {self.zip_code}, {self.phone_number}, {self.email}")

class AddressBook:
    def __init__(self):
        # Initialize the address book with a single contact (default to None)
        self.contact = None

    def add_contact(self, contact):
        
        """
        
        Description:
        Adds a Contact instance to the address book and logs the addition.
        
        Parameters:
        contact (Contact): The Contact instance to add.
        
        """
        
        self.contact = contact
        logger.info(f"Contact added: {contact.__dict__}")

    def edit_contact(self, field, new_value):
        
        """
        
        Description:
        Edits the contact's details.
        
        Parameters:
        field (str): The field to edit ('first_name', 'last_name', 'address', 'city', 'state', 'zip_code', 'phone_number', 'email').
        new_value (str): The new value for the specified field.
        
        """
        
        if self.contact:
            if field == 'first_name':
                self.contact.first_name = new_value
            elif field == 'last_name':
                self.contact.last_name = new_value
            elif field == 'address':
                self.contact.address = new_value
            elif field == 'city':
                self.contact.city = new_value
            elif field == 'state':
                self.contact.state = new_value
            elif field == 'zip_code':
                self.contact.zip_code = new_value
            elif field == 'phone_number':
                self.contact.phone_number = new_value
            elif field == 'email':
                self.contact.email = new_value
            else:
                logger.error(f"Invalid field: {field}")
                return
            logger.info(f"Contact updated: {self.contact.__dict__}")
        else:
            logger.error("No contact found to edit.")
    def display_contact(self):
        """
        
        Description:
        Display Contact.
        
        Parameters:
        None.
        
        """
        if self.contact:
                logger.info(f"Contact: {self.contact.__dict__}")
                print(f"Contact: {self.contact.__dict__}")
        else:
            print("No contacts to display.")


def get_valid_input(prompt, validation_func):
    
    """
    
    Description:
    Prompts the user for input until the input is valid according to the validation function.

    Parameters:
    prompt (str): The prompt message to display to the user.
    validation_func (function): The function used to validate the input.

    Returns:
    str: Validated user input.
    
    """
    
    while True:
        user_input = input(prompt)
        if validation_func(user_input):
            return user_input
        else:
            logger.error(f"Invalid input: {user_input}")
            print("Invalid input. Please try again.")

def is_valid_email(email):
    
    """
    
    Description:
    Validate the email address using regex.

    Parameters:
    email (str): The email address to validate.

    Returns:
    bool: True if the email is valid, False otherwise.
    
    """
    
    return re.match(EMAIL_REGEX, email) is not None

def is_valid_phone(phone):
    
    """
    
    Description:
    Validate the phone number using regex.

    Parameters:
    phone (str): The phone number to validate.

    Returns:
    bool: True if the phone number is valid, False otherwise.
    
    """
    return re.match(PHONE_REGEX, phone) is not None

def is_valid_zip(zip_code):
    
    """
    
    Description:
    Validate the zip code using regex.

    Parameters:
    zip_code (str): The zip code to validate.

    Returns:
    bool: True if the zip code is valid, False otherwise.
    
    """
    return re.match(ZIP_REGEX, zip_code) is not None

def main():
    print(f"{'*'*10}Welcome to Address Book Program{'*'*10}")

    address_book = AddressBook()

    while True:
        print("\n1. Add New Contact")
        print("2. Display Contact")
        print("3. Edit Contact")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            # Get user inputs and validate
            first_name = get_valid_input("Enter first name: ", lambda x: len(x) > 0)
            last_name = get_valid_input("Enter last name: ", lambda x: len(x) > 0)
            address = get_valid_input("Enter address: ", lambda x: len(x) > 0)
            city = get_valid_input("Enter city: ", lambda x: len(x) > 0)
            state = get_valid_input("Enter state: ", lambda x: len(x) > 0)
            zip_code = get_valid_input("Enter zip code: ", is_valid_zip)
            phone_number = get_valid_input("Enter phone number: ", is_valid_phone)
            email = get_valid_input("Enter email address: ", is_valid_email)

            # Create and add contact
            contact = Contact(first_name, last_name, address, city, state, zip_code, phone_number, email)
            address_book.add_contact(contact)
            print("\nNew Contact Added Successfully!")


        elif choice == '2':
            address_book.display_contact()
        elif choice == '3':
            print("\nEnter 1 to edit First Name.\nEnter 2 to edit Last name.\nEnter 3 to edit Address.\nEnter 4 to edit City.\nEnter 5 to edit State.\nEnter 6 to edit Zip Code.\nEnter 7 to edit Phone Number.\nEnter 8 to edit Email.")
            edit_choice = input("Enter your choice: ")

            if edit_choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
                fields = ['first_name', 'last_name', 'address', 'city', 'state', 'zip_code', 'phone_number', 'email']
                field = fields[int(edit_choice) - 1]
                new_value = get_valid_input(f"Enter new value for {field}: ", lambda x: len(x) > 0)
                address_book.edit_contact(field, new_value)
                print("\nContact Edited Successfully!")

            else:
                print("Invalid choice. Please try again.")
        elif choice == '4':
            # Exit the program
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
