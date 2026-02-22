# %%
def greet(name):
    greeting = "Hello, %s!" % name
    print(greeting)


greet("World")

# %%
lat = 45.9711247890
lon = -91.44125437908
print(f"Your location is ({lat}, {lon})")

# %%
grid = "15N"
easting = 491993.112
northing = 4977445.948
print(f"Your location is {grid} {easting:,.0f}m E  {northing:,.0f}m N")

# %%
population_data = {
    "Hennepin": 1293582,
    "Ramsey": 549097,
    "Traverse": 3052,
    "Lake of the Woods": 3783,
}

for county, population in population_data.items():
    print(f"{county:.<18}{population:.>10,}")

# %%
import sqlite3


def print_secrets(name):
    with sqlite3.connect("data/test.db") as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT secret FROM users WHERE name = '{name}'")
        for row in cur.fetchall():
            print(*row)


print_secrets("Alice")
