import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from database import*
from homepage import HomePage

# The rest of your code remains unchanged


conn, cursor = initialize_connection()

class WelcomePage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.label = tk.Label(self, text="Welcome to 1000Kitap!")
        self.label.pack(pady=10)

        self.login_button = tk.Button(self, text="Login", command=self.show_login_page)
        self.login_button.pack(pady=5)

        self.register_button = tk.Button(self, text="Register", command=self.show_register_page)
        self.register_button.pack(pady=5)


    def show_login_page(self):
        self.destroy()
        LoginPage(self.master)

    def show_register_page(self):
        self.destroy()
        RegisterPage(self.master)

class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()

        self.label = tk.Label(self, text="Login Page")
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.username_label = tk.Label(self, text="Username")
        self.username_entry = tk.Entry(self)

        self.password_label = tk.Label(self, text="Password")
        self.password_entry = tk.Entry(self, show='*')

        self.submit_button = tk.Button(self, text="Login", command=self.submit)
        self.back_button = tk.Button(self, text="Back to Welcome", command=self.show_welcome_page)

        # Centering the widgets using grid
        self.username_label.grid(row=5, column=0, pady=20)
        self.username_entry.grid(row=5, column=1, pady=20)
        self.password_label.grid(row=6, column=0, pady=20)
        self.password_entry.grid(row=6, column=1, pady=20)
        self.submit_button.grid(row=7, column=0, columnspan=2, pady=20)
        self.back_button.grid(row=8, column=0, columnspan=2, pady=5)



    def show_welcome_page(self):
        self.destroy()
        WelcomePage(self.master)

    def submit(self):
        data = {}
        data["username"]= self.username_entry.get()
        data["password_"] = self.password_entry.get()
        user = login(cursor, data)
        if user:
             self.destroy()
             UserProfilePage(self.master, user)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")

class RegisterPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.label = tk.Label(self, text="Register Page")
        self.label.grid(row=0, column=0, columnspan=2, pady=10)


        self.username_label = tk.Label(self, text="Username")
        self.username_entry = tk.Entry(self)

        self.first_name_label = tk.Label(self, text="First Name")
        self.first_name_entry = tk.Entry(self)

        self.last_name_label = tk.Label(self, text="Last Name")
        self.last_name_entry = tk.Entry(self)

        self.password_label = tk.Label(self, text="password")
        self.password_entry = tk.Entry(self,show='*')

        self.email_label = tk.Label(self, text="Email")
        self.email_entry = tk.Entry(self)

        self.gender_label = tk.Label(self, text="Gender")
        self.gender_entry = tk.Entry(self)

        self.submit_button = tk.Button(self, text="Register", command=self.submit)

        self.back_button = tk.Button(self, text="Back to Welcome", command=self.show_welcome_page)

        # Centering the widgets using grid
        self.username_label.grid(row=5, column=0, pady=20)
        self.username_entry.grid(row=5, column=1, pady=20)
        self.first_name_label.grid(row=6, column=0, pady=20)
        self.first_name_entry.grid(row=6, column=1, pady=20)
        self.last_name_label.grid(row=7, column=0, pady=20)
        self.last_name_entry.grid(row=7, column=1, pady=20)
        self.email_label.grid(row=8, column=0,pady = 20)
        self.email_entry.grid(row=8, column=1,pady = 20)
        self.password_label.grid(row=9, column=0,pady = 20)
        self.password_entry.grid(row=9, column=1,pady = 20)
        self.gender_label.grid(row=10, column=0,pady = 20)
        self.gender_entry.grid(row=10, column=1,pady = 20)

        self.submit_button.grid(row=11, column=0, columnspan=2, pady=20)
        self.back_button.grid(row=12, column=0, columnspan=2, pady=5)

    def show_welcome_page(self):
        self.destroy()
        WelcomePage(self.master)
    def submit(self):
        data = {}
        data["username"] = self.username_entry.get()
        data["first_name"] = self.first_name_entry.get()
        data["last_name"] = self.last_name_entry.get()
        data["email"] = self.email_entry.get()

        data["gender"] = self.gender_entry.get()
        data["password_"] = self.password_entry.get()

        user = register(cursor,conn,data)
        # If registration is successful, show the profile page
        if user:
            self.destroy()
            messagebox.showinfo("Registration Successful", "Registration successful! You can now log in.")

            UserProfilePage(self.master, user)
        else:
            messagebox.showerror("Registration Failed", "Failed to register user. Please try again.")

