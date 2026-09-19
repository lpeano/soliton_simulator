# REFERTO — **i tre cricchetti, misurati sui 45 snapshot**

**Blob `7c4dec1d`** · **seme `42`** · scena `N-MASSE`, 3 masse, `sep 8` · **45 snapshot**, passi
60-2700, cadenza 60 · strumento `csv/_test_fork/_tre_cricchetti.py` (`07ececc0`), esito
`csv/_test_fork/_tre_cricchetti.txt`.
**Letture fissate PRIMA:** `doc/TASK_HISTORY/2026-09-19_tre-cricchetti.md` (`05b1391`).

> **⚠ `--tau-luce` è attivo, sigillo `6/7`** *(`T3` è un risultato dichiarato)*: **ogni numero lo
> eredita.** **`--chi-basc` riscrive `perc_chi` a ogni passo.** **UN SEME, UNA SCENA.**
> **NESSUN RUN NUOVO, NESSUNA CURA.** Nessuna identificazione, nessun verdetto di fisica.

---

## 0. ⚠ LA PREMESSA ① DEL MANDATO È FALSA, E LA COLPA È DI UN MIO STRUMENTO

Il mandato diceva:

> *«dump, passo 2700: `perc_chi min = max = 1` → TUTTI +1. La popolazione è passata da tutta `-1` a
> tutta `+1`: una MONOCOLTURA CHE SI RIBALTA.»*

**Misurato leggendo `perc_chi` direttamente:**

```
fr(perc_chi == +1):  0.0000 (passo 60)  ->  0.1705 (passo 2700)
```

**Al passo 2700 l'83 % dei nodi è ancora `-1`.**

**Perché il dump diceva `min = max = 1`:** il mio `_dump_snapshot.py` applicava il **modulo a tutti
gli array**. Su `perc_chi`, che vale `±1`, il modulo dà `1` ovunque. **`min = max = 1` significava
«tutti ±1», non «tutti +1».**

> **È un difetto del mio strumento che ha prodotto una premessa falsa in un mandato**, ed è la
> **seconda volta nella stessa giornata** che quella funzione mi si ritorce contro *(la prima: i
> complessi, `3387e4a`)*. **Corretto alla fonte in `c56d992`** — i valori ora portano il segno — e
> il dump è stato **rigenerato**, perché era già uscito dal repo.

---

## 1. `chi_basc` — **TRANSIZIONE GRADUALE, non un ribaltamento**

```
fr(+1) da 0.0000 a 0.1705
snapshot con fr(+1) fra 0.05 e 0.95: 25 su 45   ->  TRANSIZIONE GRADUALE
la transizione copre i passi 1260 - 2700, e NON E' FINITA
nodi che cambiano segno fra snapshot consecutivi: da 0.0000 a 0.1083
```

**La forma è l'opposta di quella ipotizzata:** non una monocoltura che si ribalta di colpo, ma una
frazione `+1` che **cresce lentamente** e, a metà run, **non arriva a un quinto**.

### ⚠ E IL CONTROLLO DI CONSISTENZA FALLISCE — quindi la SPIEGAZIONE non vale

```
accordo fra twn>PHI_CRIT (ricostruito) e perc_chi:  minimo 0.972007   [soglia fissata: 0.999]
```

**La ricostruzione di `twn` non riproduce `perc_chi`**, quindi — **come fissato prima di misurare**
— **la lettura *«si ribalta perché `twn` supera `PHI_CRIT`»* NON VALE** e non la scrivo.

**Ipotesi sulla causa, dichiarata come ipotesi e NON usata:** `chi_basc` legge `_tw_src = _tw_t`,
cioè il `tw` **del passo corrente**, mentre lo snapshot salva `self.tw` **dopo** altri
aggiornamenti. È la famiglia di `Z19` *(«una grandezza letta in un momento del passo diverso da
quello che il codice dichiara»)*. **Non la uso come spiegazione: serve il `tw` nel momento giusto,
e dagli snapshot non c'è.**

> **Cosa resta VALIDO:** `fr(+1)` è letto **direttamente** da `perc_chi`, non ricostruito.
> **Il FATTO vale; la spiegazione no.**

### Ciò che il CODICE dice, e non serve misurare

`perc_chi[:self.n]` è riscritto **interamente a ogni passo** (`:3534`). L'eredità della mitosi
(`:1850`) **vive al massimo un passo**. **Quindi l'antimateria può nascere e viene comunque
riscritta** — ma *quanta* ne nasca, dagli snapshot a cadenza 60, **non è misurabile**.

## 2. `omega_s` — **NON è monotono. Cresce la CODA, non il centro**

```
|omega_s| mediana:  0  ->  51.22        intervalli in CRESCITA: 31 su 44  (13 SCENDONO)
|omega_s| p90:      0.52  ->  1.544e+04
|omega_s| max:      oscilla fra 5e5 e 1.3e6, senza trend netto
```

**La lettura fissata prima diceva: monotono ⇒ cricchetto (`A7`). Non è monotono: 13 intervalli su
44 scendono.** **Quindi NON è un cricchetto puro**, e non lo chiamo così.

**Ma il centro e la coda si separano di quattro ordini:** la mediana arriva a `51`, il `p90` a
`1.5 × 10⁴`. **È la coda a crescere.**

