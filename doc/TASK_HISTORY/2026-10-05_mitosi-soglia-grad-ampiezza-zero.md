# `MITOSI-SOGLIA-GRAD` **a ampiezza zero** — LA MISURA

*(Mandato di Luca del 2026-10-05, **dopo** il referto di `CRESCITA-DOPO-Z43` (`12e2ca7`).
Il simulatore **`f7237563` NON si tocca**: si misura **con una patch**.)*

> ### ⛔ **E LA MISURA CON `DT` DIMEZZATO RESTA FERMA finché Luca non lo dice.**
> ### ⛔ **E la RIMOZIONE dal simulatore — archivio col tag, censimento degli strumenti che
> ### usano `_r_nodo_mitosi`, sigillo, chiusura della voce — è UNA DECISIONE DI LUCA e sarà
> ### un prompt a parte.**

## 1. RAGIONAMENTO PRELIMINARE

### LA DOMANDA

In `decidi_divisione` *(`:8376` sul blob `f7237563`)*:

```
soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_modula))     grad_modula = |r_i - r_j|
```

**L'ampiezza `0.3` e la `tanh` sono a mano.** La voce è `MITOSI-SOGLIA-GRAD`, stato
**`DA-DECIDERE`**, e `doc/REGOLE_composizione_T3.md` §6.3 dice *«va derivata»*.
**Luca valuta di TOGLIERE del tutto la modulazione**, cioè `soglia = soglia0` su ogni arco.

### ✅ L'IPOTESI DEL GUARDIANO — **e l'ho VERIFICATA DAL CODICE, non assunta**

*Il gradiente di tempo proprio entra **già** nella torsione, quindi la modulazione della
soglia lo conta **DUE VOLTE**, con la stessa forma dell'errore della `PARTE A` di `Z43`.*

**LA CATENA, riga per riga, ed è una lettura e non una congettura:**

| | la riga | che cosa dice |
|---|---|---|
| `:7438` | `dt_n = DT * r` | il tic è il **tempo proprio** del nodo |
| `:7769` | `self.phi = (_phi_t + (dt_n_s * self.phivel) + delta_sync_phi) % _dphi()` | la fase avanza di **`dt_n * phivel`** |
| `:7772` | `dph = self._wphi(_phi_t[i] - _phi_t[j])` | la **differenza di fase** sull'arco |
| `:7795` | `self.tw += self._w8(dph + twist_dip - self.twp) - dt_e*self.tw/_ttw` | `tw` accumula l'**INCREMENTO** di `dph` |

### ➜ **QUINDI la differenza di fase sull'arco cambia, per passo, di**

```
DT * (r_i * phivel_i  -  r_j * phivel_j)
```

### **e `tw` la INTEGRA.** ### ✔ **La catena è STRUTTURALMENTE STABILITA: due estremi con `r`
diverso si sfasano, e lo sfasamento diventa torsione.** ### **Quello che la misura aggiunge
non è *se*, ma QUANTO.**

### ⚠ **E IL LIMITE DICHIARATO DAL GUARDIANO SI LEGGE NELLA STESSA RIGA**

Lo sfasamento è proporzionale **anche a `phivel`**: dove `phivel ≈ 0` il gradiente
### **non produce torsione**, qualunque sia `|r_i - r_j|`.

> ### 📌 **E LA FORMA ESATTA NON È QUELLA DEL MANDATO, e lo dico invece di sostituirla.**
> Il mandato chiede di correlare anche contro **`|r_i - r_j| · |phivel|` medio dei due
> estremi**. La grandezza che il codice produce è
> ### **`|r_i·phivel_i − r_j·phivel_j|`**, che è diversa: le due coincidono solo se `phivel`
> è **uniforme sull'arco**. ### **Riporto ENTRAMBE** — la proxy chiesta **e** la forma esatta
> — ### **e la seconda è un'aggiunta, non una sostituzione.** Se divergessero, la forma
> esatta è quella che descrive il codice.

### DOVE STA IL DOPPIO CONTEGGIO, se c'è

Il cancello `1` è `avv > soglia`, cioè `avv/soglia > 1`. Il gradiente:
* **alza il NUMERATORE** `avv = |tw|`, attraverso lo sfasamento *(la catena qui sopra)*;
* **abbassa il DENOMINATORE** `soglia`, attraverso la modulazione.

