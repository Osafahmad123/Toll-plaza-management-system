Toll Plaza Management System
============================

This is a simple Toll Plaza Management System built using Python. It uses:
- Tkinter for the Graphical User Interface (GUI)
- SQLite for the database (stores vehicle records, toll rates, etc.)

---------------------------------------------
Files Included:
---------------------------------------------
1. main.py        - This is the main file. Run this to start the application.
2. frontend.py    - This file contains the user interface built with Tkinter.
3. backend.py     - This file handles all database operations using SQLite.
4. toll_plaza.db  - This is the SQLite database (automatically created when you run the app).

---------------------------------------------
Main Features:
---------------------------------------------
- Add different vehicle types like Car, Bus, Truck.
- Set toll rates for each vehicle type.
- Record vehicle entry with number plate and time.
- Search for vehicle records by number plate.
- View all vehicle passage history.
- Automatically clear messages after 5 seconds.

---------------------------------------------
How to Run:
---------------------------------------------
Step 1: Make sure Python 3 is installed on your system.

Step 2: Install Tkinter if not already installed:
    pip install tk

Step 3: Run the main file:
    python main.py

---------------------------------------------
Optional Improvements (Future Updates):
---------------------------------------------
- Export data to Excel or CSV
- Add admin login for more security
- Print receipt for toll transactions
- Search by date range
- Integrate RFID or barcode scanning

---------------------------------------------
Author:
---------------------------------------------
Osaf Ahmad
(BSCS Student)
