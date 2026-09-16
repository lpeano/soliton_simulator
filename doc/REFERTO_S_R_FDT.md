# REFERTO — voce **S**, voce **R**, dispersione di `r`, e il conto **FDT** rifatto

> **2026-09-16.** Blob **`08784685`** (invariato). Branch `fork-su2`.
> **8 run, 2 bracci x 4 semi, 500 passi.** Quattro nuovi (semi 3 e 4) + i quattro del 2026-09-15.
> Dati: `csv/_test_fork/_vuoto_cs{OFF,ON}_s{1,2,3,4}.vuoto.csv` · verdetto:
> `csv/_test_fork/_verdetto_S_R.txt` · analisi: `csv/_test_fork/_verdetto_S_R.py` (`e43b5911`).
> Osservatore `_osserva_vuoto.py` (`54faf42d`), **sigillo 6/6 PASS**.
> **MISURA F: 0 campioni falliti su 44.**
>
> **Tutte le barre qui sono FRA SEMI** (P3 / C10), col `t` di Student per i gradi di liberta'
> effettivi: `t(3) = 3.182` dove i semi sono 4, `t(1) = 12.706` dove sono 2. **Mai 1.96.**

---

## ⚠ 0. LA COSA DA LEGGERE PRIMA DI TUTTO IL RESTO — **due `theta` diversi**

> **`t3_b_theta` di questo referto NON e' confrontabile con i numeri T3 gia' committati.**
>
> | | formula | tempo |
> |---|---|---|
> | `_rimisura_t3.py` `:73` — i numeri di **C8** (`-0.4745`, `-0.4265`, `-0.1685`…) | `theta = \|omega\| * DT` | **di COORDINATA** |
> | **MISURA F** `_osserva_vuoto.py` `:389` — i numeri di **questo referto** | `theta = \|omega\| * dt_n`, `dt_n = DT*r` | **PROPRIO** |
>
> **Non sono la stessa osservabile**, e le due pendenze differiscono di `d(log r)/d(log inerzia)`.
> **Quella fisicamente giusta e' la seconda** — `CLAUDE.md` §9: *«IL TIC DEI PROCESSI LOCALI E'
> `dt_n = DT*r`, NON `DT`; `DT` nudo e' il tempo di coordinata»*. Ma **l'attesa `-0.69` e tutti i
> confronti di C8 sono nella convenzione VECCHIA.**
>
> **Percio' la frase «la FASE 2 centra il bersaglio» NON si puo' dire**, per quanto il
> `theta_ON = -0.660` sembri cadere a `0.030` dal `-0.69`. **Sarebbe confrontare due grandezze
> diverse e chiamarlo accordo.** Lo si vede anche dal braccio OFF, che si muove nello stesso verso
> (`-0.10` -> `-0.075`) **senza che nulla lo giustifichi**: il segnale e' della convenzione, non
> della maturazione.
>
> **Costo per chiuderlo: una riga** — la stessa `g` di MISURA F contiene gia' `om_src` e `dtn`,
> basta scrivere **anche** `theta_coord = |omega|*DT` e rifare il confronto a parita' di
> definizione. **Non fatto oggi.**

---

## 1. VOCE **S** — `chi` materia: **si chiude come RUMORE**, per il criterio scritto prima

**Il criterio, da `doc/RAMIFICAZIONI.md` D.2/S, non ritoccato:** *segno concorde su 4 semi per
braccio **E** IC95 (con `t(3)`) che **esclude** 90 -> prima firma non nulla. IC95 che **contiene**
90 -> S si chiude come **rumore**, come si e' chiusa `|<n>|` (C15).*

| braccio | s1 | s2 | s3 | s4 | media | sd | **IC95 (t(3))** | esclude 90? |
|---|---|---|---|---|---|---|---|---|
| **OFF** | 89.778 | 89.876 | **89.9999** | 89.835 | **89.872** | 0.094 | **[89.722, 90.022]** | **NO** |
| **ON** | 90.048 | 90.085 | 90.003 | 90.060 | **90.049** | 0.034 | **[89.995, 90.103]** | **NO** |

> ### **S SI CHIUDE COME RUMORE. L'ipotesi si RITIRA, non si raffina** (presidio di CLAUDE.md §9).

**E il segno concorde non regge nemmeno come indizio residuo:** `OFF s3` vale **89.9999**, cioe' uno
scarto di **−0.0001** — e' il **null esatto**, non un valore «sotto 90». Su quattro semi, uno e'
esattamente sulla riga.

### 1-bis. **MA c'e' un fatto nuovo che il criterio non copriva, e va riportato separato**

