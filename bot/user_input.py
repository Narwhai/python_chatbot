branches = ["albums","songs","personal"]

topics = ["Frank Ocean", "Blonde", "Endless", "Channel Orange", "Nostalgia Ultra", "Blonded Radio"]

modifiers = ["statement","greeting","bot comment","answer","favorite","affirmative","negative"]

farewell = ["bye","goodbye","good-bye","farewell", "see ya"]

negative = ["no","nope","never","nah","don't","not","negative"]

affirmative = ["yes","yeah","yep","sure","affirmative"]

def human_response(text, memory):
    text = text.lower()

    for x in farewell:
        if x in text:
            memory["goodbye"] = True
    
    if memory.get("asking branch") is True:
        for x in topics:
            if x in text:
                memory["topics"] = x
            del(memory["asking branch"])
