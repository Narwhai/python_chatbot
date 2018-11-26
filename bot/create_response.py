import random
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#nltk.download('stopwords')

current_dir: str = os.getcwd()
parent_directory = os.path.split(current_dir)[0]
dir_path = "files"
filename = 'knowledge_base.txt'
file_path = os.path.join(parent_directory, dir_path)
file_path = os.path.join(file_path, filename)

# Searches knowledge base trying to match noun or adjective
def search_kb(sentence, noun, adjective):
  
    # Opens knowledge base 
    f = open(file_path, 'r', encoding='utf-8')
    text = f.read()
    text = text.lower()
    text = text.split('\n')
    
    # First tries to check for matches with both noun and adjective. If that fails,
    # it searches for a match with either one
    for line in text:
        if noun is not None and adjective is not None:
            if noun in line and adjective in line:
                print(line)
                return line
        if noun is not None:
            if noun in line:
                return line
        if adjective is not None:
            if adjective in line:
                return line
    
    # If that fails, it tokenizes the sentence and removes stopwords, 
    # it then tries finding a match with one of the words that remains 
    tokens = word_tokenize(sentence)
    stop_words = set(stopwords.words('english'))
    filtered_sentence = [w for w in tokens if not w in stop_words]

    for x in filtered_sentence:
        for line in text:
            if x in line:
                return line

# Searches through knowledge base for mentions of whatever song is passed
def search_kb_song(song, sentence):
    
    # Opens knowledge base 
    f = open(file_path, 'r', encoding='utf-8')
    text = f.read()
    text = text.lower()
    text = text.split('\n')
    
    # Goes through text lines looking for a match with the song
    for line in text:
        if song in line:
            return line
