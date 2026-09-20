# REFERTO — **la fuga di `|vd|` in B: gli archi non COLLASSANO, si STIRANO di `38` volte**

> Criteri **fissati PRIMA** in `doc/TASK_HISTORY/2026-09-20_fuga-vd-ramoB.md` (`012549f`), strumento
> committato prima di girarlo (`csv/_test_fork/_fuga_vd.py`, `2035429e`, `ed66e8c`).
> **Dagli snapshot gia' scritti, a run VIVI, senza fermarli.** Output: `csv/_test_fork/_fuga_vd.txt`.
> **12 snapshot in A, 3 in B. UN SEME PER RAMO.**

---

## 1. LA SERIE NEL TEMPO — **§2① , la misura che decide**

### Ramo A — nessuna deriva, per 1440 passi
```
passo    n       |vd|.p50   |vd|.p99   |vd|.MAX    n3    r_k
120     2672      0.5394     1.334      3.354       1     --
600     2856      0.2130     0.7863     3.767       1    1.19
1080    3963      0.1265     0.6169     3.091       1    1.15
1440    5906      0.1438     0.7819     2.661       1    0.87
```
**`r_k` oscilla fra `0.79` e `1.19` senza tendenza. `n3 = 1` SEMPRE.**
**E `#{|vd| > 10}` vale `0` a TUTTI E DODICI gli istanti.**

### Ramo B — la coda cresce in POPOLAZIONE, non solo in altezza
```
passo    n       |vd|.p50   |vd|.p99   |vd|.MAX    n3     r_k
120     2998      0.1921     1.176      2.923       1      --
240     3130      0.1712     0.8226    79.15        9    27.08
360     3229      0.1011     0.4926   531.6        52     6.72
```
**⚠ E IL NUMERO PIU' IMPORTANTE NON E' IL MASSIMO: sono i CONTEGGI.**
```
#{|vd| >     1      3     10     30    100}
passo 120  17279     0      0      0      0
passo 240   2897    93     52     27      0
passo 360    586   347    231    135     61
```
> **Il grosso GELA** — `#{|vd| > 1}` crolla `17279 -> 586` — **mentre la coda si POPOLA**:
> `#{|vd| > 10}` va `0 -> 52 -> 231`.
> **Non e' UN arco scappato: e' una popolazione che cresce.**

**Contro il criterio fissato prima** *(`r_k < 1.5` stabilizza, `r_k > 3` si moltiplica)*:
**`r_k = 6.72` all'ultimo intervallo -> «CONTINUA A MOLTIPLICARSI».**
**⚠ Ma `r_k` sta DECELERANDO (`27.08 -> 6.72`), e sono DUE rapporti: da soli non chiudono.**

---

## 2. ⚠ IL DISCRIMINANTE VERO — **§2③, e NON era fra le tre letture del mandato**

I 100 archi piu' veloci, all'ultimo snapshot di ciascun ramo:

| | **ramo B** (passo 360) | **ramo A** (passo 1440) |
|---|---|---|
| `\|vd\|` p50 | **114.1** | 1.803 |
| **`d` p50** | **30.12** *(mediana di TUTTI: `1.024`)* | 2.764 *(tutti: `2.63`)* |
| **`d0` p50** | **0.855** *(tutti: `0.899` — NORMALE)* | 1.772 *(tutti: `0.944`)* |
| **`d/d0` p50** | **38.52** · min `7.24` · **max `388.3`** | **1.536** · min `0.65` · max `38.8` |
| nodi distinti su 100 archi | **61** — regione LOCALIZZATA | 168 — sparsi |
| `perc_chi` dei nodi | `+1 22 / -1 39` *(sistema: `1633/1596`)* | `+1 8 / -1 160` *(sistema: `671/5235`)* |

### 2.1 La lettura ① del mandato — **il COLLASSO — e' ESCLUSA, e da un segno**

Il mandato proponeva:
> *«Pochi archi che accelerano mentre il resto rallenta e' quello che fa un COLLASSO: la materia si
> concentra, e li' le velocita' salgono.»*

**Un collasso COMPRIME: `d/d0 < 1`.**
**Qui `d/d0 = 38.52`, con un massimo di `388.3`.**

> **Quegli archi non si stanno concentrando: si stanno STIRANDO di trentotto volte la propria
> lunghezza a riposo.** **`d0` e' NORMALE** (`0.855` contro la mediana `0.899` del sistema): **non e'
> la lunghezza a riposo ad essere cambiata — e' `d` ad essere schizzata da `~0.9` a `30`.**

