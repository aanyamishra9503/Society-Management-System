# Society-Management-System
A Python-based Society Maintenance Management System that helps manage residents, track maintenance payments, and generate reports efficiently using a MySQL database.\n

Features\n
🔷Admin Authentication:\n
Secure login using hashed passwords (SHA-256)
🔷Resident Management (CRUD):\n
Add, update, delete, and search resident records
Store flat number, name, contact, and email
🔷Payment Tracking:\n
Record monthly maintenance payments
Prevent duplicate entries using unique constraints
🔷Reports Generation:\n
Generate dues report (pending payments)
Export search results and dues to CSV files
🔷Analytics:\n
Monthly total collection
Flat-wise payment history\n

🛠Tech Stack
Python
MySQL
mysql-connector
CSV (for report generation)
hashlib (for password security)
