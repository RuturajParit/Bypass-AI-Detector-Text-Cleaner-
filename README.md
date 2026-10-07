# Unicode Text Cleaner

A lightweight Python utility for detecting and removing invisible
zero-width Unicode characters from text files.

## Features

- Removes Zero Width Space (`U+200B`)
- Removes Zero Width Non-Joiner (`U+200C`)
- Removes Zero Width Joiner (`U+200D`)
- Removes Zero Width No-Break Space (`U+FEFF`)
- Preserves normal text
- Reports how many hidden characters were removed
- Uses only the Python standard library

## Requirements

Python 3.9 or newer. No external packages are required.

## Usage

Put your text in:

```text
examples/assignment.txt
```

Run:

```bash
python src/cleaner.py
```

The cleaned file is saved to:

```text
output/clean_assignment.txt
```

## License

