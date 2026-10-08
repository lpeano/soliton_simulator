# ⛔ **SOSTITUITO** — *questo documento non e' piu' la fonte* *(2026-10-08)*

> ### ⛔ **L'ELENCO QUI SOTTO ERA FATTO CON UN'EURISTICA A PAROLE CHIAVE, e ha sbagliato.**
> La verifica del guardiano su tutte le `953` voci ha trovato che ### **circa `50` delle `86`
> «METODO» erano fisica dell'era `1`**, e che ### **circa `45` lezioni di metodo erano state
> sospese.**
>
> ### ➜ **LA FONTE ADESSO SONO LE LISTE ESPLICITE DI LUCA**, applicate una per una dalla
> migrazione allo schema `2`:
>
> | | |
> |---|---|
> | la ### **traccia** di ogni ID vecchio | ### **`doc/indice/migrazione_era1.jsonl`** |
> | le voci e i loro campi | `doc/indice/voci.jsonl` |
> | il ### **referto** | `doc/REFERTO_indice_v2.md` |
> | come si interroga | `python csv/indice.py cerca --dominio METODO` |
>
> ### ⚠ **NON si cancella** *(par.5: niente `rm`)*: ### **resta leggibile come il reperto di
> un errore**, e il suo errore e' ### **il motivo per cui lo schema `2` esiste.**

---

# LE LEZIONI DI METODO — **NON si sospendono, e Luca lo confermi**

> ### ⛔ **Le voci qui sotto NON hanno ricevuto `SOSPESA-ERA-1`:** sono ### **lezioni di METODO**, e valgono anche nell'era `2`.
>
> ### ⚠ **LA CLASSIFICAZIONE E' UN'EURISTICA, e per questo l'elenco e' qui:** `tipo` in *(``presidio`, `standard`, `assioma``)* oppure una ### **parola del metodo** nel titolo o nello `stato_da`. ### ➜ **Luca lo conferma o lo corregge.**

| | |
|---|--:|
| voci dell'indice | `953` |
| in gioco *(aperto / da-decidere / `IN CODA`)* | `715` |
| ### **SOSPESE** *(fisica)* | ### **`629`** |
| ### **NON sospese** *(metodo)* | ### **`86`** |
| ### ⛔ **bloccanti fra le SOSPESE** | ### **`8`** |

## **L'ELENCO, da confermare**

