from bu_chatgpt import HKBU_ChatGPT

def main():
    print("Welcome to the HKBU ChatGPT CLI!")
    print("Type 'exit' to quit the program.\n")

    # Initialize the HKBU_ChatGPT instance
    chatgpt = HKBU_ChatGPT()

    while True:
        # Get user input
        user_input = input("You: ")
        
        # Exit condition
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # Submit the input to ChatGPT and get the response
        try:
            response = chatgpt.submit(user_input)
            print(f"ChatGPT: {response}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()