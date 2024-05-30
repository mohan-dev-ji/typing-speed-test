import tkinter as tk
import time
import random

start_time = None


# ---------------------------- FUNCTIONS ------------------------------- #


# Function to display sample text
def display_sample_text():
    sample_text_display.config(state=tk.NORMAL)
    sample_text_display.delete(1.0, tk.END)
    sample_text_display.insert(tk.END, sample_text)
    sample_text_display.config(state=tk.DISABLED)

# Function to update the highlight
def highlight_current_word():
    sample_text_display.tag_remove("highlight", 1.0, tk.END)
    if current_word_index == 0:
        start_index = f"1.0+{len(' '.join(words[:current_word_index]))}c"
    else:
        start_index = f"1.0+{len(' '.join(words[:current_word_index]))+1}c"
    end_index = f"{start_index}+{len(words[current_word_index])}c"
    sample_text_display.tag_add("highlight", start_index, end_index)
    sample_text_display.tag_config("highlight", background="grey")

# Function to handle key release event
def on_key_release(event):
    global current_word_index, start_time
    if start_time is None:
        start_timer()
    typed_text = user_input.get("1.0", tk.END).strip().split()
    if len(typed_text) > current_word_index and typed_text[current_word_index] == words[current_word_index]:
        current_word_index += 1
        highlight_current_word()
        update_wpm()

def start_timer():
    global start_time
    start_time = time.time()
    countdown(60)

def countdown(time_left):
    if time_left > 0:
        timer_label.config(text=f"Time: {time_left}s")
        root.after(1000, countdown, time_left - 1)
    else:
        timer_label.config(text="Time: 0s")
        user_input.config(state=tk.DISABLED)
        calculate_final_wpm()

def update_wpm():
    elapsed_time = time.time() - start_time
    words_typed = len(user_input.get("1.0", tk.END).strip().split())
    wpm = (words_typed / elapsed_time) * 60
    wpm_label.config(text=f"WPM: {int(wpm)}")
    print(words_typed)

def calculate_final_wpm():
    global current_word_index
    # elapsed_time = time.time() - start_time
    words_typed = len(user_input.get("1.0", tk.END).strip().split())
    # wpm = (words_typed / elapsed_time) * 60
    wpm_label.config(text=f"Final WPM: {int(current_word_index)}")

def load_words(file_path):
    with open(file_path, 'r') as file:
        words = file.read().splitlines()
    return words

# Function to select random sample text
def select_sample_text(words, sample_size=100):
    return ' '.join(random.sample(words, sample_size))

# Function to reset the test
def restart_test():
    global sample_text, words, current_word_index, start_time
    # Reset variables
    sample_text = select_sample_text(words_list)
    words = sample_text.split()
    current_word_index = 0
    start_time = None
    # Clear user input
    user_input.config(state=tk.NORMAL)
    user_input.delete("1.0", tk.END)
    user_input.config(state=tk.NORMAL)
    # Reset timer and WPM labels
    timer_label.config(text="Time: 60s")
    wpm_label.config(text="WPM: 0")
    # Display new sample text
    display_sample_text()
    # Highlight the first word
    highlight_current_word()
    # Re-enable user input
    user_input.config(state=tk.NORMAL)


# ---------------------------- UI SETUP ------------------------------- #


root = tk.Tk()
root.tite = ("Typing Speed Test")
root.geometry = ("800x400")
root.configure(padx=50, pady=50, bg="black")

# Sample text display (read-only)
sample_text_display = tk.Text(root, height=10, width=80, wrap=tk.WORD)
sample_text_display.grid(column=0, row=1, columnspan=2, pady=50)
sample_text_display.config(state=tk.DISABLED)

# User input text box
user_input = tk.Text(root, height=5, width=80, wrap=tk.WORD)
user_input.grid(column=0, row=2, columnspan=2)

# Timer and WPM labels
timer_label = tk.Label(root, text="Time: 60s")
timer_label.grid(column=0, row=0)
wpm_label = tk.Label(root, text="WPM: 0")
wpm_label.grid(column=1, row=0)

# Re-Start button to re start the test
restart_button = tk.Button(root, text="Start", command=lambda: [user_input.config(state=tk.NORMAL), restart_test()])
restart_button.grid(column=0, row=3, columnspan=2, pady=50)


# ---------------------------- Main Program ------------------------------- #


words_list = load_words('google-10000-english-no-swears.txt')

# Select random sample text
sample_text = select_sample_text(words_list)
words = sample_text.split()
word_positions = []

display_sample_text()

current_word_index = 0

user_input.bind("<KeyRelease>", on_key_release)

highlight_current_word()

root.mainloop()

