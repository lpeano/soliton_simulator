# REFERTO — **il tetto causale: tempo COORDINATO contro tempo PROPRIO** *(passo 1: la misura)*

**Mandato di Luca, 2026-10-04.** `TETTO-CAUSALE-TEMPO-COORDINATO`, **passo (1)**.
*Il simulatore **`0f060670`** non e' stato toccato.*
**Task history** *(committato PRIMA, `727533d`)*:
`doc/TASK_HISTORY/2026-10-04_tetto-causale-tempo-coordinato-misura.md`.
**Strumento** *(committato PRIMA di girare, `0cfb460`)*: blob **`19d08753`**,
`tracciato = True`, `dirty = False` — **dichiarato dal referto stesso**.

> ### ⛔ **IL CONTROLLO `(A)` HA TROVATO DIFFERENZE: VALE IL `FERMO` GIA' FISSATO.**
> ### **83 passi su 150 sono INVALIDI, e NON traggo conclusioni di fisica.**

---

## 1. IL CONTROLLO, e il `FERMO`

### **Che cosa controlla** — **la LEGGE contro CIO' CHE LA LEGGE HA SCRITTO**

`(A)` con gli `r` registrati in **`step` dello stesso passo** e gli `ii`/`jj` di **adesso**
al sito, si ricalcola `DT*0.5*(r[ii]+r[jj])` **solo** sugli archi con entrambi gli estremi
`< len(r)`, e si confronta **AL BIT** con `_dt_e_ultimo[mask]` sugli **stessi** archi.
`(B)` lo stesso confronto con **`ii` spostato di uno** deve dare differenze.
`(C)` **zero archi confrontabili = il passo NON PASSA.**

| | |
|---|--:|
| verifiche *(150 passi x 2 siti)* | **300** |
| archi mascherati | **141 546 224** |
| archi **CONFRONTATI** | **141 541 432** |
| esclusi: **un estremo oltre `len(r)`** *(nodo nato in `mitosi`)* | **4 792** |
| esclusi: **`dt_e` non finito** *(il veleno del `COMMIT 4`)* | **0** |
| verifiche con **zero archi** *(non passano)* | **0** |
| verifiche con **POTERE** *(`dt_e` varia fra gli archi)* | **296** |
| verifiche **INVERIFICABILI** *(`dt_e` costante)* | **4** |
| verifiche con potere in cui **`(B)` NON ha discriminato** | ### **0** |
| ### verifiche con **DIFFERENZE in `(A)`** | ### **166** |

### ✅ **`(B)` HA DISCRIMINATO IN TUTTE LE 296 VERIFICHE CON POTERE**, quindi `(A)` non e'
un confronto vuoto: ### **sa vedere un disallineamento, e ne ha visto uno.**

### **I PASSI, PER CLASSE**

| classe | quanti | quali |
|---|--:|---|
| **INVERIFICABILI** *(`dt_e` costante)* | **2** | `1`, `2` |
| ### **INVALIDI** *(`(A)` trova differenze)* | ### **83** | da **`42`** a **`150`** |
| **VALIDI** | **65** | da **`3`** a **`85`** |

### ⛔ **E DA `86` IN POI NESSUN PASSO E' VALIDO.** L'ultimo passo valido e' l'**`85`**.

**I passi invalidi, per esteso:** `42`, `50`, `65`, `66`, `69`–`73`, `76`–`84`, `86`–`150`.

### ⛔ **IL `FERMO`:** il mandato dice *«se `(A)` trova differenze in un passo, la misura su
quel passo e' invalida: dichiara quanti passi e quali, e **FERMATI prima di trarre
conclusioni**»*. ### **Quanti e quali sono qui sopra. Non traggo conclusioni di fisica.**

## 2. IL FATTO MISURATO CHE RESTRINGE DOVE GUARDARE

> ### 📌 **LE 166 VERIFICHE CON DIFFERENZE SONO *ESATTAMENTE* LE 166 IN CUI UN NODO E'
> ### NATO IN QUEL PASSO.** I due insiemi **coincidono**: `166 = 166`, verificato come
> ### uguaglianza fra insiemi di `(passo, sito)`, non per conteggio.

E il **primo** passo con differenze e' il **`42`**, che e' ### **il passo della prima
divisione** *(`doc/FATTI_dal_codice.md`, voce `decidi_divisione`: «il primo candidato arriva
al passo `42`»)*. ### **I passi `1`–`41` sono TUTTI puliti.**

**In ogni verifica con differenze** si misura `len_r = n_ora - 1`: cioe' `r` e' lungo come i
nodi **al momento di `step`**, e **adesso** c'e' un nodo in piu'.

