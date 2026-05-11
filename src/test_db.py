# import sqlite3
# import pandas as pd

# conn = sqlite3.connect("database/portfolio_database.db")

# query = """SELECT
#     sec.sector_name,
#     SUM(h.current_weight) AS exposure
# FROM holdings h

# JOIN portfolios p
#     ON h.portfolio_id = p.portfolio_id

# JOIN securities s
#     ON h.security_id = s.security_id

# JOIN sectors sec
#     ON s.sector_id = sec.sector_id

# WHERE p.portfolio_name = 'Conservative Income Fund'
# AND s.asset_type = 'Stock'

# GROUP BY sec.sector_name

# ORDER BY exposure DESC;"""

# df = pd.read_sql_query(query, conn)

# print(df)

# conn.close()

from sql_tool import SQLTool

# Create instance
tool = SQLTool()

# Call answer()
response = tool.answer(
    "How many portfolios do we have in total?"
)

print(response)