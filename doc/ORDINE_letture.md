# 🔬 **L'ORDINE LETTURA/RISCRITTURA, e LE REGOLE DI NASCITA**

> ### **Generato da** `csv/_test_fork/_referto_ordine.py` dalla misura
> `csv/_seal_fork/_ordine_letture/_ordine_letture.json` *(strumento `97cb0ea3`)* e dalla
> dichiarazione `doc/REGOLE_nascita.tsv`. **Non si modifica a mano.** *(`L-NUMERI`.)*

| | |
|---|---|
| scena | `nmasse 3`, `sep 6.1158`, seme `11` |
| la nascita | ### **trovata al passo 42** *(non assunta)*: `n = 12803`, `m = 471565` |
| la finestra | si apre quando **`mitosi` ritorna** *(evento `3774496`)* e si chiude **a fine del passo seguente** |
| eventi intercettati | **5661994** |
| ### **il CONTROLLO** | ### **lo stesso passo con e senza sorveglianza e' BYTE-IDENTICO** → la misura vale |
| tipo del lettore | da **`_PASSO_TIPI`**, la tabella del simulatore. **Non leggi:** `osservatore`, `disegno` |

## ⛔ **Il verdetto NON e' quello che stampa lo strumento, e va spiegato**

Lo strumento stampa *«LETTA PRIMA»* per **24** grandezze. ### **Quell'etichetta e'
FUORVIANTE, ed e' il SESTO difetto mio su questo strumento:** la finestra si apre quando
`mitosi` **ritorna**, e a quell'istante **molte grandezze sono GIA' PIENE** — chi le legge
dopo ### **non le vede corte**.

> ### 📌 **La domanda vera non e' «chi legge prima»: e' «una legge le legge CORTE?».**
> Il dato per rispondere e' **nella misura stessa**: ogni evento porta la **lunghezza**
> vista in quell'istante. ### **Quindi la misura VALE e non si rigira: si legge bene.**

| | quante | quali |
|---|---|---|
| ### **PIENE quando `mitosi` ritorna** *(nessuno puo' vederle corte)* | ### **30** | `_cs_nodo_prev` · `_deg` · `_nb` · `_nb_prec` · `_nb_ret` · `_psi_prec` · `_psi_spin_prec` · `_psi_spinor` · `_spinor_lift` · `conc_nodi` · `eta` · `mem_mot` · `omega_s` · `perc_chi` · `perc_geom` · `perc_tw` · `phi0` · `phi_s` · `phivel` · `pos` · `psi` · `psi_spin` · `rho_spin` · `_rep` · `d` · `d0` · `peq` · `tw` · `twp` · `vd` |
| ### **CORTE quando `mitosi` ritorna** | ### **10** | `_chi_core_nodi` · `_chi_core_raggio` · `_chi_core_rho0` · `_chi_geom_nodi` · `_fatt_cs_ultimo` · `_g_rampa_prec` · `_r_corrente` · `_xi_rumore` · `_dt_e_ultimo` · `_sin2_vir` |

### ➜ **Le 30 PIENE sono esattamente quelle CON una regola di nascita: la regola si vede nella misura, non solo nel codice.**

## Le **10** corte: **una legge le legge corte?**

| grandezza | cl. | `len` a fine mitosi | bersaglio | prima lettura di LEGGE | verdetto |
|---|---|---|---|---|---|
| `_chi_core_nodi` | nodo | `12802` | `12803` | — | **nessuna legge la legge** → ### **PUO' RESTARE CORTA** |
| `_chi_core_raggio` | nodo | `12802` | `12803` | — | **nessuna legge la legge** → ### **PUO' RESTARE CORTA** |
| `_chi_core_rho0` | nodo | `12802` | `12803` | — | **nessuna legge la legge** → ### **PUO' RESTARE CORTA** |
| `_chi_geom_nodi` | nodo | `12802` | `12803` | `#5661606` `step` — `len = 12803` | la legge la trova **GIA' PIENA** *(riscritta a `#4718175`)* → ### **PUO' RESTARE CORTA** |
| `_fatt_cs_ultimo` | nodo | `12802` | `12803` | — | **nessuna legge la legge** → ### **PUO' RESTARE CORTA** |
| `_g_rampa_prec` | nodo | `12802` | `12803` | `#3774771` `_pesi` — ### **`len = 12802`** | ### **AUTO-RINFRESCO**: la legge la legge corta e la **riscrive lei stessa** `+1` eventi dopo → ### **e' una REGOLA DI RINFRESCO, non un buco** |
| `_r_corrente` | nodo | `12802` | `12803` | `#3774836` `_bloch_ritardato` — `len = 12803` | la legge la trova **GIA' PIENA** *(riscritta a `#3774762`)* → ### **PUO' RESTARE CORTA** |
| `_xi_rumore` | nodo | `12802` | `12803` | `#4718234` `_passo_spinoriale` — ### **`len = 12802`** | ### **AUTO-RINFRESCO**: la legge la legge corta e la **riscrive lei stessa** `+1` eventi dopo → ### **e' una REGOLA DI RINFRESCO, non un buco** |
| `_dt_e_ultimo` | arco | `471564` | `471565` | `#5661774` `_fattore_tempo_arco` — `len = 471565` | la legge la trova **GIA' PIENA** *(riscritta a `#3774761`)* → ### **PUO' RESTARE CORTA** |
| `_sin2_vir` | arco | `471564` | `471565` | `#5661662` `step` — `len = 471565` | la legge la trova **GIA' PIENA** *(riscritta a `#3774621`)* → ### **PUO' RESTARE CORTA** |

