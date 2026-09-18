# TASK HISTORY — **metà dei nodi non invecchia?** E un conto che si può fare PRIMA di misurare

**Data:** 2026-09-18 · **Branch** `fork-su2` · **HEAD alla scrittura** `e9feb93`
**Blob:** `a1ae5090` — **e non cambierà: nessuna cura, solo lettura dei `.pkl` già esistenti.**

---

## 1. RAGIONAMENTO PRELIMINARE

### 1.1 ⚠ IL CONTO CHE VIENE PRIMA DELLA MISURA — **e dice già QUALE r hanno**

`eta += dt_n = DT · r`. Quindi **dalla crescita di `eta` si RICAVA `r`**, senza aprire niente.

Misurato *(e già nel repo, `9.56-bis`)*: `eta` mediana da **`0.0100017`** (passo 120) a
**`0.0100096`** (passo 680) = **`7.9e-06` in 560 passi**.

E il **pavimento assoluto** di `r` in `ritmo()` — `r = x/√(1+x²) + 1e-6`, `r_unit = 1/√2 + 1e-6`,
quindi `r_min = 1e-6/(1/√2 + 1e-6)`:

```
r al PAVIMENTO              : 1.414212e-06
dt_n = DT * r_floor         : 1.414212e-08
eta accumulata in 560 passi : 7.919585e-06     <- PREVISTO dal solo pavimento
eta MISURATA (120 -> 680)   : 7.900000e-06
rapporto                    : 1.0025
```

> **⚠ COINCIDE ALLO 0.25 %.**
> **PREVISIONE, scritta PRIMA di aprire i `.pkl`: il nodo MEDIANO ha `r` AL PAVIMENTO ASSOLUTO.**
> **Non «piccolo»: `1.414212e-06`, il valore che `ritmo()` restituisce quando `x = 0`.**

**Se è vero, la catena si chiude su tutto ciò che abbiamo trovato in questa sessione:**

```
la maggioranza dei nodi ha  f << median(|f|)   ->  x ~ 0  ->  r al PAVIMENTO  ->  dt_n ~ 1.4e-08
  ->  eta NON cresce  ->  ramp ~ 0  ->  il kernel di quei nodi non si accende MAI
```

**E riconcilia `Z44` con questo:** `Z44` contò i nodi con **`f` ESATTAMENTE zero** — erano **1-2 su
450**, perché `psi_spin = 0` esatto. **Qui non si tratta di `f = 0`: si tratta di `f` così piccolo
rispetto al gauge che il bottleneck li appiattisce sul pavimento.** **Due cose diverse, e la seconda
è molto più grande della prima.**

**E tocca `Z43`:** se il nodo **mediano** è un nodo **mai maturato**, allora **`median(|f|)` — il
gauge del tempo — è calcolato su una popolazione la cui metà sta al pavimento.** **Il metro è
costruito su chi non si muove.** *(È la NOTA del mandato, e il conto la sostiene.)*

### 1.2 ⚠ IL FALSIFICATORE DELLA MITOSI È GIÀ ESCLUSO DALL'ARITMETICA — ma lo verifico

`n` va da **1196 a 1204** in 1090 passi: **otto nodi.** **Se i fermi fossero i neonati, sarebbero
OTTO, non metà.** **Il mandato lo dice, e i numeri lo confermano — ma lo misuro, non lo assumo.**

**E l'età anagrafica è ricavabile senza un campo dedicato:** i nodi si **appendono** in coda, quindi
**l'INDICE è l'ordine di nascita**. Indice `< 1196` ⟹ seminato a `t = 0`. **Esatto, non stimato.**

### 1.3 ⚠ «Mediana bassa» contro «mediana PINNATA» — la distinzione che il mandato chiede

**La mediana NON è pinnata in senso stretto: si muove**, da `0.0100017` a `0.0100096`. **Si muove
alla QUINTA cifra decimale, e si muove ESATTAMENTE di quanto il pavimento impone.**
> **Non è «congelata per identità algebrica» (quello sarebbe A3): è congelata DALLA DINAMICA.**
> **È una distinzione importante e va scritta giusta nel referto.**

### 1.4 Cosa NON so

- **la FRAZIONE** esatta al valore di semina, e **se cala nel tempo**;
- **se siano SEMPRE GLI STESSI** — è la misura ② e decide fra congelamento e flusso;
- **se i fermi coincidano coi nodi con `f = 0`** di `Z44` *(prevedo di NO: quelli erano 1-2)*;
- **dove stanno** e **che grado hanno.**

---

## 2. PROGETTAZIONE

**Tutto dai `.pkl` già presenti** — istanti veri **120, 130, 470, 800, 1200** *(si citano col loro
`_db_step`, mai col nome del file: il primo watcher li aveva mislabellati)*. **Nessun run nuovo.**

**①** distribuzione di `eta`: `p05/p25/mediana/p75/p95/max` + **frazione entro una tolleranza
DICHIARATA** dal valore di semina, ai cinque istanti.

