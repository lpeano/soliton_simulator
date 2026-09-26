# CURA **A** — `rho_s/W²` NEL SOLO CONTRASTO (decisione di Luca, 2026-09-26)

*(criteri committati **PRIMA** del codice, par.5-septies.)*

## LA MODIFICA: **una potenza**, nessun flag nuovo

Dentro `CONTRASTO_INTENSIVO`, il denominatore passa da **`W`** a **`W²`**:

```
PRIMA   _rho_c = rho_s / W          (variante pesata, misurata: dimezzava il divario, non bastava)
ORA     _rho_c = rho_s / W^2
```

**`rho_s` resta INVARIATO in `mitosi`, nello Schwinger e in `lambda_nodi`** — la cura tocca
**l'inerzia**, non **il campo**. *(Le sette letture fuori da `_passo_spinoriale` sono elencate in
`doc/LETTURE_rho_s.md`; `C3` lo verifica con la byte-identità.)*

## PERCHÉ `W²` E NON `W` — **misurato, non dedotto**

```
rho ~ ramp^2.74      W ~ ramp^1.37      ->   rho ~ W^(2.74/1.37) = W^2.00      (R2 0.95-0.96)
```

**`2.00` esatto**, su due semi. `rho_s` è il **modulo quadro** di una somma pesata: dividere per `W`
**una volta** toglieva **una** potenza — e infatti la variante `/W` dimezzava il divario di pendenza
*(`1.25 → 0.62`, `2.78 → 1.44`)* senza chiuderlo.
**E la scomposizione lo conferma dall'altro lato:** `T2` *(il termine `W²`)* è il **`107`-`114 %`**
del divario dei figli.

## I CRITERI, fissati **ORA** — e la previsione numerica viene **dal dato**

| | criterio | soglia |
|---|---|---|
| **`C1'`** | sul **taglio**: pendenza del **contrasto** = quella della **coppia** entro lo **spread fra semi** | `max` differenza ON ≤ `2 ×` spread |
| **`F1`** | sui **FIGLI**: `contrasto_figlio/contrasto_maturo` **allo stesso passo**, età `2..14`, 2 semi | **atteso `exp(T1+T3) ≈ 2.5`**, accettabile **fra `1.5` e `4`** |
| **`F2`** | **OMEGA DEI FIGLI**: `|omega|_figlio / |omega|_maturo` **allo stesso passo**, dall'età 2 | **`< 10`** |
| **`C3`** | **località**: byte-identità sui campi che **non devono** cambiare, flag SPENTO contro il codice **precedente** | `0` campi diversi |
| **`C5`** | il **pavimento** `1e-6`: quante volte morde | `0` |
| **`P1-sexies`** | **il braccio con `/W` DEVE FALLIRE `C1'`** | il caso che deve fallire |

### `F1`: LA PREVISIONE È **CALCOLATA DAI DATI**, non scelta

```
exp(T1+T3), tutte le eta' e i due semi (n=26):   min 2.3265   mediana 2.4567   max 2.5387
```

**Dopo la cura il contrasto del figlio deve essere ~`2.5` volte quello dei maturi** — *più grande*,
perché `T1+T3 > 0`. **La banda misurata è `2.33`-`2.54`**, quindi la soglia `1.5`-`4` di Luca
**non fallirà per rumore**: se `F1` cade, cade per una ragione.

### `F2`: E **SE FALLISCE, NON SI CURA** — si identifica il termine e **STOP**

> **Ordine esplicito di Luca:** *«se FALLISCE con il contrasto a posto, la causa di `omega` è **un
> altro termine**: identificalo (quale addendo di `omega_new` domina sui figli) e **STOP, nessuna
> seconda cura**».*

Gli addendi da pesare, dal codice:

```
omega_new = omega_src + dt_n * ( correzione/inerzia  -  omega_src/_tau )
correzione = cross(B, nb)  +  _tq*ramp   [+ altri termini gated]
```

Quindi i candidati sono: **`omega_src`** *(la memoria: se domina, `omega` dei figli è EREDITATO o
accumulato, non prodotto dal rapporto)*, **`correzione/inerzia`** *(il termine che la cura tocca)*,
**`omega_src/_tau`** *(il freno)*. **Si misurano i tre in modulo, sui figli e sui maturi, allo
stesso passo** — e il referto dice **quale domina**, senza proporre nulla.

## COSA MI FAREBBE FERMARE

- **`C3` che cade → STOP**: la cura non è locale, e il referto lo dice invece di essere aggiustato.
- **`F1` fuori banda verso l'ALTO** *(contrasto del figlio ≫ 4× i maturi)*: la cura **rovescia** il
  divario invece di chiuderlo — sarebbe una sovracorrezione, e va detta così.
- **`C5` che comincia a mordere**: dividere per `W²` abbassa l'inerzia **due volte**, quindi il
  pavimento è il rischio vero di questa cura. *(Con `/W` non mordeva: `min 0.0655`, quattro ordini
  sopra. Con `/W²` la scala scende ancora di `~1/W`, e **va misurato, non sperato**.)*

## COSA QUESTA CURA **NON** RISOLVE, e va scritto prima

- ~~**`R3bis` è caduto**: l'asimmetria è `0` contro `2.8`, e `W²` ne toglie `2` — **resta
  `0.8`**.~~ **❌ ERRORE DI UNITÀ MIO, corretto il 2026-09-26 (rilievo di Luca), e la versione
  vecchia resta leggibile qui sopra:** avevo sottratto **2 potenze di `W`** da **2.8 potenze di
  `ramp`**. **Il conto giusto:** `W ~ ramp^1.37` → `W² ~ ramp^2.74`, quindi
  `inerzia/W² ~ ramp^0.06`, e contro la coppia (`ramp^0.10`) il residuo è **`-0.04`: zero entro
  il rumore.** **E il dato lo diceva già:** `exp(T1+T3)` è **piatto** (`×1.00`-`×1.08`) mentre
  `ramp` cresce `×5.20` — con `0.8` potenze varierebbe di **`×3.74`**.
  ⇒ **`W²` chiude l'esponente**, e la mia frase era **troppo pessimista**.
- **il taglio non è i figli**: `C1'` e `F1` guardano due popolazioni diverse, e possono dare esiti
  diversi. **Se succede, si riporta, non si sceglie quale contare.**
