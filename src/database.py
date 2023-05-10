"""
@file     database.py
@date     06/05/2023
@author   Julio Cabria
"""

BUILTIN_FUNCTIONS = {
    'open(': ['FileNotFoundError', 'PermissionError'],
    'int(': ['ValueError'],
    'float(': ['ValueError'],
}

EXCEPTION_GROUPS = {
    'BaseExceptionGroup': 'BaseException',
    'GeneratorExit': 'BaseException',
    'KeyboardInterrupt': 'BaseException',
    'SystemExit': 'BaseException',
    'Exception': 'BaseException',
    'ArithmeticError': 'Exception',
    'AssertionError': 'Exception',
    'AttributeError': 'Exception',
    'BufferError': 'Exception',
    'EOFError': 'Exception',
    'ExceptionGroup': 'Exception',
    'ImportError': 'Exception',
    'LookupError': 'Exception',
    'MemoryError': 'Exception',
    'NameError': 'Exception',
    'OSError': 'Exception',
    'ReferenceError': 'Exception',
    'RuntimeError': 'Exception',
    'StopAsyncIteration': 'Exception',
    'StopIteration': 'Exception',
    'SyntaxError': 'Exception',
    'SystemError': 'Exception',
    'TypeError': 'Exception',
    'ValueError': 'Exception',
    'Warning': 'Exception',
    'FloatingPointError': 'ArithmeticError',
    'OverflowError': 'ArithmeticError',
    'ZeroDivisionError': 'ArithmeticError',
    'ModuleNotFoundError': 'ImportError',
    'IndexError': 'LookupError',
    'KeyError': 'LookupError',
    'UnboundLocalError': 'NameError',
    'BlockingIOError': 'OSError',
    'ChildProcessError': 'OSError',
    'ConnectionError': 'OSError',
    'FileExistsError': 'OSError',
    'FileNotFoundError': 'OSError',
    'InterruptedError': 'OSError',
    'IsADirectoryError': 'OSError',
    'NotADirectoryError': 'OSError',
    'PermissionError': 'OSError',
    'ProcessLookupError': 'OSError',
    'TimeoutError': 'OSError',
    'BrokenPipeError': 'ConnectionError',
    'ConnectionAbortedError': 'ConnectionError',
    'ConnectionRefusedError': 'ConnectionError',
    'ConnectionResetError': 'ConnectionError',
    'NotImplementedError': 'RuntimeError',
    'RecursionError': 'RuntimeError',
    'IndentationError': 'SyntaxError',
    'TabError': 'IndentationError',
    'UnicodeError': 'ValueError',
    'UnicodeDecodeError': 'UnicodeError',
    'UnicodeEncodeError': 'UnicodeError',
    'UnicodeTranslateError': 'UnicodeError',
    'BytesWarning': 'Warning',
    'DeprecationWarning': 'Warning',
    'EncodingWarning': 'Warning',
    'FutureWarning': 'Warning',
    'ImportWarning': 'Warning',
    'PendingDeprecationWarning': 'Warning',
    'ResourceWarning': 'Warning',
    'RuntimeWarning': 'Warning',
    'SyntaxWarning': 'Warning',
    'UnicodeWarning': 'Warning',
    'UserWarning': 'Warning'
}


def expand_groups(groups):

    def _expand_group(group):
        exceptions = [group]
        for exc, exc_group in EXCEPTION_GROUPS.items():

            if exc_group != group:
                continue
            exceptions.append(exc)

            if exc not in EXCEPTION_GROUPS.values():
                continue
            exceptions.extend(_expand_group(exc))

        return exceptions

    return {exc
            for group
            in groups
            for exc
            in _expand_group(group)}


def exception_list():
    return EXCEPTION_GROUPS.keys()
