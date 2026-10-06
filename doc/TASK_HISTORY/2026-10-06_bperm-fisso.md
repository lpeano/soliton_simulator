# `Bperm-fisso` — **la permutazione ripescata SOLO quando `len(avv)` cambia**

*(Mandato: l'annotazione del guardiano `f922c20`, che ha fissato questo braccio ### **PRIMA di
vedere i numeri di `Bperm`**, e il prompt del 2026-10-06 che mette le due misure in sequenza.
Il simulatore ### **NON si tocca**: resta `f7237563`.)*

> ### 📌 **PERCHE' QUESTO BRACCIO ESISTE.** `Bperm` ha dato ### **`P1` su entrambi i criteri**
> *(divisioni `1.5741x`, finestra `1.1009x`)*, e la regola fissata in `f922c20` dice che `P1`
> rende il risultato ### **AMBIGUO** fra *«non conta QUALE arco»* e *«LOTTERIA»*.
> ### ⛔ **Questo braccio non e' una scelta fatta dopo i numeri: era dovuto.**

---

## LA STELLA POLARE — le cinque domande

| | risposta |
|--:|---|
| **1 `A14`** | ### **NON SI APPLICA, e il perche':** questo commit ### **non introduce nessuna legge.** La patch sostituisce **una riga** del calcolo della soglia con la **stessa** riga a morso permutato: non c'e' nessun flusso di energia o carica, perche' la soglia e' un **criterio di decisione**, non una grandezza conservata. ### **E il simulatore non cambia: la patch vive in una COPIA.** |
| **2 i tre gradini** | ### **(a) ROBUSTO AL RUMORE NUMERICO, e non oltre.** Tre semi di permutazione, e le barre si leggono ### **fra semi** *(`P3`)*. ### ⛔ **Non arriva al gradino (b)** — non toglie nessuna legge pratica — ### **ne' al (c)**, perche' non esiste un limite noto della soglia di mitosi con cui confrontarsi. ### ⚠ **E il conteggio ASSOLUTO dipende dalla piattaforma** *(`STELLA_POLARE`)*: si leggono **rapporti**, misurati sulla **stessa** piattaforma `Windows 11 / numpy 2.3.0`. |
| **3 un numero o una legge?** | ### **NESSUNO DEI DUE, e il perche':** i tre semi `101`/`202`/`303` sono **semi di un dado**, non costanti di accoppiamento — ### **non entrano in nessuna legge, e cambiarli cambia solo il campione.** La soglia `P1 = 0.5` / `P2 = 0.2` e' un **criterio di lettura** fissato prima, non un parametro del sistema. ### ⛔ **E il `0.3` che si sta misurando resta COM'E': questa misura non lo tocca.** |
| **4 `rho`, `c_s`, il segno?** | ### **NON SI APPLICA, e il perche':** la patch tocca **solo** `soglia` dentro `decidi_divisione`. ### **Non legge e non scrive `rho`, `cs`, `psi` ne' nessun segno di accoppiamento** — e `grad_modula`, che e' l'unica grandezza di tempo proprio in gioco, viene **letto** e non modificato. |
| **5 emergente o imposto?** | ### **E' ESATTAMENTE LA DOMANDA DI QUESTA MISURA**, e per questo non si risponde qui. `Bperm` ha mostrato che le nascite ### **non crollano** togliendo il legame arco-gradiente; `Bperm-fisso` chiede se quel risultato ### **sopravvive togliendo la LOTTERIA** — cioe' se e' il legame o il rumore a non contare. ### ⛔ **La risposta e' il referto, e non la scrivo prima.** |

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare*

### ✔ **IL FATTO MISURATO che fa partire tutto** *(e non e' una stima)*

Nel braccio `Bp` committato *(`dd86933`)*, `len(avv)` cambia ### **12 volte su 150 passi**, e
assume **13 valori distinti**. ### ⚠ **E I DODICI CAMBI STANNO TUTTI DOPO IL PASSO 100:**
`100, 112, 117, 121, 127, 128, 137, 140, 141, 144, 148, 149`.

> ### 📌 **QUINDI `Bperm-fisso` NON E' <<`Bperm` con meno lotterie>>: per i PRIMI CENTO PASSI
> ha UNA SOLA permutazione, fissa.** E' una differenza **qualitativa**, non un fattore
> `11.5` -- ### **e questa e' la prima cosa che ho imparato guardando i dati invece di
> ricopiare il mio stesso conto.**

### CHE COSA CREDO

| | |
|---|---|
| **la mia previsione** | ### **`Bperm-fisso` TORNA verso `Bp`:** rapporto delle divisioni fra **`0.764`** e **`1.236`** *(la banda e' **derivata**, non scelta: vedi sotto)* |
| **il ragionamento** | se il morso di un arco resta **lo stesso per tutta la corsa**, la **distribuzione** delle soglie fra gli archi e' quella di `Bp` e cambia solo ### **a chi** tocca. Il numero di archi sotto una soglia data, a ogni passo, e' **statisticamente lo stesso**. ### **Quindi l'eccesso di `Bperm` sarebbe tutto LOTTERIA** |
| **la banda, DERIVATA** | `Bp` fa **`18`** divisioni; il rumore di conteggio e' `1/sqrt(18)` = ### **`0.2357`**, quindi `1 ± 0.2357` = **`[0.764, 1.236]`**. ### ⛔ **Non e' un numero scelto a mano** *(`P1-sexies`)*, ed e' **larga** perche' `18` eventi sono pochi: per questo si guarda anche la **finestra**, dove `1/sqrt(7738)` = `0.0114` da' **`[0.9886, 1.0114]`** |

### ⛔ **COSA NON SO, e lo scrivo adesso**

1. ### **Se l'identita' degli archi si conserva mentre `len(avv)` NON cambia.** Il simulatore
   **FILTRA** gli archi *(`self.i = concatenate([self.i[keep], a, m])`)*, quindi
   ### ⚠ **un passo che toglie `k` archi e ne aggiunge `k` lascia `len(avv)` INVARIATO e
   RI-ETICHETTA la mappa arco→morso in silenzio.** ### **Non lo so, e non lo assumo: lo
   MISURO** *(controllo `C-ident`, sotto)*.
2. **Quanto vale la dispersione fra semi di `Bperm-fisso`.** In `Bperm` era `1.25` su `28.33`
   *(il `4.4 %`)*, ### **ma con una permutazione sola per corsa i tre semi potrebbero
   separarsi MOLTO di piu'**: un seme sfortunato puo' dare il morso grande a un arco che non
   si avvicina mai alla soglia, e con `13` estrazioni invece di `150` non c'e' niente che
   medi. ### **Se la dispersione esplodesse, tre semi non basterebbero, e lo direi** *(`P3`:
   per una barra servono almeno quattro semi)*.
