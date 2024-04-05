import tkinter as tk
from tkinter import messagebox
import mysql.connector

from database import *
from homepage import HomePage


DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "737123eeE."
DB_NAME = "DBMS"
conn, cursor = initialize_connection()



class WriterProfileViewer:
    def __init__(self, root, user_data):
        self.root = root
        self.user_data = user_data  # Store user_data as an attribute

        # ... rest of the __init__ method

        # Pass user_data to WriterProfileViewer instance when creating it


        self.root.title("Writer Profile Viewer")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)

        self.label_w_first_name = tk.Label(self.main_frame, text="Writer's Name:")
        self.label_w_first_name.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

        self.entry_w_first_name = tk.Entry(self.main_frame)
        self.entry_w_first_name.grid(row=0, column=1, padx=5, pady=5)

        self.label_w_last_name = tk.Label(self.main_frame, text="Writer's Last Name:")
        self.label_w_last_name.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

        self.entry_w_last_name = tk.Entry(self.main_frame)
        self.entry_w_last_name.grid(row=1, column=1, padx=5, pady=5)

        self.show_profile_button = tk.Button(self.main_frame, text="Show Profile", command=self.show_writer_profile)
        self.show_profile_button.grid(row=2, column=0, columnspan=2, pady=10)


        self.homepage_button = tk.Button(self.main_frame, text="Homepage", command=self.go_to_home_page)
        self.homepage_button.grid(row=3, column=0, columnspan=2, pady=10)

    def go_to_home_page(self):
        self.root.destroy()  # Destroy the BookProfileViewer window
        root = tk.Tk()  # Create a new root window for the HomePage
        root.title("Home Page")
        root.geometry("1250x1000")
        HomePage(root, self.user_data)

    def show_writer_profile(self):
        w_first_name = self.entry_w_first_name.get()
        w_last_name = self.entry_w_last_name.get()

        if not w_first_name or not w_last_name:
            messagebox.showerror("ERROR", "Please enter a valid name.")
            return

        writer_data = self.fetch_writer_data(w_first_name, w_last_name)

        if writer_data:
            self.show_profile_window(writer_data)
        else:
            messagebox.showinfo("Info", "Writer couldn't be found.")

    def fetch_writer_data(self, w_first_name, w_last_name):
        db_connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = db_connection.cursor(dictionary=True)
        query = f"SELECT * FROM Writer WHERE w_first_name = '{w_first_name}' AND w_last_name = '{w_last_name}'"
        cursor.execute(query)
        writer_data = cursor.fetchone()

        cursor.close()
        db_connection.close()

        print("Query:", query)
        print("Writer Data:", writer_data)

        return writer_data

    def show_profile_window(self, writer_data):
        profile_window = tk.Toplevel(self.root)

        profile_window.title(f"{writer_data['w_first_name']} {writer_data['w_last_name']}'s Profile")

        profile_frame = tk.Frame(profile_window)
        profile_frame.pack(padx=20, pady=20)

        label_w_username = tk.Label(profile_frame, text=f"Username: {writer_data['w_username']}")
        label_w_username.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        label_w_firstname = tk.Label(profile_frame, text=f"Name: {writer_data['w_first_name']}")
        label_w_firstname.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        label_w_lastname = tk.Label(profile_frame, text=f"Surname: {writer_data['w_last_name']}")
        label_w_lastname.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        label_bio = tk.Label(profile_frame, text=f"Bio: {writer_data['w_bio']}")
        label_bio.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

        label_likes = tk.Label(profile_frame, text=f"Likes: {writer_data['num_of_likes']}")
        label_likes.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

        label_books = tk.Label(profile_frame, text=f"Books: {writer_data['book_num']}")
        label_books.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)

        label_followers = tk.Label(profile_frame, text=f"Followers: {writer_data['follower_num']}")
        label_followers.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)

        label_num_of_reads = tk.Label(profile_frame, text=f"Readers: {writer_data['num_of_reads']}")
        label_num_of_reads.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)

        rate = writer_data.get('rate', float('0.00'))
        self.label_rates = tk.Label(profile_frame, text=f"Rates: {rate}")
        self.label_rates.grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)

        like_button = tk.Button(profile_frame, text="Like", command=lambda: self.like_writer(writer_data, label_likes))
        like_button.grid(row=9, column=0, padx=5, pady=5)

        follow_button = tk.Button(profile_frame, text="Follow", command=lambda: self.follow_writer(writer_data, label_followers))
        follow_button.grid(row=9, column=1, padx=5, pady=5)

        rate_button = tk.Button(profile_frame, text="Rate", command=lambda: self.show_rate_window(writer_data))
        rate_button.grid(row=9, column=2, padx=5, pady=5)

    def like_writer(self, writer_data, label_likes):
            db_connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            cursor = db_connection.cursor(dictionary=True)

            # Increment the like count and update the label
            writer_data['num_of_likes'] += 1
            label_likes.config(text=f"Likes: {writer_data['num_of_likes']}")
            
            # Update writer data in the database
            self.update_writer_data(writer_data)


            user_username = self.user_data.get("username")
            w_username = writer_data.get('w_username')

            # Insert like information into the database
            query_insert_rating = "INSERT INTO like_writer (username, w_username) VALUES (%s, %s)"
            cursor.execute(query_insert_rating, (user_username, w_username))

            
            db_connection.commit()
            cursor.close()
            db_connection.close()

    def follow_writer(self, writer_data, label_followers):
        writer_data['follower_num'] += 1
        label_followers.config(text=f"Followers: {writer_data['follower_num']}")
        self.update_writer_data(writer_data)

    def show_rate_window(self, writer_data):
        rate_window = tk.Toplevel(self.root)
        rate_window.title("Rate Writer")

        rate_frame = tk.Frame(rate_window)
        rate_frame.pack(padx=20, pady=20)

        self.label_rate_entry = tk.Label(rate_frame, text="Rate (1-5):")
        self.label_rate_entry.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

        self.entry_rate = tk.Entry(rate_frame)
        self.entry_rate.grid(row=0, column=1, padx=5, pady=5)

        submit_rate_button = tk.Button(rate_frame, text="Submit Rate", command=lambda: self.submit_rate(writer_data))
        submit_rate_button.grid(row=1, column=0, columnspan=2, pady=10)

    def submit_rate(self, writer_data):
        rate_value = self.entry_rate.get()
        if rate_value is not None:
            w_username=writer_data.get('w_username')
            writer_data = self.fetch_writer_data(writer_data['w_first_name'], writer_data['w_last_name'])
            current_average_rating = float(writer_data['rate'])
            rate_value = float(rate_value)

            num_of_ratings = int(writer_data.get('num_of_ratings', 0))  # Convert to int

            new_average_rating = ((current_average_rating * num_of_ratings) + rate_value) / (num_of_ratings + 1)
            num_of_ratings += 1

            self.update_rate(w_username, new_average_rating, num_of_ratings, rate_value)
            messagebox.showinfo("Info", "Rate submitted successfully.")

            # Update the label_rates in the show_profile_window after successful rate submission
            self.label_rates.config(text=f"Rates: {new_average_rating:.2f}")

    def update_rate(self,w_username, new_average_rating, num_of_ratings, rating ):
        db_connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = db_connection.cursor(dictionary=True)

         # Update the rate and num_of_ratings
        query = f"UPDATE Writer SET rate = {new_average_rating}, num_of_ratings = {num_of_ratings} WHERE w_username = '{w_username}'"
        cursor.execute(query)


        
        # Insert the rating into the rates table using parameterized query
        username = get_user_information(cursor, conn, self.user_data["username"])
        query_insert_rating = "INSERT INTO rates (w_username, rate_value, username) VALUES (%s, %s, %s)"
        cursor.execute(query_insert_rating, (w_username, rating, username["username"]))



        db_connection.commit()

        cursor.close()
        db_connection.close()

    def update_writer_data(self, writer_data):
        db_connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = db_connection.cursor(dictionary=True)
        
        # Update the follow_writer
        w_username = writer_data.get('w_username')
        username = get_user_information(cursor, conn, self.user_data["username"])

        query_insert_follow = "INSERT INTO follow_writer (w_username, username) VALUES (%s, %s)"
        cursor.execute(query_insert_follow, (w_username, username["username"]))


        # Update the number of likes
        query = f"UPDATE Writer SET num_of_likes = num_of_likes + 1 WHERE w_username = '{writer_data['w_username']}'"
        cursor.execute(query)

        
        query = f"UPDATE Writer SET num_of_likes = {writer_data['num_of_likes']}, follower_num = {writer_data['follower_num']} WHERE w_username = '{writer_data['w_username']}'"
        cursor.execute(query)
        db_connection.commit()

        cursor.close()
        db_connection.close()




if __name__ == "__main__":
    root = tk.Tk()
    root.title("1000Kitap-Home")
    root.geometry("800x600")



    root.mainloop()