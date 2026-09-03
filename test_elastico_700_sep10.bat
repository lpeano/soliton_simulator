@echo off
REM TEST ELASTICO SEP=10: A/B ELAST_C=100 contro ELAST_C=0.
REM Variante da 700 passi del test_elastico_300_sep10.bat.
REM 700 passi: controllo intermedio; non sostituisce il run lungo da 4000.
set SIM=soliton_simulator.py
set PASSI=700
set OGNI=5
set DBOGNI=100
set SEP=10
set CATENA=--verlet --sync --viriale --zeta-vir --pav-com --chi-basc --polo-maturo --olon-part --calore-vett
if not exist out_elast mkdir out_elast
if not exist log mkdir log
for %%S in (1 2 3) do (
  START "elast700_sep10_on_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %CATENA% --elast-c 100 --sync-db out_elast\db_on_700_sep10_s%%S.pkl --db-ogni %DBOGNI% --csv out_elast\cond_on_700_sep10_s%%S.csv --diaglog out_elast\on_700_sep10_s%%S.csv > log\elast700_sep10_on_s%%S.log 2>&1"
  START "elast700_sep10_off_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %CATENA% --elast-c 0 --sync-db out_elast\db_off_700_sep10_s%%S.pkl --db-ogni %DBOGNI% --csv out_elast\cond_off_700_sep10_s%%S.csv --diaglog out_elast\off_700_sep10_s%%S.csv > log\elast700_sep10_off_s%%S.log 2>&1"
)
echo Test elastico sep=10 lanciato: 3 semi, 700 passi, ON/OFF C=100/0.
echo Output: out_elast\*700_sep10*   Log: log\elast700_sep10*.
echo Confrontare m0_coer, m0_coer_nucleo, m0_Lz e Lz_orb_01.
pause
