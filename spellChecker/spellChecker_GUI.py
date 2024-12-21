import tkinter as tk
from tkinter import filedialog, messagebox
import re
from difflib import get_close_matches

# Load the Sinhala dictionary
dictionary_path = r'sinhalaDictionary_creation\sinhalaDictionary.txt'#path to dictionary

try:
    with open(dictionary_path, 'r', encoding='utf-8') as dict_file:
        sinhala_dictionary = set(dict_file.read().splitlines())
except FileNotFoundError:
    messagebox.showerror("Error", f"Dictionary file not found at {dictionary_path}")
    exit()

# Function to extract Sinhala words
def extract_sinhala_words(text):
    sinhala_words = re.findall(r'[\u0D80-\u0DFF]+', text)
    return sinhala_words

# Function to find and correct spelling mistakes
def correct_spelling():
    text_content = text_box.get("1.0", tk.END).strip()  # Get text from the text box
    words = extract_sinhala_words(text_content)  # Extract Sinhala words
    corrected_text = text_content

    misspelled_words = [word for word in words if word not in sinhala_dictionary]
    corrections = {}

    for word in misspelled_words:
        # Find closest matches from the dictionary
        suggestions = get_close_matches(word, sinhala_dictionary, n=1, cutoff=0.7)
        if suggestions:
            corrections[word] = suggestions[0]  # Auto-correct to the closest match
        else:
            corrections[word] = word  # Leave unchanged if no match found

    # Replace misspelled words in the text
    for incorrect, correct in corrections.items():
        corrected_text = corrected_text.replace(incorrect, correct)

    # Display the corrected text in the text box
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, corrected_text)

    # Show a message with corrections
    correction_message = "\n".join([f"{incorrect} -> {correct}" for incorrect, correct in corrections.items()])
    if correction_message:
        messagebox.showinfo("Corrections Made", f"Auto-corrected the following words:\n\n{correction_message}")
    else:
        messagebox.showinfo("No Corrections", "No misspelled words found.")

# Function to open a text file and load its content into the text box
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            text_box.delete("1.0", tk.END)  # Clear existing text
            text_box.insert(tk.END, content)

# Function to save the corrected text to a file
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text_box.get("1.0", tk.END).strip())
        messagebox.showinfo("Success", "File saved successfully.")

# Create the main application window
root = tk.Tk()
root.title("Sinhala Spell Checker with Auto-Correction")
root.geometry("800x600")

# Add a text box for input
text_box = tk.Text(root, wrap=tk.WORD, font=("Helvetica", 14))
text_box.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# Add buttons for actions
button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X, padx=10, pady=5)

open_button = tk.Button(button_frame, text="Open File", command=open_file, bg="#008CBA", fg="white", padx=10, pady=5)
open_button.pack(side=tk.LEFT, padx=5)

check_button = tk.Button(button_frame, text="Correct Spelling", command=correct_spelling, bg="#4CAF50", fg="white", padx=10, pady=5)
check_button.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(button_frame, text="Save File", command=save_file, bg="#f44336", fg="white", padx=10, pady=5)
save_button.pack(side=tk.LEFT, padx=5)

# Run the application
root.mainloop()
