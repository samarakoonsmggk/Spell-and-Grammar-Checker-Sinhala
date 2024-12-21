Sinhala Spell and Grammar Checker

Overview:

The Sinhala Spell and Grammar Checker is an AI-powered tool designed to assist in correcting spelling and grammatical errors in Sinhala text. The system utilizes deep learning models to automatically correct errors based on predefined rules of Sinhala grammar.

Features:
- Spell Checker: Detects and suggests corrections for misspelled words in Sinhala.
- Grammar Checker: 
  - Word Order Correction: Sinhala follows a subject-object-verb (SOV) word order. The subject typically comes first, followed by the object and then the verb. The grammar checker ensures that sentences adhere to this structure.
  - Question Formation: In Sinhala, questions are formed by using question particles or question words at the end of the sentence, while the sentence structure remains similar to declarative sentences. The model identifies and corrects errors in question formation.

Installation

Prerequisites
Make sure you have Python 3.7+ installed and the following libraries:

- TensorFlow (for loading and using the deep learning model)
- Keras (for model handling)
- Tkinter (for the graphical user interface)
- Numpy
- JSON (for tokenizer loading)

To install the required libraries, run:


pip install tensorflow keras numpy


Tkinter should be pre-installed with Python, but if it's not, you can install it using:


sudo apt-get install python3-tk


On Windows, Tkinter is generally bundled with Python, so you may not need to install it separately.

Model Files
Download the pre-trained **grammar correction model** and the **tokenizer JSON file**. Place them in the `models/` directory of the project.

-Grammar Model: A deep learning model trained to correct Sinhala grammar errors.
- Tokenizer JSON: The tokenizer used to preprocess the text for the model.

Example:
    grammar_correction_model_final.keras
    tokenizer.json


Usage

1. Run the Application:
   After setting up the model and tokenizer, you can run the application by executing:


   python grammarChecker_DP.py


2.Interface:
   The user interface allows you to input Sinhala text into a text area. Once entered, the model will automatically correct grammar and spelling errors upon clicking the "Correct" button. The corrected text will then be displayed in the output area.

Code Example:
Here is an example of how to use the model within the application:

python:
from tensorflow.keras.models import load_model
from keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences

Load the model
model = load_model('path_to_model/grammar_correction_model_final.keras')

Load the tokenizer
with open('path_to_tokenizer/tokenizer.json', 'r', encoding='utf-8') as file:
    tokenizer_data = json.load(file)
tokenizer = tokenizer_from_json(tokenizer_data)

def correct_sentence(sentence):
    seq = tokenizer.texts_to_sequences([sentence])
    padded_seq = pad_sequences(seq, maxlen=50, padding='post')
    prediction = model.predict(padded_seq)
    return tokenizer.sequences_to_texts(prediction)[0]

Contributing

Contributions to improve the functionality, performance, or features of this tool are welcome! Feel free to fork the repository, make your changes, and create a pull request.

Suggestions for contributions:
- Expand the dataset for model training.
- Improve the deep learning model for better performance.
- Add support for additional Sinhala language variations.
- Enhance the GUI for better user experience.

License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


This version includes the specific grammar rules for word order correction and question formation, as well as the requested features.
