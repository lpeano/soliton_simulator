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
| voci | `846` |
| ### **`DA_CLASSIFICARE` vere** *(non segnaposto)* | ### **`1`** |
| ### **segnaposto `NON_DEFINITA`** | ### **`187`** |
| ### **righe di storico** | ### **`1628`** |

```
classe    DIFETTO=200  NON_DEFINITA=187  MISURA=141  FRONTE=109  CRITERIO=90  CURA=56  PRESIDIO=34  STANDARD=29
dominio   FISICA=383  METODO=198  DA_CLASSIFICARE=187  INFRASTRUTTURA=49  DOCUMENTAZIONE=29
era       1=538  DA_CLASSIFICARE=188  ENTRAMBE=96  2=24
stato     SOSPESA=369  DA_CLASSIFICARE=188  CHIUSA=182  APERTA=82  AGENDA=24  SUPERATA=1
```

### ✔ **FATTO IN QUESTO GIRO:** il punto `4`: ### **`F8` perde il marcatore «un file `.py` del repo»**, che avevo aggiunto io. `F8` passa da `20` a ### **`14` segnali**, elencati nel commit.

### ⛔ **E DUE RICHIESTE DEL PUNTO `4` SONO INCOMPATIBILI, misurato:** *«DEVE scattare su `CONFIG-1` a `80eaf82`»* — ### **la- `CONFIG-1` e' era `1`**, e `F8` guarda solo le `ENTRAMBE`. E anche dove e' `ENTRAMBE`, l'unico marcatore che la prenderebbe ### **fa scattare `FALSO-ZERO`**, che il mandato precedente vieta. ### **La misura va nel referto: non scelgo io quale cade.**

### ⛔ **RESTA:** i punti `5` e `6`.

**Ultimo lotto applicato:** `doc/indice/_lotti/v3_indirizzate.jsonl` — ### **il punto `4` NON scrive sull'indice**: corregge un presidio.
