DUES_TXT = "dues.txt"
SEARCH_TXT = "search.txt"

def write_due_report(dues, filename=DUES_TXT):
    with open(filename, "w") as f:
        for d in dues:
            f.write(str(d) + "\n")
    print("Dues report generated as", filename)

def write_search_report(results, filename=SEARCH_TXT):
    with open(filename, "w") as f:
        for r in results:
            f.write(str(r) + "\n")
    print("Search report saved as", filename)