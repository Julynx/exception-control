"""
@file     code_parsing.py
@date     06/05/2023
@author   Julio Cabria
"""


from string_utils import grab
from string_utils import line_indentation
from string_utils import index_in_list
from string_utils import first_nonempty_line


def cut_function_body(text_lines):
    """
    Receives a list of text lines of a function with a given indentation.
    It detects the end of the function body by looking for the first line
    with a lower indentation than the given one and crops out the rest.

    Args:
        text_lines (list): List of text lines of a function.

    Returns:
        list: List of text lines of the function body.
    """
    indentation = line_indentation(first_nonempty_line(text_lines))
    f_body = []

    for line in text_lines:

        if (line.strip()
            and line_indentation(line) < indentation
                and not line.strip().startswith("except")):
            break

        f_body.append(line.rstrip())

    return f_body


class Functions:

    text_lines = ""
    from_idx = 0

    def __init__(self, filename):
        with open(filename, "r") as file:
            self.text_lines = file.readlines()

    def __iter__(self):
        return self

    def __next__(self):

        try:
            text_lines = self.text_lines[self.from_idx:]

            start = "def "
            end = ":"
            text = "\n".join(text_lines)

            declaration = (start
                           + grab(text, start=start, end=end)
                           + end).strip()

            first_idx = index_in_list(declaration, text_lines) + 1

            body = cut_function_body(text_lines[first_idx:])

            function_name = grab(declaration,
                                 start=start,
                                 end="(")

            processed_lines = (index_in_list(start, text_lines)
                               + len(declaration.split("\n"))
                               + len(body)
                               + 1)

            self.from_idx += processed_lines - 1
            line_number = self.from_idx - len(body)

            body = "\n".join(body)

            return line_number, function_name, body

        except IndexError:
            raise StopIteration


class TryExceptBlocks:

    text_lines = ""
    from_idx = 0

    def __init__(self, body_text):
        self.text_lines = body_text.split("\n")

    def __iter__(self):
        return self

    def __next__(self):

        try:
            text_lines = self.text_lines[self.from_idx:]

            first_idx = index_in_list("try:", text_lines) + 1

            body = cut_function_body(text_lines[first_idx:])

            processed_lines = first_idx + len(body)

            self.from_idx += processed_lines
            line_number = self.from_idx - len(body) - 1

            body = text_lines[first_idx-1] + "\n" + "\n".join(body)

            return line_number, body

        except IndexError:
            raise StopIteration
