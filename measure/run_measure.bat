@echo off
rem needs Python 3 with the cryptography package on PATH (or set PY to your python.exe)
cd /d "%~dp0"
if "%PY%"=="" set "PY=python"
echo Using "%PY%"
echo Measuring costs, this takes a few minutes. Please keep other programs idle.
"%PY%" measure_costs.py > measure_log.txt 2>&1
type measure_log.txt
echo.
echo Done. Results: costs_summary.txt, costs_results.csv, puzzle_results.csv
pause
