# IL TETTO DELLA TORSIONE — **la soglia di mitosi `3π` sta sul tetto?**

*(Mandato di Luca del 2026-10-06, messo in coda dopo `Bperm`. ### **Sola lettura: il
simulatore NON si tocca**, resta `f7237563`. Le tre verifiche sul codice che il mandato chiede
### **prima** del task history sono qui sotto, ed ### **due di esse CORREGGONO il conto**.)*

---

## 0. LA RICERCA NELL'INDICE — **e un mio errore da correggere**

Il mandato dice: *«Prima di aprire una voce per questa misura, cerca nell'indice se esiste
gia' qualcosa sul tetto o sull'equilibrio della torsione, o su `κ_tw`.»*

> ### ⛔ **IN `doc/CODA_2026-10-06.md` AVEVO SCRITTO CHE NON ESISTE NIENTE. E' FALSO.**
> Quella riga l'avevo scritta **io**, e rifacendo la ricerca ### **col comando** invece di
> fidarmi di essa sono uscite **quattro** voci. ### **Dire *«non esiste»* da una riga mia
> invece che da un comando e' precisamente cio' che `STANDARD 9` vieta**, e la riga sbagliata
> **resta** nel `CODA` con questa correzione accanto.

| voce | che cosa dice | che cosa c'entra |
|---|---|---|
| ### **`SCALE-TW`** *(`blocca_run_base = SI`)* | *«le scale della torsione: un'analisi completa, DA CAPO»*, mandato del 2026-09-22; prerequisito `M1` ### **gia' misurato** il 2026-09-27 | ### ⛔ **QUESTA MISURA E' UN PEZZO DI QUELLA VOCE.** Non se ne apre una nuova |
| **`ARCHI-OLTRE-4PI`** | `~109` archi stanno **oltre** `4π` dal passo `2` e **non rilassano**, in tutti i bracci | la sua **seconda strada** e' letteralmente *«il wrapping della torsione: `TORS_4PI` mette `tw` sul dominio doppio e il tetto `TW_TETTO = 4π` e' il suo estremo»* ⟹ ### **e' la verifica (b) vista dall'altro lato** |
| **`CENS-B4`** | *«costanti temporali `TAU_P`/`TAU_BG`/`TAU_TW` come RAPPORTI adimensionali»* | e' l'origine del `κ` di cui si discute |
| ### **`KAPPA-TW-COMMENTO`** | **aperta da me oggi** *(`d0bf602`)*: il commento dice `κ = 3.1831`, il codice restituisce `1` | ### **falsa questa misura alla radice** |

### ➜ **DECISIONE: nessuna voce nuova per la misura. I risultati vanno sotto `SCALE-TW`**, e
il difetto trovato strada facendo ha la sua *(`KAPPA-TW-COMMENTO`)*.

---

## LA STELLA POLARE — le cinque domande

| | risposta |
|--:|---|
| **1 `A14`** | ### **NON SI APPLICA, e il perche':** la misura ### **non introduce nessuna legge** e non muta nessuno stato. La patch aggiunge **un gancio di SOLA LETTURA** nel blocco della torsione: registra `dph`, `twp`, `twist_dip`, `tw`, `r`, `phivel` e ### **non scrive niente.** `C0` lo **dimostra** invece di lasciarlo dedurre |
| **2 i tre gradini** | ### **(a) e (c), e lo dico separatamente.** **(a)** robusto al rumore: tre passi *(`50`, `100`, `140`)* e distribuzioni, non singoli valori. ### ✔ **(c) COINCIDE CON UN LIMITE NOTO, e questa volta esiste:** un arco sintetico a `ω` e `r` costanti, evoluto con la legge **vera**, deve convergere a `|tw| = 2π·κ` ### **entro l'1 %** -- e' il controllo positivo del collaudo. ### ⛔ **Non arriva al gradino (b):** non si toglie nessuna legge pratica |
| **3 un numero o una legge?** | ### **NESSUNO DEI DUE: non si aggiunge niente, si MISURA.** ### ⚠ **Ma la misura ne TROVA due, e sono entrambi <<numeri scritti a mano>> (`A1`):** `κ = 1` *(`KAPPA-TW-COMMENTO`)* e il pavimento `1e-3` **dentro** `dom`, piu' un **terzo** -- il pavimento esterno `maximum(..., 1e-3)` -- che ### **la formula del mandato trascura.** ### **Dirlo e' il risultato; curarlo e' una decisione di Luca** |
| **4 `rho`, `c_s`, il segno?** | ### **NON SI APPLICA, e il perche':** non si tocca ne' `rho` ne' `cs`. ### ⚠ **E IL SEGNO SI TOCCA IN LETTURA, non in scrittura:** `tw*` e' una grandezza **firmata** e il mandato chiede `|tw|/|tw*|`, cioe' ### **i moduli** -- quindi un arco in cui spinta e scarica hanno segni discordi da' lo stesso rapporto di uno concorde. ### **Lo dichiaro come limite della lettura, e riporto anche il segno** |
| **5 emergente o imposto?** | ### **E' LA DOMANDA STESSA.** Se `tw*` = `2π` per **qualunque** arco a deriva costante, allora la soglia `3π` e' ### **irraggiungibile in equilibrio** e la mitosi e' **marginale per costruzione** -- cioe' ### ⛔ **IMPOSTA da due numeri scritti a mano (`κ` e la soglia), non emergente.** ### **La risposta e' il referto, e non la scrivo prima** |

---

## 1. RAGIONAMENTO PRELIMINARE

### L'IPOTESI DEL GUARDIANO, **come l'ha scritta** *(e non la ricopio per crederci)*

| | |
|---|---|
| spinta per passo | `≈ DT·(r_i·ω_i − r_j·ω_j)`, con `ω` = `phivel` |
| scarica | `dt_e·tw/τ_tw`, con `dt_e = DT·r̄` e `τ_tw = κ·2π/(|ω_i − ω_j| + 1e-3)` |
| equilibrio | `tw* = κ·2π·(r_i·ω_i − r_j·ω_j) / (r̄·(|ω_i − ω_j| + 1e-3))` |
| con `r` **uniforme** | `|tw*| = 2π` per **qualunque** arco a deriva costante |
| col dipolo, `≤ π` | il massimo raggiungibile sarebbe `2π + π = 3π`, ### **la soglia stessa** |
| corollario | con `r` **diverso** agli estremi `tw*` si sposta da `2π`: ### **il gradiente di tempo modulerebbe GIA' il tetto, in forma derivata** |

### ✔ **E IL CONTO CON `r` UNIFORME TORNA, verificato da me:** con `r_i = r_j = r`,
`tw* = 2π·r(ω_i−ω_j)/(r(|ω_i−ω_j|+1e-3))` = `2π·(ω_i−ω_j)/(|ω_i−ω_j|+1e-3)` ⟹
### **`|tw*| → 2π`** appena `|Δω| ≫ 1e-3`. ### **Il `r` si CANCELLA.**

---

## 2. LE TRE VERIFICHE SUL CODICE — **fatte PRIMA, e due correggono il conto**

### ✔ **(a) IL RAMO DI `τ_tw` E IL VALORE DI `κ`** — *fatta*

`TAU_LOCALI = True` *(`:451`)* ⟹ gira **`_tau_tw_locale`** *(`:584`)*, che restituisce

```
np.maximum( (2*np.pi) / (|phivel[i] - phivel[j]| + 1e-3),  1e-3 )
```

### ➜ **`κ = 1` ESATTAMENTE**, e `TAU_TW = 20.0` la usa **solo** il ramo non locale.

> ### ⛔ **E IL COMMENTO DICE UN'ALTRA COSA: `κ_tw = TAU_TW/(2π)` = `3.1831`.** Difetto
> aperto come **`KAPPA-TW-COMMENTO`** *(`d0bf602`)*. ### **Le due letture danno tetti `2π` e
> `20`: fisiche OPPOSTE**, e la misura si fa con `κ = 1` **perche' e' quello che il codice
> esegue** *(`CLAUDE.md` par.2)*.
>
> ### ⚠ **E C'E' UN TERZO NUMERO CHE LA FORMULA DEL MANDATO TRASCURA:** il pavimento
> **esterno** `maximum(..., 1e-3)`. Scatta se `2π/dom < 1e-3`, cioe' se `|Δω| > 6283`.
> ### **Se succeda NON LO SO, e non lo assumo inerte: diventa `M8`.**

### ⚠ **(b) `_w8` PUO' AVVOLGERE GLI INCREMENTI?** — ### **SI', ma non dove farebbe danno**

`_w8(a) = (a + 4π) % 8π − 4π`, cioe' il codominio e' `[−4π, 4π)`. Gli ingredienti, col
`FASE_2PI = False` *(`:3543`)* e `TORS_4PI = True` *(`:3077`)*:

| | intervallo | da dove |
|---|---|---|
| `dph = _wphi(_phi_t[i] − _phi_t[j])` | `[−2π, 2π)` | `_wphi` col periodo `4π` |
| `twist_dip = π/2·(χ_i − χ_j)` | `[−π, π]` | `POLO_MATURO = False`, `CHI_CORE = False`, `CHI_COOP = False` ⟹ `χ = perc_chi ∈ {−1, 0, +1}` ⟹ ### **`twist_dip ∈ {0, ±π/2, ±π}`, cinque valori e non un continuo** |

### ➜ ✔ **PRIMO RISULTATO, ed e' una DERIVAZIONE non una misura:**
`|dph + twist_dip| ≤ 3π < 4π` ⟹ ### **`twp = _w8(dph + twist_dip)` NON AVVOLGE MAI**, ed e'
uguale a `dph + twist_dip` **esattamente**.

### ➜ ⚠ **SECONDO RISULTATO:** l'argomento del `_w8` dell'incremento e'
`(dph + twist_dip)_t − (dph + twist_dip)_{t−1}` ∈ `[−6π, 6π]`, ### **quindi `_w8` PUO'
ripiegarlo** — serve `|·| > 4π`, che richiede ### **un avvolgimento di `dph`** *(un salto di
`~4π`)* **piu' un cambio di dipolo.**

