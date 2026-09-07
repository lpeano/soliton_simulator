@echo off
REM TEST RIDONDANZA: il nucleo elastico C=100 aggiunge informazione rispetto
REM al rinforzo di shear? A/B su tre semi, caso attaccato sep=4.
set SIM=soliton_simulator.py
set PASSI=4000
set OGNI=5
set DBOGNI=100
if not exist log\elast mkdir log\elast
for %%S in (1 2 3) do (
  START "elast_on_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 4 --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --viriale --zeta-vir --pav-com --chi-basc --polo-maturo --olon-part --calore-vett --elast-c 100 --sync-db db\elast\db_on_s%%S.pkl --db-ogni %DBOGNI% --csv csv\elast\cond_on_s%%S.csv --diaglog csv\elast\on_s%%S.csv > log\elast\elast_on_s%%S.log 2>&1"
  START "elast_off_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 4 --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --viriale --zeta-vir --pav-com --chi-basc --polo-maturo --olon-part --calore-vett --elast-c 0 --sync-db db\elast\db_off_s%%S.pkl --db-ogni %DBOGNI% --csv csv\elast\cond_off_s%%S.csv --diaglog csv\elast\off_s%%S.csv > log\elast\elast_off_s%%S.log 2>&1"
)
echo Test ridondanza lanciato con catena completa e DB separati: confrontare m0_coer e m0_coer_nucleo.
pause
