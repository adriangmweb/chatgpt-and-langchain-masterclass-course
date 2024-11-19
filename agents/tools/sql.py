import sqlite3
from langchain_community.tools import Tool
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(f'{current_dir}/../db.sqlite')

def run_sqlite_query(query: str) -> str:
    c = conn.cursor()
    c.execute(query)
    return c.fetchall()

run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a sqlite query against the database",
    func=run_sqlite_query
)
