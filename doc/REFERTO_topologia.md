# REFERTO — **nessuna delle quattro letture. Il grafo è in QUATTRO PEZZI che non si toccano mai**

**Blob `775ceab7`** · seme 42 · i **45 snapshot** di `_g6000` (passi 60→2700) e i 10 di `_fin_A`
(passi 6→60) · strumenti `_topologia_neonati.py` (`fb296225`), `_topologia.py` (`a3bc6a22`),
`_topologia_blocchi.py` (`75a0b053`) · esiti `_topologia_neonati.txt`, `_topologia.txt`,
`_topologia_blocchi.txt` · letture fissate **PRIMA** in
`doc/TASK_HISTORY/2026-09-20_topologia.md` (`f6d54e9`).

> **NESSUN RUN, NESSUNA CURA, il simulatore non è stato toccato.** Il clustering è **esatto, non
> campionato**: costo misurato **0.75 s** per 9511 nodi e 438 532 archi.
> **NESSUN NOME, in nessun punto di questo documento.** Si riporta la forma, coi numeri.

---

## 0. I DUE PRESIDI, verificati su tutti e 45 gli snapshot

| presidio | esito |
|---|---|
| **P0** — il grado ricalcolato da `i`/`j` contro `_deg` salvato | **0 nodi diversi su 45 snapshot su 45.** Zero auto-anelli, zero archi duplicati |
| **P1** — **la stabilità degli indici, misurata e non assunta** | `n` non cala mai; **`eta[k]` non diminuisce mai**, su nessun indice, in nessuna delle 44 transizioni |

**P1 non era mai stato misurato**: era un'assunzione scritta in `CLAUDE.md` §9 (*«i nodi si
appendono in coda»*). Tutto il seguire-le-coorti poggia su quella, e ora è misurata.

---

## 1. ⚠ IL FATTO CENTRALE — **quattro componenti, sempre le stesse, che non si toccano MAI**

```
passo    n       componenti del GRAFO INTERO      dimensioni
6        2391    4                                900   497   497   497
60       2391    4                                900   497   497   497
600      3433    4                                1114  982   735   602
1800     5938    4                                1864  1647  1246  1181
2700     9511    4                                2899  2815  2119  1678
```

**Quattro dal primo istante al passo 2700. Non si fondono, non si spezzano.**

```
archi DIRETTI fra nodi di componenti diverse:  0        (dentro la stessa: 426 587)
catene che uniscono due componenti diverse:    0 su 5167   (0.0000)
```

> **Zero. Non «pochi»: ZERO**, a tutte e tre le soglie di grado provate (`>=11`, `>=41`, `>=101`) e
> a entrambi i passi. **Non c'è nessun collegamento, di nessun tipo, fra i quattro pezzi.**

## 2. I QUATTRO PEZZI NASCONO COSÌ, e il codice lo dice

```
_semina_n_masse():   npunt = int(massa_critica_collasso() * 0.8)  = 497,  per ciascuna delle 3
SEME_INIZIALE = 900  (:4532) -> il quarto pezzo
900 + 497*3 = 2391
```

**E al passo 6 la densità interna dei tre pezzi da 497 è `1.0000` ESATTA: sono grafi COMPLETI alla
semina.** Il pezzo da 900 sta a `0.1476`.

```
densita' interna   passo 6     passo 600      passo 2700
tre pezzi da 497   1.0000      0.9994/0.9966/0.9987   0.9938/0.9925/0.9915
pezzo da 900       0.1476      0.1475                 0.1472
```

> **Il picco di grado alto NON è una forma emersa: è la condizione iniziale.** La densità **cala
> lentissimamente** (da `1.0000` a `0.992` in 2700 passi), non cresce.

## 3. L'ISTOGRAMMA — bimodale, **con una valle VUOTA di 270 valori**

**Passo 2700** *(n = 9511)*:

```
grado          quanti   frazione
2              6328     0.6653
3               630     0.0662
4               121     0.0127
5                31     0.0033
6                 9     0.0009
7                 1     0.0001
[11, 41)          0     0.0000        <- VUOTO
[41, 81)         68     0.0071
[81, 161)       577     0.0607
[161, 321)      255     0.0268
[321, 641)     1491     0.1568
```

