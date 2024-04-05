import tkinter as tk
from tkinter import simpledialog, messagebox
import mysql.connector
from database import *
from homepage import HomePage

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "737123eeE."
DB_NAME = "DBMS"

conn, cursor = initialize_connection()

class BookProfileViewer:
    def __init__(self, root,user_data):
        self.root = root
        self.user_data = user_data
        self.root.title("Book Viewer")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)

        self.label_book_name = tk.Label(self.main_frame, text="Book Name:")
        self.label_book_name.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

        self.entry_book_name = tk.Entry(self.main_frame)
        self.entry_book_name.grid(row=0, column=1, padx=5, pady=5)

        self.show_book_button = tk.Button(self.main_frame, text="Show Book", command=self.show_book)
        self.show_book_button.grid(row=2, column=0, columnspan=2, pady=10)


        self.homepage_button = tk.Button(self.main_frame, text="Homepage", command=self.go_to_home_page)
        self.homepage_button.grid(row=3, column=0, columnspan=2, pady=10)

    def go_to_home_page(self):
        self.root.destroy()  # Destroy the BookProfileViewer window
        root = tk.Tk()  # Create a new root window for the HomePage
        root.title("Home Page")
        root.geometry("1250x1000")
        HomePage(root, self.user_data)


    def show_book(self):
        book_name = self.entry_book_name.get()

        if not book_name:
            messagebox.showerror("ERROR", "Please enter a valid book name.")
            return

        book_data = self.fetch_book_data(book_name)

        if book_data:
            self.show_profile_window(book_data)
        else:
            messagebox.showinfo("Info", "Book couldn't be found.")

    def fetch_book_data(self, book_name):
        db_connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

        cursor = db_connection.cursor(dictionary=True)
        query = f"SELECT * FROM book WHERE book_name = '{book_name}'"
        cursor.execute(query)
        book_data = cursor.fetchone()

        cursor.close()
        db_connection.close()

        print("Query:", query)
        print("Book Data:", book_data)

        return book_data


    def show_profile_window(self, book_data):
        profile_window = tk.Toplevel(self.root)
        profile_window.title("Book Page")

        profile_frame = tk.Frame(profile_window)
        profile_frame.pack(padx=20, pady=20)

        label_book_name = tk.Label(profile_frame, text=f"Book Name: {book_data['book_name']}")
        label_book_name.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        label_num_of_reads = tk.Label(profile_frame, text=f"Number of Reads: {book_data['num_of_reads']}")
        label_num_of_reads.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.label_rate_of_book = tk.Label(profile_frame, text=f"Rate of Book: {book_data['rate_of_book']}")
        self.label_rate_of_book.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        label_w_username = tk.Label(profile_frame, text=f"Writer's Username: {book_data['w_username']}")
        label_w_username.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

        label_short_desc = tk.Label(profile_frame, text=f"Short Description: {book_data['short_desc']}")
        label_short_desc.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

        read_button = tk.Button(profile_frame, text="Mark as read", command=lambda: self.read_book(book_data, label_num_of_reads))
        read_button.grid(row=4, column=0, padx=5, pady=5)

        rate_button = tk.Button(profile_frame, text="Rate", command=self.rate_book)
        rate_button.grid(row=4, column=1, padx=5, pady=5)
    
    def read_book(self, book_data, label_num_of_reads):
        book_data['num_of_reads'] += 1
        label_num_of_reads.config(text=f"Number of Reads: {book_data['num_of_reads']}")
        book_id= book_data['book_id']
        self.update_book_data(book_id,book_data)



    def rate_book(self):
        book_name = self.entry_book_name.get()

        if not book_name:
            messagebox.showerror("ERROR", "Please enter a valid book name.")
            return

        rating = simpledialog.askfloat("Rate Book", "Enter your rating (1-5):", minvalue=1, maxvalue=5)

        if rating is not None:
            book_data = self.fetch_book_data(book_name)
            current_average_rating = float(book_data.get('rate_of_book', 0))
            num_of_ratings = int(book_data.get('num_of_ratings', 0))  # Convert to int

            new_average_rating = ((current_average_rating * num_of_ratings) + rating) / (num_of_ratings + 1)
            num_of_ratings += 1

            book_id= book_data['book_id']

            self.update_book_rating(book_id, book_name, new_average_rating, num_of_ratings, rating)

            self.label_rate_of_book.config(text=f"Rates: {new_average_rating:.2f}")


    def update_book_rating(self, book_id, book_name, new_average_rating, num_of_ratings, rating):
        db_connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = db_connection.cursor(dictionary=True)

        # Update the rate_of_book and num_of_ratings
        query = f"UPDATE Book SET rate_of_book = {new_average_rating}, num_of_ratings = {num_of_ratings} WHERE book_name = '{book_name}'"
        cursor.execute(query)

    
        username = self.user_data["username"]  

        query_insert_rating = f"INSERT INTO rate_book (book_id, rate_value, username) VALUES ({book_id}, {rating}, '{username}')"
        cursor.execute(query_insert_rating)

        db_connection.commit()
        cursor.close()
        db_connection.close()



    def update_book_data(self, book_id, book_data):
        db_connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = db_connection.cursor()

        
        query = f"UPDATE book SET num_of_reads = {book_data['num_of_reads']} WHERE book_id = {book_id}"
        cursor.execute(query)

        
        username = get_user_information2(cursor, conn, self.user_data["username"])
        query_insert_reading = f"INSERT INTO reads_ (book_id, username) VALUES ({book_id}, '{self.user_data['username']}')"

        cursor.execute(query_insert_reading)

        db_connection.commit()
        cursor.close()
        db_connection.close()



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Book Profile")
    root.geometry("800x600")



    root.mainloop()