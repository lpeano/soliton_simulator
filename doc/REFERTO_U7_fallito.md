# REFERTO — **U7 FALLISCE**, e sotto c'è un difetto di INDICIZZAZIONE che lo precede

> **2026-09-17.** Branch `fork-su2`, blob **`827d3bf8`** (= `HEAD`, byte grezzi, 0 CRLF), HEAD `31922ff`.
> **NESSUN RUN DI MISURA. NESSUN CABLAGGIO. NESSUNA PREDIZIONE NUMERICA.**
> Strumento: `csv/_seal_fork/_u7_separazione_scale.py` -> `.txt`. Dati: `.pkl` gia' committati.
>
> **Il mandato ordina: «Se un sigillo fallisce — U5 e U7 in particolare — committa il fallimento e
> FERMATI.» E' quello che fa questo file.**

---

## 0. IL VERDETTO IN QUATTRO RIGHE

> 1. **`doc/ASSIOMI.md` NON ESISTE sul disco.** Il mandato lo cita come riferimento e chiede che ogni
>    correzione dichiari **quale assioma soddisfa**. **Non posso verificare contro un documento che
>    non c'e'**: leggo A1-A7 **dall'uso che ne fa il mandato stesso**, e lo dichiaro.
> 2. **U7a: il FAIL si RILEGGE** (rilievo del guardiano, verificato e corretto nel meccanismo, §1-bis).
>    Lo **0.2655 %** sotto 1 **non e' transitorio di nascita** (archi col rapporto `1.0` esatto: **ZERO**)
>    **ma il VUOTO PIU' PROFONDO**: densita' mediana **4000 volte** piu' bassa, **100 %** sotto il p10.
>    **Fisiologico: non e' una violazione di A5, e' una localizzazione.**
> 3. **U7b FALLISCE, ed e' peggio:** `max(dt_e/tau_p) = 34629`. Non e' un'imprecisione, e'
>    **divergenza numerica** su ~0.11 % degli archi.
> 4. **⚠ E SOTTO C'E' ALTRO:** `d_arco` — il `d` che entra in `tau_p_loc` — e' calcolato
>    **indicizzando un array PER ARCO con indici di NODO** (`:3236`, `:3238`). **Correlazione con la
>    lunghezza vera dell'arco: −0.349.** **Anticorrelato.**

---

## 1. U7a — `rho_arco/peq >= 1` non vale ovunque (A5)

*(840 604 archi, 4 semi, 500 passi)*

| | valore |
|---|---|
| minimo | **1.36443e-06** |
| p0.1 / p1 / p5 | 0.01085 / 1.104 / 1.239 |
| mediana | 3.338 |
| **frazione sotto 1** | **0.2655 %** (2232 archi) |
| di quelli sotto 1: min / mediana / max | 1.36e-06 / 0.4477 / 0.99998 |

> **Nel caso peggiore `tau_p` varrebbe `1.36e-06` volte il tempo-luce dell'arco:** la forma di riposo
> inseguirebbe la forma attuale **un milione di volte piu' in fretta di quanto un segnale attraversi
> l'arco**.

**Il GATE D diceva «99.7 % sopra 1», ed era vero.** Il mandato chiedeva di guardare **lo 0.3 %**:
guardato, e **non e' una coda benigna** — non si ferma poco sotto 1, arriva a **1e-06**.

> **⚠ QUESTO PARAGRAFO REGISTRA IL NUMERO, NON IL VERDETTO.** La lettura *«A5 violato»* — che era la
> mia prima — **e' stata CORRETTA dal §1-bis**: quegli archi sono **il vuoto piu' profondo**, e li'
> la violazione **non c'e', perche' non c'e' niente da rilassare**. Si legga §1-bis prima di trarre
> conclusioni da questa tabella.

---

## 1-bis. IL RILIEVO DEL GUARDIANO: **conclusione GIUSTA, meccanismo SBAGLIATO** - e la versione corretta e' piu' forte

**Il rilievo:** *«`peq` e' `rho` lisciato, e un campo lisciato sta sempre SOTTO i picchi: quindi
`rho/peq >= 1` per costruzione. Lo 0.3 % sotto 1 sono archi dove `peq` non ha ancora lisciato -
archi appena nati (`peq` inizializzato a `rho`, `:3137`) o in transitorio. `U7` non e' un
falsificatore, e' una verifica che il lisciamento funzioni.»*

**L'ipotesi e' TESTABILE, e l'ho testata invece di accettarla.**

### 1-bis.1 - Il meccanismo proposto NON regge

> Se quegli archi fossero **appena inizializzati**, `peq` varrebbe **esattamente `rho`** (`:3137`),
> quindi il rapporto sarebbe **`1.0` ESATTO - non SOTTO 1.**