```
LA VALLE piu' larga senza NEMMENO UN NODO: gradi 226..495   (270 valori consecutivi)
e una seconda valle vuota: gradi 11..40                      (30 valori consecutivi)
```

> **Due picchi, e fra loro non c'è una valle poco popolata: c'è una valle VUOTA.** Su 9511 nodi,
> **nessuno** ha grado fra 226 e 495, e **nessuno** fra 11 e 40. **La lettura `B` (gradi continui)
> è falsificata con un margine che non lascia spazio.**

## 4. IL CLUSTERING — una dicotomia netta, non un gradiente

```
gruppo         quanti   C p25     C p50     C p75     C max     C == 0 %
grado 2        6328     0.0000    0.0000    0.0000    0.0000    100.0
grado 3-10      792     0.0000    0.0000    0.0000    0.0000    100.0
grado 11-100    265     0.6495    0.6815    0.7058    0.8060      0.0
grado > 100    2126     0.6255    0.9648    0.9796    0.9938      0.0
```

> **Non «basso» e «alto»: ESATTAMENTE ZERO sul 100 % dei 7120 nodi di grado ≤ 10, e MAI zero sui
> 2391 di grado ≥ 11.** Nessun nodo sta in mezzo.
> **Conseguenza diretta sui grado-2:** `C = 0` significa che **i loro due vicini non sono
> collegati fra loro**. Non chiudono nessun triangolo.

## 5. LE CATENE — **corte, e tutte INTERNE a un pezzo**

```
5167 catene (componenti indotte sui soli grado-2), 6328 nodi
lunghezza:  p25 1   p50 1   p75 1   max 11   media 1.225

lunghezza   quante   frazione
1           4374     0.8465
2            563     0.1090
3            147     0.0284
4             49     0.0095
5             21     0.0041
6              9     0.0017
7              3     0.0006
>= 9           1     0.0002
```

```
punti d'appoggio esterni per catena:   2 appoggi DISTINTI su 5167 catene su 5167  (1.0000)
                                       0 appoggi: 0     1 appoggio: 0
i due capi in DUE componenti DIVERSE:  0        (0.0000)
i due capi nella STESSA componente:    3690     (0.7141)
almeno un capo fuori da ogni blocco denso: 1477 (0.2859)
```

> **⚠ CORREZIONE A UNA MIA MISURA, e va detta perché il primo numero, letto da solo, inganna.**
> `_topologia.py` ha misurato che **il 100 % delle catene ha due punti d'appoggio DISTINTI**, e il
> numero è giusto. **Ma la domanda del mandato era un'altra:** *«i due estremi finiscono su nodi di
> grado alto DIVERSI o sullo STESSO?»* nel senso di **pezzi diversi**. **Due nodi distinti possono
> benissimo stare nello stesso pezzo**, ed è esattamente ciò che accade: `0.0000` fra pezzi
> diversi. **La misura al livello del nodo rispondeva a una domanda che non era stata fatta.**
> Ho scritto un secondo strumento (`_topologia_blocchi.py`) per prenderla al livello giusto.

**Nessuna scala caratteristica:** la lunghezza **decade monotona** da 0.85 a 0.0002, **senza
picco**. Non c'è un valore tipico diverso da 1.

**Catene per punto d'appoggio:** p25 `2` · p50 `3` · p75 `5` · max `28`. **Distribuita, non
costante.**

## 6. IL GRADO 2 È PERMANENTE — **la quarta lettura è falsificata**

*(Misurata per prima, come ordinato, perché avrebbe cambiato il significato di tutto il resto.)*

```
COORTE dei grado-2 al passo 600 (1025 nodi), seguita per 2100 passi:
passo    ancora grado 2     p25/p50/p75      max
600      100.0 %            2 / 2 / 2        2
1200      94.8 %            2 / 2 / 2        4
1800      89.9 %            2 / 2 / 2        5
2700      84.0 %            2 / 2 / 2        6

CONTROLLO (P2), i grado>=3 allo stesso t0:  p25/p50/p75 = 149 / 496 / 496  ->  149 / 496 / 498
```

