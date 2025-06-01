import tkinter as tk
from tkinter import ttk, messagebox
from student_manager import StudentManager
from fee_manager import FeeManager
from reports import ReportGenerator
from database import create_database

class FeeManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("School Fee Management System")
        self.root.geometry("1000x600")
        
        # Initialize database
        create_database()
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        # Create frames for each tab
        self.student_frame = ttk.Frame(self.notebook)
        self.fee_frame = ttk.Frame(self.notebook)
        self.report_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.student_frame, text='Student Management')
        self.notebook.add(self.fee_frame, text='Fee Management')
        self.notebook.add(self.report_frame, text='Reports')
        
        # Initialize modules
        self.student_manager = StudentManager(self.student_frame)
        self.fee_manager = FeeManager(self.fee_frame)
        self.report_generator = ReportGenerator(self.report_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = FeeManagementSystem(root)
    root.mainloop()
    
    import tkinter as tk
from tkinter import ttk, messagebox
from student_manager import StudentManager
from fee_manager import FeeManager
from reports import ReportGenerator
from database import create_database
from auth import LoginWindow

class FeeManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("School Fee Management System")
        self.root.geometry("1000x600")
        
        # Initialize database
        create_database()
        
        # Show login window first
        self.show_login()

    def show_login(self):
        # Hide main window while showing login
        self.root.withdraw()
        
        # Create login window
        login_window = tk.Toplevel(self.root)
        login_window.protocol("WM_DELETE_WINDOW", self.on_close_login)
        
        LoginWindow(login_window, self.on_login_success)

    def on_close_login(self):
        # If user closes login window, exit application
        self.root.destroy()

    def on_login_success(self, user):
        # Destroy login window and show main application
        for window in self.root.winfo_children():
            if isinstance(window, tk.Toplevel):
                window.destroy()
        
        self.root.deiconify()  # Show main window again
        self.setup_main_ui()

    def setup_main_ui(self):
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        
        # Create frames for each tab
        self.student_frame = ttk.Frame(self.notebook)
        self.fee_frame = ttk.Frame(self.notebook)
        self.report_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.student_frame, text='Student Management')
        self.notebook.add(self.fee_frame, text='Fee Management')
        self.notebook.add(self.report_frame, text='Reports')
        
        # Initialize modules
        self.student_manager = StudentManager(self.student_frame)
        self.fee_manager = FeeManager(self.fee_frame)
        self.report_generator = ReportGenerator(self.report_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = FeeManagementSystem(root)
    root.mainloop()