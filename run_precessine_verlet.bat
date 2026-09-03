@echo off
REM Variante Velocity-Verlet del test di precessione.
set SIM=soliton_simulator.py
set PASSI=20000
set OGNI=5
set SEMI=1 2 3
if not exist out_prec mkdir out_prec
if not exist log mkdir log
for %%S in (%SEMI%) do (
 START "base_verlet_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 16 --seed %%S --passi %PASSI% --ogni %OGNI% --kfrange 0 --pav-com --verlet --csv out_prec\cond_base_verlet_s%%S.csv --diaglog out_prec\diag_base_verlet_s%%S.csv > log\base_prec_verlet_s%%S.log 2>&1"
 START "vir_verlet_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 16 --seed %%S --passi %PASSI% --ogni %OGNI% --kfrange 0 --pav-com --viriale --verlet --csv out_prec\cond_vir_verlet_s%%S.csv --diaglog out_prec\diag_vir_verlet_s%%S.csv > log\vir_prec_verlet_s%%S.log 2>&1"
 START "virz_verlet_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 16 --seed %%S --passi %PASSI% --ogni %OGNI% --kfrange 0 --pav-com --viriale --zeta-vir --verlet --csv out_prec\cond_virz_verlet_s%%S.csv --diaglog out_prec\diag_virz_verlet_s%%S.csv > log\virz_prec_verlet_s%%S.log 2>&1"
)
echo Test precessione Velocity-Verlet lanciato.
pause
