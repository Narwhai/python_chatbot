import os 
import nltk
import string

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
    #print("Path in KBC: " + path)
    for file in os.listdir(path):
        filename = path + "\\" + os.fsdecode(file)
        #print("Filename: " + filename)
        #file_write = os.path.join(current_working_dir, "knowledge_base")
        with open(filename, "r", encoding='utf=8') as f_in:
            text = f_in.read()
            tokens = nltk.sent_tokenize(text)
            file_write = os.path.join(current_working_dir, "knowledge_base.txt")
            with open(file_write, "a", encoding='utf=8') as f_out:
                for token in tokens:
                    #print("****Sentence: " + token)
                    if any(word in token for word in fact_words):
                        token = token.translate(str.maketrans('','',string.punctuation))
                        #print("*****Token: " + token)
                        f_out.write(token + '\n')

knowledge_base_creator()