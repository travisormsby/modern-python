import sys


def run_with_comments(filename):
    with open(filename, "r") as f:
        modified_lines = []
        for line in f:
            # We only look for lines where the first non-whitespace is '#'
            if line.startswith("#"):
                modified_lines.append(f'print(r"""{line}""")\n')
            else:
                # Keep code lines exactly as they are
                modified_lines.append(line)

        # Execute the modified code string
        exec("".join(modified_lines), {"__name__": "__main__"})


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_with_comments(sys.argv[1])