**E il test trasversale, quello che non contiene il tempo** *(passo 2700)*:

```
fascia di eta    quanti   deg p50   grado 2 %
[0.0, 0.5)         642    2         99.8
[4.0, 8.0)        1312    2         93.7
[8.0, 16.0)       2964    496       54.5
[16.0, inf)       2689    4         36.5
```

> **Il 36.5 % dei nodi più vecchi è ancora di grado 2.** **Non è un transitorio demografico:** in
> 2100 passi la mediana della coorte **non si è mossa di un'unità**, e il massimo è passato da 2 a
> **6**. **La lettura `D` — quella che il mandato dava per più probabile — è falsificata.**

## 7. LE DUE POPOLAZIONI NON SI MESCOLANO MAI

```
nodi con grado > 100 al passo 2700:     2126, e TUTTI E 2126 erano presenti al passo 60  (1.0000)
nodi NATI dopo il passo 60:             7120, di cui con grado > 100:  0                 (0.0000)
nodi presenti al passo 60:              2391, di cui con grado 2:      0                 (0.0000)
```

**E gli archi quasi non crescono:**

```
             passo 60      passo 2700     variazione
nodi            2391          9511         +7120   (+298 %)
archi         429498        438532         +9034   (+2.1 %)
                                           1.269 archi per nodo nuovo
```

> **Nessuno dei 7120 nodi nati raggiunge mai il gruppo denso, e nessuno dei 2391 iniziali scende
> mai a grado 2.** Le due popolazioni sono **disgiunte e stabili**.

---

## 8. IL VERDETTO — **nessuna delle quattro letture, e non ne invento una quinta**

| # | richiedeva | misurato | esito |
|---|---|---|---|
| **A** | bimodali **+** clustering alto **+** catene fra pezzi **DIVERSI** | i primi due **sì**, il terzo **`0.0000`** | **CADE sul terzo** |
| **B** | gradi **continui**, nessun secondo picco | **270 valori consecutivi vuoti** | **CADE** |
| **C** | grado 2 **ma clustering alto** | `C = 0` sul **100 %** | **CADE la premessa** |
| **D** | i grado-2 sono neonati che **si allacciano** | **84 %** ancora a 2 dopo 2100 passi | **CADE** |

**LA FORMA, coi numeri e senza nome:**

1. **quattro componenti separate**, fissate dalla semina (`900 + 497×3`), che **in 2700 passi non
   scambiano nemmeno un arco**;
2. **tre di esse nascono COMPLETE** (`densità 1.0000`) e si diluiscono del **0.8 %**; la quarta
   nasce a `0.1476` e resta lì;
3. **ogni nodo nato dopo si attacca a due nodi della PROPRIA componente e non si allaccia più**:
   grado 2 per sempre, `C = 0`, catene lunghe **1** nell'85 % dei casi;
4. **le due popolazioni — seminata e nata — non si scambiano nemmeno un individuo.**

> **Ciò che si vede non è una struttura che si è formata: è la condizione iniziale, più una regola
> di nascita che aggiunge nodi senza mai collegarli fra loro.**

## 9. COSA QUESTO REFERTO **NON** DICE

- **non dice che la fisica non produca struttura**: dice che **in questa scena, con questa semina,
  la connettività non si muove**. Una scena con una semina diversa è **una misura diversa**, e non
  è stata fatta;
- **non dice perché** il pezzo da 900 stia a `0.1476` e gli altri a `1.0000`: è la semina, e non ho
  misurato la legge che la produce;
- **non spiega** perché gli archi crescano di `1.269` per nodo nuovo invece che di `2`: **il numero
  è misurato, il meccanismo no**;
- **UN SEME, UNA SCENA.** Nessuno di questi numeri ha una barra d'errore fra semi.

**E il nome non c'è, in nessuna riga.**
