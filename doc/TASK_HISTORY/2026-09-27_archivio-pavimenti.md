# `(b)1` — **i pavimenti morti sono usciti, e il sigillo byte-identico PASSA** *(2026-09-27)*

> **Mandato:** *«i pavimenti morti escono dal simulatore e vanno in `csv/_archivio/` con tag; le
> chiamate diventano scritture dirette. SIGILLO: stato byte-identico prima e dopo (23 grandezze,
> scena (ii)(a), driver, 3 passi). Se non è identico, FERMATI.»*
>
> ### ✅ **IDENTICHE TUTTE E 23, BYTE PER BYTE.**
> ### **Blob del simulatore: `e203f9a8` → `59c23942`** *(sha1 dei byte)*.

---

# 1. IL SIGILLO

| | |
|---|---|
| **PRIMA** | simulatore `e203f9a8` — **il blob del tag `pre-archivio-pavimenti`** |
| **DOPO** | simulatore `59c23942` — registrato **dentro il dump** |
| condizioni | scena `(ii)(a)`, seme `11`, `n = 2107`, `m = 70199`, **3 passi pieni**, ordine canonico, **nessuna iniezione di `rng`, nessun presidio** |
| confronto | **23 grandezze**: le 21 di stato più `i` e `j` |
| ### esito | ### **`d` `d0` `phi` `phi_s` `phivel` `psi` `psi_spin` `_psi_spinor` `_psi_prec` `_spinor_lift` `omega_s` `_nb` `_nb_prec` `eta` `tw` `twp` `vd` `peq` `mem_mot` `perc_chi` `perc_geom` `i` `j` — TUTTE identiche, 0 elementi diversi** |

**Referto:** `csv/_seal_fork/_sig_arch_pavimenti.json`.

## 1.1 — Come si rigenera lo stato **PRIMA** *(la provenienza è il tag, non un file)*

`PRIMA.npz` è nato **prima** che il dump registrasse il blob, quindi porta
`_blob_sim = (non registrato)`. **Non è un buco: la provenienza è il tag**, e il comando è questo:

```
git checkout pre-archivio-pavimenti -- soliton_simulator.py
python csv/_test_fork/_hashseed_prova.py --out=PRIMA.npz --seme=11 --passi=3
git checkout HEAD -- soliton_simulator.py
python csv/_test_fork/_hashseed_prova.py --out=DOPO.npz --seme=11 --passi=3
python csv/_test_fork/_hashseed_prova.py --confronta PRIMA.npz DOPO.npz
```

*(Gli `.npz` sono locali e non committati: **il dato è il comando**, e il sistema è deterministico.)*

> ### 📌 **E il sigillo è la prova che il pavimento NON mordeva.** Se avesse morso anche una volta
> in 3 passi, una delle 23 grandezze sarebbe diversa. **Sono identiche: quindi ciò che è uscito è
> un doppione inerte, e il par.(b)1 è dimostrato, non asserito.**

---

# 2. CHE COSA È USCITO, E DOVE È FINITO

**`csv/_archivio/_pavimenti_morti.py`** — **non gira e non si importa** *(solleva se importato)*.
Il testo è estratto **verbatim con `git cat-file -p`** dal tag, **non ricopiato a mano**.

| pezzo | dov'era |
|---|---|
| `_pav_d0` + le sue **7 chiamate** | `:4449`, e `:5899` `:6157` `:6664` `:6817` `:6840` `:6994` `:7042` |
| `_floor_d0` | `:4598` |
| il ramo `else` `np.maximum(…, 0.05)` — **Verlet** | `:5737` |
| il ramo `else` `np.maximum(…, 0.05)` — **Eulero** | `:5782` |

### **Le 7 chiamate erano `self.d0 = self._pav_d0(self.d0)`, cioè un NO-OP col driver:**
la «scrittura diretta» equivalente **è la riga stessa**, che quindi **sparisce**.
### **E i due sottocicli metrici scendono da TRE rami a DUE** — `9-ter`: il numero delle leggi
**diminuisce**.

---

# 3. ⚠ DUE DIPENDENZE CHE NON ERANO NELL'ELENCO, trovate rilevando

## 3.1 — `_floor_d0` serviva **anche alla traccia**, in sette punti

`TRACCIA_D0` chiamava `self._traccia_d0(..., pavimento=self._floor_d0())` in **7 siti**.
**`pavimento=` era già `None` per difetto**, quindi ho **tolto l'argomento** dalle sette e **la
firma di `_traccia_d0` resta**: chi traccia continua a funzionare, **senza un valore che non
esiste più**. E il commento di `TRACCIA_D0` — che diceva *«si registra il VALORE del pavimento, che
NON è una costante»* — **ora dice che quei pavimenti sono archiviati**.

## 3.2 — ### `PAV_COM` governava **solo** `_floor_d0`: **diventa INERTE**

**E il driver lo passa** (`--pav-com`). **Dichiarato in tre posti**, perché un default sbagliato è
peggio di una descrizione sbagliata *(par.6 ②)*:

