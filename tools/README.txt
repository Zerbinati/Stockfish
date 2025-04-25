==========================================
Polyglot Book Learning Automation System
==========================================

This toolset allows you to apply custom learning to a Polyglot-compatible binary book file (.bin)
based on actual game results (win, loss, draw). The system is modular and works in three stages:

1. Splitting game logs
2. Preparing learning entries
3. Applying learning to the book

--------------------------------------------------
REQUIREMENTS
--------------------------------------------------

- Python 3 installed
- learn_tool.exe (compiled C++ tool to update book entries)
- A valid Polyglot book file (e.g. book1.bin)
- BOOK_ENTRY log generated during game (book_usage.log)

--------------------------------------------------
1. SPLITTING THE BOOK LOG INTO INDIVIDUAL GAMES
--------------------------------------------------

Run the following script:

    python split_book_usage.py

This will:

- Read the file: book_usage.log
- Split it into chunks of 40 lines (20 full moves per game)
- Create a folder like: split_games_YYYYMMDD_HHMM
- Inside, you will find: game_01.log, game_02.log, etc.
- Each game file contains:
    # GAME_START
    BOOK_ENTRY ...
    ...
    # RESULT: win     <-- Change manually to loss or draw if needed
    # GAME_END

--------------------------------------------------
2. PREPARING THE BOOK LEARNING LOG
--------------------------------------------------

For each game you want to process:

1. Rename one of the game_X.log files to:

    book_usage.log

2. Then run:

    prepare_and_apply_menu.bat

3. Select the match result:

    1 = Win
    2 = Loss
    3 = Draw

This will:

- Generate a formatted log (book_usage_ready.log)
- Automatically launch apply_learn.py
- Apply the learning delta (based on result) to the book1.bin file

--------------------------------------------------
3. APPLYING THE LEARNING TO THE BOOK
--------------------------------------------------

apply_learn.py will:

- Read book_usage_ready.log
- Parse all key/move entries
- Determine the delta to apply:
    - Win  → +500
    - Loss → -500
    - Draw →  0
- Call learn_tool.exe to modify book1.bin
- Create a timestamped backup of the book in /backups/
- Log the update in learn_update_history.log
- Clear the processed log for safety

--------------------------------------------------
OPTIONAL: TEST MOVE PROBABILITIES
--------------------------------------------------

To simulate how the weight + learn values affect move probability, use:

    python simulate_book_percentages.py

You can input multiple (weight, learn) pairs and see the resulting percentages,
exactly like Scid or GUI book viewers would show.

--------------------------------------------------
FOLDER STRUCTURE (RECOMMENDED)
--------------------------------------------------

/your_folder/
├── book1.bin
├── book_usage.log
├── book_usage_ready.log
├── backups/
│   └── book1.bin.YYYYMMDD_HHMMSS.bak
├── split_games_YYYYMMDD_HHMM/
│   ├── game_01.log
│   ├── ...
├── learn_tool.exe
├── apply_learn.py
├── prepare_book_log_generic.py
├── prepare_and_apply_menu.bat
├── split_book_usage.py
├── simulate_book_percentages.py
├── learn_update_history.log
├── README.txt

--------------------------------------------------
NOTES
--------------------------------------------------

- You must manually label each game file with the correct result before preparing.
- Only the first 40 moves are processed (adjustable).
- Each execution updates the book immediately and permanently.
- Backups are always created before modification.

--------------------------------------------------
CREDITS
--------------------------------------------------

This system is designed for users who want full control over Polyglot book learning.
Developed with modular Python and C++ for educational and practical use.

Questions, improvements, or feedback are welcome!
