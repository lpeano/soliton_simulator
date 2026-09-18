# REFERTO — **La cucitura FALLISCE su entrambi i fronti, e si dimostra perché. NON si cabla**

**Data:** 2026-09-18 · **Blob** `f8f46683` (git) / `94b6cc29` (byte) · un seme (5), 120 passi
**Task history con l'obiezione, scritto e pushato PRIMA:** `02ac909`
**Strumento:** `csv/_test_fork/_Z36_cucitura.py` · **NESSUNA CURA CABLATA**

---

## 0. IL VERDETTO, in quattro righe

1. **Il candidato del mandato (§2) è ESCLUSO:** `|psi_spin[:,0]|/|psi_spin|` ha **mediana 0.9999** e
   **minimo 0.899**. **La componente non si annulla mai.**
2. **La cura toglie il 98 % del segnale:** livello `median|a|` da **3.94e-04** a **7.03e-06**,
   **rapporto 0.0179**.
3. **E non riduce nemmeno il salto: lo PEGGIORA**, da **0.712** a **0.786**.
4. **⚠ E si dimostra perché:** poiché la componente 0 è il **99.99 %** dello spinore,
   `angle(overlap) ≈ a_originale` — **la cura sottrae una quantità a sé stessa**, e resta la
   cancellazione. **Era destinata a fallire su questo oggetto.**

---

## 1. (A) IL CANDIDATO DEL MANDATO È ESCLUSO

```
|psi_spin[:,0]| / |psi_spin|   (13320 nodi-istanza, ultimi 30 passi)
   mediana 0.999881   p05 0.990825   p01 0.976511   MIN 0.899377
   frazione sotto 1e-1 / 1e-2 / 1e-3 / 1e-6 / 1e-9 :  0.000000  su tutte
```

**La prima componente non passa mai vicino a zero: è sempre almeno il 90 % del modulo.**
`angle(psi_spin[:,0])` **non è mal definito.**

> Il sospetto del mandato — *«uno spinore ruota fra le due componenti, la prima passa per zero
> regolarmente»* — **non si verifica in questo sistema.** Lo spinore **non ruota** fra le componenti:
> resta quasi interamente sulla prima.

## 2. (C) GLI STATI CONSECUTIVI SONO **QUASI IDENTICI**

```
|<psi_prec|psi>| normalizzato :  mediana 1   p05 0.999957   frazione > 0.99 = 1.0000
```

**Il 100 % delle coppie consecutive ha overlap > 0.99.** Il campo spinoriale **si muove
pochissimo** da un passo all'altro.

## 3. (B) NESSUNA CORRELAZIONE — **la parametrizzazione non c'entra**

```
corr( log(comp0/|psi|), log(salto relativo) ) = -0.0017     su 52149 nodi-coppia
tutti i 52145 nodi-coppia stanno nella fascia comp0 > 1e-1
```

**Correlazione praticamente nulla, e non esiste nemmeno una fascia a componente piccola da
confrontare.** **Il candidato del mandato cade due volte: per assenza della causa e per assenza di
correlazione.**

## 4. (D) ⚠ LA CURA FALLISCE SU ENTRAMBI I FRONTI

| | `a` ORIGINALE | `a` CURATO |
|---|---|---|
| **LIVELLO** `median\|a\|` | **3.94e-04** | **7.03e-06** |
| **SALTO** `\|Δa\|/\|a\|` | **0.712** | **0.786** |
| rapporto livello curato/originale | | **0.0179** |

**Il livello crolla di 56 volte — la cura toglie il 98 % del segnale.** Ed **è la lettura che avevo
previsto nel task history**, scritta prima di misurare.

**Ma c'è di peggio, e non l'avevo previsto: il salto NON scende, PEGGIORA** (`0.712 → 0.786`).
**Quindi non è nemmeno un compromesso «meno segnale ma più stabile»: è peggio su entrambi gli assi.**

### E la dimostrazione del perché — **era destinata a fallire su questo oggetto**

Da (A): la componente 0 è il **99.99 %** dello spinore. Quindi

```
overlap = Σ conj(psp)·ps  ≈  conj(psp[:,0])·ps[:,0]
=>  angle(overlap) ≈ angle(ps[:,0]) − angle(psp[:,0]) = a_originale
=>  a_curato = a_originale − angle(overlap) ≈ 0   +  cancellazione
```

