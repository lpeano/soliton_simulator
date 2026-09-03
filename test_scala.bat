@echo off
REM TEST INVARIANZA DI SCALA: stessa legge C=100 a due numeri di masse.
set SIM=soliton_simulator.py
set PASSI=4000
set OGNI=5
if not exist out_elast mkdir out_elast
if not exist log mkdir log
START "scala_piccola" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 4 --seed 1 --passi %PASSI% --ogni %OGNI% --verlet --elast-c 100 --csv out_elast\cond_scala_piccola.csv --diaglog out_elast\scala_piccola.csv > log\scala_piccola.log 2>&1"
START "scala_grande" /MIN cmd /c "python %SIM% --batch --nmasse 6 --sep 4 --seed 1 --passi %PASSI% --ogni %OGNI% --verlet --elast-c 100 --csv out_elast\cond_scala_grande.csv --diaglog out_elast\scala_grande.csv > log\scala_grande.log 2>&1"
echo Test invarianza di scala lanciato: confrontare osservabili normalizzate.
pause
