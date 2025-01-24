from assistant import Assistant

ariana = Assistant()
system_prompt = ""
response = ariana.get_completion("hello, who is this")
print(response) 

while True: 
    prompt = input("\n")
    response = ariana.get_completion(prompt)
    print(response) 