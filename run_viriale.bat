@echo off
REM =============================================================================
REM  run_viriale.bat - A/B della CONVERSIONE VIRIALE, UNA LEVA SOLA.
REM  Windows. Lancia dalla cartella con soliton_simulator.py:  run_viriale.bat
REM
REM  Domanda del test: la spinta radiale, RIPARTITA fra cadere (cos^2) e girare
REM  (sin^2) invece che additiva, FERMA il collasso? A differenza di K_FRANGE
REM  (additivo -> iniettava -> destabilizzava), --viriale e' conservativa
REM  (budget |grav| invariato, verificato a 1e-16). Zero parametri: l'angolo
REM  fra pozzo e flusso di fase fa da ripartitore.
REM
REM  ISOLAMENTO (guardiano): K_FRANGE=0 e zeta-loc OFF in ENTRAMBI i rami.
REM  L'unica differenza e' --viriale. Una leva alla volta.
REM
REM  CRITERIO PRIMARIO (nuovo): non solo Lz_orb, ma r_com FINALE e tempo di
REM  collasso. Precessione vera <=> il collasso si arresta (barriera centrifuga):
REM  se ON, r_com si ferma a un valore finito invece di andare a ~0.3 = ORBITA.
REM  Prova nei diaglog, finestra pre-collasso, verso/effetto CONCORDE su >=3 semi.
REM  Etichetta: --viriale e' LEGGE (zero parametri), ma il RISULTATO e' in-verifica
REM  finche' non e' replicato.
REM
REM  CARICO: 6 batch + 2 video = 8 processi. Riduci SEMI o commenta i video se serve.
REM =============================================================================

setlocal
set SIM=soliton_simulator.py
set NM=3
set SEP=16
set PASSI=20000
set FRAMES=20000
set FPS=24
set OGNI=5
set SEMI=1 2 3

if not exist out_vir   mkdir out_vir
if not exist out_video mkdir out_video
if not exist log        mkdir log

echo === A/B conversione VIRIALE (K_FRANGE=0, zeta-loc OFF in entrambi) ===
echo     %NM% masse, sep %SEP%, %PASSI% passi ^| normale vs --viriale ^| semi: %SEMI%
echo     Criterio: r_com finale (il collasso si ferma?). Log in .\log\
echo.

REM ================= BATCH: la PROVA (CSV + diaglog) su TUTTI i semi =================
for %%S in (%SEMI%) do (
  START "voff_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --kfrange 0            --csv out_vir\cond_voff_s%%S.csv --diaglog out_vir\diag_voff_s%%S.csv > log\voff_s%%S.log 2>&1"
  START "von_s%%S"  /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --kfrange 0 --viriale  --csv out_vir\cond_von_s%%S.csv  --diaglog out_vir\diag_von_s%%S.csv  > log\von_s%%S.log 2>&1"
)

REM ================= VIDEO: l'OCCHIO (camera FISSA), seed 1, off + on =================
START "video_voff_s1" /MIN cmd /c "python %SIM% --test N-MASSE --nmasse %NM% --sep %SEP% --seed 1 --giri 0 --ppf 1 --frames %FRAMES% --fps %FPS% --size 0.7,0.7,0.7 --kfrange 0           --out out_video\video_voff_s1.mp4 > log\video_voff_s1.log 2>&1"
START "video_von_s1"  /MIN cmd /c "python %SIM% --test N-MASSE --nmasse %NM% --sep %SEP% --seed 1 --giri 0 --ppf 1 --frames %FRAMES% --fps %FPS% --size 0.7,0.7,0.7 --kfrange 0 --viriale --out out_video\video_von_s1.mp4 > log\video_von_s1.log 2>&1"

echo.
echo === Lanciati. Risultati in out_vir\ (CSV+diaglog), out_video\, log\ ===
echo     Guarda soprattutto: r_com (da dist_01/02/12) FINALE, von vs voff.
echo     Se von si ferma a un raggio finito e voff va a ~0 -> il collasso si arresta.
pause
endlocal
