# REFERTO — **IL `+3.0` ERA UN SEME. A quattro semi l'effetto NON C'È**

**Data:** 2026-09-18 · **Branch:** `fork-su2` · **Blob** `11cf103f` (byte grezzi, post-cura)
**Strumento:** `csv/_test_fork/_semi_spin_feedback.py` (`a18cd12d`, committato **prima** del run,
commit `4d4db99`) · **Output:** `csv/_test_fork/_semi_spin_feedback.txt`
**Il criterio era scritto PRIMA e non è stato prorogato.**

---

## 0. P6 — le condizioni lette **dai dati**, prima di guardare i numeri

| seme | braccio | `TAU_A` | `SPIN_FEEDBACK` | seed | rc |
|---|---|---|---|---|---|
| 5 | OFF / ON | **2.0 / 2.0** | **False / True** | 5 | 0 / 0 |
| 11 | OFF / ON | **2.0 / 2.0** | **False / True** | 11 | 0 / 0 |
| 17 | OFF / ON | **2.0 / 2.0** | **False / True** | 17 | 0 / 0 |
| 23 | OFF / ON | **2.0 / 2.0** | **False / True** | 23 | 0 / 0 |

**Otto run su otto conformi, letti dal blocco `# RUN_PARAMS` di ciascun CSV.** Quattro semi con
**entrambi** i bracci validi: il disegno appaiato ha i 3 gradi di libertà che servono.

---

## 1. IL RISULTATO — **il segno non è nemmeno concorde**

| seme | n OFF | n ON | **δn** | `max\|d0\|` OFF → ON | `max\|psi\|` OFF → ON |
|---|---|---|---|---|---|
| 5 | 1754 | 1785 | **+31** | 50.22 → 42.73 | 5.834 → 5.328 |
| 11 | 1947 | 1947 | **0** | 41.51 → **201.71** | 6.363 → 9.354 |
| 17 | 1810 | 1813 | **+3** | 111.39 → **32.16** | 7.194 → 5.757 |
| 23 | 1949 | 1890 | **−59** | 99.63 → 84.37 | 6.297 → 8.797 |

**`+31 / 0 / +3 / −59`.** È la firma già catalogata (C10): su un solo seme un effetto apparente,
su quattro **il segno cambia**.

### Il criterio, applicato come scritto

```
δ CONTEGGIO NODI :  media  −6.25    SD FRA SEMI  37.84    IC95 ±60.2   -> CONTIENE LO ZERO
δ max|d0|        :  media +14.55    SD FRA SEMI 102.3     IC95 ±162.7  -> CONTIENE LO ZERO
δ max|psi|       :  media +0.887    SD FRA SEMI  2.188    IC95 ±3.482  -> CONTIENE LO ZERO
```

**Recupero medio: `−0.34 %` del braccio OFF.** Non solo non recupera: la media è **negativa**.

---

## 2. COME SI SCRIVONO I TRE NULLI — **e non si scrivono allo stesso modo**

Il presidio è esplicito: *«un risultato nullo si legge solo insieme alla risoluzione che lo ha
prodotto»*, e *«se il limite superiore è più grande della grandezza stessa, si scrive **non
misurato**, non nessun effetto»*.

| grandezza | IC95 | scala | risoluzione | **come si scrive** |
|---|---|---|---|---|
| **δ nodi** | ±60.2 | 1865 nodi (media OFF) | **3.2 %** | **«il feedback non sposta il conteggio nodi di più di ~66 nodi, cioè il 3.6 %».** Il nullo **dice qualcosa.** |
| **δ `max\|d0\|`** | ±162.7 | media δ = 14.55 | **la barra è 11× il valore** | **«NON MISURATO».** Non «nessun effetto». |
| **δ `max\|psi\|`** | ±3.482 | media δ = 0.887 | **la barra è 3.9× il valore** | **«NON MISURATO».** |

**Tre righe che dicono «contiene lo zero» e significano due cose diverse.**

---

## 3. COSA CADE, PRECISAMENTE

**Cade il `+3.0 punti` del referto precedente.** Era `1754 → 1833` su **un seme**, cioè **+79 nodi**.
La misura a quattro semi della stessa quantità dà **−6.25 ± 60.2**: il **+79 sta fuori dall'IC95**.

