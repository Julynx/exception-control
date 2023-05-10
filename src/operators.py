"""
@file     operators.py
@date     06/05/2023
@author   Julio Cabria
"""

import re


def operator_excs(line):

    excs = []

    if re.search(r'//?', line):
        excs.append("ZeroDivisionError")

    if re.search(r'\b\w+\[', line):
        excs.append("IndexError")

    return excs
