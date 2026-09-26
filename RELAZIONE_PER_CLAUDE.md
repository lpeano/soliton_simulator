> ## ⚠ DAL TAG `epoca-2`: **SISTEMA D**
> **Nuova carica (dallo spinore), scala minima `LAM` su `d` e `d0`, coesione adimensionale e causale** — piu' la **cura del mondo-dopo-i-flag**, che cambia ogni run.
> **Ogni numero misurato PRIMA appartiene all'EPOCA 1 e NON si confronta con l'epoca 2.**
> `EPOCA 2 = blob del simulatore del tag (`4954fe5b`, byte grezzi) + configurazione con `CHI_COOP`, `SCALA_MIN`, `COES_ADIM` ACCESI`. **Un run a flag spenti su quel blob e' ancora EPOCA 1**, e non e' un'opinione: lo provano `Z1` e `Z1c`, byte-identici.

> ### ⚠ CORREZIONE DEL 2026-09-21 — **la frase qui sopra e' IMPRECISA, e la lascio leggibile**
> **Cio' che avevo scritto:** *«un run a flag spenti su quel blob e' ancora EPOCA 1, lo provano `Z1`
> e `Z1c`».* **VALE SOLO CON L'ARGV NUDO.**
> **Perche' e' sbagliata:** `Z1c` confronta contro **«PRIMA + la cura del mondo»**, non contro
> **«PRIMA»** — la cura e' innestata su ENTRAMBI i bracci di proposito, senno' il sigillo misurerebbe
> LEI invece dei tre flag. **Quindi `Z1c` NON dice nulla sull'equivalenza con l'epoca 1.** A dirlo e'
> `Z1b`, che misura la differenza: **`n` 2569 -> 2580, archi 527 308 -> 526 202.** La cura e'
> **categoria D** e fa finalmente agire gli **otto** flag sul vuoto.
>
> **LA CLASSIFICAZIONE CORRETTA, in quattro righe:**
> ```
> EPOCA 1       blob PRECEDENTE al tag, qualunque configurazione
>
> EPOCA 1       blob del tag, argv NUDO, tre flag spenti
>               -> byte-identico, lo prova Z1
>
> EPOCA 1-bis   blob del tag, argv del FORK, tre flag spenti
>               -> NON e' epoca 1: e' epoca 1 CON LA CURA DEL MONDO.
>                  Il vuoto nasce coi flag del run invece che coi default. Lo misura Z1b.
>
> EPOCA 2       blob del tag + CHI_COOP, SCALA_MIN, COES_ADIM ACCESI
> ```
>
> **⚠ LA CONSEGUENZA PRATICA, ed e' operativa:** **i run del FORK di epoca 1 NON si riproducono sul
> blob nuovo, nemmeno a flag spenti** — **e NON E' UN DIFETTO.** Chi vuole rigirarli deve usare il
> **blob PRECEDENTE** (`git cat-file -p <commit>:soliton_simulator.py`, scritto in BINARIO).
>
> **Il tag NON si sposta e NON si riscrive:** un tag pubblicato che cambia sotto i piedi e' peggio
> dell'imprecisione. La correzione vive qui e in una `git notes` sul commit del tag.

---

## L'ARCHIVIO PER GIORNO - **il file vivo tiene SOLO 2026-09-26**

> **Regola di Luca, 2026-09-26.** A 20436 righe questo file non lo leggeva nessuno per intero, **quindi il suo scopo era gia' perso**. I giorni chiusi stanno in `doc/relazioni/`, uno per giorno, e `git log` resta l'indice.
> *(Diviso da `csv/_archivio_relazioni.py`, che dichiara la regola di taglio.)*

| giorno | righe | file |
|---|--:|---|
| `2026-09-14` | 134 | [`doc/relazioni/2026-09-14.md`](doc/relazioni/2026-09-14.md) |
| `2026-09-15` | 1310 | [`doc/relazioni/2026-09-15.md`](doc/relazioni/2026-09-15.md) |
| `2026-09-16` | 5551 | [`doc/relazioni/2026-09-16.md`](doc/relazioni/2026-09-16.md) |
| `2026-09-19` | 555 | [`doc/relazioni/2026-09-19.md`](doc/relazioni/2026-09-19.md) |
| `2026-09-20` | 1444 | [`doc/relazioni/2026-09-20.md`](doc/relazioni/2026-09-20.md) |
| `2026-09-21` | 5371 | [`doc/relazioni/2026-09-21.md`](doc/relazioni/2026-09-21.md) |
| `2026-09-24` | 1360 | [`doc/relazioni/2026-09-24.md`](doc/relazioni/2026-09-24.md) |
| `2026-09-25` | 3094 | [`doc/relazioni/2026-09-25.md`](doc/relazioni/2026-09-25.md) |

---

# ⚖️ **LE TRE FRAZIONI, DAL GIRO VALIDO: IL DIVARIO DEI FIGLI E' `W^2`, NON `peq`** *(2026-09-26)*

*(`csv/_test_fork/_scomposizione_figli.py`, referto in
`csv/_test_fork/_scomposizione_figli/SCOMPOSIZIONE_figli.txt`. Flag **SPENTO**, argv del driver,
2 semi, budget 120 passi, `passo_pieno`.)*

## PRIMA I CONTROLLI, perche' senza di essi le frazioni non valgono niente

```
COLLAUDO           4/4      chiude SOLO `geometrica|ok_n`    (1.776e-15 contro 9.27 del filtro vecchio)
K1   PASS   l'identita' chiude su 4300 campioni, scarto massimo 3.553e-15
K2   PASS   le frazioni hanno lo stesso segno e ordine sui DUE semi, a ogni eta'
K3          `coppia ~ ramp^0.146` (R2 0.58) e `^0.039` (R2 0.05)  ->  `R3bis` CADE
passi con NASCITE, ora TENUTI:   51 (s11)   46 (s12)      <- prima erano SCARTATI
nodi col contrasto DI CONVENZIONE, esclusi:   maturi 0/0   figli 210/211
```

> **`4300` campioni contro i `400` del giro invalidato**, e **`K2` che era `FAIL` ora e' `PASS`**:
> il campione distorto non era solo piu' piccolo, **era diverso**. **E i 210/211 figli esclusi sono
> esattamente l'eta' 1**, i nodi col `_contrasto = 1` di convenzione: nel giro invalidato erano
> sopravvissuti per caso *(`rho = 0.0` esatto)*, ora si escludono **per la causa giusta**.

## 🎯 **LA RISPOSTA: `T2` E' IL `107`-`114 %` DEL DIVARIO**

```
                %T2 (rho_s/W^2)   %T3 (peq EREDITATO)   %T1 (resto)     log(c_f/c_m)
s11  eta' 2        107.8              -3.3                 -4.5           -11.64
s11  eta' 14       114.0              -6.0                 -8.0            -6.55
s12  eta' 2        107.2              -2.8                 -4.4           -11.65
s12  eta' 14       114.4              -6.4                 -8.0            -6.53
```

> ### **IL DIVARIO DEI FIGLI E' TUTTO NEL PESO DI VICINATO, AL QUADRATO.**
> `T2` **eccede il 100 %** perche' gli altri due termini vanno **in direzione OPPOSTA** e lo
> compensano di `~8`-`14 %`.

**E LA STRUTTURA SI VEDE DIRETTAMENTE, come terza prova indipendente:**

```
rho ~ ramp^2.74        W ~ ramp^1.37        ->   rho ~ W^(2.74/1.37) = W^2.00
inerzia ~ ramp^2.80    (R2 0.95-0.96 su tutte)
```

**`2.00` esatto.** `rho_s` **e' il quadrato** di una somma pesata, e il dato lo dice **senza
passare dalla lettura del codice**.

## ❌❌ **E QUESTO RIBALTA UNA MIA LETTURA, non la sfuma**

**Cosa avevo scritto** *(sigillo esteso)*: *«la causa e' leggibile: `contrasto` e' 3-4 ordini
troppo piccolo **perche' `rho` parte da `2e-04` mentre `peq` e' ereditato a `1.37`**»*.

> ### ❌ **`T3` E' NEGATIVO: `-3` a `-6 %`.** Il `peq` del figlio e' **piu' PICCOLO** di quello dei
> ### maturi *(rapporto `~0.68`)*, quindi **riduce** il divario invece di produrlo.
> **L'errore era di CATEGORIA:** ho confrontato `peq = 1.37` con `rho = 2e-04` — **un rapporto
> interno al figlio** — e ne ho concluso qualcosa **sul confronto coi maturi**, che e' un'altra
> domanda. *(E' l'errore di popolazione di `A3`, fatto su me stesso.)*

## ⚠⚠ **MA LE FRAZIONI NON DICONO «COSA FAREBBE OGNI CURA», E LA DIFFERENZA E' GROSSA**

| | il legame frazione -> cura |
|---|---|
| **cura A**, `rho_s/W^2` | **ESATTO**: quella cura **rimuove `T2` per costruzione**. Togliere il `107`-`114 %` significa **piu'** che chiudere il divario: lo **rovescerebbe** di `~8`-`14 %` |
| **cura B**, `peq` alla nascita | **NON esatto, e qui devo essere chiaro**: `T3` e' il contributo **ATTUALE** del rapporto dei `peq`. Una cura che **cambiasse** `peq_f` — per esempio calibrandolo sul `rho` locale del figlio, cioe' da `1.37` a `~2e-04` — **sposterebbe `T3` di una quantita' ENORME**, non del suo valore attuale |

> ### **LA SCOMPOSIZIONE DICE DI COSA E' FATTO IL DIVARIO, NON COSA FAREBBE UNA CURA.**
> Per la **A** le due cose coincidono *(la cura rimuove esattamente quel termine)*. Per la **B**
> **no**: `T3 = -3 %` significa *«il `peq` ereditato non e' cio' che PRODUCE il divario»*, **non**
> *«curare `peq` alla nascita non avrebbe effetto»*. **Non ho misurato la seconda cosa**, e
> scriverlo come se l'avessi misurata sarebbe l'errore piu' facile di questa pagina.

## ✅ E `R3bis` CADE, ora su un campione valido

`coppia ~ ramp^0.146` *(`R2 0.58`)* e `^0.039` *(`R2 0.05`)*: **la coppia NON porta `ramp`.**
Quindi l'asimmetria di esponenti **fra coppia e inerzia non e' `1` contro `2`: e' `0` contro `2.8`**
— **piu' grande** di quanto l'ipotesi prevedeva, non piu' piccola.
*(E `|omega| ~ ramp^+0.16` / `^+0.07`: **sale** leggermente con `ramp`, non scende come `1/ramp`.)*

## 🛑 MI FERMO. **La scelta fra A e B e' di Luca**, e questi sono i numeri per farla.


---

# ✅ **CURA A SIGILLATA `5/6`: L'ESPLOSIONE DI OMEGA DEI FIGLI E' FINITA** *(2026-09-26)*

*(`csv/_seal_fork/_sigillo_cura_A.py`, referto in `csv/_seal_fork/_sig_cura_A/SIGILLO_cura_A.txt`.
Quattordici bracci, un processo ciascuno. Blob `df465759`; il braccio `/W` viene dal **padre** del
commit di `_wn * _wn`, non da `HEAD`.)*

```
C1'        FAIL   <- e il FAIL e' del mio CRITERIO: vedi sotto
P1-sexies  PASS   il braccio `/W` fallisce `C1'`, e le due popolazioni NON si toccano
C3         PASS   flag spento byte-identico al codice PRECEDENTE
C5         PASS   il pavimento non morde
F1         PASS   contrasto figlio/maturo fra 1.5 e 4
F2         PASS   |omega| figlio/maturo < 10
```

## 🎯 **`F2`: IL NUMERO CHE CONTA — DA `x47 000` A `x1.4`**

```
|omega|_figlio / |omega|_maturo, allo STESSO passo, media geometrica:
  ON  (`/W^2`)    eta' 2: 1.05    eta' 8: 1.42    eta' 14: 1.86      min 1.052  max 1.857
  OFF (il NULLO)  eta' 2: 16382   eta' 8: 48226   eta' 14: 44754
```

> ### **UN FATTORE ~30 000 DI RIDUZIONE.** Il difetto che avevo misurato come *«`|omega|` dei figli
> ### e' `600` contro `0.013` dei maturi»* **non c'e' piu'**: ora il figlio gira come un maturo,
> ### entro un fattore `2`.

## 🎯 **`F1`: LA PREVISIONE CALCOLATA PRIMA SI REALIZZA A MENO DELL'1 %**

```
contrasto_figlio / contrasto_maturo:
  ON   min 2.331   mediana 2.427   max 2.577      PREVISTO (calcolato PRIMA): mediana 2.4567
  OFF  7.7e-06 ... 1.6e-03                        <- cinque-sei ordini piu' in basso
```

**La previsione veniva da `exp(T1+T3)` sui dati del giro precedente**, scritta nel task history
**prima** di toccare il codice. **Misurata: `2.427` contro `2.4567` previsto, scarto `1.2 %`.**
*(Non e' una coincidenza fortunata: e' l'identita' della scomposizione che si verifica su un
sistema diverso — la cura — avendo predetto il residuo `T1+T3` dal sistema senza cura.)*

## ✅ `C5`: IL RISCHIO VERO NON SI E' MATERIALIZZATO

```
scala dell'inerzia, TUTTI i nodi:      p5        mediana    min        al pavimento
OFF                                    13.11     40.28      5.76       0/4252
`/W`                                   1.959     5.928      0.812      0/4252
`/W^2`                                 0.275     0.889      0.115      0/4252
```

**Il minimo e' `0.115`: CINQUE ordini sopra `1e-6`.** Dividere due volte abbassa la scala di `~45x`
rispetto a `OFF`, **e il pavimento resta lontano.** *(Era il criterio che avevo dichiarato come
rischio principale della cura, e si misura invece di sperarlo.)*

## ❌ **`C1'` FALLISCE, E IL DIFETTO E' DEL MIO CRITERIO — non della cura**

```
differenza |pend(contrasto) - pend(coppia)|
  OFF          1.2508   2.7838   1.3344   2.6934
  `/W`         0.6235   1.4431   0.7013   1.3760
  `/W^2`       0.0115   0.1167   0.0519   0.0535     <- un fattore 20-100 meglio di OFF
  spread FRA SEMI (ON) 0.0376   ->   soglia 2x = 0.0752
```

**Un solo valore su quattro sta sopra la soglia (`0.1167` contro `0.0752`).** E la soglia e'
**`2 x la deviazione standard dei valori ON stessi`**:

> ### **E' UN CRITERIO AUTO-REFERENZIALE: piu' la cura funziona, piu' i valori ON si stringono, piu'
> ### lo SPREAD si stringe, piu' la SOGLIA diventa severa.** Nel limite di una cura perfetta, la
> ### soglia tende a zero e **il criterio non puo' passare.**

**NON LO CORREGGO ADESSO** (`P1-sexies`: un criterio non si aggiusta dopo aver visto i numeri).
**Lo dichiaro, ed e' la seconda volta oggi** che scrivo un criterio la cui soglia dipende dai dati
che deve giudicare *(la prima era `C4`, che duplicava `C1`)*. **La forma sana sarebbe una soglia
ANCORATA al braccio OFF** — per esempio *«la differenza ON sta sotto un decimo di quella OFF»*, che
qui darebbe `0.12` contro `0.125`: **passerebbe**, e non si stringerebbe da sola. **Decide Luca.**

**E `P1-sexies` PASS dice che `C1'` DISTINGUE le due forme:** `/W` sta fra `0.62` e `1.44`, `/W^2`
fra `0.01` e `0.12` — **le due popolazioni non si toccano**, quindi il criterio **misura** la
differenza fra le due cure, anche se la sua soglia e' mal posta.

