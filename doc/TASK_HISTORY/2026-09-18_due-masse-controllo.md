# TASK HISTORY — **il run di controllo a DUE masse, e la predizione committata prima**

**Data:** 2026-09-18 · **Branch** `fork-su2` · **HEAD alla scrittura** `4f56730`
**Blob:** `a1ae5090` — **e non cambierà: nessuna cura, nessun cablaggio.**

---

## 1. RAGIONAMENTO PRELIMINARE

### 1.1 Perché questo run vale, e non è una conferma cercata

**È un A/B a variabile singola: cambia SOLO `--nmasse`, da 3 a 2.** Tutto il resto — flag, seme,
driver **sigillato**, 400 frame, istanti di snapshot — **identico a `Z49`.**

> **E la domanda non è «si ripete?» ma «il ciclo dipende dalle TRE MASSE o dal SISTEMA?»**
> **Se dipende dal sistema è un oscillatore di rilassamento, e la cosa si ridimensiona: è un
> risultato utile quanto l'altro.**

### 1.2 ⚠ IL PUNTO DI METODO, e viene prima di tutto

**La predizione è committata PRIMA del run** *(stesso giro, commit dedicato)*. **Se il run partisse
prima, il risultato sarebbe un'osservazione e non una predizione.** È par.5-septies applicato a una
previsione **di Luca**, non mia — **e vale esattamente per lo stesso motivo.**

**E ho scritto la lettura che la FALSIFICA con lo stesso peso**, col meccanismo candidato già
nominato *(`lambda_nodi` che accorcia la portata dove la densità cresce)*. **Una predizione senza il
suo falsificatore scritto accanto non è una predizione: è una scommessa.**

### 1.3 ⚠ LA REGIONE INTERNA VA RIDEFINITA, e senza questo il confronto NON tiene

**Con tre masse il centro è equidistante da tutte e tre; con due è il punto medio di un segmento.**
**`r < 4` non significa la stessa cosa nelle due geometrie.**

**Scelta, dichiarata:** **regione interna = `r < R_anello(t)/2`**, con **`R_anello(t)` MISURATO**
*(mediana del raggio dei nodi seminati a `t = 0`)*, **e `R_anello(t)` riportato a ogni istante.**
**Riporto entrambe le letture, assoluta e comovente**, come in `Z49`.
**⚠ In `Z49` coincidevano solo perché `R_anello` variava dell'8 %: NON è una licenza generale, e con
due masse va RIVERIFICATO.**

### 1.4 Cosa mi aspetto, e cosa NON so

**Non ho una predizione mia sull'esito**, e non me la invento per averne una. **La predizione è di
Luca, ed è quella che si misura.**

**Quello che posso dire prima, e lo dico:** la scena a due masse avrà **`n` iniziale ≈ 2/3** di
quella a tre *(`~1594` contro `2391`)*, perché `_semina_n_masse` semina `N_c·0.8` **per massa**.
**Se il pilota desse un `n` molto diverso, la scena non sarebbe confrontabile per popolazione e
andrebbe detto.**

**Non so** se il ciclo dipenda dal numero di masse, dalla geometria, o dalla densità totale — **e il
run a due masse non le separa tutte e tre**: cambia il numero **e** la popolazione **e** la
simmetria. **È un A/B su `--nmasse`, non su «tre corpi».** **Va scritto nel referto come limite.**

---

## 2. PROGETTAZIONE

**Pilota** per la durata *(non estrapolo: il costo cresce con `n`, e qui `n` parte più basso)* →
`STATO_RUN.md` all'avvio → **il run**, 400 frame, snapshot `10/115/190/270/375/400`.

**Le misure, le STESSE di `Z49` agli STESSI istanti:**
`nodi(regione interna)` **— la curva che decide, monotona o a U** · `rho_spin` e `|psi|` interni ·
`d` **media, mediana e p95** *(in `Z49` dicevano cose opposte: si riportano tutte e tre)* ·
la dilatazione · **il grado dell'anello** · **`r` da `eta += DT·r`**, interno contro anello.

**LE LETTURE, e sono le tre del mandato:**
- **ciclo assente o forma completamente diversa** → **la predizione di Luca REGGE;**
- **ciclo uguale** → **è un oscillatore di rilassamento del sistema: la predizione è SBAGLIATA, e si
  scrive che è sbagliata;**
- **ciclo con forma o periodo diversi** → **né l'una né l'altra: si riporta come tale.**
- **⚠ E una mia:** **se il ciclo c'è ma `rho_spin` NON si accende**, allora **«ciclo» e «accensione»
  sono due fenomeni separabili** — **e sarebbe più informativo di entrambe le letture del mandato.**

**COSA MI FA FERMARE:** nulla di tecnico. **Ma nessuna identificazione di fisica** — *bounce*,
*oscillone*, *collasso*, *protone* **non si scrivono**, qualunque forma esca.

---

## 3. TODO DEL NEXT STEP

- [x] **la predizione committata PRIMA del run** (§1 del mandato)
- [x] pilota per la durata → `STATO_RUN.md` all'avvio
- [x] il run: 400 frame, `--nmasse 2`, **tutto il resto identico** *(chiuso, 1h29, `n` 1894 → 5878)*
- [x] la regione ridefinita (§1.3) + le misure agli stessi istanti
- [x] **verdetto contro le TRE letture** — **la predizione è SBAGLIATA nella forma forte, ed è scritto**
- [x] referto + registro + relazione **nello stesso commit** *(`Z52`, `doc/REFERTO_due_masse.md`, §9.66)*
- [x] **⚠ NON toccato:** nessuna cura, nessun default, nessuna identificazione

### ⚠ ESITO — **scatta la TERZA lettura, e il §1.3 si è rivelato NECESSARIO**

- **la predizione è sbagliata nella forma forte:** il ciclo **c'è** anche a due masse, e la **discesa**
  è la stessa entro il 20 % su quattro letture, **col minimo allo stesso istante**;
- **ma non scatta nemmeno la ② secca:** `recupero/crescita` vale **`1.9624` contro `0.9906`**, e
  l'accensione finale **`×22.46`**. **Lo svuotamento è del sistema, il riempimento e l'accensione
  dipendono dal numero di masse.**
- **la MIA lettura (§2, il falsificatore 3) NON scatta alla lettera:** `rho_spin` **si accende** anche
  a due masse (`×5512`). **La separabilità c'è, ma lungo una cucitura diversa da quella che avevo
  previsto** — ed è un errore di previsione mio, non della misura;
- **il §1.3 non era una formalità:** `R_anello` varia il **`20.1 %`** a due masse contro il `9.1 %` a
  tre. **La riserva scritta prima — «in `Z49` coincidevano solo perché variava dell'8 %, e con due
  masse va RIVERIFICATO» — era giusta**, e senza la lettura comovente avrei riportato un recupero di
  `2.31` invece di `1.74`.

### TODO — il passo successivo

- [ ] **§1② del mandato coorti: la persistenza di `conc_nodi`/`conc_archi`/`masse_info` nello
      snapshot** + sigilli **`S0-S6`** — **ora SBLOCCATO: il run è chiuso e la CPU è libera** *(era
      il vincolo del `2026-09-18_coorti-tracking.md` §1.4)*
- [ ] **≥ 4 semi per braccio** se `Z52` deve diventare un fatto e non un rapporto senza barra
