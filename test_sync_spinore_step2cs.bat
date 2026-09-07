@echo off
REM ============================================================================
REM RUN AGGIUNTIVO STEP 2 - candidate INSIEME: --chi-core + --cs-dinamico + --tauloc 2.0.
REM   --cs-dinamico (portata/canale metrico) implica --chi-core --spinore-vivo (regola progetto).
REM   --tauloc 2.0 = tempo proprio locale piu' dilatato (orologi de Broglie piu' dispersi in freq):
REM     stress per la soglia di Kuramoto. Moderato per limitare il rischio di instabilita' al 1o passo.
REM A/B: --sync-spinore ON vs OFF, a PARITA' di chi-core+cs-dinamico+tauloc. 3 semi, 2000 passi.
REM DOMANDA: con canale metrico + orologi piu' dilatati, la sync aggancia (m0_spin_axis_R sale in ON)?
REM Misura COVARIANTE (N appaiato). Tutti i run con --sync.
REM ============================================================================
set SIM=soliton_simulator.py
set PASSI=2000
set OGNI=10
set DBOGNI=200
set SEP=6
set PREREQ=--spinore-vivo --spinore-corretto --sync --chi-core --cs-dinamico --tauloc 2.0
if not exist log\sync_spinore_step2cs mkdir log\sync_spinore_step2cs
REM db\<campagna>\ e csv\<campagna>\ le crea il motore (auto-mkdir). log\<campagna>\ serve al redirect di shell.
REM RIPRENDIBILE: NON cancellare i .pkl/.csv. Rilanciare il .bat RIPRENDE dal --sync-db.

for %%S in (1 2 3) do (
  echo [step2 cs+tauloc seed %%S] ON
  python %SIM% --batch --nmasse 2 --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %PREREQ% --sync-spinore --sync-db db\sync_spinore_step2cs\db_on_s%%S.pkl --db-ogni %DBOGNI% --csv csv\sync_spinore_step2cs\cond_on_s%%S.csv --diaglog csv\sync_spinore_step2cs\on_s%%S.csv > log\sync_spinore_step2cs\on_s%%S.log 2>&1
)
for %%S in (1 2 3) do (
  echo [step2 cs+tauloc seed %%S] OFF
  python %SIM% --batch --nmasse 2 --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %PREREQ% --sync-db db\sync_spinore_step2cs\db_off_s%%S.pkl --db-ogni %DBOGNI% --csv csv\sync_spinore_step2cs\cond_off_s%%S.csv --diaglog csv\sync_spinore_step2cs\off_s%%S.csv > log\sync_spinore_step2cs\off_s%%S.log 2>&1
)

echo.
echo RUN AGGIUNTIVO (chi-core+cs-dinamico+tauloc 2.0) completato: db\sync_spinore_step2cs\, csv\sync_spinore_step2cs\, log\sync_spinore_step2cs\.
echo Analisi COVARIANTE ON vs OFF a N appaiato (adattare i milestone al range N effettivo).
pause
