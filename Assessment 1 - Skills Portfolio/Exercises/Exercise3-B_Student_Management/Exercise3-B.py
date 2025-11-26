#Student Manager | Exercise3-B
import tkinter as tk
from tkinter import ttk, messagebox

#Set up main window
def setup_window():
    root.title('Student Manager')
    root.geometry('1080x720')
    root.config(bg="#bbc7ff")
    root.resizable(False, False)

#Clear content area
def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

#Load student marks from StudentMarks.txt
def load_marks():
    global students
    students = []
    try:
        with open('../../A1 - Resources/studentMarks.txt', 'r') as file:
            lines = file.readlines()
        
        #Skip first header line and proceed to each record
        for i in range(1, len(lines)):
            line = lines[i].strip()
            if not line:
                continue
            parts = line.split(',')
            
            #Store student info in dictionary
            students.append({
                'number': parts[0],
                'name': parts[1],
                'cw1': int(parts[2]),
                'cw2': int(parts[3]),
                'cw3': int(parts[4]),
                'exam': int(parts[5])
            })
    except FileNotFoundError:
        messagebox.showerror('Error', 'Student marks file not found')
    except Exception as e:
        messagebox.showerror('Error',f'Error loading file, {str(0)}')

#Write on .txt file keeping info, function to be called after add/delete/update
def save_marks():
    try:
        with open('../../A1 - Resources/studentMarks.txt', 'w') as file:
            file.write('Student Number,Student Name,CW1,CW2,CW3,Examp\n')
            for student in students:
                file.write(f"{student['number']},{student['name']},{student['cw1']},{student['cw2']},{student['cw3']},{student['exam']}\n")
        return True
    except Exception as e:
        messagebox.showerror('Error', f'Could not save to file, {str(0)}')
        return False


#Calculate percentage of coursework and exam for student
def get_percentage(student):
    cw_total = student['cw1'] + student['cw2'] + student['cw3']
    total = cw_total + student['exam']
    percentage = (total / 160) * 100
    return percentage

#Return grade based on percentage
def get_grade(percentage):
    if percentage >= 70:
        return 'A'
    elif percentage >= 60:
        return 'B'
    elif percentage >= 50:
        return 'C'
    elif percentage >= 40:
        return 'D'
    else:
        return 'F'

#View all students in table with average summary
def view_all_students():
    clear_content()
    
    title = tk.Label(content_frame, text='All Student Records', bg='#bbc7ff', fg='#000000', font=('Arial', 22, 'bold'))
    title.pack(pady=15)
    
    table_frame = tk.Frame(content_frame, bg="#bbc7ff")
    table_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    #Create Treeview with student information
    columns = ('Number', 'Name', 'CW1', 'CW2', 'CW3', 'Total Coursework', 'Exam', 'Percentage', 'Grade')
    tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
    
    #Column headers
    for col in columns:
        tree.heading(col, text=col if col in ['CW1', 'CW2', 'CW3'] else col.replace('_', ' ').title())
    
    #Column width sizes
    widths = {'Number': 90, 'Name': 160, 'CW1': 30, 'CW2': 30, 'CW3': 30, 'Total Coursework': 100, 'Exam': 60, 'Percentage': 60, 'Grade': 30}
    for col, width in widths.items():
        tree.column(col, width=width)
    
    #Add scrollbar
    scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    #Insert student data into table
    total_percent = 0
    for student in students:
        cw_total = student['cw1'] + student['cw2'] + student['cw3']
        percentage = get_percentage(student)
        grade = get_grade(percentage)
        total_percent += percentage
        
        tree.insert('', 'end', values=(student['number'], student['name'], student['cw1'], student['cw2'], student['cw3'], f"{cw_total}/60", f"{student['exam']}/100", f"{percentage:.1f}%", grade))
    
    tree.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    
    #Average summary
    if students:
        avg_percent = total_percent / len(students)
        summary = tk.Label(content_frame, text=f"Total Students: {len(students)}  Average: {avg_percent:.1f}%", bg='#3498db', fg='white', font=('Arial', 12, 'bold'), pady=10)
        summary.pack(fill='x', padx=20, pady=10)