| esito | quante |
|---|---|
| nessuna lettura di legge | ### **4** |
| letta GIA' piena | ### **4** |
| auto-rinfresco | ### **2** |
| BUCO | 0 |

### ✅ **ZERO BUCHI: nessuna legge legge una cache corta che non sia la sua stessa riscrittura.** E i due **auto-rinfreschi** sono ### **GIA' DICHIARATI E CONTATI nel codice**:

| | |
|---|---|
| `_xi_rumore` | *«questo **NON** e' un fallback: e' il **percorso normale della mitosi**; `xi` e' l'**AMBIENTE**, non una proprieta' del nodo, quindi il figlio **NON** lo eredita»*. ### **E' una regola di nascita al sito di lettura, e la misura la conferma** |
| `_g_rampa_prec` | *«e' un array **DIAGNOSTICO**, e lo dichiaro come tale: il suo disallineamento **SI CONTA** e si riparte … qui se il confronto salta si perde una **MISURA**, non una legge»*, col contatore `_g_rampa_prec_disallineata`. ### **`A8` gia' rispettato** |

> ### 📌 **CHE COSA VUOL DIRE PER IL CONTROLLO UNICO:** le **30** piene passano il controllo `len == n` **per costruzione**; le **10** corte vanno **escluse** e **dichiarate**, e per due di esse la dichiarazione ### **esiste gia' nel codice.** ### ➜ **Non c'e' niente da curare PRIMA del controllo.**

---

## 📜 **LE REGOLE DI NASCITA** *(punto 7: le ho lette io, non le ho battezzate)*

**Il mio strumento le dava «DA DECIDERE» per una ragione sola:** il valore passa da una
**variabile locale** *(`fm`, `anti`, `pos_figlio`, `chi_nuovi`, `er`, `el`, `dh`,
`calcio_phi`, `calcio_omega`)*, e l'AST leggeva **il nome della locale** invece della sua
definizione. ### **La stessa cecita' sugli ALIAS, stavolta dal lato del VALORE.**

### ⚠ **Ogni riga si VERIFICA per ANCORA, e la riga di oggi e' stampata:** i numeri di
riga **shiftano fra i blob** *(par.2)*, quindi ### **non si cita una riga — si cita un
testo e si dice dove sta adesso.**

