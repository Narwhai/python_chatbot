import os
import nltk
import string
from nltk import tokenize

current_working_dir: str = os.getcwd()

def fact_curator():

    topics = ["frank ocean", "channel orange", "blonde ", "nostalgia ultra", "endless", "blonded radio"]
    filename = "facts.txt"
    dir_path = os.path.join(current_working_dir, "files")
    file_write = os.path.join(dir_path, filename)
    file_read = os.path.join(dir_path, "knowledge_base.txt")
    
    knowledge_base = open(file_read, 'r', encoding='utf-8')
    
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

def knowledge_base_creator():
    
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

    current_working_dir: str = os.getcwd()
    path = os.path.join(current_working_dir, "clean_files")
    for file in os.listdir(path):
        filename = path + "\\" + os.fsdecode(file)
        with open(filename, "r", encoding='utf=8') as f_in:
            text = f_in.read()
            tokens = nltk.sent_tokenize(text)
            file_write = os.path.join(current_working_dir, "files")
            file_write = os.path.join(file_write, "knowledge_base.txt")
            os.makedirs(os.path.dirname(file_write), exist_ok=True)
            with open(file_write, "a", encoding='utf=8') as f_out:
                for token in tokens:
                    if any(word in token for word in fact_words):
                        token = token.translate(str.maketrans('','',string.punctuation))
                        f_out.write(token + '\n')