'''


    @Author: Shivraj Yelave
    @Date: 05-09-24
    @Last modified by: Shivraj Yelave
    @Last modified time: 075-09-24
    @Title: Address Book Program


'''
import os
import json

# Import required modules/files
import re
from logger import get_info_logger

# Regex patterns for validation
EMAIL_REGEX = r'^[\w]+([._%+-][\w]+)*@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(\.[a-zA-Z]{2,})?$'
PHONE_REGEX = r'^\d{10}$'
ZIP_REGEX = r'^\d{6}$'

# Setup logger
logger = get_info_logger('AddressBookSystem')

class Contact:
    def __init__(self, address_book_name,first_name, last_name, address, city, state, zip_code, phone_number, email):
        self.address_book_name = address_book_name
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
        self.contacts = []
        self.file_name = "address_book.json"
        self.read_from_file()  # Read contacts from file when initializing the AddressBook
    
    def add_contact(self, contact):
        
        """
        Description:        
        Adds a new contact to the address book. Checks for duplicates and inserts the contact in alphabetical order.
        
        Parameters:
        contact (Contact): The contact to be added.
        
        """
        def get_full_name(c):
            return f"{c.first_name} {c.last_name}"

        # Check if contact already exists
        full_name = get_full_name(contact)
        if any(get_full_name(c) == full_name for c in self.contacts):
            print("A contact with this name already exists.")
            return
        
        # Find the correct position to insert the new contact
        inserted = False
        for i, existing_contact in enumerate(self.contacts):
            if get_full_name(existing_contact) > full_name:
                self.contacts.insert(i, contact)
                inserted = True
                break
        
        if not inserted:
            self.contacts.append(contact)
        
        # Log contact added
        logger.info(f"Contact added: {contact.__dict__}")
        
        # Write the contact to file
        self.write_to_file()
    
    def edit_contact(self, name, field, new_value):
        
        """
        Description:
        Edits an existing contact in the address book.
        
        Parameters:
        name (str): The full name of the contact to edit.
        field (str): The field of the contact to edit.
        new_value (str): The new value for the specified field.
        
        """
        
        for contact in self.contacts:
            if (contact.first_name + " " + contact.last_name) == name:
                if hasattr(contact, field):
                    setattr(contact, field, new_value)
                    logger.info(f"Contact updated: {contact.__dict__}")
                    self.write_to_file()  # Update file after editing contact
                    return
                else:
                    logger.error(f"Invalid field: {field}")
                    print("Invalid field.")
                    return
        logger.error(f"No contact found with the name: {name}")
        print("No contact found with the provided name.")
    
    def delete_contact(self, name):
        
        """
        Description:
        Deletes a contact from the address book.
        
        Parameters:
        name (str): The full name of the contact to delete.
        
        """
        
        for i, contact in enumerate(self.contacts):
            if (contact.first_name + " " + contact.last_name) == name:
                logger.info(f"Deleting contact: {contact.__dict__}")
                del self.contacts[i]
                print("Contact deleted successfully!")
                self.write_to_file()  # Update file after deleting contact
                return
        logger.error(f"No contact found with the name: {name}")
        print("No contact found with the provided name.")
    
    def display_contacts(self, sort_by=None):
        
        """
        Description:
        Displays all contacts in the address book, optionally sorted by a given attribute.
        
        Parameters:
        sort_by (str): The attribute to sort by (e.g., 'city', 'state', 'zip_code').
        
        """
        
        # Optionally sort by the given attribute
        if sort_by and sort_by in ['city', 'state', 'zip_code']:
            self.contacts.sort(key=lambda contact: getattr(contact, sort_by))
        elif sort_by:
            print(f"Invalid attribute '{sort_by}'. Showing contacts in original order.")
        
        # Display contacts
        if self.contacts:
            for contact in self.contacts:
                logger.info(f"Contact: {contact.__dict__}")
                print(contact.__dict__)
        else:
            print("No contacts to display.")
            
    def delete_address_book(self,address_book_name):
        
        """
        
        Description:
        Deletes a specific address book from the file where multiple address books are stored.
        
        Parameters:
        file_path (str): The path to the file storing multiple address books.
        address_book_name (str): The name of the address book to delete.
        
        """
        file_path = self.file_name
        if not os.path.exists(file_path):
            print(f"The file {file_path} does not exist.")
            return
        
        with open(file_path, 'r') as file:
            try:
                # Load the data from the file
                address_books = json.load(file)
            except json.JSONDecodeError:
                print("Error decoding JSON. The file may be corrupted.")
                return
        
        # Check if the address book exists
        if address_book_name in address_books:
            # Delete the address book
            del address_books[address_book_name]
            print(f"Address book '{address_book_name}' deleted successfully!")
            
            # Write the updated data back to the file
            with open(file_path, 'w') as file:
                json.dump(address_books, file, indent=4)
                logger.info(f"Deleted address book: {address_book_name}")
        else:
            print(f"No address book found with the name '{address_book_name}'.")

    
    def write_to_file(self):
        
        """
        
        Description:
        Writes all contacts to the file in JSON format.
        
        """
        try:
            # Organize contacts into a dictionary with address book names as keys
            address_book_dict = {}
            for contact in self.contacts:
                book_name = contact.address_book_name
                if book_name not in address_book_dict:
                    address_book_dict[book_name] = []
                contact_data = {
                    "first_name": contact.first_name,
                    "last_name": contact.last_name,
                    "address": contact.address,
                    "city": contact.city,
                    "state": contact.state,
                    "zip_code": contact.zip_code,
                    "phone_number": contact.phone_number,
                    "email": contact.email
                }
                address_book_dict[book_name].append(contact_data)

            with open(self.file_name, 'w') as file:
                json.dump(address_book_dict, file, indent=4)
            print(f"Contacts successfully written to {self.file_name}.")
        except Exception as e:
            print(f"An error occurred while writing to file: {e}")
    
    def read_from_file(self):
        
        """
        
        Description:
        Reads contacts from the file and loads them into the address book.
        
        """
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, 'r') as file:
                    address_book_dict = json.load(file)
                    self.contacts = []
                    for book_name, contacts_list in address_book_dict.items():
                        for contact_data in contacts_list:
                            contact = Contact(
                                address_book_name=book_name,
                                first_name=contact_data["first_name"],
                                last_name=contact_data["last_name"],
                                address=contact_data["address"],
                                city=contact_data["city"],
                                state=contact_data["state"],
                                zip_code=contact_data["zip_code"],
                                phone_number=contact_data["phone_number"],
                                email=contact_data["email"]
                            )
                            self.contacts.append(contact)
                print(f"Contacts successfully loaded from {self.file_name}.")
            except Exception as e:
                print(f"An error occurred while reading from file: {e}")
        else:
            print(f"{self.file_name} does not exist.")

    def display_all_address_books(self):
        """
        Description:
        Displays all address books along with their contacts.
        
        """
        # Check if file exists
        if not os.path.exists(self.file_name):
            print(f"The file {self.file_name} does not exist.")
            return
        
        with open(self.file_name, 'r') as file:
            try:
                # Load the data from the file
                address_books = json.load(file)
            except json.JSONDecodeError:
                print("Error decoding JSON. The file may be corrupted.")
                return
        
        # Check if there are any address books available
        if not address_books:
            print("No Address Books available.")
            return
        
        # Iterate over each address book and display its contacts
        for book_name, contacts in address_books.items():
            logger.info(f"Address book: {book_name}")
            print(f"\nAddress Book: {book_name}")
            
            if contacts:
                for contact in contacts:
                    # Log and display each contact
                    logger.info(f"Contact: {contact}")
                    print(f"Contact: {contact}")
            else:
                print("No contacts in this address book.")