**E un numero in piu', che non era un criterio:** `|omega| k2/k77` sul taglio, ON:
**`x0.897`, `x1.187`, `x0.895`** — **sotto o intorno a `1`**, contro `x5.7`-`x176` di OFF.
**Omega non cresce piu' al calare di `k`.**

## ❌ **E LA CORREZIONE DELL'ERRORE DI UNITA' (rilievo di Luca), in tre posti**

**Avevo scritto:** *«l'asimmetria e' `0` contro `2.8`, `W^2` ne toglie `2`: **resta `0.8`**»*.
**Ho sottratto 2 potenze di `W` da 2.8 potenze di `ramp`: due basi diverse.**

```
W ~ ramp^1.37   ->   W^2 ~ ramp^2.74      inerzia/W^2 ~ ramp^(2.80-2.74) = ramp^0.06
coppia ~ ramp^0.10                        residuo:  0.06 - 0.10 = -0.04   <- ZERO nel rumore
```

**E IL DATO LO DICEVA GIA', nel referto che avevo scritto io:** `exp(T1+T3)` e' **piatto** su eta'
`2..14` (`x1.00`-`x1.08`) mentre `ramp` cresce `x5.20`. Con `0.8` potenze residue varierebbe di
**`x3.74`**; con `0.06`, di `x1.10`. **La piattezza esclude `0.8` di un fattore quattro.**

> ### ⇒ **`W^2` non e' una correzione parziale: CHIUDE L'ESPONENTE.** La mia frase *«questa cura
> ### non chiude quello»* era **troppo PESSIMISTA**, non troppo ottimista — ed e' un verso in cui
> ### sbaglio meno spesso, ma resta un errore.

**Corretto nel commento del codice, nel task history e nella scheda `inerzia-spinoriale`, con la
versione vecchia leggibile accanto** in tutti e tre.

## 🛑 MI FERMO. Il flag resta **OFF e FUORI dal driver**

**Cosa resta aperto, e non lo tocco:** **perche' la coppia non porta `ramp`** (`^0.15`, `^0.04`).
**Non e' un difetto dell'inerzia**: riguarda il termine `_tq*ramp` di `:3554` e il peso `ramp_i*ramp_j`
dentro `B`. **E' una domanda nuova, e va in coda, non in questa cura.**


---

# ⚖️ **`C1` A 4 SEMI: `FAIL` PER UN PELO** *(2026-09-26)*

> ### ❌❌ **IL TITOLO DICEVA ANCHE «E IL RESIDUO VALE `~0.06`»: E' RITIRATO** *(rilievo di Luca, 2026-09-26)*. **Titolo ritirato, leggibile:** *«`C1 a 4 semi` A 4 SEMI: `FAIL` PER UN PELO, E IL RESIDUO VALE `~0.06`»*. **Il motivo e' nel blocco di ritiro piu' sotto, e il `FAIL` stesso e' poi caduto col criterio: vedi `C1` nella forma COL SEGNO.**

*(`csv/_seal_fork/_sig_cura_A/SIGILLO_cura_A.txt`. Criterio di Luca, committato **prima** in
`4c104cf`. Esito complessivo **`5/6`**.)*

```
verso corti    4 semi: 0.1167  0.0535  0.0090  0.0247
   media 0.0510   SE 0.0238   ->  2 SE = 0.0475      NON compatibile con zero
   `/W` media 1.3774      ON sta SOTTO
verso lunghi   4 semi: 0.0115  0.0519  0.1533  0.0511
   media 0.0669   SE 0.0303   ->  2 SE = 0.0606      NON compatibile con zero
   `/W` media 0.6749      ON sta SOTTO
OFF: 1.2508  2.7838  1.3344  2.6934  1.3853  2.6912  1.2476  2.6842
```

## **`(b)` PASSA IN ENTRAMBI I VERSI, `(a)` FALLISCE PER IL 7 E IL 10 %**

**`(b)`: `ON` sta sotto `/W`** di un fattore **`27`** *(corti)* e **`10`** *(lunghi)*, e sotto `OFF`
di un fattore **`20`-`50`**. **La cura funziona, e il criterio lo dice.**

**`(a)`: la media e' a `2.1` e `2.2` SE da zero**, non a `≤ 2`. `0.0510` contro `0.0475`,
`0.0669` contro `0.0606`. **Il residuo NON e' compatibile con zero — ed e' un risultato, non un
intoppo.**

## ❌❌ **RITIRATO il 2026-09-26 (rilievo di Luca) — NON C'E' UN RESIDUO CON UN VERSO**

> **Cio' che avevo scritto, leggibile qui sotto per intero:** *«il numero del residuo e' lo stesso
> ordine che l'aritmetica degli esponenti prevedeva — `~0.06` in entrambi i casi — il residuo non
> sembra rumore»*.

**PERCHE' CADE, e non serve un dato nuovo: bastano i SEGNI, che il valore assoluto aveva buttato via.**

```
differenze FIRMATE  pend(contrasto) - pend(coppia)      (dagli STESSI json)
   corti    +0.1167   +0.0535   +0.0090   -0.0247       <- UNO NEGATIVO
   lunghi   +0.0115   +0.0519   +0.1533   -0.0511       <- UNO NEGATIVO
```

> ### **Un residuo che venga da un'asimmetria di esponenti ha UN VERSO: la pendenza del contrasto
> ### sta SEMPRE dallo stesso lato di quella della coppia.** Qui **due valori su otto hanno il segno
> ### opposto**, e la media sta a **`0.97`** e **`1.26`** errori standard da zero. **Non c'e' un
> ### residuo con un verso: c'e' dispersione fra semi.**

**E LA COINCIDENZA NUMERICA NON REGGEVA NEMMENO NEL SEGNO**, ed e' il pezzo che avrei dovuto vedere
da solo: l'aritmetica prevedeva **`0.06 - 0.10 = -0.04`**, cioe' un residuo **NEGATIVO**, mentre il
numero con cui lo confrontavo era una **media di valori assoluti**, **positiva per costruzione**.
**Ho confrontato un numero firmato con un numero che non puo' essere negativo, e ho chiamato
accordo il fatto che i moduli si somigliassero.**

**⚠ E IL MIO STESSO PARAGRAFO DI PRUDENZA NON MI HA FERMATO:** avevo scritto *«sono grandezze
DIVERSE su POPOLAZIONI DIVERSE ... una coincidenza di ORDINE DI GRANDEZZA, NON un'identita'»* —
e **poi ho messo il numero nel TITOLO**. **Dichiarare un limite e poi titolare come se non ci
fosse e' il modo in cui una cautela diventa decorativa.**

### La versione RITIRATA, leggibile per intero:

## ~~E IL NUMERO DEL RESIDUO E' LO STESSO ORDINE CHE L'ARITMETICA DEGLI ESPONENTI PREVEDEVA~~

```
dall'aritmetica (sui FIGLI):     inerzia/W^2 ~ ramp^(2.80 - 2.74) = ramp^0.06
misurato ora (sul TAGLIO):       residuo di pendenza  0.051  e  0.067
```

> ### **`~0.06` in entrambi i casi.** Il residuo non sembra rumore: sembra **cio' che resta perche'
> ### `W` non e' esattamente `rho^(1/2)`** — `rho ~ ramp^2.74` e `W ~ ramp^1.37` danno `2.74/1.37 =
> ### 2.00` **arrotondato**, e la differenza fra `2.80` (inerzia) e `2.74` (`W^2`) e' proprio `0.06`.

**⚠ E QUI MI FERMO PRIMA DI DIRE TROPPO, perche' oggi ho gia' sbagliato due volte in questo modo:**
i due `0.06` sono **grandezze DIVERSE su POPOLAZIONI DIVERSE** — uno e' un esponente in `ramp` sui
**figli**, l'altro una differenza di pendenza in `k` sul **taglio**. **E' una coincidenza di ORDINE
DI GRANDEZZA che sostiene il quadro, NON un'identita'.** Chiamarla conferma sarebbe l'errore di
categoria che Luca mi ha corretto stamattina.

## ✅ GLI ALTRI CINQUE

```
P1-sexies  PASS   `/W` sta fra 0.6065 e 1.4431, `/W^2` fra 0.0090 e 0.1533: NON si toccano
C3         PASS   flag spento byte-identico al codice PRECEDENTE (a2a60534^)
C5         PASS   il pavimento non morde
F1         PASS   contrasto figlio/maturo 2.331-2.577, previsto 2.4567
F2         PASS   |omega| figlio/maturo 1.05-1.86, contro 16382-52738 di OFF
```

## ❌❌ **E TRE DIFETTI MIEI, di cui uno GROSSO, nei due referti precedenti**

**① I BRACCI `off_*` GIRAVANO COL FLAG ACCESO.** Appena la cura e' entrata nel driver,
`ARGV_OFF = list(ARGV)` **conteneva `--contrasto-intensivo`**: il braccio spento era **un secondo
braccio acceso**, e i due stampavano numeri **identici riga per riga**.

> ### **E' il difetto del DEFAULT RIBALTATO del par.9**, in veste nuova: *«quando si ribalta un
> ### default, si cercano TUTTI i punti che ottenevano il vecchio comportamento per OMISSIONE»*.
> **E quel paragrafo l'ho citato IO, stamattina**, per spiegare perche' il driver non puo' dare il
> braccio OFF di un'obbligatoria. **L'ho scritto e non l'ho applicato al mio stesso sigillo.**
> Ora si usa `senza()`, che **asserisce** che l'opzione ci fosse.

**② La statistica era su OTTO bracci, non su QUATTRO SEMI** *(`4 semi x 2 versi` mescolati:
errore di popolazione, `A3`)*. **Ora per verso.**
**③ `C3` girava su 4 semi mentre i bracci `pf_*` esistono solo su 2** -> `FAIL` **per un difetto
di ciclo**. Un `FAIL` che viene da un braccio non lanciato **non e' un riscontro**.

## ❌ **E UN DIFETTO DEL MIO PROCESSO, che e' la causa del giro a vuoto**

**Il primo tentativo di patch e' fallito su un'ancora MENTRE GIRAVA IN BACKGROUND.** Non ho visto
l'`AssertionError`, ho creduto di aver corretto, **il commit non e' passato** *(niente da
committare)*, e **ho letto un referto del codice VECCHIO** riferendo numeri che non appartenevano a
nessuna versione corretta.

> ### **LE PATCH SI LANCIANO IN PRIMO PIANO: un patch script in background e' un `assert` che
> ### nessuno legge.** E il `[TIMBRO] committato e pulito` in testa al log **lo diceva** — un
> sigillo che gira su un file identico a `HEAD`, dopo che credevo di averlo modificato, **e' la
> prova che la modifica non c'e'**.

## ⚠ **E UN LIMITE DELLA RIPRESA, che ho costruito io ieri**

Ho dovuto **cancellare a mano** i json dei bracci `off_*`: portavano **il blob giusto con la
configurazione sbagliata**. **Il blob certifica il CODICE, non l'ARGV**, e la ripresa si fida del
blob. **-> voce `RIPRESA-ARGV` in coda.**

---

# ✅ **PASSO 1 — IL CRITERIO CON `|x|` NON ERA SODDISFACIBILE: dimostrato su rumore puro** *(2026-09-26)*

*(`csv/_collaudo_criterio_zero.py`, referto `doc/COLLAUDO_criterio_zero.txt`. Committato **prima**
di rileggere i numeri veri, come Luca ha ordinato.)*

```
scala s   forma        PASSA     media/SE p50   media/SE p90
0.01      con |x|      0.1415    2.8969         5.3771
0.01      col SEGNO    0.8606    0.7634         2.3514
0.05      con |x|      0.1404    2.9045         5.3755
0.05      col SEGNO    0.8622    0.7601         2.3407
1         con |x|      0.1414    2.8990         5.3892
1         col SEGNO    0.8612    0.7680         2.3445

con |x|     passa il 14.11 %   ->  FALLISCE l'85.89 % su RUMORE PURO
col SEGNO   passa l'86.13 %
```

> ### **IL `FAIL` DELLA FORMA CON `|x|` NON DICEVA NIENTE SULLA CURA:** quel criterio fallisce
> ### l'**85.89 %** delle volte **anche quando non c'e' nessun effetto residuo**. **Non era
> ### soddisfacibile**, e l'errore e' mio: l'ho scritto io.

**E I NUMERI DI LUCA ERANO ESATTI:** aveva detto *«~86 % delle volte, media/SE tipica 2.9»* —
misurato **`85.89 %`** e **`2.897`**.

**⚠ E SUL «~90 % o piu'» DELLA FORMA COL SEGNO: il valore vero e' `86.13 %`, non `90`**, e lo dico
invece di arrotondarlo verso l'aspettativa. **E' esatto per costruzione:** per 4 valori `iid` quella
forma e' **esattamente** un `t` di Student con **3 gradi di liberta'** contro la soglia `2`, e
`P(|t_3| <= 2) = 0.8607`. **Il criterio del collaudo era LA SEPARAZIONE** (`14 %` contro `86 %`),
**e quella c'e'.**

**UN CONTROLLO IN PIU', che doveva essere vero per costruzione:** il criterio e' un rapporto
`media/SE`, quindi **invariante di scala** — e le tre scale danno lo stesso numero a meno del
campionamento (`0.1415`, `0.1404`, `0.1414`). **Se cosi' non fosse, il collaudo sarebbe sbagliato**,
e questa riga esiste per accorgersene.

**E IL DATO MISURATO E' `2.1`-`2.2 SE`**, cioe' **PIU' VICINO A ZERO del rumore puro** *(mediana
`2.90`)*. **Il `FAIL` non era un segnale di residuo: era il criterio.**

**LIMITE DICHIARATO — ❌ E IL VERSO CHE AVEVO SCRITTO ERA INVERTITO (rilievo di Luca):**
~~*«la `SE` vera sarebbe piu' grande e il criterio piu' facile»*~~.
**SBAGLIATO.** Il criterio **usa la `SE` CALCOLATA dai 4 valori**, non quella vera. Con semi
**CORRELATI** la `SE` calcolata **SOTTOSTIMA** quella vera *(per dati correlati positivamente
`Var(media) > s^2/n`)*, quindi **`media/SE` e' GONFIATO** e il criterio **fallisce PIU' spesso**:
**il rischio e' un RESIDUO FALSO**, non un criterio piu' facile.
**E la direzione conta:** significa che un `FAIL` della forma col segno, su semi correlati,
**potrebbe essere un artefatto della correlazione** — mentre un `PASS` resterebbe informativo.
**Non ho misurato la correlazione fra i semi**, e questo limite resta.
---

# ❌ **CORREZIONE: il disallineamento del reperto C'ERA, e l'ho attribuito al commit sbagliato**

*(rilievo di Luca ripetuto, misurato commit per commit il 2026-09-26)*

```
3c5e404   copia 1554e2f9   referto cita 1554e2f9    coerente
e062fdb   copia 1554e2f9   referto cita 3cd1dd4f    ⚠ INCOERENTE
aae56ba   copia 3cd1dd4f   referto cita 3cd1dd4f    coerente
HEAD      copia 3cd1dd4f   referto cita 3cd1dd4f    coerente, albero pulito
```

> ### **IL DISALLINEAMENTO C'ERA, e l'ha creato `e062fdb`** — che ha committato **il referto nuovo
> ### senza la copia rigenerata**. **`aae56ba`, il commit segnalato, e' quello che l'ha RIPARATO.**

**La mia prima risposta diceva *«oggi non c'e' disallineamento e un ripristino lo creerebbe»*: la
**conclusione** era giusta, la **storia** no.** E la differenza conta, perche' cambia dove sta il
difetto: non in `aae56ba` (che ripara) ma in **`e062fdb`** (che ha spezzato la coppia
referto+copia). **L'ho scoperto solo elencando i blob commit per commit**, cioe' facendo la misura
invece di ricostruire a memoria — ed era il terzo caso oggi in cui una premessa su *quale commit
ha fatto cosa* si e' rivelata invertita.

