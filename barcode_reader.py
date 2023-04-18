import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import requests
from bs4 import BeautifulSoup
import json
import sqlite3
from random import random
import string
import pandas as pd


# Define a function to capture video from your camera and process each frame
def scan_barcodes():
    cap = cv2.VideoCapture(0)  # 0 means the default camera on your device
    font = cv2.FONT_HERSHEY_PLAIN
    barcode_data = None  # Create a variable to store the decoded barcode data
    while barcode_data is None:  # Keep scanning until a barcode is successfully decoded
        _, frame = cap.read()  # Read each frame from the camera
        try:
            decoded_objects = pyzbar.decode(frame)  # Decode any barcodes in the frame
            for obj in decoded_objects:
                # Draw a rectangle around the barcode and display its data
                cv2.rectangle(frame, (obj.rect.left, obj.rect.top),
                              (obj.rect.left + obj.rect.width, obj.rect.top + obj.rect.height), (255, 0, 0), 2)
                cv2.putText(frame, str(obj.data.decode('utf-8')), (obj.rect.left, obj.rect.top), font, 2,
                            (255, 255, 255),
                            2, cv2.LINE_AA)
                barcode_data = obj.data.decode('utf-8')  # Save the decoded data to the variable
            # Display the processed frame
            cv2.imshow("Barcode Scanner", frame)
            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except TypeError:
            return None
    cap.release()
    cv2.destroyAllWindows()
    return barcode_data  # Return the decoded barcode data`


# Call the function to start scanning barcodes and save the result to a variable
# barcode_result = scan_barcodes()
# print(barcode_result)   # Print the decoded barcode data

