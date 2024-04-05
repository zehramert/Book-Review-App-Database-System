from tkinter import*
import mysql.connector 
from tkinter import messagebox


#connection initializer
def initialize_connection():
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "737123eeE." )
    

    cursor = conn.cursor()  #allows you to send sql queries
    cursor.execute("USE DBMS") #choose the table you want


    return conn, cursor



def login(cursor,data):
    cursor.execute(f"""SELECT * FROM User WHERE username = '{data["username"]}' 
                       AND password_ = '{data["password_"]}' """)
    user = cursor.fetchone()
    if user:
        user_data = {

            "username": user[0],
            "first_name": user[1],
            "last_name": user[2],
            "bio": user[3],
            "goal_book_num": user[4],
            "email": user[5],
            "following_num": user[6],
            "gender": user[7],
            "past_read_num": user[8],
            "follower_num": user[9],
            "password_": user[10],
            "date_created": user[11],
        }
        return user_data
    else:
        return None


def get_user_information(cursor, conn, username):
    cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
    user_data = cursor.fetchone()

    if user_data:
        print(user_data)  # Add this line to see the structure of the user_data tuple
        user_information = {
            "username": user_data["username"],
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
            "bio": user_data["bio"],
            "goal_book_num": user_data["goal_book_num"],
            "past_read_num": user_data["past_read_num"],
            "following_num": user_data["following_num"],
            "follower_num": user_data["follower_num"]  
        }
        return user_information
    else:
        return {}

# Add this function to your database.py
def get_user_information2(cursor, conn, username):
    cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
    user_data = cursor.fetchone()

    if user_data:
        user_information = {
            "username": user_data[0],
            "first_name": user_data[1],
            "last_name": user_data[2],
            "bio": user_data[3],
            "goal_book_num": user_data[4],
            "email": user_data[5],
            "following_num": user_data[6],  # Add following_num
            "password": user_data[10],  # Add following_num
            "date_created": user_data[11],  # Add following_num

            "gender": user_data[7],
            "goal_book_num": user_data[4],
            "past_read_num": user_data[8],
            "follower_num": user_data[9]  
        }
        return user_information
    else:
        return {}
def update_bio(cursor, conn, data, new_bio):
    username = data["username"]

    cursor.execute("UPDATE User SET bio = %s WHERE username = %s", (new_bio, data["username"]))
    conn.commit()

def update_goal(cursor,conn, data, new_goal):
    cursor.execute("UPDATE User SET goal_book_num = %s WHERE username = %s", (new_goal, data["username"]))
    conn.commit()

def update_past_reads(cursor, conn, data, new_past_reads):
    cursor.execute("UPDATE User SET past_read_num = %s WHERE username = %s", (new_past_reads, data["username"]))
    conn.commit()



def create_post(cursor, conn, username, post_title, post_text):
    cursor.execute("INSERT INTO Post (post_title,username,post_content) VALUES (%s, %s, %s)",
                   ( post_title,username, post_text))
    conn.commit()



def get_recent_posts(cursor, conn):
    cursor.execute("SELECT username, post_title, post_content FROM Post ORDER BY postcreate_date DESC LIMIT 10")
    posts = cursor.fetchall()

    return posts


def get_post_id_from_text(cursor, conn, post_text):
    cursor.execute(f"SELECT post_id FROM Post WHERE post_title = '{post_text}'")
    post_id = cursor.fetchone()
    if post_id:
        return post_id[0]
    else:
        return None


def login(cursor,data):
    cursor.execute(f"""SELECT * FROM User WHERE username = '{data["username"]}' 
                       AND password_ = '{data["password_"]}' """)
    user = cursor.fetchone()
    if user:
        user_data = {
            "username": user[0],
            "first_name": user[1],
            "last_name": user[2],
            "bio": user[3],
            "goal_book_num": user[4],
            "email": user[5],
            "following_num": user[6],
            "gender": user[7],
            "past_read_num": user[8],
            "follower_num": user[9],
            "password_": user[10],
            "date_created": user[11],
        }
        return user_data
    else:
        return None
def register(cursor,conn, data):
    data.setdefault('bio', '')

    print(data)

    cursor.execute(f"""INSERT INTO User(username,first_name,last_name,bio,email,gender,password_) VALUES( 

                   '{data["username"]}',
                   '{data["first_name"]}',
                   '{data["last_name"]}',
                   '{data["bio"]}',

                   '{data["email"]}',
                   '{data["gender"]}',
                   '{data["password_"]}'
                   

    )""")

    conn.commit()
    login(cursor,data)

    return login(cursor,data)
