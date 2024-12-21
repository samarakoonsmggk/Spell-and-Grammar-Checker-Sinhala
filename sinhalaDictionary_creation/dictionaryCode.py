import re
import os

# Path to the Sinhala dataset
dataset_path = r'sinhalaDictionary_creation\textfiles'

# Function to extract Sinhala words from text
def extract_sinhala_words(text):
    """
    Extracts Sinhala words using a Unicode range for Sinhala characters.
    """
    sinhala_words = re.findall(r'[\u0D80-\u0DFF]+', text)  # Matches Sinhala Unicode characters
    return sinhala_words

# Dictionary to store unique Sinhala words
sinhala_word_set = set()

# Traverse the dataset directory and process .txt files
for root, dirs, file_list in os.walk(dataset_path):
    for file_name in file_list:
        if file_name.endswith('.txt'):  # Process only text files
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    # Extract and add Sinhala words to the set
                    words = extract_sinhala_words(text)
                    sinhala_word_set.update(words)
            except Exception as e:
                print(f"Error reading file {file_name}: {e}")

# Output file path for the Sinhala dictionary
output_path = r'sinhalaDictionary_creation\sinhalaDictionary.txt'

# Write unique Sinhala words to the dictionary file
try:
    with open(output_path, 'w', encoding='utf-8') as dict_file:
        for word in sorted(sinhala_word_set):
            dict_file.write(word + '\n')
    print(f"Sinhala dictionary successfully created at: {output_path}")
except Exception as e:
    print(f"Error writing dictionary file: {e}")
