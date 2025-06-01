import tkinter as tk
from tkinter import ttk, messagebox
from database import get_db_connection
from tkinter import filedialog
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class ReportGenerator:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        # Report selection frame
        self.report_frame = ttk.LabelFrame(self.parent, text="Generate Reports")
        self.report_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Report type selection
        ttk.Label(self.report_frame, text="Select Report Type:").grid(row=0, column=0, sticky='w')
        self.report_type = ttk.Combobox(self.report_frame, values=[
            "Student List",
            "Fee Structure",
            "Payment History",
            "Fee Defaulters"
        ])
        self.report_type.grid(row=0, column=1, pady=5, sticky='ew')
        
        # Filters
        self.filter_frame = ttk.Frame(self.report_frame)
        self.filter_frame.grid(row=1, column=0, columnspan=2, sticky='ew')
        
        ttk.Label(self.filter_frame, text="Class:").pack(side='left')
        self.filter_class = ttk.Entry(self.filter_frame, width=15)
        self.filter_class.pack(side='left', padx=5)
        
        # Generate button
        self.generate_btn = ttk.Button(self.report_frame, text="Generate Report", command=self.generate_report)
        self.generate_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Export buttons
        self.export_excel_btn = ttk.Button(self.report_frame, text="Export to Excel", command=lambda: self.export_report('excel'))
        self.export_excel_btn.grid(row=3, column=0, pady=5)
        
        self.export_pdf_btn = ttk.Button(self.report_frame, text="Export to PDF", command=lambda: self.export_report('pdf'))
        self.export_pdf_btn.grid(row=3, column=1, pady=5)
    
    def generate_report(self):
        report_type = self.report_type.get()
        if not report_type:
            messagebox.showerror("Error", "Please select a report type")
            return
            
        class_filter = self.filter_class.get()
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            if report_type == "Student List":
                if class_filter:
                    cursor.execute("SELECT id, name, class, section, roll_no, contact FROM students WHERE class=?", (class_filter,))
                else:
                    cursor.execute("SELECT id, name, class, section, roll_no, contact FROM students")
                data = cursor.fetchall()
                columns = ['ID', 'Name', 'Class', 'Section', 'Roll No', 'Contact']
                
            elif report_type == "Fee Structure":
                if class_filter:
                    cursor.execute("SELECT class, fee_type, amount, due_date FROM fee_structure WHERE class=?", (class_filter,))
                else:
                    cursor.execute("SELECT class, fee_type, amount, due_date FROM fee_structure")
                data = cursor.fetchall()
                columns = ['Class', 'Fee Type', 'Amount', 'Due Date']
                
            elif report_type == "Payment History":
                if class_filter:
                    cursor.execute('''SELECT p.receipt_no, s.name, s.class, p.fee_type, p.amount, p.payment_date 
                                  FROM payments p
                                  JOIN students s ON p.student_id = s.id
                                  WHERE s.class=?''', (class_filter,))
                else:
                    cursor.execute('''SELECT p.receipt_no, s.name, s.class, p.fee_type, p.amount, p.payment_date 
                                  FROM payments p
                                  JOIN students s ON p.student_id = s.id''')
                data = cursor.fetchall()
                columns = ['Receipt No', 'Student Name', 'Class', 'Fee Type', 'Amount', 'Payment Date']
                
            elif report_type == "Fee Defaulters":
                # This is a simplified version - in a real system you'd need to compare payments against fee structure
                cursor.execute('''SELECT s.id, s.name, s.class, s.section, s.roll_no
                              FROM students s
                              WHERE NOT EXISTS (
                                  SELECT 1 FROM payments p 
                                  WHERE p.student_id = s.id
                                  AND p.payment_date >= date('now', '-1 month')
                              ''')
                data = cursor.fetchall()
                columns = ['ID', 'Name', 'Class', 'Section', 'Roll No']
                
            conn.close()
            
            if not data:
                messagebox.showinfo("Info", "No data found for the selected report")
                return
                
            # Display data in a new window
            self.display_report(columns, data)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def display_report(self, columns, data):
        report_window = tk.Toplevel(self.parent)
        report_window.title("Report Preview")
        report_window.geometry("800x600")
        
        # Create treeview
        tree = ttk.Treeview(report_window, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # Insert data
        for row in data:
            tree.insert('', 'end', values=row)
        
        tree.pack(fill='both', expand=True)
    
    def export_report(self, format_type):
        report_type = self.report_type.get()
        if not report_type:
            messagebox.showerror("Error", "Please select a report type")
            return
            
        class_filter = self.filter_class.get()
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            if report_type == "Student List":
                if class_filter:
                    cursor.execute("SELECT id, name, class, section, roll_no, contact FROM students WHERE class=?", (class_filter,))
                else:
                    cursor.execute("SELECT id, name, class, section, roll_no, contact FROM students")
                data = cursor.fetchall()
                columns = ['ID', 'Name', 'Class', 'Section', 'Roll No', 'Contact']
                
            elif report_type == "Fee Structure":
                if class_filter:
                    cursor.execute("SELECT class, fee_type, amount, due_date FROM fee_structure WHERE class=?", (class_filter,))
                else:
                    cursor.execute("SELECT class, fee_type, amount, due_date FROM fee_structure")
                data = cursor.fetchall()
                columns = ['Class', 'Fee Type', 'Amount', 'Due Date']
                
            elif report_type == "Payment History":
                if class_filter:
                    cursor.execute('''SELECT p.receipt_no, s.name, s.class, p.fee_type, p.amount, p.payment_date 
                                  FROM payments p
                                  JOIN students s ON p.student_id = s.id
                                  WHERE s.class=?''', (class_filter,))
                else:
                    cursor.execute('''SELECT p.receipt_no, s.name, s.class, p.fee_type, p.amount, p.payment_date 
                                  FROM payments p
                                  JOIN students s ON p.student_id = s.id''')
                data = cursor.fetchall()
                columns = ['Receipt No', 'Student Name', 'Class', 'Fee Type', 'Amount', 'Payment Date']
                
            conn.close()
            
            if not data:
                messagebox.showinfo("Info", "No data found for the selected report")
                return
                
            # Ask for save location
            file_path = filedialog.asksaveasfilename(
                defaultextension=f".{format_type}",
                filetypes=[(f"{format_type.upper()} files", f"*.{format_type}")],
                title="Save report as"
            )
            
            if not file_path:
                return  # User cancelled
            
            if format_type == 'excel':
                df = pd.DataFrame(data, columns=columns)
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Success", f"Report exported to Excel successfully")
                
            elif format_type == 'pdf':
                doc = SimpleDocTemplate(file_path, pagesize=letter)
                elements = []
                
                # Add title
                styles = getSampleStyleSheet()
                title = Paragraph(f"{report_type} Report", styles['Title'])
                elements.append(title)
                
                # Add data table
                table_data = [columns] + list(data)
                table = Table(table_data)
                
                # Add style
                style = TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.grey),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0,0), (-1,0), 12),
                    ('BOTTOMPADDING', (0,0), (-1,0), 12),
                    ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                    ('GRID', (0,0), (-1,-1), 1, colors.black)
                ])
                table.setStyle(style)
                elements.append(table)
                
                doc.build(elements)
                messagebox.showinfo("Success", f"Report exported to PDF successfully")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")