3. **Se la mia previsione e' giusta.** ### ⛔ **L'ULTIMA L'HO SBAGLIATA** *(`Bperm`: previsto
   crollo, misurato `1.5741x`)*, e il motivo era che avevo ragionato su un `q05` che era un
   effetto di **SELEZIONE**. ### **Lo scrivo qui perche' chi legge pesi questa previsione per
   quello che vale.**

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *i passi, e cosa decide ciascuno*

### LA PATCH: **una riga in piu' di `Bperm`, e nient'altro**

```
            _bite = 0.3 * np.tanh(grad_modula)
            if _PERM_CACHE[0] != len(_bite):          #  <-- SOLO QUESTE TRE RIGHE
                _PERM_CACHE[0] = len(_bite)           #      sono nuove rispetto a `Bperm`
                _PERM_CACHE[1] = _PRNG.permutation(len(_bite))
            _p = _PERM_CACHE[1]
            _bite_perm = _bite[_p]
            soglia = soglia0 * (1.0 - _bite_perm)
```

### ✔ **E `len(_bite)` E' `len(avv)`, verificato dal codice e non assunto:**
`avv = np.abs(self.tw)` *(`:8303`)* e `grad_modula = np.abs(_rn[self.i] - _rn[self.j])`
*(`:8374`)* hanno ### **entrambe la lunghezza del numero di archi**. Quindi *«ripescata solo
quando `len(avv)` cambia»* e *«quando `len(_bite)` cambia»* sono ### **la stessa condizione.**

