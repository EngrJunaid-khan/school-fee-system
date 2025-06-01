import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import get_db_connection

class StudentManager:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
        self.load_students()
        
    def setup_ui(self):
        # Frame for student list
        self.list_frame = ttk.Frame(self.parent)
        self.list_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for student list
        self.student_tree = ttk.Treeview(self.list_frame, columns=('id', 'name', 'class', 'section', 'roll_no'), show='headings')
        self.student_tree.heading('id', text='ID')
        self.student_tree.heading('name', text='Name')
        self.student_tree.heading('class', text='Class')
        self.student_tree.heading('section', text='Section')
        self.student_tree.heading('roll_no', text='Roll No')
        self.student_tree.pack(fill='both', expand=True)
        
        # Frame for student form
        self.form_frame = ttk.Frame(self.parent)
        self.form_frame.pack(side='right', fill='y', padx=10, pady=10)
        
        # Form fields
        ttk.Label(self.form_frame, text="Student Name:").grid(row=0, column=0, sticky='w')
        self.name_entry = ttk.Entry(self.form_frame)
        self.name_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(self.form_frame, text="Class:").grid(row=1, column=0, sticky='w')
        self.class_entry = ttk.Entry(self.form_frame)
        self.class_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(self.form_frame, text="Section:").grid(row=2, column=0, sticky='w')
        self.section_entry = ttk.Entry(self.form_frame)
        self.section_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(self.form_frame, text="Roll No:").grid(row=3, column=0, sticky='w')
        self.roll_no_entry = ttk.Entry(self.form_frame)
        self.roll_no_entry.grid(row=3, column=1, pady=5)
        
        ttk.Label(self.form_frame, text="Father's Name:").grid(row=4, column=0, sticky='w')
        self.father_name_entry = ttk.Entry(self.form_frame)
        self.father_name_entry.grid(row=4, column=1, pady=5)
        
        ttk.Label(self.form_frame, text="Contact:").grid(row=5, column=0, sticky='w')
        self.contact_entry = ttk.Entry(self.form_frame)
        self.contact_entry.grid(row=5, column=1, pady=5)
        
        ttk.Label(self.form_frame, text="Address:").grid(row=6, column=0, sticky='w')
        self.address_entry = tk.Text(self.form_frame, height=3, width=25)
        self.address_entry.grid(row=6, column=1, pady=5)
        
        # Buttons
        self.add_btn = ttk.Button(self.form_frame, text="Add Student", command=self.add_student)
        self.add_btn.grid(row=7, column=0, pady=10)
        
        self.update_btn = ttk.Button(self.form_frame, text="Update", command=self.update_student)
        self.update_btn.grid(row=7, column=1, pady=10)
        
        self.delete_btn = ttk.Button(self.form_frame, text="Delete", command=self.delete_student)
        self.delete_btn.grid(row=8, column=0, columnspan=2, pady=5)
        
    def load_students(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, class, section, roll_no FROM students")
        students = cursor.fetchall()
        conn.close()
        
        # Clear existing data
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
            
        # Insert new data
        for student in students:
            self.student_tree.insert('', 'end', values=student)
    
    def add_student(self):
        # Get form data
        name = self.name_entry.get()
        class_ = self.class_entry.get()
        section = self.section_entry.get()
        roll_no = self.roll_no_entry.get()
        father_name = self.father_name_entry.get()
        contact = self.contact_entry.get()
        address = self.address_entry.get("1.0", tk.END).strip()
        admission_date = datetime.now().strftime("%Y-%m-%d")
        
        if not name or not class_:
            messagebox.showerror("Error", "Name and Class are required fields")
            return
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO students 
                          (name, class, section, roll_no, father_name, contact, address, admission_date)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                          (name, class_, section, roll_no, father_name, contact, address, admission_date))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student added successfully")
            self.clear_form()
            self.load_students()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {str(e)}")
    
    def update_student(self):
        selected = self.student_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a student to update")
            return
            
        student_id = self.student_tree.item(selected)['values'][0]
        
        # Get form data
        name = self.name_entry.get()
        class_ = self.class_entry.get()
        section = self.section_entry.get()
        roll_no = self.roll_no_entry.get()
        father_name = self.father_name_entry.get()
        contact = self.contact_entry.get()
        address = self.address_entry.get("1.0", tk.END).strip()
        
        if not name or not class_:
            messagebox.showerror("Error", "Name and Class are required fields")
            return
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''UPDATE students SET
                          name=?, class=?, section=?, roll_no=?, father_name=?, contact=?, address=?
                          WHERE id=?''',
                          (name, class_, section, roll_no, father_name, contact, address, student_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student updated successfully")
            self.load_students()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update student: {str(e)}")
    
    def delete_student(self):
        selected = self.student_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a student to delete")
            return
            
        student_id = self.student_tree.item(selected)['values'][0]
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Student deleted successfully")
                self.clear_form()
                self.load_students()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete student: {str(e)}")
    
    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.class_entry.delete(0, tk.END)
        self.section_entry.delete(0, tk.END)
        self.roll_no_entry.delete(0, tk.END)
        self.father_name_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.address_entry.delete("1.0", tk.END)
        import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import get_db_connection

class StudentManager:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
        self.load_students()
        
    def setup_ui(self):
        # Frame for student list and search
        self.list_frame = ttk.Frame(self.parent)
        self.list_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        # Search frame
        self.search_frame = ttk.Frame(self.list_frame)
        self.search_frame.pack(fill='x', pady=5)
        
        ttk.Label(self.search_frame, text="Search:").pack(side='left')
        self.search_entry = ttk.Entry(self.search_frame, width=30)
        self.search_entry.pack(side='left', padx=5)
        
        self.search_by = ttk.Combobox(self.search_frame, 
                                    values=["Name", "Class", "Section", "Roll No", "Father's Name"],
                                    width=15)
        self.search_by.pack(side='left', padx=5)
        self.search_by.current(0)
        
        self.search_btn = ttk.Button(self.search_frame, text="Search", command=self.search_students)
        self.search_btn.pack(side='left', padx=5)
        
        self.clear_search_btn = ttk.Button(self.search_frame, text="Clear", command=self.load_students)
        self.clear_search_btn.pack(side='left', padx=5)
        
        # Treeview for student list
        self.student_tree = ttk.Treeview(self.list_frame, columns=('id', 'name', 'class', 'section', 'roll_no'), show='headings')
        self.student_tree.heading('id', text='ID')
        self.student_tree.heading('name', text='Name')
        self.student_tree.heading('class', text='Class')
        self.student_tree.heading('section', text='Section')
        self.student_tree.heading('roll_no', text='Roll No')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.student_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.student_tree.configure(yscrollcommand=scrollbar.set)
        
        self.student_tree.pack(fill='both', expand=True)
        
        # Bind treeview selection to fill form
        self.student_tree.bind('<<TreeviewSelect>>', self.on_student_select)
        
        # Frame for student form
        self.form_frame = ttk.Frame(self.parent)
        self.form_frame.pack(side='right', fill='y', padx=10, pady=10)
        
        # Form fields
        ttk.Label(self.form_frame, text="Student Name:").grid(row=0, column=0, sticky='w')
        self.name_entry = ttk.Entry(self.form_frame)
        self.name_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(self.form_frame, text="Class:").grid(row=1, column=0, sticky='w')
        self.class_entry = ttk.Entry(self.form_frame)
        self.class_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(self.form_frame, text="Section:").grid(row=2, column=0, sticky='w')
        self.section_entry = ttk.Entry(self.form_frame)
        self.section_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(self.form_frame, text="Roll No:").grid(row=3, column=0, sticky='w')
        self.roll_no_entry = ttk.Entry(self.form_frame)
        self.roll_no_entry.grid(row=3, column=1, pady=5)
        
        ttk.Label(self.form_frame, text="Father's Name:").grid(row=4, column=0, sticky='w')
        self.father_name_entry = ttk.Entry(self.form_frame)
        self.father_name_entry.grid(row=4, column=1, pady=5)
        
        ttk.Label(self.form_frame, text="Contact:").grid(row=5, column=0, sticky='w')
        self.contact_entry = ttk.Entry(self.form_frame)
        self.contact_entry.grid(row=5, column=1, pady=5)
        
        ttk.Label(self.form_frame, text="Address:").grid(row=6, column=0, sticky='w')
        self.address_entry = tk.Text(self.form_frame, height=3, width=25)
        self.address_entry.grid(row=6, column=1, pady=5)
        
        # Buttons
        self.add_btn = ttk.Button(self.form_frame, text="Add Student", command=self.add_student)
        self.add_btn.grid(row=7, column=0, pady=10)
        
        self.update_btn = ttk.Button(self.form_frame, text="Update", command=self.update_student)
        self.update_btn.grid(row=7, column=1, pady=10)
        
        self.delete_btn = ttk.Button(self.form_frame, text="Delete", command=self.delete_student)
        self.delete_btn.grid(row=8, column=0, columnspan=2, pady=5)
        
    def load_students(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, class, section, roll_no FROM students")
        students = cursor.fetchall()
        conn.close()
        
        self.clear_treeview()
        for student in students:
            self.student_tree.insert('', 'end', values=student)
    
    def search_students(self):
        search_term = self.search_entry.get()
        search_by = self.search_by.get()
        
        if not search_term:
            self.load_students()
            return
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Map search_by to database column
        column_map = {
            "Name": "name",
            "Class": "class",
            "Section": "section",
            "Roll No": "roll_no",
            "Father's Name": "father_name"
        }
        
        column = column_map.get(search_by, "name")
        
        if column == "roll_no":
            try:
                search_term = int(search_term)
                query = f"SELECT id, name, class, section, roll_no FROM students WHERE {column}=?"
            except ValueError:
                messagebox.showerror("Error", "Roll No must be a number")
                return
        else:
            query = f"SELECT id, name, class, section, roll_no FROM students WHERE {column} LIKE ?"
            search_term = f"%{search_term}%"
        
        cursor.execute(query, (search_term,))
        students = cursor.fetchall()
        conn.close()
        
        self.clear_treeview()
        for student in students:
            self.student_tree.insert('', 'end', values=student)
    
    def clear_treeview(self):
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
    
    def on_student_select(self, event):
        selected = self.student_tree.focus()
        if not selected:
            return
            
        student_id = self.student_tree.item(selected)['values'][0]
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
        student = cursor.fetchone()
        conn.close()
        
        if student:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, student[1])
            
            self.class_entry.delete(0, tk.END)
            self.class_entry.insert(0, student[2])
            
            self.section_entry.delete(0, tk.END)
            self.section_entry.insert(0, student[3])
            
            self.roll_no_entry.delete(0, tk.END)
            self.roll_no_entry.insert(0, student[4] if student[4] else "")
            
            self.father_name_entry.delete(0, tk.END)
            self.father_name_entry.insert(0, student[5] if student[5] else "")
            
            self.contact_entry.delete(0, tk.END)
            self.contact_entry.insert(0, student[6] if student[6] else "")
            
            self.address_entry.delete("1.0", tk.END)
            self.address_entry.insert("1.0", student[7] if student[7] else "")
    
    def add_student(self):
        # Get form data
        name = self.name_entry.get()
        class_ = self.class_entry.get()
        section = self.section_entry.get()
        roll_no = self.roll_no_entry.get()
        father_name = self.father_name_entry.get()
        contact = self.contact_entry.get()
        address = self.address_entry.get("1.0", tk.END).strip()
        admission_date = datetime.now().strftime("%Y-%m-%d")
        
        if not name or not class_:
            messagebox.showerror("Error", "Name and Class are required fields")
            return
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO students 
                          (name, class, section, roll_no, father_name, contact, address, admission_date)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                          (name, class_, section, roll_no, father_name, contact, address, admission_date))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student added successfully")
            self.clear_form()
            self.load_students()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {str(e)}")
    
    def update_student(self):
        selected = self.student_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a student to update")
            return
            
        student_id = self.student_tree.item(selected)['values'][0]
        
        # Get form data
        name = self.name_entry.get()
        class_ = self.class_entry.get()
        section = self.section_entry.get()
        roll_no = self.roll_no_entry.get()
        father_name = self.father_name_entry.get()
        contact = self.contact_entry.get()
        address = self.address_entry.get("1.0", tk.END).strip()
        
        if not name or not class_:
            messagebox.showerror("Error", "Name and Class are required fields")
            return
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''UPDATE students SET
                          name=?, class=?, section=?, roll_no=?, father_name=?, contact=?, address=?
                          WHERE id=?''',
                          (name, class_, section, roll_no, father_name, contact, address, student_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student updated successfully")
            self.load_students()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update student: {str(e)}")
    
    def delete_student(self):
        selected = self.student_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a student to delete")
            return
            
        student_id = self.student_tree.item(selected)['values'][0]
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Student deleted successfully")
                self.clear_form()
                self.load_students()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete student: {str(e)}")
    
    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.class_entry.delete(0, tk.END)
        self.section_entry.delete(0, tk.END)
        self.roll_no_entry.delete(0, tk.END)
        self.father_name_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.address_entry.delete("1.0", tk.END)
        