#Search and view individual student
def view_indiv_student():
    clear_content()
    
    title = tk.Label(content_frame, text='View Individual Student', bg='#bbc7ff', fg='#000000', font=('Arial', 22, 'bold'))
    title.pack(pady=15)
    
    search_frame = tk.Frame(content_frame, bg='#bbc7ff')
    search_frame.pack(pady=20)
    
    tk.Label(search_frame, text='Select or Type Student Name:', bg='#bbc7ff', font=('Arial', 12)).pack(pady=5)
    
    #Dropdown with all student names
    student_names = sorted([student['name'] for student in students])
    selected_name = tk.StringVar()
    dropdown = ttk.Combobox(search_frame, textvariable=selected_name, values=student_names, font=('Arial', 11), width=30, state='normal')
    dropdown.pack(pady=10)
    
    result_frame = tk.Frame(content_frame, bg='#bbc7ff')
    result_frame.pack(pady=20, fill='both', expand=True, padx=40)
    
    #For when search is clicked
    def search_student():
        search_text = selected_name.get().strip()
        
        #Clear old search
        for widget in result_frame.winfo_children():
            widget.destroy()
        
        if not search_text:
            tk.Label(result_frame, text='Please select or enter a student name', bg='#bbc7ff', fg='#e74c3c', font=('Arial', 12, 'bold')).pack(pady=20)
            return
        
        #Search for student, case insensitive
        found_student = next((s for s in students if search_text.lower() in s['name'].lower()), None)
        
        #Display student's info in small frame
        if found_student:
            display_student_info(result_frame, found_student)
        else:
            tk.Label(result_frame, text='Student not found.', bg='#bbc7ff', fg='#e74c3c', font=('Arial', 12, 'bold')).pack(pady=20)
    
    search_btn = tk.Button(search_frame, text='Search', bg='#3498db', fg='white', activebackground='#45a7e9', font=('Arial', 12, 'bold'), width=12, bd=0, cursor='hand2', command=search_student)
    search_btn.pack(pady=10)

#Detailed information of student, used in multiple functions
def display_student_info(parent_frame, student):
    info_box = tk.Frame(parent_frame, bg='white', relief='solid', bd=2)
    info_box.pack(pady=20, padx=20, fill='x')
    
    #Calculate to get grade
    cw_total = student['cw1'] + student['cw2'] + student['cw3']
    percentage = get_percentage(student)
    grade = get_grade(percentage)
    
    #Display student details in a format 
    tk.Label(info_box, text=f"Name: {student['name']}", bg='white', font=('Arial', 14, 'bold')).pack(anchor='w', padx=15, pady=8)
    tk.Label(info_box, text=f"Student Number: {student['number']}", bg='white', font=('Arial', 12)).pack(anchor='w', padx=15, pady=4)
    tk.Label(info_box, text=f"CW1: {student['cw1']}/20", bg='white', font=('Arial', 12)).pack(anchor='w', padx=15, pady=4)
    tk.Label(info_box, text=f"CW2: {student['cw2']}/20", bg='white', font=('Arial', 12)).pack(anchor='w', padx=15, pady=4)
    tk.Label(info_box, text=f"CW3: {student['cw3']}/20", bg='white', font=('Arial', 12)).pack(anchor='w', padx=15, pady=4)
    tk.Label(info_box, text=f"Total Coursework: {cw_total}/60", bg='white', font=('Arial', 12)).pack(anchor='w', padx=15, pady=4)
    tk.Label(info_box, text=f"Exam Mark: {student['exam']}/100", bg='white', font=('Arial', 12)).pack(anchor='w', padx=15, pady=4)
    tk.Label(info_box, text=f"Overall Percentage: {percentage:.1f}%", bg='white', font=('Arial', 12)).pack(anchor='w', padx=15, pady=4)
    tk.Label(info_box, text=f"Grade: {grade}", bg='white', font=('Arial', 14, 'bold'), fg='#27ae60').pack(anchor='w', padx=15, pady=8)

