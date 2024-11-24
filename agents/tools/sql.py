import sqlite3
from langchain_community.tools import Tool
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(f'{current_dir}/../db.sqlite')

def list_tables() -> str:
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    return "\n".join([row[0] for row in rows if row[0] is not None])

def describe_table(table_names: list[str]) -> str:
    c = conn.cursor()
    tables = ', '.join(f"'{table_name}'" for table_name in table_names)
    rows = c.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name IN ({tables});")
    return "\n".join([row[0] for row in rows if row[0] is not None])


def run_sqlite_query(query: str) -> str:
    c = conn.cursor()
    try:
        c.execute(query)
        return c.fetchall()
    except sqlite3.OperationalError as err:
        return f"The following error occurred: {str(err)}"
    
run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a sqlite query against the database",
    func=run_sqlite_query
)

list_tables_tool = Tool.from_function(
    name="list_tables",
    description="List all tables in the database",
    func=list_tables
)

describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of table names, describe the tables",
    func=describe_table
)