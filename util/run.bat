@echo off
for /f %%f IN ('dir /b ..\test_cases') DO (CALL :RunStuff %%f)
GOTO :EOF

:RunStuff
SET name=%1
echo %name% >> run.txt
python ..\solver.py ..\test_cases\%name% result.txt >> run.txt
python compareResults.py result.txt ..\solutions\%name:~0,-4%_solution.txt >> run.txt