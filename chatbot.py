from openai import OpenAI
import tiktoken
import logging # import logging library
import datetime # import datetime to allow logging the current date and time

# create a dedicated logger for token counting, basic config function
log = logging.getLogger("chatbot_token_count")
# log the information at the INFO level, logger retrieval function
logging.basicConfig(filename = "chatbot_token_count.log", level = logging.INFO)

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

    # return the response
    return api_response

# extract and return the response text, separated response parsing from the api call
def get_response_message(response):
    return response.choices[0].message.content

# extract and return the total number of tokens, separated response parsing from the api call
def get_response_total_tokens(response):
    return response.usage.total_tokens

model = "gpt-3.5-turbo"

# tiktoken function to encode prompts
encoding = tiktoken.encoding_for_model(model)

# variable set to the model's input token limit (16385-4096 = max 12289)
token_input_limit = 12289

# initialize total tokens used outside of the loop
total_token_count = 0

# an array that will store the chat history
chat_history = []

# define user_input as an empty string
user_input = ""

# start a while loop that runs forever until explicitly broken out of
while True:
      # at the start, write an if statement when the user_input string is empty
    if (user_input == ""):
        user_input = input("Chatbot: Hello there, I'm your helpful chatbot! Type exit to end our chat. What's your name? ")
        # write an else, once the user responds
    else:
        user_input = input("You: ") #Prompt the user for input
    # write an if statement for user to stop the loop using 'break'exit
    if user_input.lower() == "exit":  #if user types "exit", stop the loop
        # logger method, use info method to log the message with the INFO level for the current date and time, and total tokens used in the chat session
        log.info("\nDate: " + str(datetime.datetime.now()) + "\nTotal tokens: " + str(total_token_count) + "\n\n")
        # replaced break with exit() 
        exit()
	
    # update the token_count to be the length of the user input
    token_count = len(encoding.encode(user_input))
    
    # code to check the user's prompt against the input token limit
    if (token_count > token_input_limit):
        print("Your prompt is too long. Please try again.")
        continue

    # add the user's input in the chat history
    chat_history.append({
        "role": "user",
        "content": user_input
    })
    
     # calls the api 
    response = get_api_chat_response_message(model, chat_history)
     # call the response text function and pass the response object from above, extracted message is stored in response_message
    response_message = get_response_message(response)
    # call the function that returns the total number of tokens used in the response and store in the variable
    response_total_tokens = get_response_total_tokens(response)
    # update the total tokens used by adding the response tokens to it keeping it current
    total_token_count += response_total_tokens

    # display the chat history response back to the user
    print("Chatbot: ", response_message)

    # append the model's response to the chat history
    chat_history.append({
        "role": "assistant",
        "content": response_message
    })