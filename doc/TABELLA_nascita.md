# **LE REGOLE DI NASCITA** — *generato da `csv/_tabella_nascita.py`, NON a mano*

> ### **La FONTE e' `REGOLE_NASCITA` in `soliton_simulator.py`** *(blob `c18c9bf6`, sha1 byte grezzi)*. ### **Questo file e' una VISTA: non si modifica a mano.**

### 📌 **E IL PRESIDIO NON E' QUESTO DOCUMENTO, E' IL CODICE:** una grandezza del registro che non compare nella tabella dell'evento ### **ferma il run** con *«regola di nascita non dichiarata per `<nome>` all'evento `<evento>`»*. Il collaudo a secco gira ### **all'import**, cosi' una riga che manca ferma il processo ### **prima** che un run cominci.

| | |
|---|---|
| **grandezze governate** | ### **36** *(i 35 registri `METRI`+`STATO`+`FINESTRA`, piu' `_peqn_idx` DICHIARATO dopo `peq`)* |
| **eventi APPROVATI** | `semina` · `divisione` · `schwinger` · `allaccio` — ### **approvati da Luca il 2026-10-01** |
| ### **eventi CONVERTITI** | ### **`divisione` · `schwinger`** — gli altri due vivono nelle loro funzioni, e `nascita()` ### **si RIFIUTA di girare** per loro invece di far finta |
| **righe in tabella** | ### **72** |

| classe, evento `divisione` | quante |
|---|---|
| `regola` | **32** |
| `collocata` | **3** |
| `non si tocca` | **1** |

| classe, evento `schwinger` | quante |
|---|---|
| `regola` | **33** |
| `collocata` | **3** |

### ⚠ **E L'ORDINE E' PARTE DEL CONTRATTO, MISURATO** *(`csv/_test_fork/_ordine_registro.py`)*: `phi` prima di `twp` · `peq` prima di `_peqn_idx` · `n0` nel **contesto** · le **6 chiamate con effetto** collocate a mano. ### **4 vincoli genuini, 0 violazioni dall'ordine del registro.**

---

# **EVENTO `divisione`**