### ⛔ **Due spinte nello STESSO verso dalla STESSA grandezza: è la forma dell'errore della
### `PARTE A`** *(dove `r` moltiplicava `omega_clk` **e** compariva in `_dts`)*.

### CHE COSA MI ASPETTO IO, e **non coincide del tutto col guardiano**

Le previsioni del guardiano sono al par.2. **La mia differenza:** mi aspetto che `Ap0` perda
**molto** — sono d'accordo — ### **ma NON per il doppio conteggio.** Dal referto
`12e2ca7`, in `Ap` gli archi che entrano nella finestra hanno `soglia` q05 = `6.9900`
contro un pavimento di `6.9129`: ### **stanno PRATICAMENTE AL MINIMO.** Portarli a `soglia0
= 9.4248` è un salto del **`+35 %`** sulla soglia che devono superare.
### ⚠ **Ma quel `6.99` è un effetto di SELEZIONE** *(il referto lo dichiara: l'insieme è
definito da `avv > soglia`)*, ### **quindi NON posso dedurne quanto perderà `Ap0`: è
esattamente ciò che questa misura serve a sapere.** ### **Lo scrivo per non spacciare dopo
una previsione per una deduzione.**

## 2. PROGETTAZIONE — *i passi, cosa decide ciascuno, cosa mi farebbe FERMARE*

### LE PREVISIONI DEL GUARDIANO, **scritte PRIMA della corsa come il mandato chiede**

| | la previsione |
|---|---|
| **`Bp0`** | le nascite **cambiano poco**, fra **`0.5x`** e **`1.0x`** di `Bp`, perché in `B` la modulazione morde solo il `5`-`10 %` sugli archi che passano |
| **`Ap0`** | perde **la maggior parte** delle nascite, **meno di `0.5x`** di `Ap` |
| **`(2)`** | correlazione **positiva e crescente** col quintile |

### I CRITERI, **fissati PRIMA e non negoziabili dopo**

| | se | allora |
|---|---|---|
| **`K1`** | `Ap0 >= 0.8x Ap` | ### **l'ipotesi <<le nascite di `A` si reggevano sul `0.3`>> è REFUTATA** |
| **`K2`** | la Spearman di `(2)` è `<= 0.05` **in valore assoluto a TUTTI E TRE i passi** | ### **l'ipotesi del DOPPIO CONTEGGIO è REFUTATA** — e allora ### **togliere la modulazione toglierebbe DEL TUTTO l'effetto del gradiente sulla mitosi**, e ### **va scritto così** |

### LA PATCH — **UNA SOLA RIGA, e il controllo `C0` lo dimostra**

L'ancora è `soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_modula))`, **unica** in entrambi i
bracci *(verificato)*. Diventa `soglia = soglia0 * (1.0 - _AMP * np.tanh(grad_modula))` con
`_AMP` iniettata dallo strumento.
### ✔ **Così `_AMP = 0.3` è l'ESPRESSIONE ORIGINALE** e `_AMP = 0.0` la annulla, **senza
toccare nessun'altra riga** — e ### **`C0` verifica che a `0.3` il braccio sia
BYTE-IDENTICO a `Bp`.**

### ⚠ **E `0.3` NON È UN LETTERALE RIMPIAZZATO DA UNA VARIABILE A CASO:** `_AMP = 0.3` deve
dare `1.0 - 0.3*tanh(x)` **al bit**. `0.3` è lo **stesso** `float64` in entrambi i casi,
quindi l'identità è esatta — ### **ma la DIMOSTRO con `C0` invece di dedurla.**

### I BRACCI

| | | |
|---|---|---|
| **`Ap0`** | la `PARTE A` *(`062172d3`)*, **ampiezza `0`** | i cancelli |
| **`Bp0`** | la `PARTE B` *(`f7237563`)*, **ampiezza `0`** | i cancelli |
| **`B03`** | la `PARTE B` **patchata con ampiezza `0.3`** | ### **solo per `C0`** |
| **`Bg`** | la `PARTE B` **non patchata**, col gancio della misura `(2)` | la correlazione |

### ✔ **E `Ap` e `Bp` NON SI RIGIRANO: vengono dal `crescita.json` committato in `12e2ca7`.**
Stessa scena, stesso seme, stesso strumento *(`a3db21b2`, esteso)*. ### **Confrontare con
numeri già committati è più forte che rigirarli**, e costa tre bracci invece di cinque.

### LA MISURA `(2)` — **l'incremento di `|tw|` contro il gradiente**

Nel braccio **`Bg`** *(con modulazione, quello di oggi)*, ai passi **`50`, `100`, `140`**:
per **ogni arco** l'incremento per passo di `|tw|` contro

1. **`|r_i - r_j|`** *(il gradiente nudo, quello che la soglia legge)*;
2. **`|r_i - r_j| · |phivel|` medio dei due estremi** *(la proxy chiesta dal mandato)*;
3. ### **`|r_i·phivel_i − r_j·phivel_j|`** *(la forma ESATTA che il codice produce — **mia
   aggiunta**)*.

Per ciascuna: **Spearman** e gli **incrementi mediani per quintile**.

### ⚠ **E SERVE UN GANCIO CHE LEGGA `|tw|` PRIMA E DOPO L'AGGIORNAMENTO**, perché
l'incremento non è osservabile da fuori: `tw` è già aggiornato a fine passo.
### **Il gancio LEGGE, non ricalcola:** prende `self.tw` ai due lati della riga `:7795`, e
`r`/`phivel` dallo stesso istante.

### ✔ LA SEPARAZIONE **SPINTA / SCARICA** — *aggiunta del guardiano, 2026-10-05*

L'aggiornamento della torsione *(`:7795`)* ha **DUE** termini, e vanno **separati**:

```
self.tw  +=  _w8(dph + twist_dip - twp)   -   dt_e * self.tw / _ttw
             \_________ SPINTA _________/       \______ SCARICA ______/
