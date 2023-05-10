#!/usr/bin/env python3

"""
@file     main.py
@date     06/05/2023
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

    table = {}

    function_exception_table(filename, table)
    print(table_str(filename, table))


if __name__ == "__main__":
    main()
