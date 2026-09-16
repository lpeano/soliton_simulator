# PREDIZIONE — il TAGLIO SPETTRALE del rumore (voce `D`)

> **Scritta PRIMA di cablare qualsiasi cosa.** 2026-09-16, blob **`08784685`** (verificato dal
> disco: byte LF, sha1 grezzo = `git hash-object` = HEAD). Branch `fork-su2`.
> **Nessuna riga di `soliton_simulator.py` toccata.**
>
> ## ⚠ E NON E' LA PREDIZIONE CHE IL MANDATO CHIEDEVA.
> Il mandato mette **P1 in vigore** — *«ogni affermazione di questo mandato che contraddica un
> fatto gia' misurato va segnalata, non eseguita… FERMATI e dillo»*. **Tre affermazioni la
> contraddicono**, e due sono **decisive**: la stima `theta 15.08 -> ~3.4` e l'ipotesi qualitativa
> **non possono verificarsi**, per ragioni misurate, non congetturate.
> **Percio': la predizione qui sotto e' CORRETTA, non trascritta, e il cablaggio NON e' stato
> fatto.** La ragione per cui il cablaggio potrebbe comunque avere senso e' **un'altra** da quella
> data, e la decisione e' di Luca (§5).

---

# 1. LE TRE CONTRADDIZIONI, in ordine di gravita'

## 1.1 — ⚠⚠ **LA RICORSIONE DATA NON RIDUCE L'AMPIEZZA. PRESERVA LA VARIANZA, esattamente.**

Il mandato da' la legge e, separatamente, la stima:

```
xi(t) = xi(t-dt)*exp(-dt/tau_c) + sqrt(1 - exp(-2 dt/tau_c)) * g(t)      <- la LEGGE
frazione superstite = 0.050 -> varianza /20 -> AMPIEZZA / 4.47           <- la STIMA
```

**Le due cose non descrivono lo stesso oggetto.** Per `x' = a x + b g` la varianza stazionaria e'
`b^2/(1-a^2)`; con `b^2 = 1 - a^2` essa vale **1 esattamente**, cioe' **quella del rumore bianco**.

**Verificato numericamente** (`tau_c = LAM/CS_M = 0.400` = 40 passi, `DT = 0.01`):

```
a = 0.975310   b = 0.220841
b^2/(1-a^2)                        = 1.000000       <- ANALITICO
varianza stazionaria simulata      = 0.997330       <- 400 000 passi
tempo di autocorrelazione          = 40.0 passi
```

> **La ricorsione OU cambia SOLO la struttura temporale del rumore, non la sua ampiezza.**
> Il calcio per passo resta **della stessa taglia**; cambia che i calci successivi sono
> **correlati** su 40 passi.
>
> La stima `varianza/20` descrive un oggetto **diverso**: un rumore **limitato in banda a densita'
> spettrale COSTANTE**, che ha meno varianza totale perche' gli si e' tolta banda. Per ottenerlo
> con questa ricorsione bisognerebbe **moltiplicare per `sqrt(2*dt/tau_c)`** — cioe' **toccare
> `amp`**, che il mandato vieta esplicitamente («`amp` non si tocca»), e che sarebbe **un
> coefficiente scelto** (§3, manopola).
>
> **Le due prescrizioni del mandato sono incompatibili fra loro.** Non e' un dettaglio di
> normalizzazione: e' la differenza fra «meno rumore» e «rumore diverso».

## 1.2 — ⚠⚠ **IL RUMORE NON MUOVE IL BLOCH. Lo muove `omega`, di TRE ORDINI DI GRANDEZZA piu'.**

Il mandato: *«il Bloch oggi decorrela da se' stesso in UN tick (spostamento medio 85.6
gradi/passo). Se il taglio riduce il kick da ~90 a ~20 gradi…»* — cioe' **attribuisce al rumore**
lo spostamento del Bloch.

