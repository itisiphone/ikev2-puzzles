@echo off
rem experiments E1-E6. Double-click to run all, or: run_experiments.bat E4
cd /d "%~dp0"
set PRISM_DIR=E:\PRISM\prism-4.10.1
set PATH=%PRISM_DIR%\lib;%PATH%
echo Started %date% %time% > experiments\run_times.txt
if not "%~1"=="" goto %~1
:E1
echo [E1] D_max = 16, forged difficulty 20/24/28 ...
echo E1 E1_Dmax16_df20-28 start %time% >> experiments\run_times.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1.sm experiments\ikev2_rq1_exp.props -const attack=1,defense=2,d_f=20:4:28,D_max=16,ratio_F=2,T=10:50:60 -exportresults experiments\E1_Dmax16_df20-28.csv:csv > experiments\log_E1_Dmax16_df20-28.txt 2>&1
echo [E1] D_max = 16, forged ZBC = 0 ...
echo E1 E1_Dmax16_df0 start %time% >> experiments\run_times.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1.sm experiments\ikev2_rq1_exp.props -const attack=1,defense=2,d_f=0,D_max=16,ratio_F=2,T=10:50:60 -exportresults experiments\E1_Dmax16_df0.csv:csv > experiments\log_E1_Dmax16_df0.txt 2>&1
echo [E1] D_max = 18, forged difficulty 20/24/28 ...
echo E1 E1_Dmax18_df20-28 start %time% >> experiments\run_times.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1.sm experiments\ikev2_rq1_exp.props -const attack=1,defense=2,d_f=20:4:28,D_max=18,ratio_F=2,T=10:50:60 -exportresults experiments\E1_Dmax18_df20-28.csv:csv > experiments\log_E1_Dmax18_df20-28.txt 2>&1
echo [E1] D_max = 18, forged ZBC = 0 ...
echo E1 E1_Dmax18_df0 start %time% >> experiments\run_times.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1.sm experiments\ikev2_rq1_exp.props -const attack=1,defense=2,d_f=0,D_max=18,ratio_F=2,T=10:50:60 -exportresults experiments\E1_Dmax18_df0.csv:csv > experiments\log_E1_Dmax18_df0.txt 2>&1
echo [E1] D_max = 20, forged difficulty 20/24/28 ...
echo E1 E1_Dmax20_df20-28 start %time% >> experiments\run_times.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1.sm experiments\ikev2_rq1_exp.props -const attack=1,defense=2,d_f=20:4:28,D_max=20,ratio_F=2,T=10:50:60 -exportresults experiments\E1_Dmax20_df20-28.csv:csv > experiments\log_E1_Dmax20_df20-28.txt 2>&1
echo [E1] D_max = 20, forged ZBC = 0 ...
echo E1 E1_Dmax20_df0 start %time% >> experiments\run_times.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1.sm experiments\ikev2_rq1_exp.props -const attack=1,defense=2,d_f=0,D_max=20,ratio_F=2,T=10:50:60 -exportresults experiments\E1_Dmax20_df0.csv:csv > experiments\log_E1_Dmax20_df0.txt 2>&1
echo [E1] D_max = 24, forged difficulty 20/24/28 ...
echo E1 E1_Dmax24_df20-28 start %time% >> experiments\run_times.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1.sm experiments\ikev2_rq1_exp.props -const attack=1,defense=2,d_f=20:4:28,D_max=24,ratio_F=2,T=10:50:60 -exportresults experiments\E1_Dmax24_df20-28.csv:csv > experiments\log_E1_Dmax24_df20-28.txt 2>&1
echo [E1] D_max = 24, forged ZBC = 0 ...
echo E1 E1_Dmax24_df0 start %time% >> experiments\run_times.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1.sm experiments\ikev2_rq1_exp.props -const attack=1,defense=2,d_f=0,D_max=24,ratio_F=2,T=10:50:60 -exportresults experiments\E1_Dmax24_df0.csv:csv > experiments\log_E1_Dmax24_df0.txt 2>&1
echo [E1] D_max = 255, forged difficulty 20/24/28 ...
echo E1 E1_Dmax255_df20-28 start %time% >> experiments\run_times.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1.sm experiments\ikev2_rq1_exp.props -const attack=1,defense=2,d_f=20:4:28,D_max=255,ratio_F=2,T=10:50:60 -exportresults experiments\E1_Dmax255_df20-28.csv:csv > experiments\log_E1_Dmax255_df20-28.txt 2>&1
echo [E1] D_max = 255, forged ZBC = 0 ...
echo E1 E1_Dmax255_df0 start %time% >> experiments\run_times.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1.sm experiments\ikev2_rq1_exp.props -const attack=1,defense=2,d_f=0,D_max=255,ratio_F=2,T=10:50:60 -exportresults experiments\E1_Dmax255_df0.csv:csv > experiments\log_E1_Dmax255_df0.txt 2>&1
if not "%~1"=="" goto done
:E2
echo [E2] attacker speed ratio_F = 0.5 ... 5 ...
echo E2 E2_ratio start %time% >> experiments\run_times.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1.sm experiments\ikev2_rq1_exp.props -const attack=1,defense=2,d_f=24:4:28,D_max=24,ratio_F=0.5:0.5:5,T=10:50:60 -exportresults experiments\E2_ratio.csv:csv > experiments\log_E2_ratio.txt 2>&1
if not "%~1"=="" goto done
:E4
echo [E4] baseline without attack ...
echo E4 E4_baseline start %time% >> experiments\run_times.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq2.sm experiments\ikev2_rq2_exp.props -gs -maxiters 100000 -const attack=0,defense=0,lam_att=0,rho=0.5,N_bots=100,H=50,tau_R=2,theta=0,k=18 -exportresults experiments\E4_baseline.csv:csv > experiments\log_E4_baseline.txt 2>&1
echo [E4] T2 flooding, 3 defences x 20 rates x 3 bot shares ...
echo E4 E4_T2 start %time% >> experiments\run_times.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq2.sm experiments\ikev2_rq2_exp.props -gs -maxiters 100000 -const attack=2,defense=0:2,lam_att=10:10:200,rho=0.25:0.25:0.75,N_bots=100,H=50,tau_R=2,theta=0,k=18 -exportresults experiments\E4_T2.csv:csv > experiments\log_E4_T2.txt 2>&1
echo [E4] T3 junk IKE_AUTH, 3 defences x 10 rates ...
echo E4 E4_T3 start %time% >> experiments\run_times.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq2.sm experiments\ikev2_rq2_exp.props -gs -maxiters 100000 -const attack=3,defense=0:2,lam_att=50:50:500,rho=0.5,N_bots=100,H=50,tau_R=2,theta=0,k=18 -exportresults experiments\E4_T3.csv:csv > experiments\log_E4_T3.txt 2>&1
if not "%~1"=="" goto done
:E5
echo [E5] table size x lifetime grid, k = 18 ...
echo E5 E5_k18 start %time% >> experiments\run_times.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq2.sm experiments\ikev2_rq2_exp.props -gs -maxiters 100000 -const attack=2,defense=2,lam_att=100,rho=0.5,N_bots=100,H=20:10:100,tau_R=2:1:10,theta=0,k=18 -exportresults experiments\E5_k18.csv:csv > experiments\log_E5_k18.txt 2>&1
echo [E5] table size x lifetime grid, k = 20 ...
echo E5 E5_k20 start %time% >> experiments\run_times.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq2.sm experiments\ikev2_rq2_exp.props -gs -maxiters 100000 -const attack=2,defense=2,lam_att=100,rho=0.5,N_bots=100,H=20:10:100,tau_R=2:1:10,theta=0,k=20 -exportresults experiments\E5_k20.csv:csv > experiments\log_E5_k20.txt 2>&1
if not "%~1"=="" goto done
:E6
echo [E6] puzzle difficulty k = 8 ... 24 under T2 ...
echo E6 E6_T2 start %time% >> experiments\run_times.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq2.sm experiments\ikev2_rq2_exp.props -gs -maxiters 100000 -const attack=2,defense=2,lam_att=100,rho=0.5,N_bots=100,H=50,tau_R=2,theta=0,k=8:2:24 -exportresults experiments\E6_T2.csv:csv > experiments\log_E6_T2.txt 2>&1
echo [E6] puzzle difficulty k = 8 ... 24 under T3 ...
echo E6 E6_T3 start %time% >> experiments\run_times.txt
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq2.sm experiments\ikev2_rq2_exp.props -gs -maxiters 100000 -const attack=3,defense=2,lam_att=300,rho=0.5,N_bots=100,H=50,tau_R=2,theta=0,k=8:2:24 -exportresults experiments\E6_T3.csv:csv > experiments\log_E6_T3.txt 2>&1
if not "%~1"=="" goto done
:done
echo Finished %date% %time% >> experiments\run_times.txt
echo.
echo Done. Results are in the experiments folder.
call run_plots.bat nopause
pause
exit /b 0
:E1none
echo [E1] rerun: D_max = none, forged ZBC = 0 ...
java -Xss4M -Djava.library.path="%PRISM_DIR%\lib" -classpath "%PRISM_DIR%\lib\prism.jar;%PRISM_DIR%\lib\*" prism.PrismCL ikev2_rq1.sm experiments\ikev2_rq1_exp.props -const attack=1,defense=2,d_f=0,D_max=255,ratio_F=2,T=10:50:60 -exportresults experiments\E1_Dmax255_df0.csv:csv > experiments\log_E1_Dmax255_df0.txt 2>&1
goto done
