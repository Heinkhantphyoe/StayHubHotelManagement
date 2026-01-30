import data_handler
from datetime import datetime, timedelta

def add_room():
    print("\n--- ADD NEW ROOM ---")
    rooms = data_handler.read_data(data_handler.FILE_ROOMS)
    r_type = input("Enter Room Type (Single/Double/Deluxe): ").strip()
    while r_type not in ['Single', 'Double', 'Deluxe']:
        print("Error: Invalid room type. Please enter Single, Double, or Deluxe.")
        r_type = input("Enter Room Type (Single/Double/Deluxe): ").strip()
    price = input("Enter Price per Night: ").strip()
    
    while not data_handler.is_valid_price(price):
        print("Error: Price must be a valid positive number.")
        price = input("Enter Price per Night: ").strip()

    # Create new record
    new_room = {
        'room_id': "R" + str(len(rooms) + 1),
        'type': r_type,
        'price': price,
        'status': 'Available',
        'cleaning_status': 'Clean'
    }
    
    rooms.append(new_room)
    data_handler.save_data(data_handler.FILE_ROOMS, rooms)
    print("Success: Room added.")

def delete_room():
    print("\n--- DELETE ROOM ---")
    room_id = input("Enter Room ID to delete: ").strip()
    rooms = data_handler.read_data(data_handler.FILE_ROOMS)
    
    # List comprehension to keep rooms NOT matching the ID
    new_rooms = [r for r in rooms if r['room_id'] != room_id]
    
    if len(rooms) == len(new_rooms):
        print("Room ID not found.Please try again.")
    else:
        data_handler.save_data(data_handler.FILE_ROOMS, new_rooms)
        print("Success: Room deleted.")

def system_summary():
    rooms = data_handler.read_data(data_handler.FILE_ROOMS)
    bookings = data_handler.read_data(data_handler.FILE_BOOKINGS)
    payments = data_handler.read_data(data_handler.FILE_PAYMENTS)
    
    total_rooms = len(rooms)
    occupied = len([r for r in rooms if r['status'] == 'Occupied'])
    
    # Calculate total income from payments
    total_income = 0
    try:
        total_income = sum(float(p.get('amount', 0)) for p in payments)
    except (ValueError, TypeError):
        pass
    
    print("\n--- SYSTEM SUMMARY REPORT ---")
    print(f"Total Rooms: {total_rooms}")
    print(f"Occupied Rooms: {occupied}")
    print(f"Total Bookings Recorded: {len(bookings)}")
    print(f"Total Hotel Income: RM {total_income:.2f}")
    if total_rooms > 0:
        print(f"Occupancy Rate: {(occupied/total_rooms)*100:.2f}%")

def update_room():
    """Update room details (type, price, status, cleaning)"""
    print("\n--- UPDATE ROOM ---")
    room_id = input("Enter Room ID to update: ").strip()

    rooms = data_handler.read_data(data_handler.FILE_ROOMS)
    target_room = data_handler.find_record_by_id(rooms, 'room_id', room_id)

    if not target_room:
        print("Error: Room ID not found.")
        return

    print("\nPress Enter to keep the current value.")

    # --- Room Type ---
    current_type = target_room.get("type", "")
    new_type = input(f"Room Type (Single/Double/Deluxe) [{current_type}]: ").strip()
    if new_type != "":
        while new_type not in ["Single", "Double", "Deluxe"]:
            print("Error: Invalid room type. Please enter Single, Double, or Deluxe.")
            new_type = input(f"Room Type (Single/Double/Deluxe) [{current_type}]: ").strip()
            if new_type == "":
                new_type = None
                break
        if new_type:
            target_room["type"] = new_type

    # --- Price ---
    current_price = target_room.get("price", "")
    new_price = input(f"Price per Night [{current_price}]: ").strip()
    if new_price != "":
        while not data_handler.is_valid_price(new_price):
            print("Error: Price must be a valid positive number.")
            new_price = input(f"Price per Night [{current_price}]: ").strip()
            if new_price == "":
                new_price = None
                break
        if new_price:
            target_room["price"] = new_price

    # --- Status ---
    current_status = target_room.get("status", "")
    new_status = input(f"Status (Available/Occupied/Maintenance/Reserved) [{current_status}]: ").strip()
    if new_status != "":
        while new_status not in ["Available", "Occupied", "Maintenance", "Reserved"]:
            print("Error: Status must be Available, Occupied, Maintenance, or Reserved.")
            new_status = input(
                f"Status (Available/Occupied/Maintenance/Reserved) [{current_status}]: "
            ).strip()
            if new_status == "":
                new_status = None
                break
        if new_status:
            target_room["status"] = new_status

    # --- Cleaning Status ---
    current_clean = target_room.get("cleaning_status", "")
    new_clean = input(f"Cleaning Status (Clean/Dirty) [{current_clean}]: ").strip()
    if new_clean != "":
        while new_clean not in ["Clean", "Dirty"]:
            print("Error: Cleaning status must be Clean or Dirty.")
            new_clean = input(f"Cleaning Status (Clean/Dirty) [{current_clean}]: ").strip()
            if new_clean == "":
                new_clean = None
                break
        if new_clean:
            target_room["cleaning_status"] = new_clean

    # Save data
    data_handler.save_data(data_handler.FILE_ROOMS, rooms)
    print("Success: Room updated.")