| id | tipo | ### **perche' METODO** | titolo |
|---|---|---|---|
| `A1-COSTANTI` | `altro` | la parola *«finestra»* | AUDIT DELLE COSTANTI TARATE — 90 commenti «misurato/tarato» nel sorgente. Si separano le... |
| `CLIP-INVENTARIO` | `altro` | la parola *«argv del driver»* | INVENTARIO dei clip, tetti e pavimenti del passo pieno: 27 TETTI FISICI su 117 guardie |
| `FRECCE-IMPOSTE` | `altro` | la parola *«argv del driver»* | il censimento delle leggi che impongono una direzione nel tempo: NOVE, e DUE curabili prima |
| `MASSA-ID` | `altro` | la parola *«caso che deve fallire»* | le masse si identificano con l'ID di massa (conc_nodi), non coi nodi del passo 0 ne' con la  |
| `MEMORIE-MANCANTI` | `altro` | la parola *«falso positivo»* | il rapporto sulle memorie: il censimento dello stato, il bilancio, e le memorie candidate |
| `PASSO-1` | `altro` | la parola *«inventario»* | IL PASSO NON È step(): SONO CINQUE CHIAMATE, e 24 script sotto csv/ avanzano in modo INCOMPL |
| `PASSO-PIENO` | `altro` | la parola *«ricopiat»* | un hook che rifiuta uno script che avanza con net.step() invece di csv/_passo.py passo_pieno |
| `PRESTAZIONI-CORSE` | `altro` | la parola *«ricopiat»* | le corse costano: sei strade per il tempo di calcolo, da affrontare a modello STABILE |
| `VIDEO-SCENA` | `altro` | la parola *«finestra»* | il video della scena del pilota: diagnostico, mostra `pos` che NON e' la distanza fisica |
| `W5` | `altro` | la parola *«p3»* | CRITERIO di POZZO-D: A/B nel driver, scena (ii)(a), 4 semi, 120 passi, con la barra fra semi |
| `COMPONENTI:B11` | `criterio-locale` | la parola *«controllo positivo»* | --cs-dinamico / sì (cs = CSM/(1+GAMMA√I), stesso GAMMA di G(rho)) / A/B storico; nessun... |
| `COMPONENTI:C3` | `criterio-locale` | la parola *«argv del driver»* | --regime (deterministico, ecc.) / cambia quattro interruttori insieme (TAUA, GPH, CALOREINIT |
| `COMPONENTI:S3` | `criterio-locale` | la parola *«controllo positivo»* | S3.0 / IL CONTROLLO POSITIVO: il test VEDE l'effetto / 39/40 nodi con \/f(1)−f(0)\/ 1e-13 |
| `ESENTE-P3` | `criterio-locale` | la parola *«p3»* | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task... [ESENTE |
| `REGISTRO_FISICA:A4` | `criterio-locale` | la parola *«p3»* | contrasto massa/vuoto e Lam al passo 1, contro P2 = 27 e P3 = 5 |
| `REGISTRO_FISICA:A5` | `criterio-locale` | la parola *«controllo positivo»* | CONTROLLO POSITIVO: ON e OFF DEVONO differire |
| `REGISTRO_FISICA:A6` | `criterio-locale` | la parola *«caso che deve fallire»* | CASO CHE DEVE FALLIRE: con maturi=False forzato, A2 deve dare FAIL |
| `REGISTRO_FISICA:E3` | `criterio-locale` | la parola *«finestra»* | E3 la finestra di D33 / mio / si riporta la popolazione delle due finestre nei due bracci /  |
| `REGISTRO_FISICA:U2-6` | `criterio-locale` | la parola *«caso che deve fallire»* | 6 È IL CASO CHE DEVE FALLIRE (P1-sexies, ed è il criterio più importante): la |
| `REGISTRO_FISICA:V6` | `criterio-locale` | la parola *«caso che deve fallire»* | il caso che DEVE fallire: la forma exp(dx/u) / deve esplodere vicino al confine, e il test l |
| `DOPPIA-COP` | `cura` | la parola *«inventario»* | LA CURA (b): la doppia copertura 4 pi e' un ASSIOMA e va resa STRUTTURALE, non misurata |
| `M-FLUSSO` | `cura` | la parola *«caso che deve fallire»* | memoria di flusso per ARCO, scalare e antisimmetrica, al posto di mem_mot |
| `M-LEGAMI` | `cura` | la parola *«finestra»* | cos(dph - tw) al posto di cos(phi0_i - phi0_j): rende viva una memoria congelata |
| `MEM-VERSO` | `cura` | la parola *«caso che deve fallire»* | il verso dell arco dalla sua MEMORIA (delta = twp - tw) invece che dal segno istantaneo |
| `POTATURA-GUARDIE` | `cura` | la parola *«numeri di riga»* | I 57 rami MORTI delle guardie di lunghezza: potatura rimandata dopo il riordino della mitosi |
| `SCHED-PASSO` | `cura` | la parola *«argv del driver»* | il passo pieno diventa uno SCHEDULATORE: le regole del passo sono architettura, non intenzio |
| `ARCHI-OLTRE-4PI` | `difetto` | la parola *«finestra»* | circa 109 archi sono oltre il tetto 4pi dal passo 2 e non rilassano, in tutti i bracci |
| `CENS-A1` | `difetto` | la parola *«ricopiat»* | [A] la RIDUZIONE AL LIMITE dello spinore: lo stato che la garantisce non e' raggiungibile |
| `CENS-A3` | `difetto` | la parola *«argv del driver»* | [A] `COPPIA_MIT`: *"(opzione, spenta di default)"*, e il default e' `1.0` |
| `CENS-A6` | `difetto` | la parola *«argv del driver»* | [A] `README.md`: *"Tutti gli script di lancio includono esplicitamente `--sync`"* |
| `CS-LAMBDA-GLOBALE` | `difetto` | la parola *«a vuoto»* | _cs_nodo non e del tutto locale: il pavimento usa _Lam = mean(/psi/^2) su TUTTA la rete |
| `D26` | `difetto` | la parola *«a vuoto»* | Le coorti non sopravvivevano allo SNAPSHOT: dopo un salva/ricarica il lignaggio ripartiva VU |
| `FALSO-UNO` | `difetto` | la parola *«falso-zero»* | un verdetto NEGATIVO prodotto da una voce che non parla del merito: il gemello di FALSO-ZERO |
| `FALSO-ZERO` | `difetto` | la parola *«falso zero»* | uno ZERO prodotto da un insieme o un campione che ho scelto io: cinque volte in una sessione |
| `INVENTARIO-SIGILLI-SENZA-COMMIT` | `difetto` | la parola *«finestra»* | 79 voci di sigillo su 82 non hanno il commit con cui rigirarle, piu una riga duplicata |
| `MCRIT-RICALCOLO` | `difetto` | la parola *«inventario»* | massa_critica_adattiva si ricalcola 7 volte per passo su stati diversi: e' una lettura mista |
| `MEM-HEBB-VERSO` | `difetto` | la parola *«caso che deve fallire»* | memoria_hebbiana_moto dipende dal verso dell'arco: d0 cambia segno e lo shift va a un solo e |
| `MITOSI-2LAM-ACCESO` | `difetto` | la parola *«argv del driver»* | il piano dichiara MITOSI_2LAM e PLAST_DIN OFF, e il DRIVER li ACCENDE: --mitosi-2lam, --plas |
| `PEQ-SEL-STANTIO` | `difetto` | la parola *«argv del driver»* | mitosi legge self.peq[sel] DOPO che peq e' stato rifiltrato con keep: archi sbagliati, in si |
| `PHI0-CONGELATA` | `difetto` | la parola *«caso che deve fallire»* | phi0 e CONGELATA: 5 scritture tutte alla nascita, e lo step la legge come memoria hebbiana |
| `PRE-RILASSAMENTO-FUORI-PASSO` | `difetto` | la parola *«falso-zero»* | 300 step() girano in _applica_flag, FUORI da esegui_passo: sei voci del passo non ci sono |
| `PRESIDIO-RIFIUTO-SOLO-SIGILLI` | `difetto` | la parola *«provenienza»* | _presidio.avvia rifiuta di girare SOLO se il nome comincia con _sigillo_: A9 lo dice senza |
| `REG-A` | `difetto` | la parola *«inventario»* | FASE A del registro della fisica: l'INVENTARIO degli scrittori di stato / MANDATO-REGISTRO § |
| `REGIME-DUE-SISTEMI` | `difetto` | la parola *«byte-inerzia»* | --regime crea un secondo sistema con lo stesso nome: SCUOTIMENTO cambia se il flag e' passat |
| `SCHERMATURA-LEGGE-REVISIONE` | `difetto` | la parola *«caso che deve fallire»* | lambda_nodi: una rho_c GLOBALE, un commento che descrive un altra legge, un numero non deriv |
| `SMP-APRI-COMMENTO` | `difetto` | la parola *«commento scaduto»* | il docstring di _smp_apri dice che la chiamano cinque leggi: oggi la chiama solo lo schedula |
| `TETTO-CAUSALE-TEMPO-COORDINATO` | `difetto` | la parola *«caso che deve fallire»* | il tetto causale usa c_s LOCALE ma DT COORDINATO: dove r e piccolo permette moti superlumina |
| `VELENO-DOMINI` | `difetto` | la parola *«controllo positivo»* | DOMINI include 9 delle 10 derivate: una derivata avvelenata VIOLA il dominio per costruzione |
| `DIVISIONE-AUTOCONSISTENTE` | `fronte` | la parola *«finestra»* | la divisione dell arco come UNA legge: dove si rompe, cosa ereditano i figli, il calcio |
| `ENERGIA-NON-DEFINITA` | `fronte` | la parola *«falso-zero»* | il modello non ha un'energia totale, e senza quella bilancio e calore non hanno base |
| `FINESTRA-PRE-NASCITA` | `fronte` | la parola *«falso-zero»* | una finestra PRIMA della prima nascita (216) non dice niente sulle nascite: e' costata TRE v |
| `GRAVITA-POTENZIALE` | `fronte` | la parola *«argv del driver»* | due potenziali nel codice e nessun Poisson risolto: Poisson e un VINCOLO DI SCALA |
| `LINGUAGGIO-REGOLE` | `fronte` | la parola *«finestra»* | un linguaggio dichiarativo delle leggi, da cui GENERARE il codice e il documento: proposta d |
| `LUNGHEZZA-COME-SEGNALE` | `fronte` | la parola *«falso-zero»* | usare len(x) < n come segnale di <<nodo nuovo>> e una toppa implicita: serve una regola |
| `NON-TRACCIATI` | `fronte` | la parola *«inventario»* | 484 file non tracciati: 98 CITATI e non tracciati sono riferimenti al vuoto, e il .gitignore |
| `REVERSIBILITA-LOCALE` | `fronte` | la parola *«a vuoto»* | reversibilita' LOCALE, irreversibilita' GLOBALE: la sola freccia e' la crescita dello spazio |
| `SIGILLO-COMPARATORE-DUPLICATO` | `fronte` | la parola *«falso-uno»* | il comparatore del lockstep e copiato in due sigilli: due copie che possono divergere |
| `SIGILLO-SENZA-CONFIGURAZIONE` | `fronte` | la parola *«p3»* | il sigillo prende la configurazione dal CLI del driver ma NON la timbra nel suo json |
| `VUOTO-LOCALE-DETERMINISTICO` | `fronte` | la parola *«finestra»* | termostato locale + scuotimento DETERMINISTICO: UNA legge per nodo, fase <-> vuoto |
| `Z43` | `fronte` | la parola *«falso-uno»* | Z43 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / APERTA — ED E' UNA DECISIONE SULLA DEFINIZI |
| `CARICA-SIMMETRIA-FASE` | `misura` | la parola *«controllo positivo»* | la carica e il verso di rotazione: il test dello spostamento globale, e quale fra Q_A e Q_B |
| `GUSCIO-ANTIFASE-EMERGENTE` | `misura` | la parola *«falso-zero»* | il guscio in antifase si forma DA SOLO e scherma? Oggi emergente e imposta sono MESCOLATE |
| `LOSCHMIDT-ECO` | `misura` | la parola *«caso che deve fallire»* | l'eco di Loschmidt PER VOCE: un errore subito grande e' irreversibilita' del CODICE |
| `SCHW-CORTI` | `misura` | la parola *«caso che deve fallire»* | il 39 % delle coppie Schwinger ACCORCIA il grafo: 2*dd < d, misurato |
| `TERMOSTATO-E-FRENO` | `misura` | la parola *«finestra»* | il termostato frena piu' di quanto rifornisca: togliergli il freno, non la sorgente |
| `H-ETC-1` | `presidio` | tipo `presidio` | PRESIDIO PROPOSTO E NON CABLATO: zero calcola_psi senza w dentro passo_pieno |
| `H-ETC-2` | `presidio` | tipo `presidio` | PRESIDIO PROPOSTO E NON CABLATO: permutare le cinque leggi deve dare lo STESSO stato (Jacobi |
| `P1` | `presidio` | tipo `presidio` | NON USARE L'ASSOCIAZIONE SENZA VERIFICARE LO STORICO. |
| `P2` | `presidio` | tipo `presidio` | PRIMA DI ESCLUDERE UN FLAG DA UNA MISURA: FORZA IL SISTEMA O LO CORREGGE? |
| `P3` | `presidio` | tipo `presidio` | NESSUNA STATISTICA SENZA BARRA D'ERRORE, e per confronti fra bracci si usa la |
| `P4` | `presidio` | tipo `presidio` | PRIMA DI MISURARE SE UNA GRANDEZZA CAMBIA, VERIFICARE CHE SIA LIBERA DI CAMBIARE. |
| `P5` | `presidio` | tipo `presidio` | OGNI RAMO else / FALLBACK / getattr(..., default) SU UN PERCORSO FISICO VA CONTATO. |
| `P6` | `presidio` | tipo `presidio` | OGNI CSV DI MISURA PORTA BLOB, SEME E TUTTI I FLAG che distinguono quel run dagli altri |
| `Q6` | `presidio` | tipo `presidio` | Q6 (1a) / confrontava i valori dopo il passo, quando il rilassamento li ha gia' mossi in... |
| `R3` | `presidio` | tipo `presidio` | pretendeva bias == 0.0 esatto e falliva su due ulp di arrotondamento |
| `R5` | `presidio` | tipo `presidio` | contava 25 aperture su 24 passi: l'iniezione del test apriva il freno lei stessa |
| `STATI-LOCALI` | `presidio` | tipo `presidio` | gli stati .npz del grafo restano LOCALI: in git vanno solo sha1, percorso e comando |
| `U3` | `presidio` | tipo `presidio` | confrontava con il mio sviluppo e/2 invece del valore esatto e/(2+e); il numero stampato... |
| `CENS-B1` | `sospetto` | la parola *«misura mancante»* | [B] *"`SPINORE_VIVO = True` **NON E' MAI STATO VALIDATO COME DEFAULT** ... |
| `CENS-B16` | `sospetto` | la parola *«inventario»* | [B] (1) INVENTARIO e (2) README sono prescritti *"nello stesso commit del  |
| `CENS-B8` | `sospetto` | la parola *«argv del driver»* | [B] *"INTEGRATORE METRICO **SPERIMENTALE** ... Default off per mantenere i |
| `GEOM-SENZA-VERSO` | `sospetto` | la parola *«falso-zero»* | perc_geom nasce da /tw/: perde il VERSO, ma la catena della torsione la usa come chiralita |
| `SCIOGLIMENTO-FASE` | `sospetto` | la parola *«non si rigira»* | perche' coer_campo va da 0.999 a 0.20 in 120 passi: la scena non tocca phivel e la coppia no |
| `SPINORE-SENZA-FASE` | `sospetto` | la parola *«byte-inerzia»* | la coppia muove phivel ma deriva da un'ALTRA fase: lo spinore ha un orologio tutto suo |
| `ROBUSTEZZA-FISICA` | `standard` | tipo `standard` | i TRE GRADINI che una conclusione di fisica deve salire: rumore numerico, legge pratica, lim |
| `TAGLIA-FINITA` | `standard` | tipo `standard` | lo scaling di taglia finita come via al limite continuo: reti diverse e si estrapola |

## ⛔ **E LE BLOCCANTI CHE HO SOSPESO: Luca le guardi**

### **Una voce bloccante sospesa NON e' una voce risolta:** blocca le corse ### **dell'era `1`**, che non si fanno piu'. ### ⚠ **Ma se una di queste e' in realta' una lezione di METODO, l'era `2` la perderebbe.**

| id | stato prima | si riferisce a | titolo |
|---|---|---|---|
| `CENS-A2` | `aperto` | `eta,mitosi,nascita` | [A] `TORS_4PI`: *"Prova sperimentale, default off"*, e il default e' `True` |
| `CENS-A7` | `aperto` | `psi,eta,calcola_psi,nascita` | [A] il commento di `calcola_psi`: *"~19 chiamanti"*, misurato **2** |
| `CENS-B7` | `aperto` | `phi,eta,scuoti_vuoto,mitosi,memoria_hebbiana_moto,rilassa_disegno` | [B] *"Default ancora off; **convergenza e superiorita' rispetto al percors |
| `CLI-1` | `da-decidere` | `eta,_cs_nodo_prev,mitosi,LAM,nascita` | I SIGILLI DI CURA 4 E CURA 5 NON HANNO MAI PROVATO IL PERCORSO CLI: impostavano S.SE |
| `D03` | `da-decidere` | `peq,d0,pos,mitosi,divisione` | La memoria del moto prende le direzioni da pos, normalizza su Imed GLOBALE, e ha un  |
| `D31` | `da-decidere` | `d0,pos,mitosi,schwinger,repuls,torsione` | Il freno di SCALAMIN (smpchiudi) E' IL MOTORE della crescita di d0: vale il 117.41 % |
| `SCALE-TW` | `da-decidere` | `phi,twp,tw,K_SYNC,mitosi,schwinger` | LE SCALE DELLA TORSIONE: un'analisi completa, DA CAPO / mandato di Luca ricevuto all |
| `U1` | `da-decidere` | `lambda_nodi,mitosi,massa_critica,chiralita,LAM,_passo_spinoriale` | URGENTE, PRIMA DI QUALUNQUE GIRO LUNGO — massacriticacollasso: 21 usi DENTRO LEGGI F |

## ⚠ **E LE SOSPESE SENZA RIFERIMENTO: `411`**

### **Il campo `si_riferisce_a` si riempie cercando NEL TESTO della voce** i nomi delle variabili di stato e delle leggi. ### ⛔ **Dove non trova niente scrive `(non trovato)`, e NON inventa:** il censimento e' ### **per DIFETTO**, e queste sono le voci che al triage ### **vanno lette a mano.**
