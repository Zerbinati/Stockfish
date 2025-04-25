# prepare_book_log_generic.py
import os
import sys

INPUT_LOG = "book_usage.log"
import os
import sys

INPUT_LOG = "book_usage.log"
OUTPUT_LOG = "book_usage_ready.log"

# Set how many lines represent one game (usually the opening)
LINES_PER_GAME = 10

def prepare_log(result):
    result = result.lower().strip()
    if result not in ["win", "loss", "draw"]:
        print(f"Invalid result: '{result}'. Use win / loss / draw.")
        return

    if not os.path.exists(INPUT_LOG):
        print(f"File {INPUT_LOG} not found.")
        return

    with open(INPUT_LOG, "r") as infile:
        lines = [line.strip() for line in infile if line.strip().startswith("BOOK_ENTRY")]

    total_lines = len(lines)
    print(f"Found {total_lines} BOOK_ENTRY lines.")

    with open(OUTPUT_LOG, "w") as out:
        for i in range(0, total_lines, LINES_PER_GAME):
            chunk = lines[i:i + LINES_PER_GAME]
            out.write("# GAME_START\n")
            for entry in chunk:
                out.write(entry + "\n")
            out.write(f"# RESULT: {result}\n")
            out.write("# GAME_END\n\n")

    print(f"New log written to: {OUTPUT_LOG}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python prepare_book_log_generic.py <win|loss|draw>")
    else:
        prepare_log(sys.argv[1])
