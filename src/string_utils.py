"""
@file     string_utils.py
@date     06/05/2023
@author   Julio Cabria
"""


def get_doctring(text):
    try:
        docstring = grab(text, start='"""', end='"""')
        return docstring
    except IndexError:
        return None


def table_str(fun_table):

    if all(not value for value in fun_table.values()):
        return "\n---- No uncaught exceptions ----\n"

    text = "\n---- Uncaught exceptions ----\n"
    for fun_name, fun_excs in fun_table.items():

        if not fun_excs:
            continue

        text += f"\n{fun_name}:\n"

        for exc_name, exc_line in fun_excs:
            text += " "*4 + f"- Line {exc_line}: {exc_name}\n"

    return text


def grab(text: str, *, start, end):
    """
    Returns text between two start and end delimiters.

    Args:
        text (str): Text to search.
        start (str): Start delimiter.
        end (str): End delimiter.

    Returns:
        str: Text between start and end delimiters.

    Raises:
        IndexError: If start or end delimiter is not found.
    """
    start_index = text.find(start)
    if start_index == -1:
        raise IndexError(f"'{start}' string not present in '{text}'.")

    end_index = text.find(end, start_index + len(start))
    if end_index == -1:
        raise IndexError(f"'{end}' string not present in '{text}'.")

    return text[start_index + len(start):end_index]


def line_indentation(line):
    """
    Returns the number of spaces at the beginning of a line.

    Args:
        line (str): Line of text.

    Returns:
        int: Number of spaces at the beginning of the line.
    """
    return len(line) - len(line.lstrip())


def index_in_list(string, lst):
    """
    Returns the index of a string in a list.

    Args:
        string (str): String to search for.
        lst (list): List of strings.

    Returns:
        int: Index of the string in the list.

    Raises:
        IndexError: If string is not found in list.
    """
    try:
        return next(idx
                    for idx, line
                    in enumerate(lst)
                    if string.strip() in line.strip())

    except StopIteration:
        raise IndexError(f"'{string}' not found in list.")


def first_nonempty_line(text_lines, start=0):
    """
    Returns the text of the first nonempty line in a list of lines.

    Args:
        text_lines (list): List of lines.

    Returns:
        int: Index of the first nonempty line.

    Raises:
        IndexError: If no nonempty lines are found.
    """
    try:
        return next(line
                    for line
                    in text_lines[start:]
                    if line.strip())

    except StopIteration:
        raise IndexError("No nonempty lines found.")