```
archi con rho/peq == 1 ESATTO :  0   (0.0000 %)      <- la popolazione "appena nata" e' VUOTA
archi con rho/peq  < 1        :  2232  (0.2655 %)
```

**Al passo 500 non c'e' un solo arco appena inizializzato.** Il transitorio di nascita **non spiega
lo 0.3 %.**

### 1-bis.2 - Ma la conclusione e' giusta, e la ragione vera e' **piu' forte**

Un campo lisciato non solo **abbassa i picchi**: **alza le valli**. E' la stessa proprieta', vista
dall'altro lato. Quindi `rho/peq < 1` dev'essere **il vuoto**, non il transitorio. **Misurato:**

| popolazione | `rho_arco` mediana | `peq` mediana | `rho/peq` mediana |
|---|---|---|---|
| tutti | 5.44e-02 | 2.14e-02 | 3.338 |
| **sopra 1** | 5.45e-02 | 2.14e-02 | 3.373 |
| **SOTTO 1** | **1.33e-05** | 4.91e-03 | 0.4477 |

> ### **Gli archi sotto 1 hanno una densita' MEDIANA QUATTROMILA VOLTE PIU' BASSA.**
> ### E il **100 %** di essi sta sotto il **p10** della distribuzione di densita' - contro il 10 %
> ### che ci si aspetterebbe per caso.

**Non sono archi giovani: sono archi VUOTI.** Il lisciamento li alza perche' i vicini hanno piu'
materia di loro. **La separazione di scale non e' imposta: e' garantita dove c'e' struttura, e cade
esattamente dove non c'e' niente da rilassare.** *(E' la formulazione del guardiano, con il
meccanismo corretto: valli del campo, non transitorio di nascita.)*

> **QUINDI SI', `U7a` cambia natura: non e' un falsificatore, e' una LOCALIZZAZIONE.** Dice
> **dove** il rapporto scende sotto 1, e la risposta - **il vuoto piu' profondo** - e' fisiologica.
> **Correggo il verdetto di `U7a` di conseguenza.**

### 1-bis.3 - MA QUESTO NON SBLOCCA `U7b`, E IL MOTIVO E' PROPRIO QUELLO

**Il riquadro qui sopra dice che in quegli archi `tau_p` diventa PICCOLO.** Ed e' esattamente li'
che `dt_e/tau_p` esplode a **34629**. **La rilettura fisiologica di `U7a` non rende stabile `U7b`:
la spiega.**

> **Un arco vuoto non ha niente da rilassare - vero. Ma il codice ci integra sopra lo stesso**, e
> `d0 += dt_e*(d - d0)/tau_p` con `dt_e/tau_p = 34629` **non rilassa verso `d`: diverge oscillando.**
> **La fisica dice "irrilevante", l'aritmetica dice "NaN".**

**Cosa lo sbloccherebbe, e non lo decido io:** un **limite inferiore causale** su `tau_p`
(`tau_p >= d/cs`, cioe' `max(rapporto, 1)`) renderebbe `U7a` vero **per costruzione** e `U7b`
automaticamente soddisfatto - **ma e' un `max(..., 1)`, cioe' un pavimento**, e questo giro nasce
per **togliere** pavimenti. **La tensione va decisa, non risolta da me.**

---

## 2. U7b — `dt_e / tau_p < 1` non vale ovunque: **divergenza**

| | valore |
|---|---|
| mediana | 0.00712 |
| p99 | 0.04015 |
| **massimo** | **34629** |
| frazione `>= 1` | **0.1127 %** |

`self.d0 += dt_e * (self.d - self.d0) / tau_p_loc`. Con `dt_e/tau_p = 34629` l'incremento vale
**34629 volte** lo scarto `(d - d0)`: **`d0` non converge, esplode oscillando.**

> **Questa non e' una violazione di principio: e' un'instabilita' dell'integratore.** Su ~950 archi
> per run. **La forma proposta per ④, cablata cosi', romperebbe il sistema.**

---

## 3. ⚠ IL DIFETTO CHE STA SOTTO: `d_arco` indicizza un array PER ARCO con indici di NODO

```python
:3236   d_arco = 0.5 * (self.d0[self.i] + self.d0[self.j])    # ramo TAU_USA_D0 (spento)
:3238   d_arco = 0.5 * (self.d[self.i]  + self.d[self.j])     # <- IL RAMO CHE GIRA
```

**Verificato dal disco:** `self.d` e `self.d0` hanno **210 422** elementi (**per ARCO**); `self.i` e
`self.j` sono **indici di NODO** (`max = 3483`, con `n = 3484`).

> **`self.d[self.i]` prende quindi l'arco numero `i`, dove `i` e' l'identificativo di un NODO.**
> Tocca **solo i primi 3484 archi su 210 422**: il **98.34 %** degli archi non e' mai letto, e il
> valore assegnato all'arco `k` non ha relazione con l'arco `k`.

**Quanto conta, misurato:**

| `d_arco` | mediana | p05 | p95 | min | max |
|---|---|---|---|---|---|
| **come lo calcola il codice** | 1.39934 | 1.33419 | 2.25770 | 1.00698 | 3.49451 |
| **la lunghezza vera `d`** | 1.47671 | 1.33242 | 1.55092 | **0.05883** | 3.72718 |

> ### **Correlazione fra le due: −0.349.** Non e' un'approssimazione imprecisa: e' **anticorrelata**.

**Conseguenza per ④:** `tau_p_loc = (d_arco/cs) * fattore` — il *«tempo-luce dell'arco»* che compare
nella formula **non e' il tempo-luce di quell'arco**. **Correggere il fattore lasciando `d_arco`
com'e' significa raffinare il secondo fattore di un prodotto il cui primo fattore e' sbagliato.**

**Cosa NON dice questo reperto:** che la cura sia `d_arco = self.d`. **Lo sembra** — `d` *e'* la
lunghezza dell'arco, e nessuna media serve — **ma cambiarlo sposta `tau_p_loc` su tutti gli archi,
ed e' una modifica di regime che va decisa, non dedotta da me.** *(E la stessa domanda si pone per
`:3236`, oggi spento: `TAU_USA_D0 = False`, acceso solo da `--tau-d0`.)*

