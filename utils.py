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