| # | grandezza | classe | regola | ancora |
|---|---|---|---|---|
| 0 | **`phi`** | ✅ regola | media (fase media dei genitori) | `self.phi = np.concatenate([self.phi, fm])` |
| 1 | **`i`** | ✅ regola | topologia: l'arco si spezza in due | `self.i = np.concatenate([self.i[keep], a, m])` |
| 2 | **`j`** | ✅ regola | topologia: l'arco si spezza in due | `self.j = np.concatenate([self.j[keep], m, b])` |
| 3 | **`_cs_nodo_prev`** | ✅ regola | eredita dal genitore `a` | `self._cs_nodo_prev = np.concatenate([_csp, np.asarray(_csp, float)[src]])` |
| 4 | **`_deg`** | 🔧 collocata | collocata | `self._grado()` |
| 5 | **`_nb`** | ✅ regola | eredita dal genitore `a` | `self._nb = np.vstack([self._nb, self._nb[src]])` |
| 6 | **`_nb_prec`** | ✅ regola | eredita dal genitore `a` | `self._nb_prec = np.vstack([self._nb_prec, self._nb_prec[src]])` |
| 7 | **`_nb_ret`** | ✅ regola | eredita dal genitore `a` | `self._nb_ret = np.vstack([_nbr_er, _nbr_er[src]])` |
| 8 | **`_psi_prec`** | ✅ regola | eredita dal genitore `a` | `self._psi_prec = np.concatenate([self._psi_prec, self._psi_prec[src]])` |
| 9 | **`_psi_spin_prec`** | ✅ regola | eredita dal genitore `a` | `self._psi_spin_prec = np.vstack([_pspr, np.asarray(_pspr)[src]])` |
| 10 | **`_psi_spinor`** | ✅ regola | eredita col SEGNO (regola D) | `self._psi_spinor = np.vstack([self._psi_spinor, er])` |
| 11 | **`_spinor_lift`** | ✅ regola | eredita col SEGNO (regola D) | `self._spinor_lift = np.vstack([self._spinor_lift, el])` |
| 12 | **`conc_nodi`** | ✅ regola | eredita la concorrenza del genitore `a` | `self.conc_nodi.append(eredita)` |
| 13 | **`eta`** | ✅ regola | zero | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` |
| 14 | **`mem_mot`** | ✅ regola | eredita dal genitore `a` | `self.mem_mot = np.vstack([self.mem_mot, self.mem_mot[a]]) if len(...) else np.zeros((len(sel), 3))` |
| 15 | **`omega_s`** | ✅ regola | eredita dal genitore `a` | `self.omega_s = np.vstack([self.omega_s, self.omega_s[src]])` |
| 16 | **`perc_chi`** | ✅ regola | eredita la chiralita' del genitore `a` | `self.perc_chi = np.concatenate([self.perc_chi, self.perc_chi[a]])` |
| 17 | **`perc_tw`** | ✅ regola | zero | `self.perc_tw = np.concatenate([self.perc_tw, np.zeros(len(sel))])` |
| 18 | **`phi0`** | ✅ regola | media (come `phi`) | `self.phi0 = np.concatenate([self.phi0, fm])` |
| 19 | **`phi_s`** | ✅ regola | eredita dal genitore `a` | `self.phi_s = np.concatenate([self.phi_s, self.phi_s[a]])` |
| 20 | **`phivel`** | ✅ regola | media dei genitori | `self.phivel = np.concatenate([self.phivel, 0.5 * (self.phivel[a] + self.phivel[b])])` |
| 21 | **`pos`** | ✅ regola | media dei genitori (punto medio) | `self.pos = np.vstack([self.pos, pos_figlio])` |
| 22 | **`psi`** | ✅ regola | media dei genitori (come `phi`) | `self.psi = np.concatenate([cur[:n0], 0.5 * (cur[a] + cur[b])])` |
| 23 | **`psi_spin`** | ✅ regola | eredita da `a` (come `phi_s`) | `self.psi_spin = np.concatenate([cs[:n0], cs[a]])` |
| 24 | **`rho_spin`** | ✅ regola | eredita da `a` (come `psi_spin`) | `self.rho_spin = np.concatenate([np.asarray(rs)[:n0], np.asarray(rs)[a]])` |
| 25 | **`_rep`** | ✅ regola | eredita dall'arco che si spezza | `self._rep = np.concatenate([self._rep[keep], self._rep[sel], self._rep[sel]])` |
| 26 | **`d`** | ✅ regola | meta' dell'arco (due tronconi) | `self.d = np.concatenate([self.d[keep], dh])  # `dh` e' GIA' i due blocchi` |
| 27 | **`d0`** | ✅ regola | meta' dell'arco, con offset plastico | `self.d0 = np.concatenate([self.d0[keep], d0new])` |
| 28 | **`peq`** | ✅ regola | eredita dall'arco che si spezza | `self.peq = np.concatenate([self.peq[keep], self.peq[sel], self.peq[sel]])` |
| 29 | **`_peqn_idx`** | — non si tocca | non si tocca | `(nessuna)` |
| 30 | **`tw`** | ✅ regola | zero | `self.tw = np.concatenate([self.tw[keep], zz, zz])` |
| 31 | **`perc_geom`** | ✅ regola | DERIVATA dalla definizione (non eredita) | `self.perc_geom = np.concatenate([self.perc_geom, _derivazione_perc_geom(self, c)])` |
| 32 | **`twp`** | ✅ regola | differenza di fase genitore-figlio | `self.twp = np.concatenate([self.twp[keep], self._wphi(self.phi[a] - fm), self._wphi(fm - self.phi[b])])` |
| 33 | **`vd`** | ✅ regola | eredita dall'arco che si spezza | `self.vd = np.concatenate([self.vd[keep], self.vd[sel], self.vd[sel]])` |
| 34 | **`_smp_d0`** | 🔧 collocata | collocata | `self._smp_chirurgia(keep=keep, nuovi=d0new)` |
| 35 | **`_smp_d`** | 🔧 collocata | collocata | `self._smp_chirurgia(keep=keep, nuovi=d0new)` |

## Le derivazioni, evento `divisione`

