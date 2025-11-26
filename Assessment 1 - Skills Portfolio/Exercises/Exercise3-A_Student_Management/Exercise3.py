#Student Manager
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
        file = open('../../A1 - Resources/studentMarks.txt', 'r')
        lines = file.readlines()
        file.close()
        
        #Skip first header line and proceed to each record
        for i in range(1, len(lines)):
            line = lines[i].strip()
            parts = line.split(',')
            
            student_num = parts[0]
            student_name = parts[1]
            cw1 = int(parts[2])
            cw2 = int(parts[3])
            cw3 = int(parts[4])
            exam = int(parts[5])
            
            #Store student info in dictionary
            students.append({
                'number': student_num,
                'name': student_name,
                'cw1': cw1,
                'cw2': cw2,
                'cw3': cw3,
                'exam': exam
            })
    except:
        messagebox.showerror('Error', 'Student marks file not found')

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

#View all students in table with average 
def view_all_students():
    clear_content()
    
    title = tk.Label(content_frame, text='All Student Records', bg='#bbc7ff', fg='#000000', font=('Arial', 22, 'bold'))
    title.pack(pady=15)
    
    table_frame = tk.Frame(content_frame, bg="#bbc7ff")
    table_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    #Create Treeview
    columns = ('Number', 'Name', 'CW1', 'CW2', 'CW3', 'Total Coursework', 'Exam', 'Percentage', 'Grade')
    tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
    
    #Column headers
    tree.heading('Number', text='Student Number')
    tree.heading('Name', text='Student Name')
    tree.heading('CW1', text='CW1')
    tree.heading('CW2', text='CW2')
    tree.heading('CW3', text='CW3')
    tree.heading('Total Coursework', text='Total Coursework')
    tree.heading('Exam', text='Exam Mark')
    tree.heading('Percentage', text='Percentage')
    tree.heading('Grade', text='Grade')
    
    #Column width sizes
    tree.column('Number', width=90)
    tree.column('Name', width=160)
    tree.column('CW1', width=30)
    tree.column('CW2', width=30)
    tree.column('CW3', width=30)
    tree.column('Total Coursework', width=100)
    tree.column('Exam', width=60)
    tree.column('Percentage', width=60)
    tree.column('Grade', width=30)
    
    #Add scrollbar
    scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    #Insert student data into table
    total_percent = 0
    for student in students:
        cw_total = student['cw1'] + student['cw2'] + student['cw3']
        percentage = get_percentage(student)
        grade = get_grade(percentage)
        total_percent = total_percent + percentage
        
        tree.insert('', 'end', values=(
            student['number'],
            student['name'],
            student['cw1'],
            student['cw2'],
            student['cw3'],
            f"{cw_total}/60",
            f"{student['exam']}/100",
            f"{percentage:.1f}%",
            grade
        ))
    
    tree.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    
    #Average summary
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
        
        if search_text == '':
            tk.Label(result_frame, text='Please select or enter a student name!', bg='#bbc7ff', fg='#e67e22', font=('Arial', 12, 'bold')).pack(pady=20)
            return
        
        #Search for student, case insensitive
        found_student = None
        for student in students:
            if search_text.lower() in student['name'].lower():
                found_student = student
                break
        
        if found_student:
            #Display student's info in small frame
            info_box = tk.Frame(result_frame, bg='white', relief='solid', bd=2)
            info_box.pack(pady=20, padx=20, fill='x')
            
            cw_total = found_student['cw1'] + found_student['cw2'] + found_student['cw3']
            percentage = get_percentage(found_student)
            grade = get_grade(percentage)
            tk.Label(info_box, text=f"Name: {found_student['name']}", bg='white', font=('Arial', 14, 'bold')).pack(anchor='w', padx=15, pady=8)
            tk.Label(info_box, text=f"Student Number: {found_student['number']}", bg='white', font=('Arial', 12)).pack(anchor='w', padx=15, pady=4)
            tk.Label(info_box, text=f"CW1: {found_student['cw1']}", bg='white',font=('Arial', 12)).pack(anchor='w', padx=15, pady=4)
            tk.Label(info_box, text=f"CW2: {found_student['cw2']}", bg='white',font=('Arial', 12)).pack(anchor='w', padx=15, pady=4)
            tk.Label(info_box, text=f"CW3: {found_student['cw3']}", bg='white',font=('Arial', 12)).pack(anchor='w', padx=15, pady=4)
            tk.Label(info_box, text=f"Total Coursework: {cw_total}", bg='white',font=('Arial', 12)).pack(anchor='w', padx=15, pady=4)
            tk.Label(info_box, text=f"Exam Mark: {found_student['exam']}/100", bg='white', font=('Arial', 12)).pack(anchor='w', padx=15, pady=4)
            tk.Label(info_box, text=f"Overall Percentage: {percentage:.1f}%", bg='white', font=('Arial', 12)).pack(anchor='w', padx=15, pady=4)
            tk.Label(info_box, text=f"Grade: {grade}", bg='white', font=('Arial', 14, 'bold'), fg='#27ae60').pack(anchor='w', padx=15, pady=8)
        else:
            tk.Label(result_frame, text='Student not found.', bg='#bbc7ff', fg='#e74c3c', font=('Arial', 12, 'bold')).pack(pady=20)
    
    search_btn = tk.Button(search_frame, text='Search', bg='#3498db', fg='white', activebackground='#45a7e9', font=('Arial', 12, 'bold'), width=12, bd=0, cursor='hand2', command=search_student)
    search_btn.pack(pady=10)