**A `HEAD` non c'e' niente da ripristinare** *(copia e referto coincidono, albero pulito)*.
**Ma il rilievo di Luca coglie un difetto reale: un commit HA lasciato un reperto incoerente, e
nessun presidio se n'e' accorto.** -> voce **`REPERTI-IMMUTABILI`**, e ora ha un caso reale da
cui nascere: **`e062fdb`**, non un'ipotesi.

---

# ✅ **`C1` PASSA NELLA FORMA COL SEGNO: `(a')` E `(b)` IN ENTRAMBI I VERSI** *(2026-09-26)*

*(`csv/_seal_fork/_c1_col_segno.py` -> `csv/_seal_fork/_sig_cura_A/C1_COL_SEGNO.txt`. **Nessun
rigiro del simulatore**: legge i json dei bracci del sigillo della cura A, blob `fb51ae80`, e
ricalcola le pendenze con **la stessa funzione `pend` del sigillo**, copiata.)*

```
verso    differenze FIRMATE                        media     SE       |media|/SE   esito
corti    +0.1167  +0.0535  +0.0090  -0.0247        +0.0386   0.0306   1.2640       COMPATIBILE
lunghi   +0.0115  +0.0519  +0.1533  -0.0511        +0.0414   0.0429   0.9656       COMPATIBILE
(b)      corti  ON 0.0510  <  /W 1.3774  (x27)  <  OFF 2.7132  (x53)
         lunghi ON 0.0669  <  /W 0.6749  (x10)  <  OFF 1.3045  (x19)
```

## 🎯 **IL NUMERO COINCIDE CON QUELLO DEL GUARDIANO, E VA DETTO ANCHE PERCHE' COINCIDE**

**Atteso da Luca dal referto: `0.97` lunghi, `1.26` corti. Misurato dallo script: `0.9656` e
`1.2640`.** *(L'unico scarto e' un arrotondamento: `+0.0090` contro `+0.0089` sul seme 13 dei
corti.)* **Non c'era modo di saperlo senza ricalcolarlo:** un numero d'accordo **per caso** e un
numero d'accordo **per costruzione** si distinguono solo facendo il conto.

## ⚠ **PERCHE' IL CRITERIO E' CAMBIATO: UN COLLAUDO, NON IL DATO**

```
su RUMORE PURO (4 valori N(0,s), 1e5 prove, seme fisso 20260926) -- la CURA PERFETTA:
   con |x|      passa il 14.11 %   ->  FALLISCE l'85.89 %,  media/SE tipica 2.897
   col SEGNO    passa l'86.13 %        (= P(|t_3| <= 2), il valore esatto)
```

> ### **La media di quantita' tutte POSITIVE non puo' essere compatibile con zero.** Il criterio
> ### vecchio falliva quasi sempre **anche quando non c'era niente da trovare**: il suo `FAIL` sui
> ### dati veri **non era un riscontro sulla cura, era un riscontro su se stesso.**

**E il collaudo e' stato committato PRIMA di rileggere i numeri** (`aae56ba` lo strumento, `ecf1e2c`
l'esito), **proprio perche' `P1-sexies` vieta di aggiustare un criterio dopo aver visto i dati.**
La forma nuova **non e' piu' larga per comodita'**: e' `t` di Student con 3 gradi di liberta' contro
la soglia `2`, e passa l'**86 %** sul nulla — **non il 100 %** — quindi un suo `FAIL` **sarebbe**
ancora informativo.

**⚠ IL LIMITE, col verso corretto:** con semi **correlati** la `SE` calcolata **sottostima** quella
vera, `|media|/SE` e' **gonfiato**, e il criterio fallisce **piu'** spesso — **il rischio e' un
residuo FALSO**, non un `PASS` regalato. **Un `PASS` resta informativo.** La correlazione fra i
quattro semi **non e' misurata**.


---

# ❌❌ **RITIRO: «IL RESIDUO `~0.06` E' L'ARITMETICA DEGLI ESPONENTI»** *(rilievo di Luca, 2026-09-26)*

**Ritirato in `RELAZIONE_PER_CLAUDE.md` (titolo e sezione, versione vecchia leggibile accanto) e
registrato in `doc/STATO_RUN.md`.**

```
differenze FIRMATE  pend(contrasto) - pend(coppia)
   corti    +0.1167   +0.0535   +0.0090   -0.0247        media/SE = 1.26
   lunghi   +0.0115   +0.0519   +0.1533   -0.0511        media/SE = 0.97
```

> ### **Due valori su otto hanno il segno opposto: un residuo da asimmetria di esponenti avrebbe UN
> ### VERSO.** Non c'e' un residuo di `0.06`: c'e' **dispersione fra semi**.

**E IL CONFRONTO NON REGGEVA NEMMENO NEL SEGNO:** l'aritmetica prevedeva **`0.06 - 0.10 = -0.04`**,
**negativo**; il numero con cui lo confrontavo era una **media di valori assoluti**, positiva **per
costruzione**. **Un numero firmato contro un numero che non puo' essere negativo.**

**⚠ E il mio paragrafo di prudenza c'era, sotto quella sezione** *(«grandezze diverse su popolazioni
diverse, coincidenza di ordine di grandezza, non un'identita'»)* **e non e' servito, perche' il
numero era nel TITOLO.** **Una cautela scritta sotto un titolo che la contraddice e' decorativa.**

**NB di onesta' sul posto del ritiro:** la frase viveva nella **relazione**, **non** nella riga
`POTENZE-1` di `STATO_RUN`. L'ho registrata anche la' perche' Luca l'ha chiesto in entrambi i posti
— **non** perche' ce l'avessi scritta: dire *«corretto in due posti»* lasciando credere che
l'errore fosse in due posti sarebbe un'esagerazione nella direzione comoda.


---

# ✅✅ **CURA A CHIUSA `6/6`, E LA BOZZA DELLA LISTA CHIUSA E' PRONTA** *(2026-09-26)*

```
C1 (a' col segno)  PASS   |media|/SE  0.9656 lunghi   1.2640 corti     4 semi, FIRMATE
C1 (b)             PASS   ON sotto /W   x27 corti   x10 lunghi
P1-sexies          PASS   le due popolazioni non si toccano
C3                 PASS   byte-identico al codice PRECEDENTE (`a2a60534^`), 121 campi
C5                 PASS   pavimento: min 0.115, cinque ordini sopra `1e-6`
F1                 PASS   2.427 contro 2.4567 PREVISTO prima del codice (1.2 %)
F2                 PASS   |omega| figlio/maturo da x47 000 a x1.4
```

**`POTENZE-1` e' CHIUSA in `doc/STATO_RUN.md`**, e la cura vive **nel driver** —
`--contrasto-intensivo` in ogni run, sigillo del driver `16/16`, **14 obbligatorie**.

## 📋 **LA BOZZA DELLA LISTA CHIUSA: `doc/LISTA_CHIUSA.md`, GENERATA E NON RICOPIATA**

*(`csv/_lista_chiusa.py`, mandato globale `0c42925` parte 1. **Nessun run.**)*

```
difetti acclarati in tabella       38
APERTI o con CURA DERIVATA         24   <- LA LISTA
gia' CURATI / non-difetti          14   <- restano in tabella, non si cancellano
voci di coda non-difetto           13   <- strumenti, domande, misure da rifare

per famiglia:  A 1   B 3   C 4   D 6   E 5   F 5   G 0 difetti
               + 13 voci di coda, di cui 8 in G
```

> ### ⚠ **NON E' ANCORA UNA LISTA CHIUSA: E' UNA PROPOSTA.** Diventa la linea d'arrivo **solo
> ### quando Luca la approva**, e finche' non lo e' **non vale il vincolo che vieta le indagini nuove**.

**COSA E' GENERATO E COSA E' MIO GIUDIZIO, dichiarato nel documento stesso:** dal file vengono
`ID`, la riga del difetto, la prova, il campo `cura` e lo stato; **mio** e' l'assegnazione alla
**FAMIGLIA**, che sta in `FAMIGLIA_DI` — **una riga per ID**, cosi' si corregge in un posto solo.

**❌❌ E DUE DIFETTI DEL MIO GENERATORE, trovati leggendo il suo output:**

```
① la regex perdeva D34 e D37    perche' portano il loro stato DOPO l'id: `| **D37** CURATO |`
                                 -> 36 difetti invece di 38, e DUE voci SPARITE IN SILENZIO
② un `%3d` senza argomento      la riga «APERTI o con CURA DERIVATA  %3d» stampava il segnaposto
```

> ### **Il primo e' il piu' grave, ed e' il difetto di `A9` in forma nuova: un elenco che PERDE
> ### righe non si denuncia**, perche' il totale sembra plausibile. **L'ho visto solo perche' avevo
> ### messo un `assert len(D) >= 30` e un controllo `SENZA FAMIGLIA`** — ma il controllo guardava
> ### **un solo verso**. **Ora guarda anche l'inverso** *(un ID classificato che la tabella non
> ### contiene)*, ed e' quello che avrebbe preso `D34` e `D37` subito.

**⚠ E DUE COSE CHE LA BOZZA NON HA, dichiarate nel documento invece di riempirle:** la
**DIMENSIONE** di ciascuna voce *(stimarla richiede di leggere il codice di ognuna: e' lavoro, non
generazione)* e l'**ordine per DIPENDENZE dentro la famiglia** *(le dipendenze non stanno in un
campo, quindi ricavarle sarebbe un giudizio mio riga per riga)*. **Il mandato le chiede entrambe:
mancano, e lo dico.**

## 🛑 **STOP, come da mandato: la lista la APPROVA Luca.**

**Il PILOTA e' registrato e NON e' partito** *(scena (ii)(a), 1 seme, 600 passi, snapshot ogni 60,
riprendibile; scopo: costo s/passo, `OMEGA-ETA` fino a `ramp = 1`, nessun crash con la cura A;
**niente tag, numeri non pubblicabili come risultato**)*.


---

# ❌❌ **LA MIA BOZZA DELLA LISTA CHIUSA ERA `STANDARD 9`: LEGGEVA UNA FONTE SOLA**
*(rilievo di Luca, 2026-09-26)*

**Luca non trovava nella bozza, fra le altre:** `SCALE-TW`, la **soglia di torsione `3π`**, `B5`
*(theta, il collo di bottiglia)*, la **cura 5 via CLI**, le **misure da rifare in configurazione del
driver** *(`chi comprime d0`, il `tasso di mitosi`, `|dx|/d` = `V8`/`V9` che decide il freno)*,
`D33`, `A3`, `CURA 3`, `PASSO-2`, `FRAG1`, `M1`, `M2`, **i 24 script con `step()` da solo**.
**Aveva ragione su tutte.**

## ❌ **IL DIFETTO DI PRINCIPIO, e quello MECCANICO**

```
di PRINCIPIO   leggevo la SOLA tabella dei difetti acclarati e presentavo il risultato come
               LA LISTA. Non si deduce l'assenza da una ricerca parziale.
MECCANICO      raccoglievo righe CONTIGUE, e la tabella `IN CODA` e' INTERROTTA da un blocco
               di codice a meta': vedevo 6 righe su 43. Un elenco che perde righe NON SI
               DENUNCIA, perche' il totale sembra plausibile.
```

> ### **E il difetto meccanico da solo bastava:** in quelle 37 righe perse c'erano `PASSO-2`,
> ### `FRAG1`, `M1`, `M2`, `A3`, `CLI-1`, `CONFIG-1`, `CONTAGIO`, `U1`, `U2` — **cioe' meta'
> ### dell'elenco di Luca.**

## ✅ **LA VERSIONE NUOVA: CINQUE FONTI, E OGNI VOCE HA UN POSTO**

```
fonte                                      voci   in LISTA   FUORI LISTA   sezioni fuori portata
STATO_RUN.md                                246       157          89                5
RAMIFICAZIONI.md                            198       118          80                1
REGISTRO_FISICA.md                          172       122          50               39
INVENTARIO_passo_incompleto.md                2         2           0                2
CONFIGURAZIONE_misure_2026-09-25.md           6         6           0                1
TOTALE                                      624       405         219               48
```

**LE FONTI SONO CINQUE E NON QUATTRO:** `CONFIGURAZIONE_misure_2026-09-25.md` e' **l'unico posto**
dove stanno le sei misure da rifare in configurazione del driver. **Senza di lei `chi comprime d0`
non comparirebbe**, ed e' esattamente il difetto da curare.

**Nessuna esclusione in silenzio:** le `219` voci `FUORI LISTA` sono **stampate per intero, con la
loro riga e col motivo proposto** — *gia' curata o chiusa*, *sospetto non acclarato*, *limite
legittimo (`A11`)*, *riga descrittiva della legge*, *dopo il run base*, *chiusa per dimostrazione*.
**La decisione di escludere e' di Luca.**

## ✅ **IL COLLAUDO NEI DUE VERSI, E IMPEDISCE** *(`csv/_collaudo_lista_chiusa.py`, 2/2)*

```
ramo che DEVE passare   il generatore vero            -> uscita 0, documento scritto
ramo che DEVE fallire   una copia con una voce che    -> uscita 3, e lo sha1 del documento
                        NON esiste nell'elenco           NON cambia: 668f7538 -> 668f7538
```

**Le quindici voci di Luca sono diventate il criterio**, e il criterio guarda **la parte IN LISTA**,
non il documento intero: **una voce che comparisse solo fra le escluse non passerebbe**.
*(Ho verificato PRIMA di stringerlo che tutte e quindici stanno in lista — lo dico perche' l'ordine
conta: stringere un criterio DOPO un `FAIL` sarebbe `P1-sexies` violato.)*

## ❌❌ **E DUE DIFETTI TROVATI STRADA FACENDO, entrambi dei REGISTRI, non del codice**

**① `VALE SEMPRE` SIGNIFICA DUE COSE OPPOSTE.** In `RAMIFICAZIONI` vuol dire **chiusa per
dimostrazione**; in `STATO_RUN` *(«APERTE DA PRIMA»)* vuol dire **la voce vale ANCORA**, cioe'
**aperta**. **Come esclusione generica aveva buttato fuori proprio `A3` e `B5`** — due delle voci
che Luca cercava. **Ora la chiusura si legge dalla SEZIONE, non dalle parole.**

**② LA TABELLA DEI DIFETTI ACCLARATI NON E' CONTIGUA:** `D34`-`D38` **cadono sotto l'intestazione
di `PROVE DI SPEGNIMENTO`**. Un'esclusione per sezione, senza guardia, **avrebbe buttato fuori
cinque difetti acclarati per la loro POSIZIONE nel file**. La guardia c'e' *(un'etichetta `Dxx` non
si esclude per sezione)*, ed e' **la stessa forma del difetto di partenza, vista dall'altro lato.**

## ⚠ **COSA MANCA ANCORA, e non lo copro**

- **la DIMENSIONE** di ciascuna voce e **l'ordine per DIPENDENZE**: nessuna fonte li porta in un
  campo, quindi sarebbero **giudizio mio riga per riga**. **Il mandato li chiede: mancano.**
- **`111` voci SENZA FAMIGLIA**: nessuna regola ha deciso. **Le elenco in una sezione a parte**
  invece di metterle in una famiglia a caso.
- **la stessa voce puo' comparire due volte** se sta in due registri. **Non le ho unificate:** un
  doppione visibile e' meno dannoso di una voce persa.
- **`405` in lista NON vuol dire «405 difetti da curare»**: vuol dire che **405 righe non portano un
  marchio di chiusura**. Fra loro ci sono criteri, previsioni e voci di lavoro. **La potatura la fa
  Luca**, ed e' il senso della parola *approvazione*.


---

# 🧭 **PROPOSTA DI LUCA: UN REGISTRO STRUTTURATO AL POSTO DELLE TABELLE** *(valutazione, 2026-09-26)*