```

### ⛔ **E L'IPOTESI DEL DOPPIO CONTEGGIO RIGUARDA LA SPINTA:** e' **quella** che deve
crescere col gradiente. ### **La SCARICA cresce col gradiente per un'altra ragione** —
`dt_e = DT*0.5*(r_i+r_j)` — ### **e va nel verso OPPOSTO.** Sommarle e correlare il totale
### **mescolerebbe le due cose**, ed e' esattamente l'errore che ho appena ritirato dal
referto di `CRESCITA-DOPO-Z43` *(`076cc29`)*.

**Quindi la misura `(2)` riporta la Spearman per `3 x 3` combinazioni:** i **tre** predittori
*(gradiente nudo, la proxy `|r_i-r_j|*|phivel|`, la forma esatta
`|r_i*phivel_i - r_j*phivel_j|`)* contro i **tre** bersagli *(incremento **TOTALE** di `|tw|`,
la **SPINTA**, la **SCARICA**)*.
### ✔ **E `K2` si applica alla SPINTA**, non al totale: e' l'ipotesi che il mandato nomina.

### COME SI CATTURANO I DUE TERMINI **senza riscrivere la legge**

La riga diventa, **sulla sola copia patchata**:

```
_spinta  = self._w8(dph + twist_dip - self.twp)
_scarica = dt_e * self.tw / _ttw
self.tw += _spinta - _scarica
```

### ✔ **E' BYTE-IDENTICA, e il perche' e' aritmetico:** `+=` su un `ndarray` valuta **tutto
il membro destro prima** di scrivere, quindi `_spinta - _scarica` e' **la stessa
sottrazione** fra gli stessi due valori, e `self.tw` dentro `_scarica` e' ancora quello di
prima. ### **Nessuna seconda scrittura della legge: gli stessi due sotto-espressioni, con un
nome.**
### ⚠ **MA LO DIMOSTRO INVECE DI DEDURLO:** il controllo `C0-tw` pretende che il braccio
`Bg` sia **byte-identico** a `Bp`.

## I CONTROLLI

| | | se fallisce |
|---|---|---|
| **`C0`** *(deve **passare**)* | `B03` **byte-identico** a `Bp`, `n` e archi finali compresi | ### ⛔ **la patch tocca più dell'ampiezza: FERMO** |
| **`C-fallisce`** *(deve **fallire**)* | `Bp0` **DEVE differire** da `Bp` | ### ⛔ **la patch non è agganciata: FERMO** |
| **`C1`** | `divisioni + schwinger == nati` *(dal simulatore)*, in **ciascun** braccio | ### ⛔ **FERMO** |
| **`C-rng`** | `rng.random(len(avv))` chiamato con la **stessa lunghezza** nei bracci con e senza modulazione | ### ⛔ **le estrazioni si spostano: il confronto non è più a parità di dado, FERMO** |
| **`C0-tw`** *(deve **passare**)* | `Bg` *(la `PARTE B` col solo **nome** dato ai due termini, piu’ il gancio)* **byte-identico** a `Bp` | ### ⛔ **la separazione ha cambiato l’aritmetica: FERMO** |

### 📌 **PERCHÉ `C-rng` NON È OVVIO, e va misurato:** la modulazione cambia `soglia`, quindi
`ecc`, `salita`, `resp` e `prob` — **ma NON `len(avv)`**, che è il numero di archi.
### ✔ **Quindi il generatore avanza dello stesso numero di estrazioni per passo**, e i due
bracci restano **a parità di dado** finché la topologia non divergerà.
### ⚠ **E DIVERGERÀ**, appena nasce un nodo in uno e non nell'altro: `len(avv)` cambia e le
estrazioni si sfasano. ### **Quindi `C-rng` non dice <<stesso dado per sempre>>: dice
<<stesso dado finché la topologia è la stessa>>**, e il passo in cui divergono si
### **riporta.**

## LA STELLA POLARE

**1 — `A14`.** **Non si applica alla misura**, che legge. ### ⚠ **Ma si applica a ciò che
potrebbe far decidere:** togliere la modulazione **cambia quanta materia nasce**, e *«quella
massa da dove veniva / dove va»* è una domanda di `A14`. ### **Nominata, non risolta.**

**2 — i tre gradini.** Gradino **(a)**: due bracci, stessa scena, stesso seme.
### ✔ **Gradino (b) È IL PUNTO DI QUESTO MANDATO:** *«regge togliendo la legge pratica?»* —
e la legge pratica **è** il `0.3`. ### ⛔ **Gradino (c): NO**, non c'è un limite noto per un
conteggio di nascite su questa scena. ### **E i conteggi assoluti dipendono dalla
piattaforma: il risultato è il RAPPORTO fra i bracci.**

**3 — numeri e leggi.** ### **ZERO aggiunti.** La misura **TOGLIE** un numero *(`0.3`)* in un
braccio e lo **misura**. ### ✔ **Ed è esattamente il tipo di cosa che `A1` chiede di fare
prima di tenere un numero a mano.**

**4 — `rho`, `c_s`, il SEGNO.** La misura non li tocca. ### **Legge `r`** *(che viene da
`cs`)* **e `phivel`**, e il **SEGNO** entra solo come cancello `3`, che non si modifica.

**5 — emergente o imposto.** ### **È LA DOMANDA, ed è la stessa di `CRESCITA-DOPO-Z43` con
un intervento invece di un'osservazione:** il referto `12e2ca7` ha detto che la soglia bassa
sugli archi che nascono è una **CORRELAZIONE** con un effetto di **selezione**, e che
separarla ### **vuole un INTERVENTO sulla soglia.** ### **Questo mandato È quell'intervento.**

## 3. TODO DEL NEXT STEP

1. **commit di questo task history**, prima dello strumento;
2. lo **strumento esteso** *(la patch a una riga, il gancio di `(2)`, i quattro controlli)*,
   col **collaudo**, e **commit prima della corsa**;
3. la **corsa**: `Ap0`, `Bp0`, `B03`, `Bg`, `150` passi, seme `11`;
4. i **controlli**, e `FERMO` se `C0`, `C-fallisce`, `C1` o `C-rng` falliscono;
5. il **referto**, **generato**, coi blob e coi criteri `K1`/`K2` **applicati come scritti**;
6. la **relazione** e le voci, nello stesso giro;
7. ### ⛔ **poi FERMO, e si aspetta Luca.**
