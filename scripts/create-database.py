import sqlite3
from sqlalchemy import create_engine, text

create_table = """
    CREATE TABLE IF NOT EXISTS users (
        name text NOT NULL,
        secret text NOT NULL
    )
"""
data = {
    "Alice": "Alice secret info",
    "Bob": "Bob secret info",
    "Carol": "Carol secret info",
}

with sqlite3.connect("data/test.db") as conn:
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute(create_table)
    for name, secret in data.items():
        cur.execute(f"INSERT INTO users(name, secret) VALUES('{name}', '{secret}')")


# maybe sqlalchemy will support t-strings by the time of the workshop
def print_secrets_sqlalchemy(name):
    engine = create_engine("sqlite:///data/test.db")
    with engine.connect() as conn:
        query = text(f"SELECT secret FROM users WHERE name = '{name}'")
        for row in conn.execute(query):
            print(*row)
