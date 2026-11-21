@echo off
rem E8, E9 and solver check. Double-click to run (about 20 minutes).
cd /d "%~dp0"
set PRISM_DIR=E:\PRISM\prism-4.10.1
set PATH=%PRISM_DIR%\lib;%PATH%
echo Started %date% %time% > experiments\run_times_E8.txt
echo [V_jacobi_E4_baseline] ...
echo V_jacobi_E4_baseline start %time% >> experiments\run_times_E8.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq2.sm experiments\ikev2_rq2_exp.props -jacobi -maxiters 100000 -const attack=0,defense=0,lam_att=0,rho=0.5,N_bots=100,H=50,tau_R=2,theta=0,k=18 -exportresults validation\V_jacobi_E4_baseline.csv:csv > validation\log_V_jacobi_E4_baseline.txt 2>&1
echo [V_jacobi_E4_T2] ...
echo V_jacobi_E4_T2 start %time% >> experiments\run_times_E8.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq2.sm experiments\ikev2_rq2_exp.props -jacobi -maxiters 100000 -const attack=2,defense=0:2,lam_att=50:50:200,rho=0.5,N_bots=100,H=50,tau_R=2,theta=0,k=18 -exportresults validation\V_jacobi_E4_T2.csv:csv > validation\log_V_jacobi_E4_T2.txt 2>&1
echo [V_jacobi_E4_T3] ...
echo V_jacobi_E4_T3 start %time% >> experiments\run_times_E8.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq2.sm experiments\ikev2_rq2_exp.props -jacobi -maxiters 100000 -const attack=3,defense=0:2,lam_att=100:200:500,rho=0.5,N_bots=100,H=50,tau_R=2,theta=0,k=18 -exportresults validation\V_jacobi_E4_T3.csv:csv > validation\log_V_jacobi_E4_T3.txt 2>&1
echo [V_jacobi_E5] ...
echo V_jacobi_E5 start %time% >> experiments\run_times_E8.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq2.sm experiments\ikev2_rq2_exp.props -jacobi -maxiters 100000 -const attack=2,defense=2,lam_att=100,rho=0.5,N_bots=100,H=20:80:100,tau_R=2:8:10,theta=0,k=18 -exportresults validation\V_jacobi_E5.csv:csv > validation\log_V_jacobi_E5.txt 2>&1
echo [E8_sar1_a] ...
echo E8_sar1_a start %time% >> experiments\run_times_E8.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=0:2,f_type=1,multi=0,w_I=0,d_f=24,D_max=18,ratio_F=2,T=10:50:60 -exportresults experiments\E8_sar1_a.csv:csv > experiments\log_E8_sar1_a.txt 2>&1
echo [E8_sar1_b] ...
echo E8_sar1_b start %time% >> experiments\run_times_E8.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=0:2,f_type=1,multi=0,w_I=0.1,d_f=24,D_max=18,ratio_F=2,T=10:50:60 -exportresults experiments\E8_sar1_b.csv:csv > experiments\log_E8_sar1_b.txt 2>&1
echo [E8_sar1_c] ...
echo E8_sar1_c start %time% >> experiments\run_times_E8.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=0:2,f_type=1,multi=1,w_I=0.1,d_f=24,D_max=18,ratio_F=2,T=10:50:60 -exportresults experiments\E8_sar1_c.csv:csv > experiments\log_E8_sar1_c.txt 2>&1
echo [E9_cookie_D18_w0] ...
echo E9_cookie_D18_w0 start %time% >> experiments\run_times_E8.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=1,f_type=0,multi=0,w_I=0,d_f=0:24:24,D_max=18,ratio_F=2,T=10:50:60 -exportresults experiments\E9_cookie_D18_w0.csv:csv > experiments\log_E9_cookie_D18_w0.txt 2>&1
echo [E9_cookie_D18_w0p1] ...
echo E9_cookie_D18_w0p1 start %time% >> experiments\run_times_E8.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=1,f_type=0,multi=0,w_I=0.1,d_f=0:24:24,D_max=18,ratio_F=2,T=10:50:60 -exportresults experiments\E9_cookie_D18_w0p1.csv:csv > experiments\log_E9_cookie_D18_w0p1.txt 2>&1
echo [E9_cookie_D255_w0] ...
echo E9_cookie_D255_w0 start %time% >> experiments\run_times_E8.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=1,f_type=0,multi=0,w_I=0,d_f=0:24:24,D_max=255,ratio_F=2,T=10:50:60 -exportresults experiments\E9_cookie_D255_w0.csv:csv > experiments\log_E9_cookie_D255_w0.txt 2>&1
echo [E9_cookie_D255_w0p1] ...
echo E9_cookie_D255_w0p1 start %time% >> experiments\run_times_E8.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=1,f_type=0,multi=0,w_I=0.1,d_f=0:24:24,D_max=255,ratio_F=2,T=10:50:60 -exportresults experiments\E9_cookie_D255_w0p1.csv:csv > experiments\log_E9_cookie_D255_w0p1.txt 2>&1
echo [E7v3_df24_a] ...
echo E7v3_df24_a start %time% >> experiments\run_times_E8.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=2,f_type=0,multi=0,d_f=24,D_max=255,ratio_F=2,w_I=0:0.05:0.1,T=10:50:60 -exportresults experiments\E7v3_df24_a.csv:csv > experiments\log_E7v3_df24_a.txt 2>&1
echo [E7v3_df24_b] ...
echo E7v3_df24_b start %time% >> experiments\run_times_E8.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=2,f_type=0,multi=0,d_f=24,D_max=255,ratio_F=2,w_I=0.25:0.25:0.5,T=10:50:60 -exportresults experiments\E7v3_df24_b.csv:csv > experiments\log_E7v3_df24_b.txt 2>&1
echo [E7v3_df0_a] ...
echo E7v3_df0_a start %time% >> experiments\run_times_E8.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=2,f_type=0,multi=0,d_f=0,D_max=255,ratio_F=2,w_I=0:0.05:0.1,T=10:50:60 -exportresults experiments\E7v3_df0_a.csv:csv > experiments\log_E7v3_df0_a.txt 2>&1
echo [E7v3_df0_b] ...
echo E7v3_df0_b start %time% >> experiments\run_times_E8.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=2,f_type=0,multi=0,d_f=0,D_max=255,ratio_F=2,w_I=0.25:0.25:0.5,T=10:50:60 -exportresults experiments\E7v3_df0_b.csv:csv > experiments\log_E7v3_df0_b.txt 2>&1
echo [E7v3_df18_a] ...
echo E7v3_df18_a start %time% >> experiments\run_times_E8.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=2,f_type=0,multi=0,d_f=18,D_max=255,ratio_F=2,w_I=0:0.05:0.1,T=10:50:60 -exportresults experiments\E7v3_df18_a.csv:csv > experiments\log_E7v3_df18_a.txt 2>&1
echo [E7v3_df18_b] ...
echo E7v3_df18_b start %time% >> experiments\run_times_E8.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=2,f_type=0,multi=0,d_f=18,D_max=255,ratio_F=2,w_I=0.25:0.25:0.5,T=10:50:60 -exportresults experiments\E7v3_df18_b.csv:csv > experiments\log_E7v3_df18_b.txt 2>&1
echo [E7v3_df16_a] ...
echo E7v3_df16_a start %time% >> experiments\run_times_E8.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=2,f_type=0,multi=0,d_f=16,D_max=255,ratio_F=2,w_I=0:0.05:0.1,T=10:50:60 -exportresults experiments\E7v3_df16_a.csv:csv > experiments\log_E7v3_df16_a.txt 2>&1
echo [E7v3_df16_b] ...
echo E7v3_df16_b start %time% >> experiments\run_times_E8.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1_wait.sm experiments\ikev2_rq1_wait.props -const attack=1,defense=2,f_type=0,multi=0,d_f=16,D_max=255,ratio_F=2,w_I=0.25:0.25:0.5,T=10:50:60 -exportresults experiments\E7v3_df16_b.csv:csv > experiments\log_E7v3_df16_b.txt 2>&1
echo Finished %date% %time% >> experiments\run_times_E8.txt
echo.
echo Done. Results are in the experiments folder.
pause