*(`doc/VALUTAZIONE_registro_strutturato.md`. **Nessuna migrazione e' cominciata: decide Luca.**)*

**LA DIAGNOSI DI LUCA E' GIUSTA, e la ragione e' piu' forte di come l'avevo capita io.** Il parser
di oggi deve **INFERIRE dalla prosa tre cose che sono DECISIONI**:

```
① che cosa e' UNA VOCE     -> inferito dalla CONTIGUITA' delle righe   ->  6 righe su 43
② qual e' il suo STATO     -> inferito dalle PAROLE   ->  `VALE SEMPRE` = chiusa E aperta
③ a quale FAMIGLIA sta     -> inferito da parole chiave  ->  111 senza famiglia, `CLI-1` in `A`
```

> ### **Tutti e tre i difetti di oggi sono fallimenti di INFERENZA, non errori di codice.** Un campo
> ### **dichiarato** non si puo' inferire male: si puo' solo sbagliare a scriverlo, **e allora si
> ### vede nel diff.**

## ✅ IL MIO PARERE, IN QUATTRO PUNTI

**① SI', ed e' meglio — ma consiglio UN FILE PER VOCE** *(`doc/difetti/<ID>.yaml`)* invece di un
`difetti.yaml` unico: **git da' una storia PER DIFETTO** *(e in questo repo la prova di un difetto
**e'** un commit)*, e *«nessuna voce si cancella»* diventa **`git diff --diff-filter=D`**, cioe' un
fatto di git invece di un controllo di parsing. **`PyYAML 6.0.3` c'e' gia'**, quindi il loader
stretto non aggiunge dipendenze. **JSON lo scarto** *(niente commenti, diff peggiore)*; **il
Markdown «macchina-primo» lo scarto per `A9`**: non toglie l'inferenza e la sua regola dipende dal
ricordarsene — **ed e' gia' stata rotta**.

**② I RISCHI, e il piu' grosso NON e' la perdita di voci:** e' **`R4`, LA COLLISIONE DI ID**, e
**l'ho misurata oggi**: **`A3` sono DUE voci diverse** — in `RAMIFICAZIONI` *«FDT del solo
scuotimento»*, **chiusa per dimostrazione**; in `STATO_RUN` *«il disegno esce dalla dinamica»*,
**aperta**. Idem `B5`, `M1`, `M2`, `C21`. **Senza ID namespaced la migrazione fonde due cose e
chiude un fronte aperto in silenzio.**
Gli altri: **`R1`** perdita di voci *(controllo: il parser di oggi resta come **secondo lettore
indipendente**, e si fa il `diff` delle due letture)*; **`R2`** stato scelto male *(controllo: il
campo **`stato_da`** con la **frase verbatim**, e **`da-decidere`** come stato legittimo)*; **`R3`**
due verita' *(controllo: le tabelle vecchie si **RIGENERANO** dentro marcatori e **il hook rifiuta
una modifica a mano dentro i marcatori** — l'intestazione «fa fede» da sola e' una nota, `A9`)*;
**`R5`** lo sweep e' esso stesso un parser su prosa — **converte ignoti in CONTATI, non li
elimina**.

**③ IL COSTO, coi numeri MISURATI separati dalle stime.** Misurato: **`436` ID distinti** in
**`217`** file `.md` *(`D` 45, `Z` 137, `S` 23, `C` 28, `B` 11, `A` 13, `E` 4, `M` 5, nomi col
trattino **170**)*, e dei nomi col trattino **circa META' NON E' UN ID** *(`BYTE-INERTE`,
`NON-ABELIANO`, `ON-OFF`, `NO-OP`, `PURE-READ`, `PRE-FORK`…)*, quindi l'elenco `ESCLUSI` vale
**~80-90 decisioni una tantum**. Stimato: **`~250-320` voci**, **`~7-10 h`** in 6-8 passi, di cui
**`3-5 h` di REVISIONE A MANO**. **Quella parte non la comprimo:** comprimerla vorrebbe dire
produrre trecento campi «plausibili», cioe' **il difetto di oggi moltiplicato per trecento**.

**④ NIENTE E' A META', E NIENTE VA BUTTATO.** Il generatore e' **finito e collaudato `2/2`**
*(`f4bc082`)*. Della sua materia: **la lettura delle cinque fonti diventa l'IMPORTATORE**; il
**collaudo resta identico** *(collauda una vista, e le viste restano)*; **le 15 voci di Luca restano
il criterio bloccante**, e diventano il controllo di completezza della migrazione; **`REG_FAM` — le
famiglie per parola chiave — MUORE, e deve morire**: e' il pezzo piu' debole, e sopravvive solo per
**proporre** una famiglia da rivedere a mano. **L'unico pezzo nuovo di macchina e' lo sweep.**

## ⛔ **E MI FERMO QUI: non ho creato nessun `.yaml`.** Il criterio di chiusura della voce e' la
scelta di Luca fra **(a)** un file per voce, **(b)** un `difetti.yaml` unico, **(c)** no / non ora.


---

# ✅ **`PASSO 1` DELL'INDICE: LE COLLISIONI DI ID SONO CHIUSE** *(2026-09-26)*

*(`csv/_collisioni_id.py`, `csv/_rinomina_collisioni.py`; referti `doc/COLLISIONI_ID.txt` e
`doc/RINOMINE_ID.txt`. **Collaudo 4/4.**)*

## 📉 **DA 60 COLLISIONI APPARENTI A 15 VERE, E POI A ZERO**

```
primo giro     294 collisioni su 317 ID   <- un numero che non significa niente
poi             60                        <- tolte le VISTE (`LISTA_CHIUSA`) e le etichette LOCALI
poi             15                        <- tolti i RIMANDI (37 righe) e COMPONENTI_PROMOSSE
dopo la rinomina 0                        <- 23 voci rinominate, collaudo 4/4
```

**TRE CLASSI DI FALSA COLLISIONE, e ciascuna e' una distinzione che serve anche all'indice:**

- **le VISTE GENERATE** — `doc/LISTA_CHIUSA.md` ricopia ogni voce dei registri, quindi **duplica per
  costruzione**. Non definisce niente.
- **le etichette LOCALI** — in `REGISTRO_FISICA` `V8`, `A1`, `P2` sono **i criteri di UN sigillo** o
  **i punti di verifica di UNA scheda**: il nome pieno e' *«`V8` della scheda `freno-legge`»*. In
  `COMPONENTI_PROMOSSE` `A1`-`A8` sono le **ragioni** di una promozione, `B1`-`B10` i **flag**
  candidati. **Si citano sempre qualificate**, e nell'indice vanno col **namespace**
  (`COMPONENTI:B9`), **che disambigua senza toccare il documento**.
- **i RIMANDI** — `STATO_RUN` ha una tabella **generata** con l'esito di ogni voce `CODICE` di
  `RAMIFICAZIONI`: i suoi **37** `Zxx` **citano, non definiscono**. Senza questa distinzione la
  regola avrebbe **rinominato un rimando**, cioe' rotto il collegamento fra i due registri.

## ❌❌ **E DUE DIFETTI MIEI, di cui uno avrebbe corrotto gli assiomi**

**① L'ORDINAMENTO GUARDAVA `kv[0][0]`, cioe' LA PRIMA LETTERA del nome del registro**, non il
registro: il confronto con `("ASSIOMI", ...)` era **sempre falso** e il peso **sempre 0**. Gli
assiomi risultavano *«tengono il nome»* **per l'ordine di lettura dei file, non per la regola**.
> ### **Una regola che sembra funzionare per la ragione sbagliata e' peggio di una regola assente:**
> ### bastava cambiare l'ordine di `GLOBALI` per rinominare `A1`, `A3`, `A11`.

**② LA RINOMINA NON ERA IDEMPOTENTE:** `\bA1\b` trova `A1` **dentro** `A1-INERZIA` *(il trattino e'
un confine di parola)*, quindi **la seconda passata avrebbe scritto `A1-INERZIA-INERZIA`**. Un
difetto che **si vede solo al secondo giro**.

## ⚠ **E UNA DECISIONE DI MERITO CHE LA REGOLA NUDA NON PRENDEVA: LE SERIE**

Le voci stanno in **serie** — le cinque **cure** `C1`-`C5`, le dieci **aperte** `B1`-`B10`, le sei
**lasciate a meta'** `A1`-`A6` — e **rinominare un solo membro e' peggio della collisione**, perche'
rompe la leggibilita' della serie.

> ### Percio' **`RAMIFICAZIONI` tiene TUTTA la serie `C1`-`C28`** *(28 voci, e `C7`/`C10`/`C11`/
> ### `C12`/`C13`/`C14`/`C18`/`C21` sono citate in `CLAUDE.md`)*, e sono **le cinque cure della coda**
> ### a prendere il nome esplicito. Viceversa `RAMIFICAZIONI` rinomina **tutta** la sua `A1`-`A3` e
> ### `B4`-`B7`, che sono serie **complete**.

**E il conteggio per registro E' UN PROXY SBAGLIATO per gli assiomi:** `A1` vale `ASSIOMI` **8**
contro `RAMIFICAZIONI` **23**, ma un assioma e' citato **per nome nudo** in `CLAUDE.md` e in ogni
referto, e quelle citazioni **non si attribuiscono a nessun registro**. **Il genere viene prima del
numero: un assioma non si rinomina mai.**

## ✅ IL COLLAUDO, NEI DUE VERSI

```
(a) collisioni residue nei registri globali           0          PASS
(b) file NON TOCCABILI con sha1 cambiato              0 su 1029  PASS   (task history, referti,
                                                                        json, ogni .py, gli
                                                                        archivi dei sigilli)
(c) un'ancora inesistente FA FALLIRE l'assert         si'        PASS   <- il ramo che deve fallire
(d) file modificati fuori dall'elenco permesso        0          PASS
```

## ⚠ **COSA LA RINOMINA NON FA, e non e' un'omissione**

**Non riscrive le CITAZIONI in prosa.** Una `A3` in prosa **non dice** a quale voce si riferisce, e
in `STATO_RUN` ce ne sono che citano **l'assioma**: riscriverle tutte **corromperebbe le citazioni
degli assiomi**. Si risolvono con l'**`alias`** dell'indice (`PASSO 2`).
**E nei reperti il nome vecchio RESTA** — task history, referti, json, codice — **ed e' giusto: un
reperto non si riscrive.**

**Effetto collaterale misurato:** le voci lette da `STATO_RUN` passano da **246** a **247**, perche'
`C1-bis` — che prima si confondeva con `C1` — **e' ora una voce distinta**.


---

# ✅ **`PASSO 2`: `doc/INDICE_ID.tsv` — 663 VOCI, E UN PRESIDIO CHE IMPEDISCE** *(2026-09-26)*

*(`csv/_indice_id.py`, `csv/_presidio_indice.py`; referti `doc/INDICE_ID_referto.txt` e
`doc/COLLAUDO_presidio_indice.txt`. **Collaudo 5/5**, e il quinto e' il **hook vero**.)*

```
voci nell'indice                 663        esclusi (non sono ID)        38
per STATO       da-decidere 466   chiuso 122   aperto 47   teoria 17   non-difetto 11
per TIPO        altro 225   criterio-locale 203   fronte 141   misura 28   difetto 25
                assioma 16   cura 14   presidio 10   standard 1
per BLOCCA      DA-DECIDERE 511   NO 147   SI 5
```

## 📌 **I NUMERI SCOMODI LI DICO PRIMA: `466` `da-decidere` e `511` `DA-DECIDERE`**

**Non e' pigrizia, ed e' l'ordine di Luca** *(«lo stato si prende dalla fonte; dove e' ambiguo
`da-decidere`. Non indovinare»)*: `blocca_run_base` vale `SI` **solo** dove il testo dice
*«bloccante»* o *«prima di qualunque giro lungo»* — **sono cinque voci** — e `NO` dove la voce e'
chiusa, e' teoria o non e' un difetto.

> ### **Riempire quella colonna a intuito sarebbe il difetto di oggi moltiplicato per cinquecento.**

## ✅ **DUE LACUNE CHIUSE CLASSIFICANDO, NON ESCLUDENDO**

**① `CLAUDE.md` DEFINISCE I PRESIDI, e l'indice non lo leggeva:** `P6` risultava *«citato 59 volte
e mai definito»*. **Un registro che si legge per primo e che l'indice non guarda e' esattamente il
difetto che l'indice deve togliere.** *(E in `CLAUDE.md` i presidi si aprono in **grassetto**, non
con un'intestazione: senza quel ramo `P1`-`P6` non esistevano.)*

**② I `288` «CITATI E MAI DEFINITI» NON SONO VOCI PERSE:** **119** sono citati **solo** in referti,
sigilli e task history, e sono **etichette di CRITERIO di quel sigillo** (`T1`, `S1`, `R3`, `K3`) —
il loro nome pieno include il sigillo. **Entrano con `tipo: criterio-locale`**, e la
classificazione viene da **DOVE sono citati**, che e' un dato e non un giudizio. **Chiamarli
`altro` li avrebbe nascosti fra le voci vere.**

## ✅ **IL PRESIDIO: TRE ESITI, NON DUE**

```
NOTO       l'ID e' nell'indice come `id` o come `alias`                    -> passa
ESCLUSO    e' fra le 38 forme dichiarate NON identificatori, col motivo    -> passa
AMBIGUO    forma NUDA di un ID con namespace, definita da DUE registri     -> AVVISA e RIFIUTA
IGNOTO     non e' in nessuno dei due                                       -> RIFIUTA
```

**L'`AMBIGUO` e' il servizio vero:** se una forma nuda e' definita in due posti, **il presidio lo
dice** invece di scegliere per conto proprio. *(Oggi sono zero, e lo dico: lo `AMBIGUO` e' un ramo
**non ancora esercitato sui dati veri**, provato solo per costruzione.)*

**COLLAUDO `5/5`, e il quinto conta piu' degli altri quattro:** i primi provano **la funzione**; il
quinto mette una riga con `QQ777` in un documento vivo, la mette in **stage** e chiama il **HOOK
VERO** — `uscita 1`, ID segnalato, **e il documento torna con lo stesso sha1**. *(Fra la funzione e
il hook c'e' `git diff --cached`, ed e' la' che un presidio si spegne in silenzio.)*

**E GUARDA SOLO LE RIGHE AGGIUNTE, dichiarato:** guardare i file interi rifiuterebbe **ogni** commit
finche' l'indice non e' perfetto, e **verrebbe aggirato il primo giorno** (`A9`). Cosi' **il debito
vecchio resta visibile nell'indice e il debito NUOVO non si crea**.

## ⚠ **TRE LIMITI, dichiarati**

- **la forma estratta puo' essere un SOTTOINSIEME del token scritto:** `ZZ888` viene segnalato come
  `Z888`. **Il presidio rifiuta comunque**, ma il nome nel messaggio d'errore puo' non coincidere
  con quello scritto.
- **`titolo_breve` e' troncato a 110 caratteri:** l'indice dice **dove** vive una voce, non che cosa
  dice. La spiegazione resta nel documento.
- **la fonte e' `file::ancora`, non `file:riga`:** un numero di riga **marcisce al primo
  inserimento**, un frammento di titolo si trova con una ricerca.


---

# 📏 **`PASSO 3`: L'INVENTARIO E' FATTO, LA STIMA RADDOPPIA. NON L'HO COMINCIATO**
*(2026-09-26, come chiesto da Luca: «se il `PASSO 3` allunga troppo la stima, dimmelo prima di
cominciarlo»)*

*(`csv/_inventario_lettori_id.py` -> `doc/INVENTARIO_lettori_id.txt`. **Nessuna riscrittura
cominciata.**)*

## ⚠ **«81 SCRIPT NOMINANO UN REGISTRO» NON ERA IL PERIMETRO**