class UserProfilePage(tk.Frame):
    def __init__(self, master, data):
        super().__init__(master)
        self.master = master
        self.data = data

        self.pack()

        self.label = tk.Label(self, text="User Profile Page")
        self.label.pack(pady=10)

        # Display user information
        self.username_label = tk.Label(self, text=f"Username: {data['username']}")
        self.username_label.pack()

        self.first_name_label = tk.Label(self, text=f"First Name: {data['first_name']}")
        self.first_name_label.pack()

        self.last_name_label = tk.Label(self, text=f"Last Name: {data['last_name']}")
        self.last_name_label.pack()
        
        self.follower_label = tk.Label(self, text="")
        self.follower_label.pack()

        self.following_label = tk.Label(self, text="")
        self.following_label.pack()
        self.bio_label = tk.Label(self, text="Bio")
        self.bio_label.pack()

        self.bio_entry = tk.Text(self, height=5, width=30)
        self.bio_entry.pack()

        self.edit_bio_button = tk.Button(self, text="Edit Bio", command=self.edit_bio)
        self.edit_bio_button.pack(pady=5)
        

        self.goal_book_label = tk.Label(self, text="Goal Book: ")
        self.goal_book_label.pack()

        self.goal_book_entry = tk.Text(self, height=1, width=5)
        self.goal_book_entry.pack()

        self.goal_book_edit_button = tk.Button(self, text="Edit Goal", command=self.edit_goal)
        self.goal_book_edit_button.pack(pady=10)

        self.past_reads_label = tk.Label(self, text="Past Reads:")
        self.past_reads_label.pack()

        self.past_reads_entry = tk.Text(self, height=1, width=5)
        self.past_reads_entry.pack()

        self.update_past_reads_button = tk.Button(self, text="Update Past Reads", command=self.update_past_reads)
        self.update_past_reads_button.pack(pady=10)


        self.back_button = tk.Button(self, text="Logout", command=self.logout)
        self.back_button.pack(pady=5)
        self.go_to_home_page_button = tk.Button(self, text="Go to HomePage", command=self.go_to_home_page)
        self.go_to_home_page_button.pack(pady=5)
        self.load_user_information()

        self.create_list_button = tk.Button(self, text="Create New List", command=self.create_new_list)
        self.create_list_button.pack(pady=5)


        # ... (existing code)

    def create_new_list(self):
        # Call the create_list method of the BookList instance
        from booklist import BookList

        BookList(self.master,self.data)

    def load_user_information(self):
        user_data = get_user_information2(cursor, conn, self.data["username"])

        follower_count = get_follower_count(cursor, conn, self.data["username"])
        following_count = get_following_count(cursor, conn, self.data["username"])

        self.follower_label.config(text=f"Followers: {follower_count}")
        self.following_label.config(text=f"Following: {following_count}")

        # Clear existing text in the widgets
        self.bio_entry.delete("1.0", END)
        self.goal_book_entry.delete("1.0", tk.END)
        self.past_reads_entry.delete("1.0", tk.END)

        # Insert new text into the widgets
        self.bio_entry.insert("1.0", user_data.get("bio", ""))
        self.goal_book_entry.insert(tk.END, str(user_data["goal_book_num"]))
        self.past_reads_entry.insert(tk.END, str(user_data["past_read_num"]))


        

    def go_to_home_page(self):
        self.destroy()
        HomePage(self.master, self.data)
        
    def update_past_reads(self):
        # Open a new window for updating past reads
        update_past_reads_window = tk.Toplevel(self)
        update_past_reads_window.title("Update Past Reads")

        update_past_reads_label = tk.Label(update_past_reads_window, text="Update Past Reads:")
        update_past_reads_label.pack(pady=10)

        update_past_reads_entry = tk.Text(update_past_reads_window, height=5, width=30)
        update_past_reads_entry.insert(tk.END, self.past_reads_entry.get("1.0", tk.END))
        update_past_reads_entry.pack(pady=10)

        save_button = tk.Button(update_past_reads_window, text="Save", command=lambda: self.save_past_reads(update_past_reads_entry))
        save_button.pack(pady=5)

    def save_past_reads(self, past_reads_entry):
        try:
            # Get the entered text from the Entry widget
            new_past_reads_str = past_reads_entry.get("1.0", tk.END).strip()

            # Try to convert the input to an integer
            past_reads_value = int(new_past_reads_str)

            # Get the user ID from the data
            username = self.data["username"]

            # Save the edited goal to the database
            update_past_reads(cursor, conn, self.data, past_reads_value)

            # Update the displayed goal
            self.past_reads_entry.delete("1.0", tk.END)
            self.past_reads_entry.insert(tk.END, str(past_reads_value))
        except ValueError:
            # Handle the case where the input is not a valid integer
            messagebox.showerror("Invalid Input", "Please enter a valid integer for the goal.")

    def edit_goal(self):
        # Open a new window for editing bio
        edit_goal_window = tk.Toplevel(self)
        edit_goal_window.title("Edit Goal")

        edit_goal_label = tk.Label(edit_goal_window, text="Edit Goal:")
        edit_goal_label.pack(pady=10)

        edit_goal_entry = tk.Text(edit_goal_window, height=5, width=30)
        edit_goal_entry.insert(tk.END, self.goal_book_entry.get("1.0", tk.END))
        edit_goal_entry.pack(pady=10)

        save_button = tk.Button(edit_goal_window, text="Save", command=lambda: self.save_goal(edit_goal_entry))

        save_button.pack(pady=5)

    def save_goal(self, new_goal_entry):
        try:
            # Get the entered text from the Entry widget
            new_goal_str = new_goal_entry.get("1.0", tk.END).strip()

            # Try to convert the input to an integer
            goal_value = int(new_goal_str)

            # Get the user ID from the data
            username = self.data["username"]

            # Save the edited goal to the database
            update_goal(cursor, conn, self.data, goal_value)

            # Update the displayed goal
            self.goal_book_entry.delete("1.0", tk.END)
            self.goal_book_entry.insert(tk.END, str(goal_value))
        except ValueError:
            # Handle the case where the input is not a valid integer
            messagebox.showerror("Invalid Input", "Please enter a valid integer for the goal.")


    def edit_bio(self):
        # Open a new window for editing bio
        edit_bio_window = tk.Toplevel(self)
        edit_bio_window.title("Edit Bio")

        edit_bio_label = tk.Label(edit_bio_window, text="Edit Bio:")
        edit_bio_label.pack(pady=10)

        edit_bio_entry = tk.Text(edit_bio_window, height=5, width=30)
        edit_bio_entry.insert(tk.END, self.bio_entry.get("1.0", tk.END))
        edit_bio_entry.pack(pady=10)

        save_button = tk.Button(edit_bio_window, text="Save", command=lambda: self.save_bio(edit_bio_entry.get("1.0", tk.END)))
        save_button.pack(pady=5)

    def save_bio(self, new_bio):
        # Get the user ID from the data
        username = self.data["username"]

        # Save the edited bio to the database
        update_bio(cursor,conn, self.data, new_bio)

        # Update the displayed bio
        self.bio_entry.delete("1.0", tk.END)
        self.bio_entry.insert(tk.END, new_bio)
    def show_welcome_page(self):
        self.destroy()
        WelcomePage(self.master)

    def logout(self):
        # Destroy the current profile page and return to the WelcomePage
        self.destroy()
        WelcomePage(self.master)




if __name__ == "__main__":
    root = tk.Tk()
    root.title("1000Kitap-Welcome")
    root.geometry("1250x800")

    welcome_page = WelcomePage(root)


    


    root.mainloop()