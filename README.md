# Python Debugging Toolkit

A lightweight debugging tool for Python scripts — no external dependencies required.

## Features
- Line-by-line execution tracing
- Display local variables at each line
- Show called functions and their return values
- Display exceptions at the moment they occur
- Log errors to JSON format (with precise crash location info)
- Inspect variables at the moment of crash with `--inspect`

## Project Structure
```
debugging/
├── main.py                  ← Entry point
├── debugger/
│   ├── cli.py               ← Command-line interface
│   ├── tracer.py            ← Execution tracing via sys.settrace
│   ├── logger.py            ← Log errors to JSON
│   └── inspector.py         ← Inspect frame variables
├── examples/
│   ├── buggy_program.py     ← Example: program with ZeroDivisionError
│   └── test.py              ← Example: direct tracer test
├── tests/
│   └── test_all.py          ← Full unit tests
└── logs/
    └── errors.json          ← Stored error logs
```

## Usage
```bash
# Simple run
python main.py examples/buggy_program.py

# With line-by-line trace
python main.py examples/buggy_program.py --trace

# With variable display
python main.py examples/buggy_program.py --trace --vars

# With variable inspection at crash
python main.py examples/buggy_program.py --inspect
```

## Running Tests
```bash
python -m pytest tests/ -v
# or
python tests/test_all.py
```