**②** **identità**: gli indici dei fermi fra istanti consecutivi — **Jaccard**, lo stesso metodo di
`Z44`. **E chi sono**: indice, grado, raggio dal centro.

**③** **il falsificatore**: nodi nati dopo `t = 0` *(indice ≥ n₀)*, e **`eta` dei fermi contro la
loro età anagrafica.**

**④** **`r` dei fermi contro la popolazione** — e **quanti di loro hanno `f = 0` esatto**
(il confronto diretto con `Z44`). *(`r` si ricava da `eta(t₂) − eta(t₁)` fra due snapshot: è la
definizione stessa, `eta += DT·r`, e non richiede che `r` sia salvato.)*

**LE LETTURE, FISSATE ADESSO** *(le quattro del mandato, più una mia)*:
- **frazione ~50 %, sempre gli stessi, `n` quasi costante** → **metà del sistema CONGELATA: `Z9` va
  riscritta. Riporta e FERMATI;**
- **flusso che riparte** → transitorio di nascita — **ma con 8 nodi nuovi non torna: cerca
  l'incoerenza;**
- **mediana bassa ma frazione «alla semina» piccola** → **coda, non congelamento;**
- **nessuna regge** → si dice, **senza inventare la quinta.**
- **⚠ LA MIA:** **se `r` dei fermi coincide col PAVIMENTO `1.414212e-06`**, allora **la causa non è
  `eta` né `ramp`: è il BOTTLENECK di `ritmo()` che li appiattisce**, e `Z9` non è la voce giusta —
  **la voce giusta è `Z43`.** **E allora l'ordine dei due mandati si inverte.**

**COSA MI FA FERMARE:** la prima lettura. **E in ogni caso: nessuna cura, nessun cablaggio, nessun
run nuovo, `EMB_IT`/`TAU_A`/`ramp` non si toccano.**

---

## 3. TODO DEL NEXT STEP

- [x] **①** distribuzione di `eta` e frazione alla semina, ai cinque istanti
- [x] **②** sono sempre gli stessi? (Jaccard) e **chi sono** (grado, raggio)
- [x] **③** il falsificatore della mitosi: età anagrafica dall'indice
- [x] **④** `r` dei fermi contro la popolazione, e **il confronto con `f = 0` di `Z44`**
- [x] **verdetto contro le cinque letture**, **senza curare**
- [x] se regge la prima: **proporre il TESTO di `Z9` riscritta, NON cablarlo**
- [x] registro + relazione + **CHECKPOINT**
- [x] **⚠ NON toccato:** `EMB_IT`, `TAU_A`, `ramp`, il gauge, il `+1e-6`

---

## 4. ESITO

**PRESO, ed era il contributo del giro: il conto fatto PRIMA di aprire i `.pkl`.**
Avevo previsto `r_fermi/r_floor = 1.0025` dalla sola crescita di `eta`; **misurato `1.0000`, su
quattro intervalli su quattro, p95 incluso.** **La quinta lettura — la mia — era quella giusta: la
causa non è `eta` né `ramp`, è il pavimento di `ritmo()`.**

**PRESO: il falsificatore della mitosi**, escluso in modo totale (4 nodi nuovi, **zero** fermi fra
loro), e l'età anagrafica ricavata **esattamente** dall'indice invece che stimata.

**PRESO: la distinzione «mediana bassa» contro «mediana pinnata».** La risposta è **nessuna delle
due**: `p05 = p25 = mediana = p75` **identici** — **non una mediana bassa, un BLOCCO.**

**NON PRESO — e sono due, entrambe più grandi di quanto mi aspettassi:**
1. **la frazione: prevedevo «~50 %», è il `93 %`**, e **non cala** in 1200 passi;
2. **CHI sono.** Non l'avevo previsto affatto: **sono LE TRE MASSE** (grado `371`, raggio
   `8.00 = sep`), e i mobili sono **il centro** (grado `9`). **La domanda «metà dei nodi non
   invecchia?» aveva una risposta strutturale, non statistica.**

**E UNA COSA CHE NON SO SPIEGARE, e non la invento:** perché i nodi a grado **371** abbiano
`|psi_spin|` **mille volte più debole** di quelli a grado **9**. **È il fatto più strano della
misura.** La quinta lettura diceva *«nessuna regge → si dice, senza inventare»*: **lo dico.**

## 5. TODO DEL PROSSIMO PASSO

- [ ] **`Z9` riscritta: il testo è PROPOSTO nel referto §8, decide Luca.** Il punto chiave è il
      criterio di chiusura: **non «`ramp` mediano cresce»**, perché quel `ramp` è di un nodo fermo
- [ ] **`Z43` va rovesciata:** in questa configurazione il metro **è `1e-9`**, non oscilla del 62 %
- [ ] **la domanda aperta:** perché grado alto ⟹ `|psi_spin|` mille volte più debole?
- [ ] **la precedenza col mandato sull'embedding la decide Luca**
- [ ] **⚠ NON toccato:** `EMB_IT`, `TAU_A`, `ramp`, il gauge, il `+1e-6`, il `max(...,1e-9)`
