import mysql.connector as sql
import csv, pickle
from datetime import date

# ----------------- File paths -----------------
RESIDENTS_CSV = "residents_backup.csv"
PAYMENTS_CSV = "payments_backup.csv"
RESIDENTS_BIN = "residents.dat"
PAYMENTS_BIN = "payments.dat"
DUES_TXT = "dues.txt"
SEARCH_TXT = "search.txt"

# ----------------- Utility Functions -----------------
def validate_flat(flat):
    if flat.isdigit():
        return True
    print("Invalid flat number!")
    return False

def format_output(record):
    print("--- Record ---")
    for item in record:
        print(item)
    print("--------------")

def write_due_report(dues, filename):
    with open(filename, "w") as f:
        for d in dues:
            f.write(str(d) + "\n")
    print("Dues report generated as", filename)

def write_search_report(results, filename):
    with open(filename, "w") as f:
        for r in results:
            f.write(str(r) + "\n")
    print("Search report saved as", filename)

# ----------------- MySQL Connection -----------------
db = sql.connect(host="localhost", user="root", password="yourpass", database="society")
cur = db.cursor()

# Create tables if not exist
cur.execute("""
CREATE TABLE IF NOT EXISTS residents (
    flat_no VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50),
    contact VARCHAR(15),
    email VARCHAR(50)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS payments (
    flat_no VARCHAR(10),
    month VARCHAR(15),
    amount INT,
    pay_date DATE,
    FOREIGN KEY (flat_no) REFERENCES residents(flat_no)
)
""")
db.commit()

# ----------------- Core Functions -----------------
def add_resident():
    flat = input("Enter flat no: ")
    if not validate_flat(flat):
        return
    name = input("Enter name: ")
    contact = input("Enter contact: ")
    email = input("Enter email: ")

    cur.execute("INSERT INTO residents VALUES (%s, %s, %s, %s)", (flat, name, contact, email))
    db.commit()

    with open(RESIDENTS_CSV, "a", newline="") as f:
        csv.writer(f).writerow([flat, name, contact, email])

    with open(RESIDENTS_BIN, "ab") as f:
        pickle.dump([flat, name, contact, email], f)

    print("Resident added successfully!")

def update_resident():
    flat = input("Enter flat no to update: ")
    new_contact = input("Enter new contact: ")
    new_email = input("Enter new email: ")
    cur.execute("UPDATE residents SET contact=%s, email=%s WHERE flat_no=%s", (new_contact, new_email, flat))
    db.commit()
    print("Record updated!")

def delete_resident():
    flat = input("Enter flat no to delete: ")
    cur.execute("DELETE FROM residents WHERE flat_no=%s", (flat,))
    db.commit()
    print("Record deleted!")

def search_resident():
    flat = input("Enter flat no to search: ")
    cur.execute("SELECT * FROM residents WHERE flat_no=%s", (flat,))
    result = cur.fetchall()
    if result:
        for r in result:
            format_output(r)
        write_search_report(result, SEARCH_TXT)
    else:
        print("No record found.")

def view_residents():
    print("Residents from MySQL:")
    cur.execute("SELECT * FROM residents")
    rows = cur.fetchall()
    for row in rows:
        format_output(row)

def record_payment():
    flat = input("Enter flat no: ")
    month = input("Enter month (e.g., Jan-2025): ")
    amount = input("Enter amount: ")
    if not amount.isdigit():
        print("Invalid amount!")
        return

    cur.execute("INSERT INTO payments VALUES (%s, %s, %s, %s)", (flat, month, int(amount), date.today()))
    db.commit()

    with open(PAYMENTS_CSV, "a", newline="") as f:
        csv.writer(f).writerow([flat, month, amount, date.today()])

    with open(PAYMENTS_BIN, "ab") as f:
        pickle.dump([flat, month, amount, date.today()], f)

    print("Payment recorded!")

def show_dues():
    month = input("Enter month to check dues: ")
    cur.execute("SELECT flat_no, name FROM residents WHERE flat_no NOT IN (SELECT flat_no FROM payments WHERE month=%s)", (month,))
    dues = cur.fetchall()
    if dues:
        print("Residents with pending dues:")
        for d in dues:
            print(d)
        write_due_report(dues, DUES_TXT)
    else:
        print("No dues for this month.")

def import_from_backup():
    try:
        with open(RESIDENTS_CSV, "r") as f:
            reader = csv.reader(f)
            for flat, name, contact, email in reader:
                cur.execute("INSERT IGNORE INTO residents VALUES (%s, %s, %s, %s)", (flat, name, contact, email))

        with open(PAYMENTS_CSV, "r") as f:
            reader = csv.reader(f)
            for flat, month, amt, pay_date in reader:
                cur.execute("INSERT IGNORE INTO payments VALUES (%s, %s, %s, %s)", (flat, month, amt, pay_date))

        db.commit()
        print("Database restored from backups.")
    except FileNotFoundError:
        print("Backup files not found.")

# ----------------- MIS / Reports -----------------
def cleared_payments():
    month = input("Enter month: ")
    cur.execute("SELECT flat_no, name FROM residents WHERE flat_no IN (SELECT flat_no FROM payments WHERE month=%s)", (month,))
    rows = cur.fetchall()
    if rows:
        print("Residents who cleared payments:")
        for r in rows:
            print(r)
    else:
        print("No records found.")

def pending_dues():
    show_dues()

def total_collection():
    month = input("Enter month: ")
    cur.execute("SELECT SUM(amount) FROM payments WHERE month=%s", (month,))
    total = cur.fetchone()[0]
    print("Total collection for", month, "=", total if total else 0)

def flat_wise_history():
    flat = input("Enter flat no: ")
    cur.execute("SELECT * FROM payments WHERE flat_no=%s", (flat,))
    rows = cur.fetchall()
    if rows:
        for r in rows:
            format_output(r)
    else:
        print("No payment history for this flat.")

# ----------------- Menu -----------------
while True:
    print("\n--- Society Maintenance Management ---")
    print("1. Add Resident")
    print("2. Update Resident")
    print("3. Delete Resident")
    print("4. Search Resident")
    print("5. View Residents")
    print("6. Record Payment")
    print("7. Show Dues")
    print("8. Import from Backup")
    print("9. Cleared Payments")
    print("10. Pending Dues")
    print("11. Total Collection for Month")
    print("12. Flat-wise Payment History")
    print("13. Exit")
    ch = input("Enter choice: ")

    if ch == "1":
        add_resident()
    elif ch == "2":
        update_resident()
    elif ch == "3":
        delete_resident()
    elif ch == "4":
        search_resident()
    elif ch == "5":
        view_residents()
    elif ch == "6":
        record_payment()
    elif ch == "7":
        show_dues()
    elif ch == "8":
        import_from_backup()
    elif ch == "9":
        cleared_payments()
    elif ch == "10":
        pending_dues()
    elif ch == "11":
        total_collection()
    elif ch == "12":
        flat_wise_history()
    elif ch == "13":
        break
    else:
        print("Invalid choice.")