```
script che nominano un registro       83
   copia-simulatore                   33   REPERTI da 7000-10500 righe: lo nominano in un COMMENTO
   scrittore-una-volta                21   `_zNNN_*.py`: hanno AGGIUNTO una voce, hanno gia' girato
   IMPORTATORE                         3   costruiscono l'indice: DEVONO leggere il Markdown
   LETTORE                            26   di cui **10** aprono davvero un registro  <- IL PERIMETRO
```

**I DIECI:** `_lista_chiusa` *(592 righe)*, `_cure_verificate` *(352)*, `_quadro_unico` *(313)*,
`_triage_difetti` *(302)*, `_inventario_passo` *(269)*, `_presidio_indice` *(240, e legge GIA'
l'indice)*, `_punto_della_situazione` *(162)*, `_stato_run` *(123, scrive il registro dei run)*,
`_collaudo_lista_chiusa` *(112)*, `_blob_nelle_voci` *(87)*.
**Da riscrivere davvero: SETTE-OTTO.**

## ❌ **E L'EURISTICA DELL'INVENTARIO SBAGLIAVA IL PERIMETRO, alla prima stesura**

Cercava il nome del registro **accanto** a un `open(`, e perdeva il caso **normale**:
`CODA = os.path.join(RADICE, "doc", "STATO_RUN.md")` e poi `io.open(CODA)`.
**Perdeva `_triage_difetti.py` e `_punto_della_situazione.py`: due lettori VERI**, cioe' proprio il
perimetro. **Da `6` a `10`.** *(Un inventario che sbaglia il perimetro fa sbagliare la stima, ed e'
peggio di un inventario assente.)*

## 💰 **LA STIMA: `4-6 h`, cioe' il DOPPIO dei passi 1 e 2 insieme**

```
i passi 1 e 2, fatti          ~3 h    (stima data prima: 2,5-3 h -- ci siamo stati)
il PASSO 3, stimato
   7-8 strumenti x (riscrittura + collaudo nei DUE versi)   ~25-40 min l'uno   = 3,5-5 h
   di cui `_lista_chiusa.py`: 592 righe il cui DISEGNO INTERO e' parsing di
   Markdown -> non e' una modifica, e' una RISCRITTURA                        = 1-1,5 h
```

> ### **Risposta alla domanda di Luca: SI', allunga la stima, e non di poco: la RADDOPPIA.**
> ### **Non l'ho cominciato.**

## ⚠ **E DUE DECISIONI CHE CAMBIANO IL COSTO, prima di cominciare**

**① L'INDICE NON HA LA COLONNA `famiglia`, E `LISTA_CHIUSA` LA USA.** L'indice porta `id`, `alias`,
`titolo_breve` *(troncato a 110 caratteri)*, `fonte`, `stato`, `blocca_run_base`, `tipo` — **le
sette colonne che Luca ha elencato**. Ma la lista chiusa raggruppa **per famiglia `A`-`G`** e stampa
**la riga intera** della voce. Quindi, una di queste tre:
```
(a) l'indice guadagna `famiglia` (e forse `testo`)   -> l'indice cresce, la vista resta ricca
(b) la vista diventa SOTTILE (id, titolo, stato, tipo) -> si perde il testo delle voci
(c) la vista continua a leggere i registri PER IL TESTO -> contraddice la regola del PASSO 3
```
**La decido io solo se Luca non decide: e allora prendo (a)**, perche' e' l'unica che non perde
informazione e non contraddice la regola.

**② GLI IMPORTATORI RESTANO A LEGGERE IL MARKDOWN, per necessita':** `_indice_id`,
`_collisioni_id`, `_rinomina_collisioni` **sono cio' che COSTRUISCE l'indice**. La regola *«nessuno
strumento deve piu' fare parsing delle tabelle Markdown»* vale per i **CONSUMATORI**. **Lo scrivo
perche' e' una precisazione di merito, non un'eccezione che mi concedo.**

## ❌❌ **E UN DIFETTO DEL MIO COMMIT PRECEDENTE, trovato dal warning di git**

**`.gitattributes` non copriva `*.tsv`**, quindi `doc/INDICE_ID.tsv` sarebbe stato riscritto in
**CRLF** al prossimo checkout — e il presidio lo legge con `newline=""`, quindi **l'ultima colonna
(`tipo`) si sarebbe portata dietro un `\r`**. Aggiunto `*.tsv text eol=lf`.
**Non e' un'ipotesi: `git` l'ha detto in chiaro** *(«LF will be replaced by CRLF»)* **nel commit
`a6e105c`, e l'ho visto perche' l'avviso era nell'output.** È la **trappola CRLF del par.5-quinquies**
in veste nuova: **un file nuovo con un'estensione nuova non e' coperto da una regola scritta per le
estensioni vecchie.**


---

# ❌❌ **DUE DIFETTI DEL PRESIDIO DELL'INDICE, TROVATI DAL PRESIDIO STESSO** *(2026-09-26)*

**Li relaziono a parte perche' sono arrivati DOPO il messaggio del commit `42942cc`**, e un riscontro
fuori dal repo non esiste *(par.5-ter)*.

## ① **IL PRESIDIO HA BLOCCATO IL MIO COMMIT, E AVEVA RAGIONE**

```
[INDICE] *** COMMIT RIFIUTATO ***
  ID citati nel MESSAGGIO e non nell'indice: SETTE-OTTO
```

`SETTE-OTTO` e' un **numerale a parole**, non un ID — ma **ha la forma di un ID**, e il presidio non
puo' saperlo. **L'ho chiuso classificando, non con l'eccezione:** i numerali a parole
*(`UNO`…`MILLE`, in testa o in coda)* sono ora fra gli **ESCLUSI col motivo**, e l'elenco passa da
**39** a **41** forme.

> ### **La via d'uscita `[SENZA-INDICE: ...]` c'era, ed e' il punto: NON l'ho usata.** Un'eccezione
> ### avrebbe fatto passare quel commit e lasciato il difetto per il prossimo.

## ② **L'INDICE SI NUTRIVA DEI PROPRI OUTPUT, E IL COLLAUDO SI AUTOCONFERMAVA**

**Misurato:** dopo la prima rigenerazione, il collaudo dava **`FAIL`** su **entrambi** i casi che
devono fallire:

```
DEVE FALLIRE  un ID inventato: `ZZ999`                 -> passa    FAIL
DEVE FALLIRE  un difetto plausibile ma assente: `D97`  -> passa    FAIL
```

**Perche':** il referto del collaudo **stampa** `ZZ999` e `D97`; lo sweep dell'indice legge **tutti**
i `.txt` di `doc/`, quindi li trovava, li metteva nell'indice come *«citati e mai definiti»*, e al
giro successivo **erano ID noti**.

> ### **Uno strumento che si nutre dei propri output si AUTOCONFERMA.** E' la stessa famiglia del
> ### criterio auto-referenziale di stamattina *(la soglia calcolata dai dati che deve giudicare)*,
> ### in veste di **circolarita' fra un indice e il suo collaudo**.

**Cura:** lo sweep **salta i cinque file che sono output di questa stessa macchina**
*(`INDICE_ID*`, `COLLISIONI_ID`, `RINOMINE_ID`, `COLLAUDO_presidio_indice`,
`INVENTARIO_lettori_id`)*, e **il referto lo dichiara col conteggio**. Dopo la cura: **`5/5 PASS`**,
end-to-end incluso.

**⚠ E IL COLLAUDO SI ERA DICHIARATO INCOMPLETO, invece di dare per buono un ramo non provato:**
*«END-TO-END NON ESEGUITO: c'erano modifiche in STAGE, e non le tocco»*. **E' quella riga che mi ha
fatto rigirare il collaudo ad albero pulito.**


---

# ✅ **`PASSO 3` RIDOTTO: LA LISTA CHIUSA LEGGE L'INDICE, E TRE DIFETTI DELLA FORMA DEGLI ID**
*(2026-09-26)*

## ✅ **LE DUE CORREZIONI DI LUCA ALL'INDICE**

**① `blocca_run_base` PER PAROLA CHIAVE ERA SBAGLIATO.** `Z25`, `Z29` e `Z73` uscivano
`non-difetto` **e** `SI` insieme — `Z73` perche' il suo testo dice *«BLOCCA LA MITOSI»*, che parla
della **mitosi**, non del run base.
> ### **Una parola che compare nel racconto di un riscontro non e' una dichiarazione sul run base.**
**Regola nuova:** un `non-difetto`, un `chiuso`, una `teoria` o un `criterio-locale` **non bloccano
MAI** → `NO`, e vince sulla parola chiave. **`blocca SI` passa da `5` a `2`; `NO` da `147` a `404`.**
**Controllo di Luca: `0` righe con stato chiuso/non-difetto/teoria e `blocca SI` — `PASS`.**

**② LO SMISTAMENTO SI LIMITA A CHI PUO' BLOCCARE.** `doc/SMISTAMENTO_run_base.md`, **generato**:
solo tipo `difetto`/`fronte`/`misura`/`cura` **e** stato `aperto`/`da-decidere` → **103 voci**, con
`id`, **un titolo di UNA riga leggibile** e la fonte, **ordinate per famiglia**
*(`A` 39, `F` 26, `B` 9, `C` 8, `E` 7, `D` 3, `G` 2, `?` 9)*.
**`SI`/`NO` NON sono riempiti a intuito: la lista e' la base su cui decide Luca.**

## 🔄 **LA VISTA NON FA PIU' PARSING: CONTEGGI PRIMA / DOPO**

```
                        PRIMA (parser su 5 fonti)      DOPO (vista sull'indice)
voci                    625                            736
in LISTA                406                            333
FUORI LISTA             219                            403   (col motivo, dai CAMPI)
sezioni fuori portata    48                              0   (non esistono piu': non legge documenti)
senza famiglia          111                            190   (la famiglia viene dall'indice)
voci PERSE                -                              2   DICHIARATE
```

**Il testo si accorcia da `420` a `117` caratteri** *(Luca ha scelto `famiglia`, non `testo`)*: la
spiegazione sta **nella fonte, che e' in colonna**.

## ⚠ **LE DUE VOCI PERSE, dichiarate PRIMA dei numeri**

**Nell'indice entrano solo le voci CON UN ID.** Non ne hanno:
- **il `tasso di mitosi`** — un punto di `COSA NON SO DERIVARE` della scheda ⑨: **una voce di
  elenco in prosa senza etichetta**;
- **`CURA 3`** — l'etichetta e' `CURA 3` **con lo SPAZIO**, e uno spazio non fa un identificatore.
  **Basterebbe `CURA-3`: e' una rinomina, e la decide Luca.**

**E TRE compaiono solo attraverso l'ID che le contiene**, dichiarato nel codice: la **soglia `3π`**
→ `D36`; **`chi comprime d0`** → `CONFIG-1`; **i 24 script** → `PASSO-1`.
**Se l'elenco delle perse cresce, il generatore SI FERMA.**

## ❌❌ **TRE DIFETTI DELLA FORMA DEGLI ID, e il terzo era grave**

```
① lo STEM era tagliato a CINQUE caratteri   -> CONFIG-1, POTENZE-1, ANCORE-1, INERZIA-1(C),
   `[A-Z][A-Za-z0-9]{0,4}`                      RIPRESA-ARGV, REPERTI-IMMUTABILI risultavano
                                                «CITATI e MAI DEFINITI». `SCALE-TW` passava solo
                                                perche' `SCALE` ha esattamente cinque lettere:
                                                **il difetto era invisibile per un carattere.**
② lo STEM chiedeva TRE caratteri col trattino -> `A3-DISEGNO` (nato dalla rinomina del PASSO 1)
                                                NON era un ID. **Gli alias delle rinomine erano
                                                2 su 23**: una citazione del nome vecchio sarebbe
                                                stata RIFIUTATA dal presidio.
③ le cifre IN CODA non erano previste         -> `FRAG1` non esisteva per la macchina degli ID.
```

**① e ③ li ha trovati il COLLAUDO della vista** *(`A3-DISEGNO` e `FRAG1` mancanti)*, **ed e' il
motivo per cui il collaudo si scrive prima.** Dopo la cura: **indice da `666` a `736` voci**, **alias
delle rinomine da `2` a `23`**.

**⚠ E UNA CLASSE RESTA FUORI, dichiarata:** un'etichetta di **UNA SOLA PAROLA MAIUSCOLA** senza
cifre ne' trattino — **`CONTAGIO`** — **non e' un ID in questo spazio**: e' la specifica di Luca
*(«nomi MAIUSCOLI col trattino»)*, e allargare la regex vorrebbe dire **prendere ogni parola
maiuscola della prosa**. **Quelle voci hanno bisogno di un ID, non di una regex piu' larga.**

## ❌ **E DUE DIFETTI MIEI DI STRUMENTO, entrambi visti dai numeri**

- **il filtro dell'enumerazione era troppo largo:** cercavo un `·` **in qualunque punto**
  dell'etichetta, e il `·` sta anche dentro `[EPOCA 1 · CODICE]`, che e' in **ogni** riga di
  `RAMIFICAZIONI`. **Le definizioni crollavano da `291` a `130` e i `fronte` da `141` a `8`.**
  **Un filtro troppo largo svuota un indice in silenzio.** Ora il test si fa **subito dopo l'ID**.
- **il collaudo della vista iniettava una tupla di DUE campi** in un elenco che ora ne ha **tre**:
  la copia truccata si schiantava in `ValueError` — uscita `1` invece di `3` — e il collaudo dava
  **`FAIL` per la ragione sbagliata**.

## ✅ **LO STATO DEI COLLAUDI, tutti rigirati**

```
la vista (`_collaudo_lista_chiusa`)        2/2 PASS   (il ramo che deve fallire NON scrive il file)
il presidio dell'indice                   5/5 PASS   (hook vero incluso, sentinella a run time)
i presidi del pre-commit (`_hook_presidi`) 8/8 OK
le collisioni                             0 su 291 ID definiti
```

## 📌 **E LA VOCE `LETTORI-INDICE` E' IN CODA** *(ordine di Luca)*

I **sei** lettori che leggono ancora il Markdown — `_cure_verificate`, `_quadro_unico`,
`_triage_difetti`, `_inventario_passo`, `_punto_della_situazione`, `_blob_nelle_voci` — stanno
nell'indice come **una voce**, `stato: aperto`, **`blocca_run_base: NO`** *(la fonte lo dichiara:
«NON BLOCCA il run base»)*, famiglia `G`. **Gli importatori restano a leggere il Markdown per
necessita': sono cio' che costruisce l'indice.**


---

# ❌❌ **DUE CURE ARRIVATE DOPO IL COMMIT `4a76517`, e le ha chieste il presidio** *(2026-09-26)*

**Il `pre-commit` ha bloccato il commit del `PASSO 3` su due ID:** `CURA-3` e **`GLOBALE-DIS`**.

## ① **`GLOBALE-DIS` NON ESISTE: L'HO INVENTATO IO TRONCANDO**