> ### 📌 **NON SMONTA IL CONTO, LO CONDIZIONA:** la formula vale ### **dove l'incremento non
> si ripiega.** Quante volte si ripiega ### **non lo so, e diventa `M6`** invece di
> un'assunzione. ### ⚠ **E `ARCHI-OLTRE-4PI` dice che una popolazione di `~109` archi vive
> SOPRA `4π` e non rilassa: quella e' esattamente la popolazione in cui l'avvolgimento e'
> plausibile**, e la misura la guardera' **separata**.

### ⛔ **(c) LA SPINTA HA ALTRI TERMINI?** — ### **SI', E UNO SMONTA IL `3π`**

| termine | stato | che cosa fa |
|---|---|---|
| ### **`twist_dip`** | ### ⛔ **ENTRA COME DIFFERENZA NEL TEMPO** | la spinta e' `_w8(D_t − D_{t−1})` con `D = dph + twist_dip`. ### **Se `twist_dip` e' COSTANTE nel tempo, la sua differenza e' ZERO e NON contribuisce all'equilibrio.** Contribuisce **solo** quando la chiralita' **cambia**, e allora e' un **calcio** di `±π/2` o `±π` che poi **decade** con `τ_tw` |
| ### **`delta_sync_phi`** | ### ⛔ **ATTIVO, e la formula lo ignora** | `K_SYNC = 1.0` *(`:382`)* ⟹ `delta_sync_phi = dt_n_s·forza·sin(media − _phi_t)` *(`:7743`)* **non e' zero**. ### **Non entra in `dph` al passo `t`** *(`dph` legge la fotografia `_phi_t`)* ### **ma entra in `self.phi`, cioe' nel `_phi_t` del passo DOPO:** e' un termine della spinta ### **con un passo di ritardo** ⟹ `M7` |
| `dt_n_s` | ### ✔ **NON e' un'omissione** | `TEMPO_SEGNO = False` *(`:3673`)* ⟹ `dt_n_s = dt_n` **esattamente** *(`:7485`)*. ### **Qui la formula e' giusta** |
| `KICK_TW = 0.35` | ⚠ **dichiarato, non misurato** | calcia le **fasi dei figli** a una mitosi *(`:8748`-`:8764`)*, non `tw`. Con `18` divisioni in `150` passi tocca una frazione minuscola di archi, e ### **lo dico invece di tacerlo** |
| nessun clip su `tw` | ### ✔ **verificato** | `tw` si scrive **solo** col `+=` della torsione e si azzera per gli archi nuovi: ### **nessun tetto numerico lo trattiene**, ed e' coerente con `ARCHI-OLTRE-4PI` |