#Show a student with highest overall percentage
def show_high_score():
    clear_content()
    
    title = tk.Label(content_frame, text='Student with Highest Overall Mark', bg='#bbc7ff', fg='#000000', font=('Arial', 22, 'bold'))
    title.pack(pady=15)
    
    result_frame = tk.Frame(content_frame, bg='#bbc7ff')
    result_frame.pack(pady=20, fill='both', expand=True, padx=40)
    
    #Finds student with highest percentage
    top_student = max(students, key=lambda x: get_percentage(x))
    display_student_info(result_frame, top_student)

#Show a student with lowest overall percentage
def show_low_score():
    clear_content()
    
    title = tk.Label(content_frame, text='Student with Highest Overall Mark', bg='#bbc7ff', fg='#000000', font=('Arial', 22, 'bold'))
    title.pack(pady=15)
    
    result_frame = tk.Frame(content_frame, bg='#bbc7ff')
    result_frame.pack(pady=20, fill='both', expand=True, padx=40)
    
    #Finds student with lowest percentage
    top_student = min(students, key=lambda x: get_percentage(x))
    display_student_info(result_frame, top_student)

#Sort student records by name or percentage
def sort_records():
    clear_content()
    
    tk.Label(content_frame, text="Sort Student Records", bg="#bbc7ff", font=("Arial", 22, "bold")).pack(pady=15)
    
    sort_frame = tk.Frame(content_frame, bg="#bbc7ff")
    sort_frame.pack(pady=20)
    
    #Sort criteria Selection
    tk.Label(sort_frame, text="Sort By:", bg="#bbc7ff", font=("Arial", 12)).pack(pady=5)
    sort_key = tk.StringVar(value="Name")
    sort_dropdown = ttk.Combobox(sort_frame, textvariable=sort_key, values=["Name", "Percentage"], state="readonly", width=20)
    sort_dropdown.pack(pady=5)
    sort_dropdown.current(0)

    #Sort order selection 
    tk.Label(sort_frame, text="Order:", bg="#bbc7ff", font=("Arial", 12)).pack(pady=5)
    sort_order = tk.StringVar(value="Ascending")
    order_dropdown = ttk.Combobox(sort_frame, textvariable=sort_order, values=["Ascending", "Descending"], state="readonly", width=20)
    order_dropdown.pack(pady=5)
    order_dropdown.current(0)
    
    #Apply sort and display result
    def apply_sort():
        key = sort_key.get()
        order = sort_order.get()
        
        #if selections are valid
        if not key or not order:
            messagebox.showwarning("Warning", "Please select both sort criteria and order")
            return
        
        #Apply different logic for name and percentage
        if key == "Name":
            reverse = (order == "Descending")  
        else:
            reverse = (order == "Ascending")
        
        #Sort by name (alphabetically) or percentage (numerically)
        if key == "Name":
            sorted_list = sorted(students, key=lambda x: x["name"].lower(), reverse=reverse)
        else:  #Percentage
            sorted_list = sorted(students, key=lambda x: get_percentage(x), reverse=reverse)
        
        show_sorted_results(sorted_list)
    
    tk.Button(sort_frame, text="Apply Sort", bg="#3498db", fg="white", font=("Arial", 12, "bold"), width=15, cursor="hand2", command=apply_sort)

