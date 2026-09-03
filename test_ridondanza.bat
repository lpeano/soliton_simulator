@echo off
REM TEST RIDONDANZA: il nucleo elastico C=100 aggiunge informazione rispetto
REM al rinforzo di shear? A/B su tre semi, caso attaccato sep=4.
set SIM=soliton_simulator.py
set PASSI=4000
set OGNI=5
set DBOGNI=100
if not exist out_elast mkdir out_elast
if not exist log mkdir log
for %%S in (1 2 3) do (
  START "elast_on_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 4 --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --viriale --zeta-vir --pav-com --chi-basc --polo-maturo --olon-part --calore-vett --elast-c 100 --sync-db out_elast\db_on_s%%S.pkl --db-ogni %DBOGNI% --csv out_elast\cond_on_s%%S.csv --diaglog out_elast\on_s%%S.csv > log\elast_on_s%%S.log 2>&1"
  START "elast_off_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 4 --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --viriale --zeta-vir --pav-com --chi-basc --polo-maturo --olon-part --calore-vett --elast-c 0 --sync-db out_elast\db_off_s%%S.pkl --db-ogni %DBOGNI% --csv out_elast\cond_off_s%%S.csv --diaglog out_elast\off_s%%S.csv > log\elast_off_s%%S.log 2>&1"
)
echo Test ridondanza lanciato con catena completa e DB separati: confrontare m0_coer e m0_coer_nucleo.
pause