**Misurato sui quattro run di oggi** (500 passi, `fdt_amp_mediana` e `theta` dallo stesso campione;
il calcio del rumore e' `atan(amp*sqrt(2))`, perche' la componente perpendicolare a `nb` di un
`N(0,I3)` ha modulo `amp*sqrt(2)`):

| run | `amp` | **calcio del rumore** | **moto del Bloch (`theta`)** | rapporto |
|---|---|---|---|---|
| OFF s3 | 0.0954 | **7.68 gradi/passo** | 37 874 gradi/passo | **0.020 %** |
| OFF s4 | 0.1049 | **8.44** | 37 866 | **0.022 %** |
| ON s3 | 0.0897 | **7.23** | 5 705 | **0.127 %** |
| ON s4 | 0.1173 | **9.42** | 4 274 | **0.220 %** |

> **Il rumore contribuisce fra lo 0.02 % e lo 0.22 % del moto del Bloch. Il resto e' `omega`.**
> Il «kick da ~90 gradi» non esiste: il calcio vale **7-9 gradi**, ed e' la sola cosa che il taglio
> spettrale puo' toccare.

**E il `85.6` e' reale ma dice un'altra cosa.** Sta in `doc/BILANCIO_ordine_spin.md:97`, e' lo
spostamento del **padre nel passo della nascita**, su **n = 7**, e il documento stesso scrive *«se
regge sulla statistica»*. Non e' una misura del rumore, e non e' una misura a regime.

**In piu', dal codice** (`CLAUDE.md` §9, gia' verificato): sotto `--spinore-corretto` il `_nb`
committato e' **DERIVATO da `_psi_spinor`** (`:2155`), e il calcio del rumore su `_nb` (`:1908`)
viene **sovrascritto** alla fine del passo. **Il rumore non entra nella traiettoria del Bloch:
entra solo nella COPPIA, via `cross(B, nb)` con l'`nb` rumoroso.**

## 1.3 — ⚠ **E quella coppia e' gia' stata misurata MARGINALE: `R_stoc = 0.041` (C6).**

Il tracing del 2026-09-15 ha misurato la frazione **stocastica** dell'incremento di `omega`:
**`R_stoc = 0.041`, sotto l'errore atteso della ricostruzione (`0.097`)** — cioe' **il rumore non
guida `omega`**, ed e' l'esito **(IV) escluso** di `doc/TRACING_omega.md`.

> **Quindi il taglio spettrale agisce su un canale che vale il 4 % dell'ingresso di `omega`, e
> lo fa senza cambiarne l'ampiezza.** Non c'e' nessuna via per cui `theta` scenda di 4.5x.

---

# 2. LA PREDIZIONE CORRETTA — e va nella direzione OPPOSTA

**`theta` non scendera'. Se si muove, sale.**

