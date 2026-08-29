@echo off
REM =============================================================================
REM  run_zetaloc.bat - A/B dello SMORZAMENTO LOCALE (ZETA_LOC), UNA LEVA SOLA.
REM  Windows. Lancia dalla cartella con soliton_simulator.py:  run_zetaloc.bat
REM
REM  Domanda del test: lo smorzamento fisso ZETA_M=0.75 STA SOFFOCANDO la
REM  precessione nativa? Con --zeta-loc lo smorzamento scende nella materia
REM  (dove rho > mediana) e resta pieno nel vuoto: se la circolazione era frenata,
REM  ora dovrebbe sopravvivere e Lz_orb crescere -- SENZA nemmeno K_FRANGE.
REM
REM  ISOLAMENTO (guardiano): K_FRANGE=0 in ENTRAMBI i rami. L'unica differenza e'
REM  lo smorzamento. Cosi' si misura l'effetto del FRENO sulla precessione nativa,
REM  non confuso col canale orbitale. Una leva alla volta.
REM
REM  REGOLE FERREE: prova nei diaglog (Lz_orb), finestra PRE-COLLASSO, verso
REM  CONCORDE su >=3 semi. --zeta-loc e' un interruttore on/off (nessun numero
REM  nuovo: e' una LEGGE, zeta modulato da rho/mediana). Ma il RISULTATO resta
REM  in-verifica finche' non e' replicato.
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

if not exist out_zeta  mkdir out_zeta
if not exist out_video mkdir out_video
if not exist log        mkdir log

echo === A/B smorzamento locale ZETA_LOC (K_FRANGE SPENTO in entrambi) ===
echo     %NM% masse, sep %SEP%, %PASSI% passi ^| zeta fisso vs zeta-loc ^| semi: %SEMI%
echo.

REM ================= BATCH: la PROVA (CSV + diaglog), K_FRANGE=0 sempre =================
for %%S in (%SEMI%) do (
  START "zoff_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --kfrange 0                 --csv out_zeta\cond_zoff_s%%S.csv --diaglog out_zeta\diag_zoff_s%%S.csv > log\zoff_s%%S.log 2>&1"
  START "zon_s%%S"  /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --kfrange 0 --zeta-loc       --csv out_zeta\cond_zon_s%%S.csv  --diaglog out_zeta\diag_zon_s%%S.csv  > log\zon_s%%S.log 2>&1"
)

REM ================= VIDEO: l'OCCHIO (camera FISSA), seed 1, off + on =================
START "video_zoff_s1" /MIN cmd /c "python %SIM% --test N-MASSE --nmasse %NM% --sep %SEP% --seed 1 --giri 0 --ppf 1 --frames %FRAMES% --fps %FPS% --size 0.7,0.7,0.7 --kfrange 0           --out out_video\video_zoff_s1.mp4 > log\video_zoff_s1.log 2>&1"
START "video_zon_s1"  /MIN cmd /c "python %SIM% --test N-MASSE --nmasse %NM% --sep %SEP% --seed 1 --giri 0 --ppf 1 --frames %FRAMES% --fps %FPS% --size 0.7,0.7,0.7 --kfrange 0 --zeta-loc --out out_video\video_zon_s1.mp4 > log\video_zon_s1.log 2>&1"

echo.
echo === Lanciati. Risultati in out_zeta\ (CSV+diaglog), out_video\, log\ ===
pause
endlocal