| dove | |
|---|---|
| `README.md` | sezione nuova: cosa faceva, il default, **e che è inerte in ENTRAMBI gli stati** |
| il commento del flag | `⚠⚠ PAV_COM È INERTE DAL 2026-09-27: il default non conta più` |
| ### il messaggio d'avvio | prima annunciava *«pavimento comovente attivo: d0 >= median(d0)-MAD(d0)»* — ### **una legge che non applicava**. Ora dichiara di essere inerte |

**Non l'ho tolto** *(decisione 3: si conserva tutto)*.

> **Il messaggio d'avvio è il caso più serio dei tre:** era `A8` al contrario — non un ramo
> silenzioso, ma **un ramo che annuncia un effetto che non produce**. Chi leggeva lo stdout di un
> run credeva di avere un pavimento comovente, e non ce l'aveva.

---

# 4. COSA CAMBIA DAVVERO — e non è il sigillo a dirlo

**Il sigillo prova che col driver non cambia niente. Ma c'è una configurazione in cui cambia**, e
va detta:

> ### **Con ENTRAMBI `SCALA_MIN` e `SCALA_MIN_PASSO` spenti** — che **il driver non usa** — prima
> `d0` aveva un pavimento e **ora non l'ha più.**
> **Non è una regressione nascosta: è il senso dell'archiviazione**, e quel comportamento si
> ritrova nel tag e in `csv/_archivio/_pavimenti_morti.py`.

**La garanzia sulle lunghezze resta `LAM`** *(`SCALA_MIN_PASSO`, `_nasce`, `SEMINA_LAM`,
`MITOSI_2LAM`)*, **che non si tocca**: `min(d) = 0.800000 = LAM` **esatto** in 16/16 stati del
pilota, **0 archi sotto `LAM`**, e il pavimento vecchio `0.05` stava **16 volte più in basso** del
minimo osservato.

---

# 5. LA FISICA: la scheda, e le quattro che il presidio ha imposto

**`H-REG-R` ha rifiutato il commit due volte, e aveva ragione due volte.**
**La prima** perché non avevo toccato `REGISTRO_FISICA`: un pavimento **è un limite**, e `A11` dice
che **un limite è una legge**. **La seconda** perché avevo aggiornato **solo** la scheda
`freno-scala-min`, mentre la rimozione cade in **quattro** funzioni con scheda propria.

| scheda | che cosa registra |
|---|---|
| **`freno-scala-min`** | la lista `funzioni=` **perde** `_pav_d0` e `_floor_d0`; e **la forma della legge**: il vincolo sulle lunghezze **era DUE sovrapposti** e ora è **UNO**, `LAM`. *(Il docstring di `_pav_d0` lo diceva già: «lasciare anche il pavimento comovente vorrebbe dire DUE leggi sovrapposte». Era risolto a runtime con un `return v`; **ora è risolto nella FORMA**.)* |
| `memoria-del-moto` | le **cinque** chiamate al pavimento vecchio, uscite |
| `fase-phi` | `step` perde il pavimento su `d` nei **due** sottocicli; **la legge sulla FASE non è toccata** |
| `mitosi-schwinger` | via la chiamata dopo la spinta; **le regole di nascita e `_nasce` NON sono toccate** |

### **`D31`** *(il freno è solo in discesa)* **non è toccata:** resta il difetto aperto di
`freno-scala-min`, ed è della cura **(d)**.

---

# 6. ⚠ DUE STRUMENTI DIVENTANO REPERTI, e lo dichiaro

| strumento | perché |
|---|---|
| **`csv/_test_fork/_etc_pavimenti.py`** | **cita NUMERI DI RIGA** — `:4453` `:4456` `:5737` `:5782` — che **dopo questa rimozione non significano più quello**. ### **Non è più ri-girabile come sigillo**: è un **reperto**, col suo referto committato. *(Non è un difetto nuovo: era una verifica una-volta-sola, e il suo referto è il dato.)* |
| **`csv/_seal_fork/_sigillo_Z1c.py`** | nomina `_pav_d0` nel docstring fra le funzioni che **non** toccava. **Il testo resta corretto come reperto storico**, ma la funzione non esiste più: **da rileggere prima di ri-girarlo** |

## 6.1 — E un difetto **dello strumento di confronto**, curato

`_hashseed_prova.py` stampava *«`PYTHONHASHSEED` non cambia niente»* **anche confrontando due blob
di simulatore diversi** — cioè **anche in questo sigillo**.
### **Una conclusione cablata nello strumento diventa vera per qualunque cosa gli si dia.**
**Curato:** il verdetto ora dice solo **se sono uguali**, e l'interpretazione sta nel referto di
chi lo chiama. **E il dump registra il blob del simulatore**, così un confronto può dire **quali**
due versioni ha confrontato invece di asserirlo.

---

# TODO DEL NEXT STEP

> ### 🛑 **STOP, un pezzo alla volta.**