### `_tau` effettivo — **70 volte più piccolo di `TAU_A`**

> **⚠ Il mandato chiedeva se la mediana di `_tau` resti «incollata a `TAU_A = 50`», citando
> `_tau = TAU_A · max(dens/dens_rif, 0.05)`. QUEL RAMO IN QUESTO RUN NON GIRA:** `--tau-luce` è ON,
> quindi `_tau = _tempo_luce_nodo(i, j)` (`:2438`). Verificato dal codice **prima** di misurare.

```
tau p50 ~ 0.69   ->   tau/TAU_A ~ 0.0138        (misurato chiamando il codice vero)
tau p25: 0.556 -> 0.282 nell'ultimo tratto      (SCENDE)
```

**`_tau` non è incollato a `TAU_A`: è settanta volte più piccolo.** La domanda del mandato si
applica a un ramo diverso, e **il punto fisso di `A3` qui non è in gioco.**

## 3. LA PORTATA — **⚠ L'IPOTESI CADE, e si scrive che cade**

**L'ipotesi** *(di Claude web, dedotta)*: densità alta → `lambda_nodi` al pavimento `0.12` →
`rc = 0.36` → nessuno si connette → i nati restano a grado 2.

**Misurato chiamando `lambda_nodi()` DAL CODICE VERO su ogni snapshot** *(non ricostruito: è una
catena ricorsiva)*:

| passo | med(lam) | rc = 3·med | med(d) | **rc/d** | deg p25 | deg p50 | deg p75 |
|---|---|---|---|---|---|---|---|
| 60 | 0.60917 | 1.82751 | 0.8626 | **2.119** | 151 | 496 | 496 |
| 600 | 0.60917 | 1.82751 | 0.9628 | 1.898 | 2 | 167 | 496 |
| 1500 | 0.60917 | 1.82751 | 1.0895 | 1.677 | 2 | 2 | 496 |
| 2100 | 0.60917 | 1.82751 | 1.2545 | 1.457 | 2 | 2 | 177 |
| 2700 | 0.60917 | 1.82750 | 1.3251 | **1.379** | 2 | 2 | 68 |

**`med(lambda)` è COSTANTE a `0.60917` per tutti i 2700 passi. NON va al pavimento** *(che è
`0.12`)*. **`rc` è immobile a `1.8275`.** **`rc/d` scende — ma da `2.119` a `1.379`, e NON scende
sotto 1.**

> **L'ipotesi CADE.** La condizione che avrebbe dovuto reggerla — `rc/d < 1` — **non si verifica
> mai**, e il meccanismo proposto *(portata che si accorcia)* **non esiste: la portata non si
> muove di una cifra.**

**MA IL GRADO SI SEPARA DAVVERO:** `p50` da `496` a `2`, `p75` da `496` a `68`.

> **Quindi la separazione c'è, e NON per la ragione ipotizzata.** Quello che si riduce non è la
> portata: **sono le distanze che crescono** (`d` mediano `0.86 → 1.33`). **Il raggio di
> connessione resta fermo mentre il sistema si dilata.**
> *(Questo è ciò che i numeri dicono. **Perché** `lambda` resti esattamente costante non l'ho
> misurato, e non lo invento.)*

## 4. L'INERZIA AL PAVIMENTO — **cresce, e il cumulato sottostima il presente**

```
per INTERVALLO (differenze dei cumulati):  0.0000  ->  0.1152     crescente in 30 intervalli su 43
```

**Nell'ultimo intervallo l'`11.5 %` delle invocazioni è al pavimento**, contro il **`6.2 %`
cumulato** che il mandato citava. **I contatori sono cumulativi: il cumulato porta il peso del
passato e sottostima ciò che sta succedendo adesso.**

**La cura regge** — non è tornata al `100 %` di prima della correzione — **ma il sistema degenerato
la sta riempiendo**, e il tasso istantaneo è quasi il doppio del cumulato.

---

## 5. `Z9` — **RIQUALIFICATA, non chiusa né risolta**

**`eta` massimo `36.37` su `TAU_A = 50` → `ramp = 0.73`.** **Il kernel STAVA maturando**, e il
sistema si è fermato **mentre maturava**.

> **La domanda non è più «come lo faccio maturare», ma «cosa succede quando matura».**
> **`Z9` resta APERTA** — `Z9-b` non è stato misurato qui — **ma il suo presupposto è cambiato: la
> maturazione non è irraggiungibile, è stata raggiunta al 73 % in 2700 passi.**

## 6. E LE CURE DI IERI TENGONO, in un sistema che degenera

```
_ritmo_chiamate 2700   con   f_tutto_nullo 1   med_sul_pavimento 2   snap_identico 1
```

**Uno o due casi su 2700.** **`Z33`, `Z42`, `Z43` reggono** anche mentre il resto diverge — ed è un
dato a favore di quelle cure, non del sistema.

---

## 7. COSA RESTA APERTO

- **perché `fr(+1)` cresce**: la spiegazione via `twn` **non ha superato il controllo**, e serve
  il `tw` nel momento giusto del passo — **dagli snapshot non c'è**;
- **perché `med(lambda)` è esattamente costante** su 2700 passi;
- **perché il run si è fermato**: il referto `doc/REFERTO_blocco_run6000.md` resta senza
  spiegazione, e nulla di quanto misurato qui la fornisce.
