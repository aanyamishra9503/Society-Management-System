from residents import add_resident, update_resident, delete_resident, search_resident, view_residents
from payments import record_payment, show_dues, cleared_payments, total_collection, flat_wise_history, import_from_backup, pending_dues


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
