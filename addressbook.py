'''


    @Author: Shivraj Yelave
    @Date: 05-09-24
    @Last modified by: Shivraj Yelave
    @Last modified time: 
    @Title: Address Book Program


'''

# Import required modules/files
import re  # Import the regular expressions module for input validation
from logger import get_info_logger  # Import the custom logger function from the logger module

# Regex patterns for validation
EMAIL_REGEX = r'^[\w]+([._%+-][\w]+)*@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(\.[a-zA-Z]{2,})?$'  # Regular expression for email validation
PHONE_REGEX = r'^\d{10}$'  # Regular expression for phone number validation (10 digits)
ZIP_REGEX = r'^\d{6}$'  # Regular expression for zip code validation (6 digits)

# Setup logger
logger = get_info_logger('AddressBook')  # Initialize the logger with the name 'AddressBook'

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
    
    while True:  # Continuously prompt the user until valid input is provided
        user_input = input(prompt)  # Display prompt and get user input

        if validation_func(user_input):  # Check if the input is valid
            return user_input  # Return valid input
        else:
            logger.error(f"Invalid input: {user_input}")  # Log an error if input is invalid
            print("Invalid input. Please try again.")  # Notify the user about invalid input

def is_valid_email(email):
    
    """
    
    Description: 
    Validate the email address using regex.

    Parameters:
    email (str): The email address to validate.

    Returns:
    bool: True if the email is valid, False otherwise.
    
    """
    
    return re.match(EMAIL_REGEX, email) is not None  # Check if the email matches the regex pattern

def is_valid_phone(phone):
    
    """
    
    Description: 
    Validate the phone number using regex.

    Parameters:
    phone (str): The phone number to validate.

    Returns:
    bool: True if the phone number is valid, False otherwise.
    
    """
    
    return re.match(PHONE_REGEX, phone) is not None  # Check if the phone number matches the regex pattern

def is_valid_zip(zip_code):
    
    """
    
    Description: 
    Validate the zip code using regex.

    Parameters:
    zip_code (str): The zip code to validate.

    Returns:
    bool: True if the zip code is valid, False otherwise.
    
    """
    
    return re.match(ZIP_REGEX, zip_code) is not None  # Check if the zip code matches the regex pattern

def main():
    # Print a welcome message to the user
    print(f"{'*'*10} Welcome to Address Book Program {'*'*10}")
    
    # Prompt the user for input and validate each field
    first_name = get_valid_input("Enter first name: ", lambda x: len(x) > 0)  # Validate first name
    last_name = get_valid_input("Enter last name: ", lambda x: len(x) > 0)  # Validate last name
    address = get_valid_input("Enter address: ", lambda x: len(x) > 0)  # Validate address
    city = get_valid_input("Enter city: ", lambda x: len(x) > 0)  # Validate city
    state = get_valid_input("Enter state: ", lambda x: len(x) > 0)  # Validate state
    zip_code = get_valid_input("Enter zip code: ", is_valid_zip)  # Validate zip code
    phone_number = get_valid_input("Enter phone number: ", is_valid_phone)  # Validate phone number
    email = get_valid_input("Enter email address: ", is_valid_email)  # Validate email address

    # Log the details of the added contact
    logger.info(f"Contact added: {first_name} {last_name}, {address}, {city}, {state}, {zip_code}, {phone_number}, {email}")

if __name__ == "__main__":
    main()  # Run the main function if the script is executed directly