# Website to use for searching barcode values
def get_price(barcode_result):
    url = "https://api.barcodespider.com/v1/lookup"
    querystring = {"upc": barcode_result}

    headers = {
        'token': "d970f9f75b5fb1d6c3a5",
        'Host': "api.barcodespider.com",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()

    price = response.text

    data_dict = json.loads(price)
    try:
        # Extract the price from the dictionary
        price = data_dict['Stores'][0]['price']
        name = data_dict['item_attributes']['title']

        print(f"The name of item is {name} and the price is {price}")

        return price, name
    except KeyError:
        return None, None


def get_email(email):
    if '@' and '.' not in email:
        return True

    # create a connection to the database
    conn = sqlite3.connect('barcode_data.db')

    c = conn.cursor()
    c.execute('''SELECT email FROM users WHERE email=?''', (email,))
    try:
        result = c.fetchall()[0][0]
    except IndexError:
        return False

    result = result == email
    # Commit the table creation
    conn.commit()

    # Close the connection
    conn.close()

    return result


def get_name(userid):
    # create a connection to the database
    conn = sqlite3.connect('barcode_data.db')

    c = conn.cursor()
    c.execute('''SELECT firstname, lastname FROM users WHERE userid=?''', (userid,))
    result = c.fetchall()[0]

    # Commit the table creation
    conn.commit()

    # Close the connection
    conn.close()

    return result[0], result[1]


def create_database():
    # Prompt the user for a database name
    dbname = 'barcode_data'

    # Create a connection to the database
    conn = sqlite3.connect(dbname + ".db")

    # Create a cursor object
    cursor = conn.cursor()

    # Create a table with three columns
    cursor.execute('''CREATE TABLE IF NOT EXISTS 'products'
                      (UPC TEXT,
                       Name TEXT,
                       Price REAL,
                       Category TEXT, 
                       UserID TEXT,  
                       FOREIGN KEY (UserID) REFERENCES users(userid))''')

    # Commit the table creation
    conn.commit()

    # Close the connection
    conn.close()

    print(
        f"Database {dbname}.db created with table 'products' containing columns 'UPC', 'Name', 'Price', 'UserID' and "
        f"'Category'.")


# create_database()


def update_database(name, barcode, price, category, userid):
    conn = sqlite3.connect("barcode_data.db")

    cursor = conn.cursor()

    cursor.execute('''INSERT INTO 'products' (UPC, Name, Price, Category, UserID) VALUES (?, ?, ?, ?,?)''',
                   (barcode, name, price, category.strip(), userid))
    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()


# update_database(sql_name,name, barcode_result, price)
def get_products(userid, category):
    conn = sqlite3.connect("barcode_data.db")
    c = conn.cursor()
    c.execute('''SELECT UPC, Name, Price FROM products WHERE UserID=? AND Category=?''', (userid, category))
    results = c.fetchall()
    return results


def checking(barcode, userid, category):
    conn = sqlite3.connect("barcode_data.db")

    cursor = conn.cursor()
    # Check if specific barcode exists in similar category for specific user
    cursor.execute('''SELECT UPC, Category FROM products WHERE (USERID=? AND UPC=? AND Category=?)''',
                   (userid, barcode, category))
    result = cursor.fetchone()
    # Insert data into the table
    conn.close()
    if result:
        return True
    else:
        return False


def get_unique_categories(userid):
    conn = sqlite3.connect('barcode_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT Category FROM products WHERE UserID=?", (userid,))
    result = cursor.fetchall()
    conn.close()
    categories = [r[0] for r in result]
    return categories


def create_user_database():
    # Prompt the user for a database name
    dbname = 'barcode_data'

    # Create a connection to the database
    conn = sqlite3.connect(dbname + ".db")

    # Create a cursor object
    cursor = conn.cursor()

    # Create a table with three columns
    cursor.execute('''CREATE TABLE IF NOT EXISTS 'users'
                   (username TEXT PRIMARY KEY, 
                    password TEXT,
                    firstname TEXT,
                    lastname TEXT,
                    email TEXT UNIQUE , 
                    userid TEXT UNIQUE)''')

    # Commit the table creation
    conn.commit()

    # Close the connection
    conn.close()

    print(
        f"Database {dbname}.db created with table 'users' containing columns 'username' and 'password'")


def add_user(username, password, first_name, last_name, email):
    # create a connection to the database
    conn = sqlite3.connect('barcode_data.db')
    result = True
    # create a cursor object
    c = conn.cursor()
    while result:
        userid = str(random())
        c.execute('''SELECT userid FROM users WHERE userid=?''', (userid,))
        result = c.fetchone()
    if not get_email(email) and verify_password(password):

        # insert the new user into the users table
        c.execute(
            '''INSERT INTO users (username, password, firstname, lastname, email, userid) VALUES (?, ?,?,?,?, ?)''',
            (username, password, first_name, last_name, email, userid))

        # commit changes to the database and close the connection
        conn.commit()
        conn.close()
        return userid
    else:
        return ''


def get_password(username, email):
    # create a connection to the database
    conn = sqlite3.connect('barcode_data.db')

    c = conn.cursor()
    c.execute('''SELECT username, email FROM users WHERE username=? AND email=?''', (username, email))
    result = c.fetchall()
    if result:
        username_result = (result[0][0] == username)
        email_result = (result[0][1] == email)
        c.execute('''SELECT password FROM users WHERE username=? AND email=?''', (username, email))
        result = c.fetchall()[0][0]

        # Commit the table creation
        conn.commit()

        # Close the connection
        conn.close()

        return username_result, email_result, result

    return False, False, ''


def get_username(firstname, lastname, email):
    # create a connection to the database
    conn = sqlite3.connect('barcode_data.db')

    c = conn.cursor()
    c.execute('''SELECT firstname ,lastname, email FROM users WHERE firstname=? AND lastname=? AND email=?''',
              (firstname, lastname, email))
    result = c.fetchall()
    if result:
        firstname_result = (result[0][0] == firstname)
        lastname_result = (result[0][1] == lastname)
        email_result = (result[0][2] == email)
        c.execute('''SELECT username FROM users WHERE firstname=? AND lastname=? AND email=?''',
                  (firstname, lastname, email))
        result = c.fetchall()[0][0]

        # Commit the table creation
        conn.commit()

        # Close the connection
        conn.close()

        return firstname_result, lastname_result, email_result, result

    return False, False, False, ''


def login(username, password):
    # create a connection to the database
    conn = sqlite3.connect('barcode_data.db')

    c = conn.cursor()
    c.execute('''SELECT username, password FROM users WHERE username=?''', (username,))
    result = c.fetchall()
    if result:
        username_result = (result[0][0] == username)
        password_result = (result[0][1] == password)
        c.execute('''SELECT userid FROM users WHERE username=?''', (username,))
        result = c.fetchall()[0][0]

        # Commit the table creation
        conn.commit()

        # Close the connection
        conn.close()

        return username_result, password_result, result

    # Commit the table creation
    conn.commit()

    # Close the connection
    conn.close()
    return False, False, 0


def verify_password(password):
    # Check if the password includes an uppercase letter
    upper_result = False
    number_result = False
    length_result = False
    special_result = False
    if len(password) > 12:
        length_result = True

    for x in password:
        if x.isupper():
            upper_result = True
        if x.isdigit():
            number_result = True
        if x in string.punctuation:
            special_result = True

    if not (special_result and number_result and upper_result and length_result):
        return False
    else:
        return True


def verify_username(username):
    # create a connection to the database
    conn = sqlite3.connect('barcode_data.db')

    c = conn.cursor()
    c.execute('''SELECT username FROM users WHERE username=?''', (username,))

    try:
        result = c.fetchall()[0][0]
    except IndexError:
        return False

    result = result == username

    # Commit the table creation
    conn.commit()

    # Close the connection
    conn.close()

    return result


def Print_most_expensive():
    conn = sqlite3.connect("barcode_data.db")

    cursor = conn.cursor()

    result = cursor.fetchall()
    sql_query = pd.read_sql_query ('''
                                    SELECT
                                    *
                                    FROM products
                                    ''', conn)

    df = pd.DataFrame(sql_query)
    hi = df.sort_values(by=['Price'])
    print( hi['Price'].iloc[-1])
 
   
def Print_least_expensive():
    conn = sqlite3.connect("barcode_data.db")

    cursor = conn.cursor()

    result = cursor.fetchall()
    sql_query = pd.read_sql_query ('''
                                    SELECT
                                    *
                                    FROM products
                                    ''', conn)

    df = pd.DataFrame(sql_query)
    hi = df.sort_values(by=['Price'])
    print( hi['Price'].iloc[0])



if __name__ == "__main__":
    create_user_database()
    create_database()
    print(get_email(''))


#Bigsemour678 or BigSemour678
#Ryannaraine07!