**E il meccanismo si legge:** una molla con `d0 = 0.855` tesa a `d = 30` esercita un richiamo
`∝ (d - d0) ≈ 29`. **Quel richiamo accelera, l'arco supera, e il ciclo riparte piu' ampio.**
**E' un'oscillazione ad ampiezza CRESCENTE, cioe' la firma di un'instabilita' numerica della
molla**, non di una struttura che si forma.

### 2.2 E il `perc_chi` dice che NON e' un fenomeno chirale
In B i nodi veloci sono `22` contro `39`, il sistema e' `1633` contro `1596`: **le proporzioni sono
quelle della popolazione**. **Non c'e' selezione di segno.**

---

## 3. §2② L'IDENTITA' — **la misura NON DISCRIMINA, e lo si sa solo grazie al controllo su A**

```
                      Jaccard fra i primi 100 archi di snapshot consecutivi
ramo B    0.047   0.042
ramo A    0.136  0.047  0.143  0.070  0.117  0.163  0.093  0.075  0.099  0.070  0.058
NULLO (insiemi indipendenti, 100 su ~528k):  1.9e-04
```

**Entrambi i rami sono ~200 volte sopra il nullo** — quindi in entrambi c'e' una persistenza reale,
**e in entrambi il ricambio e' quasi totale.** **`J = 0.04` in B sta DENTRO l'intervallo di A
(`0.047`-`0.163`).**

> **⚠ QUINDI LA LETTURA «archi sempre diversi = CONTAGIO» NON SI PUO' TRARRE:** il ricambio di B e'
> **quello normale del sistema**, misurato su A.
> **Senza la controprova del §2④ avrei letto `J = 0.04` come «contagio», e sarebbe stato un errore.**

**Cio' che distingue B non e' CHI sono gli archi veloci: e' QUANTO sono veloci e QUANTI sono.**

---

## 4. IL VERDETTO, contro i criteri scritti prima — **e cosa resta aperto**

| lettura del mandato | esito |
|---|---|
| **① STRUTTURA / collasso** | **ESCLUSA** — un collasso comprime, qui `d/d0 = 38.5` |
| **② DIVERGENZA NUMERICA** | **SOSTENUTA** da tre fatti indipendenti: `r_k = 6.72 > 3`; la coda che si **popola** (`0 -> 52 -> 231` sopra `10`); e archi tesi a **`38x`** la lunghezza a riposo con `d0` normale |
| **③ `chi_basc` FACEVA DA FRENO** | **NON DECISA, e questo run non puo' deciderla** — un seme per ramo |

**⚠ E LA DECELERAZIONE NON E' IGNORATA:** `r_k` passa da `27.08` a `6.72`. **Se il terzo rapporto
scendesse sotto `1.5`, la lettura ② andrebbe rivista.** **Il quarto snapshot di B (passo 480) NON
E' ANCORA STATO SCRITTO**, ed e' la misura che chiuderebbe il punto.

**⚠ E IL RILIEVO DEL MANDATO SU `A` RESTA IN PIEDI, e non l'ho risolto:** *«A e' stabile potrebbe
significare A e' MORTO»*. **`A` ha `671` nodi `+1` su `5906` (l'`11 %`)**, contro B che e'
`1633/1596`, **bilanciato**. **La stabilita' di A convive con una monocoltura chirale, e questo
referto NON dice quale delle due cose sia la causa dell'altra.**

---

## 5. ⚠ LO STATO DEL RAMO B MENTRE SCRIVO — **il costo e' RADDOPPIATO ancora**

```
ultima riga di progresso scritta: 17:36:49  (frame 60)
ora                             : 18:28:26
```
**`3097 s` senza scrivere**, e il progresso si scrive **ogni 5 frame**: all'ultimo ritmo misurato
(`274 s/frame`) cinque frame costerebbero `1370 s`.
> **Quindi il costo per frame e' ora `> 600 s`: e' piu' che raddoppiato dall'ultima misura.**
> **Il processo NON e' fermo** — due campioni di stack consecutivi danno `:3956` e `:3966`, dentro
> il ciclo dei sottopassi. **E' vivo, e sta pagando `nsub`.**

**Proiezione, dichiarata come tale:** ai `>600 s/frame` attuali i **440 frame** che restano
costerebbero **`> 73 ore`**, **e il ritmo sta peggiorando**: e' un **limite inferiore**.

---

**LIMITI:** un seme per ramo; **tre snapshot in B contro dodici in A**; `r_k` poggia su **due**
rapporti. **Nessuna differenza fra i bracci e' dichiarata significativa** — il nullo di un confronto
fra bracci e' la dispersione **FRA SEMI**, che questo esperimento non misura.
**E questo referto NON decide l'A/B di `chi_basc`:** diagnostica la fuga, come il mandato chiede.