### I CRITERI, **fissati PRIMA** — gli stessi di `Bperm`, piu' la lettura della lotteria

| id | su che cosa | come si legge |
|---|---|---|
| **`P1`** | rapporto `>= 0.5` | il legame col gradiente **NON** e' portante |
| **`P2`** | rapporto `<= 0.2` | il legame **E'** portante |
| **`P3`** | fra `0.2` e `0.5` | lettura **intermedia** |

### ⛔ **E LA LETTURA DELLA LOTTERIA, FISSATA ORA, prima dei numeri**

| id | se | la lettura |
|---|---|---|
| **`L-A`** | `fisso/Bp` **dentro** `[0.764, 1.236]` **e** `perm/Bp` **sopra** `1.236` | ### **L'ECCESSO DI `Bperm` ERA LA LOTTERIA.** La lettura pulita e' *«non conta QUALE arco»*, e ### **il `0.3` agisce come abbassamento della soglia** |
| **`L-B`** | `fisso/Bp` e `perm/Bp` **indistinguibili** *(entro la dispersione fra semi)*, **entrambi** sopra `1.236` | ### **LA LOTTERIA NON C'ENTRA.** La salita viene dalla permutazione in se', e ### **va capita: nessuna delle due spiegazioni basta** |
| **`L-C`** | `fisso/Bp` **sotto** `0.764` | ### ⛔ **IL LEGAME ARCO-GRADIENTE PORTA QUALCOSA**, e `Bperm` lo aveva **NASCOSTO** dietro la lotteria. Il risultato di `Bperm` non era solo ambiguo: era ### **FUORVIANTE** |
| **`L-D`** | nessuno dei tre *(per esempio `fisso` dentro la banda **e** `perm` dentro la banda)* | ### **non si forza una lettura:** si riporta il numero e si dice che ### **la tavola non lo copre** |

### I CONTROLLI — **i quattro di `Bperm`, piu' uno che misura il limite che ho dichiarato**

| id | che cosa | deve |
|---|---|---|
| **`C-perm-0`** | il braccio `Bperm-fisso-id`, con la permutazione **IDENTICA** *(`arange`)*, riproduce `Bp` | ### **PASSARE** *(e' un no-op aritmetico)* |
| **`C-distr`** | il **multiinsieme** dei morsi prima/dopo e' identico a **ogni** passo | ### **PASSARE** |
| **`C1`** | il censimento dei cancelli ricostruisce `nati` del simulatore | ### **COINCIDERE** |
| **`C-rng`** | `len(avv)` coincide con `Bp` finche' la topologia non si separa; **mai** diverso per il braccio identico | — |
| **`C-ident`** | ### **NUOVO:** a ogni passo si tiene l'**impronta `sha1` dei byte di `net.i` e `net.j`**, e si conta ### **quanti passi hanno `len(avv)` INVARIATO ma l'insieme degli archi CAMBIATO** | ### **si RIPORTA**, non ferma: e' la **misura** del limite, non una prova. Se fosse `> 0`, *«la permutazione e' fissa»* sarebbe ### **falso su quei passi**, e il referto lo direbbe |
| **`C-lotterie`** | ### **NUOVO:** si contano le permutazioni **effettivamente estratte** | ### **deve essere `13`** su `Bp`-equivalenti, e si riporta il numero vero per ogni braccio |

### ⛔ **CHE COSA MI FAREBBE FERMARE**

`C-perm-0`, `C-distr` o `C1` che falliscono ⟹ ### **`FERMO`**, si committa il fallimento e la
correzione e' **un commit a se'** *(par.5)*.

### ⚠ **E IL LIMITE DI QUESTO BRACCIO RESTA QUELLO CHE HO SCRITTO PRIMA DI VEDERE `Bperm`**

> Ripescare solo alla crescita ### **lega la permutazione alla TOPOLOGIA.** ### **Riduce la
> lotteria, non la toglie, e cambia una cosa per un'altra.** Il confronto fra i due bracci
> dice **quanto** pesa la lotteria; ### ⛔ **NESSUNO DEI DUE E' IL BRACCIO <<PULITO>>**, e il
> referto lo ripete accanto ai numeri.

