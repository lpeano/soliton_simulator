# `MAX-NODI-FERMA` — **la guardia di memoria FERMA il run** *(2026-09-28)*

> ### 🛑 **Scritto e committato PRIMA del lavoro** *(par.8)*. Il commit di questo file dev'essere
> **antenato** dei commit del codice e del sigillo.
> **Mandato di Luca:** *«MAX_NODI: fermare il run con errore esplicito nei tre siti (`:2924`,
> `:6058`, `:6481`). Sigillo byte-identico sulle 23 grandezze. Commit, STOP.»*
> **Blob del simulatore all'inizio: `1fc9235f`.**

---

# 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare*

## 1.1 — Le premesse, e da dove vengono

| | premessa | da dove |
|---|---|---|
| **①** | `MAX_NODI = 4000000` e il pilota sta attorno a **12 800** nodi: la guardia **non morde** nelle corse reali | voce `MAX-NODI-FERMA`, letta dal codice `:1851` |
| **②** | i tre siti oggi **cambiano la fisica in silenzio**: `:6058` restituisce **zero nascite**, `:2924` **tronca** la semina, `:6481` **spegne** il canale di Schwinger | letti dal codice sul blob `1fc9235f` |
| **③** | ### **il codice SA già che è sbagliato:** il commento di `:1851` dice *«se lo fosse, la misura è da rifare con più memoria, non da troncare»* | `:1851` |
| **④** | quindi il cambiamento dovrebbe essere **byte-inerte** col driver: nessuno dei tre rami viene percorso | conseguenza di ① |

## 1.2 — Che cosa mi aspetto

> ### **Byte-identico 23 su 23**, e i contatori identici. **Se NON lo è, la premessa ① è falsa** —
> cioè uno dei tre siti mordeva già — **e allora mi fermo**, perché vorrebbe dire che dei dati
> passati sono stati troncati in silenzio.

## 1.3 — ⚠ **CHE COSA NON SO**

| | |
|---|---|
| **①** | ### **non so se `MAX_NODI` possa essere SUPERATO DENTRO un passo.** `mitosi` crea nodi: se il controllo sta **all'inizio** del passo, il passo in corso può sforare e l'errore arriva **al passo dopo**. **Non so quanto sia il massimo sforo**, e non lo misuro qui |
| **②** | non so se `semina` con `n < 0` *(saturazione)* possa produrre **più di `MAX_NODI`** nodi dalla geometria: in quel ramo **il numero lo decide la geometria**, non il chiamante |
| **②-bis** | ### ✅ **RISPOSTO DAL GUARDIANO** *(Luca, 2026-09-28)*, e la risposta è **sì e no**: in saturazione il numero calcolato con `MAX_NODI` ### **non viene usato** — `_semina_lam` riceve `-1` e il numero lo decide la geometria con `n = len(p)`. ### **Quindi oggi la saturazione NON è controllata da `MAX_NODI`.** **Prescrizione:** il controllo va **dopo `n = len(p)`, sul numero vero, PER ENTRAMBI I RAMI.** *(La mia prima stesura ne metteva **due** — uno prima sul numero chiesto, uno dentro il solo ramo `SEMINA_LAM` — e quello dentro il ramo **lasciava scoperto l'altro ramo**.)* |
| **③** | ### **non so se qualcuno DIPENDA dal troncamento.** Se un test o una scena passa un `n` più grande di `MAX_NODI` aspettandosi il troncamento, con questa cura **muore**. Lo cerco, ma per nome: è un limite *(`A9`)* |
| **④** | non so se `MAX_NODI` sia letta da altri punti che non ho ancora visto: `:7872`, `:8157` la stampano, `:8427` la riscrive dal CLI. **Quelle sono stampe e configurazione, non fisica** — ma la lista dei siti l'ho fatta con `grep` |

---

# 2. PROGETTAZIONE DEL RAGIONAMENTO — *come intendo arrivarci*

## 2.1 — La forma della cura: **UN controllo, non tre**

**Il mandato dice *«UN controllo dello schedulatore»*.** Tre `raise` copiati in tre posti sarebbero
**tre leggi**, e `9-ter` dice di non moltiplicarle. Quindi:

```
class LimiteNodiSuperato(RuntimeError)          # un'eccezione DEDICATA, non un SystemExit generico
def _ferma_se_oltre_max_nodi(n_attuale, quanti, dove)   # UNA funzione, e non tronca mai
```