- **`phi`** — *media (fase media dei genitori)*: `fm` e' il punto medio di fase fra i genitori, calcolato nella preparazione (con `MITOSI_DIR` spostato verso il genitore piu' teso, e con `ANTIFASE_ADD` eventualmente ribaltato di mezzo giro)
- **`i`** — *topologia: l'arco si spezza in due*: l'arco `a-b` sparisce (`keep`) e nascono `a-m` e `m-b`: `i` prende `a` e `m`, `j` prende `m` e `b`. ORDINE ESSENZIALE: e' una concatenazione, e l'ordine DECIDE la topologia
- **`j`** — *topologia: l'arco si spezza in due*: il compagno di `i`: insieme danno `a-m` e `m-b`
- **`_cs_nodo_prev`** — *eredita dal genitore `a`*: STA PRIMA della guardia sugli spinori DI PROPOSITO: questa cache vive sotto `CS_DINAMICO and (FORK_SU2_MEM or STEP2_OROLOGIO)`, NON sotto `--spinore-corretto`. Senza, `len(_cs_nodo_prev) < n` e `tau = d/cs` calcolava `d/CS_M`: MISURATO nell'80% dei passi. NB: concatena `_csp` INTERO, non `_csp[:n0]` -- convenzione diversa da quella di `psi`, e si conserva tale
- **`_deg`** — *collocata*: la scrive `_grado()`, collocata DOPO il blocco perche' LEGGE `i`, `j` e `len(phi)`: e' una DERIVATA della topologia, non una regola di nascita. Insieme a `_deg` invalida `_cicli_topologici` e richiama `_costruisci_struttura`
- **`_nb`** — *eredita dal genitore `a`*: il Bloch del figlio e' quello del padre. ### E IL SUO ESITO E' UNA CONDIZIONE PER `_nb_prec`: oggi `_nb_prec` e' estesa solo DENTRO il ramo di `_nb`, ed e' una dipendenza di CONTROLLO, non di dato -- quindi non la vedrebbe nessun grafo sui dati. Si conserva passando l'esito nel contesto
- **`_nb_prec`** — *eredita dal genitore `a`*: ### SOLO SE `_nb` E' STATA ESTESA: e' il nido di oggi, conservato
- **`_nb_ret`** — *eredita dal genitore `a`*: [FORK SU(2) STRATO 1] il Bloch RITARDATO e' memoria di NODO: il figlio eredita il passato del padre. Senza, al passo dopo `len(_nb_ret) != n` e la memoria veniva RESETTATA a ogni mitosi
- **`_psi_prec`** — *eredita dal genitore `a`*: evita il reset spurio GLOBALE in `ritmo()` su `len != n`
- **`_psi_spin_prec`** — *eredita dal genitore `a`*: SNAPSHOT DEL RITMO SPINORIALE (4pi). Senza, `len(_psi_spin_prec) != n` e la guardia ESATTA di `ritmo()` scartava il ramo a 4pi: MISURATO nel 95.33% delle chiamate, e la FASE 5 era INERTE in ogni run `--campo-spinoriale`. E' `n x 2` COMPLESSO, quindi `vstack`
- **`_psi_spinor`** — *eredita col SEGNO (regola D)*: eredita lo spinore COMPLESSO col segno, non un Bloch ri-derivato. `segno = +1` per la mitosi; `-1` per l'antinodo (doppia copertura opposta)
- **`_spinor_lift`** — *eredita col SEGNO (regola D)*: il sollevamento, con la stessa convenzione di segno di `_psi_spinor`
- **`conc_nodi`** — *eredita la concorrenza del genitore `a`*: ### QUESTA REGOLA CURA LA CRESCITA PER MUTAZIONE: prima `conc_nodi` era l'UNICA grandezza del registro che cresceva con `.append`, cioe' INVISIBILE all'AST e alla sorveglianza. Ora e' una SCRITTURA VERA. ### E IL `len` CRESCENTE SI CONSERVA: `.append` dentro il ciclo faceva crescere `len(self.conc_nodi)` a ogni giro, quindi un `kk` scartato all'inizio poteva passare il test piu' tardi. Si costruisce la lista nuova e si appende A QUELLA, non alla vecchia: stesso comportamento, anche nel caso limite
- **`eta`** — *zero*: il figlio nasce senza `eta`
- **`mem_mot`** — *eredita dal genitore `a`*: la memoria di moto del padre; se la memoria non c'e' ancora, zeri
- **`omega_s`** — *eredita dal genitore `a`*: il ritmo spinoriale del padre
- **`perc_chi`** — *eredita la chiralita' del genitore `a`*: [CHI_COOP via 2 di 3] profilo dormiente, non ancora accoppiato. ### E QUESTO RAMO SPOSTA `N(+1) - N(-1)` DI `+segno(perc_chi[a])` PER FIGLIO: aggiunge un nodo dello STESSO segno del genitore. L'altro ramo (Schwinger) lo sposta nel verso OPPOSTO, e ### ⚠ I DUE SI CANCELLANO SOLO SUGLI ARCHI DOVE SCATTANO ENTRAMBI: la conservazione e' DELLA COPPIA, non della somma dei due rami. ### MISURATO: 9 contro 1 in 72 passi, cioe' +8. ### Per questo i nati si contano DUE volte e non una: un totale non direbbe da dove viene la carica.
- **`perc_tw`** — *zero*: salto a 0: il profilo di torsione percorso riparte
- **`phi0`** — *media (come `phi`)*: la fase di riferimento nasce DOVE nasce la fase: lo stesso `fm`
- **`phi_s`** — *eredita dal genitore `a`*: lo spinore di fase del padre -- ed e' il COMPAGNO di `psi_spin`, che eredita per la stessa ragione
- **`phivel`** — *media dei genitori*: la velocita' di fase media. SOMMA DI DUE ADDENDI: in IEEE-754 l'addizione e' COMMUTATIVA, quindi l'ordine dei due genitori NON cambia un bit (misurato). Da TRE addendi non lo sarebbe
- **`pos`** — *media dei genitori (punto medio)*: il figlio nasce sul punto medio geometrico; l'asimmetria della mitosi diretta vive nella FASE, non nella posizione
- **`psi`** — *media dei genitori (come `phi`)*: e la somma e' COMPLESSA: due genitori in antifase danno un figlio con `\|psi\| ~ 0`. E' interferenza distruttiva, cioe' FISICA, non un errore. SI CONTA e non si assume (`A8`): se la cache non e' allineata a `n0` non si puo' ereditare, e quel salto e' cio' che faceva spegnere la schermatura per TUTTA la rete (`PSI-FLASH`)
- **`psi_spin`** — *eredita da `a` (come `phi_s`)*: eredita, non media: il compagno `phi_s` eredita
- **`rho_spin`** — *eredita da `a` (come `psi_spin`)*: [PSI-FLASH] `rho_spin` COME `psi_spin`, e NON e' un'aggiunta ovvia: senza, `_rho_sorgente` prendeva il suo ripiego AL PASSO DOPO la nascita e restituiva `\|psi\|^2` invece di `rho_spin` PER TUTTA LA RETE -- il GRADINO del +11%. Sono la stessa grandezza vista in due modi, `rho_spin = psi_spin^dag psi_spin`
- **`_rep`** — *eredita dall'arco che si spezza*: `_rep` e' per ARCO e segue la STESSA struttura degli altri array per arco: NON si eredita da `src` come gli stati per NODO. I due archi figli ereditano la memoria dell'arco da cui nascono, che e' cio' che `[sel], [sel]` fa
- **`d`** — *meta' dell'arco (due tronconi)*: `dh` e' ora i DUE BLOCCHI (`t*d[sel]` per `a`-`m` e `(1-t)*d[sel]` per `m`-`b`), passati per `_nasce('mitosi', 1, 0, meta=len(dh_a))`: `md = 1` e non 2 perche' ogni voce e' ora UN arco vero, e `meta` fa calcolare `_fab` PER META' cosi' `_sm_lun` resta identico al bit. Nella preparazione: e' il dimezzamento che produce la compressione degenere, perche' la geometria di equilibrio si accorcia a ogni suddivisione
- **`d0`** — *meta' dell'arco, con offset plastico*: con `PLAST_DIN` l'offset e' emergente (stress metrico per eccesso di torsione, saturato); con `PLAST_MIT > 0` e' proporzionale a `sciolta`; altrimenti e' `dh` nudo. `d0new` e' GIA' i DUE BLOCCHI (dai due mezzi `dh_a` e `dh_b`, nello stesso ordine), cioe' i due figli, e passa per `_nasce('mitosi', 0, 1)`. ### ⚠ E IL NOME `sciolta` PRESUPPONE UNA COSA NON MISURATA: `sciolta` e' solo `\|tw\|/PHI_CRIT`, cioe' LA TORSIONE DELL'ARCO IN UNITA' DEL QUANTO -- e <<sciolta>> suggerisce che sia stata LIBERATA e spesa da qualche parte. ### NON LO E': vedi la regola di `tw` e `DIVISIONE-AUTOCONSISTENTE:M1`. ### Il nome NON si cambia qui (sarebbe una riga di logica in un commit di soli commenti): e' IN CODA.
- **`peq`** — *eredita dall'arco che si spezza*: ### L'EREDITA' DELLA MITOSI NON SI TOCCA, e il perche' e' una frase di `PEQ_NASCITA_LOCALE`: *un arco che si spezza non NASCE, CONTINUA*. Per questo qui non c'e' `nan` e nello Schwinger si'
- **`_peqn_idx`** — *non si tocca*: la marca degli archi nati con `peq = nan` esiste SOLO per lo Schwinger: la mitosi non ne crea (eredita `peq`, non lo lascia da calibrare). DICHIARATO, non omesso
- **`tw`** — *zero*: i due tronconi nascono con `tw = 0`: la torsione dell'arco SPARISCE. ### IL CALCIO LA USA COME MISURA MA NON LA CONSERVA: `\|tw\|` decide QUANTO colpire i genitori, e l'avvolgimento NON viene trasferito -- MISURATO: `DIVISIONE-AUTOCONSISTENTE:M1`, ~1.2 giri persi per arco diviso, SENZA BILANCIO. Se debba conservarsi e' `DIVISIONE-AUTOCONSISTENTE`, APERTA. ### ⛔ E LA FRASE DI PRIMA ERA FALSA, e la lascio scritta perche' un errore non si cancella (par.8): diceva che la torsione era <<SCIOLTA dalla divisione, ed e' cio' che il calcio ha SPESO>>, cioe' DAVA PER RISOLTA una domanda aperta. Rilievo del guardiano, 2026-10-03.
- **`perc_geom`** — *DERIVATA dalla definizione (non eredita)*: [COMMIT 5, decisione di Luca del 2026-09-29] ### NON SI EREDITA PIU': la geometria e' *<<il giro e' compiuto o no>>*, e questo si LEGGE dagli archi del nodo -- la media di `\|tw\|` contro `PHI_CRIT`, la STESSA definizione di `chi_basc`. Un valore EREDITATO poteva CONTRADDIRE la definizione, e per un passo il frame-drag lo leggeva. ### Il nato ha archi con `tw = 0`, quindi OGGI la derivazione da' `-1`; scritta come DERIVAZIONE e non come costante resta giusta quando `DIVISIONE-AUTOCONSISTENTE` dara' ai figli una torsione
- **`twp`** — *differenza di fase genitore-figlio*: ### VINCOLO 1 DEL CONTRATTO: legge `phi[a]`/`phi[b]` DOPO il calcio, che e' una scrittura INDICIZZATA sui genitori -- quindi `phi` deve stare PRIMA, e nell'ordine del registro ci sta (`METRI` precede `STATO`)
- **`vd`** — *eredita dall'arco che si spezza*: la velocita' metrica dell'arco si eredita come `_rep` e `peq`
- **`_smp_d0`** — *collocata*: [SCALA_MIN_PASSO C3 / COES_CAUSALE C4] la fotografia di inizio passo subisce LE STESSE operazioni di `d0`, altrimenti un confronto `fine - inizio` per posizione confronterebbe ARCHI DIVERSI. NON e' una regola di nascita: e' una CHIRURGIA sullo snapshot, e si colloca nella preparazione perche' legge solo `keep` e `d0new`
- **`_smp_d`** — *collocata*: [SCALA_MIN_PASSO C3 / COES_CAUSALE C4] la fotografia di inizio passo subisce LE STESSE operazioni di `d0`, altrimenti un confronto `fine - inizio` per posizione confronterebbe ARCHI DIVERSI. NON e' una regola di nascita: e' una CHIRURGIA sullo snapshot, e si colloca nella preparazione perche' legge solo `keep` e `d0new`


