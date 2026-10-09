# L'AVANZAMENTO DELLA FASE `2` — **dove siamo, e il comando per riprendere**

> ### ⛔ **QUESTO FILE SI AGGIORNA A OGNI LOTTO**, con un commit e un push. Se il lavoro si
> interrompe, ### **si riparte da qui senza rifare niente.**

| | |
|---|---|
| ramo | `primo-ordine` |
| punto di ritorno | tag ### **`pre-indice-v2`** *(prima dello schema `2`)* |
| schema in vigore | ### **`3`** *(la classe `NON_DEFINITA`)* |
| simulatore | `b8c21049`, ### **non toccato** |

---

## ✔ **FATTO**

| | |
|---|---|
| ### **schema `3`** | la classe ### **`NON_DEFINITA`** nel vocabolario, col validatore che la ### **vieta** con uno stato diverso da `DA_CLASSIFICARE`. Collaudo: ### **`21` su `21`** *(due casi nuovi: `NON_DEFINITA` con `APERTA` ### **rifiutata**, e il caso sano)* |
| ### **`aggiorna-lotto`** | la ### **stessa** via di scrittura, in blocco: una riga di storico ### **per voce**, le stesse asserzioni, e ### **una validazione prima** *(senza i derivati, che sono stale per costruzione)* ### **piu' una INTERA dopo** |
| ### **punto `1` (a)** | ### **`233`** segnaposto → classe `NON_DEFINITA`. ### ⚠ **`ESENTE-P3` ESCLUSO:** e' un segnaposto per titolo, ma la ### **lista `1` di Luca** lo ha fatto una voce vera — ### **una decisione dichiarata batte il titolo** |
| ### **punto `1` (b)** | le ### **`51` `TEORIA`** corrette: la classe viene dal ### **`tipo_era1` DICHIARATO**. ### ⭐ **`TEORIA` era il vecchio STATO `teoria` trasportato come CLASSE**, ed e' un difetto della migrazione. `K2a` `K2b` → `CRITERIO`/`METODO`, padre `OSSERVABILE-P1`; `T3a` `T3b` → padre `DRIVER-SCENA-II`; `M0a` → `DIFETTO`/`INFRASTRUTTURA` |
| ### **punto `1` (c)** | ### **`20`** assiomi e principi: `16` → `FISICA`, `4` → `METODO`, tutti era `ENTRAMBE`, con `nota_guardiano` ### **«da confermare da Luca»** |
| ### **punto `1` (d)** | ### **`9`** voci da `INFRASTRUTTURA` a `METODO`, col motivo di ciascuna |

**L'ultimo lotto applicato:** `doc/indice/_lotti/correzioni.jsonl` — ### **`313` voci**,
`313` righe di storico, e la validazione ### **intera** passa.

---

## ⛔ **CHE COSA RESTA**

| ordine | che cosa | quante |
|--:|---|--:|
| `1` | `doc/REGOLE/par9.md` allo schema in vigore *(commit da solo)* | — |
| `2` | le voci ### **vere** `DA_CLASSIFICARE`: le `tipo_era1 = altro` e quelle senza evidenza | ### **`247`** |
| `3` | le ### **`CHIUSE` senza dominio** *(ricevono solo dominio ed era)* | ### **`184`** |
| `4` | i ### **segnaposto** `NON_DEFINITA`: alias, etichetta, o concetto da definire | ### **`233`** |
| `5` | il referto `doc/REFERTO_indice_v2_fase2.md` | — |

---

## 📌 **IL COMANDO PER RIPRENDERE**

```
cd /c/Users/lpeano/soliton_simulator
git pull                                        # ramo primo-ordine
python csv/indice.py valida                     # deve passare
python csv/indice.py cerca --stato DA_CLASSIFICARE   # che cosa resta

# per LEGGERE un lotto (descrizione, fonte, metadati dell'era 1 -- MAI il solo titolo):
python csv/indice.py mostra --stato DA_CLASSIFICARE --segnaposto NO --da 0 --quante 50

# per APPLICARE un lotto:
python csv/indice.py aggiorna-lotto doc/indice/_lotti/<nome>.jsonl
```

### ⚠ **E LE REGOLE DEL LAVORO, perche' chi riprende non le ritrovi altrove:**

| | |
|---|---|
| ### **si legge il CONTENUTO** | `descrizione`, `fonte`, e i metadati dell'era `1`. ### ⛔ **MAI il solo titolo, e MAI per parola chiave** |
| ### **il motivo CITA** | ogni `--motivo` riporta una frase della descrizione o della fonte. ### **Niente motivi generici**, e il lotto ### **rifiuta** un motivo sotto i `20` caratteri |
| ### ✔ **il dubbio e' un esito** | se il contenuto non basta, la voce ### **RESTA `DA_CLASSIFICARE`** con `meta.motivo_dubbio`. ### **Non c'e' un numero minimo da classificare** |
| ### **la mescolanza non si forza** | due cose di dominio diverso in una voce ⇒ `meta.da_dividere = true` e una proposta in `nota_guardiano`. ### **La divisione la decide Luca** |
| ### **le liste del guardiano NON cambiano** | salvo le correzioni `(c)` e `(d)` del punto `1`. ### **Un disaccordo va nel REFERTO, non nell'indice** |

---

## 📌 **STATO AL 2026-10-09** — *aggiornato a ogni lotto*

| | |
|---|--:|
| voci | `829` |
| ### **`DA_CLASSIFICARE` vere** *(non segnaposto)* | ### **`1`** |
| ### **segnaposto `NON_DEFINITA`** | ### **`181`** |
| ### **righe di storico** | ### **`1046`** |

```
classe    DIFETTO=209  NON_DEFINITA=181  FRONTE=169  CRITERIO=107  MISURA=55  CURA=46  PRESIDIO=34  STANDARD=28
dominio   FISICA=439  DA_CLASSIFICARE=181  METODO=136  INFRASTRUTTURA=46  DOCUMENTAZIONE=27
era       1=445  DA_CLASSIFICARE=182  ENTRAMBE=176  2=26
stato     SOSPESA=274  CHIUSA=187  DA_CLASSIFICARE=182  APERTA=160  AGENDA=26
```

### ✔ **FATTO IN QUESTO GIRO:** il blocco `C`: ### **`16` etichette RIPRISTINATE come voci**, perche' la mia regola era sbagliata -- ### **un documento e' esattamente il posto in cui un ID si DEFINISCE.** `12` criteri di sigillo *(`TS-*`, `TW-*`)*, `O4` *(un'obiezione al bersaglio!)*, `SHAKE-THEN-FREEZE` *(con la sua chiusura, `5cffa73`)*, e `D5`/`D6` ### **OMONIMI, che NON si scelgono.** Piu' `crea-lotto`, ### **la via che mancava per far NASCERE una voce**

### ⛔ **RESTA:** il blocco `D` *(il campo `commit` dello storico, vuoto in `982` righe)* e il blocco `E` *(i controlli e il referto `doc/REFERTO_indice_v3_correzione.md`)*

**Ultimo lotto applicato:** `doc/indice/_lotti/v3_C.jsonl`
