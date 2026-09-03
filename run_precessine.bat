@echo off
REM ============================================================================
REM  IL RUN DELLA PRECESSIONE — mette insieme tutto il lavoro:
REM   - freno anisotropo (--zeta-vir): il CREATORE di verso (valvola)
REM   - pavimento comovente (--pav-com): niente muro assoluto che falsa
REM   - misura pulita: rcom_ (raggio COMOVENTE dai baricentri) e s2_medio
REM     nei diaglog -> testa la legge   R ~ s2^(2/3)/(1-s2)
REM  Tre condizioni per seme, tutte con pavimento comovente:
REM    base : niente
REM    vir  : solo viriale
REM    virz : viriale + freno anisotropo   <-- il candidato
REM  DOMANDA: virz fa comparire Lz_orb concorde? e rcom segue s2^(2/3)/(1-s2)?
REM ============================================================================
set SIM=soliton_simulator.py
set NM=3
set SEP=16
set PASSI=20000
set OGNI=5
set SEMI=1 2 3

if not exist out_prec  mkdir out_prec
if not exist out_video mkdir out_video
if not exist log        mkdir log

echo === RUN PRECESSIONE (%NM% masse, %PASSI% passi, semi %SEMI%) ===
echo     pavimento comovente ovunque; misura rcom + s2 nei diaglog
echo.

for %%S in (%SEMI%) do (
  START "base_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --sync --kfrange 0 --pav-com                       --csv out_prec\cond_base_s%%S.csv --diaglog out_prec\diag_base_s%%S.csv > log\base_s%%S.log 2>&1"
  START "vir_s%%S"  /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --sync --kfrange 0 --pav-com --viriale            --csv out_prec\cond_vir_s%%S.csv  --diaglog out_prec\diag_vir_s%%S.csv  > log\vir_s%%S.log 2>&1"
  START "virz_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --sync --kfrange 0 --pav-com --viriale --zeta-vir --csv out_prec\cond_virz_s%%S.csv --diaglog out_prec\diag_virz_s%%S.csv > log\virz_s%%S.log 2>&1"
)

START "video_virz_s1" /MIN cmd /c "python %SIM% --test N-MASSE --nmasse %NM% --sep %SEP% --seed 1 --giri 0 --ppf 1 --frames %PASSI% --fps 24 --size 0.7,0.7,0.7 --sync --kfrange 0 --pav-com --viriale --zeta-vir --out out_video\video_virz_s1.mp4 > log\video_virz_s1.log 2>&1"

echo Lanciati. Diaglog in out_prec\, video in out_video\, log in log\.
echo Al ritorno: leggo Lz_orb (concorde?), rcom_ vs s2_medio (segue s2^(2/3)/(1-s2)?).
echo Se troncano: set SEMI=1 e rilancia, poi 2, poi 3.