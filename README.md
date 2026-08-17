# StayHubHotelManagement

A console-based hotel management system built with Python.

## Features

The system supports role-based workflows:

- **Manager**: room management, system summary, daily/monthly reports
- **Receptionist**: guest registration/update, reservation, check-in/out, cancellation, room availability
- **Accountant**: payment recording, income reports, outstanding payments, monthly financial summary
- **Housekeeping**: cleaning status updates, maintenance resolution, cleaning schedule
- **Guest**: view available rooms, make reservation, view booking history, cancel reservation

## Project Structure

- `/home/runner/work/StayHubHotelManagement/StayHubHotelManagement/main.py` - entry point and login flow
- `/home/runner/work/StayHubHotelManagement/StayHubHotelManagement/data_handler.py` - shared file I/O and validation helpers
- `/home/runner/work/StayHubHotelManagement/StayHubHotelManagement/*_ops.py` - role-specific operations
- `/home/runner/work/StayHubHotelManagement/StayHubHotelManagement/data/` - plain-text data storage

## Requirements

- Python 3.10+
- No external dependencies (standard library only)

## Run

From the repository root:

```bash
python main.py
```

## Default Login Accounts

### Staff

| Role | Username | Password |
|---|---|---|
| Manager | `manager` | `admin123` |
| Receptionist | `recept` | `user123` |
| Accountant | `acc` | `money123` |
| Housekeeping | `house` | `clean123` |

### Guest

Example guest account:

- Username: `guest`
- Password: `123456789`

(Additional guest accounts are available in `data/guest.txt`.)

## Data Files

The application stores data in comma-separated `.txt` files under `/home/runner/work/StayHubHotelManagement/StayHubHotelManagement/data/`:

- `rooms.txt`
- `bookings.txt`
- `users.txt`
- `guest.txt`
- `payments.txt`
- `note.txt`

## Notes

- Data is persisted directly to text files.
- If a required file is missing, the app creates an empty one automatically.
