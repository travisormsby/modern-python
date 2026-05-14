# Manage environments

By far the worst part of working with Python is managing the environment where Python runs. If you're the audience for this workshop, you don't need me to retraumatize you with explanations about why this happens. You already know the pain.

Instead, let's celebrate that recently some new tooling has emerged that really does make this problem substantially better.

## pyproject.toml

To save a record of your environment, you might be used to doing something like `pip freeze > requirements.txt` or `conda env export > environment.yml`. In theory, somebody else can create a copy of your environment from these files.

Sadly, that theory often doesn't work in practice. For anything that needs more than a handful of explicit dependencies, it is probably best to instead use a [pyproject.toml file](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/). This is the modern standard for tracking dependencies, and is integrated with other recently developed tools.

For our purposes, the most important part of the file is the \[project\] table. Here is that table for this workshop's pyproject.toml file:

```python
--8<-- "pyproject.toml:project"
```

These are not the only supported keys, but they're the ones the \[project\] table is going to need at minimum:

- The `name` and `version` keys are required by the pyproject.toml standard.
- The `requires-python` key tells people which versions of Python this project is compatible with.
- The `dependencies` key is a list of this project's dependencies.
   
    Most of the time, your dependencies will just need to specify name and version range, such as `pandas` needing at least version 3.0.1 and less than version 4. But you can also use [dependency specifiers](https://packaging.python.org/en/latest/specifications/dependency-specifiers/#dependency-specifiers) to provide additional information. In this example, the `pywin32` dependency is only installed on Windows systems. This means you can have a single pyproject.toml file that works for everybody.

    The dependencies listed here are the ones that your project actually cares about. But for creating reproducible environments, you also need to install the dependencies of those dependencies. And the dependencies of _those_ dependencies. And so on.
    
    For that, you need a lock file. A lock file specifies everything your environment needs, whether you rely on it directly or not. Lock files are human-readable, but they are long and complicated, so you definitely don't want to make one manually. Instead, you add explicit dependencies to pyproject.toml and then rely on some other tool, like `uv` or `pixi`, to automatically create a lock file.

## PEP 723 inline script metadata

For projects that don't require many dependencies, a pyproject.toml file is overkill. Instead, the [PEP 723 inline script metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/) format makes possible to define Python dependencies right at the top of the .py file itself.



## `uv`

Astral is a software company that makes tooling for the Python ecosystem, including an environment management tool called `uv`. This tool immediately became a big hit because it significantly improved the process for managing environments, mostly by being orders of magnitude faster than other options.

Once you install `uv`, you can either use a `pyproject.toml` file or inline script metadata to create environments for scripts.

## `pixi` 

As great as `uv` is, there are two reasons you probably don't want to migrate everything to use it:

1. Astral was recently acquired by OpenAI and will be dissolved as part of that acquisition. The future of `uv` is uncertain, though Astral's leadership says they will continue to work on it.

2. You can only use `uv` to handle Python dependencies. Most geospatial Python projects will have important non-Python dependencies, notably `GDAL`.

For any work that requires non-Python dependencies, it is better to use a different tool called `pixi`. It's just as fast to resolve pure Python dependencies because it can use `uv` under the hood. But it can also manage packages on `conda` channels, including non-Python dependencies.

While `pixi` doesn't currently support inline script metadata, it does support using pyproject.toml to manage dependencies.

## Exercise 1

1. Install `pixi` using the <a href="https://pixi.prefix.dev/latest/installation/" target="_blank" rel="noopener noreferrer">instructions in their documentation</a> :lucide-external-link:.

1. In the terminal, navigate to the directory where you extracted the materials for this workshop.

    ```shell
    cd "<path to materials>"
    ```

1. Run this command to create a new project called `modern-python` with a pyproject.toml file:

    ```shell
    pixi init modern-python --format pyproject
    ```

    If you leave off the `--format pyproject` argument, `pixi` will create a project using its default pixi.toml format. This format works great if you only need to share with other `pixi` users. But to make the project more broadly usable, create it using the pyproject format.

1.  