> ### ⛔ **ECCO LA CORREZIONE AL CONTO DEL GUARDIANO, e la scrivo PRIMA della corsa.**
> L'argomento *«`2π` + il dipolo `π` = `3π`, cioe' la soglia»* tratta il dipolo come un
> ### **termine additivo costante** della spinta. ### **Non lo e': nell'equilibrio entra la
> sua DERIVATA TEMPORALE, che e' zero se la chiralita' sta ferma.**
>
> ### ➜ **Quindi in regime di chiralita' STATICA il tetto e' `2π`, NON `3π`** — e la soglia
> `3π` sarebbe ### **piu' lontana** di quanto l'ipotesi dica, non marginale: **irraggiungibile
> in equilibrio.** ### ⚠ **La mitosi vivrebbe allora SOLO sui TRANSITORI** *(calci di dipolo,
> avvolgimenti di `dph`, archi nuovi)*, che e' una fisica **diversa** da *«evento marginale
> per costruzione»*.
>
> ### ✔ **E NON CAMBIO `M2`/`M3`, CHE IL MANDATO HA FISSATO con `|tw*| + |twist_dip|`:**
> restano **come sono**, e accanto si misurano ### **`M2b`/`M3b` senza il dipolo.**
> ### **Il confronto fra le due coppie E' la verifica di questa correzione**, e se mi
> sbagliassi si vedrebbe da li'.

