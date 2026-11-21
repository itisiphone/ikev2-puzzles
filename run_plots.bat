@echo off
rem draw figures 3-8 and table 3 from experiments\*.csv
cd /d "%~dp0"
set "CONDA_DIR=E:\Anaconda\anacondainstall"
set "PATH=%CONDA_DIR%;%CONDA_DIR%\Library\mingw-w64\bin;%CONDA_DIR%\Library\usr\bin;%CONDA_DIR%\Library\bin;%CONDA_DIR%\Scripts;%PATH%"
echo Drawing figures ...
"%CONDA_DIR%\python.exe" experiments\plot_figures.py > experiments\plot_log.txt 2>&1
type experiments\plot_log.txt
echo.
echo Figures are in experiments\figures
if "%~1"=="" pause