| sito | oggi | domani |
|---|---|---|
| **schedulatore** `esegui_passo` | *(niente)* | ### **il controllo, una volta per passo**, prima di validare la composizione |
| `:2924` `semina` | `max(0, min(n, MAX_NODI − self.n))` | ### **chiama il controllo e non tronca** |
| `:6058` `mitosi` | `if self.n >= MAX_NODI or not len(self.tw): return 0` | **resta solo** `not len(self.tw)` |
| `:6481` Schwinger | `if COPPIA_MIT > 0.0 and self.n < MAX_NODI:` | **resta solo** `COPPIA_MIT > 0.0` |

> ### 📌 **Perché il controllo va all'INIZIO del passo e non alla fine:** all'inizio è una
> **precondizione** — *«questo passo si può fare»* — e un passo che non si può fare **non comincia**.
> Alla fine sarebbe una **constatazione**, e lo stato sarebbe già oltre il limite.
> ### ⚠ **E il limite di questa scelta, dichiarato:** un passo che sfora **finisce**, e l'errore
> arriva **al passo successivo**. Lo **misuro nel sigillo** *(quanti nodi di sforo)* invece di
> supporlo.

## 2.2 — I passi, e **cosa decide ciascuno**

| | passo | che cosa decide | ### **cosa mi farebbe FERMARE** |
|---|---|---|---|
| **0** | **la dump PRIMA**, col simulatore ancora `1fc9235f` *(già committato)* | è il termine di confronto | — |
| **1** | **cerco chi dipende dal troncamento**: ogni chiamante di `semina` con `n` grande | se qualcuno ci conta, la cura cambia forma | ### **se trovo un chiamante che si aspetta il troncamento: FERMO e lo dico** |
| **2** | **il codice**: l'eccezione, la funzione, i quattro siti | — | ### **se per farlo funzionare servisse un numero nuovo: FERMO** *(`A1`, nessuna manopola)* |
| **3** | **la dump DOPO** e il confronto | ### **byte-identico 23/23?** | ### **se NON è identico: FERMO.** Vorrebbe dire che un ramo mordeva già |
| **4** | **il caso che DEVE fallire**: `--maxnodi` basso | il controllo **ferma davvero**? | ### **se NON solleva l'errore, il presidio non esiste** *(`A9`)* |
| **5** | **il controllo POSITIVO**: lo stesso comando sul blob **VECCHIO** | il vecchio **continuava** in silenzio? | ### **se anche il vecchio si fermasse, la cura non serve e l'avrei inventata** |

## 2.3 — Le letture si fissano **QUI**, prima di vedere i numeri

| | criterio | soglia |
|---|---|---|
| **A** | byte-identità sul driver | ### **23 grandezze su 23, 0 diverse** — nient'altro passa |
| **B** | il caso che deve fallire | l'eccezione è **`LimiteNodiSuperato`**, il messaggio **nomina `MAX_NODI`** e **dice il numero**, e il processo **esce diverso da 0** |
| **C** | il controllo positivo | il **vecchio blob**, stesso comando, **esce 0** e produce uno stato |
| **D** | lo sforo dentro il passo | **si RIPORTA il numero**, non è un criterio di successo |

**⚠ E il criterio `B` è il più importante**, perché è `P1-sexies`: **il caso che deve fallire è
quello che dimostra che il presidio esiste.** Un presidio che non fallisce mai **non si distingue da
uno assente** *(`A9`)*.

---

# 3. TODO DEL NEXT STEP — *operativa*

| | |
|---|---|
| ☐ | **dump PRIMA** col blob `1fc9235f`: `python csv/_test_fork/_hashseed_prova.py --out=…PRIMA.npz --seme=11 --passi=3` |
| ☐ | **cercare i chiamanti di `semina`** e vedere se qualcuno passa un `n` vicino a `MAX_NODI` |
| ☐ | scrivere **`LimiteNodiSuperato`** e **`_ferma_se_oltre_max_nodi`**, e cablarli nei **quattro** punti *(i tre siti più lo schedulatore)* |
| ☐ | aggiornare il **commento di `:1851`** nominando `MAX_NODI` *(`H-P7`)*, il **README** *(par.6 ②)* e **`REGISTRO_FISICA`** |
| ☐ | **commit del codice**, col blob prima → dopo |
| ☐ | **`csv/_seal_fork/_sig_max_nodi.py`**: i tre bracci `A`, `B`, `C`, più la misura `D` |
| ☐ | **commit del sigillo**, poi ### **STOP** |

> ### ⚠ **Due commit e non uno, e la ragione è il par.5:** *«il codice che genera un output dev'essere
> già committato quando l'output nasce»*. Il sigillo gira **sul simulatore curato**: se codice e
> sigillo stessero nello stesso commit, l'output sarebbe nato **prima** del commit del codice che
> l'ha prodotto. **Luca ha scritto «Commit, STOP» al singolare: lo leggo come «poi committa e
> fermati», e dichiaro qui perché sono due.**
