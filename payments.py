from db import cur, db
import csv,pickle
from datetime import date
from utils import format_output 
from reports import write_due_report

PAYMENTS_CSV = "payments_backup.csv"
PAYMENTS_BIN = "payments.dat"
DUES_TXT = "dues.txt"

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
