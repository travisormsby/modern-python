#!/usr/bin/env -S uv run --script
# /// script
# requires-python = "<=3.14"
# dependencies = [
#   "pandas==3"
# ]
# ///

import pandas
import sys

print(pandas.__version__)
print(sys.version)
print(sys.executable)
