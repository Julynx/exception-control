"""
@file     functions.py
@date     10/05/2023
@author   Julio Cabria
"""

import re


def function_excs(line):

    excs = []

    if re.search(r'[(\s]open\(', line):
        excs.append("FileNotFoundError")
        excs.append("PermissionError")

    if re.search(r'[(\s]int\(', line):
        excs.append("ValueError")

    if re.search(r'[(\s]float\(', line):
        excs.append("ValueError")

    return excs
