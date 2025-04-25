@echo off
echo Learn Tool for Polyglot .bin Book
echo Usage: learn_tool.bat book.bin hex_key hex_move delta
echo Example: learn_tool.bat book.bin 8A2D3C4B5E6F7081 1234 500
learn_tool.exe %1 %2 %3 %4
pause
