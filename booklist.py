import tkinter as tk
from tkinter import messagebox
import mysql.connector

from database import *
conn, cursor = initialize_connection()


class BookList:
    def __init__(self, root,user_data):
        self.root = root
        self.root.title("Book Viewer")

        self.user_data = user_data
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)

        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="737123eeE.",
            database="DBMS"
        )

        self.cursor = self.connection.cursor()

        self.create_list_button = tk.Button(self.main_frame, text="Create new list", command=self.create_list)
        self.create_list_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.book_lists = {}  # Change to a dictionary to store list data

        self.view_list_button = tk.Button(self.main_frame, text="View List", command=self.view_list)
        self.view_list_button.grid(row=2, column=2, columnspan=2, pady=10)
    def create_list(self):
        self.new_list_window = tk.Toplevel(self.root)
        self.new_list_window.title("Create New List")

        tk.Label(self.new_list_window, text="List Name:").pack(pady=5)
        self.list_name_entry = tk.Entry(self.new_list_window)
        self.list_name_entry.pack(pady=5)

        tk.Button(self.new_list_window, text="Save", command=lambda: self.save_list(self.new_list_window, self.list_name_entry)).pack(pady=10)

    def save_list(self, new_list_window, list_name_entry):
        current_list_name = list_name_entry.get()

        if not current_list_name:
            messagebox.showerror("ERROR", "Please enter a valid list name.")
            return

        # Get the username from the user_data
        username = self.user_data["username"]

        # Create a new list in the dictionary
        self.book_lists[current_list_name] = []

        # Add the new list to the database
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="737123eeE.",
            database="DBMS"
        )
        cursor = db_connection.cursor(dictionary=True)

        # Insert the new list into the database
        query_insert_booklist = "INSERT INTO BookList (list_name, username) VALUES (%s, %s)"
        cursor.execute(query_insert_booklist, (current_list_name, username))

        db_connection.commit()

        cursor.close()
        db_connection.close()

        messagebox.showinfo("Info", f"List '{current_list_name}' saved successfully.")
        new_list_window.destroy()


    def view_list(self):
        if not self.book_lists:
            messagebox.showinfo("Info", "No lists created yet.")
        else:
            list_selection_window = tk.Toplevel(self.root)
            list_selection_window.title("Select List")

            tk.Label(list_selection_window, text="Select a List:").pack(pady=5)

            list_names = list(self.book_lists.keys())
            list_var = tk.StringVar(value=list_names)
            listbox = tk.Listbox(list_selection_window, listvariable=list_var, selectmode=tk.SINGLE)
            listbox.pack(pady=10)

            view_list_button = tk.Button(list_selection_window, text="View List", command=lambda: self.display_list(listbox.curselection()))
            view_list_button.pack(pady=10)

    def display_list(self, selected_list_indices):
        if selected_list_indices:
            selected_list_index = selected_list_indices[0]
            list_names = list(self.book_lists.keys())

            if 0 <= selected_list_index < len(list_names):
                selected_list_name = list_names[selected_list_index]

                if selected_list_name in self.book_lists:
                    view_list_window = tk.Toplevel(self.root)
                    view_list_window.title(f"View List - {selected_list_name}")

                    for book_name in self.book_lists[selected_list_name]:
                        tk.Label(view_list_window, text=f"  Book Name: {book_name}").pack()

                    tk.Button(view_list_window, text="Add Book", command=lambda: self.add_book(view_list_window, selected_list_name)).pack(pady=10)
                else:
                    messagebox.showinfo("Info", f"No books in the selected list: {selected_list_name}")
            else:
                messagebox.showinfo("Info", "Please select a valid list.")
        else:
            messagebox.showinfo("Info", "Please select a list.")

    def add_book(self, view_list_window, selected_list_name):
        add_book_window = tk.Toplevel(self.root)
        add_book_window.title("Add Book to List")

        tk.Label(add_book_window, text="Book Name:").pack(pady=5)
        book_name_entry = tk.Entry(add_book_window)
        book_name_entry.pack(pady=5)

        tk.Button(add_book_window, text="Add", command=lambda: self.save_book(add_book_window, book_name_entry, selected_list_name)).pack(pady=10)

    def save_book(self, add_book_window, book_name_entry, selected_list_name):
        book_name = book_name_entry.get()

        if not book_name:
            messagebox.showerror("ERROR", "Please enter a valid book name.")
            return

        else:
            messagebox.showinfo("Info", f"Book '{book_name}' added to the list '{selected_list_name}'.")

        self.book_lists[selected_list_name].append(book_name)  # Add the book to the selected list

        # Veritabanına ekleme işlemi
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="737123eeE.",
            database="DBMS"
        )
        cursor = db_connection.cursor()

    # Kitabı sadece Include tablosuna ekleyin
        query_insert_include = "INSERT INTO Include (book_id, list_id) VALUES ((SELECT book_id FROM Book WHERE book_name = %s), (SELECT list_id FROM BookList WHERE list_name = %s))"
        cursor.execute(query_insert_include, (book_name, selected_list_name))

        db_connection.commit()

        cursor.close()
        db_connection.close()

        add_book_window.destroy()

    def fetch_book_data(self, book_name):
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="737123eeE.",
            database="DBMS"
        )

        cursor = db_connection.cursor(dictionary=True)
        query = f"SELECT * FROM Book WHERE book_name = '{book_name}'"
        cursor.execute(query)
        book_data = cursor.fetchone()

        cursor.close()
        db_connection.close()

        print("Query:", query)
        print("Book Data:", book_data)

        return book_data

if __name__ == "__main__":
    root = tk.Tk()
    root.mainloop()