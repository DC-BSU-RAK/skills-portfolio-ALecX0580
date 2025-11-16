import tkinter as tk
from tkinter import messagebox
import random

#Global variables to track game state
difficulty = None
current_question = 0
score = 0
lives = 3
total_questions = 10
questions = []
answering = True
choice_buttons = []

#Set up main window
def setup_window():
    root.title('Math Quiz Game')
    root.geometry('1080x720')
    root.config(bg='#2c3e50')
    root.resizable(False, False)

#Clear all widgets from screen
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

#Display main menu
def show_main_menu():
    clear_window()
    
    title = tk.Label(root, text='Math Quiz', bg='#2c3e50', fg='#ecf0f1', font=('Arial', 48, 'bold'))
    title.pack(pady=80)
    
    subtitle = tk.Label(root, text='The Four Ops', bg='#2c3e50', fg='#95a5a6', font=('Arial', 18, 'italic'))
    subtitle.pack(pady=10)
    
    btn_frame = tk.Frame(root, bg='#2c3e50')
    btn_frame.pack(pady=80)
    
    play_btn = tk.Button(btn_frame, text='PLAY', bg='#27ae60', fg='white', font=('Arial', 24, 'bold'), width=15, height=2, bd=0, cursor='hand2', command=show_difficulty_menu)
    play_btn.pack(pady=15)
    
    exit_btn = tk.Button(btn_frame, text='EXIT', bg='#e74c3c', fg='white', font=('Arial', 24, 'bold'), width=15, height=2, bd=0, cursor='hand2', command=root.quit)
    exit_btn.pack(pady=15)

#Display difficulty selection menu
def show_difficulty_menu():
    clear_window()
    
    title = tk.Label(root, text='Select Difficulty', bg='#2c3e50', fg='#ecf0f1', font=('Arial', 36, 'bold'))
    title.pack(pady=60)
    
    btn_frame = tk.Frame(root, bg='#2c3e50')
    btn_frame.pack(pady=50)
    
    easy_btn = tk.Button(btn_frame, text='EASY\n(2 Digits)', bg='#3498db', fg='white', font=('Arial', 20, 'bold'), width=18, height=3, bd=0, cursor='hand2', command=lambda: start_quiz('easy'))
    easy_btn.pack(pady=15)
    
    intermediate_btn = tk.Button(btn_frame, text='INTERMEDIATE\n(3 Digits)', bg='#f39c12', fg='white', font=('Arial', 20, 'bold'), width=18, height=3, bd=0, cursor='hand2', command=lambda: start_quiz('intermediate'))
    intermediate_btn.pack(pady=15)
    
    advance_btn = tk.Button(btn_frame, text='ADVANCE\n(4 Digits)', bg='#e74c3c', fg='white', font=('Arial', 20, 'bold'), width=18, height=3, bd=0, cursor='hand2', command=lambda: start_quiz('advance'))
    advance_btn.pack(pady=15)
    
    back_btn = tk.Button(btn_frame, text='BACK', bg='#95a5a6', fg='white', font=('Arial', 16, 'bold'), width=18, height=2, bd=0, cursor='hand2', command=show_main_menu)
    back_btn.pack(pady=20)

#Initialize quiz with selected difficulty
def start_quiz(diff):
    global difficulty, current_question, score, lives, questions
    difficulty = diff
    current_question = 0
    score = 0
    lives = 3
    questions = []
    generate_questions()
    show_question()

