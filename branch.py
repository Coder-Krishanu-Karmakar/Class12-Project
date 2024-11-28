import mysql.connector as conn
import random
import datetime

db = conn.connect(host="localhost", user="root", password="tiger", autocommit=True, database="guess_the_number")

cursor = db.cursor()

'''
SUBFUNCTIONS OF THE Game's Branch START HERE
'''

def game_loop(username):

    number_to_guess = random.randint(1, 100)

    chances = 10

    print(f"Welcome {username} to the Guess the Number game!")
    print("I'm thinking of a number between 1 and 100. You have 10 chances to guess it.")

    while chances > 0:
        guess = int(input("Enter your guess: "))
        
        if guess < number_to_guess - 30:
            print("Your number is very small. Try again.")
        elif guess > number_to_guess + 30:
            print("Your number is very large. Try again.")
        elif guess < number_to_guess - 20:
            print("Your number is small. Try again.")
        elif guess > number_to_guess + 20:
            print("Your number is large. Try again.")
        elif guess < number_to_guess:
            print("Your number is a little small. Try again.")
        elif guess > number_to_guess:
            print("Your number is a little large. Try again.")
        else:
            print(f"Congratulations, {username}! You guessed the number correctly.")
            score = chances
            break
        
        chances -= 1

    else:
        print(f"Sorry, {username}. You ran out of chances. The number was {number_to_guess}")
        score = 0
    
    print(f"Your final score is: {score}")
    cursor.execute("INSERT INTO scores VALUES (%s, %s, %s)", (username, score, datetime.datetime.now().strftime('%Y-%m-%d')))
    

def score(username):
    cursor.execute("SELECT score,date FROM scores WHERE username = %s", (username,))
    scores = cursor.fetchall()
    for i in scores:
        print(f"{i[0]} points achieved on {i[-1]}")

def highscore(username):

    cursor.execute("SELECT score,date FROM scores WHERE username = %s", (username,))
    highscore = cursor.fetchall()
    x = (max(highscore))

    print(f"Your highscore is {x[0]} on {x[1]}")

def clear_score(username):
    cursor.execute("DELETE FROM scores WHERE username = %s", (username,))
    print("Your score is cleared.")

def delete_account(username):
    cursor.execute("DELETE FROM scores WHERE username = %s", (username,))
    cursor.execute("DELETE FROM users WHERE username = %s", (username,))
    print("Your account is deleted.")

def ChangeUsernamePassword(username):
    while True:
        newUsername = input("Enter a new Username: ")
        cursor.execute("select username from users where username = %s", (newUsername,)) 
        if (cursor.fetchall() == []) and (not (newUsername.isspace() or newUsername=="")):
            break
        else:
            print("Invalid Username or Username already exists....")
            continue
    while True:
        newPassword = input("Enter a new Password")
        if newPassword == "" or newPassword.isspace():
            print("Enter a valid password...")
        else:
            break

    cursor.execute("update users set username = %s, password = %s where username = %s", (newUsername,newPassword,username))
    cursor.execute("update scores set username = %s where username = %s", (newUsername,username))
    

'''
SUBFUNCTIONS OF THE MAIN END HERE
'''

def main(username):
    while True:
        print("""
        Commands -->
        1 - Start the game
        2 - Show the score
        3 - Show the highscore
        4 - Clear the score
        5 - Delete the account
        6 - Change Username and Password
        7 - Exit the game
        """)

        ui = input("Enter your command: ")

        if ui == "1":
            game_loop(username)
        elif ui == "2":
            score(username)
        elif ui == "3":
            highscore(username)
        elif ui == "4":
            clear_score(username)
        elif ui == "5":
            delete_account(username)
            break
        elif ui == '6':
            ChangeUsernamePassword(username)
            print("Data changed, kindly sign in again....")
            break
        elif ui == "7":
            print("You are exiting the game.")
            break
        else:
            print("Invalid command.")
        
