from datetime import datetime
import data_handler

# ------------------------------
# Accountant Functions
# ------------------------------


def record_guest_payment(payments, bookings):
    book_id = input("Enter Booking ID for payment: ")
    booking = data_handler.find_record_by_id(bookings, "booking_id", book_id)

    if booking:
        amount = input("Enter Amount Paid: ")
        if data_handler.is_valid_price(amount):
            pay_date = datetime.now().strftime("%Y-%m-%d")
            method = input("Enter Method (Cash/Card): ")
            while method not in ["Cash", "Card"]:
                print("Error: Payment method must be 'Cash' or 'Card'.")
                method = input("Enter Method (Cash/Card): ")

            new_payment = {
                "payment_id": "P" + str(len(payments) + 1),
                "booking_id": book_id,
                "amount": float(amount),
                "date": pay_date,
                "method": method,
            }

            payments.append(new_payment)
            data_handler.save_data(data_handler.FILE_PAYMENTS, payments)
            # save_data(FILE_PAYMENTS, payments)
            print(f"Success: Payment recorded for Booking {book_id}")
        else:
            print("Error: Invalid amount entered.")
    else:
        print("Error: Booking ID not found.")


def generate_income_report(payments):
    start_date = input("Enter Start Date (YYYY-MM-DD): ")
    while not data_handler.is_valid_date(start_date):
        print("\nError: Invalid date format.Please use YYYY-MM-DD format.")
        start_date = input("Enter Start Date (YYYY-MM-DD): ")

    end_date = input("Enter End Date (YYYY-MM-DD): ")
    while not data_handler.is_valid_date(end_date):
        print("\nError: Invalid date format.Please use YYYY-MM-DD format.")
        end_date = input("Enter End Date (YYYY-MM-DD): ")
    total_income = 0.0

    print(f"\n--------- INCOME REPORT ({start_date} to {end_date}) ---------")
    for record in payments:
        if start_date <= record["date"] <= end_date:
            print(
                f"{record['date']} | Book ID: {record['booking_id']} | Amount: {record['amount']}"
            )
            total_income += float(record["amount"])
    print(f"Total Income Collected: {total_income}")
    print("-------------------------------------------------")


# This report identifies bookings that require payment by comparing booking records with payment records.
# Cancelled and pending bookings are excluded,
def generate_outstanding_report(bookings, payments):
    total_owed = 0.0

    print("\n--- OUTSTANDING PAYMENTS REPORT ---")

    # Create a set of paid booking IDs
    paid_booking_ids = {p["booking_id"] for p in payments}

    for b in bookings:
        status = b.get("status")

        # Skip cancelled or pending bookings
        if status in ("Cancelled", "Pending"):
            continue

        # If booking not paid
        if b["booking_id"] not in paid_booking_ids:
            amount = float(b.get("total_price", 0))
            total_owed += amount

            print(
                f"Unpaid Booking: {b['booking_id']} | "
                f"Guest: {b['guest_name']} | "
                f"Status: {status} | "
                f"Amount Due: RM {amount}"
            )

    print("----------------------------------")
    print(f"TOTAL OUTSTANDING AMOUNT: RM {total_owed:.2f}")


# def generate_monthly_summary(payments):
#     target_month = input("Enter Month to summarize (YYYY-MM): ")

#     # Validate input
#     try:
#         datetime.strptime(target_month, "%Y-%m")
#     except ValueError:
#         print("Invalid month format! Use YYYY-MM.")
#         return

#     monthly_total = 0.0

#     for p in payments:
#         try:
#             payment_date = datetime.strptime(p["date"], "%Y-%m-%d")
#             if payment_date.year == int(target_month[:4]) and payment_date.month == int(target_month[5:7]):
#                 monthly_total += float(p["amount"])
#         except ValueError:
#             print(f"Skipping invalid date: {p['date']}")
#             continue

#     print(f"\n--- FINANCIAL SUMMARY FOR {target_month} ---")
#     print(f"TOTAL REVENUE FOR MONTH: {monthly_total:.2f}")
#     print("--------------------------------------")


def get_valid_month():
    while True:
        target_month = input("Enter Month to summarize (YYYY-MM): ")
        try:
            # Normalize month to always 2 digits
            dt = datetime.strptime(target_month, "%Y-%m")
            return dt.strftime("%Y-%m")  # returns 'YYYY-MM' format
        except ValueError:
            print("Invalid month format! Please enter in YYYY-MM format.")


def generate_monthly_summary(payments):
    """
    Simple monthly summary: only total revenue.
    """
    target_month = get_valid_month()
    total_revenue = 0.0

    for p in payments:
        if p["date"].startswith(target_month):
            total_revenue += float(p.get("amount", 0))

    print(f"\n--- TOTAL REVENUE FOR {target_month} ---")
    print(f"Total Revenue: RM {total_revenue:.2f}")
    print("--------------------------------------")


# ------------------------------
# Main Accountant Menu
# ------------------------------
def show_menu():
    payments = data_handler.read_data(data_handler.FILE_PAYMENTS)
    bookings = data_handler.read_data(data_handler.FILE_BOOKINGS)

    while True:
        print("\n--- ACCOUNTANT MAIN MENU ---")
        print("1. Record Guest Payment")
        print("2. Generate Income Report")
        print("3. Generate Outstanding Payment Report")
        print("4. Generate Monthly Financial Summary")
        print("5. Exit")

        choice = input("Enter choice (1-5): ")

        if choice == "1":
            record_guest_payment(payments, bookings)
        elif choice == "2":
            generate_income_report(payments)
        elif choice == "3":
            generate_outstanding_report(bookings, payments)
        elif choice == "4":
            generate_monthly_summary(payments)
        elif choice == "5":
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