---

## 3. PROGETTAZIONE DEL RAGIONAMENTO — che cosa si misura

### **I CINQUE DEL MANDATO**, nel braccio `Bp` *(modulazione **invariata**)*, ai passi
`50`, `100`, `140`:

| id | che cosa |
|---|---|
| **`M1`** | per ogni arco `|tw| / |tw*|`, con `tw*` sui valori ### **CAUSALI** *(`r` e `phivel` del passo che ha prodotto la spinta: e' la lezione di `99782e1`)*. Distribuzione, ### **solo sugli archi con `|Δω|` sopra il proprio `q25`** *(dove la deriva e' definita)* |
| **`M2`** | la Spearman fra `|tw|` e `|tw*| + |twist_dip|` |
| **`M3`** | la frazione di archi con `|tw*| + |twist_dip| >= 3π`, e la frazione con `>=` **soglia modulata** |
| **`M4`** | gli archi sopra soglia *(`g1`)* contro gli altri: distribuzioni di `|tw*|`, `|twist_dip|` e `|r_i − r_j|` |
| **`M5`** | la distribuzione di `|twist_dip|`: la frazione esattamente a `0`, a `π/2` e a `π` |

### **I CINQUE CHE AGGIUNGO**, perche' le verifiche `(b)` e `(c)` lo impongono

| id | che cosa | perche' |
|---|---|---|
| **`M2b`** | la Spearman fra `|tw|` e `|tw*|` ### **SENZA il dipolo** | se la correzione di `(c)` e' giusta, `M2b` deve essere **almeno buona quanto** `M2` |
| **`M3b`** | la frazione con `|tw*| >= 3π`, **senza** il dipolo | ### **e' il tetto vero in regime statico** |
| **`M6`** | la frazione di `(passo, arco)` in cui `|D_t − D_{t−1}| > 4π`, cioe' ### **il `_w8` RIPIEGA DAVVERO**; e, separata, la stessa frazione ### **sui soli archi con `|tw| >= 4π`** *(`ARCHI-OLTRE-4PI`)* | la formula vale **dove non ripiega** |
| **`M7`** | `|Δ(delta_sync_phi)|` sull'arco contro `|DT·(r_iω_i − r_jω_j)|`: ### **quanto pesa il termine che la formula ignora** | `K_SYNC = 1.0`: **e' attivo** |
| **`M8`** | quante volte il pavimento **esterno** `maximum(..., 1e-3)` ### **vincola**, cioe' `|Δω| > 6283` | non lo assumo inerte |

