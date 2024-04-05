import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from database import *

conn, cursor = initialize_connection()

class HomePage(tk.Frame):
    def __init__(self, master, user_data):
        super().__init__(master)
        self.master = master
        self.user_data = user_data

        self.pack()

        self.label = tk.Label(self, text="Home Page")
        self.label.pack(pady=10)

        self.post_title_label = tk.Label(self, text="Post Title:")
        self.post_title_label.pack()

        self.post_title_entry = tk.Text(self, height=2, width=30)
        self.post_title_entry.pack()

        self.post_text_label = tk.Label(self, text="Create a new post:")
        self.post_text_label.pack()

        self.post_text_entry = tk.Text(self, height=5, width=30)
        self.post_text_entry.pack()

        self.post_button = tk.Button(self, text="Post", command=self.create_post)
        self.post_button.pack(pady=10)

        self.posts_label = tk.Label(self, text="Recent Posts:")
        self.posts_label.pack()

        self.canvas = tk.Canvas(self)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.posts_frame = tk.Frame(self.canvas)
        self.posts_frame.pack()

        self.canvas.create_window((0, 0), window=self.posts_frame, anchor="nw", tags="self.posts_frame")

        self.posts_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.user_profile_button = tk.Button(self, text="My Profile", command=self.go_to_user_profile)
        self.user_profile_button.pack(side=tk.TOP, anchor=tk.NE, pady=5)

        
        self.writer_profile_button = tk.Button(self, text="Writer Profile", command=self.go_to_writer_profile)
        self.writer_profile_button.pack(side=tk.TOP, anchor=tk.NE, pady=5)

        self.book_profile_button = tk.Button(self, text="Book Profile", command=self.go_to_book_profile)
        self.book_profile_button.pack(side=tk.TOP, anchor=tk.NE, pady=5)

        # Follow button
        self.follow_button = tk.Button(self, text="Follow", command=self.follow_user)
        self.follow_button.pack(pady=5)

        # Unfollow button
        self.unfollow_button = tk.Button(self, text="Unfollow", command=self.unfollow_user)
        self.unfollow_button.pack(pady=5)
        
        self.back_button = tk.Button(self, text="Logout", command=self.logout)
        self.back_button.pack(side=tk.TOP, anchor=tk.NE, pady=5)

        self.refresh_posts()
    
    def go_to_book_profile(self):
        from book_profile import BookProfileViewer
        self.destroy()
        BookProfileViewer(self.master,self.user_data)


    def go_to_writer_profile(self):
        from writer_profile import WriterProfileViewer

        self.destroy()
        WriterProfileViewer(self.master,self.user_data)



    def go_to_user_profile(self):
        from login import UserProfilePage
        self.destroy()
        UserProfilePage(self.master, self.user_data)

    def create_post(self):
        post_title = self.post_title_entry.get("1.0", tk.END).strip()
        post_text = self.post_text_entry.get("1.0", tk.END).strip()
        if post_title and post_text:
            create_post(cursor, conn, self.user_data["username"], post_title, post_text)

            messagebox.showinfo("Success", "Post created successfully.")
            self.post_text_entry.delete("1.0", tk.END)
            self.post_title_entry.delete("1.0", tk.END)

            self.refresh_posts()
        else:
            messagebox.showerror("Error", "Post title and content cannot be empty.")

    def refresh_posts(self):
        # Clear previous posts and comments
        for widget in self.posts_frame.winfo_children():
            widget.destroy()

        posts = get_recent_posts(cursor, conn)
        for post in posts:
            post_frame = tk.Frame(self.posts_frame, relief="solid", bd=1)
            post_frame.pack(pady=5, fill="x")

            username, post_title, post_text = post
            post_label = tk.Label(post_frame, text=f"{username}: {post_title}")
            post_label.pack()
            post_text_label = tk.Text(post_frame, height=2, width=30)
            post_text_label.insert(tk.END, post_text)
            post_text_label.config(state="disabled")
            post_text_label.pack()

            post_id = get_post_id_from_text(cursor, conn, post_title)
            post_frame.post_id = post_id  # Attach post_id as an attribute to the frame

            # Add comment button
            comment_button = tk.Button(post_frame, text="Add Comment", command=lambda pid=post_id: self.add_comment(pid))
            comment_button.pack(pady=5)

            like_button = tk.Button(post_frame, text="Like Post", command=lambda pid=post_id: self.like_post(pid))
            # Display like count
            like_count = get_like_count(cursor, conn, post_id)
            like_count_label = tk.Label(post_frame, text=f"Likes: {like_count}")
            like_count_label.pack()

            # Display comments
            comments = get_comments(cursor, conn, post_id)
            for comment in comments:
                comment_frame = tk.Frame(post_frame)
                comment_frame.pack(pady=2)
                comment_user, comment_content = comment
                comment_label = tk.Label(comment_frame, text=f"{comment_user}: {comment_content}")
                comment_label.pack()

            like_button.pack(pady=5)
    def like_post(self, post_id):
        if post_id is not None:
            username = self.user_data["username"]
            if not has_liked(cursor, conn, username, post_id):
                like_post(cursor, conn, username, post_id)
                messagebox.showinfo("Success", "Post liked successfully.")
                # Optionally, you can refresh the posts here if needed
                self.refresh_posts()
            else:
                messagebox.showinfo("Info", "You have already liked this post.")
        else:
            messagebox.showerror("Error", "Invalid post selected.")
    def get_selected_post(self):
            # Get the selected post from the posts_frame
            selected_widget = self.posts_frame.focus_get()
            while selected_widget and not hasattr(selected_widget, "post_id"):
                selected_widget = selected_widget.master
            return selected_widget

    def add_comment(self, post_id):
        if post_id:
            comment_content = self.get_comment_content()

            if comment_content:
                add_comment(cursor, conn, self.user_data["username"], post_id, comment_content)

                messagebox.showinfo("Success", "Comment added successfully.")
                self.refresh_posts()
            else:
                messagebox.showerror("Error", "Comment content cannot be empty.")
        else:
            messagebox.showerror("Error", "Please select a post to comment on.")

    def get_comment_content(self):
        return simpledialog.askstring("Comment", "Enter your comment:")







    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig("self.posts_frame", width=canvas_width)



    def follow_user(self):
        followed_username = simpledialog.askstring("Follow User", "Enter the username to follow:")
        if followed_username:
            if followed_username == self.user_data["username"]:
                messagebox.showerror("Error", "You cannot follow yourself.")
            else:
                follow_user(cursor, conn, self.user_data["username"], followed_username)
                messagebox.showinfo("Success", f"You are now following {followed_username}.")
                self.refresh_follow_stats()


    def unfollow_user(self):
        followed_username = simpledialog.askstring("Unfollow User", "Enter the username to unfollow:")
        if followed_username:
            unfollow_user(cursor, conn, self.user_data["username"], followed_username)
            messagebox.showinfo("Success", f"You are no longer following {followed_username}.")
            self.refresh_follow_stats()


    def refresh_follow_stats(self):
        following_num = get_following_count(cursor, conn, self.user_data["username"])
        follower_num = get_follower_count(cursor, conn, self.user_data["username"])

        # Update the following_num and follower_num in the User table
        update_follow_stats(cursor, conn, self.user_data["username"])

        # Update the displayed following count in the GUI
        self.user_data["following_num"] = following_num

        messagebox.showinfo("Success", f"Following: {following_num}, Followers: {follower_num}")





    def logout(self):
        from login import WelcomePage
        self.destroy()
        WelcomePage(self.master)




if __name__ == "__main__":
    root = tk.Tk()
    root.title("1000Kitap-Home")
    root.geometry("800x600")



    root.mainloop()
