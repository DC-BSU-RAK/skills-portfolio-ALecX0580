#Joke Assistant
import tkinter as tk
from tkinter import messagebox
import random
import winsound

#Variables to store jokes and current joke info
jokes = []
current_setup = ""
current_punchline = ""

#Set up main window
def setup_window():
    root.title('Joke Assistant')
    root.geometry('1080x720')
    root.config(bg='#ecf0f1')
    root.resizable(False, False)

#Clear all widgets from screen
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

#Load jokes from RandomJokes.txt
def load_jokes():
    global jokes
    try:
        file = open('../../A1 - Resources/randomJokes.txt', 'r')
        lines = file.readlines()
        file.close()
        
        #Go through each line in file
        for line in lines:
            line = line.strip()
            #Remove dash at start
            if line.startswith('-'):
                line = line[1:].strip()
            
            #Split joke into setup and punchline
            if '?' in line:
                parts = line.split('?', 1)
                setup = parts[0].strip() + '?'
                punchline = parts[1].strip()
                jokes.append({'setup': setup, 'punchline': punchline})
    except:
        messagebox.showerror('Error', 'Jokes file not Found.')

#Display main joke screen
def show_joke_screen():
    global setup_label, punchline_label, punchline_btn, next_joke_btn
    clear_window()
    
    title = tk.Label(root, text='Alexa the Joker', bg='#ecf0f1', fg='#2c3e50', font=('Arial', 48, 'bold'))
    title.pack(pady=30)
    
    setup_label = tk.Label(root, text='Click Buttons to Hear Jokes', bg='#ecf0f1', fg='#7f8c8d', font=('Arial', 16), wraplength=500, justify='center')
    setup_label.pack(pady=20)
    
    #Label for punchline
    punchline_label = tk.Label(root, text='', bg='#ecf0f1', fg='#27ae60', font=('Arial', 24, 'bold'), wraplength=500, justify='center')
    punchline_label.pack(pady=10)
    
    #Frame to hold buttons
    btn_frame = tk.Frame(root, bg='#ecf0f1')
    btn_frame.pack(pady=30)
    
    #Button to tell joke
    alexa_btn = tk.Button(btn_frame, text='Alexa tell me a Joke', bg='#F1C40F', fg='white', font=('Arial', 16, 'bold'), width=20, height=2, bd=0, cursor='hand2', command=tell_joke)
    alexa_btn.pack(pady=10)
    
    #Button to show punchline, starting disabled
    punchline_btn = tk.Button(btn_frame, text='Show Punchline', bg='#e67e22', fg='white', font=('Arial', 16, 'bold'), width=20, height=2, bd=0, cursor='hand2', command=show_punchline, state='disabled')
    punchline_btn.pack(pady=10)
    
    #Button to get next joke, also starting disabled
    next_joke_btn = tk.Button(btn_frame, text='Next Joke', bg='#3498db', fg='white', font=('Arial', 16, 'bold'), width=20, height=2, bd=0, cursor='hand2', command=tell_joke, state='disabled')
    next_joke_btn.pack(pady=10)
    
    #Button to close program
    quit_btn = tk.Button(btn_frame, text='Quit', bg='#e74c3c', fg='white', font=('Arial', 16, 'bold'), width=20, height=2, bd=0, cursor='hand2', command=root.quit)
    quit_btn.pack(pady=10)

#Display random joke
def tell_joke():
    global current_setup, current_punchline
    
    #Check if there is jokes
    if len(jokes) == 0:
        messagebox.showwarning('No Jokes', 'There is no Jokes')
        return
    
    #Use random lib to pick a joke from list
    joke = random.choice(jokes)
    current_setup = joke['setup']
    current_punchline = joke['punchline']
    
    setup_label.config(text=current_setup, fg='#2c3e50')
    punchline_label.config(text='')
    
    #Enable buttons
    punchline_btn.config(state='normal')
    next_joke_btn.config(state='disabled')

#Show punchline and play sound when button is clicked
def show_punchline():
    punchline_label.config(text=current_punchline, fg='#27ae60')
    punchline_btn.config(state='disabled')

    #PLay Laugh Track when punchline is shown
    winsound.PlaySound('Sitcom-Laugh.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

    #Enable Next Joke Button after Sound
    next_joke_btn.config(state='normal')

#Start program
root = tk.Tk()
setup_window()
load_jokes()
show_joke_screen()
root.mainloop()