# **EVENTO `schwinger`**

| # | grandezza | classe | regola | ancora |
|---|---|---|---|---|
| 0 | **`phi`** | ✅ regola | antifase del figlio di mitosi | `self.phi = np.concatenate([self.phi, anti])` |
| 1 | **`i`** | ✅ regola | topologia: due archi nuovi verso i genitori | `self.i = np.concatenate([self.i, aa, k])` |
| 2 | **`j`** | ✅ regola | topologia: due archi nuovi verso i genitori | `self.j = np.concatenate([self.j, k, bb])` |
| 3 | **`_cs_nodo_prev`** | ✅ regola | eredita dal genitore `aa` | `self._cs_nodo_prev = np.concatenate([_csp, np.asarray(_csp, float)[src]])` |
| 4 | **`_deg`** | 🔧 collocata | collocata | `self._grado()` |
| 5 | **`_nb`** | ✅ regola | eredita dal genitore `aa` | `self._nb = np.vstack([self._nb, self._nb[src]])` |
| 6 | **`_nb_prec`** | ✅ regola | eredita dal genitore `aa` | `self._nb_prec = np.vstack([self._nb_prec, self._nb_prec[src]])` |
| 7 | **`_nb_ret`** | ✅ regola | eredita dal genitore `aa` | `self._nb_ret = np.vstack([_nbr_er, _nbr_er[src]])` |
| 8 | **`_psi_prec`** | ✅ regola | eredita dal genitore `aa` | `self._psi_prec = np.concatenate([self._psi_prec, self._psi_prec[src]])` |
| 9 | **`_psi_spin_prec`** | ✅ regola | eredita dal genitore `aa` | `self._psi_spin_prec = np.vstack([_pspr, np.asarray(_pspr)[src]])` |
| 10 | **`_psi_spinor`** | ✅ regola | eredita INVERTITA (antichirale) | `er = self._psi_spinor[src].copy(); er = -er` |
| 11 | **`_spinor_lift`** | ✅ regola | eredita INVERTITA (antichirale) | `el = self._spinor_lift[src].copy(); el = -el` |
| 12 | **`conc_nodi`** | ✅ regola | eredita la concorrenza di `aa`, MARCATA `schwinger` | `eredita = [[v[0], v[1], v[2], "schwinger"] if len(v) == 3 else v[:] for v in eredita]` |
| 13 | **`eta`** | ✅ regola | zero | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` |
| 14 | **`mem_mot`** | ✅ regola | zero | `self.mem_mot = np.vstack([self.mem_mot, np.zeros((nc, 3))]) if len(...) else np.zeros((nc, 3))` |
| 15 | **`omega_s`** | ✅ regola | eredita dal genitore `aa` | `self.omega_s = np.vstack([self.omega_s, self.omega_s[src]])` |
| 16 | **`perc_chi`** | ✅ regola | eredita INVERTITA (la CARICA si coniuga) | `self.perc_chi = np.concatenate([self.perc_chi, -self.perc_chi[aa]])` |
| 17 | **`perc_tw`** | ✅ regola | zero | `self.perc_tw = np.concatenate([self.perc_tw, np.zeros(nc)])` |
| 18 | **`phi0`** | ✅ regola | antifase (come `phi`) | `self.phi0 = np.concatenate([self.phi0, anti])` |
| 19 | **`phi_s`** | ✅ regola | zero | `self.phi_s = np.concatenate([self.phi_s, np.zeros(nc)])` |
| 20 | **`phivel`** | ✅ regola | media dei genitori | `self.phivel = np.concatenate([self.phivel, 0.5 * (self.phivel[aa] + self.phivel[bb])])` |
| 21 | **`pos`** | ✅ regola | media dei genitori (punto medio) | `self.pos = np.vstack([self.pos, (1-FRAZ_NASCITA) * self.pos[aa] + FRAZ_NASCITA * self.pos[bb]])` |
| 22 | **`psi`** | ✅ regola | media dei genitori (come `phi`) | `self.psi = np.concatenate([cur[:n0], 0.5 * (cur[a] + cur[b])])` |
| 23 | **`psi_spin`** | ✅ regola | eredita da `aa` (come `phi_s`... che qui e' zero) | `self.psi_spin = np.concatenate([cs[:n0], cs[a]])` |
| 24 | **`rho_spin`** | ✅ regola | eredita da `aa` (come `psi_spin`) | `self.rho_spin = np.concatenate([np.asarray(rs)[:n0], np.asarray(rs)[a]])` |
| 25 | **`_rep`** | ✅ regola | zero (archi NUOVI) | `self._rep = np.concatenate([self._rep, np.zeros(2 * nc)])` |
| 26 | **`d`** | ✅ regola | meta' della distanza fra i genitori | `self.d = np.concatenate([self.d, dd])  # `dd` e' GIA' i due blocchi` |
| 27 | **`d0`** | ✅ regola | meta' della distanza fra i genitori | `self.d0 = np.concatenate([self.d0, dd])  # `dd` e' GIA' i due blocchi` |
| 28 | **`peq`** | ✅ regola | `nan` = da calibrare sul PROPRIO arco | `self.peq = np.concatenate([self.peq, np.full(2 * nc, pmed)])` |
| 29 | **`_peqn_idx`** | ✅ regola | la marca degli archi nati con `nan` | `self._peqn_idx = np.arange(len(self.peq) - 2 * nc, len(self.peq))` |
| 30 | **`tw`** | ✅ regola | zero | `self.tw = np.concatenate([self.tw, zz2, zz2])` |
| 31 | **`perc_geom`** | ✅ regola | DERIVATA dalla definizione (non eredita) | `self.perc_geom = np.concatenate([self.perc_geom, _derivazione_perc_geom(self, c)])` |
| 32 | **`twp`** | ✅ regola | differenza di fase genitore-antinodo | `self.twp = np.concatenate([self.twp, self._wphi(self.phi[aa] - anti), self._wphi(anti - self.phi[bb])])` |
| 33 | **`vd`** | ✅ regola | zero (archi NUOVI) | `self.vd = np.concatenate([self.vd, np.zeros(2 * nc)])` |
| 34 | **`_smp_d0`** | 🔧 collocata | collocata | `self._smp_chirurgia(nuovi=dd)  # `dd` e' GIA' i due blocchi` |
| 35 | **`_smp_d`** | 🔧 collocata | collocata | `self._smp_chirurgia(nuovi=dd)  # `dd` e' GIA' i due blocchi` |

