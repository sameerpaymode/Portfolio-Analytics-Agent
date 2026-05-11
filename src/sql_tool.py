import sqlite3
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()



DB_PATH = "database/portfolio_database.db"


class SQLTool:

    def __init__(self):
        # self.conn = sqlite3.connect(DB_PATH)
        self.conn = sqlite3.connect(
            f"file:{DB_PATH}?mode=ro",
            uri=True
        )
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        # Load schema once during init
        self.schema = self.load_schema()

    def load_schema(self):
        """
        Load complete database schema dynamically
        """

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT name, sql
            FROM sqlite_master
            WHERE type='table'
        """)

        tables = cursor.fetchall()

        schema = "\n\n".join(
            [table_sql for _, table_sql in tables if table_sql]
        )

        return schema

    def generate_sql(self, question):

        prompt = f"""
        You are an expert SQL generator.

        Database schema:
        {self.schema}

        Rules:
        - Generate ONLY valid SQLite SQL
        - No markdown
        - No explanation
        - No ```sql
        - only on single line (no new line)


        Question:
        {question}
        """

        response = self.client.models.generate_content(
            model=os.getenv("GEMINI_MODEL"),
            contents=prompt
        )

        sql = (
            response.text
            .strip()
            .replace("```sql", "")
            .replace("```", "")
        )

        return sql

    def run_query(self, sql):

        # Basic safety
        # if not sql.lower().startswith("select"):
        #     raise Exception("Only SELECT queries are allowed")

        cursor = self.conn.cursor()

        cursor.execute(sql)

        columns = [desc[0] for desc in cursor.description]

        rows = cursor.fetchall()

        # Convert rows into dicts
        result = [
            dict(zip(columns, row))
            for row in rows
        ]

        return result

    def answer(self, question):

        sql = self.generate_sql(question)

        result = self.run_query(sql)

        formatted = self.format_result(result)

        return {
            "sql": sql,
            "type": formatted["type"],
            "result": formatted["result"]
        }


    def format_result(self, result):

        # Empty result
        if not result:
            return {
                "type": "empty",
                "result": []
            }

        # Assume result is list of dicts
        first_row = result[0]

        num_rows = len(result)
        num_cols = len(first_row)

        # Single value
        if num_rows == 1 and num_cols == 1:
            return {
                "type": "single_value",
                "result": list(first_row.values())[0]
            }

        # Single column -> list
        if num_cols == 1:
            col_name = list(first_row.keys())[0]

            return {
                "type": "list",
                "result": [row[col_name] for row in result]
            }

        # Multi-column -> table
        return {
            "type": "table",
            "result": result
        }




    def calculate_sector_exposure(
        self,
        portfolio_name: str
    ):

        query = """
        SELECT
            sec.sector_name,
            ROUND(SUM(h.current_weight), 2) AS exposure_percentage

        FROM holdings h

        JOIN portfolios p
            ON h.portfolio_id = p.portfolio_id

        JOIN securities s
            ON h.security_id = s.security_id

        JOIN sectors sec
            ON s.sector_id = sec.sector_id

        WHERE
            p.portfolio_name = ?
            AND s.asset_type = 'Stock'

        GROUP BY sec.sector_name

        ORDER BY exposure_percentage DESC
        """

        cursor = self.conn.cursor()

        cursor.execute(
            query,
            (portfolio_name,)
        )

        rows = cursor.fetchall()

        columns = [
            desc[0]
            for desc in cursor.description
        ]

        result = [
            dict(zip(columns, row))
            for row in rows
        ]

        return {
            "portfolio": portfolio_name,
            "sector_exposures": result
        }    
    


# if __name__ == "__main__":

#     tool = SQLTool()

#     response = tool.answer(
#         "Show all projects ordered by latest"
#     )

#     print("\nGenerated SQL:")
#     print(response["sql"])

#     print("\nResult:")
#     print(response["result"])