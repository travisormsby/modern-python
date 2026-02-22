# Create dynamic text

It's very useful to be able to create text dynamically from values that are only known at run time. Several different methods for generating such text have been used through Python's history.

## Older methods

The oldest pattern for creating dynamic text used [C-style string formatting](https://docs.python.org/3/tutorial/inputoutput.html#old-string-formatting):

```python
def greet(name):
    greeting = "Hello, %s!" % name
    print(greeting)

greet("World")
```

In 3.0, Python introduced the [`format` method](https://docs.python.org/3/library/stdtypes.html#str.format) on strings:

```python
def greet(name):
    greeting = "Hello, {}!".format(name)
    print(greeting)

greet("World")
```

You may see these patterns in older code. If you're making updates to that code it's better to stay consistent and use the same pattern. But if you're writing new code, it's generally going to be better to use newer patterns.

## F-strings 

In 3.6, Python introduced [formatted string literals](https://docs.python.org/3/reference/lexical_analysis.html#formatted-string-literals), usually called f-strings. Like the `format` method, f-strings use curly braces to identify placeholders. But they put the code to be evaluated inside those braces:

```python
def greet(name):
    greeting = f"Hello, {name}!"
    print(greeting)

greet("World")
```

Relative to older methods, f-strings are easier to understand because you don't have to swap back and forth between the placeholder and the value. For most dynamic text, you should use f-strings.

## Formatting values with f-strings

Because f-strings are often used for prettified user-facing output, raw values are often not a good choice. For example:

```python
lat = 45.9711247890
lon = -91.44125437908
print(f"Your location is ({lat}, {lon})")
```

You could use the `round` function, but that implies you care about the rounded value. You probably don't. You probably just need to represent the true value in a more user-friendly way. The appropriate way to do this is to use Python's [format specification language](https://docs.python.org/3/library/string.html#format-specification-mini-language).

```python
lat = 45.9711247890
lon = -91.44125437908
print(f"Your location is ({lat:.2f}, {lon:.2f})") # (1)!
```

1. > `.2f` means to represent the number with 2 digits to the right of the decimal point in fixed point form.

The distinction between "here is a value" and "here is a representation of a value" is subtle, but meaningful. It's the difference between what the value _is_ and what the value _looks like_. 

Thousands separators are another common use case for format specification:

```python
grid = "15N"
easting = 491993.112
northing = 4977445.948
print(f"Your location is {grid} {easting:,.0f}m E  {northing:,.0f}m N") # (1)!
```

1. > `,.0f` means to represent the number with a thousands separator, 0 digits to the right of the decimal point in fixed point form.

The third most common use case for format specification is aligning text to a specific width, which is useful for making text line up.

```python
population_data = {
    "Hennepin": 1293582,
    "Ramsey": 549097,
    "Traverse": 3052,
    "Lake of the Woods": 3783
}

for county, population in population_data.items():
    print(f"{county:.<18}{population:.>10,}") #(1)!
```

1. > `.<18` means to align the text to the left of a cell at least 18 characters wide, padding any empty spaces with a `.` character. `.>10,` has a similar meaning, but aligned right to a cell at least 10 characters wide, using a thousands separator.

## The problem with f-strings

F-strings make it hard to sanitize user input. That can lead to security vulnerabilities, like SQL injection attacks.

```python
import sqlite3

def print_secrets(name):
    with sqlite3.connect("data/test.db") as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT secret FROM users WHERE name = '{name}'")
        for row in cur.fetchall():
            print(*row)

print_secrets("Alice") #(1)!
print_secrets("' OR 1=1; -- ") #(2)!
```

1. > Shows only Alice's secrets
2. > Shows everybody's secrets

This code works as expected when you pass the function a name. `#!python print_secrets("Alice")` returns only Alice's secrets because the f-string evaluates to:

`"SELECT secret FROM users WHERE name = 'Alice'"`

`#!python print_secrets("' OR 1=1; -- ")` however returns everybody's secrets because the f-string evaluates to:

`"SELECT secret FROM users WHERE name = '' OR 1=1; -- '"`

Since `1=1` is always true, this code will show the secrets of everybody in the database (the `--` starts a line comment to prevent the final `'` from causing a syntax error). 

SQL injections are a well-known attack vector, so there is a defined way to handle this problem. Use parameterized queries, not f-strings:

```python
def safe_print_secrets(name):
    with sqlite3.connect("data/test.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT secret FROM users WHERE name = ?", (name,))
        for row in cur.fetchall():
            print(*row)

safe_print_secrets("Alice") #(1)!
safe_print_secrets("' OR 1=1; -- ") #(2)!
```

1. > Shows only Alice's secrets
2. > Shows nothing because the parameter is invalid

Parameterized queries have the same problem that old-fashioned C-style format strings had. They're difficult to reason about because the values are separated from their position in the string.

## T-strings

To help get the convenience of f-strings with the safety of parameterized queries, in 3.14 Python introduced [template string literals](https://docs.python.org/3/library/string.templatelib.html), also known as t-strings. Other than using a `t` prefix instead of an `f`, the syntax for creating t-strings is identical to f-strings.

But t-strings are not actually strings. The object that gets created is a `Template` and it looks nothing like a `str`.

```python
def greet(name):
    greeting = t"Hello, {name}!" 
    print(greeting)

greet("World")
```

Unlike f-strings, t-strings separate the static part from the dynamic part. When you pass a t-string to a function, it's possible for the function to know which parts might be dangerous and do something about them.

For example, we can create a function that transforms a t-string into a parameterized query:

```python
from string.templatelib import Interpolation, Template


def sanitize_sql(template):
    if not isinstance(template, Template):
        raise TypeError("Must be a template string") #(1)!
    parts = []
    args = []
    for item in template: #(2)!
        if isinstance(item, str): #(3)!
            parts.append(item)
        elif isinstance(item, Interpolation): #(4)!
            parts.append("?") #(5)!
            args.append(item.value) #(6)!

    query = "".join(parts)
    return query, tuple(args)
```

1. > This function fails on any input that isn't a `Template` to keep people from accidentally passing it a potentially-unsafe f-string. 

2. > When you iterate over a `Template` object, you get both the static and dynamic chunks in order. The first chunk will always be a static string (though it might be empty) and so will the last chunk. There will always be exactly one more static string than dynamic Interpolation.

3. > The static string parts of the `Template` were created by whoever wrote t-string and are presumed safe. 

4. > The values from the interpolated parts came from outside the t-string and could be malicious. They may need special handling.

5. > Instead of putting the interpolated value in the query string, we put a `?`, which is what is expected for a parameterized query in `sqlite3`.

6. > The `value` property is what you get from the evaluated expression inside the curly braces of the t-string. Instead of going in the query string, it becomes one of the args that will be passed to the parameterized query string.

Instead of passing the t-string directly to the `execute` method, we can use this function to get the sanitized SQL. That information can be passed to the `execute` method safely as a parameterized query. That gives us the convenience of an f-string without the risk.

Unfortunately, there's still another problem. You have to remember to pass the string to `sanitize_sql` every single time. You can't forget even once. That kind of responsibility is better borne by library authors than people using the libraries. 

Most libraries, including `sqlite3`, are still working on adding support for t-strings. It's a hard job because in reality it's much more complex than just using the example sanitizing code above. We can, however, fake it for simple cases with an extension of the `Cursor` object.

```python
class TStringCursor(sqlite3.Cursor): #(1)!
    def better_execute(self, template):
        return self.execute(*sanitize_sql(template))


def patched_print_secrets(name):
    with sqlite3.connect("data/test.db") as conn:
        cur = conn.cursor(factory=TStringCursor) #(2)!
        cur.better_execute(t"SELECT secret FROM users WHERE name = {name}")
        for row in cur.fetchall():
            print(*row)

patched_print_secrets("Alice") #(3)!
patched_print_secrets("' OR 1=1; -- ") #(4)!
```

1. > A new class that has everything the original `sqlite3.Cursor` object has, plus a `better_execute` method that only lets you execute sanitized t-strings as parameterized queries.

2. > The `factory` parameter is `sqlite3`'s supported pattern for extending the `Cursor` object with custom functionality.

3. > Shows only Alice's secrets.

4. > Shows nothing because the parameter is invalid after sanitizing the t-string.