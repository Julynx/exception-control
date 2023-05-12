"""
@file     exceptions.py
@date     06/05/2023
@author   Julio Cabria
"""

from code_parsing import Functions
from code_parsing import TryExceptBlocks
from string_utils import grab
from string_utils import get_doctring
from string_utils import remove_string_literals
from database import expand_groups
from database import exception_list
from operators import operator_excs
from functions import function_excs


def documented_exceptions(docstring):
    """
    Returns the exceptions documented in the docstring.

    Args:
        docstring (str):     Docstring of the function.

    Returns:
        list:   Exceptions documented in the docstring, expanded to
                include the exceptions in the groups they belong to.
    """
    if docstring is None:
        return set()

    return expand_groups({exc
                          for exc
                          in exception_list()
                          if exc in docstring})


def not_handled(raised, caught):
    """
    Returns the exceptions not handled by the try-except blocks.
    Reads EXCEPTION_GROUPS from database.py

    Args:
        raised (dict):  Exceptions raised in the text.
                            dict[exception_name]=line_idx
        caught (dict):  Exceptions caught in the text.
                            dict[exception_name]=line_idx

    Returns:
        dict:   Exceptions not handled by the try-except blocks.
                    dict[exception_name]=line_idx
                An exception is considered handled if it is in 'caught'
                or if a group it belongs to is in 'caught'.
    """
    try:
        handled = expand_groups(caught.keys())

    except KeyError:
        handled = set()

    return {exc: line_idx
            for exc, line_idx
            in raised.items()
            if exc not in handled}


def raised_exceptions(text, fun_dict=None):
    """
    Returns the exceptions raised in the text.

    Args:
        text (str): Phython code as a string.
        fun_dict (dict): Dictionary of functions.
            fun_dict[fun_name] = {exception_name: line_idx, ...}

    Returns:
        dict: Exceptions raised in the text.
              dict[exception_name]=line_idx
    """
    fun_dict = fun_dict or {}
    excs = {}

    for line_idx, line in enumerate(text.split("\n")):

        if line.lstrip().startswith("#"):
            continue

        line = f"{line}\n"
        clean_line = remove_string_literals(line)

        # Implicit exceptions (python built-in functions)
        excs.update({exc: line_idx
                     for exc
                     in function_excs(clean_line)})

        # Implicit exceptions (python built-in operators
        excs.update({exc: line_idx
                     for exc
                     in operator_excs(clean_line)})

        # Implicit exceptions (user-defined functions)
        excs.update({exc: line_idx
                     for funct_call
                     in (fun_excs
                         for fun_name, fun_excs
                         in fun_dict.items()
                         if f"{fun_name}(" in clean_line
                         and f"def {fun_name}" not in clean_line)
                     for exc, _
                     in funct_call})

        # Explicit exceptions (manually raised)
        try:
            exception = grab(clean_line, start="raise ", end="\n").strip()
        except IndexError:
            continue

        exception_name = exception.split("(", maxsplit=1)[0]
        exception_name = exception_name.split("#", maxsplit=1)[0]
        excs[exception_name] = line_idx

    return excs


def caught_exceptions(text):
    """
    Returns the exceptions caught in the text.

    Args:
        text (str): Phython code as a string.

    Returns:
        dict: Exceptions caught in the text.
              dict[exception_name]=line_idx
    """
    excs = {}

    for line_idx, line in enumerate(text.split("\n")):

        if line.lstrip().startswith("#"):
            continue

        try:
            exception = grab(line, start="except ", end=":").strip()
            if exception.strip() == "":
                exception = "unnamed exception"

        except IndexError:
            continue

        excs[exception] = line_idx

    return excs


def function_exception_table(filename):

    def _search_outside(fun_idx,
                        fun_body,
                        fun_dict,
                        try_except_boundaries):

        excs_in_body = {exc: fun_idx+line_idx+1
                        for exc, line_idx
                        in raised_exceptions(fun_body, fun_dict).items()}

        for start, end in try_except_boundaries:
            excs_in_body = {exc: line
                            for exc, line
                            in excs_in_body.items()
                            if line not in range(start, end)}

        return excs_in_body

    def _search_inside(fun_idx, fun_body, fun_dict):

        excs_to_return = {}
        try_except_boundaries = []

        for try_idx, try_body in TryExceptBlocks(fun_body):
            start_line = try_idx + fun_idx + 1
            end_line = try_idx + fun_idx + len(try_body.strip().split('\n'))

            try_except_boundaries.append((start_line, end_line))

            excs_inside = {exc: start_line+line_idx
                           for exc, line_idx
                           in not_handled(
                               raised_exceptions(try_body, fun_dict),
                               caught_exceptions(try_body)).items()}

            excs_to_return.update(excs_inside)

        return try_except_boundaries, excs_to_return

# def function_exception_table(filename, fun_dict):

    fun_dict = {}
    documented_dict = {}

    for fun_idx, fun_name, fun_body in Functions(filename):

        # Undocumented exceptions
        excs_for_fun = {}

        try_except_boundaries, inside_excs = _search_inside(fun_idx,
                                                            fun_body,
                                                            fun_dict)
        excs_for_fun.update(inside_excs)

        outside_excs = _search_outside(fun_idx,
                                       fun_body,
                                       fun_dict,
                                       try_except_boundaries)
        excs_for_fun.update(outside_excs)

        fun_dict[fun_name] = sorted(excs_for_fun.items(),
                                    key=lambda x: x[1])

        # Documented exceptions
        docstring_text = get_doctring(fun_body)
        documented_dict[fun_name] = documented_exceptions(docstring_text)

    return fun_dict, documented_dict
