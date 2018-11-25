import user_input

running = True
introduction = False 
used_facts = {}
memory = {}

while running:
    if not introduction:
        name = input("Hello I'm a Frank Ocean expert. Who are you? ")
        memory["name"] = name
        user_response = name
        introduction = True
    else:
        user_response = input(bot_response+"\n:")

    memory = user_input.human_response(user_response, memory)

    bot_response, memory = response.create_response(memory)

    if memory.get("goodbye"):
        running = False
        print(bot_response)