#modules to import
import pyperclip
import random
import string
import customtkinter as CTk
import tkinter
from tkinter import ttk
from tkinter import messagebox

passwords = []

class PasswordManager:
    def __init__(self):
        self.root = CTk.CTk()
        self.root.title("Password Manager")
        self.root.geometry("400x300")
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("CTkButton", background="black", foreground="white")
        self.style.configure("CTkLabel", background="black", foreground="white")
        self.style.configure("CTkEntry", background="white", foreground="black")
        self.passwords = []
        self.create_widgets()

    def create_widgets(self):
        CTk.CTkLabel(self.root, text="Website:", fg_color="transparent").grid(row=0, column=0, padx=20)
        CTk.CTkLabel(self.root, text="Email/Username:", fg_color="transparent").grid(row=1, column=0, padx=20)
        CTk.CTkLabel(self.root, text="Password:", fg_color="transparent").grid(row=2, column=0, padx=20)
        self.website_entry = CTk.CTkEntry(self.root)
        self.username_entry = CTk.CTkEntry(self.root)
        self.password_entry = CTk.CTkEntry(self.root)
        self.website_entry.grid(row=0, column=1)
        self.username_entry.grid(row=1, column=1)
        self.password_entry.grid(row=2, column=1)
        CTk.CTkButton(self.root, text="Enter your Password", command=self.add_password).grid(row=3, column=0, padx=20)
        CTk.CTkButton(self.root, text="Generate a Password", command=self.generate_password).grid(row=3, column=1, padx=20)

    def add_password(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        if website and username and password:
            self.passwords.append((website, username, password))
            tkinter.messagebox.showinfo(title="Success", message="Password added successfully!")
            self.website_entry.delete(0, CTk.END)
            self.username_entry.delete(0, CTk.END)
            self.password_entry.delete(0, CTk.END)
        else:
             tkinter.messagebox.showerror(title="Hey! Listen!", message="Enter info, no empties allowed")

    def generate_password(self):
        letters = string.ascii_letters
        digits = string.digits
        symbols = string.punctuation
        password = "".join(random.choice(letters + digits + symbols) for _ in range(16))
        self.password_entry.insert(0, password)
    
    def copy_password():
        password = password_input.get()
        pyperclip.copy(password)

    def run(self):
        self.root.mainloop()

    def save_passwords():
        passwords = []
        for website, username, password in zip(website_input.get(), username_input.get(), password_input.get()):
            password_dict = {"website": website, "username": username, "password": password}
            passwords.append(password_dict)

    f = open("passwords.txt", "w")
    for password_dict in passwords:
        f.write(f"{password_dict['website']}:{password_dict['username']}:{password_dict['password']}\n")
    f.close()

#System Settings
CTk.set_appearance_mode("System")
CTk.set_default_color_theme("dark-blue")

if __name__ == "__main__":
    app = PasswordManager()
    app.run()
