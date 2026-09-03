@echo off
REM ============================================================================
REM TEST A/B SPINORE VIVO + PLASTICITA' DINAMICA (--spinore-vivo --plast-din).
REM Copia di test_spinore_vivo.bat con IN PIU' la legge di plasticita' metrica
REM dinamica (--plast-din): alla mitosi il d0 dei nuovi archi riceve un offset
REM plastico emergente da stress metrico ed eccesso di torsione (zero parametri).
REM
REM CONFRONTO: out_spinore_plastdin (questo) vs out_spinore (campagna base).
REM   Entrambi hanno --spinore-vivo; differiscono SOLO per --plast-din -> isola
REM   l'effetto della plasticita' dinamica sull'ordine di spin emergente.
REM
REM Misure: berry_spin_*, spin_cluster_modulo (S_M), spin_cluster_omega (omega_S),
REM   olonomia_fase_*, circolazione_topologica_*, piu' scala/metrica: d0_mean/max,
REM   stress, dil, m0_raggio, scala_com (per vedere dove/quanto genera volume).
REM
REM DOMANDE:
REM   1) la plasticita' dinamica cambia S_M / omega_S rispetto alla base?
REM      (l'ordine di spin dipende dalla geometria che si rilassa?)
REM   2) genera volume dove c'e' tensione: d0_max sale, stress metrico cala?
REM Disciplina: 2000 passi, semi 1 e 2. Non concludere da 1 seme.
REM ============================================================================
set SIM=soliton_simulator.py
set PASSI=2000
set OGNI=10
set DBOGNI=200
set SEP=10
set OUT=out_spinore_plastdin
if not exist %OUT% mkdir %OUT%
if not exist log mkdir log

set BASE=--verlet --sync --plast-din
set CATENA=--verlet --sync --plast-din --viriale --zeta-vir --pav-com --chi-basc --polo-maturo --olon-part --calore-vett --ls-azim

REM ==== PRIMA gli ON (portano l'informazione), POI gli OFF (baseline confermativa) ====

REM ---- PART 1 ON: canale non-abeliano sul binario, base minima + plast-din. ----
for %%S in (1 2) do (
  echo [part1 seed %%S] binario ON (plast-din)
  python %SIM% --batch --nmasse 2 --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %BASE% --spinore-vivo --sync-db %OUT%\db_m2_on_s%%S.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_m2_on_s%%S.csv --diaglog %OUT%\m2_on_s%%S.csv > log\pd_m2_on_s%%S.log 2>&1
)

REM ---- PART 2 ON: precessione, base piena + --ls-azim + plast-din. ----
for %%S in (1 2) do (
  echo [part2 seed %%S] precessione ON (plast-din)
  python %SIM% --batch --nmasse 2 --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %CATENA% --spinore-vivo --sync-db %OUT%\db_prec_on_s%%S.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_prec_on_s%%S.csv --diaglog %OUT%\prec_on_s%%S.csv > log\pd_prec_on_s%%S.log 2>&1
)

REM ---- BASELINE OFF-plast (spinore congelato ma plast-din attivo, solo seme 1) ----
echo [part1] binario OFF-spinore (plast-din, baseline, seme 1)
python %SIM% --batch --nmasse 2 --sep %SEP% --seed 1 --passi %PASSI% --ogni %OGNI% %BASE% --sync-db %OUT%\db_m2_off_s1.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_m2_off_s1.csv --diaglog %OUT%\m2_off_s1.csv > log\pd_m2_off_s1.log 2>&1
echo [part2] precessione OFF-spinore (plast-din, baseline, seme 1)
python %SIM% --batch --nmasse 2 --sep %SEP% --seed 1 --passi %PASSI% --ogni %OGNI% %CATENA% --sync-db %OUT%\db_prec_off_s1.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_prec_off_s1.csv --diaglog %OUT%\prec_off_s1.csv > log\pd_prec_off_s1.log 2>&1

echo.
echo Test spinore-vivo + plast-din completato: 6 run in %OUT%\, log in log\ (pd_*).
echo Confronto vs base: S_M, omega_S, berry_spin_* (out_spinore_plastdin vs out_spinore).
echo Metrica/volume: d0_mean/d0_max, stress, dil, m0_raggio, scala_com.
pause
