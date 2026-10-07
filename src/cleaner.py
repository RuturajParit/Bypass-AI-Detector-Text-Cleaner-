"""
Text Cleaner

Removes invisible/zero-width Unicode characters from text files.
"""

from pathlib import Path

ZERO_WIDTH_CHARS = {
    "\u200b",  
    "\u200c",  
    "\u200d",  
    "\ufeff",  
}


def clean_text(text: str) -> tuple[str, int]:
    """Remove zero-width Unicode characters from text."""
    cleaned = "".join(
        character for character in text
        if character not in ZERO_WIDTH_CHARS
    )
    return cleaned, len(text) - len(cleaned)


def clean_file(input_file: Path, output_file: Path) -> int:
    """Clean a text file and save the result."""
    text = input_file.read_text(encoding="utf-8")
    cleaned_text, removed = clean_text(text)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(cleaned_text, encoding="utf-8")

    return removed


def main() -> None:
    input_file = Path("examples/assignment.txt")
    output_file = Path("output/clean_assignment.txt")

    if not input_file.exists():
        print(f"File not found: {input_file}")
        return

    removed = clean_file(input_file, output_file)

    print("Cleaning complete!")
    print(f"Hidden Unicode characters removed: {removed}")
    print(f"Output file: {output_file}")


if __name__ == "__main__":
    main()
