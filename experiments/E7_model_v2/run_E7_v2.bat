@echo off
rem E7 (Discussion): wait-window mitigation, version 2 (solve both puzzles, cheaper first). Double-click to run (about 15 minutes).
cd /d "%~dp0"
set PRISM_DIR=E:\PRISM\prism-4.10.1
set PATH=%PRISM_DIR%\lib;%PATH%
echo Started %date% %time% > experiments\run_times_E7.txt
echo [E7] forged d_f = 24, wait window w_I = 0:0.05:0.1 ...
echo E7_df24_a start %time% >> experiments\run_times_E7.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=2,d_f=24,D_max=255,ratio_F=2,w_I=0:0.05:0.1,T=10:50:60 -exportresults experiments\E7_df24_a.csv:csv > experiments\log_E7_df24_a.txt 2>&1
echo [E7] forged d_f = 24, wait window w_I = 0.25:0.25:0.5 ...
echo E7_df24_b start %time% >> experiments\run_times_E7.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=2,d_f=24,D_max=255,ratio_F=2,w_I=0.25:0.25:0.5,T=10:50:60 -exportresults experiments\E7_df24_b.csv:csv > experiments\log_E7_df24_b.txt 2>&1
echo [E7] forged d_f = 0, wait window w_I = 0:0.05:0.1 ...
echo E7_df0_a start %time% >> experiments\run_times_E7.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=2,d_f=0,D_max=255,ratio_F=2,w_I=0:0.05:0.1,T=10:50:60 -exportresults experiments\E7_df0_a.csv:csv > experiments\log_E7_df0_a.txt 2>&1
echo [E7] forged d_f = 0, wait window w_I = 0.25:0.25:0.5 ...
echo E7_df0_b start %time% >> experiments\run_times_E7.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=2,d_f=0,D_max=255,ratio_F=2,w_I=0.25:0.25:0.5,T=10:50:60 -exportresults experiments\E7_df0_b.csv:csv > experiments\log_E7_df0_b.txt 2>&1
echo [E7] forged d_f = 18, wait window w_I = 0:0.05:0.1 ...
echo E7_df18_a start %time% >> experiments\run_times_E7.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=2,d_f=18,D_max=255,ratio_F=2,w_I=0:0.05:0.1,T=10:50:60 -exportresults experiments\E7_df18_a.csv:csv > experiments\log_E7_df18_a.txt 2>&1
echo [E7] forged d_f = 18, wait window w_I = 0.25:0.25:0.5 ...
echo E7_df18_b start %time% >> experiments\run_times_E7.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=2,d_f=18,D_max=255,ratio_F=2,w_I=0.25:0.25:0.5,T=10:50:60 -exportresults experiments\E7_df18_b.csv:csv > experiments\log_E7_df18_b.txt 2>&1
echo [E7] forged d_f = 16, wait window w_I = 0:0.05:0.1 ...
echo E7_df16_a start %time% >> experiments\run_times_E7.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=2,d_f=16,D_max=255,ratio_F=2,w_I=0:0.05:0.1,T=10:50:60 -exportresults experiments\E7_df16_a.csv:csv > experiments\log_E7_df16_a.txt 2>&1
echo [E7] forged d_f = 16, wait window w_I = 0.25:0.25:0.5 ...
echo E7_df16_b start %time% >> experiments\run_times_E7.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=2,d_f=16,D_max=255,ratio_F=2,w_I=0.25:0.25:0.5,T=10:50:60 -exportresults experiments\E7_df16_b.csv:csv > experiments\log_E7_df16_b.txt 2>&1
echo Finished %date% %time% >> experiments\run_times_E7.txt
echo.
echo Done. Results are in the experiments folder.
pause