---

## ⛔ ANNOTAZIONE DEL 2026-10-06 — **LE BANDE ERANO TROPPO STRETTE, in due modi**

*(Correzione del guardiano al blob `1bf6fe2`. ### **La banda originale qui sopra NON si
cancella** -- il par.8 vuole che resti -- e queste sono ### **fissate PRIMA della corsa**.
I conti li ho ### **rifatti io**, e ne esce anche **un errore nel suo**.)*

### ✔ **IL PRIMO PUNTO: `1/sqrt(18)` E' UNA SOLA DEVIAZIONE STANDARD**

| | |
|---|---|
| **la mia banda** | `1 ± 1/sqrt(18)` = `[0.7643, 1.2357]` |
| **il difetto** | e' **`1 sigma`**. ### ⛔ **Anche con la previsione GIUSTA, un conteggio cade fuori da `1 sigma` il `31.7 %` delle volte** -- cioe' **una volta su tre**. Un criterio che boccia un'ipotesi vera un terzo delle volte **non e' un criterio** |
| **la banda CORRETTA** | `1 ± 2/sqrt(18)` = `0.4714` ⟹ ### **`[0.5286, 1.4714]`**, cioe' `[0.53, 1.47]` *(fuori il `~4.6 %` delle volte)* |

### ✔ **IL SECONDO PUNTO, ed e' il piu' grave: `1/sqrt(7738)` ASSUME L'INDIPENDENZA**

`7738` sono **passi-arco**, non eventi indipendenti: ### **lo stesso arco resta nella finestra
per molti passi consecutivi.** La statistica efficace e' ### **molto** piu' piccola, e
`1/sqrt(7738)` = `0.0114` ### ⛔ **e' una banda FINTA: lo `1.1 %`, quando il rumore vero
misurato e' il DOPPIO.**

### ✔ **E IL RUMORE VERO NON SI STIMA: E' MISURATO, in `Bperm`** *(`d97ac64`)*

| | divisioni | finestra |
|---|--:|--:|
| i tre semi | `27`, `28`, `30` | `8722`, `8301`, `8534` |
| media | `28.3333` | `8519.0` |
| dispersione *(`pstdev`, `÷N`)* | `1.2472` = **`4.4019 %`** | `172.1995` = **`2.0214 %`** |
| errore della MEDIA *(`/sqrt(3)`)* | `2.5415 %` | **`1.1670 %`** |
| **`2x` l'errore della media** | `5.08 %` | ### **`2.3340 %`** ⟹ **`[0.9767, 1.0233]`** |

### ⛔ **E QUI C'E' UN ERRORE NEL CONTO DEL GUARDIANO, e lo scrivo perche' il mandato lo
### chiede**

Il `2.0 %` e' **`pstdev`**, la deviazione standard di **POPOLAZIONE** *(divide per `N`)* --
e' quella che lo strumento stampa. ### ⚠ **Ma per STIMARE la dispersione da tre campioni
l'estimatore non distorto e' quello di CAMPIONE** *(divide per `N-1`)*, e vale
### **`stdev/pstdev = sqrt(N/(N-1))` = `1.2247`**:

| | con `pstdev` | con `stdev` *(non distorta)* |
|---|--:|--:|
| dispersione relativa, finestra | `2.0214 %` | **`2.4756 %`** |
| errore della media | `1.1670 %` | **`1.4293 %`** |
| `2x` ⟹ banda | `[0.9767, 1.0233]` | ### **`[0.9714, 1.0286]`** |

> ### 📌 **COME LO RISOLVO, senza reinterpretare una decisione che non e' mia:** la banda che
> ### **VALE e' quella del guardiano, `[0.9767, 1.0233]`**, perche' e' lui che l'ha fissata e
> la sua formula dice *«la dispersione misurata»*, che e' il numero che lo strumento stampa.
> ### ⚠ **E riporto accanto `[0.9714, 1.0286]`:** se il risultato cadesse **fra le due**, la
> lettura ### **non e' decisa dal dato ma dalla scelta dell'estimatore**, e il referto lo
> direbbe invece di scegliere.

### ⛔ **E UN LIMITE PIU' GRANDE DI ENTRAMBE LE BANDE, che dichiaro ORA**

*«`2x` l'errore della media»* e' una regola **a `2 sigma`**, e con **tre** semi ci sono
### **due gradi di liberta'**: l'intervallo al `95 %` vero vuole `t(0.025, 2)` = **`4.3027`**,
non `2`. Cioe' `± 5.02 %` ⟹ `[0.9498, 1.0502]` *(o `± 6.15 %` ⟹ `[0.9385, 1.0615]` con
l'estimatore non distorto)*. ### **E `P3` dice che per una barra fra semi servono ALMENO
QUATTRO SEMI.**

> ### ✔ **Applico la regola del guardiano COM'E' SCRITTA**, perche' e' la sua decisione.
> ### ⛔ **Ma il referto dira' che una banda a `2 sigma` su TRE semi e' OTTIMISTICA di un
> fattore `~2.15`**, e che ### **la cura vera sarebbe un quarto seme, non una banda piu'
> larga.**

### LA REGOLA NUOVA: **`fisso` contro `perm` si confrontano con l'ERRORE COMBINATO**

### **La finestra di `Bperm-fisso` si dice *«diversa da `Bperm`»* se**

```
|media_fisso - media_perm|  >  2 * sqrt( se_fisso^2 + se_perm^2 )
```

dove ogni `se` e' la **dispersione fra i suoi tre semi diviso `sqrt(3)`**. ### ✔ **E questo e'
piu' giusto della banda**, perche' confronta **due medie con la loro incertezza ciascuna**
invece di una media contro un numero trattato come esatto. Per `Bperm` oggi:
### **`se_perm` = `121.8` eventi, cioe' lo `1.4293 %`** *(con l'estimatore non distorto;
`1.1670 %` con `pstdev`)*.

