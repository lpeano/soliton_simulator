# LA RISCRITTURA AL PRIMO ORDINE — **che cosa sparisce, che cosa rinasce, e perché**

> ### ⛔ **QUESTO DOCUMENTO NON È UNA CURA, ED È IL PUNTO.** `A16` dice che il simulatore di
> oggi *(`b8c21049`)* viola l'assioma ### **nel suo cuore**, e che la cura ### **non è una
> legge**: è una riscrittura. Qui sta ### **che cosa** va riscritto, con i ### **numeri
> misurati** che hanno portato alla decisione.
>
> ### ⚠ **E IL SIMULATORE NON SI TOCCA:** resta `b8c21049`. Il prototipo vive in
> `proto_primo_ordine/`, ### **fuori** dal simulatore e ### **senza importarlo**.

---

# ① LA FORMA PROPOSTA — **e che cosa resta aperto**

### **LO STATO.** Uno per nodo, `ψ_k ∈ C²`, e ### **nient'altro**:

```
psi_k = |psi_k| * e^{i phi_k / 2} * chi_k          chi_k = direzione di Bloch
```

### ⛔ **`phi` NON è una variabile:** si ### **legge** da `ψ`. ### **E non esiste `phivel`.**

### **L'EVOLUZIONE.** Primo ordine, una sola `H`:

```
i * dpsi_k/dt  =  dH / dpsi_k*
```

### **LA FORMA DI `H` DEL PROTOTIPO** *(prima versione, e `A16` dice esplicitamente che la
forma ### **si decide con misure**)*:

```
H  =  - somma_archi w_ij * ( <psi_i| U_ij |psi_j> + c.c. )   +  (g/2) * somma_k |psi_k|^4
```

| pezzo | che cos'è | ### **che cosa resta aperto** |
|---|---|---|
| `w_ij` | il peso d'arco | ### ⛔ **FISSO nel prototipo**, e il documento lo dichiara una ### **violazione provvisoria di `A16.3`**: una memoria congelata |
| `U_ij ∈ SU(2)` | il trasporto sull'arco | ### ⛔ **FISSO** per la stessa ragione. ### **La memoria dinamica dentro `H` è il passo successivo, e lo decide Luca** |
| `g` | il termine non lineare | ### **si SCANDISCE**, non si sceglie: il prototipo prova cinque valori dichiarati prima |
| la metrica, il vuoto, le nascite | — | ### **non ci sono ancora.** Vedi `③` |

---

# ② CHE COSA SPARISCE — **e il numero che lo giustifica**

| che sparisce | perché, con la misura |
|---|---|
| ### **`phivel`** e l'inerzia ### **`M_PH`** | sono il ### **secondo ordine**: `M_PH·Δphivel/dt_n = coppia` *(`:7760`, `:7830`)*. ### ⛔ **`A16.2` non li ammette**, e non c'è una misura che li salvi: ci sono perché il modello è stato scritto così |
| ### **la coppia come FORZA** | ### ⛔ **MISURATO, non argomentato:** la coppia del driver ### **non è `−∂H/∂φ` di nessuna energia.** Il collaudo di `D3` dà scarto relativo ### **`1.054`** contro la forma `U(2)`, e il collaudo di `D2-BIS` dà ### **`1.18e-01`** per una coppia non di gradiente contro `2.55e-06` per una che lo è |
| ### **il termostato sulle velocità** | agisce su `phivel`, che non esisterà. ### **E la misura dice che è quasi innocuo dove conta:** nella decomposizione di `dT` di `B-SCAL-TS` vale ### **`+394.56`** contro ### **`+8804.86`** della coppia |
| ### **lo scuotimento** *(`scuoti_vuoto`)* | ### **non fa lavoro: inietta varianza.** La parte quadratica è il ### **`99.4 %`** in entrambe le classi *(`D1`)*. In `A16` il vuoto non è un calcio additivo: è ### **uno scambio che deve emergere** *(`A15.3`)* |
| ### **la sincronizzazione** *(`K_SYNC`, `delta_sync_phi`)* | sposta `φ` ### **fuori** dalla dinamica *(`:7805`, sommata a `:7831`)*. ### ⛔ **E MISURATO: è la sorgente.** Togliendola si perde il ### **`93.44 %`** della crescita di `H` ### **a `A` fissa**, e ### **non costa coerenza** *(`AUC` al `400` da `0.9394` a `0.9333`)*: ### **pompava senza ordinare** |
| ### **l'orologio privato `α` dello spinore** | `_psi_spinor` ha una fase comune ### **sua**, diversa da `φ/2`: ### **MISURATO `rms(wrap(α − φ/2)) = 1.9716` radianti** *(mediana `1.7377`)*. ### ⛔ **`A16.1` dice UN SOLO orologio per nodo**, e oggi ce ne sono ### **due** |

---

# ③ CHE COSA DEVE RINASCERE IN FORMA NUOVA — **e non è ancora scritto**

| che cosa | il vincolo che `A16` impone |
|---|---|
| ### **le nascite** | devono ### **conservare la norma totale** *(`A16.4`, `A14.3`)*: la norma è la ### **carica di Noether della fase**. Oggi la nascita ### **aggiunge** nodi e la norma non è controllata |
| ### **il vuoto locale** | l'oblio e il riscaldamento devono ### **EMERGERE** da `H` come scambio col vuoto *(`A15.3`, `A16.3`)*, non essere un termine additivo |
| ### **le memorie** | ### **gradi di libertà lenti DENTRO `H`**, con la loro parte di energia. ### ⛔ **Nel prototipo `w` e `U` sono FISSI: è la violazione provvisoria dichiarata, ed è il primo passo successivo** |
| ### **la metrica** | `A16` non la nomina. ### **Resta fuori da questo documento**, e resta una decisione di Luca |

