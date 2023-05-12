#!/usr/bin/env python3

"""
@file     main.py
@date     12/05/2023
@author   Julio Cabria
"""

import sys
from exceptions import function_exception_table
from string_utils import table_str


def main():

    try:
        filename = sys.argv[1]

    except IndexError:
        print("Usage: python3 main.py <filename>")
        sys.exit(1)

    try:
        table, documented = function_exception_table(filename)
        table_txt = table_str(filename, table, documented)

    except OSError:
        table_txt = f"\nFile '{filename}' not found.\n"

    print(table_txt)


if __name__ == "__main__":
    main()
