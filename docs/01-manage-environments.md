# Manage environments

By far the worst part of working with Python is managing the environment where Python runs. If you're the audience for this workshop, you don't need me to retraumatize you with explanations about why this happens. You already know the pain.

Instead, let's celebrate that recently some new tooling has emerged that really does make this problem substantially better.

## `uv`

Astral is a software company that makes tooling for the Python ecosystem, including an environment management tool called `uv`. This tool immediately became a big hit because it significantly improved the process for managing environments, mostly by being orders of magnitude faster than other options.

Once you install `uv`, you can either use a `pyproject.toml` file to organize your project's dependencies, or use `uv` to automatically create temporary environments for scripts that use the [PEP 723 inline script metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/) format.

## `pixi` 

As great as `uv` is, there are two reasons you probably don't want to migrate everything to use it:

1. Astral was recently acquired by OpenAI and the company will be dissolved as part of that acquisition. The future of `uv` is uncertain, though Astral's leadership says they will continue to work on it.

2. You can only use `uv` to handle Python dependencies. Most geospatial Python projects will have important non-Python dependencies, notably `GDAL`.

For most geospatial work with Python, it is better to use a different tool called `pixi`. It uses `uv` under the hood, so it's just as fast to resolve pure Python dependencies. But it can also manage packages on `conda` channels, including non-Python dependencies.

While `pixi` doesn't support inline script metadata, it does support using `pyproject.toml` to manage dependencies.