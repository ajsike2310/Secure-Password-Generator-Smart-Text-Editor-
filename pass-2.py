import tkinter as tk
from tkinter import filedialog, messagebox, font, colorchooser
import random
import string
import sqlite3
from PIL import Image, ImageTk  

# ---- Database Setup ----
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL)
""")
conn.commit()

# Password Generator Function
def generate_password(length=12, use_uppercase=True, use_digits=True, use_special=True):
    characters = string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# ---- Save Password to Database ----
def save_password(username, password1):
    if not password1.strip():
        messagebox.showerror("Error", "Password cannot be empty!")
        return
    cursor.execute("INSERT INTO passwords (username, password) VALUES (?, ?)", (username, password1))
    conn.commit()
    messagebox.showinfo("Success", "Password saved!")

# ---- Show Saved Passwords ----
def show_saved_passwords(username):
    saved_passwords_window = tk.Toplevel()
    saved_passwords_window.geometry('600x400')
    saved_passwords_window.title('Saved Passwords')
    saved_passwords_window.configure(bg='#1E1E1E')

    tk.Label(saved_passwords_window, text="Your Saved Passwords", font=("Roboto", 16, "bold"), bg='#1E1E1E', fg='#00FFFF').pack(pady=10)
    passwords_listbox = tk.Listbox(saved_passwords_window, width=50, bg='#2D2D2D', fg='#00FFFF', bd=0, highlightthickness=0, relief='flat')
    passwords_listbox.pack(fill="both", expand=True, padx=20, pady=10)

    cursor.execute("SELECT password FROM passwords WHERE username = ?", (username,))
    records = cursor.fetchall()

    for record in records:
        passwords_listbox.insert(tk.END, record[0])

    close_button = tk.Button(saved_passwords_window, text="Close", command=saved_passwords_window.destroy, bg='#00FFFF', fg='#1E1E1E', bd=0, highlightthickness=0, relief='flat', padx=20, pady=10, font=("Roboto", 12), activebackground='#00CCCC')
    close_button.pack(pady=10)

# ---- Clipboard Integration ----
def copy_to_clipboard(text, app):
    if text.strip():
        app.clipboard_clear()
        app.clipboard_append(text)
        app.update()
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showerror("Error", "No password to copy!")

# ---- User Authentication ----
def validate_login(username, password, login_window):
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    record = cursor.fetchone()
    if record and record[0] == password:
        messagebox.showinfo("Login Successful", "Welcome!")
        login_window.destroy()
        main_application(username)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# ---- Signup User ----
def signup_user(username, password, signup_window):
    try:
        if not username.strip() or not password.strip():
            messagebox.showerror("Error", "Username or password cannot be empty!")
            return
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Signup Successful", "You can now log in!")
        signup_window.destroy()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")

# ---- Signup Page ----
def signup_page():
    signup_window = tk.Toplevel()
    signup_window.geometry('600x500')
    signup_window.title('Sign Up')
    signup_window.configure(bg='#1E1E1E')

    tk.Label(signup_window, text='Sign Up', font=("Roboto", 20, "bold"), bg='#1E1E1E', fg='#00FFFF').pack(pady=10)
    username_entry = tk.Entry(signup_window, bg='#2D2D2D', fg='#00FFFF', bd=0, highlightthickness=0, insertbackground='#00FFFF', font=("Roboto", 12))
    username_entry.pack(pady=10, padx=20, ipady=5, fill='x')

    password_entry = tk.Entry(signup_window, show='*', bg='#2D2D2D', fg='#00FFFF', bd=0, highlightthickness=0, insertbackground='#00FFFF', font=("Roboto", 12))
    password_entry.pack(pady=10, padx=20, ipady=5, fill='x')

    signup_button = tk.Button(signup_window, text="Sign Up", command=lambda: signup_user(username_entry.get(), password_entry.get(), signup_window), bg='#00FFFF', fg='#1E1E1E', bd=0, highlightthickness=0, relief='flat', padx=20, pady=10, font=("Roboto", 12), activebackground='#00CCCC')
    signup_button.pack(pady=20)

# ---- Login Page ----
def login_page():
    login_window = tk.Tk()
    login_window.geometry('600x400')
    login_window.title('User Login')
    login_window.configure(bg='#1E1E1E')

    tk.Label(login_window, text='Login', font=("Roboto", 20, "bold"), bg='#1E1E1E', fg='#00FFFF').pack(pady=10)
    username_entry = tk.Entry(login_window, bg='#2D2D2D', fg='#00FFFF', bd=0, highlightthickness=0, insertbackground='#00FFFF', font=("Roboto", 12))
    username_entry.pack(pady=10, padx=20, ipady=5, fill='x')

    password_entry = tk.Entry(login_window, show='*', bg='#2D2D2D', fg='#00FFFF', bd=0, highlightthickness=0, insertbackground='#00FFFF', font=("Roboto", 12))
    password_entry.pack(pady=10, padx=20, ipady=5, fill='x')

    login_button = tk.Button(login_window, text="Login", command=lambda: validate_login(username_entry.get(), password_entry.get(), login_window), bg='#00FFFF', fg='#1E1E1E', bd=0, highlightthickness=0, relief='flat', padx=20, pady=10, font=("Roboto", 12), activebackground='#00CCCC')
    login_button.pack(pady=10)

    signup_button = tk.Button(login_window, text="Sign Up", command=signup_page, bg='#00FFFF', fg='#1E1E1E', bd=0, highlightthickness=0, relief='flat', padx=20, pady=10, font=("Roboto", 12), activebackground='#00CCCC')
    signup_button.pack()

    login_window.mainloop()

# ---- Main Application GUI ----
def main_application(username):
    app = tk.Tk()
    app.title("Password Generator & Text Editor")
    app.geometry("1920x1080")
    app.configure(bg='#1E1E1E')

    # Load the background image
    try:
        bg_image = Image.open("background.jpg")  # Replace with your image path
        bg_image = bg_image.resize((1920, 1080), Image.LANCZOS)
        bg_image_tk = ImageTk.PhotoImage(bg_image)

        # Create a canvas to place the background image
        canvas = tk.Canvas(app, width=800, height=600)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=bg_image_tk, anchor="nw")

        # Add widgets on top of the canvas
        tk.Label(canvas, text=f'Welcome, {username}', font=("Roboto", 16), bg='#1E1E1E', fg='#00FFFF').place(relx=0.5, rely=0.1, anchor="center")
        generate_button = tk.Button(canvas, text="Password Generator amd Text Editor", command=lambda: generate_password_window(username, app), bg='#00FFFF', fg='#1E1E1E', bd=0, highlightthickness=0, relief='flat', padx=20, pady=10, font=("Roboto", 12), activebackground='#00CCCC')
        generate_button.place(relx=0.5, rely=0.3, anchor="center")

        show_passwords_button = tk.Button(canvas, text="Show Saved Passwords", command=lambda: show_saved_passwords(username), bg='#00FFFF', fg='#1E1E1E', bd=0, highlightthickness=0, relief='flat', padx=20, pady=10, font=("Roboto", 12), activebackground='#00CCCC')
        show_passwords_button.place(relx=0.5, rely=0.4, anchor="center")

        logout_button = tk.Button(canvas, text="Logout", command=app.destroy, bg='#00FFFF', fg='#1E1E1E', bd=0, highlightthickness=0, relief='flat', padx=20, pady=10, font=("Roboto", 12), activebackground='#00CCCC')
        logout_button.place(relx=0.5, rely=0.5, anchor="center")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load background image: {e}")
        app.configure(bg='#1E1E1E')  # Fallback to default background color

    app.mainloop()

# ---- Password Generator Frame ----
def generate_password_window(username, app):
    gen_window = tk.Toplevel(app)
    gen_window.title("Generate Password")
    gen_window.geometry("1920x1080")
    gen_window.configure(bg='#1E1E1E')

    password_var = tk.StringVar()
    length_var = tk.IntVar(value=12)

    use_uppercase = tk.BooleanVar(value=True)
    use_digits = tk.BooleanVar(value=True)
    use_special = tk.BooleanVar(value=True)

    tk.Label(gen_window, text="Password Length:", bg='#1E1E1E', fg='#00FFFF', font=("Roboto", 12)).pack()
    tk.Scale(gen_window, from_=6, to=32, orient='horizontal', variable=length_var, bg='#2D2D2D', fg='#00FFFF', bd=0, highlightthickness=0).pack()

    tk.Checkbutton(gen_window, text="Include Uppercase Letters", variable=use_uppercase, bg='#1E1E1E', fg='#00FFFF', selectcolor='#2D2D2D', font=("Roboto", 12)).pack()
    tk.Checkbutton(gen_window, text="Include Digits", variable=use_digits, bg='#1E1E1E', fg='#00FFFF', selectcolor='#2D2D2D', font=("Roboto", 12)).pack()
    tk.Checkbutton(gen_window, text="Include Special Characters", variable=use_special, bg='#1E1E1E', fg='#00FFFF', selectcolor='#2D2D2D', font=("Roboto", 12)).pack()

    generate_button = tk.Button(gen_window, text="Generate", command=lambda: password_var.set(generate_password(length_var.get(), use_uppercase.get(), use_digits.get(), use_special.get())), bg='#00FFFF', fg='#1E1E1E', bd=0, highlightthickness=0, relief='flat', padx=20, pady=10, font=("Roboto", 12), activebackground='#00CCCC')
    generate_button.pack(pady=10)

    password_entry = tk.Entry(gen_window, textvariable=password_var, state='readonly', bg='#2D2D2D', fg='#00FFFF', bd=0, highlightthickness=0, font=("Roboto", 12))
    password_entry.pack(pady=5, padx=20, ipady=5, fill='x')

    save_button = tk.Button(gen_window, text="Save Password", command=lambda: save_password(username, password_var.get()), bg='#00FFFF', fg='#1E1E1E', bd=0, highlightthickness=0, relief='flat', padx=20, pady=10, font=("Roboto", 12), activebackground='#00CCCC')
    save_button.pack(pady=10)

    copy_button = tk.Button(gen_window, text="Copy to Clipboard", command=lambda: copy_to_clipboard(password_var.get(), app), bg='#00FFFF', fg='#1E1E1E', bd=0, highlightthickness=0, relief='flat', padx=20, pady=10, font=("Roboto", 12), activebackground='#00CCCC')
    copy_button.pack(pady=10)

    # Text Editor Frame
    text_editor_frame = tk.LabelFrame(gen_window, text="Text Editor", bg='#1E1E1E', fg='#00FFFF', font=("Roboto", 12))
    text_editor_frame.pack(pady=10, fill="both", expand=True, padx=20)
    text_editor = tk.Text(text_editor_frame, wrap=tk.WORD, width=40, height=8, bg='#2D2D2D', fg='#00FFFF', bd=0, highlightthickness=0, font=("Roboto", 12))
    text_editor.pack(fill="both", expand=True, padx=10, pady=10)

    # File Handling Functions
    def open_file():
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                text_editor.delete(1.0, tk.END)
                text_editor.insert(tk.END, content)

    def save_file():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(text_editor.get(1.0, tk.END))

    # File Handling Buttons
    file_handling_frame = tk.Frame(text_editor_frame, bg='#1E1E1E')
    file_handling_frame.pack(pady=5)

    open_button = tk.Button(file_handling_frame, text="Open File", command=open_file, bg='#00FFFF', fg='#1E1E1E', bd=0, highlightthickness=0, relief='flat', padx=20, pady=10, font=("Roboto", 12), activebackground='#00CCCC')
    open_button.grid(row=0, column=0, padx=5)

    save_button = tk.Button(file_handling_frame, text="Save File", command=save_file, bg='#00FFFF', fg='#1E1E1E', bd=0, highlightthickness=0, relief='flat', padx=20, pady=10, font=("Roboto", 12), activebackground='#00CCCC')
    save_button.grid(row=0, column=1, padx=5)

    # Customization Options
    customization_frame = tk.LabelFrame(gen_window, text="Customization Options", bg='#1E1E1E', fg='#00FFFF', font=("Roboto", 12))
    customization_frame.pack(pady=10, fill="both", expand=True, padx=20)

    font_var = tk.StringVar(value="Roboto")
    tk.Label(customization_frame, text="Font:", bg='#1E1E1E', fg='#00FFFF', font=("Roboto", 12)).grid(row=0, column=0, sticky="w")
    tk.OptionMenu(customization_frame, font_var, "Roboto", "Arial", "Courier", "Times New Roman", "Verdana").grid(row=0, column=1, sticky="w")
    apply_button = tk.Button(customization_frame, text="Apply", command=lambda: text_editor.configure(font=font.Font(family=font_var.get(), size=12)), bg='#00FFFF', fg='#1E1E1E', bd=0, highlightthickness=0, relief='flat', padx=20, pady=10, font=("Roboto", 12), activebackground='#00CCCC')
    apply_button.grid(row=0, column=2, sticky="w")

    def change_text_color():
        color_code = colorchooser.askcolor(title="Choose Text Color")[1]
        if color_code:
            text_editor.configure(fg=color_code)
        gen_window.focus_set()  # Set focus back to the main window

    color_button = tk.Button(customization_frame, text="Text Color", command=change_text_color, bg='#00FFFF', fg='#1E1E1E', bd=0, highlightthickness=0, relief='flat', padx=20, pady=10, font=("Roboto", 12), activebackground='#00CCCC')
    color_button.grid(row=1, column=0, columnspan=3, pady=5)

# ---- Start the Application ----
if __name__ == "__main__":
    login_page()