def update_bio(cursor, conn, data, new_bio):
    cursor.execute("UPDATE User SET bio = %s WHERE username = %s", (new_bio, data["username"]))
    conn.commit()

def update_goal(cursor,conn, data, new_goal):
    cursor.execute("UPDATE User SET goal_book_num = %s WHERE username = %s", (new_goal, data["username"]))
    conn.commit()

def update_past_reads(cursor, conn, data, new_past_reads):
    cursor.execute("UPDATE User SET past_read_num = %s WHERE username = %s", (new_past_reads, data["username"]))
    conn.commit()





def create_post(cursor, conn, username, post_title, post_text):
    cursor.execute("INSERT INTO Post (post_title, username, post_content) VALUES (%s, %s, %s)", (post_title, username, post_text))
    conn.commit()

# Modify the get_recent_posts method in database.py
def get_recent_posts(cursor, conn):
    cursor.execute("SELECT username, post_title,post_content FROM Post ORDER BY postcreate_date DESC LIMIT 50")
    posts = cursor.fetchall()
    return posts


def get_post_id_from_text(cursor, conn, post_title):
    cursor.execute(f"SELECT post_id FROM Post WHERE post_title = '{post_title}'")
    post_id = cursor.fetchone()
    if post_id:
        return post_id[0]
    else:
        return None



    conn.commit()
def has_liked(cursor, conn, username, post_id):
    cursor.execute("SELECT * FROM Likes WHERE username = %s AND post_id = %s", (username, post_id))
    return cursor.fetchone() is not None


def like_post(cursor, conn, username, post_id):
    if post_id is not None:
        # Insert a new like
        cursor.execute("INSERT INTO Likes (username, post_id) VALUES (%s, %s)", (username, post_id))
        conn.commit()

        # Update the like count in the Post table
        update_post_like_count(cursor, conn, post_id)
    else:
        messagebox.showerror("Error", "Invalid post selected.")

# Add a new function update_post_like_count in database.py
def update_post_like_count(cursor, conn, post_id):
    # Get the current like count for the post
    cursor.execute("SELECT COUNT(*) FROM Likes WHERE post_id = %s", (post_id,))
    like_count = cursor.fetchone()[0]

    # Update the Post table with the new like count
    cursor.execute("UPDATE Post SET like_num = %s WHERE post_id = %s", (like_count, post_id))
    conn.commit()

# Add a new function get_like_count to database.py
def get_like_count(cursor, conn, post_id):
    cursor.execute("SELECT COUNT(*) FROM Likes WHERE post_id = %s", (post_id,))
    like_count = cursor.fetchone()[0]
    return like_count

def add_comment(cursor, conn, username, post_id, comment_content):
    cursor.execute(
        "INSERT INTO Comments (user_name, post_id, comment_content) VALUES (%s, %s, %s)",
        (username, post_id, comment_content)
    )
    conn.commit()


# database.py

def get_comments(cursor, conn, post_id):


    cursor.execute("SELECT user_name, comment_content FROM comments WHERE post_id = %s", (post_id,))
    comments = cursor.fetchall()
    return comments
# follow_user fonksiyonunu güncelle
def follow_user(cursor, conn, follower_username, followed_username):
    sql = "INSERT INTO Follow (follower_username, followed_username) VALUES (%s, %s)"
    cursor.execute(sql, (follower_username, followed_username))

    # Artırılan takip edilen sayısını güncelle
    update_follow_stats(cursor, conn, followed_username)

    conn.commit()

# unfollow_user fonksiyonunu güncelle
def unfollow_user(cursor, conn, follower_username, followed_username):
    sql = "DELETE FROM Follow WHERE follower_username = %s AND followed_username = %s"
    cursor.execute(sql, (follower_username, followed_username))

    # Azaltılan takip edilen sayısını güncelle
    update_follow_stats(cursor, conn, followed_username)
    conn.commit()

def get_following_count(cursor, conn, username):
    sql = "SELECT COUNT(*) FROM Follow WHERE follower_username = %s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()
    return result[0] if result else 0

def get_follower_count(cursor, conn, username):
    sql = "SELECT COUNT(*) FROM Follow WHERE followed_username = %s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()
    return result[0] if result else 0

def update_follow_stats(cursor, conn, username):
    # Takip edilen sayısını al
    following_num = get_following_count(cursor, conn, username)
    # Takipçi sayısını al
    follower_num = get_follower_count(cursor, conn, username)

    # Güncelleme sorgusunu çalıştır
    sql = "UPDATE User SET following_num = %s, follower_num = %s WHERE username = %s"
    cursor.execute(sql, (following_num, follower_num, username))

    conn.commit()