**Perche':** con il rumore bianco la parte stocastica della coppia e' **indipendente a ogni passo**
-> `omega` stocastico cresce come `sqrt(n)`. Con il rumore **correlato su `tau_c = 40 passi`**, per
`n < 40` la stessa forza e' **coerente**, quindi cresce come **`n`**: un fattore fino a
**`sqrt(40) ~ 6.3`** *sulla sola componente stocastica*. Poiche' quella componente vale `R_stoc =
0.041` dell'incremento, l'effetto sul totale e' **al piu' qualche punto percentuale, in SALITA**.

| grandezza | previsione |
|---|---|
| `theta` (entrambe le convenzioni) | **variazione ≲ 5 %**, e il **segno atteso e' +** |
| `omega/sqrt(n)` | **potrebbe smettere di essere costante** — ma **al rialzo**, non al ribasso: e' la firma del passaggio a forzante **coerente**, non dell'uscita dal regime diffusivo verso l'ordine |
| `chi` | **nessun effetto atteso** oltre la barra fra semi (0.03) |
| aliasing | **invariato.** Servono **30.2x**; l'effetto atteso e' **~1x** |

**La possibilita' qualitativa del mandato — `B` che si stabilizza e `cross(B,nb)` che acquista una
direzione persistente — richiede che il rumore domini la decorrelazione del Bloch.
MISURATO: la domina allo 0.02-0.22 %.** `B` e' costruito da `_nb_prec`, il Bloch **committato**, il
cui moto e' `omega`. **Colorare il rumore non puo' stabilizzare `B`.**

**LE TRE LETTURE, fissate ora:**
- **`|theta_ON - theta_OFF| < 5 %` e `omega/sqrt(n)` invariato** -> **predizione confermata**: il
  rumore e' piu' fisico e **non cambia nulla di misurabile**. E' l'esito atteso.
- **`theta` SALE oltre il 5 %** -> il meccanismo della forzante coerente morde piu' del previsto:
  **interessante, e nella direzione sbagliata** per l'aliasing. Riportare, non festeggiare.
- **`theta` SCENDE in modo significativo** -> **la mia analisi qui sopra e' sbagliata**, e il
  reperto e' che uno dei tre fatti misurati (C6, il rapporto 0.02-0.22 %, o la conservazione della
  varianza) non regge. **Reperto grosso, e sarebbe a mio carico.**

---

# 3. QUELLO CHE RESTA IN PIEDI DEL MANDATO — ed e' la parte che conta

> **«Si fa perche' il rumore bianco e' fisicamente SBAGLIATO, non perche' ci si aspetta che
> risolva l'aliasing.»**

**Questa giustificazione REGGE, intatta, e non dipende da nessuna delle tre correzioni.** Un rumore
bianco discreto inietta a **tutte** le frequenze fino a Nyquist, comprese quelle che il passo non
risolve; nessun rumore fisico lo fa. **`tau_c = LAM/CS_M` e' derivato, non scelto** — e' il
tempo-luce del solitone — e la ricorsione **non introduce coefficienti**.

**Il cablaggio ha quindi ancora senso, ma per UNA ragione sola e con UN'attesa sola:**
**correggere una legge sbagliata, aspettandosi che NON cambi i numeri.** *(E' la forma migliore di
un test: se una correzione di principio non muove nulla, lo si e' imparato; se muove, si e'
imparato di piu'.)*

**PERCHE' MI FERMO QUI E NON CABLO:**
1. **Le due prescrizioni del mandato sono incompatibili** (§1.1): «`amp` non si tocca» **e**
   «ampiezza /4.47» non possono valere insieme. **Quale delle due intendi e' una tua decisione**,
   e la seconda richiede un coefficiente, cioe' §3.
2. **L'attesa dichiarata (`theta 15.08 -> 3.4`) non e' raggiungibile** con la legge data. Cablare
   ora significherebbe misurare contro un bersaglio che so gia' sbagliato — che e' esattamente il
   difetto della voce **R**, appena refutata.
3. Il mandato stesso lo prescrive: *«Se rileggendo il registro qualcosa non torna, FERMATI e
   dillo.»*

**Se il via e' «cabla la legge cosi' com'e', con l'attesa corretta di §2», il lavoro e' pronto e
i sigilli N1-N6 restano validi cosi' come sono scritti** — con **una correzione da fare comunque**:

> **⚠ IL `dt` DELLA RICORSIONE DEV'ESSERE `dt_n = DT*r`, NON `DT`.**
> Il mandato scrive `dt` senza dirlo. Il rumore e' un **processo locale del nodo**, e `CLAUDE.md`
> §9 e' esplicito: *«il tic dei processi locali e' `dt_n = DT*r`; `DT` nudo e' il tempo di
> COORDINATA, e usarlo dentro un rilassamento locale impone la foliazione sincrona globale = un
> frame preferito, un etere»*. **E' esattamente l'errore gia' preso una volta nello Strato 1**, che
> S1..S6 passavano identici e solo **S7** ha stanato. `dt_n` e' disponibile: e' un **parametro** di
> `_passo_spinoriale`. **Un sigillo tipo S7 — due nodi con `r` diverso devono decorrelare in tempi
> diversi — va aggiunto a N1-N6**, o l'errore passerebbe invisibile come allora.