| grandezza | cl. | evento | ### **regola** | riga OGGI | come si legge |
|---|---|---|---|---|---|
| `phi` | metro-nodo | **semina** | estrazione nuova | `:3134` | fase CASUALE sul doppio giro; nel ramo con `fase` data e` `float(fase) + rng.normal(0, 0.05, n)` |
| `phi` | metro-nodo | **divisione** | media (fase media dei genitori) | `:6616` | `D` e` la differenza di fase fra i genitori: `phi[a] - D/2` E` IL PUNTO MEDIO. Con `MITOSI_DIR` il `bias = 0.5*tanh(...)` sposta il punto medio secondo l asimmetria di torsione, e a :6638 un `flip` puo` aggiungere mezzo giro |
| `phi` | metro-nodo | **Schwinger** | antifase del figlio di mitosi | `:6784` | mezzo giro esatto dal figlio scelto: e` la coppia particella-antiparticella |
| `phi0` | nodo | **divisione** | uguale a phi alla nascita | `:6641` | stesso `fm` di `phi`: il nato ha fase di riferimento UGUALE alla sua fase, cioe` scarto zero |
| `phi0` | nodo | **Schwinger** | uguale a phi alla nascita | `:6804` | stesso `anti` di `phi` |
| `pos` | nodo | **divisione** | punto medio dei genitori | `:6617` | media aritmetica delle due posizioni |
| `pos` | nodo | **Schwinger** | punto medio | `:6802` | media aritmetica |
| `phivel` | nodo | **semina** | ### **estrazione nuova, oppure zero** ### ⚠ **DA PORTARE A LUCA** | `:3154` | DUE RAMI: col calore iniziale un calcio gaussiano (a :3152 moltiplicato per `chi_nuovi`), senza calore `np.zeros(n)` a :3157 |
| `phivel` | nodo | **divisione** | media dei genitori | `:6643` | semisomma esplicita |
| `perc_chi` | nodo | **semina** | estrazione nuova | `:3144` | sorteggio del segno, lo STESSO array usato anche per `perc_geom` |
| `perc_chi` | nodo | **divisione** | eredita dal genitore a | `:6647` | copia diretta |
| `perc_chi` | nodo | **Schwinger** | eredita INVERTITA (carica opposta) | `:6810` | il segno meno: l antiparticella ha carica opposta |
| `perc_geom` | nodo | **semina** | estrazione nuova | `:3185` | lo stesso sorteggio di `perc_chi` |
| `perc_geom` | nodo | **divisione** | eredita dal genitore a | `:6650` | copia diretta |
| `perc_geom` | nodo | **Schwinger** | ### **eredita DIRETTA, NON invertita** ### ⚠ **DA PORTARE A LUCA** | `:6814` | copia diretta -- e alla Schwinger `perc_chi` INVERTE e `perc_geom` NO |
| `omega_s` | nodo | **semina** | estrazione nuova | `:3191` | calcio gaussiano isotropo sui tre assi |
| `omega_s` | nodo | **divisione** | eredita dal genitore | `:2363` | copia diretta dal genitore `src` |
| `_psi_spinor` | nodo | **divisione** | eredita COL SEGNO di doppia copertura | `:2365` | copia dal genitore, e a :2367 `er = -er` per l antichirale: segno di doppia copertura opposto |
| `_spinor_lift` | nodo | **divisione** | eredita COL SEGNO | `:2370` | copia dal genitore, e a :2372 `el = -el` |
| `d` | arco | **divisione** | META` del padre, con pavimento LAM | `:6690` | l arco si spezza in due tronconi da `d/2`, e `_nasce(dh, mitosi, 2, 0)` impone la scala minima LAM |
| `d` | arco | **Schwinger** | nuova a scala minima | `:6790` | i due archi della coppia nascono alla scala minima, non ereditano |
| `d` | arco | **allaccio** | nuova a scala minima | `:3359` | il troncone parte da LAM |
| `d0` | arco | **divisione** | ### **META`, con tre rami** ### ⚠ **DA PORTARE A LUCA** | `:6722` | TRE RAMI a :6704 :6707 :6709 che scelgono fra `d0h` (meta` di d0) e `dh` (meta` di d) |
| `tw` | arco | **divisione** | zero | `:6734` | i tronconi nascono senza torsione |
| `tw` | arco | **allaccio** | zero | `:3366` | l arco nuovo nasce senza torsione |
| `i` | metro-arco | **divisione** | topologia: l arco a-b e` SOSTITUITO da a-m e m-b | `:6710` | `keep` TOGLIE l arco spezzato: non e` un valore che si eredita, e` la topologia |
| `j` | metro-arco | **divisione** | topologia: secondo troncone | `:6711` | idem |
| `i` | metro-arco | **Schwinger** | topologia: due archi nuovi verso k | `:6840` | il nodo `k` della coppia si allaccia ad `aa` e `bb` |
| `j` | metro-arco | **Schwinger** | topologia: due archi nuovi verso k | `:6841` | idem |

**Ancore verificate: 29 su 29.** ### ✅ **Tutte trovate, e UNA VOLTA SOLA.**

## 🛑 **I 3 casi che porto a Luca, e SOLO questi**

**Il mandato dice: *«porta SOLO i casi in cui la regola esistente ti sembra fisicamente
discutibile, uno per uno, con la riga»*.** ### **Gli altri li ho scritti e non li porto.**

### ⚠ `phivel` — evento **semina** — `:3154`

**La regola che c'e':** estrazione nuova, oppure zero. **Come si legge:** DUE RAMI: col calore iniziale un calcio gaussiano (a :3152 moltiplicato per `chi_nuovi`), senza calore `np.zeros(n)` a :3157

### ⚠ `perc_geom` — evento **Schwinger** — `:6814`

**La regola che c'e':** eredita DIRETTA, NON invertita. **Come si legge:** copia diretta -- e alla Schwinger `perc_chi` INVERTE e `perc_geom` NO

### ⚠ `d0` — evento **divisione** — `:6722`

**La regola che c'e':** META`, con tre rami. **Come si legge:** TRE RAMI a :6704 :6707 :6709 che scelgono fra `d0h` (meta` di d0) e `dh` (meta` di d)

