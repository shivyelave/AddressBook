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
        # Initialize the address book with a list to store multiple contacts
        self.contacts = []

    def add_contact(self, contact):
        
        """
        
        Description:
        Adds a Contact instance to the address book and logs the addition.
        
        Parameters:
        contact (Contact): The Contact instance to add.
        
        """
        self.contacts.append(contact)
        logger.info(f"Contact added: {contact.__dict__}")

    def edit_contact(self, name, field, new_value):
        
        """
        
        Description:
        Edits a contact's details identified by the name.
        
        Parameters:
        name (str): The name of the contact to edit.
        field (str): The field to edit ('first_name', 'last_name', 'address', 'city', 'state', 'zip_code', 'phone_number', 'email').
        new_value (str): The new value for the specified field.
        
        """
        
        for contact in self.contacts:
            if (contact.first_name + " " + contact.last_name) == name:
                if field == 'first_name':
                    contact.first_name = new_value
                elif field == 'last_name':
                    contact.last_name = new_value
                elif field == 'address':
                    contact.address = new_value
                elif field == 'city':
                    contact.city = new_value
                elif field == 'state':
                    contact.state = new_value
                elif field == 'zip_code':
                    contact.zip_code = new_value
                elif field == 'phone_number':
                    contact.phone_number = new_value
                elif field == 'email':
                    contact.email = new_value
                else:
                    logger.error(f"Invalid field: {field}")
                    return
                logger.info(f"Contact updated: {contact.__dict__}")
                return
        logger.error(f"No contact found with the name: {name}")
        print("No contact found with the provided name.")

    def delete_contact(self, name):
        
        """
        
        Description:
        Deletes a contact identified by the name.
        
        Parameters:
        name (str): The name of the contact to delete.
        
        """
        
        for i, contact in enumerate(self.contacts):
            if (contact.first_name + " " + contact.last_name) == name:
                logger.info(f"Deleting contact: {contact.__dict__}")
                del self.contacts[i]
                print("Contact deleted successfully!")
                return
        logger.error(f"No contact found with the name: {name}")
        print("No contact found with the provided name.")

    def display_contacts(self):
        
        """
        
        Description:
        Displays all contacts in the address book.
        
        Parameters:
        None.
        
        """
        if self.contacts:
            for contact in self.contacts:
                logger.info(f"Contact: {contact.__dict__}")
                print(contact)
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
    print(f"{'*'*10}Welcome to Address Book System{'*'*10}")

    # Dictionary to hold multiple Address Books
    address_books = {}

    while True:
        print("\n1. Create New Address Book")
        print("2. Select Address Book")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            # Create a new Address Book
            book_name = get_valid_input("Enter the name for the new Address Book: ", lambda x: len(x) > 0)
            if book_name in address_books:
                print("An Address Book with this name already exists.")
            else:
                address_books[book_name] = AddressBook()
                print(f"Address Book '{book_name}' created successfully!")

        elif choice == '2':
            # Select an Address Book
            if not address_books:
                print("No Address Books available. Create one first.")
                continue

            book_name = input("Enter the name of the Address Book to select: ")
            if book_name not in address_books:
                print("Address Book not found.")
                continue

            address_book = address_books[book_name]

            while True:
                print(f"\nAddress Book '{book_name}'")
                print("1. Add New Contact")
                print("2. Display Contacts")
                print("3. Edit Contact")
                print("4. Delete Contact")
                print("5. Go Back")

                sub_choice = input("Enter your choice: ")

                if sub_choice == '1':
                    while True:
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

                        more_contacts = input("Do you want to add another contact? (yes/no): ").strip().lower()
                        if more_contacts != 'yes':
                            break

                elif sub_choice == '2':
                    address_book.display_contacts()

                elif sub_choice == '3':
                    print("\nEnter 1 to edit First Name.\nEnter 2 to edit Last name.\nEnter 3 to edit Address.\nEnter 4 to edit City.\nEnter 5 to edit State.\nEnter 6 to edit Zip Code.\nEnter 7 to edit Phone Number.\nEnter 8 to edit Email.")
                    edit_choice = input("Enter your choice: ")

                    if edit_choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
                        full_name = input("Enter the full name of the contact to edit: ")
                        fields = ['first_name', 'last_name', 'address', 'city', 'state', 'zip_code', 'phone_number', 'email']
                        field = fields[int(edit_choice) - 1]
                        new_value = get_valid_input(f"Enter new value for {field}: ", lambda x: len(x) > 0)
                        address_book.edit_contact(full_name, field, new_value)
                        print("\nContact Edited Successfully!")

                    else:
                        print("Invalid choice. Please try again.")

                elif sub_choice == '4':
                    full_name = input("Enter full name to delete contact: ")
                    address_book.delete_contact(full_name)

                elif sub_choice == '5':
                    break

                else:
                    print("Invalid choice. Please try again.")

        elif choice == '3':
            # Exit the program
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
