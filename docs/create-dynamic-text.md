# Create dynamic text

It's very useful to be able to create text dynamically from values that are only known at run time. Reports, logging, debugging, and presenting information to users all frequently require information that won't be known ahead of time. 

Several different methods for generating such text have been used through Python's history.

## Older methods

The oldest pattern for creating dynamic text used [C-style string formatting](https://docs.python.org/3/tutorial/inputoutput.html#old-string-formatting):

```python
--8<-- "snippets/02-create-dynamic-text.py:c-style-formatting"
```

```text title="output"
--8<-- "output/02-create-dynamic-text.txt:c-style-formatting"
```

In 3.0, Python introduced the [`format` method](https://docs.python.org/3/library/stdtypes.html#str.format) on strings:

```python
--8<-- "snippets/02-create-dynamic-text.py:string-format-method"
```

```text title="output"
--8<-- "output/02-create-dynamic-text.txt:string-format-method"
```

You may see either of these patterns in older code. If you're making updates to code that uses these patterns, it's better to stay consistent and use the same pattern. 

But if you're writing new code, it's better to use newer patterns.

## F-strings 

In 3.6, Python introduced [formatted string literals](https://docs.python.org/3/reference/lexical_analysis.html#formatted-string-literals), usually called f-strings. Like the `format` method, f-strings use curly braces to identify placeholders. But they put the expression to be evaluated inside those braces:

```python
--8<-- "snippets/02-create-dynamic-text.py:f-string"
```

```text title="output"
--8<-- "output/02-create-dynamic-text.txt:f-string"
```

Relative to older methods, f-strings are easier to understand because the expressions are not separated from their position in the output string. For most dynamic text, you should use f-strings.

## Formatting values with f-strings

Because f-strings are often used for prettified user-facing output, raw values are often not a good choice. The code below, for example, is bad:

```python
--8<-- "snippets/02-create-dynamic-text.py:bad-formatting"
```

```text title="output"
--8<-- "output/02-create-dynamic-text.txt:bad-formatting"
```

You could use the `round` function, but that implies you care about the rounded value. You probably don't. You probably just need to represent the true value in a more user-friendly way. The appropriate way to do this is to use Python's [format specification language](https://docs.python.org/3/library/string.html#format-specification-mini-language).

```python
--8<-- "snippets/02-create-dynamic-text.py:precision-formatting"
```

1. > `.2f` means to represent the number with 2 digits to the right of the decimal point in fixed point form.

```text title="output"
--8<-- "output/02-create-dynamic-text.txt:precision-formatting"
```

The distinction between "here is a value" and "here is a representation of a value" is subtle, but meaningful. It's the difference between what the value _is_ and what the value _looks like_. Like how a feature class is different from the way a layer is styled in a map. 

Thousands separators are another common use case for format specification:

```python
--8<-- "snippets/02-create-dynamic-text.py:separator-formatting"
```

1. > `,.0f` means to represent the number with a thousands separator, 0 digits to the right of the decimal point in fixed point form.

```text title="output"
--8<-- "output/02-create-dynamic-text.txt:separator-formatting"
```

The third most common use case for format specification is aligning text to a specific width, which is useful for making text line up.

```python
--8<-- "snippets/02-create-dynamic-text.py:width-formatting"
```

1. > `.<18` means to align the text to the left of a cell at least 18 characters wide, padding any empty spaces with a `.` character. `.>10,` has a similar meaning, but aligned right to a cell at least 10 characters wide, using a thousands separator.


```text title="output"
--8<-- "output/02-create-dynamic-text.txt:width-formatting"
```


## The problem with f-strings

While f-strings are useful, you have to be very careful when you create an f-string with user-provided values. That can lead to security vulnerabilities, like SQL injection attacks. 

For example, let's say we have a database with some information that shouldn't be public. A logged-in user requests information that's private to them, and we have some code to fetch that information from the database.

```python
--8<-- "snippets/02-create-dynamic-text.py:sql-injection-def"
```

In normal situations, this code works as expected:

```python
--8<-- "snippets/02-create-dynamic-text.py:sql-injection-call-normal"
```

```text title="output"
--8<-- "output/02-create-dynamic-text.txt:sql-injection-call-normal"
```

This shows only Alice's secrets because the f-string evaluates to:

```sql
"SELECT secret FROM users WHERE name = 'Alice'"
```

A malicious user, however, could create a username that includes a SQL injection:

```python
--8<-- "snippets/02-create-dynamic-text.py:sql-injection-call-malicious"
```

```text title="output"
--8<-- "output/02-create-dynamic-text.txt:sql-injection-call-malicious"
```

This returns everybody's secrets because the f-string evaluates to:

```sql
"SELECT secret FROM users WHERE name = '' OR 1=1; -- '"
```

Since `#!sql 1=1` is always true, this code will show the secrets of everybody in the database (`#!sql --` starts a line comment to prevent the final `#!sql '` from causing a syntax error). 

SQL injections are a well-known attack vector, so there is a defined way to handle this problem: use parameterized queries, not f-strings:

```python
--8<-- "snippets/02-create-dynamic-text.py:parameterized-queries-def"
```

Calling with a normal input returns a normal value:
```python
--8<-- "snippets/02-create-dynamic-text.py:parameterized-queries-call-normal"
```

```text title="output"
--8<-- "output/02-create-dynamic-text.txt:parameterized-queries-call-normal"
```

SQL injection fails to return anything with parameterized queries:
```python
--8<-- "snippets/02-create-dynamic-text.py:parameterized-queries-call-malicious"
```

```text title="output"
--8<-- "output/02-create-dynamic-text.txt:parameterized-queries-call-malicious"
```

Unfortunately, parameterized queries have the same problem that old-fashioned string formatting had. They're difficult to reason about because the values are separated from their position in the string.

## T-strings

To help get the convenience of f-strings with the safety of parameterized queries, in 3.14 Python introduced [template string literals](https://docs.python.org/3/library/string.templatelib.html), also known as t-strings. Other than using a `t` prefix instead of an `f`, the syntax for creating t-strings is identical to f-strings.

But despite their name, t-strings are not actually strings. The object that gets created is a `Template` and it looks nothing like a `str`.


```python
--8<-- "snippets/02-create-dynamic-text.py:t-string"
```

```text title="output"
--8<-- "output/02-create-dynamic-text.txt:t-string"
```

Unlike f-strings, t-strings separate the static parts (the strings) from the dynamic parts (the interpolations). When you pass a t-string to a function, it's possible for the function to know which parts might be malicious and do something about them.


## The problem with t-strings

Sadly, t-strings are not magic. Just because they _make it possible_ to do something about the potentially malicious part of a dynamic string doesn't mean they _actually do it_. 

Somebody has to write what's called a tag function to process the t-string safely. It's not easy. Even just to print out a trivial `hello world` example is several lines of code:

```python
--8<-- "snippets/02-create-dynamic-text.py:tag-function"
```

1. > One block of code to handle to static parts of the t-string, which should be safe
1. > A separate block of code to handle to dynamic parts of the t-string, which could be malicious.

```text title="output"
--8<-- "output/02-create-dynamic-text.txt:tag-function"
```

Tag functions are not the sort of thing typical users would write. This is the kind of responsibility that is better borne by library authors than by people using the libraries.

Many libraries are still working on adding support for t-strings. SQLAlchemy 2.1 has already done that work, so we get the flexibility of f-strings without the SQL injection risk when we use that library:

```python
--8<-- "snippets/02-create-dynamic-text.py:t-string-in-library-def"
```

1. > Other than swapping out a `text` object for a `tstring`, the code is identical to the unsafe code that used f-strings. The library authors wrote the appropriate tag functions, so as users we get the advantages with very little extra work.

Normal queries work correctly:
```python
--8<-- "snippets/02-create-dynamic-text.py:t-string-in-library-call-normal"
```

```text title="output"
--8<-- "output/02-create-dynamic-text.txt:t-string-in-library-call-normal"
```

And SQL injections are automatically blocked:
```python
--8<-- "snippets/02-create-dynamic-text.py:t-string-in-library-call-malicious"
```

```text title="output"
--8<-- "output/02-create-dynamic-text.txt:t-string-in-library-call-malicious"
```

When library authors have finished the work of incorporating t-strings into their code, everybody will get the advantage of safety for free. That work is being completed unevenly, so you want to check for t-string compatibility with the libraries you use.