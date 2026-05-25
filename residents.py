from db import cur, db
from utils import validate_flat, format_output
from reports import write_search_report
import csv,pickle 

RESIDENTS_CSV = "residents_backup.csv"
RESIDENTS_BIN = "residents.dat"
SEARCH_TXT = "search.txt"


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
    new_contact = input("Enter new contact (enter original if no change): ")
    new_email = input("Enter new email (enter original if no change): ")
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
