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


def print_secrets(name):
    with sqlite3.connect("data/test.db") as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT secret FROM users WHERE name = '{name}'")
        for row in cur.fetchall():
            print(*row)


def safe_print_secrets(name):
    with sqlite3.connect("data/test.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT secret FROM users WHERE name = ?", (name,))
        for row in cur.fetchall():
            print(*row)


from string.templatelib import Interpolation, Template


def sanitize_sql(template):
    if not isinstance(template, Template):
        raise TypeError("Must be a template string")
    parts = []
    args = []
    for item in template:
        if isinstance(item, str):
            parts.append(item)
        elif isinstance(item, Interpolation):
            parts.append("?")
            args.append(item.value)

    query = "".join(parts)
    return query, tuple(args)


class TStringCursor(sqlite3.Cursor):
    def better_execute(self, template):
        return self.execute(*sanitize_sql(template))


def patched_print_secrets(name):
    with sqlite3.connect("data/test.db") as conn:
        cur = conn.cursor(factory=TStringCursor)
        cur.better_execute(t"SELECT secret FROM users WHERE name = {name}")
        for row in cur.fetchall():
            print(*row)


print_secrets("Alice")
print_secrets("Alice' OR 1=1; -- ")
safe_print_secrets("Alice")
safe_print_secrets("Alice' OR 1=1; -- ")
patched_print_secrets("Alice")
patched_print_secrets("Alice' OR 1=1; -- ")