#Generate all questions for quiz
def generate_questions():
    global questions
    
    #Set number ranges based on difficulty
    if difficulty == 'easy':
        num_range_min = 10
        num_range_max = 99
        mult_min = 2
        mult_max = 15
        div_min = 2
        div_max = 15
    elif difficulty == 'intermediate':
        num_range_min = 100
        num_range_max = 999
        mult_min = 10
        mult_max = 99
        div_min = 10
        div_max = 99
    else:
        num_range_min = 1000
        num_range_max = 9999
        mult_min = 100
        mult_max = 999
        div_min = 100
        div_max = 999
    
    operations = ['+', '-', '*', '/']
    
    #Create 10 random questions
    for i in range(total_questions):
        operation = random.choice(operations)
        
        if operation == '+':
            num1 = random.randint(num_range_min, num_range_max)
            num2 = random.randint(num_range_min, num_range_max)
            answer = num1 + num2
        
        elif operation == '-':
            num1 = random.randint(num_range_min, num_range_max)
            num2 = random.randint(num_range_min, num_range_max)
            #Swap to ensure positive result
            if num2 > num1:
                temp = num1
                num1 = num2
                num2 = temp
            answer = num1 - num2
        
        elif operation == '*':
            num1 = random.randint(num_range_min, num_range_max)
            num2 = random.randint(mult_min, mult_max)
            answer = num1 * num2
        
        else:  #Division
            #Work backwards to ensure clean division
            answer = random.randint(num_range_min, num_range_max)
            num2 = random.randint(div_min, div_max)
            num1 = answer * num2
        
        #Generate 3 wrong choices
        choices = [answer]
        while len(choices) < 4:
            if answer < 100:
                wrong = answer + random.randint(-15, 15)
            elif answer < 1000:
                wrong = answer + random.randint(-50, 50)
            else:
                wrong = answer + random.randint(-200, 200)
            
            if wrong > 0 and wrong not in choices:
                choices.append(wrong)
        
        random.shuffle(choices)
        
        questions.append({
            'num1': num1,
            'num2': num2,
            'operation': operation,
            'answer': answer,
            'choices': choices
        })

#Display current question
def show_question():
    global lives, answering, choice_buttons, lives_label, feedback_label
    clear_window()
    lives = 3
    answering = True
    choice_buttons = []
    
    question_data = questions[current_question]
    
    #Header with question info
    header_frame = tk.Frame(root, bg='#34495e')
    header_frame.pack(fill='x', pady=0)
    
    question_label = tk.Label(header_frame, text=f'Question {current_question + 1}/{total_questions}', bg='#34495e', fg='#ecf0f1', font=('Arial', 18, 'bold'))
    question_label.pack(side='left', padx=20, pady=15)
    
    quit_btn = tk.Button(header_frame, text='QUIT', bg='#c0392b', fg='white', font=('Arial', 14, 'bold'), width=8, bd=0, cursor='hand2', command=show_main_menu)
    quit_btn.pack(side='left', padx=20, pady=15)
    
    score_label = tk.Label(header_frame, text=f'Score: {score}', bg='#34495e', fg='#f39c12', font=('Arial', 18, 'bold'))
    score_label.pack(side='right', padx=20, pady=15)
    
    lives_label = tk.Label(header_frame, text='❤️ 3', bg='#34495e', fg='#e74c3c', font=('Arial', 20, 'bold'))
    lives_label.pack(side='right', padx=20, pady=15)
    
    #Question display
    question_frame = tk.Frame(root, bg='#2c3e50')
    question_frame.pack(pady=40)
    
    question_text = tk.Label(question_frame, text=f"{question_data['num1']} {question_data['operation']} {question_data['num2']} = ?", bg='#2c3e50', fg='#ecf0f1', font=('Arial', 42, 'bold'))
    question_text.pack(pady=20)
    
    feedback_label = tk.Label(question_frame, text='', bg='#2c3e50', font=('Arial', 16, 'bold'))
    feedback_label.pack(pady=10)
    
    #Answer choices in grid
    choices_frame = tk.Frame(root, bg='#2c3e50')
    choices_frame.pack(pady=20, fill='both', expand=True, padx=40)
    
    choices_frame.grid_rowconfigure(0, weight=1)
    choices_frame.grid_rowconfigure(1, weight=1)
    choices_frame.grid_columnconfigure(0, weight=1)
    choices_frame.grid_columnconfigure(1, weight=1)
    
    colors = ['#2ECC71', '#E74C3C', '#F1C40F', '#3498DB']
    
    for i in range(4):
        choice = question_data['choices'][i]
        row = i // 2
        col = i % 2
        
        btn = tk.Button(choices_frame, text=str(choice), bg=colors[i], fg='white', font=('Arial', 36, 'bold'), bd=0, cursor='hand2', relief='flat', command=lambda c=choice: check_answer(c))
        btn.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        choice_buttons.append(btn)

