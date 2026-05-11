from google import genai
from google.genai import types

from dotenv import load_dotenv
import os
load_dotenv()

from src.sql_tool import SQLTool


class PortfolioAgent:
    def __init__(self):
        # self.db_connection = sqlite3.connect('portfolio_database.db')
        self.sql_tool = SQLTool()
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )
        
    def ask_database(self,question: str) -> dict:
        """
        Ask questions to the portfolio database.
        Generates SQL and returns query results.
        """
        return self.sql_tool.answer(question)

    def exposure_calculator(self,portfolio_name:str):
        """
        calculate sector exposures for specific portfolio. 
        """
        return self.sql_tool.calculate_sector_exposure(portfolio_name=portfolio_name)
    
    def answer_question(self, question):
        # Your logic here
        config = types.GenerateContentConfig(
            tools=[self.ask_database, self.exposure_calculator]
        )

        response = self.client.models.generate_content(
            model=os.getenv("GEMINI_MODEL"),
            contents=question,
            config= config,
        )

        return response
        