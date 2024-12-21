import csv
from tokenizers import Tokenizer, models, pre_tokenizers, trainers

text_data = []

# Open the file with proper encoding
with open('grammar_dataset/sentence_pairs.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        text_data.append(row[0])  # Assuming the text is in the first column

tokenizer = Tokenizer(models.BPE())
tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()

trainer = trainers.BpeTrainer(vocab_size=5000, min_frequency=2, show_progress=True)
tokenizer.train_from_iterator(text_data, trainer)
tokenizer.save("tokenizer.json")