### ⚠ **E QUI MI FERMO, perche' il mandato lo dice.** La lettura che questi numeri
suggeriscono — *che `_dt_e_ultimo` non sia ri-allineato dalla ristrutturazione degli archi
che `mitosi` fa* — e' ### **un'IPOTESI che NON ho verificato**, e la scrivo come tale.
### **Cio' che e' MISURATO e' la corrispondenza 1:1 con i passi in cui nasce un nodo, e
l'ampiezza dello scarto.**

**Lo scarto, nei primi passi invalidi:**

| passo | sito | diversi / confrontati | scarto max |
|--:|---|--:|--:|
| `42` | `clip_spinta` | **91 992** / 471 563 | `1.342e-02` |
| `42` | `coes` | **91 992** / 471 563 | `1.342e-02` |
| `50` | `clip_spinta` | **89 722** / 471 564 | `1.274e-02` |
| `65` | `clip_spinta` | **73 280** / 471 565 | `1.180e-02` |

### ⛔ **E LO SCARTO NON E' ARROTONDAMENTO: `1.342e-02` e' PIU' GRANDE DI `DT = 0.01`.**
*(I due siti danno lo **stesso** numero perche' usano la **stessa** `mask`, gli **stessi**
`ii`/`jj` e la **stessa** fonte: e' coerente, non una coincidenza.)*

## 3. I PASSI INVERIFICABILI, e il ramo che li produce

| passo | perche' `r = 1` su ogni nodo |
|--:|---|
| **`1`** | ### **`_ritmo_sicurezza`**, e lo ho **MISURATO**: vale `1` a fine corsa, cioe' e' scattato **una volta sola**. E' il ramo che restituisce `np.ones(self.n)` quando `_psi_prec` e' assente o di lunghezza sbagliata — *«non esiste uno stato precedente con cui confrontarsi»* |
| **`2`** | **`_ritmo_med_assente`** *(attribuzione di **Luca**)*. ### ⚠ **E NON L'HO MISURATO:** il contatore **esiste** nel simulatore *(`:5267`)*, l'ho verificato, ma la mia corsa registrava `_ritmo_med_non_promosso`, che e' **un altro contatore**. ### **Quindi riporto l'attribuzione come di Luca, verificata NEL CODICE e non nella mia misura** |

### ⚠ **PERCHE' <<INVERIFICABILI>> E NON <<PASSANO>>:** con `r = 1` ovunque, `dt_e` e' un
array **costante** pari a `DT`, quindi ### **nessuna permutazione degli indici e'
rilevabile** — ne' `(A)` ne' `(B)` hanno potere. ### **Dirli *«identici»* sarebbe un
`FALSO-UNO`**, ed e' il guardiano ad averlo scritto nel mandato prima che lo misurassi.

### **E I CONTATORI DI `ritmo()` A FINE CORSA** *(letti al gancio di `step`, dove sono
**correnti**, perche' `ritmo()` gira dentro `step` prima del gancio)*:

| | |
|---|--:|
| `_ritmo_chiamate` | **150** |
| `_ritmo_sicurezza` | **1** |
| `_ritmo_snap_identico` | **0** |
| `_ritmo_guard4pi_ko` | **0** |
| `_ritmo_med_non_promosso` | **0** |

### ✅ **QUINDI `r` NON E' DEGENERE: `148` passi su `150` hanno `r` che varia**, e spazia da
**`1.455472e-06`** a **`1.414213e+00`** — ### **sei ordini di grandezza**, piu' ampio del
`2e-5 .. 1.41` che la voce d'indice citava.
### **Il primo passo in cui `r` non e' `1` ovunque e' il `3`.**

## 4. I SITI, censiti DALL'AST, e quali GIRANO

| sito | che cos'e' | guardia | gira |
|---|---|---|---|
| `:9146` | `passo_causale = c_sistema*DT` | `GRAV_BIFASE and len(proj)` | **SI** |
| `:9202` | lo **stesso**, ricalcolato | `+ VIRIALE` | **SI** |
| `:9203` | ### **CLIP** `clip(spinta, +-p)` | `+ VIRIALE` | ### **SI** |
| `:9209` | `clip(grav, +-p)` | **`ELSE` di `VIRIALE`** | ### **NO** |
| `:9340` | ### **SCALA** `_delta_coes = (_csa*DT) * _F_adim` | `COES_ADIM`, `COES_CAUSALE` | ### **SI** |
| `:9341` | il **confronto `_glob`** | idem | **SI** |
| `:9351` | `LAM*sqrt(K_C)*DT` | **`ELSE` di `COES_CAUSALE`** | ### **NO** |

### ⛔ **IL MANDATO NE NOMINAVA QUATTRO: L'AST NE TROVA CINQUE.** Il quinto e' `:9341`,
cioe' il **confronto `_glob`** — che il mandato chiede **a parte**.

### ⛔ **E I DUE SITI CHE GIRANO HANNO NATURA DIVERSA:** `:9203` **clippa** *(«quanti archi
limita» e' ben definito)*; `:9340` **scala** — `|_F_adim| <= 1` per costruzione, quindi il
tetto **non limita: lo FISSA**, e cambiare `DT -> dt_e` moltiplica `_delta_coes` per
`dt_e/DT` su **OGNI** arco. ### **Misurarli con la stessa domanda avrebbe prodotto numeri
invece di vedersi.**

**La configurazione, letta dal CLI** *(mai a mano: `H-P3`)*: `TAU_LOC = 1.0` ·
`TEMPO_SEGNO = False` · `COES_CAUSALE = True` · `COES_ADIM = True` · `VIRIALE = True` ·
`GRAV_BIFASE = True` · `CS_DINAMICO = True` · `CS_M = 2.0` · `LAM = 0.8` · `K_C = 2.0` ·
`DT = 0.01`. **Scena:** `nmasse = 3`, `sep = 6.1158` — **dall'argv** — `n = 12802`,
`471 564` archi.

## 5. I NUMERI, **RISTRETTI AI 65 PASSI VALIDI**

### ⛔ **GLI AGGREGATI SU 150 PASSI NON SI POSSONO LEGGERE:** mescolano `65` passi validi,
`83` invalidi e `2` inverificabili. ### **Quelli che seguono sono ricalcolati sui SOLI passi
validi**, dal `json` committato.

### **`:9203` — il CLIP, cono GLOBALE**

| | fino a 72 *(62 passi validi)* | tutti *(65 passi, `<= 85`)* |
|---|--:|--:|
| archi-passo | 29 237 011 | **30 651 762** |
| **limitati OGGI** | 25 418 709 | **26 666 143** |
| **limitati con la CURA** | 26 122 778 | **27 373 302** |
| da limitato a **NON** limitato | 691 475 | **726 198** |
| da non limitato a **LIMITATO** | 1 395 544 | **1 433 357** |
| il tetto **STRINGE** | 12 849 209 | **13 349 102** |
| il tetto **ALLARGA** | 16 387 802 | **17 302 660** |
| **uguali** | 0 | **0** |
| `dt_e/DT`: min / med / max | `1.53e-06` / `1.215` / `1.414` | `1.53e-06` / **`1.385`** / `1.414` |
| `r_i`: min / med / max | `1.46e-06` / `1.258` / `1.414` | `1.46e-06` / `1.393` / `1.414` |
| `\|spinta\|`: min / med / max | `1.49e-13` / `5.48e-02` / `8.76e-01` | `1.49e-13` / `5.49e-02` / `8.76e-01` |

### **`:9340` — la SCALA, cono LOCALE**

| | fino a 72 | tutti *(`<= 85`)* |
|---|--:|--:|
| il tetto **STRINGE** / **ALLARGA** | 12 849 209 / 16 387 802 | **13 349 102** / **17 302 660** |
| `\|_F_adim\| > 0.99` *(«al tetto»)* | ### **0** | ### **0** |
| `_csa` *(cono locale)*: min / med / max | `0.611` / `1.376` / `1.997` | `0.611` / `1.376` / `1.997` |
| tetto **oggi**: min / med / max | `6.11e-03` / `1.376e-02` / `1.997e-02` | `6.11e-03` / `1.376e-02` / `1.997e-02` |
| tetto **con la cura** | `1.48e-08` / `1.623e-02` / `2.818e-02` | `1.48e-08` / `1.794e-02` / `2.818e-02` |
| `_glob` **se diventasse tempo proprio** | `1.73e-08` / `1.374e-02` / `1.600e-02` | `1.73e-08` / `1.567e-02` / `1.600e-02` |
| **stringe / allarga vs `_glob`** *(l'effetto della sola `c_s` locale)* | 5 870 227 / 23 366 784 | **6 175 411** / **24 476 351** |
| **ripieghi `CS_M`** | ### **0** | ### **0** |

### ✅ **E LA SEPARAZIONE CHE LA STELLA POLARE CHIEDEVA E' MISURATA:** `COES_CAUSALE` *(la
`c_s` locale, la cura **gia' fatta**)* **allarga** su `24 476 351` archi-passo e **stringe**
su `6 175 411` — ### **un fattore `4` a favore dell'allargamento.** **Questo e' l'effetto
della `c_s`, non del tempo**, e i contatori del simulatore lo misuravano gia'.

### ⚠ **IL RIPIEGO `CS_M = 2.0` NON SCATTA MAI** *(`0` su `150` passi)*, quindi oggi e'
**inerte**. ### **Ma resta una toppa, e MISURATA: `CS_M*DT = 0.02` contro
`c_sistema*DT = 0.0113137085` — quasi il DOPPIO del tetto che sostituisce.** Un ripiego piu'
**largo** di cio' che rimpiazza non e' conservativo. **Dichiarato, non curato**
*(congelamento)*.

## 6. IL VELENO DEL `COMMIT 4`, ai siti del tetto

| | |
|---|--:|
| archi-passo mascherati con `dt_e` **NON FINITO** | **1 458** *(su `83` passi)* |
| esclusi dal controllo **per non finito** | **0** |
| esclusi dal controllo **per estremo oltre `len(r)`** | **4 792** |

> ### 📌 **OGNI ARCO COL VELENO E' ANCHE FUORI RANGE:** il veleno cade **esattamente** sugli
> archi che toccano un nodo **nato in quel passo**. ### **E' il caso che
> `VELENO-ORIENTATO` aveva previsto, e che il task history aveva scritto PRIMA di misurare:
> una cura che facesse leggere `_dt_e_ultimo` a `memoria_hebbiana_moto` leggerebbe `NaN`
> sugli archi nati in quel passo.**

## 7. CHE COSA QUESTO REFERTO **NON** DICE

1. ### **Non trae conclusioni di fisica**, per il `FERMO`: `83` passi su `150` sono invalidi.
2. ### **Non dice che `_dt_e_ultimo` sia disallineato:** dice che `(A)` trova differenze
   **esattamente** nei passi in cui nasce un nodo. **La causa e' un'ipotesi, non una misura.**
3. ### **Non dice se la cura stringa o allarghi NETTAMENTE:** i conteggi sui passi validi
   ci sono, ma **si fermano al passo `85`** e la traiettoria continua fino a `150`.
4. ### **Non e' un sigillo** e non vale per `TAU_LOC = 0`, per `VIRIALE = False`, ne' per
   `COES_CAUSALE = False` — i due rami spenti **non sono stati misurati**, per definizione.

## 8. PROVENIENZA, e **un mio errore da dichiarare**

**Piattaforma:** python **3.13.2** / numpy **2.3.0** / **Windows 11** / **AMD64**.
**Simulatore:** `0f060670` *(sha1 dei byte grezzi, **non toccato**)*. **Copia patchata:**
rigenerata a ogni giro, **4 ancore** tutte asserite uniche. **Strumento:** `19d08753`.

### ⛔ **L'ERRORE: in `0cfb460` ho committato un referto che cita lo strumento `75189105`,
### un blob che il repo NON HA.** Quel file era l'uscita della **sonda a 2 passi**, prodotta
da uno stato intermedio *(dopo due patch, prima del commit)*. ### **E' la specie di difetto
`_sonda_scherm`: un referto che nomina uno strumento introvabile.**
### ⚠ **E l'ironia conta:** ci sono arrivato perche' **`H-NON-TRACCIATI` mi ha bloccato** e
ho committato quel file per sbloccarmi, ### **senza controllarne il timbro** — il presidio
nato contro i riferimenti al vuoto mi ha spinto a crearne uno.
**Il referto di oggi dichiara `19d08753`, `tracciato = True`, `dirty = False`.**

### ⚠ **E UNA SECONDA IMPRECISIONE, nel messaggio di `0b3af63`:** dicevo *«il suo `[TIMBRO]`
dichiara il blob `ae23a757`»*. Il `[TIMBRO]` sta nello **stdout** *(lo stampa
`_presidio.avvia`)*, **non dentro `_collaudo.txt`**, che passa dal mio `stampa()`.
### **L'attribuzione poggiava sull'uscita che avevo letto io, non sul file committato.**

### ✅ **E UNA VERIFICA CHE IL MANDATO CHIEDEVA:** *«i numeri della misura devono essere
identici a quelli del referto gia' fatto»*. Il referto precedente era la **sonda a 2 passi**,
non una corsa: gli unici passi confrontabili sono `1` e `2`, e su quelli
### **22 grandezze su 22 sono IDENTICHE, 0 diverse.** ### **La misura non e' cambiata: e'
cambiato solo il controllo.**

---

**Comandi, verbatim:**

```
python csv/_test_fork/_tetto_causale_tempo.py --collaudo
python -u csv/_test_fork/_tetto_causale_tempo.py --passi=150
```