#Display sorted results
def show_sorted_results(sorted_list):
    clear_content()
    
    title = tk.Label(content_frame, text='Sorted Student Records', bg='#bbc7ff', fg='#000000', font=('Arial', 22, 'bold'))
    title.pack(pady=15)
    
    table_frame = tk.Frame(content_frame, bg="#bbc7ff")
    table_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    columns = ('Number', 'Name', 'CW1', 'CW2', 'CW3', 'Total Coursework', 'Exam', 'Percentage', 'Grade')
    tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
    
    for col in columns:
        tree.heading(col, text=col)
    
    widths = {'Number': 90, 'Name': 160, 'CW1': 30, 'CW2': 30, 'CW3': 30, 'Total Coursework': 100, 'Exam': 60, 'Percentage': 60, 'Grade': 30}
    for col, width in widths.items():
        tree.column(col, width=width)
    
    scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    #Input sorted data
    for student in sorted_list:
        cw_total = student['cw1'] + student['cw2'] + student['cw3']
        percentage = get_percentage(student)
        grade = get_grade(percentage)
        
        tree.insert('', 'end', values=(
            student['number'], student['name'], student['cw1'], student['cw2'], student['cw3'], f"{cw_total}/60", f"{student['exam']}/100", f"{percentage:.1f}%", grade))
    tree.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

#Make form to create, to add student record
def add_student():
    clear_content()
    
    tk.Label(content_frame, text="Add New Student", bg="#bbc7ff", font=("Arial", 22, "bold")).pack(pady=15)
    
    form_frame = tk.Frame(content_frame, bg="#bbc7ff")
    form_frame.pack(pady=20)
    
    #Create input fields for all student information
    fields = ['Student Number', 'Student Name', 'CW1 (0-20)', 'CW2 (0-20)', 'CW3 (0-20)', 'Exam (0-100)']
    entries = {}
    
    for field in fields:
        field_frame = tk.Frame(form_frame, bg="#bbc7ff")
        field_frame.pack(pady=8)
        
        tk.Label(field_frame, text=f"{field}:", bg="#bbc7ff", font=("Arial", 11), width=18, anchor='e').pack(side='left', padx=5)
        entry = tk.Entry(field_frame, font=("Arial", 11), width=25)
        entry.pack(side='left', padx=5)
        entries[field] = entry
    
    #Save the new student record
    def save_student():
        try:
            #Validate input values
            num = entries['Student Number'].get().strip()
            name = entries['Student Name'].get().strip()
            cw1 = int(entries['CW1 (0-20)'].get())
            cw2 = int(entries['CW2 (0-20)'].get())
            cw3 = int(entries['CW3 (0-20)'].get())
            exam = int(entries['Exam (0-100)'].get())
            
            #Validation checks
            if not num or not name:
                messagebox.showerror("Error", "Student number and name are required")
                return
            
            #Check for duplicate student number
            if any(s['number'] == num for s in students):
                messagebox.showerror("Error", "Student number already exists")
                return
            
            #Validate mark ranges
            if not (0 <= cw1 <= 20 and 0 <= cw2 <= 20 and 0 <= cw3 <= 20):
                messagebox.showerror("Error", "Coursework marks must be between 0 and 20")
                return
            
            if not (0 <= exam <= 100):
                messagebox.showerror("Error", "Exam mark must be between 0 and 100")
                return
            
            #Add new student to record and save to file
            students.append({
                'number': num, 'name': name, 'cw1': cw1, 'cw2': cw2, 'cw3': cw3, 'exam': exam})
            
            if save_marks():
                messagebox.showinfo("Success", f"Student {name} added successfully")
                view_all_students()
        
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for marks")
    
    #Form buttons
    btn_frame = tk.Frame(form_frame, bg="#bbc7ff")
    btn_frame.pack(pady=20)
    
    tk.Button(btn_frame, text="Save Student", bg="#27ae60", fg="white",  font=("Arial", 11, "bold"), width=15, cursor="hand2", command=save_student).pack(side='left', padx=5)
    tk.Button(btn_frame, text="Cancel", bg="#e74c3c", fg="white",  font=("Arial", 11, "bold"), width=15, cursor="hand2", command=view_all_students).pack(side='left', padx=5)

