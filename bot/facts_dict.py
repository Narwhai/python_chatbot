import re
import os

# Facts are taken from facts.txt and added to a Dictionary
def create_facts_dict():
    
    current_dir: str = os.getcwd()
    parent_directory = os.path.split(current_dir)[0]
    dir_path = 'files'
    filename = 'facts.txt'
    file_path = os.path.join(parent_directory, dir_path)
    file_path = os.path.join(file_path, filename)

    f = open(file_path, 'r', encoding='utf-8')

    text = f.read()
    text = text[:-2]
    text = text.lower()
    text = text.split('*')
    facts = {}
    
    for x in text:
        x = x.split('\n')
        if '' in x:
            x.remove('')
        if x[0] not in facts:
            facts[x[0]] = x[1:len(x)-1]
    return facts

create_facts_dict()

