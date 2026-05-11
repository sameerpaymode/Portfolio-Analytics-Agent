from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from sql_tool import SQLTool
load_dotenv()

# def test_tool():
#     """use this tool to test if tool is working"""
#     return "working tool and say - its all okay and mention passcode: sameer is a good boi"

sql_tool = SQLTool()


# Wrapper function for Gemini
def ask_database(question: str) -> dict:
    """
    Ask questions to the portfolio database.
    Generates SQL and returns query results.
    """
    return sql_tool.answer(question)

# Configure the client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

config = types.GenerateContentConfig(
    tools=[ask_database]
)

# Make the request
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="hi there, How many portfolios do we have in total? name all",
    config=config,
)

print("\nExample 2: Automatic function calling")
print(response.text)
