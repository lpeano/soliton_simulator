# TASK HISTORY — il video dagli snapshot: vedere le quattro componenti

**Data** 2026-09-20 · **branch** `fork-su2` · **HEAD** `a143dc1` · **blob** `775ceab7`
(sha1 dei byte grezzi verificato, non solo `git hash-object`) · albero **pulito** ·
dati: i **45 snapshot** di `csv/_test_fork/_g6000` (passi 60-2700, blob `7c4dec1d`).

> **NESSUN RUN DI FISICA. Il simulatore non si tocca. Nessuna cura, nessun verdetto.**
> E' un'ISPEZIONE: i numeri che escono di qui non entrano in un referto come risultato.

---

## 1. RAGIONAMENTO PRELIMINARE — cosa credo prima di guardare

Il referto della topologia (`3a02819`) dice che il grafo e' in **quattro componenti che non si
toccano mai**, e che i due picchi del grado sono **la semina**. Il conto geometrico lo spiega:
`rc = 3*median(lambda_nodi()) <= 2.4` contro `sep = 8` — **il raggio di allaccio e' tre volte piu'
corto della distanza fra le masse.**

Mi aspetto tre addensamenti separati che si espandono ciascuno per conto suo, dentro il quarto
pezzo (il vuoto seminato), e **mai un ponte**.

**Cosa NON so, e che il video potrebbe mostrare:**
- se cio' che sembrava «condensazione fra le masse» sia **il quarto pezzo** che si struttura per
  conto suo: spazialmente in mezzo, topologicamente scollegato;
- se le tre masse si avvicinino o si allontanino **nello spazio**, pur restando scollegate.

> **Il rischio e' di LEGGERE il video.** Un'immagine convince piu' di un numero, ed e' la terza
> immagine in due giorni dopo la Y e il protone — **le prime due sono cadute sotto misura.**

## 2. PROGETTAZIONE — come ci arrivo, e cosa decide ogni passo

### (1) IL BLOB — risolto PRIMA di scrivere il tool [fatto]
`carica_stato` confronta `db_blob` con `ver['blob']` e solleva `RuntimeError`: gli snapshot
sarebbero **rifiutati**.
**Strada B, gia' provata in `_scena_video_ripresa.py`:** nello SCRIPT si replica la logica di
`carica_stato` **meno la verifica del blob** — `setattr` degli `attrs`, ripristino di `rng_state`,
e **l'invalidazione delle cache derivate** (`_S`, `_perm`, `_ker_cache`), che e' la parte che si
dimentica e che romperebbe `_mat()`.
**Nessun flag nuovo nel simulatore. Nessuna riscrittura del blob negli snapshot.**

### (2) LE FUNZIONI DI DISEGNO SONO CAMBIATE FRA I DUE BLOB? NO — verificato [fatto]
Estratte una per una da `git cat-file -p 7c4dec1d` e confrontate col disco:

```
campo_spaziale   IDENTICA (56 righe)   carica_stato  IDENTICA (48)
pozzo_grafo      IDENTICA (22)         salva_stato   IDENTICA (69)
diagnostica      IDENTICA (32)         lambda_nodi   IDENTICA (23)
rilassa_disegno  IDENTICA (31)         _allaccia     IDENTICA (28)
intensita        IDENTICA (2)
```

L'intero delta fra i due blob e' di **70 righe in 5 punti**: i due flag sperimentali (~`:666`), il
sito della coppia (~`:2440`) e il cablaggio CLI (`:5578`, `:5624`, `:5992`). **Nessuno tocca il
rendering.**
> Va detto lo stesso in testa al video: **gli stati vengono da un blob, il disegno da un altro.**
> Che le funzioni coincidano lo rende innocuo, non lo rende taciuto.

### (3) NESSUNA FISICA — verificato dal codice, non promesso
Si chiamano **solo** `diagnostica()`, `campo_spaziale()`, `pozzo_grafo()`, `intensita()`.
**Non** si chiama `step()`, `mitosi()`, `rilassa_disegno()`, `memoria_hebbiana_moto()`,
`scuoti_vuoto()`.

