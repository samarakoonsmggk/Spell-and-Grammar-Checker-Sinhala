import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import tkinter as tk
from tkinter import filedialog, scrolledtext
import os

# Define absolute file paths
DATASET_PATH = r"grammar_dataset\sentence_pairs.csv"
TOKENIZER_PATH = r"grammar_dataset\tokenized_sentences.csv"

def load_datasets():
    """Load and validate the necessary datasets"""
    try:
        # Read the main sentence pairs dataset
        print(f"Attempting to load dataset from: {DATASET_PATH}")
        data = pd.read_csv(DATASET_PATH)
        
        # Print available columns to help with debugging
        print("Available columns in CSV:", data.columns.tolist())
        
        # Load tokenizer data
        print(f"Attempting to load tokenizer from: {TOKENIZER_PATH}")
        tokenizer_data = pd.read_csv(TOKENIZER_PATH)
        print("Tokenizer columns:", tokenizer_data.columns.tolist())
        
        return data, tokenizer_data
        
    except FileNotFoundError as e:
        print(f"Error: Could not find file: {str(e)}")
        raise
    except Exception as e:
        print(f"Error loading datasets: {str(e)}")
        raise

def train_statistical_model():
    """Train the statistical model using the sentence pairs dataset"""
    try:
        data, tokenizer_data = load_datasets()
        vectorizer = CountVectorizer()
        
        # Print first few rows of data to verify content
        print("\nFirst few rows of training data:")
        print(data.head())
        
        # Get the actual column names from your CSV
        incorrect_col = data.columns[0]  # First column
        correct_col = data.columns[1]    # Second column
        
        print(f"\nUsing columns: '{incorrect_col}' for incorrect sentences and '{correct_col}' for correct sentences")
        
        # Convert to string type to handle any numeric values
        X = vectorizer.fit_transform(data[incorrect_col].astype(str))
        y = data[correct_col].astype(str)
        
        model = LogisticRegression(max_iter=1000)
        model.fit(X, y)
        return model, vectorizer
    except Exception as e:
        print(f"Error during training: {str(e)}")
        return None, None

def correct_sentence_statistical(sentence, model, vectorizer):
    """Apply statistical correction to a single sentence"""
    try:
        vector = vectorizer.transform([sentence])
        prediction = model.predict(vector)
        return prediction[0]
    except Exception as e:
        return f"Error correcting sentence: {str(e)}"

class GrammarCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("සිංහල ව්‍යාකරණ පරීක්ෂකය - Statistical ML")
        self.setup_gui()
        
    def setup_gui(self):
        # Input section
        tk.Label(self.root, text="වාක්‍ය ඇතුළත් කරන්න:", font=("Iskoola Pota", 12)).pack(pady=5)
        self.input_text_area = scrolledtext.ScrolledText(
            self.root, width=60, height=10, font=("Iskoola Pota", 11))
        self.input_text_area.pack(padx=10, pady=5)
        
        # Correction button
        tk.Button(
            self.root, 
            text="නිවැරදි කරන්න",
            command=self.correct_text,
            font=("Iskoola Pota", 11),
            bg="#4CAF50",
            fg="white",
            pady=5
        ).pack(pady=10)
        
        # Output section
        tk.Label(self.root, text="නිවැරදි කළ වාක්‍ය:", font=("Iskoola Pota", 12)).pack(pady=5)
        self.output_text_area = scrolledtext.ScrolledText(
            self.root, width=60, height=10, font=("Iskoola Pota", 11))
        self.output_text_area.pack(padx=10, pady=5)
        
    def correct_text(self):
        input_text = self.input_text_area.get("1.0", tk.END).strip()
        if not input_text:
            return
            
        try:
            corrected_text = "\n".join([
                correct_sentence_statistical(line, self.model, self.vectorizer)
                for line in input_text.split("\n")
                if line.strip()
            ])
            self.output_text_area.delete("1.0", tk.END)
            self.output_text_area.insert(tk.END, corrected_text)
        except Exception as e:
            self.output_text_area.delete("1.0", tk.END)
            self.output_text_area.insert(tk.END, f"Error: {str(e)}")

def main():
    try:
        print("Starting grammar checker application...")
        # Initialize model
        model, vectorizer = train_statistical_model()
        if model is None or vectorizer is None:
            raise Exception("Failed to initialize the model")
            
        # Setup GUI
        root = tk.Tk()
        app = GrammarCheckerGUI(root)
        app.model = model
        app.vectorizer = vectorizer
        
        # Configure window
        root.geometry("800x600")
        root.configure(bg='#f0f0f0')
        
        # Start application
        root.mainloop()
    except Exception as e:
        print(f"Application error: {str(e)}")
        
if __name__ == "__main__":
    main()