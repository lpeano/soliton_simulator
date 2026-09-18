# TASK HISTORY — **`Z9` rimisurata sul blob ATTUALE**

**Data:** 2026-09-18 · **Branch** `fork-su2` · **HEAD alla scrittura** `993240d`
**Blob:** `72acd6aa` (git) / `aa84755b` (byte grezzi) — *sono due spazi di hash diversi*
**Task:** Luca rileva che il numero di `Z9` è vecchio di **due generazioni di codice**, e chiede di
rifare la misura già fatta due volte: **`ramp` mediano ai passi 1 / 60 / 120**, contro
**`0.0002 / 0.0106 / 0.0217`**.

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare*

### Il rilievo di Luca è corretto, e l'ho verificato dalla storia

```
Z9 aperta        blob 69ee5403
Z9 RIMISURATA    blob a8f1b2f4   -> "sostanzialmente INTATTA"
blob ATTUALE     72acd6aa
```

Fra `a8f1b2f4` e oggi sono entrati `Z25`, `Z24/Z27`, **e i due default `SPINORE_VIVO = True` e
`SPIN_FEEDBACK = True`.** **Il numero è vecchio, e va rimisurato prima che qualcosa vi poggi sopra.**

### Il meccanismo che Luca descrive è reale

```
eta += dt_n      dt_n = DT · r      r = ritmo()      r dipende da psi
```

Il feedback ora gira e aggiunge un termine a `coppia` → `phivel` → `phi` → `psi` → `r` → `dt_n` →
`eta`. **La catena esiste tutta**, e `SPINORE_VIVO` acceso cambia l'evoluzione SU(2) a monte.

### ⚠ MA PRIMA DI MISURARE, P4: **la grandezza è LIBERA di cambiare?**

Letto `ritmo()` dal sorgente (`:2043-2049`), **non citato da C12**:

```python
f   = signed if TEMPO_PROPRIO_ORIENTATO else np.abs(signed)
med = max(median(|f|), 1e-9)
x   = f / med
r   = x/sqrt(1+x^2) + 1e-6            # MONOTONA in x
r_unit = 1/sqrt(2) + 1e-6             # il valore di r a x = 1
return 1.0 + TAU_LOC * (r/r_unit - 1.0)        con TAU_LOC = 1.0
```

**`TEMPO_PROPRIO_ORIENTATO = False` di default** (`:741`), quindi **`f = |signed| ≥ 0`** e
**`median(x) = 1` ESATTAMENTE.** La mappa `x → r` è monotona, quindi `median(r) = r_unit`, quindi
**il valore restituito ha mediana `1.0` ESATTA**, qualunque cosa faccia `psi`.

> **Quindi `median(dt_n) = DT` esattamente, e l'incremento MEDIANO di `eta` per passo è PINNATO PER
> COSTRUZIONE.** Il meccanismo che Luca descrive **è bloccato al primo ordine da una
> normalizzazione**.

**È C12 — ma la condizione andava verificata, non citata:** con
`--tempo-proprio-orientato` l'ancoraggio **cadrebbe**, perché `f` sarebbe firmato mentre `med` resta
`median(|f|)`. **Di default il flag è off, quindi l'ancoraggio tiene.**

### Cosa può ANCORA cambiare, ed è lì che va guardato

1. **La FORMA della distribuzione di `r`**, non la sua mediana: `eta` è una **somma su molti passi**,
   e `median_nodi(Σ_t r_t) ≠ Σ_t median_nodi(r_t)`. **Se cambia QUALI nodi sono veloci, la mediana
   accumulata si sposta anche con la mediana istantanea fissa.**
2. **La POPOLAZIONE**: più o meno nodi, e soprattutto **quanti neonati** (che entrano con `eta = 0`
   e abbassano la mediana). **Il conteggio nodi è cambiato** — `548 → 461` dopo `Z27` su un seme.
3. **`TAU_A`**: `ramp = min(1, eta/TAU_A)`. Le misure storiche di `Z9` sono a **`TAU_A = 50`**, le
   mie recenti a **`2.0`**. **Confrontare `ramp` fra i due sarebbe A3c puro.** **Va rifatta a
   `TAU_A = 50`**, che è la configurazione delle misure storiche.

### La mia previsione, dichiarata perché può essere sbagliata

**Mi aspetto `ramp` mediano sostanzialmente invariato** — entro un fattore ~2, non ordini di
grandezza — **perché il canale principale è pinnato.** **Se cambiasse molto, la causa NON sarebbe
quella che Luca descrive**, e andrebbe cercata nella popolazione (punto 2).

**Cosa NON so:** quanto pesi il punto 1 (la forma della distribuzione) rispetto al punto 2 (i
neonati). **Non l'ho mai separato, e potrei non riuscirci in questo giro.**

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *i passi, cosa decide ciascuno, cosa mi ferma*

**Passo 0 — LO STRUMENTO.** `csv/_test_fork/_rimisura_Z9.py` **esiste già ed è committato**: è la
stessa misura fatta due volte. **Si rifà quella, non se ne scrive una nuova** — è il punto di
par.5-quinquies. **MA va verificato che misuri la configurazione NUOVA:** la sua lista di flag
**non contiene `SPIN_FEEDBACK`**, e funziona **solo perché il default è stato promosso**. *Decide:*
se la misura è sulla config attuale o su quella vecchia. **Da stampare, non da assumere.**

