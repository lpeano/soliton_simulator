@echo off
REM TEST SENSIBILITA: scansione del coefficiente elastico C=30/100/300.
set SIM=soliton_simulator.py
set PASSI=4000
set OGNI=5
if not exist out_elast mkdir out_elast
if not exist log mkdir log
for %%S in (1 2) do (
  for %%C in (30 100 300) do (
    START "elast_c%%C_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 4 --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --elast-c %%C --csv out_elast\cond_c%%C_s%%S.csv --diaglog out_elast\c%%C_s%%S.csv > log\elast_c%%C_s%%S.log 2>&1"
  )
)
echo Test sensibilita' lanciato: confrontare m0_coer e m0_coer_nucleo.
pause
