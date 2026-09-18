# REFERTO — **Il §1 è chiuso: il gauge è NELLA MATERIA, la mia obiezione è REFUTATA, e `cs` è VIVO**

**Data:** 2026-09-18 · **Blob** `f8f46683` · un seme (5), 120 passi, ramo **4pi** su 124/126 invocazioni
**Task history con l'obiezione, scritto e pushato PRIMA:** `0e571b4` · **Sonda:** `dd48ec0`
**Strumento:** `csv/_test_fork/_gauge_vuoto.py` (`sha1-BYTE 72c4c39e`) · **NESSUNA CURA CABLATA**

---

## 0. IL VERDETTO CONTRO LE CINQUE LETTURE FISSATE PRIMA

| lettura fissata prima (task history `0e571b4`) | esito |
|---|---|
| `cs/CS_M` mediano **~ 1** → cura cosmetica, ci si ferma | **NO** — vale **0.8265** |
| `cs/CS_M` mediano **<< 1** → il gauge è nella materia, l'allineamento vale | **✓ SÌ**, ma **meno di quanto la parola «<<» suggerisce**: è `0.83`, non `0.1` |
| `cs_std/cs` trascurabile → la via cade | **NO — è `17.6 %`**, e **è il dato più grosso del giro** |
| ⚠ `median(I)/mean(I)` stabile ~1 → il gauge proposto è ancorato a sé | **NO — LA MIA OBIEZIONE È REFUTATA.** Varia `0.145 → 0.653 → 0.462` |
| ⚠ `f·d/CS_M` fuori da O(1) di **> 3 ordini** → non cablabile | **NON SCATTA: è 1.7 ordini.** **Ma un altro numero, che non avevo fissato, dice qualcosa di forte** |

> **ESITO: via libera al §2 sulle prime tre letture. Ma il quinto punto va deciso da Luca, non da me,
> perché il criterio che avevo scritto NON scatta e quello che conta l'ho trovato dopo.**

---

## 1. (A) `cs` È VIVO — **e questo ROVESCIA un fatto stabile di CLAUDE.md**

```
cs/CS_M (13320 nodi-istanza, ultimi 30 passi)
   min 0.28336   p05 0.528252   MEDIANA 0.8265   p95 0.992235   max 0.999835
   frazione > 0.99 : 0.0632     > 0.9 : 0.2786     < 0.5 : 0.0369
   cs_std/cs per passo : MEDIANA 0.176142   min 0.165775   max 0.194487
```

**`cs_std/cs = 17.6 %`.** CLAUDE.md par.9 dice, come **fatto stabile**:

> *«`cs_std/cs` fra **0.0086 %** e **0.24 %**, sempre sotto l'1 % … `tau = d/cs` **E'** `tau ∝ d` …
> il braccio ON **non testa il tempo-luce**»*

**Quel fatto è SUPERATO, di un fattore ~2000 rispetto allo 0.0086 % e di ~73 rispetto allo 0.24 %,
ed è SOPRA la soglia dell'1 % di diciassette volte.**

**E si sa PERCHÉ, dal codice e non da una congettura:** la cura di `cs_floor` del 2026-09-16
(categoria D) ha sostituito la scala **assoluta** `1/GAMMA² = 400` con la scala **relazionale**
`_Lam = mean(I)`:

```python
_Lam   = float(np.mean(_I))                                  # :2914
_scala = max(_Lam, 1e-30) / (GAMMA_TURBO*GAMMA_TURBO)
cs_floor = CS_M / (1.0 + np.sqrt(_I) * np.sqrt(1.0/_scala))  # :2921
```

Con la vecchia scala, `I ~ 1e-7` contro `400` dava `sqrt(I/400) ~ 1e-5`: **`cs` era inchiodato a
`CS_M`.** Con `mean(I)`, il rapporto `I/mean(I)` è **O(1) per costruzione**, a **qualunque densità**.

> **`cs` non è diventato vivo perché il sistema è maturato: è diventato vivo perché la scala è
> diventata relazionale.** **Era una correzione di difetto senza flag, e ha riaperto un fronte che
> il registro dava per chiuso «alle densità simulabili».**

**⚠ E COSA QUESTO NON DICE:** non dice che `tau = d/cs` sia **fisicamente distinguibile** da
`tau ∝ d` nei run veri — quello richiede il confronto, non la dispersione. Dice che **la premessa
che lo escludeva è caduta**: la soglia dell'1 % era il criterio scritto, e **oggi è superata**.

## 2. (B) IL GAUGE ATTUALE STA **NELLA MATERIA** — ma non «più degli altri»

