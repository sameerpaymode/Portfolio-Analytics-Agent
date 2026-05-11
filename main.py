from src.portfolioagent import PortfolioAgent

def answer(question:str):
        
    agent = PortfolioAgent()

    response = agent.answer_question(question=question)
    print("Agent Response : ",response.text)

    usage = response.usage_metadata
    print("\n=== TOKEN USAGE ===")
    print("Prompt Tokens:", usage.prompt_token_count)
    print("Completion Tokens:", usage.candidates_token_count)
    print("Total Tokens:", usage.total_token_count)

    print("\n=== TOOL CALLS ===")

    history = response.automatic_function_calling_history

    for item in history:
        if item.role == "model":
            for part in item.parts:
                if hasattr(part, "function_call") and part.function_call:
                    print("\nTool Used:")
                    print("Function:", part.function_call.name)
                    print("Arguments:")
                    print(part.function_call.args)

        elif item.role == "user":

            for part in item.parts:

                if hasattr(part, "function_response") and part.function_response:

                    print("\nTool Response:")
                    print(part.function_response.response)

def main(question):
    return answer(question)

if __name__ == "__main__":
    question = input("question : ")
    while question != "bye":
        main(question)