@echo off
rem E0: no-attack baseline of M1 and deadlock checks. Double-click to run (a few minutes).
cd /d "%~dp0"
set PRISM_DIR=E:\PRISM\prism-4.10.1
set PATH=%PRISM_DIR%\lib;%PATH%
echo Started %date% %time% > experiments\run_times_E0.txt
echo [E0] M1 without attack, defences 0..2, T = 10 and 60 s ...
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1.sm experiments\ikev2_rq1_baseline.props -const attack=0,defense=0:2,d_f=24,D_max=18,ratio_F=2,T=10:50:60 -exportresults experiments\E0_M1_noattack.csv:csv > experiments\log_E0_M1_noattack.txt 2>&1
echo [E0] deadlock checks: M1 under attack ...
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1.sm experiments\deadlock.props -const attack=1,defense=2,d_f=0:24:24,D_max=18,ratio_F=2 -exportresults experiments\E0_deadlock_M1_a.csv:csv > experiments\log_E0_deadlock_M1_a.txt 2>&1
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1.sm experiments\deadlock.props -const attack=1,defense=2,d_f=0:24:24,D_max=255,ratio_F=2 -exportresults experiments\E0_deadlock_M1_b.csv:csv > experiments\log_E0_deadlock_M1_b.txt 2>&1
echo [E0] deadlock checks: wait-window variant ...
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\deadlock.props -const attack=1,defense=2,d_f=0:8:24,D_max=255,ratio_F=2,w_I=0.1 -exportresults experiments\E0_deadlock_wait.csv:csv > experiments\log_E0_deadlock_wait.txt 2>&1
echo Finished %date% %time% >> experiments\run_times_E0.txt
echo.
echo Done. Results are in the experiments folder.
pause
