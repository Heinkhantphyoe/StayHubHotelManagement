import data_handler

def show_menu():
    while True:
        print("\nHOUSEKEEPING MENU")
        print("1. Update Room Cleaning Status")
        print("2. Update Maintenance Issue")
        print("3. View Daily Cleaning Schedule")
        print("0. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            update_cleaning_status()
        elif choice == "2":
            update_maintenance_issue()
        elif choice == "3":
            view_cleaning_schedule()
        elif choice == "0":
            break
        else:
            print("Invalid choice")

def update_cleaning_status():
    view_cleaning_schedule()

    room_id = input("Enter Room ID: ")

    rooms = data_handler.read_data(data_handler.FILE_ROOMS)
    target_room = data_handler.find_record_by_id(rooms, "room_id", room_id)

    if target_room is None:
        print("Error: Room ID not found.")
        return

    if target_room["cleaning_status"] != "Dirty":
        print("Error: This room is already clean.")
        return

    target_room["cleaning_status"] = "Clean"

    if target_room["status"] == "Available":
        print("Room is now ready for guests.")

    data_handler.save_data(data_handler.FILE_ROOMS, rooms)
    print("Success: Room marked as Clean.")
    
def update_maintenance_issue():
    print("\n--- HOUSEKEEPING: RESOLVE ROOM MAINTENANCE ---")

    rooms = data_handler.read_data(data_handler.FILE_ROOMS)

    print("Current Rooms in Maintenance:")
    print("---------------------------------")

    for room in rooms:
        if room["status"] == "Maintenance":
            print(f"Room ID: {room['room_id']} | Type: {room['type']}")

    print("---------------------------------")

    target_id = input("Enter Room ID to set as Available: ")
    target_room = data_handler.find_record_by_id(rooms, "room_id", target_id)

    if target_room is None:
        print(f"Error: Room ID {target_id} does not exist.")
        return

    if target_room["status"] == "Maintenance":
        target_room["status"] = "Available"
        target_room["cleaning_status"] = "Dirty"

        data_handler.save_data(data_handler.FILE_ROOMS, rooms)
        print(f"Success: Room {target_id} updated to Available. Need to Clean.")
    else:
        print(f"Error: Room {target_id} is not currently in Maintenance.")

def view_cleaning_schedule():
    rooms = data_handler.read_data(data_handler.FILE_ROOMS)

    print("\nDAILY CLEANING SCHEDULE")
    for room in rooms:
        if room["cleaning_status"] != "Clean":
            print(room["room_id"], room["type"], room["cleaning_status"])