### I CRITERI, **fissati dal mandato e non ritoccati**

| | |
|---|---|
| l'ipotesi del **tetto** e' **REFUTATA** se | la **mediana** di `M1` cade **fuori** da `[0.3, 2]`, **oppure** se la Spearman di `M2` e' **sotto `0.3`** a **tutti e tre** i passi |
| la **seconda** ipotesi e' **REFUTATA** se | **meno del `30 %`** degli archi ha `twist_dip = 0` |

### LE PREVISIONI — **quella del guardiano e la mia, accanto**

| id | il guardiano | io |
|---|---|---|
| **`M1`** | mediana di `|tw|/|tw*|` fra `0.5` e `1.2`, con una coda che **non supera `1` di molto** | ### **la mediana sta DENTRO la sua banda**, e ci sto: se il tetto e' `2π` e la scarica lavora, il rapporto deve stare vicino a `1`. ### ⚠ **Ma prevedo una CODA PIU' LUNGA della sua**, per gli `~109` archi di `ARCHI-OLTRE-4PI`, che stanno sopra `4π` e **non rilassano**: per loro `|tw|/|tw*|` sara' `> 2` |
| **`M3`** | con la soglia `3π` la frazione e' ### **sotto lo `0.1 %`** | ### **concordo, e prevedo che `M3b` sia ANCORA PIU' BASSA** -- vicina a **zero esatto** -- perche' senza il dipolo il tetto e' `2π` e `2π < 3π` |
| **`M4`** | gli archi in `g1` hanno `|tw*| + |twist_dip|` **piu' alto** degli altri | ### ⛔ **QUI MI SEPARO: prevedo che la differenza sia DEBOLE o assente su `|tw*|`**, e che gli archi in `g1` si distinguano ### **per `|twist_dip|` e per il TRANSITORIO**, non per il tetto di equilibrio. Se avessi ragione, `g1` non e' *«gli archi col tetto alto»* ma *«gli archi colpiti di recente»* |
| **`M5`** | la **maggioranza** degli archi ha `twist_dip = 0` | ### **concordo**, e per una ragione che si puo' dire prima: `twist_dip = 0` ⟺ `χ_i = χ_j`, e in una rete a chiralita' per regioni la maggioranza degli archi sta **dentro** una regione |

### ⛔ **E LA MIA PREVISIONE PRECEDENTE ERA SBAGLIATA**

Su `Bperm` avevo previsto il crollo e ho misurato `1.5741x`. ### **Chi legge pesi queste
previsioni per quello che vale un mio pronostico: uno su uno sbagliato.**

### I CONTROLLI

| id | che cosa | deve |
|---|---|---|
| **`C0`** | il braccio patchato per leggere i valori e' ### **byte-identico a `Bp`** su tutti i conteggi e tutti i passi | ### **PASSARE** |
| **controllo POSITIVO** *(nel collaudo)* | un arco **sintetico** con `ω` e `r` costanti, evoluto con la ### **legge vera** della torsione, deve convergere a `|tw| = 2π·κ` ### **entro l'1 %** | ### **CONVERGERE** |
| **controllo CHE DEVE FALLIRE** *(nel collaudo)* | lo stesso arco con ### **`κ = 2`** | ### **NON** deve convergere a `2π` |

### ⛔ **CHE COSA MI FAREBBE FERMARE**

`C0` che fallisce ⟹ ### **`FERMO`**: il gancio non sarebbe di sola lettura, e ogni numero
della misura sarebbe sospetto.

---

## ⛔ ANNOTAZIONE DEL 2026-10-06 — **LA VERIFICA (b) SAPEVA MENO DI QUANTO SI PUO'
## SAPERE: l'avvolgimento di `dph` inietta `-4π` ESATTI, e `_w8` non lo ripara**

