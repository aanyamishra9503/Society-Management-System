import mysql.connector as sql

db = sql.connect(host="localhost", user="root", password="yourpass", database="society")
cur = db.cursor()

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
print("Database connected and tables ready.")