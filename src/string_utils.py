"""
@file     string_utils.py
@date     12/05/2023
@author   Julio Cabria
"""

import re
from colorama import Fore, Back, Style


def green(text):
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}"


def red(text):
    return f"{Fore.RED}{text}{Style.RESET_ALL}"


def yellow(text):
    return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"


def cyan(text):
    return f"{Fore.CYAN}{text}{Style.RESET_ALL}"


def grey_bkg(text):
    return f"{Back.LIGHTBLACK_EX}{text}{Style.RESET_ALL}"


def remove_string_literals(text):

    pattern = r'(\'[^\']*\'|\"[^\"]*\")'
    text = re.sub(pattern, '', text)

    triple_quote_index = text.find('"""')
    if triple_quote_index == -1:
        return text

    return text[:triple_quote_index]


def to_dict_inverted(list_of_tuples):

    dictionary = {}

    for key, value in list_of_tuples:

        if value in dictionary:
            dictionary[value] += ", " + key
            continue

        dictionary[value] = key

    return dictionary


def get_doctring(text):
    try:
        docstring = grab(text, start='"""', end='"""')
        return docstring
    except IndexError:
        return None


def table_str(filename, fun_table, documented_table):

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

    except OSError:
        return f"\nError: File '{filename}' not found.\n"

    printed = False
    text = ""
    for fun_name, fun_excs in fun_table.items():

        fun_excs = {exc_line: exc_name
                    for exc_line, exc_name
                    in to_dict_inverted(fun_excs).items()
                    if exc_name not in documented_table[fun_name]}

        if not fun_excs:
            continue

        text += f"\n{green(fun_name)}\n"

        for exc_line, exc_name in fun_excs.items():
            text += " "*2 + f"{yellow(exc_name)}\n"

            try:
                file_line = shortened(lines[exc_line-1].strip())

            except IndexError:
                file_line = "Could not load line preview."

            printed = True
            line_number = " "*2 + grey_bkg(str(exc_line).rjust(4))
            text += f"{line_number}  {file_line}\n"

    text += \
        cyan("""
To remove an exception from the report, enclose
the code inside a try/except block or add the
exception name to the function's docstring.
""")

    if not printed:
        text = "\n---- No uncaught exceptions ----\n"

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
                    if line.strip()
                    and not line.lstrip().startswith("#"))

    except StopIteration:
        raise IndexError("No nonempty lines found.")


def shortened(text, length=60):
    return text[:length-3] + "..." if len(text) > length else text
