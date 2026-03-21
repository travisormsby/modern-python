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
from sqlalchemy import create_engine, text

DATABASE_URL = "sqlite:///data/test.db"


def print_secrets(name, database=DATABASE_URL):
    engine = create_engine(database)
    with engine.connect() as conn:
        stmt = text(f"SELECT secret FROM users WHERE name = '{name}'")
        rows = conn.execute(stmt).fetchall()
        if rows:
            for row in rows:
                print(*row)
        else:
            print("No records returned")


# --8<-- [end:sql-injection-def]

# --8<-- [start:sql-injection-call-normal]
normal_name = "Alice"
print_secrets(normal_name)
# --8<-- [end:sql-injection-call-normal]

# --8<-- [start:sql-injection-call-malicious]
malicious_name = "' OR 1=1; -- "
print_secrets(malicious_name)
# --8<-- [end:sql-injection-call-malicious]


# --8<-- [start:parameterized-queries-def]
def print_secrets(name, database=DATABASE_URL):
    engine = create_engine(database)
    with engine.connect() as conn:
        stmt = text("SELECT secret FROM users WHERE name = :name")
        params = {"name": name}
        rows = conn.execute(stmt, params).fetchall()
        if rows:
            for row in rows:
                print(*row)
        else:
            print("No records returned")


# --8<-- [end:parameterized-queries-def]

# --8<-- [start:parameterized-queries-call-normal]
print_secrets(normal_name)
# --8<-- [end:parameterized-queries-call-normal]

# --8<-- [start:parameterized-queries-call-malicious]
print_secrets(malicious_name)
# --8<-- [end:parameterized-queries-call-malicious]

# --8<-- [start:t-string]
greeting = t"Hello, {name}!"
print(greeting)
# --8<-- [end:t-string]

# --8<-- [start:tag-function]
from string.templatelib import Interpolation


def print_tstring(tstring):
    output_str = ""
    for item in tstring:
        if isinstance(item, str):  # (1)!
            output_str += item
        elif isinstance(item, Interpolation):  # (2)!
            output_str += item.value
    print(output_str)


print_tstring(greeting)
# --8<-- [end:tag-function]


# --8<-- [start:t-string-in-library-def]
from sqlalchemy import tstring


def print_secrets(name, database=DATABASE_URL):
    engine = create_engine(database)
    with engine.connect() as conn:
        stmt = tstring(t"SELECT secret FROM users WHERE name = {name}")  # (1)!
        rows = conn.execute(stmt).fetchall()
        if rows:
            for row in rows:
                print(*row)
        else:
            print("No records returned")


# --8<-- [end:t-string-in-library-def]

# --8<-- [start:t-string-in-library-call-normal]
print_secrets(normal_name)
# --8<-- [end:t-string-in-library-call-normal]

# --8<-- [start:t-string-in-library-call-malicious]
print_secrets(malicious_name)
# --8<-- [end:t-string-in-library-call-malicious]
