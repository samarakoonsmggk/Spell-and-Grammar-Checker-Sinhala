import tkinter as tk
from tkinter import scrolledtext, messagebox
from difflib import get_close_matches
import re

class SinhalaAutoCorrector:
    def __init__(self, root):
        self.root = root
        self.root.title("සිංහල ස්වයංක්‍රීය වචන හා ව්‍යාකරණ නිවැරදි කිරීම- Rule Based")
        self.root.geometry("800x600")
        
        try:
            # Load dictionary of correct words
            with open('sinhalaDictionary_creation\sinhalaDictionary.txt', 'r', encoding='utf-8') as f:
                self.dictionary = set(f.read().splitlines())
            
            # Define grammar rules
            self.grammar_rules = {
                # SOV word order patterns
                'word_order': [
                    {
                        'pattern': r'(මම|අපි|ඔහු|ඇය|ඔවුන්)\s+(\w+මි|\w+යි|\w+ති)\s+([^.]+)',
                        'correction': lambda m: f"{m.group(1)} {m.group(3)} {m.group(2)}"
                    }
                ],
                # Question formation rules
                'question': [
                    {
                        'pattern': r'(කොහි|කවුද|මොකද|කුමක්)\s*(?!ද)[.?]?$',
                        'correction': lambda m: f"{m.group(1)}ද?"
                    },
                    {
                        'pattern': r'(.+[^ද])[?]$',
                        'correction': lambda m: f"{m.group(1)}ද?"
                    }
                ],
                # Subject-verb agreement
                'verb_agreement': [
                    {
                        'pattern': r'(මම)\s+.+?([^මි])[.?]?$',
                        'correction': lambda m: f"{m.group(1)} {m.group(2)}මි"
                    },
                    {
                        'pattern': r'(ඔහු|ඇය)\s+.+?([^යි])[.?]?$',
                        'correction': lambda m: f"{m.group(1)} {m.group(2)}යි"
                    }
                ]
            }
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading resources: {str(e)}")
            return

        self.setup_gui()

    def setup_gui(self):
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        tk.Label(input_frame, text="නිවැරදි කිරීමට අවශ්‍ය පාඨය ඇතුළත් කරන්න:", 
                font=("Iskoola Pota", 12)).pack()
        
        self.input_text = scrolledtext.ScrolledText(input_frame, height=8, 
                                                  font=("Iskoola Pota", 12), wrap=tk.WORD)
        self.input_text.pack(pady=5, fill=tk.BOTH, expand=True)

        tk.Button(self.root, text="ස්වයංක්‍රීයව නිවැරදි කරන්න", 
                 command=self.auto_correct,
                 font=("Iskoola Pota", 11), 
                 bg="#4CAF50", fg="white", 
                 padx=20, pady=5).pack(pady=10)

        output_frame = tk.Frame(self.root)
        output_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        tk.Label(output_frame, text="නිවැරදි කරන ලද පාඨය:", 
                font=("Iskoola Pota", 12)).pack()
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=8, 
                                                   font=("Iskoola Pota", 12), wrap=tk.WORD)
        self.output_text.pack(pady=5, fill=tk.BOTH, expand=True)

        accuracy_frame = tk.Frame(self.root)
        accuracy_frame.pack(pady=5, padx=10, fill=tk.X)
        
        self.spelling_accuracy_label = tk.Label(accuracy_frame, 
                                              text="අක්ෂර වින්යාස නිරවද්යතාව: 0%", 
                                              font=("Iskoola Pota", 11))
        self.spelling_accuracy_label.pack(side=tk.LEFT, padx=10)
        
        self.grammar_accuracy_label = tk.Label(accuracy_frame, 
                                             text="ව්‍යාකරණ නිරවද්යතාව: 0%", 
                                             font=("Iskoola Pota", 11))
        self.grammar_accuracy_label.pack(side=tk.RIGHT, padx=10)

    def correct_spelling(self, word):
        """Apply spell checking using dictionary"""
        if word in self.dictionary:
            return word
            
        # Find closest match in dictionary
        matches = get_close_matches(word, self.dictionary, n=1, cutoff=0.8)
        return matches[0] if matches else word

    def apply_grammar_rules(self, sentence, rule_type):
        """Apply specific grammar rules to the sentence"""
        corrected = sentence
        for rule in self.grammar_rules[rule_type]:
            match = re.search(rule['pattern'], corrected)
            if match:
                corrected = rule['correction'](match)
        return corrected

    def correct_grammar(self, sentence):
        """Apply all grammar rules in sequence"""
        corrected = sentence
        
        # Check and correct word order (SOV)
        corrected = self.apply_grammar_rules(corrected, 'word_order')
        
        # Check and correct question formation
        if '?' in corrected or any(q in corrected.lower() for q in ['කොහි', 'කවුද', 'මොකද', 'කුමක්']):
            corrected = self.apply_grammar_rules(corrected, 'question')
        
        # Check and correct verb agreement
        corrected = self.apply_grammar_rules(corrected, 'verb_agreement')
        
        return corrected

    def calculate_accuracy(self, original, corrected):
        """Calculate similarity between original and corrected text"""
        words1 = set(original.split())
        words2 = set(corrected.split())
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        return (intersection / union * 100) if union > 0 else 100

    def auto_correct(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "කරුණාකර පාඨයක් ඇතුළත් කරන්න")
            return
            
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        corrected_sentences = []
        changes = []
        
        total_spelling_accuracy = 0
        total_grammar_accuracy = 0
        
        for sentence in sentences:
            # Spelling correction
            words = sentence.split()
            corrected_words = []
            
            for word in words:
                corrected = self.correct_spelling(word)
                if corrected != word:
                    changes.append(f"Spelling: {word} → {corrected}")
                corrected_words.append(corrected)
            
            spell_corrected = ' '.join(corrected_words)
            
            # Grammar correction
            grammar_corrected = self.correct_grammar(spell_corrected)
            if grammar_corrected != spell_corrected:
                changes.append(f"Grammar: {spell_corrected} → {grammar_corrected}")
            
            # Calculate accuracies
            spelling_accuracy = self.calculate_accuracy(sentence, spell_corrected)
            grammar_accuracy = self.calculate_accuracy(spell_corrected, grammar_corrected)
            
            total_spelling_accuracy += spelling_accuracy
            total_grammar_accuracy += grammar_accuracy
            
            corrected_sentences.append(grammar_corrected)
        
        # Update accuracy labels
        avg_spelling_accuracy = total_spelling_accuracy / len(sentences)
        avg_grammar_accuracy = total_grammar_accuracy / len(sentences)
        
        self.spelling_accuracy_label.config(
            text=f"අක්ෂර වින්යාස නිරවද්යතාව: {avg_spelling_accuracy:.1f}%")
        self.grammar_accuracy_label.config(
            text=f"ව්‍යාකරණ නිරවද්යතාව: {avg_grammar_accuracy:.1f}%")
        
        # Display corrected text
        final_text = '. '.join(corrected_sentences) + ('?' if text.strip().endswith('?') else '.')
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", final_text)
        
        # Show corrections
        if changes:
            messagebox.showinfo("නිවැරදි කිරීම්", "\n".join(changes))

def main():
    root = tk.Tk()
    app = SinhalaAutoCorrector(root)
    root.mainloop()

if __name__ == "__main__":
    main()