# Manage environments

By far the worst part of working with Python is managing the environment where Python runs. If you're the audience for this workshop, you don't need me to retraumatize you with explanations about why this happens. You already know the pain.

Instead, let's celebrate that recently some new tooling has emerged that really does make this problem substantially better.

## `uv`

Astral is a software company that makes tooling for the Python ecosystem. When they released `uv` a couple years ago, it immediately became a big hit because it significantly improved the process for managing environments.

Once you install `uv`, you can either use a `pyproject.toml` file to organize your project's dependencies, or use `uv` to automatically create temporary environments for scripts that use the PEP 723 inline script metadata format.

## `pixi` 

The downside of`uv` is that it really only works for Python dependencies. Most geospatial Python projects will have important non-Python dependencies, notably `GDAL`. These dependencies are quite difficult to manage, and `uv` can't help with that. This is why historically, many geospatial professionals turned to `conda`, since it can handle Python and non-Python dependencies. 

With `pixi`, you get the best of both. It uses `uv` under the hood to handle Python dependencies. And it can access pre-built binaries on `conda` channels to manage non-Python dependencies as well.

Sadly, `pixi` doesn't support inline script metadata, but it does support using `pyproject.toml` for dependencies.