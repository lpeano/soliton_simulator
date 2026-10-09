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
| voci | `830` |
| ### **`DA_CLASSIFICARE` vere** *(non segnaposto)* | ### **`1`** |
| ### **segnaposto `NON_DEFINITA`** | ### **`181`** |
| ### **righe di storico** | ### **`1163`** |

```
classe    DIFETTO=210  NON_DEFINITA=181  FRONTE=169  CRITERIO=94  MISURA=68  CURA=46  PRESIDIO=34  STANDARD=28
dominio   FISICA=381  METODO=194  DA_CLASSIFICARE=181  INFRASTRUTTURA=47  DOCUMENTAZIONE=27
era       1=451  DA_CLASSIFICARE=182  ENTRAMBE=172  2=25
stato     SOSPESA=280  CHIUSA=187  DA_CLASSIFICARE=182  APERTA=156  AGENDA=25
```

### ✔ **FATTO IN QUESTO GIRO:** il punto `2`: ### **la classe `CRITERIO` e' una cosa sola** -- `58` voci da `FISICA` a `METODO` e ### **`13` ESITI MISURATI** a classe `MISURA` restando `FISICA`, ciascuno ### **con la frase che l'ha deciso**. `era` e `stato` ### **invariati**. `4` candidati ### **rifiutati leggendo** *(in `== 0` e in «contro `P2 = 27`» il numero e' ### **un controllo**, non una misura)*

### ⛔ **RESTA:** il punto `3` *(`F2`, le `8` eccezioni che citano il «sostituisce»)*, `4` *(`F3`)*, `5` *(`F4` e la ### **regola dell'intestazione**, collaudata su `POST-HOC` e `TW-1`)* e `6` *(il referto `doc/REFERTO_indice_v3_segnali.md`)*

**Ultimo lotto applicato:** `doc/indice/_lotti/v3_p2.jsonl`
