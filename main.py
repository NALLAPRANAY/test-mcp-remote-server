import os
import sqlite3
from fastmcp import FastMCP

mcp=FastMCP("ExpenseTracking")

DB_PATH=os.path.join(os.path.dirname(__file__),"expenses.db")
CATEGORIES_PATH=os.path.join(os.path.dirname(__file__),"categories.json")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT DEFAULT '',
            note TEXT DEFAULT ''
            )
            """
        )

init_db()

@mcp.tool()
def add_expense(date, amount,category,subcategory='',note=''):
    """Add an expense to the database"""
    with sqlite3.connect(DB_PATH) as c:
        curs=c.execute(
            """
            INSERT INTO expenses (date, amount,category,subcategory,note ) VALUES (?,?,?,?,?)
         
            """,
            (date, amount,category,subcategory,note)
        )
        return {'status':'OK','id':curs.lastrowid}


@mcp.tool()
def list_expenses():
    '''list all the expenses'''
    with sqlite3.connect(DB_PATH) as c:
        cur=c.execute("""
                SELECT id, date, amount,category,subcategory,note from expenses ORDER BY id ASC  """)
        cols=[col[0] for col in cur.description]
        return [dict(zip(cols,r)) for r in cur.fetchall()]

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    """List of categories and subcategories"""
    with open(CATEGORIES_PATH) as f:
        return f.read()

if __name__=="__main__":
    mcp.run(transport="http",host="0.0.0.0",port=8000)

