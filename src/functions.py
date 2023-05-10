"""
@file     functions.py
@date     10/05/2023
@author   Julio Cabria
"""

from database import BUILTIN_FUNCTIONS


def function_excs(line):

    excs = []

    for func_call, func_excs in BUILTIN_FUNCTIONS.items():

        if func_call not in line:
            continue

        excs.extend(func_excs)

    return excs