## Le derivazioni, evento `schwinger`

- **`phi`** — *antifase del figlio di mitosi*: [FASE_2PI, D35] L'ANTIFASE E' META' DEL DOMINIO: `+pi` su 2pi, `+2pi` su 4pi. Con `phi` su 4pi il `+2pi` NON e' un'antifase -- il campo legge `exp(i phi)` e l'antiparticella sarebbe IDENTICA alla particella
- **`i`** — *topologia: due archi nuovi verso i genitori*: l'antinodo si allaccia a ENTRAMBI i genitori: `aa-k` e `k-bb`. Nessun arco sparisce (non c'e' `keep`): la coppia AGGIUNGE
- **`j`** — *topologia: due archi nuovi verso i genitori*: il compagno di `i`
- **`_cs_nodo_prev`** — *eredita dal genitore `aa`*: la stessa regola della divisione, col genitore `aa`: fuori dalla guardia sugli spinori, per la stessa ragione
- **`_deg`** — *collocata*: come nella divisione: una DERIVATA della topologia, collocata dopo il blocco perche' legge `i`, `j` e `len(phi)`
- **`_nb`** — *eredita dal genitore `aa`*: e il suo esito resta la condizione di `_nb_prec`, come nella divisione
- **`_nb_prec`** — *eredita dal genitore `aa`*: SOLO SE `_nb` e' stata estesa
- **`_nb_ret`** — *eredita dal genitore `aa`*: il Bloch ritardato del genitore
- **`_psi_prec`** — *eredita dal genitore `aa`*: evita il reset spurio globale in `ritmo()`
- **`_psi_spin_prec`** — *eredita dal genitore `aa`*: lo snapshot del ritmo spinoriale a 4pi
- **`_psi_spinor`** — *eredita INVERTITA (antichirale)*: ### `segno = -1`: doppia copertura OPPOSTA, coerente con `perc_chi = -perc_chi[genitore]`. E' la regola `eredita INVERTITA` del piano, e l'unica dove il segno conta
- **`_spinor_lift`** — *eredita INVERTITA (antichirale)*: la stessa convenzione di segno di `_psi_spinor`
- **`conc_nodi`** — *eredita la concorrenza di `aa`, MARCATA `schwinger`*: se `aa` concorre a una massa, l'antinodo vi concorre pure (categoria *creazione di coppie* = accrescimento); se `aa` non concorre a nulla, l'antinodo resta senza concorrenza (materia nuova dal vuoto teso). ### ⚠ E LA FRASE DI PRIMA AFFERMAVA UN TRASFERIMENTO CHE NESSUNO HA MISURATO: diceva che <<la Schwinger DRENA tensione di una massa esistente>>. ### QUESTA REGOLA NON DRENA NIENTE: copia la lista di concorrenza del genitore e le aggiunge una MARCA `schwinger`. Che la creazione di coppia dreni la tensione della massa e' una LETTURA FISICA PLAUSIBILE, non una misura -- e il bilancio della torsione alla nascita e' `DIVISIONE-AUTOCONSISTENTE`, APERTA. Rilievo del guardiano, 2026-10-03. ### E qui pure la mutazione diventa SCRITTURA, col `len` crescente conservato
- **`eta`** — *zero*: l'antinodo nasce senza `eta`
- **`mem_mot`** — *zero*: ### E QUI LA REGOLA E' DIVERSA DALLA MITOSI, ed e' dichiarata: il figlio della divisione EREDITA la memoria di moto del padre, l'antinodo nasce con memoria NULLA -- non continua un moto, comincia
- **`omega_s`** — *eredita dal genitore `aa`*: il ritmo spinoriale del genitore
- **`perc_chi`** — *eredita INVERTITA (la CARICA si coniuga)*: ### l'antiparticella nasce con chiralita' OPPOSTA al genitore: `-perc_chi[aa]`. ### QUINDI QUESTO SINGOLO NODO SPOSTA `N(+1) - N(-1)` DI `-segno(perc_chi[aa])`, non di zero. ### ⚠ LA CONSERVAZIONE E' DELLA COPPIA, NON DEL RAMO, E LA COPPIA NON SI FORMA SEMPRE: la mitosi aggiunge un figlio dello STESSO segno, lo Schwinger un antinodo OPPOSTO, e i due si cancellano SOLO sugli archi dove scattano ENTRAMBI -- e lo Schwinger scatta su un SOTTOINSIEME (`pick`). ### E I CONTATORI DEL REPO LO DICONO: 72 passi, seme 11 -> `_g_nati_mitosi = 9` contro `_g_nati_schwinger = 1`, cioe' `N(+1) - N(-1)` si e' spostato di +8 in quel run (`csv/_test_fork/_sonda_commit3/_sonda_commit3.json`, `nati_dopo`). ### ⛔ E LA FRASE DI PRIMA DICEVA <<E' IL RAMO CHE CONSERVA, la coppia e' NEUTRA e `N(+1) - N(-1)` NON cambia>>: era VERA DELLA COPPIA e FALSA DEL RAMO, e i due contatori esistono proprio per distinguerle. Rilievo del guardiano, 2026-10-03.
- **`perc_tw`** — *zero*: salto a 0
- **`phi0`** — *antifase (come `phi`)*: la fase di riferimento nasce dove nasce la fase
- **`phi_s`** — *zero*: ### E QUI PURE LA REGOLA E' DIVERSA DALLA MITOSI: il figlio della divisione EREDITA `phi_s` dal padre, l'antinodo nasce a ZERO -- inerte se lo spinore di fase e' spento
- **`phivel`** — *media dei genitori*: come nella divisione: due addendi, e in IEEE-754 l'addizione di DUE addendi e' commutativa al bit
- **`pos`** — *media dei genitori (punto medio)*: l'anti-nodo e' collocato sul punto medio COME il nodo, cosi' i due nascono SOVRAPPOSTI e la dinamica (antifase -> repulsione) li separa da se'. ### NON si impone alcuna forza: solo la fase opposta
- **`psi`** — *media dei genitori (come `phi`)*: [PSI-FLASH] lo STESSO per il canale di Schwinger: i genitori sono `aa`/`bb`. ### E IL SEGNO NON SI TOCCA: `psi` e' un campo COMPLESSO, e l'antinodo nasce a fase `anti = fm + pi`, cioe' il segno e' GIA' nella sua fase
- **`psi_spin`** — *eredita da `aa` (come `phi_s`... che qui e' zero)*: la regola e' la stessa della divisione, e NON segue `phi_s` in questo evento: `phi_s` dell'antinodo e' zero, `psi_spin` eredita. ### E' una ASIMMETRIA DI OGGI, dichiarata qui invece che nascosta -- il commit 3 SPOSTA, non cura
- **`rho_spin`** — *eredita da `aa` (come `psi_spin`)*: coerente con `psi_spin`: sono la stessa grandezza vista in due modi
- **`_rep`** — *zero (archi NUOVI)*: ### E QUI LA REGOLA E' DIVERSA DALLA MITOSI: i due tronconi della divisione EREDITANO la memoria dell'arco che si spezza (`[sel], [sel]`); gli archi della coppia NASCONO, e nascono senza memoria
- **`d`** — *meta' della distanza fra i genitori*: `dd` e' ora i DUE BLOCCHI: `max(t*L, 0.05)` per `aa`-`k` e `max((1-t)*L, 0.05)` per `k`-`bb`, con `L = norm(pos[aa]-pos[bb])`, per `_nasce('schwinger', 2, 2)`. ### E la lunghezza viene da `pos`, non da `d`: e' la voce `A3` della coda. `norm(..., axis=1)` somma TRE componenti in ordine FISSO, quindi non dipende dall'ordine
- **`d0`** — *meta' della distanza fra i genitori*: ### LO STESSO `dd` di `d`: e' il QUARTO SITO di `_nasce`, `x2` su ENTRAMBE le grandezze -- l'arco della coppia nasce A RIPOSO, cioe' `d == d0`, e quindi senza stress
- **`peq`** — *`nan` = da calibrare sul PROPRIO arco*: [PEQ_NASCITA_LOCALE, C2] `nan` significa *da calibrare sulla `rho` del PROPRIO arco*, ed e' la STESSA convenzione di `_allaccia`: `step` lo fa all'inizio del passo dopo, e da' `anom = 0` ESATTO alla nascita. ### Il ramo storico prendeva `median(self.peq)`, una statistica GLOBALE dentro una legge locale (`A2`)
- **`_peqn_idx`** — *la marca degli archi nati con `nan`*: ### VINCOLO 2 DEL CONTRATTO: gli indici si riferiscono all'array FINALE, quindi questa regola DEVE girare DOPO `peq` -- ed e' per questo che `_peqn_idx`, che in nessun registro sta, e' DICHIARATO subito dopo `peq` in `ORDINE_DI_NASCITA`. Serve a distinguere QUESTI `nan` da quelli di `_allaccia`, che la SEMINA scrive su TUTTI gli archi al primo passo
- **`tw`** — *zero*: gli archi della coppia nascono senza torsione
- **`perc_geom`** — *DERIVATA dalla definizione (non eredita)*: [COMMIT 5, decisione di Luca del 2026-09-29] ### LA SCELTA VECCHIA ERA DICHIARATA E NON OVVIA -- la CARICA nasce opposta (e' antimateria), la GEOMETRIA copiata tale e quale -- e la decisione di Luca la SUPERA ALLA RADICE: la geometria non si EREDITA affatto, ne' diritta ne' coniugata, perche' si LEGGE dagli archi del nodo (media di `\|tw\|` contro `PHI_CRIT`, la definizione di `chi_basc`). ### Cosi' la domanda *<<si coniuga o no?>>* non si pone: non e' una carica, e' una MISURA sugli archi
- **`twp`** — *differenza di fase genitore-antinodo*: legge `phi[aa]`/`phi[bb]`, che sono GENITORI: l'estensione di `phi` non li tocca, quindi qui l'arco e' INERTE (misurato). Ma l'ordine resta quello del registro, che e' lo stesso di prima
- **`vd`** — *zero (archi NUOVI)*: come `_rep`: nascono fermi, non continuano un moto
- **`_smp_d0`** — *collocata*: [SCALA_MIN_PASSO C3] lo snapshot segue anche lo Schwinger, e qui SENZA `keep`: la coppia aggiunge archi e non ne toglie
- **`_smp_d`** — *collocata*: [SCALA_MIN_PASSO C3] lo snapshot segue anche lo Schwinger, e qui SENZA `keep`: la coppia aggiunge archi e non ne toglie

