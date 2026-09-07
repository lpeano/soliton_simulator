@echo off
REM ============================================================================
REM STEP 2 (candidate UNA ALLA VOLTA) - prima candidata: --chi-core.
REM Parte dal minimo freddo (PREREQ) e AGGIUNGE una sola candidata di classe B:
REM   --chi-core = riferimento chirale locale (il settore SU(2) usa chiralita_core_locale()).
REM A/B: --sync-spinore ON vs OFF, a PARITA' di --chi-core. Un flag = una variabile.
REM DOMANDA: --chi-core da' il CANALE che fa propagare la sync (m0_spin_axis_R sale in ON)
REM   o e' inerte/contrasta (come al minimo freddo, dove la sync era NEGATIVA)?
REM Misura COVARIANTE (N appaiato): m0_spin_axis_R, m0_omega_axis_R, m0_spin_core_cv.
REM Disciplina: 2000 passi, 3 semi, regime freddo, tutti i run con --sync.
REM ============================================================================
set SIM=soliton_simulator.py
set PASSI=2000
set OGNI=10
set DBOGNI=200
set SEP=6
set PREREQ=--spinore-vivo --spinore-corretto --sync --chi-core
if not exist log\sync_spinore_step2 mkdir log\sync_spinore_step2
REM db\<campagna>\ e csv\<campagna>\ le crea il motore (auto-mkdir). log\<campagna>\ serve al redirect di shell.
REM RIPRENDIBILE: NON cancellare i .pkl/.csv. Rilanciare il .bat RIPRENDE dal --sync-db.

for %%S in (1 2 3) do (
  echo [step2 chi-core seed %%S] ON
  python %SIM% --batch --nmasse 2 --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %PREREQ% --sync-spinore --sync-db db\sync_spinore_step2\db_on_s%%S.pkl --db-ogni %DBOGNI% --csv csv\sync_spinore_step2\cond_on_s%%S.csv --diaglog csv\sync_spinore_step2\on_s%%S.csv > log\sync_spinore_step2\on_s%%S.log 2>&1
)
for %%S in (1 2 3) do (
  echo [step2 chi-core seed %%S] OFF
  python %SIM% --batch --nmasse 2 --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %PREREQ% --sync-db db\sync_spinore_step2\db_off_s%%S.pkl --db-ogni %DBOGNI% --csv csv\sync_spinore_step2\cond_off_s%%S.csv --diaglog csv\sync_spinore_step2\off_s%%S.csv > log\sync_spinore_step2\off_s%%S.log 2>&1
)

echo.
echo STEP 2 (chi-core) completato: 6 run: db in db\, csv in csv\, log in log\.
echo Analisi COVARIANTE ON vs OFF a N appaiato (adattare i milestone al range N effettivo).
pause
