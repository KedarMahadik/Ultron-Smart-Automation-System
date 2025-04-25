import csv
import sqlite3
 
con = sqlite3.connect("ultron.db")
cursor = con.cursor()

#query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
#cursor.execute(query)

# query = "INSERT INTO sys_command VALUES (null,'notepad', 'C:\\Windows\\notepad.exe')"
# cursor.execute(query)
# con.commit()

# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO web_command VALUES (null,'google', 'https://web.google.com/')"
# cursor.execute(query)
# con.commit()


# testing module
# app_name = "android studio"
# cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
# results = cursor.fetchall()
# print(results[0][0])

# Create a table with the desired columns
#cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')


# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
# desired_columns_indices = [0, 1]

# # # Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# # Commit changes and close connection
# con.commit()
# con.close()

# query = 'kunal'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# print(results[0][0])

# cursor.execute("DELETE FROM web_command WHERE id = ?", (4,))
# con.commit()



# --------------------contacts -------------------


# query = "INSERT INTO contacts VALUES (9,'Disha', '7447416575', 'dishagawade692@gmail.com')"
# cursor.execute(query)
# con.commit()


# cursor.execute("DELETE FROM contacts WHERE id = ?", (8,))
# con.commit()

# --------------------web_commmand -------------------

# query = "INSERT INTO web_command VALUES (null,'gmail', 'https://mail.google.com/mail/u/0/#inbox?compose=new')"
# cursor.execute(query)
# con.commit()


# cursor.execute("DELETE FROM web_command WHERE id = ?", (3,))
# con.commit()

# --------------------sys_commmand -------------------

# query = "INSERT INTO sys_command VALUES (null,'telegram', 'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Word 2016.ink')"
# cursor.execute(query)
# con.commit()


# cursor.execute("DELETE FROM sys_command WHERE id = ?", (3,))
# con.commit()