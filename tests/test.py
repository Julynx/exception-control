"""
@file     test.py
@date     DD/MM/YYYY
@author   Julio Cabria
"""


def function0():
    raise TypeError("Hello \"world")


def function1(*, arg1: int, arg2: int) -> int:
    arg1 += 3

    if arg1 > 20:
        raise ValueError("arg1 is greater than 20")
    if arg1 > 40:
        raise Exception
    return 20 + arg2


def function2(*, arg1: int, arg2: int) -> int:

    try:
        res = arg1 / arg2
        raise ZeroDivisionError
    except Exception:
        res = 1
    except:
        res = 2
    return res


def main() -> int:
    """
    Main function
    """

    print("Hello world")
    print("Hello world")
    print("Hello world")

    l = [1, 2, 3, 4, 5]
    a = 3
    b = 0
    c = a / b
    try:
        c = l[10]
    except IndexError:
        print("IndexError")

    try:
        function0()
    except Exception:
        pass

    function1(arg1=1, arg2=2)
    raise Exception("This is an exception")


if __name__ == "__main__":
    main()
