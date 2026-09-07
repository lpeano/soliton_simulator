@echo off
REM ============================================================================
REM RUN AGGIUNTIVO - come step2cs (--chi-core --cs-dinamico --tauloc 2.0) MA con
REM   --scuotimento: regime deterministico + RIBOLLIO DEL VUOTO forzato ON.
REM   La dinamica resta deterministica; il vuoto pero' ribolle (temperatura) ->
REM   piu' rumore/agitazione = stress ulteriore per la soglia di Kuramoto.
REM A/B: --sync-spinore ON vs OFF, a PARITA' di chi-core+cs-dinamico+tauloc+scuotimento.
REM DOMANDA: col vuoto ribollente la sync aggancia meglio (annealing/eccitazione aiuta a
REM   uscire da minimi frustrati) o peggio (troppo caldo per il Kuramoto)? 3 semi, 2000 passi.
REM Misura COVARIANTE (N appaiato). Tutti i run con --sync.
REM ============================================================================
set SIM=soliton_simulator.py
set PASSI=2000
set OGNI=10
set DBOGNI=200
set SEP=6
set PREREQ=--spinore-vivo --spinore-corretto --sync --chi-core --cs-dinamico --tauloc 2.0 --scuotimento
if not exist out_sync_spinore_step2cssc mkdir out_sync_spinore_step2cssc
if not exist log mkdir log
REM RIPRENDIBILE: NON cancellare i .pkl/.csv. Rilanciare il .bat RIPRENDE dal --sync-db.

for %%S in (1 2 3) do (
  echo [step2 cs+tauloc+scuoti seed %%S] ON
  python %SIM% --batch --nmasse 2 --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %PREREQ% --sync-spinore --sync-db out_sync_spinore_step2cssc\db_on_s%%S.pkl --db-ogni %DBOGNI% --csv out_sync_spinore_step2cssc\cond_on_s%%S.csv --diaglog out_sync_spinore_step2cssc\on_s%%S.csv > log\sync_step2cssc_on_s%%S.log 2>&1
)
for %%S in (1 2 3) do (
  echo [step2 cs+tauloc+scuoti seed %%S] OFF
  python %SIM% --batch --nmasse 2 --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %PREREQ% --sync-db out_sync_spinore_step2cssc\db_off_s%%S.pkl --db-ogni %DBOGNI% --csv out_sync_spinore_step2cssc\cond_off_s%%S.csv --diaglog out_sync_spinore_step2cssc\off_s%%S.csv > log\sync_step2cssc_off_s%%S.log 2>&1
)

echo.
echo RUN AGGIUNTIVO (chi-core+cs-dinamico+tauloc 2.0 + scuotimento) completato: 6 run in out_sync_spinore_step2cssc\.
echo Analisi COVARIANTE ON vs OFF a N appaiato (adattare i milestone al range N effettivo).
pause
