@echo off
REM ============================================================================
REM CAMPAGNA B (test-GRATIS del guardiano): la DE-PARAM da sola ordina il SEGNO?
REM   Ipotesi (piu' profonda di sync-fase-orologio): la frustrazione nasce dagli
REM   orologi che si SFASANO (frequenze rho*r troppo disperse). La de-param riduce
REM   la dispersione del ~95% (corr(omega_clk,deg) 0.948 -> ~0) -> orologi a
REM   frequenze simili -> potrebbero NON sfasarsi piu' -> il SEGNO resta coerente
REM   DA SOLO, senza alcun sync esplicito. Se e' cosi', la de-param sola risolve.
REM
REM A/B: --deparam-orologio ON vs OFF, a parita' di tutto. Minimo freddo
REM   (--spinore-vivo --spinore-corretto --sync). 3 semi, 2000 passi, sep 6.
REM   Un flag = una variabile (solo la de-param cambia).
REM
REM MISURA (dal diaglog, COVARIANTE): m0_spin_axis_R = il SEGNO nel nucleo, l'unica
REM   osservabile CERTIFICATA dt-indipendente (§36). Leggere a N APPAIATO su 3 semi,
REM   oltre il rumore fra semi (NON il "+0.011" su 1 seme).
REM   -> de-param ON alza m0_spin_axis_R concorde su 3 semi, oltre il rumore =
REM      la dispersione era il muro, abbattuto -> vicinissimi allo spin 1/2.
REM   -> nessun cambiamento = la de-param sola non basta -> serve --sync-fase-orologio (A).
REM
REM Fondamenta gia' pulite (§35/§36): condensazione sanata (--ogni neutro), diaglog
REM   puro, orologio pura-fase (non tocca la gravita', sigillo nb 6.7e-16).
REM RIPRENDIBILE: NON cancellare i .pkl/.csv; rilanciare il .bat riprende dal --sync-db.
REM ============================================================================
set SIM=soliton_simulator.py
set PASSI=2000
set OGNI=100
set DBOGNI=200
set SEP=6
set PREREQ=--spinore-vivo --spinore-corretto --sync
if not exist log\deparam_segno mkdir log\deparam_segno
REM db\deparam_segno\ e csv\deparam_segno\ le crea il motore (auto-mkdir). log\ serve al redirect di shell.

REM ==== ON: de-param ATTIVA (orologio relazionale pura-fase) ====
for %%S in (1 2 3) do (
  echo [deparam-segno seed %%S] ON (de-param)
  python %SIM% --batch --nmasse 2 --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %PREREQ% --deparam-orologio --sync-db db\deparam_segno\db_on_s%%S.pkl --db-ogni %DBOGNI% --csv csv\deparam_segno\cond_on_s%%S.csv --diaglog csv\deparam_segno\on_s%%S.csv > log\deparam_segno\on_s%%S.log 2>&1
)
REM ==== OFF: baseline SENZA de-param (orologio estensivo/globale legacy) ====
for %%S in (1 2 3) do (
  echo [deparam-segno seed %%S] OFF (baseline)
  python %SIM% --batch --nmasse 2 --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %PREREQ% --sync-db db\deparam_segno\db_off_s%%S.pkl --db-ogni %DBOGNI% --csv csv\deparam_segno\cond_off_s%%S.csv --diaglog csv\deparam_segno\off_s%%S.csv > log\deparam_segno\off_s%%S.log 2>&1
)

echo.
echo CAMPAGNA B completata: 6 run in db\deparam_segno\ csv\deparam_segno\ log\deparam_segno\.
echo Analisi COVARIANTE (N appaiato), de-param ON vs OFF su 3 semi, sul SEGNO certificato:
echo   python analisi_covariante.py m0_spin_axis_R csv\deparam_segno\on_s1.csv csv\deparam_segno\off_s1.csv
echo   (ripetere per s2, s3; verdetto: ON > OFF concorde su 3 semi e oltre il rumore fra semi?)
pause
