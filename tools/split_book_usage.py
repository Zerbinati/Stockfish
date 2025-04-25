# split_book_usage.py
import os
import datetime

INPUT_LOG = "book_usage.log"
LINES_PER_GAME = 40  # Each game consists of 40 BOOK_ENTRY lines (20 full moves)
BASE_FOLDER = "split_games"

def split_log():
    if not os.path.exists(INPUT_LOG):
        print(f"File '{INPUT_LOG}' not found.")
        return

    with open(INPUT_LOG, "r") as infile:
        lines = [line.strip() for line in infile if line.strip().startswith("BOOK_ENTRY")]

    if not lines:
        print("No BOOK_ENTRY lines found.")
        return

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    output_folder = f"{BASE_FOLDER}_{timestamp}"
    os.makedirs(output_folder, exist_ok=True)

    count = 0
    for i in range(0, len(lines), LINES_PER_GAME):
        chunk = lines[i:i + LINES_PER_GAME]
        count += 1
        filename = os.path.join(output_folder, f"game_{count:02}.log")
        with open(filename, "w") as f:
            f.write("# GAME_START\n")
            f.writelines(line + "\n" for line in chunk)
            f.write("# RESULT: win\n")   # Change manually if needed
            f.write("# GAME_END\n")

    print(f"{count} game file(s) written to folder '{output_folder}'.")

if __name__ == "__main__":
    split_log()
