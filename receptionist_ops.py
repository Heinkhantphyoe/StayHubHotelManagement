import data_handler
from datetime import datetime,timedelta

def show_menu():
    while True:
        print("\n--- RECEPTIONIST MENU ---")
        print("1. Register New Guest")
        print("2. Update Guest Information")
        print("3. Book Room")
        print("4. Check-In Guest")
        print("5. Check-Out Guest")
        print("6. Cancel Booking")
        print("7. View Room Availability")
        print("0. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            register_guest()
        elif choice == "2":
            update_guest()
        elif choice == "3":
            book_room()
        elif choice == "4":
            check_in()
        elif choice == "5":
            check_out()
        elif choice == "6":
            cancel_booking()
        elif choice == "7":
            view_room_availability()
        elif choice == "0":
            break
        else:
            print("Invalid choice")


# =========================
# REGISTER GUEST
# =========================
def register_guest():
    print("\n--- REGISTER NEW GUEST ---")
    
    # 1. Collect Personal Info
    name = input("Enter Full Name: ").strip()
    ic_pass = input("Enter IC or Passport Number: ").strip()
    phone = input("Enter Phone Number: ").strip()
    email = input("Enter Email Address: ").strip()

    while not data_handler.check_valid_email(email):
        print("Error: Invalid email format.type again.")
        email = input("Enter Email Address: ").strip()
    
    # 2. Collect Login Info
    username = input("Enter New Username: ").strip()
    password = input("Enter New Password: ").strip()

    while not data_handler.check_valid_password(password):
        print("Error: Password must be at least 6 characters long.")
        password = input("Enter New Password: ").strip()
    
    # 3. Validation
    if not name or not ic_pass or not username or not password:
        print("Error: All fields (Name, IC, Username, Password) are required.")
        return
    
    # Check for duplicates (Username AND IC)
    guests = data_handler.read_data(data_handler.FILE_GUESTS)
    for g in guests:
        if g['ic_passport'] == ic_pass:
            print("Error: Guest with this IC/Passport already registered!")
            return
        if g['username'] == username:
            print("Error: Username already taken!")
            return

    # 4. Save Data
    new_id = f"G{len(guests) + 1}"
    
    new_guest = {
        'guest_id': new_id,
        'username': username,
        'password': password,
        'full_name': name, # using 'full_name'
        'phone': phone,
        'ic_passport': ic_pass,
        'email': email
    }
    
    guests.append(new_guest)
    data_handler.save_data(data_handler.FILE_GUESTS, guests)
    print(f"Success: Guest {name} registered. They can now login as '{username}'.")


def book_room():
    print("\n--- ADVANCE ROOM RESERVATION ---")
    
    # 1. Validate Guest (Using Standard Loop)
    guest_id = input("Enter Guest ID (e.g., G1): ").strip()
    guests = data_handler.read_data(data_handler.FILE_GUESTS)
    
    found_guest = None
    for g in guests:
        if g['guest_id'] == guest_id:
            found_guest = g
            break  # Stop looping once found
            
    if not found_guest:
        print("Error: Guest ID not found. Please register first.")
        return

    # 2. Find Room and Get Price
    room_type = input("Enter Desired Room Type: ").strip()
    days = input("Enter Number of Nights: ").strip()
    
    if not days.isdigit():
        print("Error: Nights must be a number.")
        return
    
    nights_int = int(days)
    rooms = data_handler.read_data(data_handler.FILE_ROOMS)
    
    assigned_room = None
    room_price = 0.0
    
    for r in rooms:
        # Check Type, Status, and Cleaning
        if (r['type'].lower() == room_type.lower() and 
            r['status'] == 'Available' and 
            r['cleaning_status'] == 'Clean'):
            assigned_room = r
            room_price = float(r['price'])
            break # Stop looping once found
            
    if not assigned_room:
        print(f"Error: No clean '{room_type}' rooms available.")
        return

    # 3. Calculate Dates & Total
    now_obj = datetime.now()
    check_in_str = now_obj.strftime("%Y-%m-%d")
    check_out_obj = now_obj + timedelta(days=nights_int)
    check_out_str = check_out_obj.strftime("%Y-%m-%d")
    total_cost = room_price * nights_int

    # 4. Create Booking Record
    bookings = data_handler.read_data(data_handler.FILE_BOOKINGS)
    new_id = f"B{len(bookings) + 1}"
    
    new_booking = {
        'booking_id': new_id,
        'guest_name': found_guest['full_name'],
        'guest_id': guest_id,
        'room_id': assigned_room['room_id'],
        'check_in': check_in_str,
        'check_out': check_out_str,
        'nights': days,
        'status': 'Confirmed',
        'total_price': f"{total_cost:.2f}"
    }
    
    # 5. Save Files
    assigned_room['status'] = 'Reserved'
    bookings.append(new_booking)
    data_handler.save_data(data_handler.FILE_BOOKINGS, bookings)
    data_handler.save_data(data_handler.FILE_ROOMS, rooms)
    
    print("-" * 40)
    print(f"SUCCESS: Room {assigned_room['room_id']} Reserved for {nights_int} nights.")
    print(f"Total Price: RM {total_cost:.2f}")
    print("-" * 40)
    print("\n--- ADVANCE ROOM RESERVATION ---")
    

# =========================
# UPDATE GUEST
# =========================
def update_guest():
    print("\n--- UPDATE GUEST INFO ---")
    search_id = input("Enter Guest ID to update (e.g., G1): ").strip()
    
    guests = data_handler.read_data(data_handler.FILE_GUESTS)
    target_guest = None
    
    # 1. Find the guest by ID
    for g in guests:
        if g['guest_id'] == search_id:
            target_guest = g
            break
            
    if not target_guest:
        print("Error: Guest ID not found.")
        return
        
    print(f"Editing Guest: {target_guest['full_name']} (User: {target_guest['username']})")
    print("Leave field blank to keep current value.")
    
    # 2. Collect New Data (Press Enter to skip)
    new_name = input(f"New Name ({target_guest['full_name']}): ").strip()
    new_phone = input(f"New Phone ({target_guest['phone']}): ").strip()
    new_email = input(f"New Email ({target_guest['email']}): ").strip()

    if new_email:
        while not data_handler.check_valid_email(new_email) :
            print("Error: Invalid email format.type again.")
            new_email = input(f"New Email ({target_guest['email']}): ").strip()

    new_pass = input(f"New Password ({target_guest['password']}): ").strip()
    if new_pass:
        while not data_handler.check_valid_password(new_pass):
            print("Error: Password must be at least 6 characters long.")
            new_pass = input(f"New Password ({target_guest['password']}): ").strip()
    # 3. Apply Updates
    # We do NOT allow changing 'guest_id' or 'username' to prevent system errors
    if new_name: target_guest['full_name'] = new_name
    if new_phone: target_guest['phone'] = new_phone
    if new_email: target_guest['email'] = new_email
    if new_pass: target_guest['password'] = new_pass
    
    # 4. Save Changes
    data_handler.save_data(data_handler.FILE_GUESTS, guests)
    print(f"Success: Guest information for {search_id} updated.")
    

# ====================
# CHECK-IN with booking
# ====================
def check_in():
    print("\n--- GUEST CHECK-IN ---")
    
    # Step 1: Ask if they have a reservation
    has_booking = input("Do you have a reservation? (yes/no): ").strip().lower()
    
    if has_booking == 'yes':
        # --- PATH A: PROCESS EXISTING RESERVATION ---
        booking_id = input("Enter Booking ID (e.g., B1): ").strip()
        
        # Load Data
        bookings = data_handler.read_data(data_handler.FILE_BOOKINGS)
        rooms = data_handler.read_data(data_handler.FILE_ROOMS)
        
        # 1. Find the Booking
        target_booking = None
        for b in bookings:
            if b['booking_id'] == booking_id:
                target_booking = b
                break
        
        if not target_booking:
            print("Error: Booking ID not found.")
            return
            
        # 2. Validate Status
        # Only 'Confirmed' bookings can check in. 
        # 'Active' means already here, 'Cancelled' is void.
        if target_booking['status'] != 'Confirmed':
            print(f"Error: Cannot check-in. Current status is '{target_booking['status']}'.")
            return

        print(f"Reservation Found: {target_booking['guest_name']}")
        print(f"Room: {target_booking['room_id']} ({target_booking['check_in']} to {target_booking['check_out']})")
        
        confirm = input("Confirm Check-In? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Check-in cancelled.")
            return

        # 3. Update Booking Status
        target_booking['status'] = 'Checked-in'
        
        # 4. Update Room Status (Reserved -> Occupied)
        room_found = False
        for r in rooms:
            if r['room_id'] == target_booking['room_id']:
                r['status'] = 'Occupied'
                room_found = True
                break
        
        if not room_found:
            print("Warning: Room ID in booking not found in rooms.txt!")
        
        # 5. Save Changes
        data_handler.save_data(data_handler.FILE_BOOKINGS, bookings)
        data_handler.save_data(data_handler.FILE_ROOMS, rooms)
        print(f"Success: Guest {target_booking['guest_name']} is now Checked-In.")

    elif has_booking == 'no':
        # --- PATH B: WALK-IN ---
        # Calls the separate helper function for new guests
        walk_in_check_in()
        
    else:
        print("Invalid input. Please type 'yes' or 'no'.")

# =========================
# CHECK-IN without booking
# =========================
def walk_in_check_in():
    print("\n--- WALK-IN CHECK-IN ---")
    
    # 1. Validate Guest
    guest_id = input("Enter Guest ID: ").strip()
    guests = data_handler.read_data(data_handler.FILE_GUESTS)
    
    found_guest = None
    for g in guests:
        if g['guest_id'] == guest_id:
            found_guest = g
            break
            
    if not found_guest:
        print("Error: Guest not found. Please register first.")
        return

    # 2. Select Room
    room_type = input("Enter Room Type: ").strip()
    days = input("Enter Nights: ").strip()
    
    if not days.isdigit():
        print("Error: Invalid number.")
        return
        
    nights_int = int(days)
    rooms = data_handler.read_data(data_handler.FILE_ROOMS)
    
    assigned_room = None
    room_price = 0.0
    
    for r in rooms:
        if (r['type'].lower() == room_type.lower() and 
            r['status'] == 'Available' and r['cleaning_status'] == 'Clean'):
            assigned_room = r
            room_price = float(r['price'])
            break
            
    if not assigned_room:
        print("Error: No rooms available.")
        return

    # 3. Calculations
    now_obj = datetime.now()
    check_in_str = now_obj.strftime("%Y-%m-%d")
    check_out_obj = now_obj + timedelta(days=nights_int)
    check_out_str = check_out_obj.strftime("%Y-%m-%d")
    total_cost = room_price * nights_int

    # 4. Save Data
    bookings = data_handler.read_data(data_handler.FILE_BOOKINGS)
    new_id = f"B{len(bookings) + 1}"
    
    new_booking = {
        'booking_id': new_id,
        'guest_name': found_guest['full_name'],
        'guest_id': guest_id,
        'room_id': assigned_room['room_id'],
        'check_in': check_in_str,
        'check_out': check_out_str,
        'nights': days,
        'status': 'Checked-in',
        'total_price': f"{total_cost:.2f}"
    }
    
    assigned_room['status'] = 'Occupied'
    bookings.append(new_booking)
    data_handler.save_data(data_handler.FILE_BOOKINGS, bookings)
    data_handler.save_data(data_handler.FILE_ROOMS, rooms)
    
    print(f"Walk-in Successful. Total to Pay: RM {total_cost:.2f}")

 

# =========================
# CHECK-OUT
# =========================
def check_out():
    print("\n--- GUEST CHECK-OUT ---")
    
    # 1. Input Room ID
    room_id = input("Enter Room ID to Checkout: ").strip()
    
    # 2. Find Active Booking for this Room
    bookings = data_handler.read_data(data_handler.FILE_BOOKINGS)
    target_booking = None
    
    # We loop to find a booking for this room that is 'Active' or 'Checked-in'
    for b in bookings:
        if b['room_id'] == room_id and (b['status'] == 'Active' or b['status'] == 'Checked-in'):
            target_booking = b
            break
            
    if not target_booking:
        print("Error: No active booking found for this room.")
        return

    # 3. Get Room Price (Needed for Late Fee Calculation)
    rooms = data_handler.read_data(data_handler.FILE_ROOMS)
    room_price = 0.0
    target_room = None
    
    for r in rooms:
        if r['room_id'] == room_id:
            target_room = r
            room_price = float(r['price'])
            break

    # 4. Check for Late Fees
    expected_checkout_str = target_booking['check_out']
    today_obj = datetime.now()
    today_str = today_obj.strftime("%Y-%m-%d")
    
    # Convert strings to Date Objects for math
    # strptime parses "2025-12-05" into a date object
    expected_date_obj = datetime.strptime(expected_checkout_str, "%Y-%m-%d")
    
    # Calculate difference
    late_fee = 0.0
    overdue_days = 0
    
    # If Today is AFTER Expected Date
    if today_obj.date() > expected_date_obj.date():
        delta = today_obj.date() - expected_date_obj.date()
        overdue_days = delta.days
        late_fee = overdue_days * room_price
        
        print(f"\nALERT: Guest is overdue by {overdue_days} day(s)!")
        print(f"Late Fee Applied: RM {late_fee:.2f} ({overdue_days} x RM {room_price})")

    # 5. Calculate Final Total
    # Read current total (remove 'RM' or whitespace if present)
    current_total = float(target_booking['total_price'])
    final_total = current_total + late_fee
    
    print("-" * 40)
    print(f"Guest Name:     {target_booking['guest_name']}")
    print(f"Original Total: RM {current_total:.2f}")
    print(f"Late Fees:      RM {late_fee:.2f}")
    print(f"FINAL TOTAL:    RM {final_total:.2f}")
    print("-" * 40)
    
    confirm = input("Confirm Check-out and Payment? (y/n): ").strip().lower()
    if confirm != 'y':
        return

    # 6. Update Files
    # Update Booking
    target_booking['status'] = 'Checked-out'
    target_booking['total_price'] = f"{final_total:.2f}"
    # Optionally update the check_out date to today so history is accurate
    target_booking['check_out'] = today_str 
    
    # Update Room (Set to Dirty so Housekeeping sees it)
    if target_room:
        target_room['status'] = 'Available'
        target_room['cleaning_status'] = 'Dirty'

    
    data_handler.save_data(data_handler.FILE_BOOKINGS, bookings)
    data_handler.save_data(data_handler.FILE_ROOMS, rooms)
    
    print(f"Success: Room {room_id} has been checked out.")
    print("Status: Available (Dirty) - Housekeeping notified.")


# =========================
# CANCEL BOOKING
# =========================
def cancel_booking():
    print("\n--- CANCEL RESERVATION ---")
    
    # 1. Input Booking ID
    booking_id = input("Enter Booking ID to Cancel (e.g., B1): ").strip()
    
    bookings = data_handler.read_data(data_handler.FILE_BOOKINGS)
    rooms = data_handler.read_data(data_handler.FILE_ROOMS)
    
    # 2. Find the Booking
    target_booking = None
    for b in bookings:
        if b['booking_id'] == booking_id:
            target_booking = b
            break
            
    if not target_booking:
        print("Error: Booking ID not found.")
        return

    # 3. Simple Status Check
    # We ONLY allow cancelling 'Confirmed' bookings.
    if target_booking['status'] not in ['Confirmed']:
        print(f"Error: Cannot cancel this booking. Current status is '{target_booking['status']}'.")
        print("You can only cancel reservations that have not arrived yet.")
        return

    # 4. Confirmation
    print(f"Cancelling reservation for {target_booking['guest_name']} (Room {target_booking['room_id']}).")
    confirm = input("Are you sure? (y/n): ").strip().lower()
    
    if confirm != 'y':
        return

    # 5. Process Cancellation
    # Update Booking
    target_booking['status'] = 'Cancelled'
    target_booking['total_price'] = "0.00"
    
    # Update Room (Make it Available again)
    for r in rooms:
        if r['room_id'] == target_booking['room_id']:
            r['status'] = 'Available'
            # We don't change cleaning_status because the guest never entered the room.
            break
            
    # 6. Save
    data_handler.save_data(data_handler.FILE_BOOKINGS, bookings)
    data_handler.save_data(data_handler.FILE_ROOMS, rooms)
    print("Success: Reservation cancelled. Room is now Available.")
# =========================
# VIEW ROOM AVAILABILITY
# =========================
def view_room_availability():
    print("\n--- AVAILABLE ROOMS ---")
    
    rooms = data_handler.read_data(data_handler.FILE_ROOMS)
    
    # Header
    print(f"{'ID':<8} {'Type':<12} {'Price':<10} {'Condition'}")
    print("-" * 45)
    
    found_any = False
    
    for r in rooms:
        # We ONLY show the room if the status is strictly 'Available' and 'Clean'
        if r['status'] == 'Available' and r['cleaning_status'] == 'Clean':
            condition = r['cleaning_status']
            price = f"RM{float(r['price']):.0f}"
            
            print(f"{r['room_id']:<8} {r['type']:<12} {price:<10} {condition}")
            found_any = True

    if not found_any:
        print("No rooms are currently available.")
        
    print("-" * 45)


