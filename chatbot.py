from openai import OpenAI

client = OpenAI()

# accepts a preferred model and a list of messages
# makes chat completions API call
# returns the response message content
def get_api_chat_response_message(model, messages):
    # make the API call
    api_response = client.chat.completions.create(
        model = model,
        messages = messages
    )

    # extract the response text
    response_content = api_response.choices[0].message.content

    # return the response text
    return response_content

model = "gpt-3.5-turbo"

# create a multi-turn conversation
# an array that will store the chat history
chat_history = []

# define user_input as an empty string
user_input = ""

# start a while loop that runs forever until explicitly broken out of
while True:
    # at the start, write an if statement when the user_input string is empty
    if (user_input == ""):
        user_input = input("Chatbot: Hello there, I'm your helpful chatbot!  Type exit to end our chat. What is your name? ")
        chat_history.append({
            "role": "user",
            "content": user_input
        })

    # write an else, once the user responds
    else: 
        user_input = input("You:  ") #Prompt the user for input
    
    # write an if statement for user to stop the loop using 'break'exit
    if user_input.lower() == "exit": #if ueser types "exit", stop the loop
        break
    
    # add the user's input in the chat history
    chat_history.append({
        "role": "user",
        "content": user_input
    })
  
    # calls the api
    response = get_api_chat_response_message(model, chat_history)

    # display the model's resopnse back to the user
    print("Chatbot: ", response)

    # append the model's response to the chat history
    chat_history.append({
        "role": "assistant",
        "content": response
    })

  