## c-style strings are bad
# %%

species = "Canada lynx"
lat = 48.8
lon = 93.2

output = "A %s was sighted at %d° N, %d° W" % (species, lat, lon)
print(output)

# .format method is bad
# %%
output = "A {} was sighted at {}° N, {}° W".format(species, lat, lon)
print(output)

# f-strings are good
# %%
output = f"A {species} was sighted at {lat}° N, {lon}° W"
print(output)

# f-strings are insecure
# %%
from sqlalchemy import create_engine, text


def print_secrets(name):
    engine = create_engine("sqlite:///data/users.db")
    with engine.connect() as conn:
        stmt = text(f"SELECT secret FROM users WHERE name = '{name}'")
        rows = conn.execute(stmt).fetchall()
        if rows:
            for row in rows:
                print(*row)
        else:
            print("No records returned")


# %%
normal_name = "Alice"
print_secrets(normal_name)

# %%
malicious_name = "' OR 1=1; -- "
print_secrets(malicious_name)

# t-strings are more secure
# %%
from sqlalchemy import tstring


def print_secrets(name):
    engine = create_engine("sqlite:///data/users.db")
    with engine.connect() as conn:
        # stmt = text(f"SELECT secret FROM users WHERE name = '{name}'")
        stmt = tstring(t"SELECT secret FROM users WHERE name = {name}")
        rows = conn.execute(stmt).fetchall()
        if rows:
            for row in rows:
                print(*row)
        else:
            print("No records returned")


# String methods are bad
# %%
filepath = "/data/country=Bangladesh/year=1997/buildings.parquet"
parts = filepath.split("/")
file_name = parts[-1]
file_stem = file_name.replace(".parquet", "")
params = "&".join([p for p in parts if "=" in p])
url = f"https://api.example.com/{file_stem}?{params}"
print(url)

# os.path.join is only a little better
# %%
import os

parts = filepath.split(os.sep)
file_name = parts[-1]
file_stem = os.path.splitext(file_name)[0]
params = "&".join([p for p in parts if "=" in p])
url = f"https://api.example.com/{file_stem}?{params}"
print(url)

# pathlib is much better
# %%
from pathlib import Path

filepath = Path(filepath)
params = "&".join([p for p in filepath.parts if "=" in p])
url = f"https://api.example.com/{filepath.stem}?{params}"
print(url)


# %%
correct = {"propertyId": "0123456789", "value": 251482.17}
missing_field = {"value": 251482.17}
wrong_types = {"propertyId": 1234567890, "value": "324398.71"}
uncoercable = {
    "propertyId": ["0123456789", "1234567890"],
    "value": [251482.17, 324398.71],
}

# Pydantic (v2) is best
# %%
from pydantic import BaseModel, ConfigDict, ValidationError


class ValidSubmission(BaseModel):
    propertyId: str
    value: float
    model_config = ConfigDict(coerce_numbers_to_str=True)


for submission in (correct, missing_field, wrong_types, uncoercable):
    try:
        print(ValidSubmission(**submission))
    except ValidationError as e:
        for error in e.errors():
            print(error["msg"])
