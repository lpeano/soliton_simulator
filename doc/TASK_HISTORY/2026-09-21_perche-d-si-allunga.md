# 2026-09-21 — **PERCHE' UN ARCO SI ALLUNGA 150 VOLTE?** `TRACCIA_VD`

Mandato: misurare **chi spinge `d`**, col metodo che ha funzionato per `d0`. **Nessuna cura.**
Simulatore all'avvio `01146a16`. HEAD `78f0efd`. **Nessun run attivo: la macchina e' libera.**

---

## 1. RAGIONAMENTO PRELIMINARE

### 1.1 Perche' la domanda si e' spostata — **da un mio numero, non da un'ipotesi**

Imporre `d0 >= LAM` limita lo stress a `d_max/LAM - 1`. **Guadagno misurato: `10.9x`-`21.1x`.**
**Ma nel ramo B al passo 360 il limite resta `185.4`, perche' `d_max = 149.1`.**
> **La cura ferma il DENOMINATORE. Il NUMERATORE continua a crescere.**
> **E nella rigiocata `0 -> 120` `d` cresce LISCIO e MONOTONO (`x2.7`) mentre `d0` SALTA (`x0.33`):
> ci siamo concentrati su `d0` perche' saltava, e `d` non l'ha guardato nessuno.**

### 1.2 Cio' che il codice dice GIA', letto ieri e da non ri-dedurre

```
acc = cs_arco^2 * lap  +  src  -  beta * vd          (tre termini, verificati su tutte le occorrenze)

lap  = 0.5*(med[i]+med[j]) - q   con q = d - d0   -> laplaciano dell'ALLUNGAMENTO, non di `d`
src  = ALPHA_M * (rho - peq)/max(peq, 1e-9)       -> ⚠ `peq` AL DENOMINATORE, e `peq` DEGENERA
beta = 2*ZETA_M*cs / max(d, 1e-6)                 -> ⚠⚠ INVERSAMENTE proporzionale a `d`
```
**Due dei tre si amplificano nella direzione del guaio. Il terzo diffonde l'allungamento.**

### 1.3 Cosa NON so

- **non so quale dei tre domini**, ne' se lo stesso domini sull'arco e sulla popolazione
  *(`Z79` ha insegnato che le due letture possono divergere ed essere vere entrambe)*;
- **non so se `beta` sia gia' debole al passo 120** o se lo diventi dopo: `d` a `1.97` da'
  `beta ~ 2*0.75*2/1.97 = 1.52`, che **non** e' piccolo. **Il collasso del freno, se c'e', e' piu'
  in la';**
- **non so se `src` sia gia' anomalo prima del 120:** `peq` degenera **1 volta** entro il 120 in
  B *(il transitorio)*, e **14 entro il 240**. **La finestra `0 -> 120` potrebbe non vederlo.**

### 1.4 Cosa mi aspetto (**non si riscrive se sbagliato**)

- **mi aspetto che nella finestra `0 -> 120` domini `cs^2*lap`**, perche' e' l'unico termine
  proporzionale a `cs^2 = 4` e l'allungamento c'e' gia';
- **mi aspetto che `beta*vd` sia un freno REALE ma non sufficiente** a `d ~ 2`;
- **mi aspetto che `src` sia piccolo nella finestra `0 -> 120`** e che diventi protagonista dopo il
  240, insieme alla degenerazione di `peq`. **Se cosi' fosse, questa misura NON vedrebbe la seconda
  fase, e lo dico prima.**

---

## 2. PROGETTAZIONE

### 2.1 La forma — **la stessa di `TRACCIA_D0`, che ha funzionato**
Sotto **`TRACCIA_VD`** *(`False` di default)*, dentro il ramo `VERLET` di `step`, **subito dopo il
calcolo di `acc_t`**: si registrano i **TRE contributi SEPARATI, col segno**, piu' `d`, `vd`, `d0`,
`d - d0`, `beta`, `cs_arco`.

**TRE LIVELLI, come per `d0`:**
```
DETTAGLIO   l'arco 16-481, cercato per COPPIA DI NODI (mai per indice)
RIASSUNTO   gli archi dei cinque nodi: p50 e max di ciascun termine, col segno
GLOBALE     quante volte il sito e' girato
```
**⚠ I tre termini si registrano SEPARATI e NON la loro somma:** la somma e' `acc`, che gia' si
vedrebbe da `vd`. **La domanda e' la RIPARTIZIONE.**

### 2.2 ⚠ E LE DUE GUARDIE, che stanotte sono servite due volte
- **se `--traccia-vd` e' chiesto e il log resta VUOTO -> ESCE CON ERRORE;**
- **se la tabella per-arco non ha righe -> ESCE CON ERRORE.**
> **Due difetti della stessa famiglia in un giro** *(`--traccia` letto dopo aver sovrascritto
> `sys.argv`; `_passo_corrente` mai impostato)*, **entrambi silenziosi.** `A8` applicato a me.

### 2.3 Il costo
`19` siti di `d0` costavano una `copy()` ciascuno. **Qui i termini sono gia' calcolati: si leggono,
non si ricopia niente.** **A flag spento e' un `if` su una globale.** La rigiocata resta **~9 min**.

### 2.4 LE LETTURE, fissate qui (sono quelle del mandato)
```
UN termine domina verso l'esterno   -> e' il motore dell'allungamento
`src` domina                        -> si collega alla seconda fase di B, voce aperta insieme
`cs^2*lap` domina                   -> la propagazione allunga: si guarda `lap` di COSA
`-beta*vd` troppo debole            -> non c'e' motore: manca il FRENO, sistema sottosmorzato
nessuno spiega il profilo liscio    -> SI DICE
```

### 2.5 Cosa mi FERMA
- **`Z1` (byte-identita' a flag spento) che fallisce** -> STOP;
- **`Z3` (la rigiocata non riproduce piu' il ramo B col flag acceso)** -> si corregge, non si
  giustifica.

---

## 3. TODO
1. [x] `§5.1` le due verifiche -> **l'asimmetria del pavimento NON esiste; `d` e' integrato da `vd`**
2. [x] `§5.2` l'enumerazione -> **tre termini, e due si amplificano da soli**
3. [ ] la strumentazione `TRACCIA_VD`, **committata PRIMA del sigillo**
4. [ ] **Z0-Z4** -> **se `Z1` o `Z3` falliscono, STOP**
5. [ ] la rigiocata `0 -> 120` -> **la tabella: chi spinge `d`, sull'arco E sulla popolazione**
6. [ ] la voce nel registro -> CHECKPOINT
