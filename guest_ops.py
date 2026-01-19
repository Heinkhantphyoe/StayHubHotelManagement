import data_handler
from datetime import datetime, timedelta

def view_available_rooms():
    print("\n--- AVAILABLE ROOMS ---")
    rooms = data_handler.read_data(data_handler.FILE_ROOMS)
    print(f"{'Type':<12} {'Price/Night':<12}")
    print("-" * 30)
    
    # Use a set to show unique types available (don't list 50 single rooms)
    available_rooms = set()
    for r in rooms:
        if r['status'] == 'Available' and r['cleaning_status'] == 'Clean':
            # Store tuple: (Type, Price)
            available_rooms.add((r['type'], r['price']))
            
    if not available_rooms:
        print("Sorry, no rooms available at the moment.")
    else:
        for r_type, price in available_rooms:
            print(f"{r_type:<12} RM {float(price):.2f}")
    

def make_reservation(current_guest):
    print("\n--- MAKE A RESERVATION ---")
    
    room_type = input("Enter Room Type (Single/Double/Deluxe): ").strip()
    days = input("Enter Number of Nights: ").strip()
    
    if not days.isdigit():
        print("Error: Nights must be a number.")
        return
    
    # 1. Check Availability
    rooms = data_handler.read_data(data_handler.FILE_ROOMS)
    target_room = None
    
    for r in rooms:
        if (r['type'].lower() == room_type.lower() and 
            r['status'] == 'Available' and r['cleaning_status'] == 'Clean'):
            target_room = r
            break
            
    if not target_room:
        print("Sorry, no rooms of that type are available.")
        return

    # 2. Confirm Price
    price = float(target_room['price'])
    total = price * int(days)
    print(f"Price per night: RM {price:.2f}")
    print(f"Total for {days} nights: RM {total:.2f}")
    
    confirm = input("Confirm Booking? (y/n): ").strip().lower()
    if confirm != 'y': return

    # 3. Create Booking
    bookings = data_handler.read_data(data_handler.FILE_BOOKINGS)
    new_id = f"B{len(bookings) + 1}"
    
    # Date Logic
    now = datetime.now()
    check_in = now.strftime("%Y-%m-%d")
    check_out = (now + timedelta(days=int(days))).strftime("%Y-%m-%d")
    
    new_booking = {
        'booking_id': new_id,
        'guest_name': current_guest['full_name'],
        'guest_id': current_guest['guest_id'], # Link to this specific user
        'room_id': target_room['room_id'],
        'check_in': check_in,
        'check_out': check_out,
        'nights': days,
        'status': 'Confirmed', # Guests create 'Confirmed' reservations
        'total_price': f"{total:.2f}"
    }
    
    # 4. Update Files
    target_room['status'] = 'Reserved'
    bookings.append(new_booking)
    
    data_handler.save_data(data_handler.FILE_BOOKINGS, bookings)
    data_handler.save_data(data_handler.FILE_ROOMS, rooms)
    print(f"Success! Your Booking ID is {new_id}.")
    print("Please proceed to payment at the reception upon arrival.")

def my_history(current_guest):
    print(f"\n--- BOOKING HISTORY: {current_guest['full_name']} ---")
    
    bookings = data_handler.read_data(data_handler.FILE_BOOKINGS)
    my_bookings = [b for b in bookings if b['guest_id'] == current_guest['guest_id']]
    
    if not my_bookings:
        print("No booking history found.")
    else:
        print(f"{'ID':<6} {'Room':<6} {'Check-In':<12} {'Status':<12} {'Total (RM)'}")
        print("-" * 55)
        for b in my_bookings:
            print(f"{b['booking_id']:<6} {b['room_id']:<6} {b['check_in']:<12} {b['status']:<12} {b['total_price']}")
    

def cancel_my_booking(current_guest):
    # [cite_start]Requirement: Cancel reservations [cite: 37]
    print("\n--- CANCEL MY RESERVATION ---")
    
    booking_id = input("Enter Booking ID to cancel: ").strip()
    
    bookings = data_handler.read_data(data_handler.FILE_BOOKINGS)
    rooms = data_handler.read_data(data_handler.FILE_ROOMS)
    
    # Find booking that belongs to THIS guest
    target = None
    for b in bookings:
        if b['booking_id'] == booking_id and b['guest_id'] == current_guest['guest_id']:
            target = b
            break
            
    if not target:
        print("Error: Booking ID not found in your history.")
        return
        
    # Validation: Guests can only cancel 'Confirmed' (future) bookings
    if target['status'] != 'Confirmed':
        print(f"Cannot cancel. Current status is '{target['status']}'.")
        print("Contact reception for assistance.")
        return

    # Process Cancellation
    target['status'] = 'Cancelled'
    target['total_price'] = "0.00"
    
    # Free the room
    for r in rooms:
        if r['room_id'] == target['room_id']:
            r['status'] = 'Available'
            break
            
    data_handler.save_data(data_handler.FILE_BOOKINGS, bookings)
    data_handler.save_data(data_handler.FILE_ROOMS, rooms)
    print("Reservation cancelled successfully.")

def show_menu(current_guest):
    while True:
        print(f"\n=== WELCOME, {current_guest['full_name'].upper()} ===")
        print("1. View Available Rooms")
        print("2. Make a Reservation")
        print("3. My Booking History & Bills")
        print("4. Cancel a Reservation")
        print("0. Logout")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            view_available_rooms()
        elif choice == '2':
            make_reservation(current_guest)
        elif choice == '3':
            my_history(current_guest)
        elif choice == '4':
            cancel_my_booking(current_guest)
        elif choice == '0':
            break
    