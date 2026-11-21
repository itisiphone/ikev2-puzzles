@echo off
rem draw figures 3-7 and the model-size table from experiments\*.csv
rem needs Python 3 with matplotlib on PATH (or set PY to your python.exe)
cd /d "%~dp0"
if "%PY%"=="" set "PY=python"
echo Drawing figures ...
"%PY%" experiments\plot_figures.py > experiments\plot_log.txt 2>&1
type experiments\plot_log.txt
echo.
echo Figures are in experiments\figures
if "%~1"=="" pause