Il titolo di una voce veniva tagliato a **117 caratteri** *(e a 111 nell'indice)* **a meta' parola**:
`GLOBALE-DISEGNO §4` diventava **`GLOBALE-DIS`**.

> ### **Un troncamento che taglia a meta' parola INVENTA UN ID**, e il presidio — giustamente — lo
> ### segnalava come sconosciuto **in un documento che questa stessa macchina aveva scritto.**

**Cura:** si tronca **su un confine di parola** *(`_taglia`, nell'indice e nella vista)*.
**⚠ E il difetto si e' manifestato due volte in dieci minuti:** la prima patch di `_taglia` **non e'
stata scritta su disco** *(lo script si e' fermato su un'ancora sbagliata prima della `write`)*,
mentre la patch che la **chiamava** era passata: il generatore girava con un `NameError`.
**Un patch script che scrive alla fine lascia il file COERENTE o INTATTO; se le patch sono due
script diversi, quella garanzia non c'e' piu'.**

## ② **LA VIA D'USCITA VALEVA SOLO NEL `commit-msg`, CIOE' TROPPO TARDI**

`[SENZA-INDICE: <motivo>]` viene letto dal hook `commit-msg` — ma **il `pre-commit` gira PRIMA**, e
rifiutava senza nemmeno leggere l'eccezione. **Con `git commit -F` il messaggio e' gia' in
`.git/COMMIT_EDITMSG`**: il `pre-commit` ora lo legge come ripiego, e la via d'uscita funziona **a
entrambi gli stadi**.

> ### **Una via d'uscita che non si puo' imboccare non e' una via d'uscita**: e' un blocco con una
> ### promessa scritta accanto.

**Collaudi rigirati dopo le due cure:** vista **`2/2`**, presidio dell'indice **`4/4`** *(l'end-to-end
si e' dichiarato NON eseguito: c'erano modifiche in stage — e lo dice invece di darlo per buono)*,
presidi del pre-commit **`8/8`**.


---

# 🧊 **LISTA CHIUSA CONGELATA — 4 condizioni su 4, e un difetto GRAVE del presidio trovato dal
suo collaudo** *(2026-09-26)*

## ✅ LE CONDIZIONI DI FINE, verificate DA SCRIPT

```
(1) voci DA-DECIDERE nello smistamento ..............   0   PASS
(2) contraddizioni stato/blocca .....................   0   PASS
(3) voci NOMINATE dal mandato e assenti dall'indice ..   0   PASS
(4) STATO_RUN allineato: D11 "chiuso"   D09 "aperto" (di proposito)
```

```
indice            741 voci      blocca: SI 8   NO 520   DA-DECIDERE 212   DA VERIFICARE 1
smistamento       139 voci      0 DA-DECIDERE
lista chiusa      352 in lista  389 fuori col motivo   0 voci PERSE
collaudi          vista 2/2 - presidio indice 5/5 - hook 8/8 - collisioni 0 su 322
```

**`SI` sono ESATTAMENTE le otto del mandato:** `DRIVER-SCENA-II`, `OSSERVABILE-P1`, `D02`, `D31`,
`U1`, `CLI-1`, `SCALE-TW`, `D03`.

## ⚠ **UNA VOCE NON TORNA, E NON L'HO FORZATA: `D09`**

Il mandato la dava per **CHIUSA** *(«smentito da `Z73` stesso: 4651 nati nel run lungo»)*.
**Il numero `4651` NON E' NEL REPO** — cercato in tutti i `.md`, `.txt` e `.py` tracciati — e la riga
di `Z73` in `RAMIFICAZIONI` e' ancora **`DA RIVERIFICARE`** e dice che `chi_basc` **BLOCCA** la
mitosi. **Resta `aperto`, con `blocca = DA VERIFICARE` e il motivo stampato nello smistamento.**
*(Le altre prove le ho verificate sul disco: `pozzo_grafo` usa `self.pos` a `:6541` ✅; `_smorza`
smorza **solo la discesa** ✅; `01eda44` e' la cura di `Z87` ✅; le quattro righe di
`DRIVER-SCENA-II` — `:223`, `:328`, `:7187`, `:8681` — ✅.)*

## ❌❌ **IL DIFETTO GRAVE, e l'ha trovato il collaudo end-to-end**

Avevo fatto leggere al `pre-commit` il file `.git/COMMIT_EDITMSG` per poter honorare
`[SENZA-INDICE: ...]` anche la'.

> ### **Git scrive `COMMIT_EDITMSG` DOPO il `pre-commit`** *(l'ordine e' `pre-commit` →
> ### `prepare-commit-msg` → `commit-msg`)*: **leggevo il messaggio del commit PRECEDENTE.**
> ### **Un solo commit con un'eccezione dichiarata avrebbe spento il presidio per tutti i commit
> ### successivi**, fino al cambio di quel file.

**Cura:** il controllo dell'indice vive in **UN solo stadio, `commit-msg`**, dove il messaggio
**esiste** — e guarda **le righe aggiunte ai documenti vivi PIU' il messaggio**. Il `pre-commit` non
lo chiama piu'. **Il ramo end-to-end del collaudo e' l'unico che poteva vederlo**, perche' fra la
funzione e il hook c'e' git.

## ❌ **E CINQUE DIFETTI DELLE CORREZIONI, tutti visti dai NUMERI**

```
① le DECISIONI si applicavano DOPO la scrittura del TSV      -> l'indice restava DA-DECIDERE su
                                                                 D02, D03, D14, D15, SCALE-TW:
                                                                 **la decisione c'era e l'indice
                                                                 non la portava**
② le frasi di chiusura pescavano nelle celle DI MEZZO        -> CLI-1 «chiusa» da «7/7 e 8/8
   (dove stanno le PROVE, che citano i sigilli di ALTRE voci)    restano validi», D31 da «4/4:
                                                                 deriva», RAMPA-2 da «RAMPA-1 ne ha
                                                                 curata UNA»: **tre voci aperte
                                                                 chiuse dal sigillo di qualcun
                                                                 altro**
③ `D31` era `tipo: altro` per la TABELLA SPEZZATA            -> una delle otto voci `SI` **fuori
                                                                 dallo smistamento**
④ la parola chiave batteva la regola                         -> Z21, Z25, Z29 uscivano `SI` pur
                                                                 essendo fronti «vale per quella
                                                                 scena»: ora **la regola vince**
⑤ in un mio patch script `\b` e' diventato un BACKSPACE       -> quattro criteri del collaudo
   (0x08) invece di un confine di parola                         cercavano `\x08D02\x08`: **sempre
                                                                 falsi**, e il collaudo diceva
                                                                 «MANCA» su voci presenti
```

**Il ⑤ e' il piu' istruttivo per me:** un criterio che non puo' mai essere vero **si comporta come
un criterio severo**. L'unica ragione per cui l'ho visto e' che **il generatore si FERMA** invece di
avvisare.

## 🧊 **DA QUI SI SPUNTA, NON SI RIGENERA**

Tag **`lista-chiusa-v1`**. L'ordine di lavoro degli otto `SI` e' in testa a
`doc/SMISTAMENTO_run_base.md`, con il **perche' dell'ordine** e una stima per voce
*(somma: `8,5-12,5 h`, senza il run e senza le decisioni)*.
**Il lavoro sui `SI` comincia solo col via di Luca.**


---

# ⛔ **PUNTO 5 (`LETTORI-INDICE`): NESSUNO DEI SEI SI CONVERTE COM'E'. RESTA APERTA.**
*(2026-09-26, `doc/LETTORI_INDICE_analisi.md`, generata)*

**Luca:** *«se uno ha bisogno di un campo che l'indice non ha, dimmelo invece di rileggere il
Markdown»*. **Vale per tutti e sei, e per TRE ragioni diverse.**

```
CONSUMATORE  _punto_della_situazione  162   manca `avanzamento` (IN CORSO / IN CODA / FATTO):
                                            l'indice ha `stato`, che NON distingue IN CORSO da
                                            IN CODA -- ed e' la distinzione che quel documento serve
CONSUMATORE  _triage_difetti          302   mancano `classe` (CODICE/MISURA/PROVA) e `esito`
GENERATORE   _cure_verificate         352   legge il CODICE e SCRIVE dentro STATO_RUN
GENERATORE   _quadro_unico            313   legge il CODICE e il DRIVER, e SCRIVE dentro STATO_RUN
PROSA        _blob_nelle_voci           87   il suo OGGETTO e' la prosa dei registri: convertirlo
                                            distruggerebbe cio' che misura
FUORI        _inventario_passo        269   legge gli script di `csv/`: non apre i tre registri
```

## 📌 **LA PROPOSTA MINIMA: TRE CAMPI, e due strumenti su sei si convertono**

- **`avanzamento`** — dal **primo marcatore della cella** *(e porta con se' il difetto gia' curato
  di quello strumento: conta il primo nel TESTO, non il primo di una lista)*;
- **`classe`** — dal tag `[EPOCA n · CLASSE]` delle righe di `RAMIFICAZIONI`, **che l'indice oggi
  BUTTA VIA** *(lo togliamo dal titolo per renderlo leggibile)*;
- **`esito`** — **non si ricava**: e' il triage stesso a produrlo. Servirebbe che il triage
  **SCRIVESSE** nell'indice invece di leggerlo, **e questo cambia il verso del flusso: lo decide
  Luca.**

## ⚠ **PERCHE' NON HO CHIUSO `LETTORI-INDICE`**

La condizione di fine e' *«nessun consumatore apre piu' i registri per TROVARE DIFETTI»*. **Per i
quattro fuori perimetro e' gia' vera oggi — ma per una ragione diversa da quella attesa: non li
aprono per quello.** Per i due consumatori **non e' vera**, e per renderla vera serve una decisione
sui tre campi. **Chiudere la voce adesso vorrebbe dire dichiarare finito un lavoro che dipende da te.**


---

# ⚠ **L'INDICE E' CAMBIATO DOPO IL TAG, ED E' UNA CURA DELLA MACCHINA — IL DELTA E' MISURATO**
*(2026-09-26)*

Il tag **`lista-chiusa-v1`** congela `7935806`. Subito dopo, il presidio ha rifiutato un commit su
**`LETTORI-INDICE)`** — **con la parentesi attaccata**: `()` sta nella forma degli ID per
`INERZIA-1(C)`, e cosi' una parentesi **della prosa** veniva letta come parte del nome.

**Cura:** le parentesi devono essere **BILANCIATE** *(se un token finisce con `)` e non contiene
`(`, la parentesi non e' sua)*.

**IL DELTA, misurato confrontando l'indice AL TAG con quello di adesso:**

```
al tag 741 voci      ora 740 voci
SPARITE (1):  `CLI-1)`        <- un token spurio: la parentesi della prosa
NUOVE   (0):  nessuna
```

> ### **Il congelamento regge:** non e' cambiata **nessuna** voce della lista. E' sparito **un
> ### token che non era un ID**, e con esso `LETTORI-INDICE)`. **«Da qui si spunta, non si
> ### rigenera» vale per il CONTENUTO; una cura della MACCHINA che toglie un fantasma non e' una
> ### rigenerazione della lista** — e lo dico col diff, non a parole.

**Le quattro condizioni di fine restano soddisfatte dopo la cura** *(`0`/`0`/`0` + `D11` chiuso)*, e
i collaudi pure *(presidio `4/4` senza end-to-end perche' c'erano modifiche in stage, vista `2/2`)*.


---

# ✅ **`LETTORI-INDICE` CHIUSA, e `D09` con lei** *(decisioni di Luca, 2026-09-26)*

## ① **`_triage_difetti` RITIRATO** *(`STANDARD 10`)*

Spostato in **`csv/_archivio/`** *(`git mv`, non cancellato)*: **lo smistamento dell'indice fa lo
stesso lavoro**, e una cura non aumenta il numero degli strumenti.

## ② **`_punto_della_situazione` CONVERTITO, e il campo `avanzamento` esiste**

**Legge soltanto `doc/INDICE_ID.tsv`.** Collaudo **5/5 nei due versi**, e il caso che deve fallire
e' quello vero: **`CONTAGIO` e' nel Markdown e NON nell'indice** *(un'etichetta di una parola sola
non e' un ID)* — **non compare, ed e' il prezzo dichiarato della fonte unica.**

**❌ E UN DIFETTO MIO, preso al primo giro:** calcolavo `avanzamento` da `stato_src`, che passa per
`_nudo()` — **e `_nudo()` cancella le emoji**. Cercavo `✅`/`▶`/`⏸` **dopo averli rimossi**: il campo
usciva `(senza marcatore)` su **740 voci su 740**.
> ### **Un campo vuoto travestito da campo pieno.** Se l'avessi solo guardato in tabella l'avrei
> ### creduto buono: l'ha denunciato il CONFRONTO prima/dopo, che mostrava `438` righe tutte uguali.

**IL CONFRONTO PRIMA/DOPO** *(`doc/LETTORI_INDICE_confronto.md`, generato; il PRIMA e' committato
come reperto)*:

```
gruppo               PRIMA   DOPO          task elencati   PRIMA 60   DOPO 95
(senza marcatore)       23      -  (filtrati e dichiarati)
CON RISERVA              3     43
FATTO                   17     31
IN CODA                 13      9
BLOCCATO                 -      5
DIFETTI E SOSPETTI      47     47
```

**TRE CLASSI DI DIFFERENZA, e due sono GUADAGNI:**
- **`+68` comparse** — il vecchio leggeva **solo `STATO_RUN`**, l'indice copre **tutti i registri**;
- **`-30` sparite perche' SENZA MARCATORE** — il vecchio lo prendeva dalla **quarta cella**, l'indice
  dalla **prima e dall'ultima**, che e' dove una riga dichiara **il proprio** stato. **Non allargo:**
  le celle di mezzo contengono **le prove**, che citano i `✅` di **altre** voci — ed e' il difetto
  che quello strumento aveva gia' curato una volta;
- **`-3` sparite perche' NON SONO ID** — e due erano **NOMI DI FILE** *(`_verifica_registro.py`,
  `doc/PATTERN_DI_PROVA.md`)*: **il vecchio parser le listava come task.**

## ③ **I QUATTRO FUORI PERIMETRO, dichiarati nella voce**

`_cure_verificate` e `_quadro_unico` leggono **il CODICE** e aprono `STATO_RUN` **per SCRIVERCI**;
`_blob_nelle_voci` ha per **oggetto la PROSA**; `_inventario_passo` legge **gli script**. **Nessuno
dei quattro apre un registro per TROVARE DIFETTI**, che e' la condizione di fine.

## ④ **`D09` CHIUSO, e la lezione e' mia: `STANDARD 9` vale anche per `git log`**

La smentita **c'era**, nel **messaggio** del commit **`48a3555`**:
> *«Z73 CORRETTA IN LOCO, RITIRATA UNA SECONDA VOLTA: `chi_basc` NON BLOCCA LA MITOSI. Il ramo A gira
> CON `chi_basc` acceso ed e' andato **da 2672 a 7323 nodi, 4651 nati in 1560 passi**»*.

**Io avevo cercato `4651` nei soli file tracciati** e avevo concluso *«non e' nel repo»*.
> ### **`STANDARD 9` — non si deduce l'assenza da una ricerca parziale — VALE ANCHE PER `git log`.**
> ### **Un messaggio di commit E' il repo.** E' la stessa forma dell'errore che avevo appena curato
> ### *(cinque fonti invece di una)*, ripetuta su un'altra superficie: **i file non sono tutto.**

`Z73` ora porta **`RITIRATA`** con la frase e il commit; `D09` e' **`NON E' UN DIFETTO`**, `blocca NO`.
**La misura di partenza era su 60 passi e un seme: era CORTA, non sbagliata.**


---

# 📐 **IL DELTA RISPETTO AL TAG, E LA VERIFICA DELLA CONDIZIONE DI FINE** *(2026-09-26)*

## ✅ IL DELTA, col diff — e sono ESATTAMENTE le tre decisioni di questo mandato

```
colonne   al tag  9  ->  ora 10      nuova: `avanzamento`
voci      al tag 741 ->  ora 740     SPARITE 1: `CLI-1)` (il token spurio della parentesi)
                                     NUOVE   0
campi cambiati (3):
   D09              stato aperto -> non-difetto      blocca DA VERIFICARE -> NO
   Z73              stato aperto -> non-difetto      blocca NO -> NO
   LETTORI-INDICE   stato aperto -> chiuso           blocca NO -> NO
