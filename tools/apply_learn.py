import subprocess
import datetime

# Configuration
LOG_FILE = "book_usage.log"
HISTORY_LOG = "learn_update_history.log"

DELTA_MAP = {
    "win": 500,
    "loss": -500,
    "draw": 0
}

# Parse one line and extract book, key, move
def parse_log_line(line):
    parts = line.strip().split()
    book = None
    key = None
    move = None
    for part in parts:
        if part.startswith("book="):
            book = part[5:]
        elif part.startswith("key="):
            key = part[4:]
        elif part.startswith("move="):
            move = part[5:]
    return book, key, move

# Process a block of one game
def process_game_block(entries, result):
    delta = DELTA_MAP.get(result, 0)
    print(f"\nProcessing game with result: {result} (delta = {delta})")

    with open(HISTORY_LOG, "a") as hist:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hist.write(f"\n=== Game processed at {timestamp} (Result: {result}) ===\n")

        for line in entries:
            if not line.startswith("BOOK_ENTRY"):
                continue

            book, key, move = parse_log_line(line)
            if book and key and move:
                book_file = "book1.bin" if book.lower() == "book1" else "book2.bin"
                print(f"Updating: {book} ({book_file}) key={key}, move={move}")
                subprocess.run(["learn_tool.exe", book_file, key, move, str(delta)])

                hist.write(f"{book_file} key={key} move={move} delta={delta}\n")

# Main batch processing
def main():
    current_block = []
    current_result = None
    inside_game = False
    games_processed = 0

    with open(LOG_FILE, "r") as f:
        for line in f:
            line = line.strip()

            if line == "# GAME_START":
                inside_game = True
                current_block = []
                current_result = None

            elif line.startswith("# RESULT:") and inside_game:
                current_result = line.split(":")[1].strip().lower()

            elif line == "# GAME_END" and inside_game:
                if current_result:
                    process_game_block(current_block, current_result)
                    games_processed += 1
                else:
                    print("\nWarning: game block missing result, skipped.")
                inside_game = False
                current_block = []

            elif inside_game:
                current_block.append(line)

    print(f"\n✅ All done. {games_processed} games processed.")

    # Clear the original log
    with open(LOG_FILE, "w") as f:
        f.write("")  # Empty the log

    print("🧹 book_usage.log has been cleared.")
    print(f"📄 Updates saved to {HISTORY_LOG}")

if __name__ == "__main__":
    main()