### ⚠ **E LA TAVOLA `L-A`/`L-B`/`L-C`/`L-D` RESTA COM'E'**, letta con queste bande: cambia
**la larghezza**, non **il significato** delle quattro righe.

### ⛔ **UNA COSA DA DICHIARARE SULL'ORDINE: LA CORSA ERA GIA' PARTITA**

Il mandato dice *«da committare PRIMA dello strumento e della corsa»*. ### **Quando e'
arrivato, lo strumento era committato** *(`34a11dc`)* ### **e la corsa era in volo.**
### ✔ **E NON LA FERMO, perche' la banda non cambia NIENTE di cio' che la corsa registra:**
il `json` porta i **conteggi grezzi**, e la banda e' una **lettura** che si applica dopo.
### **Lo strumento stampa la banda VECCHIA, e questo si cura in un commit a se' a run chiuso;
il referto applica QUESTE bande, ed e' lui la lettura autorevole.** ### ⛔ **Lo scrivo invece
di lasciar credere che l'ordine sia stato rispettato.**

## 3. TODO DEL NEXT STEP

1. **commit di questo task history**, ### **DA SOLO**, prima dello strumento;
2. lo **strumento**: il modo `--perm-fisso` *(la cache della permutazione)*, il braccio
   identico per `C-perm-0`, i controlli `C-ident` e `C-lotterie`, e il **collaudo**;
3. **commit dello strumento**, prima della corsa;
4. la **corsa**: `Bpf-s1`, `Bpf-s2`, `Bpf-s3` e `Bpf-id`, in **lockstep**;
5. i **controlli**, e `FERMO` se `C-perm-0`, `C-distr` o `C1` falliscono;
6. le **uscite** col verdetto, e poi il **referto generato**, che riporta
   ### **ENTRAMBI i bracci** -- `Bperm` e `Bperm-fisso` -- con `P1`/`P2`/`P3` sulla **media**
   e la tavola `L-A`/`L-B`/`L-C`/`L-D`;
7. poi ### **la misura del TETTO DELLA TORSIONE**, e si aspetta Luca **solo dopo quel
   referto**.
