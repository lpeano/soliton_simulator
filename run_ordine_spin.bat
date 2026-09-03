@echo off
REM ============================================================================
REM  TEST: l'ORDINE DI SPIN a domini emerge sul lungo? (l'ultima domanda aperta)
REM  Gli spin _nb hanno accoppiamento coi vicini (B=somma vicini) ma FRUSTRATO
REM  dalla riflessione chirale (uguali -> z ribaltato). Con --chi-basc le
REM  chiralita' si organizzano in domini -> la frustrazione diventa STRUTTURATA.
REM  DOMANDA: sul lungo, gli spin si ordinano PER DOMINI (asse coerente locale)
REM           o restano isotropi (vetro di spin per sempre)?
REM  Se si ordinano -> l'L.S (--ls-azim) potrebbe poi dare precessione.
REM  Spezzabile col DB. Un seme alla volta.
REM ============================================================================
set SIM=soliton_simulator.py
set NM=3
set SEP=8
set PASSI=20000
set OGNI=5
set DBOGNI=100
set SEMI=1

if not exist out_spin mkdir out_spin
if not exist log       mkdir log

echo === ORDINE DI SPIN con chi-basc (seme %SEMI%, %PASSI% passi) ===
echo.

for %%S in (%SEMI%) do (
  START "spin_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --sync --chi-basc --sync-db out_spin\db_spin_s%%S.pkl --db-ogni %DBOGNI% --csv out_spin\cond_spin_s%%S.csv --diaglog out_spin\diag_spin_s%%S.csv > log\spin_s%%S.log 2>&1"
)

echo Lanciato. Al ritorno guardo: lo spinore si ordina (verso azim coerente) nel tempo?
echo Nel diaglog c'e' gia' l'ordine di spin ('sp' = angolo medio). Spezzabile col DB.
echo Altri semi: SEMI=1 -> 2 -> 3.