def generate_daily_report():
    """Generate daily performance report."""
    print("\n--- DAILY PERFORMANCE REPORT ---")
    
    bookings = data_handler.read_data(data_handler.FILE_BOOKINGS)
    payments = data_handler.read_data(data_handler.FILE_PAYMENTS)
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Bookings made today
    today_bookings = [b for b in bookings if b.get('check_in') == today]
    
    # Payments made today
    today_payments = [p for p in payments if p.get('date') == today]
    today_revenue = sum(float(p.get('amount', 0)) for p in today_payments if data_handler.is_valid_price(p.get('amount', 0)))
    
    print(f"Date: {today}")
    print(f"New Check-ins Today: {len(today_bookings)}")
    print(f"Payments Received Today: {len(today_payments)}")
    print(f"Daily Revenue: RM {today_revenue:.2f}")
    
    # Active bookings
    active_bookings = [b for b in bookings if b.get('status') == 'Checked-in']
    pending_bookings = [b for b in bookings if b.get('status') == 'Confirmed']
    print(f"Current Active Bookings: {len(active_bookings)}")
    print(f"Pending Bookings (Not Yet Checked In): {len(pending_bookings)}")
    
    if today_bookings:
        print("\nNew Check-ins:")
        for b in today_bookings:
            print(f"  - {b['guest_name']} (Room {b['room_id']})")

def generate_monthly_report():
    """Generate monthly performance report."""
    print("\n--- MONTHLY PERFORMANCE REPORT ---")
    
    bookings = data_handler.read_data(data_handler.FILE_BOOKINGS)
    payments = data_handler.read_data(data_handler.FILE_PAYMENTS)
    rooms = data_handler.read_data(data_handler.FILE_ROOMS)
    
    current_month = datetime.now().strftime("%Y-%m")
    
    # Filter bookings and payments for current month
    month_bookings = [b for b in bookings if b.get('check_in', '')[:7] == current_month]
    month_payments = [p for p in payments if p.get('date', '')[:7] == current_month]
    
    # Calculate monthly revenue
    month_revenue = 0
    try:
        month_revenue = sum(float(p.get('amount', 0)) for p in month_payments)
    except (ValueError, TypeError):
        pass
    
    # Calculate average occupancy and count booking statuses
    checked_out_bookings = [b for b in month_bookings if b.get('status') == 'Checked-out']
    active_bookings = [b for b in month_bookings if b.get('status') == 'Checked-in']
    pending_bookings = [b for b in month_bookings if b.get('status') == 'Confirmed']
    total_rooms = len(rooms) if len(rooms) > 0 else 1
    days_in_month = datetime.now().day
    
    if days_in_month > 0:
        avg_occupancy = (len(checked_out_bookings) / total_rooms / days_in_month) * 100
    else:
        avg_occupancy = 0
    
    print(f"Month: {current_month}")
    print(f"Total Bookings: {len(month_bookings)}")
    print(f"Completed Bookings: {len(checked_out_bookings)}")
    print(f"Active Bookings: {len(active_bookings)}")
    print(f"Pending Bookings: {len(pending_bookings)}")
    print(f"Total Revenue: RM {month_revenue:.2f}")
    print(f"Average Occupancy Rate: {avg_occupancy:.2f}%")
    print(f"Total Rooms: {total_rooms}")
    
    if len(month_payments) > 0:
        avg_payment = month_revenue / len(month_payments)
        print(f"Average Payment per Booking: RM {avg_payment:.2f}")

def show_menu():
    while True:
        print("\n=== MANAGER MENU ===")
        print("1. View All Rooms")
        print("2. Add New Room")
        print("3. Update Room")
        print("4. Delete Room")
        print("5. View System Summary")
        print("6. Generate Daily Report")
        print("7. Generate Monthly Report")
        print("0. Back to Main Menu")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            rooms = data_handler.read_data(data_handler.FILE_ROOMS)
            print(f"\n{'ID':<10} {'Type':<10} {'Price':<10} {'Status':<15} {'Cleaning Status'}")
            print("-" * 60)
            for r in rooms:
                print(f"{r['room_id']:<10} {r['type']:<10} {r['price']:<10} {r['status']:<15} {r['cleaning_status']}")
        elif choice == '2':
            add_room()
        elif choice == '3':
            update_room()
        elif choice == '4':
            delete_room()
        elif choice == '5':
            system_summary()
        elif choice == '6':
            generate_daily_report()
        elif choice == '7':
            generate_monthly_report()
        elif choice == '0':
            break
        else:
            print("Invalid input.")