#Select and delete a student record
def delete_student():
    clear_content()
    
    tk.Label(content_frame, text="Delete Student Record", bg="#bbc7ff", font=("Arial", 22, "bold")).pack(pady=15)
    
    search_frame = tk.Frame(content_frame, bg='#bbc7ff')
    search_frame.pack(pady=20)
    
    tk.Label(search_frame, text='Select Student to Delete:', bg='#bbc7ff', font=('Arial', 12)).pack(pady=5)
    
    #Dropdown showing students with their numbers for identification
    student_options = [f"{s['number']} - {s['name']}" for s in students]
    selected = tk.StringVar()
    dropdown = ttk.Combobox(search_frame, textvariable=selected, values=student_options, font=('Arial', 11), width=35, state='readonly')
    dropdown.pack(pady=10)
    
    #Confirm and execute deletion
    def confirm_delete():
        if not selected.get():
            messagebox.showwarning("Warning", "Please select a student")
            return
        
        #Extract student number from selection
        student_num = selected.get().split(' - ')[0]
        student = next((s for s in students if s['number'] == student_num), None)
        
        if student:
            #Confirmation before deleting
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {student['name']}?"):
                students.remove(student)
                if save_marks():
                    messagebox.showinfo("Success", "Student deleted successfully")
                    view_all_students()
    
    tk.Button(search_frame, text="Delete Student", bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), width=15, cursor="hand2", command=confirm_delete).pack(pady=10)

#Select student and update their information
def update_student():
    clear_content()
    
    tk.Label(content_frame, text="Update Student Record", bg="#bbc7ff", font=("Arial", 22, "bold")).pack(pady=15)
    
    search_frame = tk.Frame(content_frame, bg='#bbc7ff')
    search_frame.pack(pady=20)
    
    tk.Label(search_frame, text='Select Student to Update:', bg='#bbc7ff', font=('Arial', 12)).pack(pady=5)
    
    student_options = [f"{s['number']} - {s['name']}" for s in students]
    selected = tk.StringVar()
    dropdown = ttk.Combobox(search_frame, textvariable=selected, values=student_options, font=('Arial', 11), width=35, state='readonly')
    dropdown.pack(pady=10)
    
    form_frame = tk.Frame(content_frame, bg='#bbc7ff')
    form_frame.pack(pady=20)
    
    #Form fields for updating, disabled initially 
    fields_info = [
        ('Student Name', 'name'),
        ('CW1 (0-20)', 'cw1'),
        ('CW2 (0-20)', 'cw2'),
        ('CW3 (0-20)', 'cw3'),
        ('Exam (0-100)', 'exam')
    ]
    
    entries = {}
    for label, key in fields_info:
        field_frame = tk.Frame(form_frame, bg='#bbc7ff')
        field_frame.pack(pady=8)
        
        tk.Label(field_frame, text=f"{label}:", bg="#bbc7ff", font=("Arial", 11), width=18, anchor='e').pack(side='left', padx=5)
        entry = tk.Entry(field_frame, font=("Arial", 11), width=25, state='disabled')
        entry.pack(side='left', padx=5)
        entries[key] = entry
    
    current_student = [None]  #Use list to store reference in nested function
    
    #Load selected student's data into form fields
    def load_student():
        if not selected.get():
            return
        
        student_num = selected.get().split(' - ')[0]
        student = next((s for s in students if s['number'] == student_num), None)
        
        if student:
            current_student[0] = student
            #Enable and input form fields
            for key, entry in entries.items():
                entry.config(state='normal')
                entry.delete(0, tk.END)
                entry.insert(0, str(student[key]))
    
    #Validate and save updated information
    def save_update():
        if not current_student[0]:
            messagebox.showwarning("Warning", "Please select a student first")
            return
        
        try:
            name = entries['name'].get().strip()
            cw1 = int(entries['cw1'].get())
            cw2 = int(entries['cw2'].get())
            cw3 = int(entries['cw3'].get())
            exam = int(entries['exam'].get())
            
            if not name:
                messagebox.showerror("Error", "Student name cannot be empty")
                return
            
            if not (0 <= cw1 <= 20 and 0 <= cw2 <= 20 and 0 <= cw3 <= 20):
                messagebox.showerror("Error", "Coursework marks must be between 0 and 20")
                return
            
            if not (0 <= exam <= 100):
                messagebox.showerror("Error", "Exam mark must be between 0 and 100")
                return
            
            #Update student record
            current_student[0]['name'] = name
            current_student[0]['cw1'] = cw1
            current_student[0]['cw2'] = cw2
            current_student[0]['cw3'] = cw3
            current_student[0]['exam'] = exam
            
            if save_marks():
                messagebox.showinfo("Success", "Student updated successfully")
                view_all_students()
        
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for marks")
    
    #Buttons for Updating
    btn_frame = tk.Frame(search_frame, bg="#bbc7ff")
    btn_frame.pack(pady=10)
    
    tk.Button(btn_frame, text="Load Student", bg="#3498db", fg="white", font=("Arial", 11, "bold"), width=15, cursor="hand2", command=load_student).pack(side='left', padx=5)
    
    save_btn_frame = tk.Frame(form_frame, bg="#bbc7ff")
    save_btn_frame.pack(pady=20)
    
    tk.Button(save_btn_frame, text="Save Changes", bg="#27ae60", fg="white", font=("Arial", 11, "bold"), width=15, cursor="hand2", command=save_update).pack(side='left', padx=5)
    
    tk.Button(save_btn_frame, text="Cancel", bg="#e74c3c", fg="white", font=("Arial", 11, "bold"), width=15, cursor="hand2", command=view_all_students).pack(side='left', padx=5)

