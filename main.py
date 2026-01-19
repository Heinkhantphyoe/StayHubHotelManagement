import os
import time
import data_handler  # Your helper file
# Import the module for each group member
# Note: You must create these files for this to work!
import manager_ops
import receptionist_ops
import accountant_ops
import housekeeping_ops
import guest_ops

# --- LOGIN SYSTEM ---
def login():
    """
    Reads users.txt and guest.txt to validate username and password.
    Returns the role if successful, or None if failed.
    """
    print("\n" + "="*35)
    print(" STAY HUB HOTEL MANAGEMENT SYSTEM")
    print("="*35)
    
    input_user = input("Username: ").strip()
    input_pass = input("Password: ").strip()
    
    # Check staff users first
    users = data_handler.read_data(data_handler.FILE_USERS)
    
    if users:
        for user in users:
            if user['username'] == input_user and user['password'] == input_pass:
                print(f"\nLogin Successful! Welcome, {user['full_name']} ({user['role']})")
                return user['role'],user
            
    
    # Check guest users
    guests = data_handler.read_data(data_handler.FILE_GUESTS)
    
    if guests:
        for guest in guests:
            if guest['username'] == input_user and guest['password'] == input_pass:
                print(f"\nLogin Successful! Welcome, {guest['full_name']} (Guest)")
                time.sleep(1)
                return "Guest",guest
    
    print("\nError: Invalid Username or Password.")
    return "",None

# --- MAIN CONTROLLER ---
def main():
    while True:
        # 1. Perform Login
        role,user = login()
        
        if role:
            # 2. Redirect to specific module based on Role
            # This is where your group members' work connects
            if role == "Manager":
                manager_ops.show_menu() # Member 1's Code
            
            elif role == "Receptionist":
                receptionist_ops.show_menu() # Member 2's Code
            
            elif role == "Accountant":
                accountant_ops.show_menu() # Member 3's Code
            
            elif role == "Housekeeping":
                housekeeping_ops.show_menu() # Member 4's Code
            
            elif role == "Guest":
                guest_ops.show_menu(user) # Guest Operations
            
            else:
                print(f"Error: Role '{role}' is not recognized.")
        
        # 3. Exit or Re-login option
        choice = input("\nType 'exit' to close or Enter to login again: ").lower()
        if choice == 'exit':
            print("System Shutting Down...")
            print("Goodbye!Thank you for using Stay Hub Hotel Management System.")
            break

if __name__ == "__main__":
    main()