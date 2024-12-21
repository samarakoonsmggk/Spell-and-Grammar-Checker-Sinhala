import tkinter as tk
from tkinter import scrolledtext, messagebox
import tensorflow as tf
import json
import numpy as np
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

class SinhalaAutoCorrector:
    def __init__(self, root):
        self.root = root
        self.root.title("සිංහල ස්වයංක්‍රීය වචන හා ව්‍යාකරණ නිවැරදි කිරීම")
        self.root.geometry("800x600")
        
        try:
            # Load dictionary of correct words
            with open('sinhalaDictionary_creation\sinhalaDictionary.txt', 'r', encoding='utf-8') as f:
                self.dictionary = set(f.read().splitlines())
            
            # Load correct sentences for reference
            with open('grammar_dataset\correctSentences.txt', 'r', encoding='utf-8') as f:
                self.correct_sentences = f.read().splitlines()
            
            # Load tokenizer
            with open('tokenizer.json', 'r', encoding='utf-8') as f:
                self.tokenizer = json.load(f)
            
            # Load grammar model
            self.model = load_model('models\grammar_correction_model_final.keras')
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading resources: {str(e)}")
            return

        self.setup_gui()
        self.max_sequence_length = 100

    def setup_gui(self):
        # Input area
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        tk.Label(input_frame, 
                text="නිවැරදි කිරීමට අවශ්‍ය පාඨය ඇතුළත් කරන්න:",
                font=("Iskoola Pota", 12)).pack()
        
        self.input_text = scrolledtext.ScrolledText(input_frame,
                                                  height=8,
                                                  font=("Iskoola Pota", 12),
                                                  wrap=tk.WORD)
        self.input_text.pack(pady=5, fill=tk.BOTH, expand=True)

        # Correction button
        tk.Button(self.root,
                 text="ස්වයංක්‍රීයව නිවැරදි කරන්න",
                 command=self.auto_correct,
                 font=("Iskoola Pota", 11),
                 bg="#4CAF50",
                 fg="white",
                 padx=20,
                 pady=5).pack(pady=10)

        # Output area
        output_frame = tk.Frame(self.root)
        output_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        tk.Label(output_frame,
                text="නිවැරදි කරන ලද පාඨය:",
                font=("Iskoola Pota", 12)).pack()
        
        self.output_text = scrolledtext.ScrolledText(output_frame,
                                                   height=8,
                                                   font=("Iskoola Pota", 12),
                                                   wrap=tk.WORD)
        self.output_text.pack(pady=5, fill=tk.BOTH, expand=True)

    def correct_spelling(self, word):
        if word in self.dictionary:
            return word
            
        best_match = word
        min_distance = float('inf')
        
        for dict_word in self.dictionary:
            distance = self.levenshtein_distance(word, dict_word)
            if distance < min_distance and distance <= 2:
                min_distance = distance
                best_match = dict_word
                
        return best_match

    def correct_grammar(self, sentence):
        # First try to find an exact match in correct sentences
        for correct_sent in self.correct_sentences:
            if self.similarity_score(sentence, correct_sent) > 0.8:
                return correct_sent
        
        # If no match found, use model for correction
        try:
            tokens = sentence.split()
            corrected_tokens = []
            
            for i, token in enumerate(tokens):
                # Get context (previous and next words)
                context = tokens[max(0, i-2):i] + tokens[i+1:i+3]
                
                # Prepare input for model
                sequence = self.prepare_sequence(token, context)
                prediction = self.model.predict(sequence, verbose=0)
                
                if prediction[0][0] < 0.5:
                    # Find best replacement from dictionary
                    corrected_token = self.find_best_replacement(token, context)
                    corrected_tokens.append(corrected_token)
                else:
                    corrected_tokens.append(token)
            
            return ' '.join(corrected_tokens)
            
        except Exception:
            # If model fails, use similarity-based correction
            return self.find_similar_sentence(sentence)

    def prepare_sequence(self, word, context):
        # Combine word and context
        text = ' '.join([word] + context)
        
        # Convert to sequence using tokenizer
        sequence = []
        for w in text.split():
            if w in self.tokenizer:
                sequence.append(self.tokenizer[w])
            else:
                sequence.append(1)  # Unknown token
                
        # Pad sequence
        padded = pad_sequences([sequence], maxlen=self.max_sequence_length, padding='post')
        
        # Create attention mask
        mask = np.where(padded != 0, 1, 0)
        
        return [padded, mask]

    def find_best_replacement(self, word, context):
        best_word = word
        best_score = float('-inf')
        
        for correct_word in self.dictionary:
            if abs(len(correct_word) - len(word)) <= 2:
                score = self.context_similarity_score(correct_word, context)
                if score > best_score:
                    best_score = score
                    best_word = correct_word
                    
        return best_word

    def auto_correct(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "කරුණාකර පාඨයක් ඇතුළත් කරන්න")
            return
            
        # Split into sentences
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        corrected_sentences = []
        
        for sentence in sentences:
            # First correct spelling of each word
            words = sentence.split()
            corrected_words = [self.correct_spelling(word) for word in words]
            spell_corrected = ' '.join(corrected_words)
            
            # Then correct grammar
            grammar_corrected = self.correct_grammar(spell_corrected)
            corrected_sentences.append(grammar_corrected)
        
        # Join sentences and display
        final_text = '. '.join(corrected_sentences) + '.'
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", final_text)
        
        # Show changes
        self.show_corrections(text, final_text)

    def show_corrections(self, original, corrected):
        changes = []
        orig_words = original.split()
        corr_words = corrected.split()
        
        for orig, corr in zip(orig_words, corr_words):
            if orig != corr:
                changes.append(f"{orig} → {corr}")
        
        if changes:
            messagebox.showinfo("නිවැරදි කිරීම්", "\n".join(changes))

    def similarity_score(self, s1, s2):
        # Calculate similarity between two sentences
        words1 = set(s1.split())
        words2 = set(s2.split())
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return len(intersection) / len(union)

    def context_similarity_score(self, word, context):
        # Calculate how well a word fits in the given context
        word_score = 0
        for correct_sent in self.correct_sentences:
            if word in correct_sent and any(c in correct_sent for c in context):
                word_score += 1
        return word_score

    def levenshtein_distance(self, s1, s2):
        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]

    def find_similar_sentence(self, sentence):
        best_match = sentence
        best_score = 0
        
        for correct_sent in self.correct_sentences:
            score = self.similarity_score(sentence, correct_sent)
            if score > best_score:
                best_score = score
                best_match = correct_sent
                
        return best_match if best_score > 0.3 else sentence

def main():
    root = tk.Tk()
    app = SinhalaAutoCorrector(root)
    root.mainloop()

if __name__ == "__main__":
    main()