**E cade anche il «costo» di `+21 punti` su `d0`.** Era anch'esso un seme. Qui `d0` fa
`−7.5 / +160.2 / −79.2 / −15.3`: **due semi migliorano, uno peggiora di 4.9 volte, uno migliora
molto.** La dispersione è tale che **non si può dire niente** — il che, si noti, **toglie anche
l'argomento contrario**: non ho una prova che il feedback peggiori `d0`.

> **Il mio verdetto precedente — *«ha spostato il problema»* — era costruito su DUE numeri di un
> seme solo, e nessuno dei due sopravvive. La formulazione giusta è più povera e più onesta:
> a quattro semi, SPIN_FEEDBACK non produce un effetto misurabile su nessuna delle tre grandezze.**

---

## 4. ⭐ UN CONTROLLO GRATIS CHE NON AVEVO PROGRAMMATO

**Il braccio OFF del seme 5 dà `1754` nodi — esattamente come nell'esperimento PRE-CURA**
(`csv/_test_fork/_esperimento_spin_feedback.txt`, commit `1347246`: *«TAU_A=2.0, feedback OFF :
1754 nodi»*).

**La cura del denominatore è inerte a flag spento su un run batch VERO di 120 passi**, non solo
nello stub del sigillo. È il rito §2.1 (*«flag OFF = byte-identico»*) confermato **sul campo**.

**Onestà su cosa questo prova:** un conteggio nodi identico dopo 120 passi su un sistema caotico è
una condizione **necessaria e molto stringente** — basta una differenza a `1e-16` per farlo
divergere — **ma non è una dimostrazione di byte-identità**. È una conferma forte, non una prova.

---

## 5. LA LETTURA PRE-REGISTRATA CHE SI APPLICA

Il mandato del `2026-09-17` fissava quattro letture. Quella che si applica è la seconda:

> *«la perdita resta uguale → **l'ipotesi cade.** Candidato successivo: **`TAU_A` è anche la VITA
> MEDIA** (`:2265`), e a `2.0` la memoria di spin muore 25 volte più in fretta. Sarebbe **`Z10`: un
> numero per due leggi, una crescita e un decadimento.»*

**L'ipotesi «il `−32 %` dipendeva dalla trasmissione staccata» CADE.** Il `−32 %` non è colpa del
feedback mancante, perché riattaccarlo — e riattaccarlo **riparato** — non lo recupera.

**Il fronte si sposta su `Z10`**, che era già aperto e ora è il candidato principale.

---

## 6. COSA RESTA VERO DI QUESTO GIRO

**Il valore di questo giro non è nel risultato dell'A/B: è nella BONIFICA.**

1. **Il denominatore era un errore ed è corretto** — `|sum(out)|/max|out|` da **1.112** a
   **6.5e-16**. Il termine **non inietta più coppia netta**. Vale **a prescindere** dall'A/B:
   un cricchetto è un difetto anche se il termine non produce effetti misurabili.
2. **`G6`: la fase è cucita** — cambi di segno **0.35 %** contro un nullo di **50 %**. Prima volta
   che qualcuno lo verifica, e dice che il termine è una **corrente orientata vera**.
3. **E adesso `SPIN_FEEDBACK` ha un sigillo** (12/12), che prima non aveva. Serve a
   **diagnosticare**, non a decidere se tenerlo.

**`SPIN_FEEDBACK` resta OFF di default.** L'A/B non dà nessuna ragione per cambiarlo, e la cura è
una **correzione di difetto** (categoria D), non una promozione.

---

## 7. IL LIMITE, dichiarato

- **Quattro semi sono il minimo**, non l'abbondanza: `t(0.025,3) = 3.182` contro `t(∞) = 1.96`.
  Con 8 semi la barra si stringerebbe di ~1.6 volte, e la risoluzione su δn passerebbe da 3.2 % a
  ~2 %. **Un effetto vero ma piccolo (≤ 1 %) resterebbe invisibile a questo disegno.**
- **120 passi** sono ~1/50 della maturazione di `ramp` (§9.32): il sistema è nel transitorio.
- **Una sola scena** (3 masse, `sep 8`).
