import os
import nltk
import string
from nltk import tokenize

current_working_dir: str = os.getcwd()

# Creates a smaller knowledge base focused only on facts about Frank Ocean, his albums, and his radio show
def fact_curator():

    topics = ["frank ocean", "channel orange", "blonde ", "nostalgia ultra", "endless", "blonded radio"]
    filename = "facts.txt"
    dir_path = os.path.join(current_working_dir, "files")
    file_write = os.path.join(dir_path, filename)
    file_read = os.path.join(dir_path, "knowledge_base.txt")
    
    knowledge_base = open(file_read, 'r', encoding='utf-8')
    
    # Goes through bigger knowledge base and picks out lines that contain one of the topics.
    # It goes through each topic one at a time, and topics are separated with a '*' and a newline
    for topic in range(len(topics)):
        knowledge_base.seek(0)
        if topic >= len(topics):  
            break
        else:
            with open(file_write, "a", encoding='utf-8') as f_out:
                f_out.write(topics[topic] + "\n")
                for line in knowledge_base:
                    if topics[topic] in line:
                        out = line
                        out = ' '.join(out.split())
                        f_out.write(out + "\n")
                f_out.write("*\n")

# Creates a knowledge base from the clean files obtained from the web scraper
# TODO actually might be better to use the raw files 
def knowledge_base_creator():
    
    # Words related to Frank Ocean
    fact_words = ["frank", "ocean", "orange", "blonde", "endless", "nostalgia", "ultra", "album",
                    "mixtape", "release", "name", "lyrics", "genre", "rb ", " rb", "r&b", "music", "born",
                    "birth", "california", "topic", "production", "instrumentation","recording",
                    "contract", "studio", "single", "vocal","christopher", "lonny", "breaux" ,
                    "francis", "edwin", "musical", "career", "future", "style", "wrote", "write",
                    "song", "songs", "cover", "art", "label", "channel", "influenced", "influence",
                    "released", "release", "acclaim", "critical", "def", "jam", "tour", "date", "blonded",
                    "radio", "beats1", "interview", "beats", "birthday", "grammy", "video", "mtv", "written"
                    "deal", "songwriting", "oceans" "franks", "tracks", "track", "featuring", "billboard", 
                    "billboards"]    

    path = os.path.join(current_working_dir, "clean_files")

    # Goes through each file in the directory and finds lines that can be added to the knowledge base
    for file in os.listdir(path):
        filename = path + "\\" + os.fsdecode(file)
        with open(filename, "r", encoding='utf=8') as f_in:
            text = f_in.read()
            tokens = nltk.sent_tokenize(text)
            file_write = os.path.join(current_working_dir, "files")
            file_write = os.path.join(file_write, "knowledge_base.txt")
            # A new directory is created to hold the knowledge bases
            os.makedirs(os.path.dirname(file_write), exist_ok=True)
            with open(file_write, "a", encoding='utf=8') as f_out:
                for token in tokens:
                    if any(word in token for word in fact_words):
                        token = token.translate(str.maketrans('','',string.punctuation))
                        f_out.write(token + '\n')