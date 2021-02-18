# Performance evaluation for Python functions

This package is supposed to provide decorator function which you can use
to easily measure the performance of Python functions.

## Installation
```
pip install evaltools
```

## Features
Version 0.0:
- Runtime measurement
- FLOP measurement (if supported by kernel)

## Usage
You can find some examples on how to use this library in *examples.py*. 

Minimal working example:
```Python
# mwe.py
from evaltools.utils import runtime


@runtime(show=True)
def loop(n):
    a = 0
    for i in range(n):
        a += 1

        
if __name__ == "__main__":
    log_time = {}
    loop(n=1000, log_time=log_time)

    print(log_time)
```
Output:
```commandline
>>> python mwe.py
loop	RUNTIME: 0.04 ms
{'loop': 0.03600120544433594}
```

## Contribution
Feel free to contribute any performance evaluation features you find useful. Simply develop on a 
new feature branch and merge it into the master via a PR.
