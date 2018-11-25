import re

# This puts the the facts from facts.txt into a dictionary
def get_facts():
    f = open('facts.txt', encoding='utf-8')
    text = f.read()
    text = text.lower()
    #text = text.replace('--', ' ')
    #text = re.sub(r"[,\/#!?$%\^&\*;:{}=\-\'_`~()\"]+", ' ', text)
    text = text.split('*')
    dict = {}

    for x in text:
        x = x.split('\n')
        if '' in x:
            x.remove('')
        if x[0] not in dict:
            dict[x[0]] = x[1:len(x)-1]

    #for x in dict:
        #print(x)
        #print(dict[x])
        #print("***\n")


get_facts()