**Passo 1 — P4: verificare l'ancoraggio invece di fidarsi del ragionamento.** Misurare
`median(ritmo())` sui passi: **deve valere `1.0` a meno dell'epsilon.** *Decide:* se la previsione
di §1 poggia su un fatto o su una mia lettura.

**Passo 2 — LA MISURA STORICA, a `TAU_A = 50`.** `ramp` mediano ai passi **1 / 60 / 120**, contro
`0.0002 / 0.0106 / 0.0217`, **e il passo estrapolato per `ramp = 1`** contro `~5526`.
**Le due scene, come nella rimisura precedente:** quella **originale** (confrontabile coi numeri
storici) e quella del **batch** (il sistema che gira davvero). **Non si mescolano.**

**Passo 3 — se il numero è cambiato, SEPARARE LE CAUSE:** crescita di `eta` per passo (il canale
pinnato) contro **frazione di neonati** nella popolazione (il canale della mediana).

**LE LETTURE, FISSATE ADESSO:**
- **`ramp` invariato entro un fattore ~2** → `Z9` regge, il numero si aggiorna e **non cambia
  nessuna conclusione**;
- **`ramp` molto più grande** (maturazione più rapida) → `Z9` si **allenta**, e va detto **quanto**;
- **`ramp` molto più piccolo** → `Z9` **peggiora**, e ogni misura a 120 passi vive ancora più
  profondamente nel transitorio;
- **in ogni caso**, se cambia **mentre `median(r) = 1.0` regge**, la causa è la **popolazione**, non
  il meccanismo di Luca — **e questo è il risultato che mi interessa di più.**

**COSA MI FA FERMARE:**
- se lo strumento risultasse misurare la config **vecchia** → si riporta **quello** prima di tutto,
  ed è un difetto dello strumento, non un risultato su `Z9`;
- se `median(r)` **non** fosse `1.0` → la mia lettura di `ritmo()` è sbagliata, **e va riportata
  prima della misura**.

**E una cosa che NON farò:** non deciderò se `Z9` precluda `Z30`. **Misuro il numero**; la
conseguenza è di Luca.

---

## 3. TODO DEL NEXT STEP

- [x] **passo 0** — verificare che `_rimisura_Z9.py` misuri la config **nuova** *(lo fa solo perché
      il default è stato promosso: va stampato)*
- [x] **passo 1** — `median(ritmo())` è `1.0` all'epsilon? *(P4: la grandezza è libera di cambiare?)*
- [x] **passo 2** — `ramp` mediano a **1 / 60 / 120**, **`TAU_A = 50`**, **due scene separate**
- [x] **passo 3** — se cambia: separare *crescita di `eta`* da *frazione di neonati*
- [x] referto + `Z9` aggiornata **col blob e la data** + relazione + riportare a Luca
- [ ] **⚠ NON toccare:** `Z30` (decisione di Luca), `Z31`, il punto 1 di `Z24`

---

## 4. ESITO — *cosa il ragionamento preliminare aveva preso, e cosa no*

**PRESO, ed era il contributo principale:** il rilievo **P4** — *la grandezza è libera di cambiare?*
La risposta è **no al primo ordine**, e questo **spiega** il risultato invece di limitarsi a
riportarlo. Senza quel passo avrei scritto *«Z9 non è cambiata»* senza sapere **perché**, e il
prossimo che cambia `psi` si sarebbe rifatto la stessa domanda da capo.

**PRESO anche:** il difetto dello strumento (la lista di flag senza `SPIN_FEEDBACK`) e il rischio
`A3c` su `TAU_A`, entrambi trovati **prima** di misurare.

**E la previsione era giusta:** *«invariato entro un fattore ~2»* → **entro il 3 %**.

**NON PRESO:** **ho scritto male il criterio P4 due volte di fila.** Prima col **massimo** — che
dava `1.000e+00` e avrebbe detto il contrario del vero. Poi con una soglia di `1e-6` che ha
etichettato **116 chiamate su 246** come «degeneri» quando sono `1.0` a quattro cifre.
**In un giro dedicato a verificare un ancoraggio, ho sbagliato due volte lo statistico con cui lo
verificavo.** È la stessa famiglia che continuo a catalogare negli altri, e stavolta è mia due
volte di seguito.

**E una cosa che non avevo previsto:** il fallback su `_cs_nodo_prev` è **1.21 %**, non zero.
**Piccolo ma non nullo, e non l'ho interpretato** — manca il confronto con la rimisura precedente.

## 5. TODO DEL PROSSIMO PASSO *(aggiornato)*

- [ ] **il numero da citare d'ora in poi è quello della scena (B): `ramp = 1` a `~6049` passi**
- [ ] **`Z9` NON precludeva `Z30`**: la decisione su `nudo`/`linea` è di Luca, sui due punti insieme
- [ ] **da verificare:** il fallback `_cs_nodo_prev` all'**1.21 %** — era zero nella rimisura
      precedente? *(non ho il numero sottomano: va ripreso dal referto di allora)*
- [ ] **⚠ NON toccare:** `Z31`, il punto 1 di `Z24` (`refl` = legge nuova)
