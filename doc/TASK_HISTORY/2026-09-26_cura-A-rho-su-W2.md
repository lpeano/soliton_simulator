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

---

# ✅ **`C1'` SI CHIUDE CON 4 SEMI — criterio scritto PRIMA** *(decisione di Luca, 2026-09-26)*

> **❌ LA SOGLIA NON SI CAMBIA DOPO AVER VISTO I NUMERI.** La mia proposta *«un decimo di OFF»*
> avrebbe dato `0.12` contro `0.125`: **passerebbe per un margine del 4 %, ed e' una soglia
> SCELTA SUL DATO.** Luca la rifiuta, e ha ragione: sarebbe `P1-sexies` violato nel modo piu'
> elegante — una soglia che *sembra* derivata perche' si riferisce al braccio OFF, ma il cui
> valore (`1/10`) e' stato scelto **guardando il risultato**.

## IL CRITERIO NUOVO, e il difetto di quello vecchio

**Il vecchio:** `max(|Δpend| ON) <= 2 x std(|Δpend| ON)`. **Auto-referenziale**: la soglia si
stringe **con** i valori che deve giudicare, e nel limite di una cura perfetta **tende a zero**.

**Il nuovo, deciso da Luca** — e `P3` delle regole lo impone comunque *(per una barra fra semi
servono `>= 4` semi)*:

```
C1''''  su 4 SEMI:
   (a) media( |pend(contrasto) - pend(coppia)| ) ON  e' COMPATIBILE CON ZERO
       entro 2 ERRORI STANDARD sui 4 semi        ->   media <= 2 * SE,  SE = std/sqrt(4)
   (b) e sta SOTTO quella di `/W`                ->   media_ON < media_suW
```

**Perche' e' sano dove il vecchio non lo era:** la soglia e' **l'errore della media**, non la
dispersione dei valori; e `(b)` ancora il giudizio a **un'altra popolazione misurata** — il braccio
`/W` — invece che a se stesso. **Nessun numero scelto:** il `2` degli errori standard e' la
convenzione statistica, non una taratura *(e con 4 semi `t(0.025,3) = 3.18`, quindi `2 SE` e'
**piu' severo** di un IC95 vero: lo dichiaro invece di spacciarlo per equivalente)*.

**SOLO IL TAGLIO, nessun'altra modifica** *(ordine di Luca)*: `F1`, `F2`, `C3`, `C5` sono gia'
chiusi a 2 semi e **non si rifanno**.

**COSA MI FAREBBE FERMARE:** se `(a)` passa e `(b)` no — cioe' la media ON e' compatibile con zero
**ma non piu' piccola** di quella di `/W` — allora **il criterio non distingue le due forme** e il
`PASS` sarebbe casuale. **Si riporta, non si sceglie.**

---

# 🔁 **IL CRITERIO `(a)` SI CORREGGE IN `(a')`: LE DIFFERENZE SI PRENDONO COL SEGNO**
*(rilievo di Luca, 2026-09-26; **il motivo e' un COLLAUDO, non il dato**)*

## I DUE CRITERI, FIANCO A FIANCO

```
(a)   VECCHIO      media( |pend(contrasto) - pend(coppia)| )  <=  2 * SE( |...| )
(a')  NUOVO      | media(  pend(contrasto) - pend(coppia)  ) |  <=  2 * SE( ... )
                                      ^^^^^^^^^^^^^^^^^^ FIRMATE, senza valore assoluto
(b)   INVARIATO    la media ON sta SOTTO quella del braccio `/W`
```

**L'unica differenza e' il VALORE ASSOLUTO**, e cambia tutto: **una media di quantita' tutte
positive non puo' essere compatibile con zero.** Il suo valore atteso e' `> 0` **per costruzione**,
qualunque cosa faccia la cura.

## ⚠ **IL MOTIVO DEL CAMBIO E' IL COLLAUDO, NON IL DATO — e la distinzione e' il punto**

`P1-sexies` vieta di aggiustare un criterio **dopo aver visto i numeri**. Qui il criterio si cambia
perche' un **collaudo su un caso a risposta nota** dimostra che **non era soddisfacibile**, e quel
collaudo e' stato **scritto e committato PRIMA** di rileggere i numeri veri
*(`csv/_collaudo_criterio_zero.py`, `aae56ba`; esito `ecf1e2c`)*:

```
su RUMORE PURO -- 4 valori N(0,s), 1e5 prove, seme fisso: la CURA PERFETTA, solo dispersione
   con |x|      passa il 14.11 %   ->  FALLISCE l'85.89 %,  media/SE tipica 2.897
   col SEGNO    passa l'86.13 %                            (= P(|t_3| <= 2), esatto)
```

> ### **Un criterio che fallisce l'86 % delle volte quando NON c'e' niente da trovare non misura
> ### la cura: misura se stesso.** Il suo `FAIL` sui dati veri **non era un riscontro**.

**E la forma nuova non e' «piu' larga»: e' `t_3` contro `2`**, cioe' la statistica ordinaria. Passa
l'86 % sul nulla — **non il 100 %** — quindi un suo `FAIL` **resterebbe** informativo.

## ESITO, dai json GIA' SCRITTI *(nessun rigiro del simulatore)*

`csv/_seal_fork/_c1_col_segno.py` -> `csv/_seal_fork/_sig_cura_A/C1_COL_SEGNO.txt`

```
verso    differenze FIRMATE                        media     SE       |media|/SE   esito
corti    +0.1167  +0.0535  +0.0090  -0.0247        +0.0386   0.0306   1.2640       COMPATIBILE
lunghi   +0.0115  +0.0519  +0.1533  -0.0511        +0.0414   0.0429   0.9656       COMPATIBILE
(b)      corti  ON 0.0510 < /W 1.3774 (x27)   lunghi  ON 0.0669 < /W 0.6749 (x10)  PASS
```

**Il numero esce dallo SCRIPT e coincide con quello che il guardiano aveva calcolato dal referto**
*(atteso `0.97` lunghi, `1.26` corti; misurato `0.9656` e `1.2640`)*. **Lo dico anche se coincide:**
la verifica era chiesta perche' un numero d'accordo per caso e un numero d'accordo per costruzione
si distinguono solo dichiarandolo.

**⚠ E IL LIMITE, col verso GIUSTO** *(la mia prima formulazione lo aveva invertito, corretta da Luca
in `9d9c44a`)*: con semi **CORRELATI** la `SE` calcolata dai 4 valori **SOTTOSTIMA** quella vera,
quindi `|media|/SE` e' **GONFIATO** e il criterio fallisce **PIU'** spesso. Il rischio e' un
**residuo FALSO**, non un `PASS` regalato: **un `PASS` resta informativo, un `FAIL` andrebbe
guardato due volte.** **La correlazione fra i semi NON e' misurata.**