---

# ④ I FATTI MISURATI CHE HANNO PORTATO ALLA DECISIONE *(2026-10-07 e 2026-10-08)*

> ### **DA DOVE VIENE OGNI NUMERO**, perche' `L-NUMERI` dice che un numero ricopiato
> non ha provenienza:
>
> | fonte | che cosa |
> |---|---|
> | `doc/REFERTO_h3_termostato_2026-10-07.md` | `AUC`, coerenze, il bilancio, le quote, `W_sync`, `dU_A` |
> | `csv/_test_fork/_termo_h3/*.json` | tutto cio' che il referto genera, e il ricalcolo indipendente |
> | `csv/_test_fork/_termo_h3/collaudo_u2.txt` | `3.494e-16`, `1.054`, `1.9716` *(il collaudo della forma `U(2)`)* |
> | ### ⚠ **`python csv/_test_fork/_termo_h3.py --collaudo`** | `2.55e-06` e `1.18e-01` *(il collaudo del gradiente)*. ### **Questa uscita NON e' committata come file:** si ri-ottiene col comando, che e' nell'inventario -- e lo dichiaro invece di far credere che venga da un referto |
>
> ### ✔ **E sono stati RICALCOLATI dai json uno per uno** *(script di verifica nello scratchpad)*: `230/230`, `+564721.69`, `+394.5614`, `+8804.8634`, `93.44 %`, `51.65 %`, `-22250.2756`, `dU_A +21435.8389` e `-4284.3679`, `AUC` e coerenze. ### ⚠ **E il mio controllo aveva un difetto suo:** sulla quota quadratica metteva le due classi ### **insieme** e dava `99.6` invece di `99.45` *(vuoto)* e `99.42` *(masse)*. ### **Curato il controllo, non il numero.**

| misura | il fatto | il numero |
|---|---|---|
| ### **`D1`** | ### **la coppia POMPA** | `P_coppia` positiva in ### **`230` passi su `230`** nelle masse, somma `+564721.69` |
| `D1` | e lo scuotimento ### **non fa lavoro: inietta varianza** | quota quadratica ### **`99.4 %`** in entrambe le classi |
| ### **`D2`** | una coppia che ### **legge la fase** tiene la coerenza | `AUC` al `400` ### **`0.9020`** contro `0.4679` del controllo |
| ### **`D2-BIS`** | e la tiene ### **anche senza i due forzanti globali** | `AUC` al `400` ### **`0.9394`**, coerenza per massa `0.9024` · `0.9264` · `0.9495` |
| `D2-BIS` | ### **il bilancio dell'energia chiude come identità** | la somma delle voci riproduce `dT` ### **cifra per cifra** |
| `D2-BIS` | ### ⛔ **e la coppia del driver NON è un gradiente** | `1.18e-01` contro `2.55e-06` |
| ### **`D2-TER`** | ### **la sincronizzazione è la sorgente della parte in `φ`** | toglie il ### **`93.44 %`** della crescita a `A` fissa, il `51.65 %` di quella totale |
| `D2-TER` | ### **e NON costa coerenza: pompava senza ordinare** | `AUC` al `400` ### **`0.9333`** senza sync, `0.9891` al `230` *(meglio che col sync)* |
| `D2-TER` | `W_sync` misurato contro la stima dedotta | `−22250.2756` contro `−22251.2229`, rapporto ### **`1.0000`** |
| ### **`D3`** | la forma `U(2)` ### **è** `−∂E/∂φ` di un'energia scritta | identità algebrica ### **`3.494e-16`**, limite `U(1)` ### **esatto** |
| `D3` | ### ⛔ **e la fase dello spinore NON è `φ/2`** | `rms(wrap(α − φ/2))` = ### **`1.9716`** radianti |

### ➜ **LA LETTURA CHE NE ESCE, e che `A16` mette per iscritto:** ciò che tiene le masse è
### **la forma della coppia** *(una coppia che è il gradiente di un'energia che legge la fase
che muove)*; ciò che pompa sono ### **i forzanti e la sincronizzazione**, che ### **non
ordinano**. ### **Quindi non manca una legge in più: ne mancano di meno, e scritte da una sola
`H`.**

---

# ⑤ CHE COSA QUESTO DOCUMENTO NON DICE

| | |
|---|---|
| la ### **forma definitiva** di `H` | ### ⛔ **non la fissa, e `A16` dice che si decide con MISURE.** Il prototipo prova ### **una** forma, non ### **la** forma |
| che il prototipo ### **sostituisca** il simulatore | ### ⛔ **no.** È un ### **banco**, fuori dal simulatore e senza importarlo. Il simulatore resta `b8c21049` |
| che la simulazione sia ### **meccanica quantistica** | ### **no**, e `A16` lo dice da sé: su un grafo di migliaia di nodi è ### **un campo con la FORMA della dinamica quantistica**, non uno stato a molti corpi |
| ### **la memoria dinamica, le nascite, il vuoto** | ### **decisioni successive di Luca.** Nel prototipo `w` e `U` sono ### **fissi**, ed è dichiarato come violazione provvisoria di `A16.3` |
| ### **le scale e i semi** | il prototipo gira su ### **`3` semi** e una scansione di ### **`5`** valori di `g`: ### **`P3` non è soddisfatta**, e il documento non pretende il contrario |