#Update lives display
def update_lives():
    global lives_label
    if lives > 0:
        lives_label.config(text=f'❤️ {lives}', fg='#e74c3c')
    else:
        lives_label.config(text='🖤 0', fg='#95a5a6')

#Check if answer is correct
def check_answer(selected):
    global lives, score, answering
    
    #Prevent multiple clicks
    if not answering:
        return
    
    question_data = questions[current_question]
    correct = question_data['answer']
    
    if selected == correct:
        answering = False
        for btn in choice_buttons:
            btn.config(state='disabled', cursor='arrow')
        
        #Award points based on lives remaining
        if lives == 3:
            points = 10
        elif lives == 2:
            points = 5
        elif lives == 1:
            points = 1
        else:
            points = 0
        
        score = score + points
        feedback_label.config(text=f'Correct! +{points} points', fg='#2ecc71')
        root.after(1500, next_question)
    else:
        lives = lives - 1
        update_lives()
        
        if lives == 0:
            answering = False
            for btn in choice_buttons:
                btn.config(state='disabled', cursor='arrow')
            
            feedback_label.config(text=f'Wrong! The answer was {correct}', fg='#e74c3c')
            root.after(2000, next_question)
        else:
            if lives == 1:
                feedback_label.config(text=f'Try again! {lives} life remaining', fg='#e74c3c')
            else:
                feedback_label.config(text=f'Try again! {lives} lives remaining', fg='#e74c3c')

#Move to next question
def next_question():
    global current_question
    current_question = current_question + 1
    if current_question < total_questions:
        show_question()
    else:
        show_results()

#Display final results
def show_results():
    clear_window()
    
    results_frame = tk.Frame(root, bg='#2c3e50')
    results_frame.pack(expand=True)
    
    title = tk.Label(results_frame, text='Quiz Completed!', bg='#2c3e50', fg='#ecf0f1', font=('Arial', 42, 'bold'))
    title.pack(pady=40)
    
    max_score = total_questions * 10
    
    score_label = tk.Label(results_frame, text=f'Your Score: {score}/{max_score}', bg='#2c3e50', fg='#f39c12', font=('Arial', 36, 'bold'))
    score_label.pack(pady=30)
    
    #Show performance message based on score
    percentage = (score / max_score) * 100
    if percentage >= 90:
        message = 'Excellent!'
        color = '#2ecc71'
    elif percentage >= 70:
        message = 'Great!'
        color = '#3498db'
    elif percentage >= 50:
        message = 'Good Try!'
        color = '#f39c12'
    else:
        message = 'Back to Basics'
        color = '#e74c3c'
    
    message_label = tk.Label(results_frame, text=message, bg='#2c3e50', fg=color, font=('Arial', 28, 'bold'))
    message_label.pack(pady=20)
    
    btn_frame = tk.Frame(results_frame, bg='#2c3e50')
    btn_frame.pack(pady=40)
    
    play_again_btn = tk.Button(btn_frame, text='Play Again', bg='#27ae60', fg='white', font=('Arial', 20, 'bold'), width=15, height=2, bd=0, cursor='hand2', command=show_difficulty_menu)
    play_again_btn.pack(pady=10)
    
    main_menu_btn = tk.Button(btn_frame, text='Main Menu', bg='#3498db', fg='white', font=('Arial', 20, 'bold'), width=15, height=2, bd=0, cursor='hand2', command=show_main_menu)
    main_menu_btn.pack(pady=10)
    
    exit_btn = tk.Button(btn_frame, text='Exit', bg='#e74c3c', fg='white', font=('Arial', 20, 'bold'), width=15, height=2, bd=0, cursor='hand2', command=root.quit)
    exit_btn.pack(pady=10)

#Start program
root = tk.Tk()
setup_window()
show_main_menu()
root.mainloop()