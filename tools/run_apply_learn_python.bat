@echo off
set PYTHON_EXEC=python
set SCRIPT=apply_learn_batch.py

echo Running batch update from book_usage.log...
%PYTHON_EXEC% %SCRIPT%

pause

