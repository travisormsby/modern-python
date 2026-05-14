#!/usr/bin/env

# --8<-- [start:os-path-join]
import os

root = "/home/user/scripts"
filename = "test.py"
full_path = os.path.join(root, filename)
print(full_path)
# --8<-- [end:os-path-join]

# --8<-- [start:os-path-split]
new_file = os.path.splitext(full_path)[0] + ".txt"
print(new_file)
# --8<-- [end:os-path-split]

# --8<-- [start:pathlib]
from pathlib import Path

root_path = Path(root)
full_path = root_path / filename
print(full_path)
# --8<-- [end:pathlib]

# --8<-- [start:path-type]
path_type = type(full_path)
print(path_type)
# --8<-- [end:path-type]

# --8<-- [start:keys]
path_dict = {full_path: "This is the full path"}
print(path_dict)

# --8<-- [end:keys]

# --8<-- [start:parts]
print(full_path.parts)

# --8<-- [end:parts]

# --8<-- [start:parent]
print(full_path.parent)

# --8<-- [end:parent]

# --8<-- [start:name]
print(full_path.name)
print(full_path.stem)
print(full_path.suffix)
print(full_path.with_suffix(".txt"))

# --8<-- [end:name]


# --8<-- [start:absolute]
relative_path = Path("docs/03-manipulate-filepaths.md")
full_path = relative_path.absolute()
print(full_path)
# --8<-- [end:absolute]

# --8<-- [start:exists]
print(full_path.exists())
print(full_path.is_file())
print(full_path.is_dir())
# --8<-- [end:exists]

# --8<-- [start:iterdir]
for child in full_path.parent.iterdir():
    if child.is_file():
        print(child.name)
# --8<-- [end:iterdir]

# --8<-- [start:glob]
markdown_files = full_path.parent.glob("0*.md")
for file in markdown_files:
    print(file.name)
# --8<-- [end:glob]

# --8<-- [start:path-input]
import sqlite3
import pandas as pd

database = Path("data/example.db")
conn = sqlite3.connect(database)
df = pd.read_sql_query("SELECT * FROM users", conn)
print(df)

# --8<-- [end:path-input]

# --8<-- [start:path-input-fail]
import json
import traceback

filepath = Path("data/example.db")
data = {"file": filepath}


def print_json(data):
    try:
        json_str = json.dumps(data)
        print(json_str)
    except TypeError:
        print(traceback.format_exc())


print_json(data)

# --8<-- [end:path-input-fail]

# --8<-- [start:str-input]
data = {"file": str(filepath)}
print_json(data)


# --8<-- [end:str-input]


# --8<-- [start:open]
filepath = Path("data/example.txt")

with open(filepath, "w") as f:
    f.write("This is some example text")

with open(filepath, "r") as f:
    print(f.read())
# --8<-- [end:open]

# --8<-- [start:write-read]
filepath.write_text("Some new text to overwrite the old")
read_text = filepath.read_text()
print(read_text)
# --8<-- [end:write-read]
