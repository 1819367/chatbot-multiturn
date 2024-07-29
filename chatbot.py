from openai import OpenAI
import tiktoken

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

    # Print the entire API response to evaluate token usage
    # print("API Response:", api_response)

    # Print token usage
    # print("Token Usage:", api_response.usage)

    # extract the response text
    response_content = api_response.choices[0].message.content

    # return the response text
    return response_content

model = "gpt-3.5-turbo"

# tiktoken function to encode prompts
encoding = tiktoken.encoding_for_model(model)

# print statement to print out the encoding variable
# print(encoding)

# variable set to the model's input token limit (16385-4096 = max 12289)
token_input_limit = 12289

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
         # write an else, once the user responds
    else: 
        user_input = input("You:  ") #Prompt the user for input
    # write an if statement for user to stop the loop using 'break'exit
    if user_input.lower() == "exit": #if ueser types "exit", stop the loop
        # break, replaced with exit()
        exit()

    # encode the user's input with tiktoken 
    # user_input_encoded = encoding.encode(user_input)
    # print the encoded under input
    # print(user_input_encoded)

    # update the token_count to be the length of the user input
    token_count = len(encoding.encode(user_input))
    # print the token count
    # print(f"Token Count: {token_count}")

    # code to check the user's prompt against the input token limit
    if (token_count > token_input_limit):
        print("Your prompt is too long.  Please try again.")
        continue

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

  