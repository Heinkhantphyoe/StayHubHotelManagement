import os
from datetime import datetime


# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# CONSTANTS - File Names
# defining them here ensures everyone uses the exact same filenames
FILE_ROOMS = os.path.join(SCRIPT_DIR, "data/rooms.txt")
FILE_BOOKINGS = os.path.join(SCRIPT_DIR, "data/bookings.txt")
FILE_USERS = os.path.join(SCRIPT_DIR, "data/users.txt")
FILE_PAYMENTS = os.path.join(SCRIPT_DIR, "data/payments.txt")
FILE_GUESTS = os.path.join(SCRIPT_DIR, "data/guest.txt")

def read_data(filename):
    """
    Reads a comma-separated text file and returns a list of dictionaries.
    Assumes the FIRST line of the text file is the Header (column names).
    """
    data_list = []
    
    # Validation: Check if file exists [cite: 88]
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found. Creating a new one...")
        # Create empty file if it doesn't exist to prevent crash
        with open(filename, 'w') as f: 
            pass 
        return []

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            
            # If file is empty, return empty list
            if len(lines) < 2:
                return []

            # Get headers from the first line (remove whitespace)
            headers = lines[0].strip().split(',')
            
            # Process the rest of the lines
            for line in lines[1:]:
                if line.strip():  # Skip empty lines
                    values = line.strip().split(',')
                    
                    # Create a dictionary for this row
                    # Example: {'room_id': '101', 'type': 'Deluxe'}
                    row_dict = {}
                    for i in range(len(headers)):
                        # Safety check in case a line is missing a value
                        if i < len(values):
                            row_dict[headers[i]] = values[i]
                        else:
                            row_dict[headers[i]] = "" 
                    
                    data_list.append(row_dict)
                    
        return data_list

    except IOError:
        print(f"Error: Unable to read from {filename}.")
        return []

def save_data(filename, data_list):
    """
    Writes a list of dictionaries back to the text file.
    Overwrites the existing file with new data.
    """
    if not data_list:
        return # Nothing to save

    try:
        with open(filename, 'w') as file:
            # 1. Extract Headers from the first dictionary keys
            headers = list(data_list[0].keys())
            
            # 2. Write the Header line
            file.write(",".join(headers) + "\n")
            
            # 3. Write the Data lines
            for entry in data_list:
                # Convert all values to string to be safe
                # Use .get() to handle missing keys with empty string
                values = [str(entry.get(key, "")) for key in headers]
                file.write(",".join(values) + "\n")
                
        print(f"Success: Data saved to {filename}.")
        
    except IOError:
        print(f"Error: Unable to write to {filename}.")
    except Exception as e:
        print(f"Error: Failed to save data - {str(e)}")


# --- VALIDATION FUNCTIONS ---
def is_valid_price(price_str):
    """Validates if a string is a valid positive price."""
    try:
        price = float(price_str)
        return price > 0
    except (ValueError, TypeError):
        return False

def is_valid_integer(value_str):
    """Validates if a string is a valid positive integer."""
    try:
        value = int(value_str)
        return value > 0
    except (ValueError, TypeError):
        return False


def is_valid_date(date_str):
    """Check only YYYY-MM-DD format."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False


def find_record_by_id(data_list, id_field, id_value):
    """Finds a record in a data list by ID field."""
    for record in data_list:
        if record.get(id_field) == id_value:
            return record
    return None

def find_all_by_field(data_list, field_name, field_value):
    """Finds all records where field matches value."""
    results = []
    for record in data_list:
        if record.get(field_name) == field_value:
            results.append(record)
    return results

def check_valid_email(email):
    """Basic email format validation."""
    if "@" in email and "." in email:
        return True
    return False

def check_valid_password(password):
    """Basic password strength validation."""
    if len(password) < 6:
        return False
    return True