**Nota di igiene:** la scansione su **tutti** gli array per-arco (`d0`, `d`, `peq`, `tw`, `twp`,
`vd`, `g`) indicizzati con `self.i`/`self.j` trova **solo queste due righe**. Il difetto e'
**confinato**, non sistemico. *(Poche righe sopra, `lap = 0.5*(med[i] + med[j]) - q` usa lo stesso
schema ma su `med`, che e' **per NODO**: li' e' **corretto**. Lo schema `X[i]` e' giusto o sbagliato
**a seconda di cosa sia `X`**, ed e' per questo che un occhio distratto non lo vede.)*

---

## 4. `doc/ASSIOMI.md` NON ESISTE

```
ls doc/ASSIOMI.md      -> non esiste
ls doc/ | grep -i assio -> nessun file
```

Il mandato lo mette fra i riferimenti di §0-bis e ordina: *«ogni correzione porta accanto quale
assioma soddisfa»*. **Non posso verificare contro un documento assente.**

**Come ho letto A1-A7 in questo referto — dichiarato, non assunto:** dall'**uso** che il mandato
stesso ne fa (A1 = zero parametri/derivato; A2 = localita'; A3 = nessuna scala assoluta; A4 = tempo
proprio locale; A5 = causalita'; A7 = niente cricchetti senza stato). **E' un'inferenza mia da
contesto, non una lettura.** *(P1: non ho un fatto stabilito su questo, sto leggendo per analogia.)*

**Serve il file**, oppure che gli assiomi vengano dettati: finche' non c'e', la clausola §0④ non e'
verificabile — e una regola non verificabile non protegge.

---

## 5. COSA E' PRONTO, E COSA NO

| | stato |
|---|---|
| **① `inerzia`** | **GATE A e B superati.** Nessun ostacolo noto. **Non cablata** (U7 blocca il giro) |
| **② `spinta`** | dipende da `_rep` di ③. Nessun ostacolo proprio |
| **③ `_rep`** | realizzabile. Servono: snapshot di `dt_e` su `self`, estensione a `:1855`/`:3482`/`:3560` col pattern di `peq`, contatore su `:3360` |
| **④ plasticita'** | **BLOCCATA da U7a e U7b, e da `d_arco` (§3)** |
| **⑤ `spin_locale`** | rimozione di codice morto. Nessun ostacolo |
| **⑥ `_floor_d0`** | sospesa per decisione, come da mandato |

**NON ho cablato nulla, NON ho lanciato run di misura, NON ho scritto predizioni numeriche.**
**NON ho misurato ne' riportato:** `chi`, `|<n>|`, autocorrelazione, `theta`, `omega/sqrt(n)`,
`L_tot`, MISURA U, `cs_std/cs`.

**Provenienza:** i `.pkl` sono del blob **`a44adc31`**. Per U7 la domanda e' **strutturale** (una
frazione viola un vincolo?), e il `cs_floor` relazionale cambia i **valori**, non la **forma** della
domanda — **ma il numero esatto della frazione andra' riconfermato sul blob attuale.**
