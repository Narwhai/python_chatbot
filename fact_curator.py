import sys, os

def fact_curator():
    #current_working_dir: str = os.getcwd()

    topics = ["frank ocean", "channel orange", "blonde ", "nostalgia ultra", "endless", "blonded radio"]

    knowledge_base = open("knowledge_base.txt", 'r', encoding='utf-8')
    
    filename = "facts.txt"
    
    for topic in range(len(topics)):
        fact_count = 0
        knowledge_base.seek(0)
        if topic >= len(topics):  
            break
        else:
            with open(filename, "a", encoding='utf-8') as f_out:
                f_out.write(topics[topic] + "\n")
                for line in knowledge_base:
                    if topics[topic] in line:
                        out = line
                        out = ' '.join(out.split())
                        f_out.write(out + "\n")
                        fact_count += 1
                    if fact_count == 11 and topic < (len(topics)-1):
                        f_out.write("*" + "\n")                        
                    if fact_count == 11: 
                        break

    """
    for line in knowledge_base:
        count = 0
        #print(topic_count)
        if topic_count >= len(topics):
            break
        else:
            #print("*********")
            #print(topics[topic_count])
            for x in range(len(topics)):
                #print(topics[topic_count])
                if topics[x] in line:
                    print(line.split(topics[x],1)[1])
                    count += 1
                if count == 2:
                    topic_count += 1
                    break

        if "frank ocean" in line:
            print(line.split("frank ocean",1)[1])
            count += 1
        #print(count)
        if count == 5:
            break
        """
fact_curator()