```

> ### **Nessun'altra voce si e' mossa.** Il congelamento tiene: cio' che e' cambiato e' **quello che
> ### Luca ha deciso**, piu' una colonna nuova e un fantasma in meno.

## ⚠ **LA CONDIZIONE DI FINE: verificata, ma il conteggio GREZZO SALE, e va spiegato**

`csv/_inventario_lettori_id.py` rigirato: i **LETTORI che aprono davvero un registro** passano da
**10** a **11**. **Non e' una regressione, e non lo dico per rassicurare: lo dico con l'elenco.**

```
_archivio/_triage_difetti.py   RITIRATO: e' in archivio, non gira piu'
_punto_della_situazione.py     apre STATO_RUN **nel COLLAUDO**, per provare che `CONTAGIO` --
                               che vive nel Markdown e NON nell'indice -- **non passa**
_analisi_lettori_indice.py     NUOVO: nomina i registri perche' il suo mestiere e' dire CHI li apre
_confronto_pds.py              NUOVO: confronta due output, non cerca difetti
_lista_chiusa / _presidio_indice / _collaudo_lista_chiusa   nominano `LISTA_CHIUSA` e i registri
                               come ELENCO DI FONTI, non li aprono per trovare difetti
_cure_verificate / _quadro_unico   GENERATORI: leggono il CODICE e SCRIVONO in `STATO_RUN`
_blob_nelle_voci               ha per OGGETTO la prosa dei registri
_inventario_passo / _stato_run  fuori perimetro (script e registro dei run)
```

> ### **IL LIMITE E' DELLA VERIFICA, non del lavoro:** l'inventario **non puo' distinguere «apre per
> ### TROVARE DIFETTI» da «nomina un registro»** — e' un'euristica sul sorgente. **La condizione di
> ### fine, come Luca l'ha scritta, e' soddisfatta; il numero grezzo no, e i due fatti convivono.**
> ### Chiamare «11 → 0» quello che l'euristica non sa misurare sarebbe un timbro falso.

**Cio' che si potrebbe fare, e non faccio ora perche' non e' stato chiesto:** dare all'inventario un
criterio piu' fine *(distinguere `open()` in lettura di un registro **da** la sola comparsa del nome
in un elenco di fonti o in un collaudo)*. **Sarebbe una voce nuova, e la lista e' congelata.**


---

# 🔬 **LA REVISIONE STORICA DEGLI OTTO `SI` E' NEL REPO** *(2026-09-26)*

`doc/REVISIONE_SI_2026-09-26.md`, e **ogni voce dell'indice che vi compare porta l'ancora della sua
sezione** nella colonna nuova **`revisione`** *(piu' i rimandi in testa allo smistamento)*.

## ⚠ **TRE LIVELLI DI EVIDENZA, e il documento non li mescola**

```
✅ VERIFICATO          l'ho aperto io: file, riga, e la FRASE che la riga contiene
🟨 DI LUCA              una misura o un numero della sua revisione: NON l'ho rifatto
🧠 INFERENZA            un ragionamento: si giudica dalla forma, non da un numero
```

**Perche' la distinzione e' la prima cosa del documento:** oggi ho **chiuso una voce su un numero che
non era nei file** *(`D09`)* e **creduto buono un campo vuoto** *(`avanzamento`, 740 su 740)*.
**Un documento che non dice quale riga ha aperto chi lo ha scritto e' una voce di corridoio.**

## ✅ **CIO' CHE HO VERIFICATO IO, riga per riga**

```
_scena_video.py:223    l'argv FISSA `--test N-MASSE`
_scena_video.py:328    `S.avvia_test("N-MASSE")()`  -- il costruttore ufficiale, anche qui N-MASSE
:7187                  `raise SystemExit(` dentro `_massa` (che comincia a :7169)
:8681                  `net.semina(-1 if SEMINA_LAM else a.nodi)`
:7290-7295             il commento della scena (ii): «UN SOLO VUOTO... si SOMMEREBBE... lo DICO»
:6541                  `v = self.pos[jj] - self.pos[ii]`  -- `L` viene dal DISEGNO
:4186                  `_smorza`: «smorzando solo la DISCESA», `eff = where(scende, dx*fatt, dx)`
:580                   `massa_critica_collasso`, forma adattiva
:2954-2961             `lambda_nodi` ritorna `np.full(self.n, LAM)`: COSTANTE UNIFORME
:5212                  la repulsione di coerenza: `u = riempimento * coerenza`, con
                       `massa_critica_collasso()` come fallback  -> **agisce sulle MASSE**
48a3555                data **2026-09-20**, e il messaggio dice «4651 nati in 1560 passi»
```

## 🟨 **CIO' CHE HO LASCIATO MARCATO COME TUO, invece di assorbirlo**

`L/d` fino a **x8** *(`Z103`)* · **454418** campioni sopra `0.5` · **78-89 %** di archi saturi
*(`Z112`)* · nati **218/216** · `lambda_nodi` = **0.7615·LAM** · la capacita' **621** · le **21**
occorrenze di cui **due mordono** · che `N-MASSE` **con `SEMINA_LAM`** finisca *proprio* in quel
`SystemExit` · che manchi un `--seme` **reale**.
**Di queste ho verificato l'ESISTENZA della riga, non il numero.**

## 🧠 **LE INFERENZE PIU' IMPORTANTI, e due RITIRI**

- **`tanh` conserva la MEDIA di `u = d − LAM`, l'esponenziale la MEDIANA; la distanza fra masse e'
  una SOMMA, quindi segue la MEDIA → `tanh` favorito PER PRINCIPIO**, non per un numero.
- ❌ **`exp(8.97e4)` su `4239163` e' un conto SBAGLIATO: l'esponente e' PER ARCO** *(`~0.3` a 120
  passi)*. **Sommare gli esponenti di archi diversi tratta un prodotto di fattori indipendenti come
  un unico fattore.**
- ❌ **«`4π` sulle facce» NON REGGE:** per un triangolo l'angolo solido e' **< `2π`**, quindi la fase
  di Berry **< `π`**. **`3π` non e' un quanto: e' il MASSIMO DELL'INGRESSO ISTANTANEO** *(`2π` di fase
  + `π` di torsione dipolare)*, e per questo **solo la coda lo raggiunge**.
- ⚠ **le due forme simmetriche CONGELANO gli archi a `LAM` esatto** *(`u → 0`)*: **non e' un difetto
  dimostrato, e' una conseguenza della forma** — va guardata sui dati.
- ⚠ **e un precedente di METODO:** la rimisura del 25 **soddisfaceva il criterio di riapertura** e fu
  dichiarata *«regge»*, **in configurazione sbagliata**.

## ❌ **UNA DATA CORRETTA, e la regola che ne esce**

Nella riga `Z73` avevo scritto che la ritrattazione era del **2026-09-24**: `git log` dice che
`48a3555` e' del **2026-09-20**. Corretto, col motivo accanto.
> ### **La data di un commit si legge da git, non si ricorda.** E' la stessa lezione di stamattina
> ### *(`STANDARD 9` vale anche per `git log`)*, vista dall'altro lato: **git e' la fonte, non la
> ### memoria.**

## ✅ **IL DELTA CONTRO IL TAG, col diff**

```
colonne 9 -> 11   nuove: `avanzamento`, `revisione`
voci  741 -> 740  sparita: `CLI-1)` (il token spurio)   nuove: nessuna
campi di DECISIONE cambiati (3):  D09  Z73  LETTORI-INDICE   -- esattamente le decisioni di Luca
```

**Le quattro condizioni di fine restano soddisfatte, e i collaudi pure** *(vista `2/2`, presidio
`5/5`, collisioni `0` su `322`)*.


---

# 🏛️ **L'INDICE E' LA FONTE: l'importatore si e' SPENTO** *(ultimo passo, 2026-09-26)*

## ✅ **LE QUATTRO COSE, e la quinta chiesta a meta' strada**

**① ULTIMA IMPORTAZIONE, poi l'importatore E' SPENTO.** `csv/_indice_id.py` ha girato per l'ultima
volta *(aggiungendo le colonne `motivo` e `nota`)* ed e' in
**`csv/_archivio/_indice_id_importatore.py`**.
> ### **Rilanciarlo ora sovrascriverebbe la FONTE con una RICOSTRUZIONE**, buttando via le decisioni
> ### scritte nelle colonne. **E' scritto nel suo docstring e nell'inventario**, non solo qui.

**② LE DECISIONI SONO NEI DATI, non nel codice.** `TIPO_A_MANO` → colonna **`nota`**
*(«tipo deciso a mano: …»)*; le `DECISIONI` della revisione → colonna **`motivo`** *(la prova in una
frase)*; l'**ordine di lavoro** → **`doc/ORDINE_SI.tsv`**, estratto **dall'AST** del vecchio
generatore *(non ricopiato a mano: `P1-ter`)*. **Nel codice delle viste non c'e' piu' una sola
decisione.**

**③ `csv/_indice_id.py` ORA E' UN VALIDATORE** e **non genera niente**: schema *(13 colonne esatte)*,
vocabolari, ID **unici e ben formati**, coerenza `stato`/`blocca`, **`motivo` obbligatorio dove
`blocca = SI`** *(una decisione senza prova non passa)*, e **nessuna voce persa rispetto al tag**
*(con le cancellazioni **DICHIARATE**: oggi una sola, il token spurio `CLI-1)`)*.
**Gira da solo nel `pre-commit`.** Collaudo **6/6**: l'indice vero passa, e **quattro guasti diversi
vengono rifiutati** *(stato inventato, tipo inventato, famiglia inventata, `blocca SI` su una voce
chiusa)*.

**④ LE VISTE SI GENERANO DAI DATI:** `_lista_chiusa`, **`_vista_smistamento`** *(nuovo: la vista era
dentro l'importatore)*, `_punto_della_situazione`.

**⑤ LE ISTRUZIONI D'USO SONO IN `CLAUDE.md`, sezione 11** — **14 righe**, con fonte, colonne, stati,
comandi, che cosa blocca il run base e dove sta il perche' di ogni `SI`.

## ✅ **IL COLLAUDO DELLE ISTRUZIONI, ed e' il piu' severo della giornata**

`csv/_collaudo_istruzioni.py` **non usa cio' che so: usa cio' che la sezione DICE.** Estrae la
sezione 11, ne legge **colonne, stati, tipi e comandi**, **costruisce la riga del difetto finto dalle
colonne DICHIARATE** *(e si ferma se l'intestazione dell'indice non coincide con quella scritta nella
sezione)*, e prova i due versi sul **hook vero**.

```
K0 la sezione dichiara fonte, 13 colonne, 5 stati e i comandi ....... OK
K1 DEVE FALLIRE  il difetto finto SOLO in `STATO_RUN` ... uscita 1 ... OK
K2 DEVE PASSARE  lo stesso con la RIGA nell'indice ...... uscita 0 ... OK
K3 i cinque comandi della sezione girano tutti, uscita 0 ............ OK
K4 il difetto finto COMPARE nello smistamento ....................... OK
K5 tutti i file tornano identici (sha1) ............................. OK
                                    -> 6/6: **LA SEZIONE 11 BASTA DA SOLA**
```

> ### **Un'istruzione d'uso si collauda facendo il lavoro CON QUELLA E NIENT'ALTRO.** Se avessi
> ### provato *«so aggiungere un difetto»* avrei collaudato me, non la sezione.

## ✅ **IL DELTA, col diff**

```
contro HEAD (1a764b0)   colonne 11 -> 13  (nuove: motivo, nota)
                        voci 740 -> 740   sparite: nessuna   nuove: nessuna
                        VOCI CAMBIATE nei campi di decisione: **0**
contro il tag           colonne  9 -> 13  voci 741 -> 740 (il token spurio)
                        cambiate: 3 -- D09, Z73, LETTORI-INDICE, **le decisioni gia' dichiarate**