#Show welcome screen on startup
def show_welcome():
    clear_content()
    welcome = tk.Label(content_frame, text='Welcome to Student Manager', bg='#bbc7ff', fg='#000000', font=('Arial', 26, 'bold'))
    welcome.pack(expand=True)

#Initialize main window
root = tk.Tk()
setup_window()

#Create sidebar
sidebar = tk.Frame(root, bg='#3c3c3c', width=270)
sidebar.pack(side='left', fill='y')
sidebar.pack_propagate(False)

sidebar_title = tk.Label(sidebar, text='Student Manager', bg='#3c3c3c', fg='white', font=('Arial', 18, 'bold'))
sidebar_title.pack(pady=20)

#Define all menu buttons with their respective commands
menu_buttons = [
    ('View All Students', view_all_students),
    ('View Individual Student', view_indiv_student),
    ('Highest Overall Student', show_high_score),
    ('Lowest Overall Student', show_low_score),
    ('Sort Records', sort_records),
    ('Add Student', add_student),
    ('Delete Student', delete_student),
    ('Update Student', update_student)
]

#Create dynamic menu buttons 
for text, command in menu_buttons:
    btn = tk.Button(sidebar, text=text, bg='#3498db', fg='white', activebackground='#45a7e9', font=('Arial', 12, 'bold'), width=22, height=3, bd=0, cursor='hand2', command=command)
    btn.pack(pady=2, padx=10)

#Quit Button
quit_btn = tk.Button(sidebar, text='Quit', bg='#c91d19', fg='white', activebackground="#e74e4b", font=('Arial', 12, 'bold'), width=22, height=2, bd=0, cursor='hand2', command=root.quit)
quit_btn.pack(side='bottom', pady=10, padx=10)

#Display main content
content_frame = tk.Frame(root, bg='#bbc7ff')
content_frame.pack(side='right', fill='both', expand=True)

#Load student data and show welcome screen, then start app
load_marks()
show_welcome()
root.mainloop()