import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import get_db_connection

class FeeManager:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
        self.load_fee_structures()
        
    def setup_ui(self):
        # Fee structure frame
        self.structure_frame = ttk.LabelFrame(self.parent, text="Fee Structure")
        self.structure_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for fee structure
        self.fee_tree = ttk.Treeview(self.structure_frame, columns=('id', 'class', 'fee_type', 'amount', 'due_date'), show='headings')
        self.fee_tree.heading('id', text='ID')
        self.fee_tree.heading('class', text='Class')
        self.fee_tree.heading('fee_type', text='Fee Type')
        self.fee_tree.heading('amount', text='Amount')
        self.fee_tree.heading('due_date', text='Due Date')
        self.fee_tree.pack(fill='both', expand=True)
        
        # Add fee structure form
        self.add_structure_frame = ttk.Frame(self.structure_frame)
        self.add_structure_frame.pack(fill='x', pady=5)
        
        ttk.Label(self.add_structure_frame, text="Class:").pack(side='left')
        self.structure_class = ttk.Entry(self.add_structure_frame, width=15)
        self.structure_class.pack(side='left', padx=5)
        
        ttk.Label(self.add_structure_frame, text="Fee Type:").pack(side='left')
        self.fee_type = ttk.Entry(self.add_structure_frame, width=15)
        self.fee_type.pack(side='left', padx=5)
        
        ttk.Label(self.add_structure_frame, text="Amount:").pack(side='left')
        self.amount = ttk.Entry(self.add_structure_frame, width=10)
        self.amount.pack(side='left', padx=5)
        
        ttk.Label(self.add_structure_frame, text="Due Date:").pack(side='left')
        self.due_date = ttk.Entry(self.add_structure_frame, width=10)
        self.due_date.pack(side='left', padx=5)
        
        self.add_structure_btn = ttk.Button(self.add_structure_frame, text="Add Fee Structure", command=self.add_fee_structure)
        self.add_structure_btn.pack(side='left', padx=5)
        
        # Payment frame
        self.payment_frame = ttk.LabelFrame(self.parent, text="Fee Payment")
        self.payment_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Payment form
        ttk.Label(self.payment_frame, text="Student ID:").grid(row=0, column=0, sticky='w')
        self.student_id = ttk.Entry(self.payment_frame)
        self.student_id.grid(row=0, column=1, pady=5)
        
        ttk.Label(self.payment_frame, text="Fee Type:").grid(row=1, column=0, sticky='w')
        self.payment_fee_type = ttk.Combobox(self.payment_frame)
        self.payment_fee_type.grid(row=1, column=1, pady=5)
        
        ttk.Label(self.payment_frame, text="Amount:").grid(row=2, column=0, sticky='w')
        self.payment_amount = ttk.Entry(self.payment_frame)
        self.payment_amount.grid(row=2, column=1, pady=5)
        
        self.make_payment_btn = ttk.Button(self.payment_frame, text="Record Payment", command=self.record_payment)
        self.make_payment_btn.grid(row=3, column=0, columnspan=2, pady=5)
    
    def load_fee_structures(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, class, fee_type, amount, due_date FROM fee_structure")
        fee_structures = cursor.fetchall()
        conn.close()
        
        # Clear existing data
        for item in self.fee_tree.get_children():
            self.fee_tree.delete(item)
            
        # Insert new data
        for fee in fee_structures:
            self.fee_tree.insert('', 'end', values=fee)
        
        # Update fee type combobox
        fee_types = list(set([fee[2] for fee in fee_structures]))  # Get unique fee types
        self.payment_fee_type['values'] = fee_types
    
    def add_fee_structure(self):
        class_ = self.structure_class.get()
        fee_type = self.fee_type.get()
        amount = self.amount.get()
        due_date = self.due_date.get()
        
        if not class_ or not fee_type or not amount:
            messagebox.showerror("Error", "Class, Fee Type and Amount are required")
            return
            
        try:
            amount = float(amount)
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO fee_structure 
                          (class, fee_type, amount, due_date)
                          VALUES (?, ?, ?, ?)''',
                          (class_, fee_type, amount, due_date))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Fee structure added successfully")
            self.load_fee_structures()
            self.structure_class.delete(0, tk.END)
            self.fee_type.delete(0, tk.END)
            self.amount.delete(0, tk.END)
            self.due_date.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add fee structure: {str(e)}")
    
    def record_payment(self):
        student_id = self.student_id.get()
        fee_type = self.payment_fee_type.get()
        amount = self.payment_amount.get()
        
        if not student_id or not fee_type or not amount:
            messagebox.showerror("Error", "All fields are required")
            return
            
        try:
            student_id = int(student_id)
            amount = float(amount)
            payment_date = datetime.now().strftime("%Y-%m-%d")
            receipt_no = f"RCPT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if student exists
            cursor.execute("SELECT name FROM students WHERE id=?", (student_id,))
            student = cursor.fetchone()
            if not student:
                messagebox.showerror("Error", "Student ID not found")
                return
                
            # Record payment
            cursor.execute('''INSERT INTO payments 
                          (student_id, amount, payment_date, fee_type, receipt_no)
                          VALUES (?, ?, ?, ?, ?)''',
                          (student_id, amount, payment_date, fee_type, receipt_no))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Payment recorded successfully\nReceipt No: {receipt_no}")
            self.student_id.delete(0, tk.END)
            self.payment_amount.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Student ID must be a number and Amount must be a number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to record payment: {str(e)}")
            