> **La cura sottrae `a` a sé stessa.** Ciò che resta è **cancellazione catastrofica** — differenza di
> due quantità quasi uguali — **e per questo il salto relativo AUMENTA invece di diminuire.**

**Il conto nel task history era giusto nella conclusione e incompleto nella ragione:** avevo scritto
che per rotazione rigida `a_curato = 0`. La misura dice che **non serve la rotazione rigida**: basta
che **una componente domini**, ed è il caso qui al 99.99 %.

### E perché nel lift funziona, mentre qui no

Nel lift le due componenti sono `cos(θ/2)` e `sin(θ/2)e^{iφ}` — **entrambe vive**, e la fase globale
è **gauge**. Qui **una componente ne porta il 99.99 %**, e la sua fase **è il segnale**.
**Lo stesso codice, su oggetti diversi, fa cose opposte.**

---

## 5. ⚠ E `Z36` VA RI-LETTO — **il `64.7 %` è un rapporto su una grandezza minuscola**

Da (C), gli stati consecutivi hanno overlap **> 0.99 nel 100 % dei casi**, e da (D) il livello di `a`
è **3.94e-04 rad/passo**.

> **Il «tempo proprio salta del 65 %» significa: una fase che avanza di `4e-04` per passo varia del
> 65 % di quel `4e-04`, cioè di `~2.8e-04`.** In valore assoluto è **più piccolo** del salto del
> feedback (`1.1e-03`).

**È la stessa forma dell'errore del `2.706`: un rapporto grande perché il denominatore è piccolo.**
**La mia frase precedente — *«il tempo proprio non è cucito, venti volte peggio del feedback»* — resta
vera sul RAPPORTO, ma va qualificata:** in valore assoluto il salto è **minore**, e gli stati sono
**quasi identici**. **Non è «il tempo proprio è rumore».**

*(E non è rumore numerico: `4e-04` è dodici ordini sopra la precisione di `angle` su numeri di
modulo ~1. La fluttuazione è reale — è la sua **interpretazione** che cambia.)*

**`Z36` resta aperta, ma la domanda si affina:** non *«la fase è confrontabile?»* — **lo è, l'overlap
è 1** — ma **«un avanzamento di fase di `4e-04` per passo, che fluttua del 65 %, è l'orologio che
vogliamo?»** *(E si ricollega a `Z9`: con un avanzamento così piccolo, la maturazione è lenta **per
costruzione**.)*

---

## 6. VERDETTO CONTRO LE QUATTRO LETTURE FISSATE PRIMA

| lettura | esito |
|---|---|
| salto scende **e** livello resta → si cabla | **NO** |
| **salto scende ma livello crolla** → non si cabla, `L1` sarebbe un falso PASS | **quasi**: il livello crolla, ma il salto **non scende** |
| domina la componente che si annulla → diagnosi diversa | **NO — esclusa dalla misura** |
| **salto NON scende → la cucitura non è il meccanismo: reperto, e si ferma** | **✓ È QUESTA**, aggravata dal crollo del livello |

> **NON SI CABLA.** E il motivo non è una preferenza: **è dimostrato dalla struttura dell'oggetto**
> (una componente al 99.99 %), non solo misurato su un seme.

**E `L1` da solo sarebbe stato un falso PASS se il salto fosse sceso** — **il sigillo del mandato
guardava un numero solo.** **La coppia salto+livello era necessaria**, ed è nel task history.

## 7. COSA NON HO FATTO, E PERCHÉ

**Non ho cablato nulla** (§6 del mandato: *«NON cablare prima del §2»*), **non ho toccato
`psi_spin`, la definizione di `f`, il gauge.** **`Z9` non è stata rimisurata**: il §5 del mandato la
prevede *dopo* la cura, e la cura non c'è.

## 8. I LIMITI

Un seme, 120 passi, una scena. **La dominanza della componente 0 al 99.99 % potrebbe essere di
questa configurazione** *(`_psi_spinor` nasce da `exp(i·φ)` sull'asse 0 — vedi il fallback a
`:2657`)*: **in un sistema dove lo spinore ruotasse davvero fra le componenti, il candidato del
mandato tornerebbe in gioco.** **È una condizione da ricontrollare, non un fatto universale.**