*(Scritta ### **dopo** il commit del task history e ### **prima** dello strumento e della
corsa. La sezione `(b)` qui sopra ### **NON si riscrive:** diceva *«`_w8` PUO' ripiegare, e
quante volte non lo so»*, che e' **vero ma debole**. ### **Il conto si poteva CHIUDERE, e
l'ho chiuso.**)*

### IL CONTO, fatto con uno script e non a mente

Con `FASE_2PI = False` il periodo di `dph` e' `4π`. A un avvolgimento, `dph` salta di
`-4π`, e la differenza grezza diventa `delta - 4π`. Allora:

| | `_w8(delta - 4π)` | errore |
|---|--:|--:|
| **ramo `TORS_4PI`** *(quello che gira)* | `-12.553371` | ### ⛔ **`-4π` ESATTI** |
| **ramo non-`4π`** *(`_w4`, `twp = dph`)* | `+0.013000` | ### ✔ **`-1.9e-15`** |

### ➜ ⛔ **UN AVVOLGIMENTO DI `4π` E' INVISIBILE A UN MODULO DI PERIODO `4π` E VISIBILE A
### UNO DI PERIODO `8π`.** Il ramo che gira ### **non ripara** cio' che l'altro ripara
**esatto**. Difetto aperto come ### **`TORS-W8-AVVOLGIMENTO`**.

### CHE COSA CAMBIA NELLA MISURA

1. ### **`M6` diventa piu' preciso e piu' importante:** non si conta solo
   `|D_t - D_{t-1}| > 4π`, si contano ### **gli avvolgimenti di `dph`** e, separatamente,
   ### **i calci di `~±4π` che ne risultano** -- che sono **lo stesso evento visto due
   volte**, e misurarlo in due modi e' il controllo che il conteggio e' giusto;
2. ### ⚠ **la formula del tetto vale FRA DUE AVVOLGIMENTI**, non su tutta la corsa: un arco
   che avvolge spesso **non ha** un equilibrio `tw*`, ha una **successione di transitori**.
   ### **Questo entra nel referto come limite della lettura di `M1`**;
3. ### ⛔ **e NON indago `ARCHI-OLTRE-4PI`**, che Luca ha messo fra le cose da non toccare:
   riporto il meccanismo e il puntatore, ### **non la verifica che li collegherebbe.**

### ✔ **E I DUE CONTROLLI SINTETICI SONO GIA' VERIFICATI, prima dello strumento**

| controllo | atteso | misurato |
|---|---|--:|
| **POSITIVO** *(`κ = 1`, nessun avvolgimento, `200000` passi)* | `|tw| → 2π` entro l'`1 %` | `6.280045` contro `6.283185`: ### **scarto `0.0500 %`** ✔ |
| **CHE DEVE FALLIRE** *(`κ = 2`)* | ### **NON** deve convergere a `2π` | `12.560091`, cioe' ### **`99.9 %` fuori** ✔ |

### 📌 **E il controllo positivo dice anche una cosa sul conto del guardiano:** con `κ = 1`
l'equilibrio e' `2π` ### **esatto entro lo `0.05 %`**, e ### **non `3π`** -- perche' nel
sintetico `twist_dip` e' **costante**, quindi la sua derivata e' zero.
### ✔ **La correzione scritta nella sezione `(c)` e' confermata dal controllo positivo
PRIMA della corsa.**

## 4. TODO DEL NEXT STEP

1. **commit di questo task history**, ### **DA SOLO**, prima dello strumento;
2. lo **strumento** `csv/_test_fork/_tetto_torsione.py`: il gancio di **sola lettura** nel
   blocco della torsione, `M1`-`M8`, `C0`, e il **collaudo** coi due controlli sintetici;
3. **commit dello strumento**, prima della corsa;
4. il **giro corto** *(`STANDARD 7`)*, poi la **corsa**;
5. le **uscite** col verdetto, poi il **referto generato**;
6. ### **poi FERMO, e si aspetta Luca:** `κ`, la soglia, il dipolo locale e il `0.3` sono
   ### **decisioni sue**.