```

**«0 voci cambiate» e' verificato contro `HEAD`**, che e' la domanda giusta per QUESTO passo: il
refactoring ha spostato **dove** vivono le decisioni, **non quali sono**.

## ❌ **UN DIFETTO MIO, e il solito posto**

Nel patch che aggiungeva le colonne, `re.sub(r"[\t\n]", …)` e' diventato **un TAB e un NEWLINE VERI
dentro la stringa** → `SyntaxError`. **Il blocco di scrittura del TSV e' stato ricostruito con
`replace`, che non ha escape da rovinare.**
> ### **Quarta volta oggi che un escape muore in un patch script** *(`\b` → backspace, `\u2014` →
> ### em-dash, `\s` → warning, ora `\t`)*. **La regola operativa e': nei patch script non si scrivono
> ### escape — si usa `chr()` o `replace`.**


---

# 🧹 **PROPOSTA DI RIORDINO DELLE REGOLE** *(2026-09-26, sessione nuova — SOLO PROPOSTA)*

**`doc/REGOLE_proposta.md`, generata da `csv/_regole_proposta.py`. Non ho toccato `CLAUDE.md`, ne' i
hook, ne' un assioma.**

## ✅ LE PRECONDIZIONI, verificate e stampate PRIMA di tutto

```
(a) il tag `lista-chiusa-v1` esiste ......... 7935806, 2026-09-26      OK
(b) LETTORI-INDICE `chiuso`, D09 `non-difetto` ...................     OK
(c) `python csv/_indice_id.py` ............. 740 voci, exit 0          OK
(d) albero di lavoro ....................... PULITO, nemmeno un `_log.txt`   OK
```

## 📉 I CONTEGGI, MISURATI

```
regole in vigore ............ 76  ->  62   (14 fuse o tolte; 58 con le tre fusioni in coda)
di cui AUTOMATICHE ..........  8  ->   9   (+1 proposta: l'inventario degli strumenti)
righe di CLAUDE.md ......... 1576 -> ~153  (sotto le 400 del presidio proposto)
righe lette all'avvio ...... 2714 -> ~1021
RELAZIONE_PER_CLAUDE.md ... 20364 -> un giorno, il resto in `doc/relazioni/`
```

> ### 🎯 **IL NUMERO CHE DECIDE: `par.9` da sola e' 671 righe su 1576, il 43 % di `CLAUDE.md`
> ### — e NON E' UNA REGOLA: sono FATTI dal codice.** Il secondo taglio e' la **storia** *(`par.0-ter`
> ### 208 + `par.5-quinquies` 130 = 338 righe)*, che va in un archivio **che non si legge all'avvio**.

## ❌❌ **DUE COLLISIONI DI NOME, ed e' lo stesso difetto che l'indice ha curato per i difetti**

| nome | in `CLAUDE.md` | nei hook |
|---|---|---|
| **`P3`** | nessuna statistica senza barra d'errore | un sigillo che configura il modulo a mano |
| **`P5`** | ogni ramo `else`/fallback va contato | un referto senza la configurazione intera |

**Lo stesso nome per due regole diverse.** Per i *difetti* l'abbiamo curato il 2026-09-26 *(`A3` era
tre voci)*; **per le regole no.** Proposta: i presidi dei hook prendono il prefisso **`H-`**, che
dice *«questo lo impedisce una macchina»*.

## ✅ **IL CONTROLLO CHE RENDE LA PROPOSTA VERIFICABILE**

**76 id estratti dalle fonti, 76 con una destinazione, 0 senza, 0 orfane** — e **lo script SI FERMA**
se un id resta senza destinazione. *Nessun comportamento imposto da Luca puo' sparire in silenzio.*

## ❌ **UN CONTO CHE SMENTIVA LA PROPOSTA A CUI ERA ALLEGATO**

La prima stima di `CLAUDE.md` DOPO dava **497 righe** — **sopra la soglia di 400 che la proposta
stessa chiede**: sottraeva solo `par.9` e le sezioni del posto 5, **ignorando le fusioni**.
> ### **Un numero che contraddice il documento in cui sta non si arrotonda: si rifa'.** Ora e'
> ### calcolato **per sezione**, con l'ipotesi **dichiarata** *(chi esce vale `0`, chi si fonde `2`
> ### righe, chi resta il `40 %` se supera le 20 righe)*, e da' **153**.

## ⚠ **E UN CONTO CHE ANCORA NON TORNA, dichiarato nel documento**

Il posto 2 *(`PATTERN_DI_PROVA`, **tetto 10**)* raccoglierebbe **16** regole. **Non ci sta, e lo
scrivo invece di alzare il tetto**: propongo **tre fusioni** — `P3`+`P6`+`par.9-bis` *(un numero
senza barra, seme, flag ed EPOCA non e' un dato)*, `P4`+`L-SOGLIA` *(il test vuoto visto da due
lati)*, `STANDARD 3`+`STANDARD 4` *(che cosa si confronta con che cosa)* — che lo portano a **10**.

## 🔒 I TRE MECCANISMI CONTRO LA RICRESCITA

**①** una regola nuova **ne sostituisce una** *(il tetto di 10 al posto 2, fatto valere da un
conteggio)*; **②** un **presidio nel `pre-commit`** che rifiuta `CLAUDE.md` **oltre le 400 righe**;
**③** a ogni **tag d'epoca**, la revisione dei presidi **mai scattati** — *un presidio che non ha mai
rifiutato niente non sta impedendo niente* (`A9`), **e i hook contano gia' le proprie invocazioni**.

## ⛔ **STOP: decide Luca.** Nessun documento nuovo e' stato scritto — `STORIA_REGOLE.md`,
`FATTI_dal_codice.md` e `doc/relazioni/` sono **destinazioni proposte**, e scriverli sarebbe
**applicare**.

---

# 🧹 **IL RIORDINO E' APPLICATO** *(2026-09-26, mandato di Luca con sei modifiche)*

> **Non e' piu' una proposta.** Luca ha approvato `doc/REGOLE_proposta.md` con le modifiche
> `a`-`i`, e questo blocco di commit la **applica**. Il prima e' nel tag **`regole-pre-riordino`**
> (`4f15f7a`), e ogni migrazione ha uno **script che si rigira** e un controllo che dice se ha
> perso qualcosa.

## ① `RELAZIONE_PER_CLAUDE.md`: **da 20436 righe a 1636** — l'archivio per giorno

**MISURATO** (`csv/_archivio_relazioni.py`, che stampa i numeri: `L-NUMERI`):

```
righe in ingresso ......... 20437        (elementi del taglio: con il fine-riga finale)
preambolo che resta .......    36
giorni riconosciuti .......     9
    2026-09-14    134      2026-09-15   1310      2026-09-16   5551
    2026-09-19    555      2026-09-20   1444      2026-09-21   5371
    2026-09-24   1360      2026-09-25   3094      2026-09-26   1582  <- resta nel file vivo
righe in uscita (somma) ... 20437        <- IDENTICA: nessuna riga riscritta, nessuna persa
```

**LA REGOLA DI TAGLIO E' DICHIARATA, perche' e' un GIUDIZIO e non una misura:** si taglia su ogni
intestazione (`#` o `##`) che **contiene una data**, e il pezzo che segue appartiene a quella data
fino al taglio successivo. Il preambolo — cio' che precede il primo taglio — **resta nel file
vivo**, perche' dice *come si legge*, non *che cosa e' successo un giorno.

**PERCHE' NON E' ESTETICA, ed e' scritto nella proposta:** la relazione e' il file che una sessione
nuova legge **per primo**, e a 20436 righe **non la leggeva nessuno per intero** — quindi il suo
scopo era **gia' perso**. L'archivio lo restituisce, e `git log` resta l'indice.

## ② `par.9` esce da `CLAUDE.md`: **671 righe di FATTI, ora ordinate PER FUNZIONE**

**Il numero che decideva, e adesso e' misurato:** `par.9` era **669 righe di corpo su 1575**, e
**non era una regola: erano FATTI verificati sul codice**. Ora sono `doc/FATTI_dal_codice.md`.

**LA MODIFICA DI LUCA (punto `e`) E' L'ORDINAMENTO PER FUNZIONE**, e non e' cosmetica: prima un
fatto su `ritmo()` stava in mezzo a un fatto su `mitosi()` e a un presidio di statistica, e chi
apriva `ritmo()` **non aveva modo di sapere che ce n'era uno**.

```
punti di primo livello di par.9 ........ 53
funzioni con almeno un fatto ........... 11
righe di par.9 NON ritrovate nell'uscita  0      <- lo spostamento e' VERBATIM, e verificato
```

| funzione | riga di oggi (AST) | fatti |
|---|--:|--:|
| `rapporto_guardie` | 606 | 1 |
| `_eredita_spinore_figli` | 1933 | 1 |
| `ritmo` | 2983 | 3 |
| `_passo_spinoriale` | 3100 | **13** |
| `salva_stato` | 4617 | 3 |
| `_cs_nodo` | 4734 | 2 |
| `_bloch_ritardato` | 4789 | 2 |
| `_tempo_luce_nodo` | 4947 | 3 |
| `_coppia_interferenza` | 5019 | 1 |
| `mitosi` | 5871 | 2 |
| `memoria_hebbiana_moto` | 6547 | 3 |

**LE RIGHE SONO MISURATE DALL'AST, non ricopiate** — e questo cura un difetto che `par.9`
denunciava da sola: *«le righe citate qui sotto sono SHIFTATE»*. Le righe **dentro** i fatti
restano quelle di allora, perche' **i reperti non si riscrivono**; l'intestazione porta quella
di oggi.

**E IN `CLAUDE.md` C'E' LA REGOLA CHE LO RENDE UTILE:** *«prima di toccare una funzione del
simulatore, leggi i suoi fatti in `doc/FATTI_dal_codice.md`»*.

**⚠ COSA QUESTO *NON* DICE:** che la destinazione di ogni punto sia giusta. **I numeri sono
misurati, le destinazioni no**: stanno in una mappa `DESTINAZIONE` di 53 righe dentro
`csv/_riordino_fatti.py`, **una riga per punto**, e si correggono in un posto solo.
**E diciassette dei 53 punti NON sono fatti su una funzione: sono PRESIDI DI LETTURA**, e stanno
in una sezione a parte che rimanda alla regola che li copre.

## ③ La STORIA delle regole esce, e due sezioni vanno dove vivono le cose che dicono

**`doc/STORIA_REGOLE.md` — 964 righe, archivio VERBATIM, che NON si legge all'avvio** (punto `f`).
Contiene **ogni sezione** di `CLAUDE.md` di prima **tranne `par.9`**, e in testa una tabella di
**23 righe** che dice, per ognuna, **dove vive oggi la sua regola**.

**LA FONTE E' IL TAG, NON IL DISCO**, ed e' una decisione di metodo: `CLAUDE.md` viene riscritto
dal riordino, e uno script che leggesse il disco alla seconda esecuzione **archivierebbe il file
gia' asciugato, facendo sparire la storia in silenzio**.

```
righe di CLAUDE.md al tag ............. 1575
sezioni archiviate ....................   23
sezioni SENZA destinazione ............    0    <- lo script si ferma se non e' 0
righe NON ritrovate (par.9 escluso) ...    0
```

**E UN DIFETTO VERO, TROVATO SPOSTANDO:** `CLAUDE.md` conteneva **un byte NUL** (riga 505, dentro
la formula `sha1("blob <len>\0" + contenuto)`). **Un NUL fa dichiarare BINARIO il file a `grep`** —
`grep -n '^## ' CLAUDE.md` rispondeva *«Binary file CLAUDE.md matches»* invece di elencare le
sezioni. **Un presidio che gira `grep` su quel file non trova niente, e non lo dice.** Nell'archivio
il NUL e' diventato due caratteri visibili, **con l'ancora contata** (`P1-quater`).

**E LE DUE SEZIONI CHE NON ERANO REGOLE DI LAVORO:**

| sezione | dove va | perche' |
|---|---|---|
| **`par.4`** — le regole fisiche da non violare | **`doc/REGISTRO_FISICA.md`** (in coda, 27 righe) | **sono FISICA**, e il posto delle leggi e' il registro delle leggi |
| **`par.6`** — stato e ordine del lavoro | **`doc/STATO_RUN.md`** (dopo l'INDIRIZZO, 28 righe) | **e' STATO, non una regola** |

**L'innesto in `STATO_RUN` e' PRIMA delle voci di run, non in coda**, e il perche' e' meccanico:
quel file e' letto da `csv/_stato_run.py`, che cerca `## APERTO` e `**chiuso` per rifiutare
l'apertura di un run quando il precedente e' ancora aperto. **Verificato dopo l'innesto: 17
`APERTO` e 17 `chiuso`, il bilancio regge.**

## ④ `CLAUDE.md`: **da 1575 a 330 righe**, e il posto 2 riscritto

| | PRIMA | DOPO | |
|---|--:|--:|---|
| `CLAUDE.md` | **1575** | **330** | tetto 400, e un presidio lo impedisce |
| **righe lette all'avvio** *(misurate, non stimate)* | **2706** | **1045** | **-61 %**, e da **8** documenti a **3** |

**IL PUNTO `i` DEL MANDATO — LA DISCREPANZA `~1021` CONTRO `~1291` — E' RISOLTA, E LA CAUSA E'
UN NUMERO CALCOLATO DUE VOLTE CON DUE FORMULE:** in `csv/_regole_proposta.py` il **documento**
stampava `_avvio - _fuori_cl` *(→ ~1291)* e lo **stdout del commit** stampava
`_avvio - _fuori_cl - int(_storia * 0.8)` *(→ ~1021)*. **Nessuna delle due era sbagliata di
aritmetica: erano due grandezze diverse col medesimo nome** — una scontava la storia, l'altra no.
**E' esattamente `L-NUMERI` al contrario:** il numero usciva da uno script, ma **da due
espressioni**, e nessuno le confrontava. **Adesso e' MISURATO: 2706 → 1045**, e il conto sta in
`csv/_controlli_riordino.py`, che lo stampa documento per documento.

**IL POSTO 2 (`doc/PATTERN_DI_PROVA.md`): 93 → 172 righe**, con la lista di controllo di un
sigillo (ex `par.2`) e le fusioni approvate:

- **`P3` + `P6` + `par.9-bis`** → *«un numero senza la sua BARRA D'ERRORE, il suo SEME, i suoi
  FLAG e la sua EPOCA non e' un dato»*, **e il «almeno 4 semi» resta esplicito** (modifica `a`);
- **`L-SOGLIA` dentro `P1-sexies`** — *«un criterio si collauda su un caso a risposta nota,
  compreso il caso nullo, e la sua soglia non dipende dai dati che giudica»* (modifica `b`);
- **`STANDARD 3` + `STANDARD 4`**, con **entrambe** le clausole (modifica `c`);
- **`P4` resta SOLA**: Luca ha rifiutato la fusione che la proposta chiedeva.

> ### ⚠ **E IL CONTO DEL POSTO 2 NON TORNA: 11 REGOLE PER UN TETTO DI 10. LO DICO.**
> **Anche la proposta ne dava 12, non 10: quel «10» era sbagliato in aritmetica** *(16 righe −2
> −1 −1 = 12; togliendo `par.2`, che diventa la **lista di controllo** e non una riga, fa 11)*.
> **Non ho scelto io l'undicesima da fondere**, perche' sarebbe decidere al posto di Luca — e la
> fusione che lui ha **esplicitamente rifiutato** era proprio una di queste. **Le tre candidate,
> con quello che si perderebbe, sono scritte in fondo a `doc/PATTERN_DI_PROVA.md`. E' in coda.**

**E UN'ANCORA CORRETTA:** `csv/_collaudo_istruzioni.py` cercava `^## 11\. L'INDICE DEI DIFETTI`.
Col riordino quella sezione e' diventata `par.9`, e il collaudo **si schiantava** — *il modo piu'
facile di non accorgersene* (`A8`). Ora l'ancora e' **il NOME, non il numero**, com'e' scritto in
`CLAUDE.md` par.2. **Esito invariato: `6/6 PASS`.**

## ⑤ I presidi dei hook prendono il prefisso `H-` — **una collisione di nomi, curata**

**IL DIFETTO ERA REALE E DELLO STESSO TIPO CHE L'INDICE HA CURATO PER I DIFETTI** *(`A3` era tre
voci)*: **`P3` e `P5` erano DUE REGOLE DIVERSE CON LO STESSO NOME** — la regola di metodo di
`CLAUDE.md` e il presidio del hook. **Chi citava `P3` non diceva quale.**

**LA FORMA E' QUELLA CHE HA SCRITTO LUCA — `H-P3`, `H-P5`, ...**, cioe' **il nome di prima col
prefisso**. La proposta aveva suggerito nomi **semantici** (`H-CLI`, `H-CONFIG`, `H-ANCORA`) e
**li ho scartati**: col nome di prima ogni citazione storica (`P5` in un referto del 25/9) resta
**leggibile** e si risolve con l'`alias`. **Se Luca intendeva i nomi semantici, si cambia con una
rigirata di `csv/_rinomina_hook.py`.**

```
37 sostituzioni nei 7 sorgenti dei hook, OGNUNA asserita per se' (P1-quater)
21 marcatori `ESENTE-Pn` -> `ESENTE-H-Pn` in 20 file
collaudo dei presidi: 8/8 OK          collaudo del validatore: 6/6 PASS
```

**E IL NOVE-ESIMO PRESIDIO E' NUOVO: `H-RIGHE`** (punto `h`) — *`CLAUDE.md` non passa le 400
righe*. **Collaudato nei due versi, 5/5.** E **sta in `commit-msg`, non in `pre-commit`**: la via
d'uscita `[CLAUDE-OLTRE-400: ...]` vive **nel messaggio**, e in `pre-commit` il messaggio **non
esiste ancora** — leggerlo la' significa leggere **il commit PRECEDENTE**, cioe' spegnere il
presidio per sempre alla prima eccezione. *(E' lo stesso difetto gia' trovato su `H-INDICE`.)*

**DUE DIFETTI MIEI, TROVATI DAI PRESIDI STESSI MENTRE COMMITTAVO — e sono il valore vero di
questo giro:**

1. **`H-RIGHE` ha RIFIUTATO il commit 1/6.** Giusto: guarda il file che **sara'** a `HEAD`, e
   fino al commit 4/6 era ancora quello da 1575 righe. **Rifiuto vero, non sintetico.**
2. **La via d'uscita non attraversava le righe.** La mia regex era senza `re.S`, e una
   dichiarazione scritta **su tre righe** — come si scrive un motivo che vale la pena di leggere
   — **veniva ignorata e il commit rifiutato lo stesso**. **Il collaudo non l'aveva preso perche'
   i suoi quattro casi avevano il messaggio su UNA riga: il caso sintetico era piu' povero del
   caso reale.** Aggiunto il quinto caso, `dichiarato_su_piu_righe`.
3. **`H-INDICE` ha rifiutato il commit 4/6 per `L-PATCH`**, che avevo **citato** in `CLAUDE.md`
   senza dargli la riga nell'indice. **Aveva ragione.**

**E LA FORMA DEGLI ID E' STATA ALLARGATA, con la misura accanto:** `[A-Z][A-Z0-9]{1,}(-...)+`
chiedeva **due** caratteri prima del trattino, quindi **`H-P3` e `L-SOGLIA` non erano id validi**
— il validatore rifiutava **sedici voci su sedici** dei nomi che Luca stesso aveva dettato, e il
presidio leggeva `L-DOPO-STOP` come **`DOPO-STOP`**, segnalando come ignoto **un pezzo di un id
che c'e'**. Allargata a **uno** stem. **Misurato l'effetto: gli ignoti passano da 6 a 0**, dopo
aver dichiarato in `INDICE_ID_ESCLUSI.tsv` le sei forme che **non sono id** (`A-B`, `U-U`,
`UTF-8`, `CLAUDE-OLTRE-400`, `ESENTE-H-P5`, il marcatore HTML dell'innesto).
