# TASK HISTORY — `chi_basc` a OFF. E tre premesse del mandato non reggono alla verifica

**Data** 2026-09-20 · **branch** `fork-su2` · **HEAD** `16fa8d9` · **blob** `27f1ab03`
*(sha1 byte grezzi; git `3437e260`)* · albero **pulito** · **nessun run.**

> **Nessun run lungo finché questo non è chiuso. Una modifica, un sigillo.**
> **⚠ E la prima cosa che ho fatto è applicare la REGOLA NUOVA del §4 al mandato stesso** — *ogni
> affermazione presa da un commento o da una documentazione va verificata contro lo stato attuale
> prima di essere usata come premessa.* **Tre non hanno retto.**

---

## 1. ⚠ `§0①` — **L'ANELLO C'È, MA NON È ISTANTANEO. E non passa dalla riga citata**

### (a) La riga `:3612` NON GIRA
```python
:3607   elif VERSO_CHI and len(self.perc_chi) >= self.n:
:3612       twn = (np.pi * 0.5 * (self.perc_chi[i] - self.perc_chi[j])) / PHI_CRIT
```
**`VERSO_CHI = False`** *(`:671`)*, e nel run non è acceso. **Quel ramo è morto.**

### (b) L'anello si chiude ALTROVE, e la catena è questa
```
:1530  chiralita_core_locale()   ->  chi = self.perc_chi[...]          LEGGE perc_chi
:3604  if CHI_CORE ...           ->  twn = f(chi_core)                 CHI_CORE = 1 nel run
:3736  chi_torsione = self._chi_core_nodi if CHI_CORE ...              LEGGE perc_chi
:3745  twist_dip = f(chi_torsione)
:3750  self.tw += self._w8(dph + twist_dip - self.twp) - ...           tw <- perc_chi
:3765  perc_chi[:n] = where(twn(_tw_t) > PHI_CRIT, 1, -1)              perc_chi <- tw
```

### (c) ⚠ MA NON È ISTANTANEO, e la ragione è un dettaglio che va misurato non dedotto
```python
:3408   _tw_t = self.tw.copy()          <- SNAPSHOT a INIZIO passo
:3750   self.tw += ...                  <- tw aggiornato QUI
:3759   _tw_src = _tw_t                 <- chi_basc usa lo SNAPSHOT, non il tw appena scritto
```

> **`perc_chi(t+1) = F(tw(t))` e `tw(t+1) = G(tw(t), perc_chi(t))`: entrambe le gambe leggono il
> valore di INIZIO passo dell'altra.**
> **È una mappa accoppiata con UN PASSO DI RITARDO SU OGNI GAMBA, non una funzione istantanea di sé
> stessa.** **`A6` nella sua lettera NON è violato.**
> **Ma è un ANELLO CHIUSO di periodo 2, e `perc_chi` è una VARIABILE SCHIAVA di `tw`.** **Va
> dichiarato, ed è quello che il mandato chiedeva di fare invece di dedurre.**

## 2. ⚠ `§2` — **IL DEFAULT È GIÀ `False`. La modifica NON è nel simulatore**

```
:746   CHI_BASC = False                              <- il default di MODULO, gia' OFF
:6397  p.add_argument("--chi-basc", store_true)      <- chi lo accende
csv/_test_fork/_scena_video.py:109   "--chi-basc"    <- IL DRIVER LO PASSA
prog.csv del run:  CHI_BASC=1
```

> **Il simulatore non va toccato: la modifica è nel DRIVER.**
> **E il driver lo sapeva già:** a `:133` stampa *«`--chi-basc` RISCRIVE `perc_chi` a ogni passo:
> non è un'etichetta di lignaggio»*. **L'avviso c'era; la conseguenza non era stata tratta.**

**LA FORMA DELLA MODIFICA, nell'idioma che il driver già usa:** **`--chi-basc=on|off` NOMINALE,
default `off`**. **Con `on` il driver fa ESATTAMENTE quello che faceva** — ed è il sigillo `Z1`.

## 3. ⚠ `§4` — **I NUMERI CHE IL MANDATO PORTA COME PROVA NON REGGONO**