1. **(b)2 — `SYNC_UPDATE` e i suoi rami parziali** in archivio; **`--sync` diventa un no-op
   accettato**. Stesso sigillo byte-identico: **col driver è spento, quindi niente deve cambiare**.
   ⚠ **E va ricordato il raggio misurato nella FASE 0:** `SYNC_UPDATE` vive in `step` +
   `_passo_spinoriale`, **7 + 6 usi**, e **zero** nelle altre quattro leggi.
2. **(b)3 — gli altri rami morti di `CLIP-INVENTARIO`**, uno alla volta, ognuno col suo sigillo.
3. Poi **(c) la cura**.

## LE VOCI D'INDICE CHE QUESTO DOCUMENTO TOCCA

`ARCH-PAVIMENTI` · `CLIP-INVENTARIO` · `ETC-PASSO` · `D31` · `A8` · `A11` · `A13`

---

# 7. ⚠ **LA PRECEDENZA ERA ROVESCIATA, e il sigillo di (b)1 non poteva vederlo**

> **Correzione di Luca su `7840039`, ed è giusta.**
> ### **Blob: `59c23942` *(rotto)* → `f845d30d` *(corretto)*.**

## 7.1 — L'errore

Togliendo il ramo del pavimento avevo collassato

```
if SCALA_MIN_PASSO:  nudo          elif SCALA_MIN:  freno          else:  0.05
```

in `if SCALA_MIN: freno / else: nudo`. ### **Questo ROVESCIA la precedenza.**
Prima `SCALA_MIN_PASSO` era la **prima** condizione della catena e **vinceva**; dopo, con
**entrambi** i flag accesi, avrebbe vinto `SCALA_MIN` e **si sarebbe frenato DUE volte** — per
scrittura **e** a fine passo — **mentre deve vincere il freno PER PASSO** (`C3`), che è l'intero
punto della cura: frenare scrittura per scrittura fa dipendere il risultato **dall'ordine**.

**La forma, ora esplicita in entrambi i sottocicli:**
### `if SCALA_MIN and not SCALA_MIN_PASSO: freno` · `else: nudo`

**E la precedenza sulle scritture di `d0` era GIÀ intatta** — verificato dal codice, non assunto:
`_sd0` controlla `SCALA_MIN_PASSO` **per primo e ritorna**, poi `if not SCALA_MIN: return dx`.
**Quella catena non l'avevo toccata.**

## 7.2 — Il sigillo, **tre bracci**

| | confronto | atteso | esito |
|---|---|---|---|
| **A** | `PRIMA` *(tag `e203f9a8`)* vs **corretto** `f845d30d`, **col driver** | IDENTICO | ### **PASSA — 0 diverse** |
| **B** | tag `e203f9a8` vs corretto `f845d30d`, **con `--scala-min` E `--scala-min-passo`** | IDENTICO | ### **PASSA — 0 diverse** |
| **C** | ### **CONTROLLO CHE DEVE FALLIRE** | DIVERSO | ### **FALLISCE come deve — 18 grandezze diverse** |

**Il braccio C** confronta il tag col **blob ROTTO** `59c23942`, con entrambi i flag: **18
grandezze diverse**, `d` e `d0` su **tutti i 70199 archi**, `tw` `twp` `vd` `peq` idem.
*(Restano identiche solo `eta`, `perc_chi`, `perc_geom`, `i`, `j` — cioè ciò che il freno non
tocca.)*

> ### 📌 **Senza il braccio C questo sigillo non proverebbe niente.** Due «identici» dicono solo
> che qualcosa non è cambiato; **è il caso che FALLISCE a dimostrare che il sigillo guarda proprio
> la precedenza.** È `P1-sexies`, ed è la stessa lezione di `HASHSEED-RIPROD`: **una prova
> costruita in modo che non possa smentirti non è una prova.**

**Referto:** `csv/_seal_fork/_sig_precedenza_scalamin.json` *(i tre bracci, col dettaglio)*.
**Condizioni:** scena `(ii)(a)`, seme `11`, `n = 2107`, `m = 70199`, 3 passi pieni, ordine
canonico, nessuna iniezione di `rng`, nessun presidio. **Il confronto dichiara l'ARGV INTERO di
entrambi gli stati** *(`P5`)*, e per il braccio B stampa *«configurazioni UGUALI»*.

## 7.3 — ### La lezione, e vale oltre questo caso

> ### **Un `elif` che diventa `else` non è una semplificazione: è un cambio di ordine fra due
> condizioni.**
>
> **E il sigillo byte-identico di `(b)1` non poteva vederlo**, perché col driver `SCALA_MIN` è
> **spento**: ### **un sigillo su UNA configurazione non certifica una PRECEDENZA fra due flag.**
> Per quella serve **la configurazione in cui entrambe sono accese**, ed è esattamente il braccio
> che mancava.

**⚠ E una cosa sul braccio A:** `PRIMA.npz` non registra l'`ARGV` *(è nato prima del campo)*,
quindi il confronto stampa *«configurazioni DIVERSE»*. **Non è un disallineamento di
configurazione: è un campo assente**, e il braccio B — dove entrambi i file lo portano — dichiara
*«configurazioni UGUALI»*.
