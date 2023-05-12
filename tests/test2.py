import sys


def test_fun():
    """
    Raises:
        : Thi
    """
    raise ValueError


def main() -> int:  # fun_idx = 3
    """
    Main function
    """

    print("Hello world")
    print("Hello world")
    print("Hello world")

    test_fun()

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
