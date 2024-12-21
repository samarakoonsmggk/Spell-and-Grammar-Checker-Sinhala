import tensorflow as tf
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
import os

# Paths
model_path = r"models\grammar_correction_model_final.keras"
tokenizer_path = r"tokenizer.json"

# Verify if tokenizer file exists
if not os.path.exists(tokenizer_path):
    messagebox.showerror("Error", f"Tokenizer file not found at {tokenizer_path}. Please verify the path.")
    exit()

# Load tokenizer with error handling
try:
    with open(tokenizer_path, 'r', encoding='utf-8') as file:
        tokenizer_json = file.read()
        # Verify the JSON is valid
        try:
            json.loads(tokenizer_json)  # Test if JSON is valid
        except json.JSONDecodeError as e:
            messagebox.showerror("Error", f"Invalid JSON format in tokenizer file: {str(e)}")
            exit()
            
        tokenizer = tokenizer_from_json(tokenizer_json)
        if tokenizer is None:
            messagebox.showerror("Error", "Failed to create tokenizer from JSON")
            exit()
except Exception as e:
    messagebox.showerror("Error", f"Error loading tokenizer: {str(e)}")
    exit()

# Load pre-trained model
try:
    if not os.path.exists(model_path):
        messagebox.showerror("Error", f"Model file not found at {model_path}. Please verify the path.")
        exit()
    
    model = tf.keras.models.load_model(model_path)
except Exception as e:
    messagebox.showerror("Error", f"Error loading model: {str(e)}")
    exit()

# Function to correct a sentence
def correct_sentence_deep_learning(sentence):
    try:
        seq = tokenizer.texts_to_sequences([sentence])
        padded_seq = pad_sequences(seq, maxlen=50, padding='post')
        prediction = model.predict(padded_seq, verbose=0)  # Added verbose=0 to reduce output
        predicted_seq = tf.argmax(prediction, axis=-1).numpy()
        corrected_sentence = tokenizer.sequences_to_texts(predicted_seq)[0]
        return corrected_sentence
    except Exception as e:
        messagebox.showerror("Error", f"Error in sentence correction: {str(e)}")
        return sentence  # Return original sentence if correction fails

# Function to process text input and correct grammar
def dl_checker():
    input_text = input_text_area.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Input Required", "Please enter some text to correct.")
        return

    try:
        corrected_text = "\n".join(
            [correct_sentence_deep_learning(line) for line in input_text.split("\n") if line.strip()]
        )
        output_text_area.delete("1.0", tk.END)
        output_text_area.insert(tk.END, corrected_text)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during processing: {str(e)}")

# GUI Setup
root = tk.Tk()
root.title("Sinhala Grammar Checker - Deep Learning")

tk.Label(root, text="Enter Text:", font=("Helvetica", 14)).pack(pady=5)
input_text_area = scrolledtext.ScrolledText(root, width=60, height=10, font=("Helvetica", 12))
input_text_area.pack(pady=10)

tk.Button(root, text="Correct", command=dl_checker, font=("Helvetica", 12), bg="#4CAF50", fg="white").pack(pady=5)

tk.Label(root, text="Corrected Text:", font=("Helvetica", 14)).pack(pady=5)
output_text_area = scrolledtext.ScrolledText(root, width=60, height=10, font=("Helvetica", 12))
output_text_area.pack(pady=10)

root.mainloop()