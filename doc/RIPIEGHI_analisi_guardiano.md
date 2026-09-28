# Analisi del guardiano sui 99 confronti len(x) vs n
Blob del simulatore f7541d03, flag del driver letti dal modulo caricato. Scritta il 2026-09-28 alle 20:00, PRIMA dell'analisi manuale di Claude Code.

## 1. LEGITTIMI: estendono SOLO la coda per i nuovi, lasciano intatti gli esistenti (5)
2262 _estendi_psi_spinor · 3576 omega_s · 3583 _nb · 3620 _xi · 7009 mem_mot

## 2. DIAGNOSTICA, fuori dal passo (30)
I 30 della classe (c) di 7684ced, confermati: le funzioni sono chiamate solo da batch_condensazione, _diag_completa, _classifica_tracking, disegno e misure. Unica nota: _allaccia (3352) gira nella costruzione della scena (semina), non nel passo.

## 3. GIÀ CURATI: il ramo di scorta solleva (3)
3391 lambda_nodi · 4462 _nb_grav · _rho_sorgente (non compare nella tabella di 7684ced: da capire perché)

## 4. SOSTITUZIONI PER TUTTA LA RETE, VIVE con il driver (~30): devono diventare errore
- tempo proprio spento (dt_n = DT, r = 1 per tutti): 5280, 5344, 6000, 3461 (3461: separare l'inizializzazione None dal len != n)
- cs dinamica spenta (cs = CS_M per tutti): 3747, 4145, 5384, 5454, 5754, 7328
- densità a zero o a uno per tutti: 4084/4086, 6225, 7394
- ritmo a 4pi che ripiega sul ritmo scalare 2pi: 3477, e 5541/5545 (lo snapshot di psi_spin non si prende, e allora 3477 ripiega)
- torsione a 4pi che ripiega sul ramo 2pi: 5852 (tocca direttamente DOPPIA-COP)
- chiralità del core sostituita da perc_chi: 3680, 5715/5730
- intere leggi saltate per tutti: 5838 (spinore vivo), 2478 (feedback spinoriale), 5885 (basculamento chirale), 5911/5917 (chi da spinore), 7129/7133 (proiezione gravitazionale)
- phivel a zero per tutti: 5799
- _nb ricostruito da phi_s per tutti: 7115 (separare l'inizializzazione)
- Bloch ritardato azzerato per tutti: 5264 (andrebbe estesa la coda con nb_cur dei nuovi)
- calcola_psi a metà passo, in OR con l'inizializzazione: 2525, 3600, 3715, 7002 (separare come in lambda_nodi)

## 5. STESSA NATURA, DORMIENTI con il driver (flag spenti): 4138 (OROLOGIO_SEGNO), 5587/5592 (TEMPO_SEGNO), 5722 (VERSO_CHI), 5868 (POLO_MATURO), 7186 (LS_AZIM)

## 6. TRONCAMENTI len > n -> taglio: 2265, 3578, 3587
Se non esiste una legge che toglie nodi, non devono mai scattare: errore. Da verificare che nessuna legge tolga nodi.

## 7. Da classificare a parte
5859: cache di chi_torsione di lunghezza sbagliata -> ricalcolo a metà passo (lettura mista, non sostituzione).
5750: confronta len(d0) (ARCHI) con n (NODI): sempre vero, innocuo, ma scritto male.
2153: _aggiorna_lift_spinoriale fa return (aggiornamento saltato per tutti) con inizializzazione in OR con len < n: separare.

## 8. Proposta sulla forma della cura (DECIDE LUCA)
Non 40 raise sparsi, ma UN SOLO controllo dello schedulatore: nella fase "apri" e subito dopo mitosi, tutte le grandezze per nodo del REGISTRO hanno lunghezza n, altrimenti CacheCorta con il nome della grandezza. Poi le guardie di sostituzione si tolgono (restano solo le vere inizializzazioni, separate dall'OR). Coincide con il registro delle grandezze per nodo del riordino di T3.