**Il mandato dice:** *«`|tw|` mediana `7.9`, `p75 = 12.61`, contro `4π = 12.566`. A `4π` un quarto
dei nodi supererebbe la soglia. NON zero.»*

**MISURATO sui 45 snapshot di `_g6000`** *(blob `7c4dec1d`, `CHI_BASC = 1`)*:

```
passo   |tw| p25   p50     p75     p95     sopra 2pi   sopra 4pi
60       0.223    0.648   1.095   4.484      0.3 %       0.1 %
600      0.972    2.245   4.025   6.425      5.7 %       0.0 %
1800     1.142    2.377   3.905   6.607      6.2 %       0.1 %
2700     1.073    2.247   3.778   6.741      6.6 %       0.2 %
```

> **Mediana `2.25`, non `7.9`. `p75` `3.78`, non `12.61`. E sopra `4π`: `0.2 %`, non «un quarto».**
> **La premessa è falsificata di circa DUE ORDINI.**
> **⚠ E l'ironia va registrata, non nascosta: sono i numeri offerti A SOSTEGNO della regola nuova,
> e la regola nuova li falsifica.** **Questo NON indebolisce la regola: la conferma.**

**Non so da dove vengano quei numeri** *(altra configurazione? `perc_tw`? un'altra grandezza?)*.
**Non li cito, e la voce su `PHI_CRIT` porterà i MIEI numeri misurati.**

## 4. LA MODIFICA, e cosa NON si tocca
- **driver: `--chi-basc=on|off`, default `off`;**
- **`perc_chi` resta scritta SOLO alla nascita:** `:4294` *(mitosi, eredita uguale)* e `:4415`
  *(antinodo Schwinger, eredita opposta)* — **righe VERE, quelle del mandato sono slittate;**
- **NON si toccano** `cs`, `I`, `tau`, `PHI_CRIT`, `:602`, `:1849`, `:2690`, `:3612`, `:6154`;
- **NON si separa in due array** *(valutato e scartato: `maturita` resterebbe senza lettori, `A8`)*;
- **`:4294` NON si cura:** va **registrata** come voce aperta *(l'eredità UGUALE rompe la
  conservazione che le sole coppie di Schwinger darebbero)*.

## 5. L'A/B — le letture fissate PRIMA
```
ramo A: --chi-basc=on    (come i run finora)     ramo B: --chi-basc=off   (la decisione)
```
| # | esito | conclusione |
|---|---|---|
| **α** | in `B` **`N(+1)−N(−1)` si muove solo per nascite**, e l'olonomia netta / `L` **sopravvive** | **`chi_basc` non serviva più: il settore spinoriale ha assorbito il suo scopo** |
| **β** | in `B` **l'olonomia netta si azzera e la precessione sparisce** | **`chi_basc` serviva davvero: lo dico, e la decisione torna a Luca** |
| **γ** | `L` cambia **di poco** | **si riporta il numero, non si sceglie fra α e β** |
| **δ** | in `B` `N(−1)` **identicamente zero** | **reperto**: la carica nasce tutta dello stesso segno |

**Si confrontano anche:** `omega_s`, `tw`, `coer_l`, `_deg` agli stessi percentili, e **i NATI PER
RAMO** *(`:4294` contro `:4415`)* **con contatori distinti (`A8`)**.

## 6. I SIGILLI
**`Z0`** riferimento `27f1ab03` byte grezzi · **`Z1`** con `--chi-basc=on` **BYTE-IDENTICO
[BLOCCANTE]** · **`Z2`** con `off` **DEVE** differire · **`Z3`** `perc_chi` non è più riscritta
*(confronto prima/dopo su più passi)* · **`Z4`** l'anello è rotto **dal codice, non dai numeri** ·
**`Z5`** stabilità + rigiro dei sigilli del giro.

## 7. COSA MI FA FERMARE
- **`Z1` non byte-identico** → **STOP**;
- **lettura `β`** → **si riporta e la decisione torna a Luca**, non si procede;
- **`N(−1)` a zero** → è un reperto, si riporta.
