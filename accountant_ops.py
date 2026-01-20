from datetime import datetime
import data_handler

# ------------------------------
# Accountant Functions
# ------------------------------


def record_guest_payment():
    payments = data_handler.read_data(data_handler.FILE_PAYMENTS)
    bookings = data_handler.read_data(data_handler.FILE_BOOKINGS)

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


def generate_income_report():
    payments = data_handler.read_data(data_handler.FILE_PAYMENTS)   

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
def generate_outstanding_report():

    bookings = data_handler.read_data(data_handler.FILE_BOOKINGS)
    payments = data_handler.read_data(data_handler.FILE_PAYMENTS)   

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


def get_valid_month():
    while True:
        target_month = input("Enter Month to summarize (YYYY-MM): ")
        try:
            # Normalize month to always 2 digits
            dt = datetime.strptime(target_month, "%Y-%m")
            return dt.strftime("%Y-%m")  # returns 'YYYY-MM' format
        except ValueError:
            print("Invalid month format! Please enter in YYYY-MM format.")


def generate_monthly_summary():
    print("\n--- MONTHLY FINANCIAL REPORT ---")
    payments = data_handler.read_data(data_handler.FILE_PAYMENTS)

    target_month = get_valid_month()
        
    if not payments:
        print("No payment records found in system.")
        return

    # Initialize Counters
    total_revenue = 0.0
    transaction_count = 0
    method_breakdown = {} # Dictionary to store totals like {'Cash': 500, 'Card': 200}
    monthly_transactions = [] # List to store just this month's payments to print later

    # 2. Process Data
    for p in payments:
        # Check if date matches (e.g., "2025-12-01" starts with "2025-12")
        if p['date'].startswith(target_month):
            amount = float(p['amount'])
            method = p.get('method', 'Unknown') # Default to 'Unknown' if missing
            
            # Update Totals
            total_revenue += amount
            transaction_count += 1
            
            # Update Method Breakdown
            if method in method_breakdown:
                method_breakdown[method] += amount
            else:
                method_breakdown[method] = amount
            
            # Add to list for the ledger table
            monthly_transactions.append(p)

    if transaction_count == 0:
        print(f"No transactions found for {target_month}.")
        return

    # 3. Print Detailed Ledger Table
    print(f"\nDetailed Ledger for {target_month}")
    print(f"{'Date':<12} {'Pay ID':<10} {'Booking':<10} {'Method':<10} {'Amount (RM)'}")
    print("-" * 60)
    
    for t in monthly_transactions:
        print(f"{t['date']:<12} {t['payment_id']:<10} {t['booking_id']:<10} {t.get('method','-'):<10} {float(t['amount']):.2f}")
        
    print("-" * 60)

    # 4. Print Summaries
    print(f"\nSUMMARY STATISTICS")
    print(f"Total Transactions: {transaction_count}")
    
    print("\nREVENUE BY METHOD:")
    if not method_breakdown:
        print("  No method data available.")
    else:
        for method, amt in method_breakdown.items():
            print(f"  {method:<10}: RM {amt:.2f}")

    print("=" * 30)
    print(f"TOTAL REVENUE:    RM {total_revenue:.2f}")
    print("=" * 30)

# ------------------------------
# Main Accountant Menu
# ------------------------------
def show_menu():

    while True:
        print("\n--- ACCOUNTANT MAIN MENU ---")
        print("1. Record Guest Payment")
        print("2. Generate Income Report")
        print("3. Generate Outstanding Payment Report")
        print("4. Generate Monthly Financial Summary")
        print("5. Exit")

        choice = input("Enter choice (1-5): ")

        if choice == "1":
            record_guest_payment()
        elif choice == "2":
            generate_income_report()
        elif choice == "3":
            generate_outstanding_report()
        elif choice == "4":
            generate_monthly_summary()
        elif choice == "5":
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