Letto dal sorgente (era il precedente di `lambda_vuoto`, che sembrava di sola lettura e chiamava
`calcola_psi()`): `campo_spaziale` scrive **solo cache di rendering** (`_r3`, `_r3_G`,
`_ker_cache`); `lambda_nodi` alza `_calcolo_schermatura` e **lo riabbassa in un `finally``;
`pozzo_grafo`, `intensita`, `diagnostica` sono letture pure. **Nessuna chiama `calcola_psi()`.**
E tutto cio' che leggono — `pos`, `phi`, `psi`, `d`, `d0`, `tw`, `i`, `j` — **e' negli snapshot**,
verificato campo per campo.

### (4) I FLAG — percorso ufficiale, e si CONFRONTANO coi dati
`sys.argv` uguale a quello del driver, poi `_cli()` + `_applica_regime()` + `_applica_flag()`.
*(E' la lezione di ieri: un modulo importato senza `_applica_flag` ha `CAMPO_SPINORIALE=False`.)*
**E non basta applicarli: si confrontano uno per uno con i 20 flag scritti dal run stesso
nell'intestazione di `_g6000/prog.csv`** (P6). Se anche uno differisce, **STOP**: il disegno
dipende da `SCHERMATURA`, `CAMPO_SPINORIALE`, `GAMMA`, `LAM`.

### (5) LE QUATTRO COMPONENTI, A COLORI STABILI
Componenti connesse del grafo intero, **stessa costruzione del referto** (matrice simmetrizzata,
niente auto-anelli) e **stesso presidio P0**: il grado dalla matrice deve coincidere con `_deg`.

**Criterio di identita', dichiarato: ogni componente prende il colore del PIU' PICCOLO indice di
nodo che contiene.** Regge perche' gli indici sono stabili — **misurato, non assunto**: `eta[k]`
non diminuisce in nessuna delle 44 transizioni (`Z65`, P1) — e perche' ogni nodo nasce **dentro**
una componente. **Verifica per frame:** le componenti devono essere 4 e i quattro indici-ancora
devono restare gli stessi. Se cambiano **si stampa**, non si ricolora in silenzio.

**In sovrimpressione:** passo, `n`, numero di componenti, taglia di ciascuna, e **archi fra
componenti diverse, che deve restare 0** (la verifica visiva del reperto).

**Due pannelli:** a sinistra il **campo** (`campo_spaziale`, stessa ricetta di colore della GUI:
`CMAP_INTERF`, percentile 99 con memoria, gamma adattiva, soglia di trasparenza); a destra il
**grafo**, nodi a `pos[:, :2]`, **colore = componente**, luminosita' dal pozzo `phi_g` di
`pozzo_grafo()` — cosi' la funzione e' usata davvero, non citata.

### (6) DUE SCELTE DI RESA, dichiarate perche' cambiano cosa si vede
- **vista FISSA** (`M = None`, proiezione lungo `z`), non rotante: una camera che gira
  confonderebbe la lettura della separazione;
- **inquadratura FISSA su tutti i frame**, da una pre-passata che misura `max|pos|` snapshot per
  snapshot. Un'inquadratura ri-normalizzata a ogni frame **nasconderebbe l'espansione** — stesso
  motivo per cui `CLAUDE.md` par.4 vieta i confronti a passo fisso su un sistema che si dilata.
  **La serie dei `max|pos|` si stampa**, cosi' la monotonia e' un dato e non un'assunzione.

## 3. I PRESIDI
- il tool e' uno **strumento**, non una misura: nessun numero che ne esce entra in un referto;
- **la cadenza, dichiarata in testa al video:** 45 snapshot a **60 passi** contro i **6
  passi/frame** dell'originale -> **dieci volte piu' a scatti**, ~2.2 s a 20 fps. Serve a
  **ispezionare**, non a guardare;
- **il costo si misura sul primo frame e si riporta PRIMA** di lanciare su tutti e 45;
- **la cartella di output non si cancella** (`Z31`, ripetuto due volte in due giorni);
- **uno snapshot alla volta in RAM.**

## 4. COSA MI FA FERMARE
- un flag che non combacia con `prog.csv` -> **STOP**: starei disegnando un'altra fisica;
- le componenti che non sono 4, o gli indici-ancora che cambiano -> **si riporta**;
- una grandezza di disegno **non presente nello snapshot** e da ricalcolare -> **STOP e riporto
  quale**, come chiede il mandato;
- il costo del primo frame molto sopra i pochi secondi attesi -> riporto prima di lanciare.

## 5. TODO DEL NEXT STEP
1. [fatto] blob/branch dal disco; (1) e (2) risolti e verificati;
2. lo **strumento**, committato **prima** di girarlo;
3. **il primo frame** col costo -> riportare;
4. i **45 frame** e il video, coi quattro colori e i contatori;
5. presentare il file a Luca + relazione (par.5-ter).
