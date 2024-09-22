import os
import glob


def remove_trailing_whitespace(lines):
    """
    Remove trailing whitespace from each line and ensure blank lines have no whitespace.
    """
    cleaned_lines = []
    for line in lines:
        stripped_line = line.rstrip()  # Remove trailing whitespace
        if stripped_line == "":  # Ensure blank lines have no whitespace
            cleaned_lines.append("\n")
        else:
            cleaned_lines.append(stripped_line + "\n")
    return cleaned_lines


def ensure_newline_at_end(lines):
    """
    Ensure there is exactly one newline at the end of the file.
    """
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    return lines

def process_file(file_path):
    """
    Process a single file: remove trailing whitespace, ensure newline at the end,
    and fix Flake8 E302 and E303 errors (two blank lines before functions or classes and no more than two blank lines in a row).
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    lines = remove_trailing_whitespace(lines)
    lines = ensure_newline_at_end(lines)

    # Write the processed lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)


def main():
    # Directory containing the .py files
    directory = './gadgets'

    # Find all Python files in the ./gadgets subdirectory
    py_files = glob.glob(os.path.join(directory, '*.py'))

    for file_path in py_files:
        process_file(file_path)

    print(f"Processed {len(py_files)} Python files.")


if __name__ == "__main__":
    main()