def search_person_in_city(address_book, city):
    
    """
    
    Description:
    Searches for persons in a specific city within the provided address book and displays the result.
    
    Parameters:
    address_book (AddressBook): The AddressBook instance to search within.
    city (str): The city to search for persons in.
    
    """
    
    found_contacts = []
    
    # Iterate over the contacts in the address book
    for contact in address_book.contacts:
        if contact.city.lower() == city.lower():  # Match city case-insensitively
            found_contacts.append(contact)

    # Display the results
    if found_contacts:
        print(f"Found persons in city '{city}':")
        logger.info(f"Found persons in city '{city}':")

        for contact in found_contacts:
            print(contact.__dict__)
            logger.info(contact.__dict__)
    else:
        print(f"No persons found in city '{city}'.")
        logger.info(f"No persons found in city '{city}'.")


def persons_by_state(address_book, state):
    
    """
    
    Description:
    Creates a dictionary where the state is the key, and the values are the names of persons 
    (first and last name) from the specified state in the provided address book.
    
    Parameters:
    address_book (AddressBook): The AddressBook instance to search within.
    state (str): The state to search for persons in.

    Returns:
    dict: A dictionary with the state as the key and a list of person names as values.
    
    """
    state_persons_dict = {}

    # Iterate over the contacts in the address book
    for contact in address_book.contacts:
        if contact.state.lower() == state.lower():  # Match state case-insensitively
            full_name = contact.first_name + " " + contact.last_name
            if state not in state_persons_dict:
                state_persons_dict[state] = [full_name]
            else:
                state_persons_dict[state].append(full_name)
    
    return state_persons_dict



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
    print(f"{'*'*10} Welcome to Address Book System {'*'*10}")

    # Dictionary to hold multiple Address Books
    address_books = {}

    while True:
        print("\n1. Create New Address Book")
        print("2. Select Address Book")
        print("3. Display Address Book")
        print("4. Search contact by city in Address Book")
        print("5. Get Persons by State in Address Book")
        print("6. Delete Address Book")
        print("7. Exit")

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

                        # Check for duplicate contact
                        full_name = f"{first_name} {last_name}"
                        if any(contact.first_name + " " + contact.last_name == full_name for contact in address_book.contacts):
                            print("A contact with this name already exists. Please enter a different name.")
                            continue

                        address = get_valid_input("Enter address: ", lambda x: len(x) > 0)
                        city = get_valid_input("Enter city: ", lambda x: len(x) > 0)
                        state = get_valid_input("Enter state: ", lambda x: len(x) > 0)
                        zip_code = get_valid_input("Enter zip code: ", is_valid_zip)
                        phone_number = get_valid_input("Enter phone number: ", is_valid_phone)
                        email = get_valid_input("Enter email address: ", is_valid_email)

                        # Create and add contact
                        contact = Contact(book_name,first_name, last_name, address, city, state, zip_code, phone_number, email)
                        address_book.add_contact(contact)
                        print("Contact added successfully!")
                        break

                elif sub_choice == '2':
                    # Ask user if they want to sort the display
                    sort_choice = input("Do you want to display contacts sorted by an attribute? (y/n): ")
                    
                    if sort_choice.lower() == 'y':
                        print("Select attribute to sort by:")
                        print("1. City")
                        print("2. State")
                        print("3. Zip Code")
                        sub_choice = input("Enter your choice (1/2/3): ")

                        if sub_choice == '1':
                            address_book.display_contacts(sort_by='city')
                        elif sub_choice == '2':
                            address_book.display_contacts(sort_by='state')
                        elif sub_choice == '3':
                            address_book.display_contacts(sort_by='zip_code')
                        else:
                            logger.error("Invalid choice. Displaying contacts in original order.")
                            print("Invalid choice. Displaying contacts in original order.")
                            address_book.display_contacts()
                    elif sort_choice.lower() == 'n':
                        address_book.display_contacts()
                    else:
                        print("Invalid option. Displaying contacts in original order.")
                        address_book.display_contacts()

                elif sub_choice == '3':
                    full_name = input("Enter full name to edit contact: ")
                    if any(contact.first_name + " " + contact.last_name == full_name for contact in address_book.contacts):
                        print("\n1. Edit First Name")
                        print("2. Edit Last Name")
                        print("3. Edit Address")
                        print("4. Edit City")
                        print("5. Edit State")
                        print("6. Edit Zip Code")
                        print("7. Edit Phone Number")
                        print("8. Edit Email")
                        edit_choice = input("Enter your choice: ")

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

            AddressBook().display_all_address_books() 


        elif choice == '4':
            if len(address_books) != 0:
                book_name = input("Enter the name of the Address Book to search: ")
                if book_name not in address_books:
                    print("Address Book not found.")
                    continue

                address_book = address_books[book_name]

                city_to_search = get_valid_input("Enter city to search: ", lambda x: len(x) > 0)
                search_person_in_city(address_book,city_to_search)
            else:
                print("No address books available.")

        elif choice == '5':
            if len(address_books) != 0:
                book_name = input("Enter the name of the Address Book to search: ")
                if book_name not in address_books:
                    print("Address Book not found.")
                    continue

                address_book = address_books[book_name]

                state_to_search = get_valid_input("Enter state to search: ", lambda x: len(x) > 0)
                state_persons_dict = persons_by_state(address_book, state_to_search)
                
                if state_persons_dict:
                    print(f"\nPersons in state '{state_to_search}':")
                    logger.info(f"Persons in state '{state_to_search}':")

                    for state, names in state_persons_dict.items():
                        logger.info(f"State: {state}")

                        print(f"State: {state}")
                        for name in names:
                            logger.info(f"- {name}")

                            print(f"- {name}")
                        logger.info(f"Total Contact: {len(names)}")
                        print(f"\nTotal Contact: {len(names)}")
                else:
                    logger.error(f"No persons found in state '{state_to_search}'.")

                    print(f"No persons found in state '{state_to_search}'.")
            else:
                logger.error("No address books available.")

                print("No address books available.")

        elif choice == '6':
            delete_book_name = get_valid_input("Enter Address book name to  delete:  ", lambda x: len(x) > 0)
            address_book = AddressBook()
            address_book.delete_address_book(delete_book_name)



        elif choice == '7':
            # Exit the program
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
