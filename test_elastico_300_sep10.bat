@echo off
REM TEST ELASTICO RAPIDO SEP=10: A/B ELAST_C=100 contro ELAST_C=0.
REM Identico a test_elastico_300.bat, cambia solo sep da 4 a 10.
REM 300 passi: controllo preliminare, non verdetto sul plateau.
set SIM=soliton_simulator.py
set PASSI=300
set OGNI=5
set DBOGNI=100
set SEP=10
set CATENA=--verlet --sync --viriale --zeta-vir --pav-com --chi-basc --polo-maturo --olon-part --calore-vett
if not exist out_elast mkdir out_elast
if not exist log mkdir log
for %%S in (1 2 3) do (
  START "elast300_sep10_on_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %CATENA% --elast-c 100 --sync-db out_elast\db_on_300_sep10_s%%S.pkl --db-ogni %DBOGNI% --csv out_elast\cond_on_300_sep10_s%%S.csv --diaglog out_elast\on_300_sep10_s%%S.csv > log\elast300_sep10_on_s%%S.log 2>&1"
  START "elast300_sep10_off_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %CATENA% --elast-c 0 --sync-db out_elast\db_off_300_sep10_s%%S.pkl --db-ogni %DBOGNI% --csv out_elast\cond_off_300_sep10_s%%S.csv --diaglog out_elast\off_300_sep10_s%%S.csv > log\elast300_sep10_off_s%%S.log 2>&1"
)
echo Test elastico sep=10 lanciato: 3 semi, 300 passi, ON/OFF C=100/0.
echo Output: out_elast\*300_sep10*   Log: log\elast300_sep10*.
echo Confrontare m0_coer, m0_coer_nucleo, m0_Lz e Lz_orb_01.
pause
