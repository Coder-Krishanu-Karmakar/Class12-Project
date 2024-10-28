import os
import mysql.connector as conn

db = conn.connect(host="localhost", user="root", password="tiger", autocommit=True)
cursor = db.cursor()


def checkDatabase():
    cursor.execute("SHOW DATABASES")
    a = cursor.fetchall()
    if ("guess_the_number",) not in a:
        cursor.execute("CREATE DATABASE guess_the_number")
        cursor.execute("USE guess_the_number")
        cursor.execute("CREATE TABLE users(username char(50) PRIMARY KEY NOT NULL, password char(50) NOT NULL)")
        cursor.execute("CREATE TABLE scores(username char(50) , score int, date DATE, foreign key(username) references users(username))")

checkDatabase()
cursor.execute("USE guess_the_number")

def signUp():
    username = input("Enter username: ")
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    if result:
        print("Username already exists. Please choose a different username.")
        return False
    password = input("Enter password: ")


    cursor.execute("INSERT INTO users VALUES (%s, %s)", (username, password))

    print("Account created successfully")
    return True

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    result = cursor.fetchone()
    if result:
        print("Login successful")
        import branch
        branch.main(username)
        return True
    else:
        print("Invalid username or password")
        return False

while True:
    print('''
        Press 1 to create account
        Press 2 to login to an existing account
        Press 3 to exit
          ''')
    
    UI = input("Enter your choice: ")
    if UI == "1":
        while True:
            r = signUp()
            if r:
                break

    elif UI == "2":
        while True:
            r = login()
            if r:
                break
    elif UI == "3":
        print("Exited")
        break
    else:
        print("Invalid input")