```
                            min        p05       MEDIANA     p95       max
cs/CS_M dei nodi x~1     0.310686   0.52674    0.801208   0.976818   0.999361   (n = 866)
cs/CS_M di TUTTI         0.28336    0.528252   0.826500   0.992235   0.999835   (n = 13320)
rho/peq dei nodi x~1     0.00341    0.277966   1.272030   2.81652    7.03346
rho/peq di TUTTI         3.14e-05   0.212592   1.354120   3.29607    14.4576
```

**Il nodo mediano di `f` ha `cs/CS_M = 0.80`: il gauge attuale è ancorato a un punto dove
l'orologio metrico va al `80 %` del vuoto**, cioè **`(cs/CS_M)² = 0.64`** nel fattore di `STEP2`.
**I due riferimenti NON coincidono: differiscono di un fattore `0.64` nel fattore d'orologio.**
**La prima lettura (cura cosmetica) NON scatta.**

**⚠ MA VA DETTO ANCHE IL CONTRARIO, perché è nella stessa tabella:** i nodi a `x ~ 1` **non si
distinguono dalla popolazione** — `0.801` contro `0.8265`, `1.272` contro `1.354`. **Il nodo mediano
di `f` è semplicemente un nodo tipico.** Quindi la frase *«se il mediano sta nella materia la
dilatazione è schiacciata»* va letta così: **non è che il gauge sia finito in un posto strano; è che
TUTTA la popolazione sta nella materia**, e il gauge ci sta dentro con lei.

## 3. (C) ⚠ **LA MIA OBIEZIONE È REFUTATA DALLA MISURA**

Avevo scritto, prima di guardare, che `cs/CS_M` **non è ancorato al vuoto ma a `mean(I)`**, e che
quindi ha *«un punto fisso della famiglia C12»* che renderebbe la cura uno spostamento di problema.

```
passo      mean(I)        median(I)      median/mean    frac I>mean
primo      0              0              0              0
1/4        1.22494e-07    1.77809e-08    0.145157       0.264108
meta'      2.09719e-06    1.37017e-06    0.653338       0.343115
ultimo     2.49265e-05    1.15266e-05    0.462422       0.310811

cs/CS_M MEDIANO nel tempo: primo 1   1/4 0.871125   meta' 0.822722   ultimo 0.841146
```

> **`median(I)/mean(I)` varia di un fattore 4.5 fra istanti. Il nodo TIPICO non è inchiodato.**

**Dove avevo ragione:** la scala **è** `mean(I)`, una statistica sulla propria popolazione — è nel
codice, e resta vero. **Dove avevo torto, e la differenza è tutta:** `median(|f|)` inchioda
`median(x) = 1` **ESATTAMENTE, per identità, sempre**; `mean(I)` inchioda solo
`mean(I/mean I) = 1`, e **su una distribuzione asimmetrica la MEDIA non è il nodo tipico**.
**È la stessa asimmetria che nel 2026-09-17 fece cadere il punto fisso di `_tau`** — lì per un
filtro di sottopopolazione, qui per la skewness — **e il segno è di nuovo a favore della legge.**

> **I due ancoraggi NON sono della stessa specie, e questo è un argomento A FAVORE del mandato che
> avevo scritto per metterlo in dubbio.** **Il gauge proposto è genuinamente meno auto-referenziale
> di quello attuale.**

## 4. (D) ⚠ **IL PUNTO CHE NON SO DECIDERE DA SOLO**

```
                          min         p05        MEDIANA     p95        max
f*d/CS_M  (candidato)  1.34566e-06  0.00131405  0.0188326  0.449795   3.42613
f*d/cs    (tempo-luce) 1.63875e-06  0.00167696  0.0244282  0.471975   3.51089
f/median|f| (ATTUALE)  9.04427e-05  0.0785782   1.000000   12.2263    190.493

                 x < 1e-3     x > 1e3    in [0.1, 10]
f*d/CS_M          0.0394       0.0000       0.1510
f*d/cs            0.0286       0.0000       0.1786
f/median|f|       0.0005       0.0000       0.8712
```

**IL CRITERIO CHE AVEVO FISSATO NON SCATTA:** avevo scritto *«fuori da O(1) di più di tre ordini →
non cablabile»*. **È 1.7 ordini** (mediana `0.0188`). **Non lo sposto a posteriori: NON SCATTA.**

**Ma il numero che conta l'ho trovato dopo, e non l'avevo fissato: la frazione nella banda utile
passa da `87.1 %` a `15.1 %`.**

**E la conseguenza è ARITMETICA, non una predizione di run** — la mappa `r_norm(x) =
(x/√(1+x²)+1e-6)/(1/√2+1e-6)` applicata alla distribuzione **misurata**, nello stesso istante:

| | `x` | `r_normalized` |
|---|---|---|
| mediana **attuale** | `1` | **`1.000`** *(per identità)* |
| mediana **col candidato** | `0.0188` | **`0.027`** |
| massimo misurato col candidato | `3.43` | **`1.358`** *(contro il tetto `√2 = 1.414`)* |
| minimo misurato col candidato | `1.35e-06` | **`3.3e-06`** *(contro il pavimento `1.414e-06`)* |

> **Il TETTO non si apre (`1.358` contro `1.414`) e il PAVIMENTO non si abbassa: è la POPOLAZIONE
> che scivola in fondo.** Poiché nessun nodo supera `x = 10`, la frazione con `x < 0.1` è
> **`1 − 0.151 = 84.9 %`**, e `x = 0.1 → r_norm = 0.141`:
> **l'`84.9 %` dei nodi finirebbe nel DECIMO INFERIORE dell'intervallo di dilatazione**, contro
> **≤ `12.9 %`** oggi.

**⚠ E QUI SERVE LA DECISIONE DI LUCA, perché ci sono DUE letture legittime e la misura non le separa:**

1. **È UN DIFETTO:** il ginocchio del bottleneck sta a `x = 1`; con il tipico a `0.019` il
   bottleneck lavora nel suo tratto **lineare** e non discrimina più — **`r` diventa quasi
   proporzionale a `f`**, e la saturazione, che è la ragione per cui la forma esiste, **non morde
   per nessuno.**
2. **È LA FISICA:** *«il nodo tipico ha un orologio 53 volte più lento del vuoto»* **è esattamente
   ciò che una dilatazione gravitazionale deve dire**, e con `median(|f|)` quel fatto era
   **invisibile per costruzione**, perché il tipico valeva 1 per decreto.

> **NON È UN «ALLINEAMENTO DI GAUGE»: È UN CAMBIO DI SIGNIFICATO DI `r`** — da *«ritmo relativo al
> nodo tipico»* a *«ritmo relativo al vuoto»*. **La prima lettura la chiama degenerazione, la
> seconda la chiama misura. Io non ho un criterio, scritto prima, che le separi — e non me lo
> invento adesso.**

## 5. E IL §2 DEL MANDATO — **cosa la misura dice già sui due candidati**

*(Non è un cablaggio: è il dato che ho in mano, e serve alla decisione.)*

| | `cs_nodo/d_nodo` | **`CS_M/d_nodo`** |
|---|---|---|
| mediana di `x` | `0.0244` | `0.0188` |
| banda `[0.1,10]` | `17.9 %` | `15.1 %` |
| statistica di popolazione al suo interno | **SÌ** — `cs` contiene `mean(I)` (§3) | **NO — nessuna** |
| riferimento | **locale in entrambi i fattori** | **vuoto** (numeratore) + **scala locale** |

**I due sono numericamente quasi indistinguibili (fattore 1.3): la scelta è di PRINCIPIO, non di
effetto.** **E il principio dice `CS_M/d_nodo`:** è l'unico dei due che **non contiene nessuna
statistica sulla propria popolazione**, ed è **la stessa ancora già certificata in sezione A**
(`omega_clk *= (cs/CS_M)²`). `d_nodo` è già calcolato da `_tempo_luce_nodo` (`:3036-3044`).
**Zero coefficienti nuovi.**

**⚠ UNA RISERVA DICHIARATA E NON MISURATA:** `d_nodo` **cade su `LAM`** per i nodi isolati
(`d_nodo[grado <= 0] = LAM`, `:3041`) e nel fallback senza archi (`:3043`). **Il mandato vieta
`LAM`, e per quella via rientrerebbe.** **Non ho contato quanti nodi passano di lì** — è un ramo
`else` su un percorso fisico, quindi per P5 **va contato prima di cablare**, non dopo.

---

## 6. COSA NON HO FATTO, E PERCHÉ

**Nessuna cura cablata** (§4 del mandato: *«NON cablare prima del §1»*). Non ho toccato
`median(|f|)`, il `+1e-6`, la forma `x/√(1+x²)`, `psi_spin`, il gauge. **Non ho usato `LAM`.**
**Non ho corretto `TAU_A`/`TAU_DIFF`/`PHI_CRIT`/`TAU_BG`:** M8 dice di riportarli, e si riportano
**dopo** una cura che non c'è.

## 7. I LIMITI

Un seme, 120 passi, una scena. **`cs_std/cs = 17.6 %` è di QUESTA scena e di QUESTA maturazione** —
e il precedente del 2026-09-15 insegna proprio che quel rapporto **cresce col tempo**, quindi va
dichiarato con l'istante. Il fallback `cs = CS_M` è scattato **2 volte su 248** chiamate (`0.8 %`):
la cache è viva. `rho/peq` usa la proiezione arco→nodo di `peq`, **la stessa forma già usata a
`:2295-2297`**, dichiarata e non nuova.
