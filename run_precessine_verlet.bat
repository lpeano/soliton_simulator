@echo off
REM Variante Velocity-Verlet del test di precessione.
set SIM=soliton_simulator.py
set PASSI=20000
set OGNI=5
set SEMI=1 2 3
if not exist log\prec mkdir log\prec
for %%S in (%SEMI%) do (
 START "base_verlet_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 16 --seed %%S --passi %PASSI% --ogni %OGNI% --sync --kfrange 0 --pav-com --verlet --csv csv\prec\cond_base_verlet_s%%S.csv --diaglog csv\prec\diag_base_verlet_s%%S.csv > log\prec\base_prec_verlet_s%%S.log 2>&1"
 START "vir_verlet_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 16 --seed %%S --passi %PASSI% --ogni %OGNI% --sync --kfrange 0 --pav-com --viriale --verlet --csv csv\prec\cond_vir_verlet_s%%S.csv --diaglog csv\prec\diag_vir_verlet_s%%S.csv > log\prec\vir_prec_verlet_s%%S.log 2>&1"
 START "virz_verlet_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 16 --seed %%S --passi %PASSI% --ogni %OGNI% --sync --kfrange 0 --pav-com --viriale --zeta-vir --verlet --csv csv\prec\cond_virz_verlet_s%%S.csv --diaglog csv\prec\diag_virz_verlet_s%%S.csv > log\prec\virz_prec_verlet_s%%S.log 2>&1"
)
echo Test precessione Velocity-Verlet lanciato.
pause
