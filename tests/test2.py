import sys


def main() -> int:  # fun_idx = 3
    """
    Main function
    """

    print("Hello world")
    print("Hello world")
    print("Hello world")

    try:  # try_idx = 9
        raise ValueError  # exc_idx = 1
    except Exception:
        pass

    print("Hello world")
    print("Hello world")
    print("Hello world")

    if sys.argv[1] == "1":
        raise Exception("This is an exception")

    try:  # try_idx = 21
        raise IndexError  # exc_idx = 1
    except Exception:
        pass


if __name__ == "__main__":
    main()