#Same format with view_indiv_student, to display student info
def student_infoframe(student):
    result_frame = tk.Frame(content_frame, bg='#bbc7ff')
    result_frame.pack(pady=20, fill='both', expand=True, padx=40)

    info_box = tk.Frame(result_frame, bg='white', relief='solid', bd=2)
    info_box.pack(pady=20, padx=20, fill='x')

    cw_total = student['cw1'] + student['cw2'] + student['cw3']
    percentage = get_percentage(student)
    grade = get_grade(percentage)

    tk.Label(info_box, text=f"Name: {student['name']}", bg='white',font=('Arial', 14, 'bold')).pack(anchor='w', padx=15, pady=8)
    tk.Label(info_box, text=f"Student Number: {student['number']}", bg='white',font=('Arial', 12)).pack(anchor='w', padx=15, pady=4)
    tk.Label(info_box, text=f"CW1: {student['cw1']}", bg='white', font=('Arial', 12)).pack(anchor='w', padx=15, pady=4)
    tk.Label(info_box, text=f"CW2: {student['cw2']}", bg='white', font=('Arial', 12)).pack(anchor='w', padx=15, pady=4)
    tk.Label(info_box, text=f"CW3: {student['cw3']}", bg='white', font=('Arial', 12)).pack(anchor='w', padx=15, pady=4)
    tk.Label(info_box, text=f"Total Coursework: {cw_total}", bg='white', font=('Arial', 12)).pack(anchor='w', padx=15, pady=4)
    tk.Label(info_box, text=f"Exam Mark: {student['exam']}/100", bg='white', font=('Arial', 12)).pack(anchor='w', padx=15, pady=4)
    tk.Label(info_box, text=f"Overall Percentage: {percentage:.1f}%", bg='white', font=('Arial', 12)).pack(anchor='w', padx=15, pady=4)
    tk.Label(info_box, text=f"Grade: {grade}", bg='white', font=('Arial', 14, 'bold'), fg='#27ae60').pack(anchor='w', padx=15, pady=8)

#Show a student with highest overall percentage
def show_high_score():
    clear_content()
    
    title = tk.Label(content_frame, text='Student with Highest Overall Mark', bg='#bbc7ff', fg='#000000', font=('Arial', 22, 'bold'))
    title.pack(pady=15)

    #Finds student with higest percentage
    top_student = max(students, key=lambda x: get_percentage(x))

    student_infoframe(top_student)

#Show a student with lowest overall percentage
def show_low_score():
    clear_content()
    
    title = tk.Label(content_frame, text='Student with Lowest Overall Mark', 
                    bg='#bbc7ff', fg='#000000', font=('Arial', 22, 'bold'))
    title.pack(pady=15)

    #Finds student with lowest percentage
    top_student = min(students, key=lambda x: get_percentage(x))

    student_infoframe(top_student)

#Show welcome screen
def show_welcome():
    clear_content()
    welcome = tk.Label(content_frame, text='Welcome to Student Manager', bg='#bbc7ff', fg='#000000', font=('Arial', 26, 'bold'))
    welcome.pack(expand=True)

#Start program
root = tk.Tk()
setup_window()

#Create sidebar
sidebar = tk.Frame(root, bg='#3c3c3c', width=270)
sidebar.pack(side='left', fill='y')
sidebar.pack_propagate(False)

sidebar_title = tk.Label(sidebar, text='Student Manager', bg='#3c3c3c', fg='white', font=('Arial', 18, 'bold'))
sidebar_title.pack(pady=30)

#Menu buttons
btn1 = tk.Button(sidebar, text='View All Students', bg='#3498db', fg='white', activebackground='#45a7e9', font=('Arial', 12, 'bold'), width=22, height=3, bd=0, cursor='hand2', command=view_all_students)
btn1.pack(pady=10, padx=10)

btn2 = tk.Button(sidebar, text='View Individual Student', bg='#3498db', fg='white', activebackground='#45a7e9', font=('Arial', 12, 'bold'), width=22, height=3, bd=0, cursor='hand2', command=view_indiv_student)
btn2.pack(pady=10, padx=10)

btn3 = tk.Button(sidebar, text='Highest Overall Student', bg='#3498db', fg='white', activebackground='#45a7e9', font=('Arial', 12, 'bold'), width=22, height=3, bd=0, cursor='hand2', command=show_high_score)
btn3.pack(pady=10, padx=10)

btn4 = tk.Button(sidebar, text='Lowest Overall Student', bg='#3498db', fg='white', activebackground='#45a7e9', font=('Arial', 12, 'bold'), width=22, height=3, bd=0, cursor='hand2', command=show_low_score)
btn4.pack(pady=10, padx=10)

quit_btn = tk.Button(sidebar, text='Quit', bg='#c91d19', fg='white', activebackground="#e74e4b", font=('Arial', 12, 'bold'), width=22, height=2, bd=0, cursor='hand2', command=root.quit)
quit_btn.pack(side='bottom', pady=20, padx=10)

#Main Content area
content_frame = tk.Frame(root, bg='#bbc7ff')
content_frame.pack(side='right', fill='both', expand=True)

#Load info and show welcome
load_marks()
show_welcome()
root.mainloop()