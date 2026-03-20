# --8<-- [start:c-style-formatting]
name = "World"
greeting = "Hello, %s!" % name
print(greeting)
# --8<-- [end:c-style-formatting]

# --8<-- [start:string-format-method]
greeting = "Hello, {}!".format(name)
print(greeting)
# --8<-- [end:string-format-method]

# --8<-- [start:f-string]
greeting = f"Hello, {name}!"
print(greeting)
# --8<-- [end:f-string]

# --8<-- [start:bad-formatting]
lat = 45.9711247890
lon = -91.44125437908
loc_string = f"Your location is ({lat}, {lon})"
print(loc_string)
# --8<-- [end:bad-formatting]

# --8<-- [start:precision-formatting]
loc_string = f"Your location is ({lat:.2f}, {lon:.2f})"  # (1)!
print(loc_string)
# --8<-- [end:precision-formatting]

# --8<-- [start:separator-formatting]
grid = "15N"
easting = 491993.112
northing = 4977445.948
loc_string = f"Your location is {grid} {easting:,.0f}m E  {northing:,.0f}m N"  # (1)!
print(loc_string)
# --8<-- [end:separator-formatting]

# --8<-- [start:width-formatting]
population_data = {
    "Hennepin": 1293582,
    "Ramsey": 549097,
    "Traverse": 3052,
    "Lake of the Woods": 3783,
}

for county, population in population_data.items():
    print(f"{county:.<18}{population:.>10,}")  # (1)!

# --8<-- [end:width-formatting]

# --8<-- [start:sql-injection-def]
import sqlite3


def print_secrets(name):
    with sqlite3.connect("data/test.db") as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT secret FROM users WHERE name = '{name}'")
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(*row)
        else:
            print("No records returned")


# --8<-- [end:sql-injection-def]

# --8<-- [start:sql-injection-call-safe]
normal_name = "Alice"
print_secrets(normal_name)
# --8<-- [end:sql-injection-call-safe]

# --8<-- [start:sql-injection-call-unsafe]
malicious_name = "' OR 1=1; -- "
print_secrets(malicious_name)
# --8<-- [end:sql-injection-call-unsafe]


# --8<-- [start:parameterized-queries-def]
def safe_print_secrets(name):
    with sqlite3.connect("data/test.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT secret FROM users WHERE name = ?", (name,))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(*row)
        else:
            print("No records returned")


# --8<-- [end:parameterized-queries-def]

# --8<-- [start:parameterized-queries-call-safe]
safe_print_secrets(normal_name)
# --8<-- [end:parameterized-queries-call-safe]

# --8<-- [start:parameterized-queries-call-unsafe]
safe_print_secrets(malicious_name)
# --8<-- [end:parameterized-queries-call-unsafe]

# --8<-- [start:t-string]
greeting = t"Hello, {name}!"
print(greeting)
# --8<-- [end:t-string]

# --8<-- [start:t-string-to-parameterized-query-def]
from string.templatelib import Interpolation, Template
import traceback


def sanitize_sql(template):
    try:
        if not isinstance(template, Template):
            raise TypeError("Must be a template string")  # (1)!
        parts = []
        args = []
        for item in template:  # (2)!
            if isinstance(item, str):  # (3)!
                parts.append(item)
            elif isinstance(item, Interpolation):  # (4)!
                parts.append("?")  # (5)!
                args.append(item.value)  # (6)!

        query = "".join(parts)
        return query, tuple(args)
    except TypeError:
        return traceback.format_exc()


# --8<-- [end:t-string-to-parameterized-query-def]

# --8<-- [start:t-string-to-parameterized-query-call]
t_string_query = sanitize_sql(t"SELECT secret FROM users WHERE name = {malicious_name}")
print(t_string_query)
# --8<-- [end:t-string-to-parameterized-query-call]

# --8<-- [start:t-string-to-parameterized-query-call-f-string]
f_string_query = sanitize_sql(f"SELECT secret FROM users WHERE name = {malicious_name}")
print(f_string_query)
# --8<-- [end:t-string-to-parameterized-query-call-f-string]


# --8<-- [start:t-string-for-library-def]
class TStringCursor(sqlite3.Cursor):  # (1)!
    def better_execute(self, template):
        return self.execute(*sanitize_sql(template))


def better_print_secrets(name):
    with sqlite3.connect("data/test.db") as conn:
        cur = conn.cursor(factory=TStringCursor)  # (2)!
        cur.better_execute(t"SELECT secret FROM users WHERE name = {name}")
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(*row)
        else:
            print("No records returned")


# --8<-- [end:t-string-for-library-def]

# --8<-- [start:t-string-for-library-call-safe]
better_print_secrets(normal_name)
# --8<-- [end:t-string-for-library-call-safe]

# --8<-- [start:t-string-for-library-call-unsafe]
better_print_secrets(malicious_name)
# --8<-- [end:t-string-for-library-call-unsafe]