```
CONTRASTO ON - OFF = +0.1769 +- 0.0500    IC95 [+0.0177, +0.3362]   (t(3)=3.182)
-> ESCLUDE lo ZERO
```

**Non e' «S e' un segnale».** S chiedeva *«`chi` si stacca dal casuale?»*: **no**. Questo dice
un'altra cosa: **`--tau-luce` sposta `chi` di +0.18 gradi rispetto a OFF.** Sono due domande
diverse e vanno tenute diverse.

> **⚠ E IL CONFONDENTE E' ENORME, quindi va detto insieme al numero:** i due bracci **non
> differiscono solo per la legge di `tau`**: differiscono per **`theta`, di un fattore ~7**
> (**91.5-105.2** giri/passo OFF contro **11.9-16.5** ON). **Un settore campionato sette volte
> meglio puo' dare una `chi` diversa per ragioni di CAMPIONAMENTO, non di fisica.** Finche'
> **entrambi** i bracci sono aliasati — e lo sono, `fr>360g` vale **0.99** OFF e **0.75-0.85** ON —
> **questo contrasto non e' interpretabile come effetto fisico.**
> **Lo chiuderebbe:** un braccio con `theta < 1` giro/passo, oppure un terzo braccio a risoluzione
> intermedia — se il contrasto **scala con la risoluzione**, e' campionamento; se resta costante,
> e' fisica.

### 1-ter. **L'INDETERMINATO di `OFF_s2` era un SEME. Chiuso.**

| | s1 | **s2** | **s3** | **s4** |
|---|---|---|---|---|
| `chi_p90` OFF, `z` interno | −0.48 | **−4.17** | **+0.69** | **+0.39** |

I due semi nuovi hanno **segno OPPOSTO** a quello anomalo, e la dispersione fra semi del braccio OFF
(`sd = 0.374`) e' **due volte e mezzo** quella dell'ON (`0.153`). **`OFF_s2` era un seme anomalo,
non un segnale del braccio OFF.** *(E' la stessa chiusura di C15, e per la stessa ragione giusta:
**piu' dati, non una rilettura**.)*

---

## 2. VOCE **R** — **REFUTATA.** E lo dice il numero piu' pulito del lotto

L'ipotesi: *l'anello `tau -> omega -> phi -> psi -> inerzia -> sigma` mette `sigma` **a valle** di
`tau`, quindi l'attesa `-0.69` — calcolata col `sigma` del braccio vecchio — punterebbe al bersaglio
sbagliato.* Era **l'unica ipotesi sul tavolo che non richiedesse di trovare qualcosa di rotto**, e il
registro la marcava *«va provata per prima»*.

**Se l'anello esistesse, `sigma` dovrebbe cambiare quando cambia `tau`. Cambiando `tau` di DUE
ORDINI DI GRANDEZZA (pendenza `+1.708` -> `+0.020`), `sigma` NON SI MUOVE:**

| braccio | `sigma` s3 | `sigma` s4 | **media** | `tau` medio |
|---|---|---|---|---|
| **OFF** | −1.0498 | −1.0592 | **−1.0545** | **+1.708** |
| **ON** | −1.0562 | −1.0554 | **−1.0558** | **+0.020** |

> ### **Differenza di `sigma` fra i due bracci: `0.0013`. La barra di sistema e' `0.030` (C10).**
> **Ventitre volte piu' piccola del rumore.** `sigma` **non e' a valle di `tau`**: e' indipendente
> da `tau` entro ogni precisione che questo sistema permetta. **L'anello, come meccanismo che
> spieghi il divario, NON C'E'.**

**E l'attesa ricalcolata non chiude il divario: lo PEGGIORA.**

| braccio | `sigma` | `tau` | **attesa = `sigma + tau/2`** | `theta` misurato | **divario** |
|---|---|---|---|---|---|
| **OFF** | −1.0545 | +1.708 | **−0.2004** | −0.0747 | **+0.126** |
| **ON** | −1.0558 | +0.020 | **−1.0456** | −0.6597 | **+0.386**, IC95 [+0.054, +0.718] |

**Nel braccio ON l'IC95 del divario ESCLUDE lo zero.** *(Nell'OFF lo contiene, ma con `t(1) = 12.706`
su due semi quell'IC95 e' largo `1.55`: non dice nulla — vedi §5.)*

**Quindi, e mi fermo qui come prescritto (P1):** l'anello non era la causa. **NON cerco un colpevole
nuovo.** Il fatto da registrare e' che la catena `theta = sigma + tau/2` **lascia un residuo
positivo in ENTRAMBI i bracci**, e che quel residuo **non e' spiegato**.

