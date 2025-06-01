import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
from database import get_db_connection

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x200")
        self.on_login_success = on_login_success
        
        ttk.Label(root, text="Username:").pack(pady=5)
        self.username = ttk.Entry(root)
        self.username.pack(pady=5)
        
        ttk.Label(root, text="Password:").pack(pady=5)
        self.password = ttk.Entry(root, show="*")
        self.password.pack(pady=5)
        
        self.login_btn = ttk.Button(root, text="Login", command=self.authenticate)
        self.login_btn.pack(pady=10)
        
    def authenticate(self):
        username = self.username.get()
        password = self.password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required")
            return
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", 
                          (username, hashed_password))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                self.root.destroy()
                self.on_login_success(user)
            else:
                messagebox.showerror("Error", "Invalid username or password")
        except Exception as e:
            messagebox.showerror("Error", f"Authentication failed: {str(e)}")
            import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
from database import get_db_connection

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x200")
        self.on_login_success = on_login_success
        
        # Make the window modal
        self.root.grab_set()
        self.root.focus_set()
        
        ttk.Label(root, text="Username:").pack(pady=5)
        self.username = ttk.Entry(root)
        self.username.pack(pady=5)
        
        ttk.Label(root, text="Password:").pack(pady=5)
        self.password = ttk.Entry(root, show="*")
        self.password.pack(pady=5)
        
        self.login_btn = ttk.Button(root, text="Login", command=self.authenticate)
        self.login_btn.pack(pady=10)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.authenticate())
        
    def authenticate(self):
        username = self.username.get()
        password = self.password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required")
            return
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", 
                          (username, hashed_password))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                self.root.destroy()
                self.on_login_success(user)
            else:
                messagebox.showerror("Error", "Invalid username or password")
        except Exception as e:
            messagebox.showerror("Error", f"Authentication failed: {str(e)}")