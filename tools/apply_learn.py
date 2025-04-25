# apply_learn.py
import os
import shutil
import subprocess
from datetime import datetime

# Configuration
LOG_FILE = "book_usage_ready.log"
BOOK_FILE = "book1.bin"  # Change if needed
LEARN_TOOL = "learn_tool.exe"
HISTORY_LOG = "learn_update_history.log"
BACKUP_FOLDER = "backups"

# Delta values per result type
DELTA_VALUES = {
    "win": 500,
    "loss": -500,
    "draw": 0
}

def apply_learn():
    if not os.path.exists(LOG_FILE):
        print(f"Log file '{LOG_FILE}' not found.")
        return

    if not os.path.exists(BOOK_FILE):
        print(f"Book file '{BOOK_FILE}' not found.")
        return

    # Read and parse the log
    with open(LOG_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    result = None
    entries = []

    for line in lines:
        if line.startswith("# RESULT:"):
            result = line.split(":")[1].strip().lower()
        elif line.startswith("BOOK_ENTRY"):
            parts = line.split()
            key = None
            move = None
            for p in parts:
                if p.startswith("key="):
                    key = p.split("=")[1]
                elif p.startswith("move="):
                    move = p.split("=")[1]
            if key and move:
                entries.append((key, move))

    if not result or result not in DELTA_VALUES:
        print("Invalid or missing result in log.")
        return

    delta = DELTA_VALUES[result]

    if not entries:
        print("No BOOK_ENTRY found in log.")
        return

    # Backup the book file
    os.makedirs(BACKUP_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_FOLDER, f"{BOOK_FILE}.{timestamp}.bak")
    shutil.copy2(BOOK_FILE, backup_path)
    print(f"Backup created: {backup_path}")

    print(f"\nApplying learning for result: {result.upper()} (delta = {delta})")
    print(f"Updating {len(entries)} entries...\n")

    with open(HISTORY_LOG, "a") as history:
        for key, move in entries:
            cmd = [LEARN_TOOL, BOOK_FILE, key, move, str(delta)]
            try:
                subprocess.run(cmd, check=True)
                print(f"Updated: key={key}, move={move}, delta={delta}")
                history.write(f"{BOOK_FILE} | key={key} | move={move} | delta={delta} | result={result} | time={timestamp}\n")
            except subprocess.CalledProcessError:
                print(f"Failed to update: key={key}, move={move}")

    # Clear the log after processing
    open(LOG_FILE, "w").close()
    print("\nLog cleared.")

if __name__ == "__main__":
    apply_learn()