> **⚠ E c'e' una tensione con C3 che NON risolvo, la dichiaro:** C3 dice che il residuo e'
> **transitorio**, misurato **`0.979 -> 0.010`** fra i passi 50 e 400. Qui, a **500 passi**, vale
> **+0.126** (OFF) e **+0.386** (ON). **O C3 non si estende a questa configurazione, o le due
> misure non sono la stessa cosa** — e il §0 di questo referto dice che c'e' gia' **una** ragione
> nota per cui potrebbero non esserlo (i due `theta`). **Va sciolto prima di usare o C3 o questo
> numero.**

### 2-bis. **Un risultato collaterale che vale piu' di quanto sembri: C1 si riproduce, quattro volte**

`sigma` misurato oggi su **quattro run indipendenti**: **−1.0498, −1.0592, −1.0562, −1.0554**
(`r^2` fra 0.968 e 0.973, `n` fra 2458 e 3019). Il tracing del 2026-09-15 dava **−1.056**.
**Quattro semi, due bracci, due leggi di `tau` diverse, e l'esponente non si muove di 0.01.**
**ESITO (I) — «`omega = coppia/inerzia` porta esattamente il −1 richiesto» — e' confermato in modo
molto piu' forte di come era stato stabilito**, e stavolta con la barra giusta.

---

## 3. LA DISPERSIONE DI `r` — **era rumore.** Il «~10 %» su 2 semi non sopravvive a 4

| braccio | s1 | s2 | s3 | s4 | media | sd | IC95 (t(3)) |
|---|---|---|---|---|---|---|---|
| **OFF** | 0.3935 | 0.3542 | 0.4240 | 0.3461 | **0.3795** | 0.0362 | [0.322, 0.437] |
| **ON** | 0.4283 | 0.3979 | 0.4099 | 0.3337 | **0.3924** | 0.0411 | [0.327, 0.458] |

```
ON - OFF = +0.0130 +- 0.0274    IC95 [-0.0741, +0.1001]   ->  COMPATIBILE CON RUMORE
in relativo: +3.4 %  (su 2 semi sembrava ~10 %)
```

**Il controllo di C12 tiene:** `r_mediana` vale **1.000000** su sette run su otto e **0.999999**
sull'ottavo — cioe' **la costante che deve valere per costruzione**. Serviva a dimostrare che la
dispersione e' l'unico numero libero, e lo dimostra.

> **Quindi la FASE 5 (doppia copertura 4pi) non ha, ad oggi, NESSUN effetto misurabile** — ne' sulla
> mediana di `r` (che non poteva averne, C12), ne' sulla sua dispersione (che poteva, e non ne ha).
> **La cura C11 era giusta** — un flag dichiarato attivo e inerte al 95.33 % e' un difetto comunque —
> **ma il suo effetto fisico resta non dimostrato**, esattamente come per C7 (voce **P**).

---

## 4. IL CONTO **FDT**, rifatto sul sistema non castrato — **resta INAPPLICABILE, e NON SI CABLA**

Derivazione invariata (`doc/ANALISI_gilbert_fdt.md`), ingredienti **misurati** ora con **FASE 5
attiva** e **`--cs-dinamico` acceso**: `lambda = amp^2 * |B| / (2*dt*kT)` con `kT = Lam`;
controllo di consistenza `kT_equipartizione = I*<omega^2>/3`.

| braccio | seme | `\|B\|` | `amp` | `Lam` | **`lambda`** | **`tau_smorz`** | **`tau_disordine`** | **`kT/Lam`** |
|---|---|---|---|---|---|---|---|---|
| OFF | 3 | 0.554 | 0.0954 | 0.00903 | 27.9 | 3.58 passi | 0.00117 passi | **1.26e6** |
| OFF | 4 | 0.508 | 0.1049 | 0.01092 | 25.6 | 3.91 | 0.00126 | **9.96e5** |
| ON | 3 | 0.558 | 0.0897 | 0.00799 | 28.1 | 3.56 | 0.00431 | **1.85e5** |
| ON | 4 | 0.481 | 0.1173 | 0.01364 | 24.3 | 4.12 | 0.00626 | **1.21e5** |

**Cosa e' MIGLIORATO — e non e' poco:**

| | prima (sistema castrato) | **ora** | fattore |
|---|---|---|---|
| `lambda` | 3.47 /tempo | **~26** | **×7.5** |
| `tau_smorzamento` | 28.8 passi | **3.7-3.8 passi** | **×7.7 piu' veloce** |
| `kT_equip / Lam` | ~2e7 | **1.1e6** (OFF) / **1.5e5** (ON) | **×18 / ×130** |
| `tau_smorz / tau_disordine` | ~1e4 | **3081** (OFF) / **726** (ON) | **×3 / ×13** |

