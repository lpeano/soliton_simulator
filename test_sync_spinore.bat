@echo off
REM ============================================================================
REM TEST --sync-spinore : SCALA "minimo freddo" (metodo del guardiano).
REM   NON accendere tutti gli switch insieme: nasconde piu' di quanto rivela.
REM   Classi rispetto all'effetto SINCRONIZZAZIONE:
REM     A PREREQUISITI  : --spinore-vivo --spinore-corretto --sync  (gli orologi + ETC)
REM     B CANDIDATE     : --cs-dinamico, --chi-core, --guscio-morbido (una alla volta, STEP 2)
REM     C RUMORE/PERTURB: --calore-vett, --plast-din, --polo-maturo, --olon-part,
REM                       --ls-azim, --verso-chi (DISORDINANO: fuori dal minimo freddo)
REM
REM STEP 1 - MINIMO FREDDO: SOLO prerequisiti, ambiente pulito e freddo (regime
REM   deterministico default: SCUOTIMENTO=off, solo calcio iniziale). A/B: --sync-spinore
REM   ON vs OFF, a parita' di tutto il resto. 3 semi. Un flag = una variabile.
REM
REM MISURA (dal diaglog, gauge-invariante) - NON concludere da soli:
REM   spin_cluster_modulo (S_M)   -> sale verso 1 con ON? (spin allineati)
REM   berry_spin_* firmata/assoluta-> sale (coerente) o resta ~0 (frustrato)?
REM   dispersione omega_s / assi   -> cala con ON? (orologi sincronizzati)
REM   Leggere COVARIANTE: a N appaiato (analisi_covariante.py), non a passo fisso.
REM
REM   -> Se S_M/Berry salgono concordi su 3 semi: la sync FUNZIONA (isolata) -> STEP 2.
REM   -> Se non salgono: e' la sync stessa o la soglia di Kuramoto (troppo disordine),
REM      e lo SAI, perche' era il minimo, non altri switch.
REM Disciplina: 2000 passi (dopo la formazione), 3 semi. ON prima, OFF baseline dopo.
REM ============================================================================
set SIM=soliton_simulator.py
set PASSI=2000
set OGNI=10
set DBOGNI=200
set SEP=6
REM PREREQUISITI (classe A) soltanto: nessuno switch di classe B o C.
set PREREQ=--spinore-vivo --spinore-corretto --sync
if not exist out_sync_spinore mkdir out_sync_spinore
if not exist log mkdir log
REM RIPRENDIBILE: NON cancellare i .pkl/.csv. Se un run e' interrotto, rilanciare questo .bat
REM RIPRENDE dal --sync-db (il sim carica lo stato, fa i passi rimanenti, appende il diaglog).
REM Per ripartire PULITI: cancellare a mano la cartella, o passare --db-cleanup ai singoli run.

REM ==== PRIMA gli ON (portano l'informazione), POI gli OFF (baseline confermativa) ====
for %%S in (1 2 3) do (
  echo [sync-spinore seed %%S] minimo freddo ON
  python %SIM% --batch --nmasse 2 --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %PREREQ% --sync-spinore --sync-db out_sync_spinore\db_on_s%%S.pkl --db-ogni %DBOGNI% --csv out_sync_spinore\cond_on_s%%S.csv --diaglog out_sync_spinore\on_s%%S.csv > log\sync_spinore_on_s%%S.log 2>&1
)
for %%S in (1 2 3) do (
  echo [sync-spinore seed %%S] minimo freddo OFF
  python %SIM% --batch --nmasse 2 --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %PREREQ% --sync-db out_sync_spinore\db_off_s%%S.pkl --db-ogni %DBOGNI% --csv out_sync_spinore\cond_off_s%%S.csv --diaglog out_sync_spinore\off_s%%S.csv > log\sync_spinore_off_s%%S.log 2>&1
)

echo.
echo STEP 1 completato: 6 run in out_sync_spinore\, log in log\.
echo Analisi COVARIANTE (a N appaiato), ON vs OFF su 3 semi:
echo   python analisi_covariante.py spin_cluster_modulo out_sync_spinore\on_s1.csv out_sync_spinore\off_s1.csv
echo   (ripetere per berry_spin_media_assoluta e per la dispersione di omega/assi)
echo Attento alla SOGLIA di Kuramoto: puo' sincronizzare il nucleo (denso, frequenze simili)
echo ma non il guscio (rado, frequenze disperse) - e' un risultato, va LETTO non forzato.
pause
