# Manipulate filepaths

If you are working directly with files, you are going to want some kind of way to work with filepaths programatically.

## Older method

Originally, the way to treat paths was as strings. The standard library `os` module had several helper functions for manipulating paths, but ultimately they were all wrappers around string manipulation. For example, the `os.path.join` function was used to join parts of a path together:

```python
--8<-- "snippets/03-manipulate-filepaths.py:os-path-join"
```

```text title="output"
--8<-- "output/03-manipulate-filepaths.txt:os-path-join"
```

For consistency, if you have existing scripts that use the `os` module to manipulate paths, continue using it as you maintain those scripts. 

But treating filepaths as strings has some disadvantages - notably that the required string methods to manipulate those paths can be convoluted and hard to reason about. For example, if you want to create file path that is identical to an existing path, but with a different file extension, you need to do something like:

```python
--8<-- "snippets/03-manipulate-filepaths.py:os-path-split"
```

```text title="output"
--8<-- "output/03-manipulate-filepaths.txt:os-path-split"
```

So for new scripts, it is better to avoid treating file paths as strings.

## `Path` objects

The modern way to work with filepaths is [`pathlib`](https://docs.python.org/3/library/pathlib.html). Unlike the older method, `pathlib` treats paths as specific `Path` objects, not as generic strings. One advantage of this structure is that you can concatenate parts of the path using the `/` operator instead of a more convoluted call to `os.path.join`:

```python
--8<-- "snippets/03-manipulate-filepaths.py:pathlib"
```

```text title="output"
--8<-- "output/03-manipulate-filepaths.txt:pathlib"
```

While a `Path` object has a string representation that you see when you print it out, it is not a string. It is a more complex objects that, among other things, is aware of the operating system where it was created. When you use `Path`, it automatically creates for you the correct `PosixPath` objects for Linux/Unix/BSD/MacOS and `WindowsPath` objects for Windows. This means `Path` objects work cross-platform by default.

```python
--8<-- "snippets/03-manipulate-filepaths.py:path-type"
```

```text title="output"
--8<-- "output/03-manipulate-filepaths.txt:path-type"
```

## Path manipulation methods

`Path` objects have methods and properties with semantics that make the purpose more obvious. This is better than using generic string methods that need comments or documentation to explain. These come in two categories:

- [Pure path](https://docs.python.org/3/library/pathlib.html#pure-paths) methods and properties operate abstractly on the path, and don't need to check the actual file system for anything.
- [Concrete path](https://docs.python.org/3/library/pathlib.html#concrete-paths) methods and properties need to interact with the file system.

This distinction matters because only pure path methods and properties are totally predictable when run on different machines. Concrete methods and properties, on the other hand, depends on the actual file system on the machine where the script is run. 

Exercise care when working with concrete path methods and properties, because they leave you open to the dreaded "it worked on my machine" problem. For example, Windows filepaths aren't case sensitive, and MacOS filepaths are. So code that worked on your Windows machine may fail if run on a Mac.

It's possible to directly create `PurePath`, `PurePosixPath`, and `PureWindowsPath` objects that only have pure methods and properties. But generally you will want to stick with `Path` objects that have both kinds.

### Example pure path manipulation

The `parent` method returns a `Path` object for the parent directory of the `Path`.

```python
--8<-- "snippets/03-manipulate-filepaths.py:parent"
```

```text title="output"
--8<-- "output/03-manipulate-filepaths.txt:parent"
```

The `name` method will return the final path component, including the extension. The `stem` method returns the name without the extension, `suffix` returns just the extension (including the `.`), and `with_suffix` lets you swap a new extension:

```python
--8<-- "snippets/03-manipulate-filepaths.py:name"
```

```text title="output"
--8<-- "output/03-manipulate-filepaths.txt:name"
```

### Example concrete path manipulation

The `absolute` method returns the absolute path for a given relative path:

```python
--8<-- "snippets/03-manipulate-filepaths.py:absolute"
```

```text title="output"
--8<-- "output/03-manipulate-filepaths.txt:absolute"
```

The `exists`, `is_file` and `is_dir` methods give you information about the path:

```python
--8<-- "snippets/03-manipulate-filepaths.py:exists"
```
```text title="output"
--8<-- "output/03-manipulate-filepaths.txt:exists"
```

The `iterdir` method lets you iterate over the contents of a directory, returned in arbitrary order:

```python
--8<-- "snippets/03-manipulate-filepaths.py:iterdir"
```

```text title="output"
--8<-- "output/03-manipulate-filepaths.txt:iterdir"
```

The `glob` method lets you search for all the files that match a particular pattern.

```python
--8<-- "snippets/03-manipulate-filepaths.py:glob"
```

```text title="output"
--8<-- "output/03-manipulate-filepaths.txt:glob"
```



## Using `Path` objects as inputs

Most operations that work on file path strings will accept `Path` objects:

```python
--8<-- "snippets/03-manipulate-filepaths.py:path-input"
```

```text title="output"
--8<-- "output/03-manipulate-filepaths.txt:path-input"
```

But `Path` objects are not substitutes for file path strings everywhere. For example, the `json` module cannot serialize `Path` objects the way it can file path strings:

```python
--8<-- "snippets/03-manipulate-filepaths.py:path-input-fail"
```

```python title="output"
--8<-- "output/03-manipulate-filepaths.txt:path-input-fail"
```

If a `Path` object doesn't work, you may need to cast it to a string first:

```python
--8<-- "snippets/03-manipulate-filepaths.py:str-input"
```

```python title="output"
--8<-- "output/03-manipulate-filepaths.txt:str-input"
```


## Reading and writing files

Because you can usually use a `Path` object instead of a filepath string, you could pass it to the `open` function if you want to read or write data:

```python
--8<-- "snippets/03-manipulate-filepaths.py:open"
```

```text title="output"
--8<-- "output/03-manipulate-filepaths.txt:open"
```

But for small and medium sized files, there's a better way. `Path` objects have `read_text`, `write_text`, `read_bytes` and `write_bytes` methods that access the contents of files directly. It still uses the context manager behind the scenes, files are closed safely, but the more straightforward code makes it easier to understand what is happening.

```python
--8<-- "snippets/03-manipulate-filepaths.py:write-read"
```

```text title="output"
--8<-- "output/03-manipulate-filepaths.txt:write-read"
```

One caveat for the `read_text` and `read_bytes` methods is that they read the entire file into memory at once. For large files, that could potentially cause memory pressure on the system. In those cases, it would be better to read the file in chunks using the built-in `open` function. 


