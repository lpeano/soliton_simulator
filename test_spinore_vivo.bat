@echo off
REM ============================================================================
REM TEST A/B SPINORE VIVO: reinnesto dell'evoluzione SU(2) (--spinore-vivo).
REM   OFF = spinore congelato all'init planare (Berry=0 per costruzione).
REM   ON  = spinore vivo, reinnestato nell'ordine ETC (legge lo snapshot t).
REM Un flag = una variabile: le due braccia differiscono SOLO per --spinore-vivo.
REM
REM Misure gauge-invarianti nel diaglog (calcolate senza coordinate):
REM   berry_spin_*            = fase di Berry (invariante di Bargmann, non-abeliano)
REM   olonomia_fase_*         = olonomia di fase sui cicli (componente armonica/vortici)
REM   circolazione_topologica_* = corrente orbitale sui cicli (curl-free -> ~0 atteso)
REM
REM DOMANDE:
REM   1) con lo spinore vivo la fase di Berry resta !=0 e coerente a run lungo,
REM      o collassa a ~0 per frustrazione (vetro di spin chirale)?
REM   2) lo spinore vivo alimenta una precessione orbitale reale (Lz_orb, m0_Lz)
REM      che era assente da congelato? Confrontare con Berry/circolazione.
REM Disciplina: 2000 passi (dopo la formazione), semi 1 e 2. Non concludere da 1 seme.
REM ============================================================================
set SIM=soliton_simulator.py
set PASSI=2000
set OGNI=10
set DBOGNI=200
set SEP=10
if not exist out_spinore mkdir out_spinore
if not exist log mkdir log

REM ---- PART 1: canale non-abeliano sul binario. Base minima (--verlet --sync). ----
REM         berry_spin (curvatura spinoriale) e circolazione (orbitale) sono gia'
REM         separati: il canale intrinseco si legge da berry_spin anche sul binario.
REM         NB: il batch semina >=2 masse (metriche di coppia), la massa singola
REM         non e' supportata dall'harness -> si usa il binario come config minima.
set BASE=--verlet --sync
set CATENA=--verlet --sync --viriale --zeta-vir --pav-com --chi-basc --polo-maturo --olon-part --calore-vett --ls-azim

REM ==== PRIMA gli ON (portano l'informazione), POI gli OFF (baseline confermativa) ====

REM ---- PART 1 ON: canale non-abeliano sul binario, base minima. ----
for %%S in (1 2) do (
  echo [part1 seed %%S] binario ON
  python %SIM% --batch --nmasse 2 --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %BASE% --spinore-vivo --sync-db out_spinore\db_m2_on_s%%S.pkl --db-ogni %DBOGNI% --csv out_spinore\cond_m2_on_s%%S.csv --diaglog out_spinore\m2_on_s%%S.csv > log\spinore_m2_on_s%%S.log 2>&1
)

REM ---- PART 2 ON: precessione, base piena + --ls-azim (che legge _nb). ----
for %%S in (1 2) do (
  echo [part2 seed %%S] precessione ON
  python %SIM% --batch --nmasse 2 --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %CATENA% --spinore-vivo --sync-db out_spinore\db_prec_on_s%%S.pkl --db-ogni %DBOGNI% --csv out_spinore\cond_prec_on_s%%S.csv --diaglog out_spinore\prec_on_s%%S.csv > log\spinore_prec_on_s%%S.log 2>&1
)

REM ---- BASELINE OFF (confermativa, solo seme 1, in coda) ----
echo [part1] binario OFF (baseline appaiata, solo seme 1)
python %SIM% --batch --nmasse 2 --sep %SEP% --seed 1 --passi %PASSI% --ogni %OGNI% %BASE% --sync-db out_spinore\db_m2_off_s1.pkl --db-ogni %DBOGNI% --csv out_spinore\cond_m2_off_s1.csv --diaglog out_spinore\m2_off_s1.csv > log\spinore_m2_off_s1.log 2>&1
echo [part2] precessione OFF (baseline appaiata, solo seme 1)
python %SIM% --batch --nmasse 2 --sep %SEP% --seed 1 --passi %PASSI% --ogni %OGNI% %CATENA% --sync-db out_spinore\db_prec_off_s1.pkl --db-ogni %DBOGNI% --csv out_spinore\cond_prec_off_s1.csv --diaglog out_spinore\prec_off_s1.csv > log\spinore_prec_off_s1.log 2>&1

echo.
echo Test spinore-vivo completato: 6 run in out_spinore\, log in log\.
echo Confronto Part 1 (off vs on): berry_spin_max/media_assoluta, olonomia_fase_*, circolazione_topologica_*.
echo Confronto Part 2 (precessione): Lz_orb_*, m0_Lz vs berry_spin/circolazione gauge-invarianti.
pause