> ### **E non basta lo stesso, di tre ordini di grandezza.**
> La lettura era fissata PRIMA: *`kT/Lam` ~1e7 o piu' -> inapplicabile per ragione strutturale;
> ordine 1-100 -> applicabile*. **Il valore migliore misurato e' `1.2e5`: e' sceso di due ordini,
> e resta MILLECINQUECENTO VOLTE sopra il tetto della banda in cui il FDT si applica.**
> Lo smorzamento derivato allinea in **3.7 passi**; il rimescolamento avviene in **0.0012-0.0063
> passi**. **Il sistema si disordina fra 726 e 3081 volte piu' in fretta di quanto il FDT sappia
> frenarlo.**
>
> **NON SI CABLA.** Un `lambda` grande abbastanza sarebbe **SCELTO** (§3, manopola), e metterebbe
> dissipazione senza la fluttuazione che la accompagna: **lo stesso errore, ribaltato.**

**NB onesto sulla riga «intermedio» dello script:** la mia soglia binava `>= 1e6` come strutturale e
`<= 100` come applicabile, quindi il braccio ON (`1.5e5`) e' finito nella casella *«intermedio, si
riporta senza forzare»*. **E' un artefatto della mia binatura, non una lettura fisica:** `1.5e5` non
e' «a meta' strada», e' **tre ordini dalla parte dell'inapplicabile**. Lo scrivo perche' chi legge
solo l'output dello script non prenda quell'etichetta per un giudizio.

**E il perche' STRUTTURALE resta quello di oggi** (`doc/MAPPA_accoppiamenti_spin.md`): non e' che il
FDT sia *quasi* applicabile. **Non c'e' un bilancio da cui `lambda` possa uscire**, perche' il torque
non e' azione-reazione e nel file non esiste un'energia totale. **Il FDT e' la terza porta chiusa,
non la piu' stretta.**

**⚠ Un caveat sul `kT` di equipartizione, dichiarato:** usa `I = inerzia mediana`, che vale
**3.47e-6** nel run ON s4 — cioe' **sopra** il pavimento `1e-6`, quindi per una volta e' una massa e
non una regolarizzazione (**2458-3019 nodi liberi su ~2500-3800**, il pavimento si e' rilasciato).
**A 500 passi il numero e' onesto**; a 300 non lo sarebbe stato.

---

## 5. COSA QUESTO REFERTO **NON** DICE

1. **Non dice che la FASE 2 centri il bersaglio.** Vedi §0: `theta` e' misurato in **due
   convenzioni diverse** e il confronto col `-0.69` non e' valido finche' non si rifa' a parita' di
   definizione.
2. **Non dice che `--tau-luce` produca una firma fisica su `chi`.** Il contrasto `+0.177` esclude lo
   zero **ma** i due bracci differiscono di **~7x in risoluzione**, e nessuno dei due e' risolto.
3. **Non dice nulla sul braccio OFF della voce R con forza:** quel divario ha **2 semi**, quindi
   `t(1) = 12.706` e un IC95 largo **1.55**. **Le colonne `t3_*` esistono solo nei run di oggi**, e
   i quattro run del 15 sono precedenti al cablaggio di MISURA F. **Per una barra vera sulla voce R
   servono 4 semi per braccio, cioe' due run in piu' per braccio.**
4. **Non dice che lo spin non si organizzi.** `theta` resta a **11.9-16.5 giri/passo** nel braccio
   migliore, con **l'84 %** dei nodi oltre il giro intero: **ogni esito negativo qui e' quello che
   l'aliasing produrrebbe da solo** (C14).

## 6. COSA SI PUO' PORTARE VIA, in quattro righe

> 1. **`S` e' chiusa: rumore.** Ma resta aperta una domanda **diversa**, il contrasto ON−OFF, con un
>    confondente di risoluzione che va tolto prima di interpretarlo.
> 2. **`R` e' refutata**, e dal dato piu' pulito del lotto: `sigma` cambia di **0.0013** mentre `tau`
>    cambia di **due ordini di grandezza**.
> 3. **`ESITO (I)` e' confermato quattro volte**: l'esponente `−1.056` non si muove di 0.01 fra semi,
>    bracci e leggi di `tau`.
> 4. **Il FDT resta chiuso**, ora con numeri **cento volte migliori** e **millecinquecento volte
>    insufficienti**.
