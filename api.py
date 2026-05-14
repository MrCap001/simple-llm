import os
import sys
import tkinter as ttk
from tkinter import *
import customtkinter as cttk
import threading
import subprocess

##Initialize CustomTkinter appearance
cttk.set_appearance_mode("System")  # "Light" or "Dark"
cttk.set_default_color_theme("blue")

##Create the main application window
app = cttk.CTk()
app.geometry("600x700")

##Set the title of the window
app.title("2026 Python IA phrase prediction")

##Set the main title
titleLabel = cttk.CTkLabel(app, text="2026 Python IA phrase prediction", font=cttk.CTkFont(size=36, weight="bold"))
titleLabel.pack(pady=20)


## create a label and an entry set widget
history = cttk.CTkEntry(app, width=400, height=400, state=DISABLED)
history.pack(pady=20)
entry = cttk.CTkEntry(app, width=400, placeholder_text="Write the phrase the System has to finish")
entry.pack(pady=20)

# function to get text from entry widget
def print_entry_text():
    history = entry.get()       #rework
    print(history)

##script progress variables
progress_running = False
progress_value = 0.0

def update_progress():
    global progress_value, progress_running
    if not progress_running:
        return

    progress_value += 0.01
    if progress_value > 1.0:
        progress_value = 0.0

    progressbar.set(progress_value)
    app.after(100, update_progress)


def start_progress():
    global progress_running, progress_value
    if progress_running:
        return

    progress_value = 0.0
    progressbar.set(progress_value)
    progress_running = True
    app.after(100, update_progress)


def stop_progress():
    global progress_running, progress_value
    progress_running = False
    progress_value = 1.0
    progressbar.set(progress_value)


def run_script():
    start_progress()
    phrase = entry.get()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, "main.py")

    def target():
        try:
            subprocess.run([sys.executable, script_path, phrase], check=True, cwd=script_dir)
        finally:
            app.after(0, stop_progress)

    thread = threading.Thread(target=target, daemon=True)
    thread.start()


## send button for running the main script
run_button = cttk.CTkButton(app, text="Send the Phrase", command=run_script)
run_button.pack()

## progress bar to show the progress of the script      #is needed the threading for the processbar to run
progressbar = cttk.CTkProgressBar(app, orientation="horizontal", mode="determinate", width=400, height=30)
progressbar.pack(pady=20, padx=20, fill="x")
progressbar.set(0) # Start at 0%

##Last instruction
app.mainloop()