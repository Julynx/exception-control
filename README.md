# exception-control
*Performs limited static analysis for uncaught exceptions in a Python file.*

This is a ⚠️WIP⚠️. Check out 
[tested behavior](#tested-behavior),
[untested behavior](#untested-behavior)
and 
[limitations](#limitations).


<br>
<br>
<p align="center">  
  <img width="600" src="https://i.imgur.com/l27TRKi.png">
</p>
<br>

## Usage
To check for uncaught exceptions in a Python file:
```
python3 main.py [filename]
```
Multiple files support is limited, but you can try this:
```
python3 main.py <(cat [file1] [file2]...)
```

## Tested behavior
The following behavior has been verified for the included test files [tests/test.py](https://github.com/Julynx/exception-control/blob/main/tests/test.py) and [tests/test2.py](https://github.com/Julynx/exception-control/blob/main/tests/test2.py):
- Detects exceptions manually raised by functions (```raise Exception```).
- Detects exceptions raised by calling functions outside try-except blocks.
- Detects exceptions raised by using operators like indexing ```arr[index]``` and dividing ```a / b or a // b```.
- Excludes exceptions caught in ```except Exception:``` clauses from the report and understands the [Exception Hierarchy](https://docs.python.org/3/library/exceptions.html#exception-hierarchy).
- Excludes exceptions documented in [function docstrings](https://peps.python.org/pep-0257/) from the report.

## Untested behavior
- May fail with nested try/except blocks.
- More extensive testing needs to be done to detect additional [limitations](#limitations).

## Limitations
- Will miss a lot of exceptions:
  - Due to Python being a dynamic language with duck typing, there are many exceptions that cannot be detected statically.
  - The exceptions raised by most popular functions are undocumented and therefore not visible from the outside.
  - Exceptions are stored by name. If there are multiple ```TypeError``` in a function, only the last one will be reported.
- Will report all exceptions even if they will never be raised in execution:
  - Due to it being a static analysis tool, it does not follow a variable along the code or determine its possible values.
  - That is why, exceptions will be reported for any indexing or division operations regardless if they are "safe" or not.
- Does not work well with classes or custom exceptions:
  - There can be many classes in a single document with methods in different classes sharing the same name.
  - There are many ways to instantiate a class and call its methods.
  - It is, in some cases, impossible to determine the class of a variable and the function called using static analysis.
- Does not support external libraries:
  - External libraries are unsupported, but the code is extensible enough to make it possible to include them in the future.
- Support for multiple files is limited:
  - Support for multiple files is done through [Bash Process Substitution](https://tldp.org/LDP/abs/html/process-sub.html). ```python3 main.py <(cat [file1] [file2]...)```
  - Line numbers will be relative to the merged files and not per file.
  - Functions are searched by name, so renamed functions ```from <module> import <function> as <new_name>``` will not be detected.
