# A COSA SI ACCOPPIA LO SPIN? — mappa **letta dal codice**, nessuna misura

> **2026-09-16.** Blob `08784685`. Branch `fork-su2`. **Sola lettura del sorgente.**
> Mandato: §5 del TODO del 2026-09-16.
>
> **LA DOMANDA, e perche' non e' oziosa.** Una dissipazione manda energia **da qualche parte**.
> In un materiale magnetico la manda nel reticolo: c'e' un bagno esterno, e il coefficiente di
> Gilbert **si deriva** dall'accoppiamento a quel bagno. Questo sistema e' **relazionale e chiuso**:
> non c'e' un «fuori». Quindi o lo spin **cede a un altro settore** — e allora `lambda` **non si
> sceglie, lo da' il bilancio** — oppure non cede a nessuno, e **qualunque termine dissipativo
> violerebbe una conservazione**.
>
> **Ogni riga di questo documento porta la riga di codice.** Dove dico «non misurato», non e'
> misurato: le ampiezze di violazione **non sono state quantificate in questo giro**.

---

## 0. IL VERDETTO IN QUATTRO RIGHE

> 1. **Lo spin NON e' isolato: e' uno dei settori piu' accoppiati del file.** Decide **dove la
>    materia si divide** (mitosi), **quanto pesa** (sorgente di gravita') e **con che verso tira**
>    (`grav *= <nb_i . nb_j>`).
> 2. **Ma non esiste NESSUNA grandezza conservata che venga scambiata.** Gli accoppiamenti sono
>    **modulazioni**, non **trasferimenti**: nessun settore perde cio' che lo spin guadagna.
> 3. **Il termine `-omega/tau` e' un POZZO PURO.** Il momento angolare che toglie **non compare
>    da nessun'altra parte**: `omega_s` e' scritto in **un solo punto** del passo (`:2154`) e letto
>    in **due** (`:1984` e `:2136`), piu' un diagnostico.
> 4. **Nel file non esiste nessuna funzione di energia totale.** `grep -i energ` da' solo commenti
>    e l'energia **del vuoto** `Lam` (una densita' locale d'interferenza), mai un bilancio.
>    **Il test di sanita' «il sistema conserva l'energia?» non e' mai stato fatto perche' non c'e'
>    nulla da chiamare.**

**Conseguenza diretta sul mandato di Gilbert:** `lambda` **non e' derivabile da un bilancio**,
perche' **non c'e' un bilancio**. Ne' dal FDT (gia' escluso, `doc/ANALISI_gilbert_fdt.md`), ne'
dall'accoppiamento a un bagno (non c'e' bagno). **Resterebbe una scelta ⇒ §3, manopola.**

---

## 1. COSA ESCE DALLO SPIN (e dove va)

| # | da | a | riga | forma | sempre attivo? |
|---|---|---|---|---|---|
| **U1** | `omega_s` | `_psi_spinor` (e quindi `_nb`) | **2050-2058**, **2136-2146** | `U = exp(-i/2 omega.sigma dt)`, rotazione **unitaria** | **si'** |
| **U2** | `_nb` (via `psi_spin`) | `rho_spin` = **la densita' SORGENTE** | **2255-2259** | `psi_spin = M(w) @ (amp * _psi_spinor)`; `rho_spin = psi_spin^dag psi_spin` | si', con `--campo-spinoriale` |
| **U3** | `rho_spin` | **gravita'** (sorgente) | **1787** via `_rho_sorgente()` | `rho` del pozzo | si' |
| **U4** | `rho_spin` | **inerzia dello spin stesso** | **1952** | `inerzia = max(_rho_sorgente(), 1e-6)` | si' — **anello su se stesso** |
| **U5** | `rho_spin` | **soglia di MITOSI** | **3173** | `I = _rho_sorgente()` | si' |
| **U6** | `rho_spin` | **coppie di Schwinger** | **3316** | `I = _rho_sorgente()` | si' |
| **U7** | `_nb` | **la SPINTA gravitazionale**, moltiplicata | **3583-3586** | `grav = grav * (<nbg_i . nbg_j> * sign(dpozzo))` | **si', e non e' dietro nessun flag di esperimento** (solo `SPINORE`, che e' `True`) |

> **U7 e' l'accoppiamento piu' forte e il meno citato.** In `memoria_hebbiana_moto` — che gira a
> **ogni passo** — la spinta gravitazionale di ogni arco viene **moltiplicata per il prodotto
> scalare dei Bloch dei due estremi**. Due nodi con spin **antipodali** si respingono invece di
> attrarsi; due ortogonali **non si vedono**. Con `chi = 90.0 +- 39.2` (il valore misurato, che e'
> il **nullo** di direzioni casuali, `CLAUDE.md` §9) questo fattore e' **una variabile casuale di
> media ~0**: la gravita' del fork e' modulata da un numero che oggi e' **rumore**.
> *(Che `chi` sia al nullo e' misurato; che questo sia un **difetto** non e' stabilito, ed e' fuori
> dal mandato di oggi. Vedi anche il caveat di §7.2: `nbg` non e' `nb`.)*

---

## 2. COSA ENTRA NELLO SPIN (e da dove)

| # | da | a | riga | forma |
|---|---|---|---|---|
| **D1** | Bloch dei **vicini** (`_nb_prec`) | `B` | **1917-1932** | `B_i = (1/deg_i) * SOMMA_j w_ij * refl_ij * nb_j` |
| **D2** | `B` | `omega_s` | **1956** | `correzione = cross(B, nb)` |
| **D3** | Bloch del **campo emesso** | `omega_s` | **1962** | `correzione += cross(_nb_grav(), nb)` |
| **D4** | **rumore del vuoto** | `_nb` | **1908** | `_nb += N(0,1) * amp`, `amp = sqrt(Lam)/(1+I2/Lam)` |
| **D5** | — | `omega_s` | **1984** | **`- omega_src/_tau`** — **il pozzo** |
| **D6** | nascita | `omega_s` | **1654** | `calcio_omega` in `semina()`: punto zero **alla nascita**, non per passo |

---

## 3. IL PUNTO CHE DECIDE — **il torque NON e' azione-reazione**

`d(omega_i)/dt = cross(B_i, nb_i)/inerzia_i`, e poiche' il momento angolare e'
`L_i = inerzia_i * omega_i`, **l'inerzia si cancella**: il bilancio va fatto sul torque nudo,
`T_i = cross(B_i, nb_i)`. Dal codice (`:1928-1932`):

```
B_i = (1/deg_i) * SOMMA_j w_ij * refl_ij * nb_j       deg_i = SOMMA_j w_ij
refl_ij = diag(1,1,-1) se chi_i*chi_j > 0,  I altrimenti
```

**Due rotture, entrambe leggibili dalla formula, nessuna delle due misurata come ampiezza:**

1. **La normalizzazione.** Il contributo della coppia `(i,j)` al torque su `i` e'
   `(w_ij/deg_i) * cross(nb_j, nb_i)`; quello su `j` e' `(w_ij/deg_j) * cross(nb_i, nb_j)`.
   Sono opposti **solo se `deg_i == deg_j`**. Su un grafo di grado disomogeneo — cioe' **questo** —
   **non lo sono.** Il torque e' una **media** sui vicini, e una media non e' una somma di
   interazioni a due corpi.
2. **La riflessione.** Sui legami fra chiralita' **uguali** il vicino entra **riflesso**
   (`z -> -z`). `cross(R nb_j, nb_i)` e `cross(R nb_i, nb_j)` **non sono opposti in nessun caso
   non banale**: qui l'antisimmetria non e' rotta da una normalizzazione, e' **rotta nella
   struttura**.

> **Quindi `SOMMA_i L_i` non e' conservata**, e non per errore numerico: **per costruzione**.
> Non c'e' quantita' da bilanciare, e quindi non c'e' bilancio da cui far uscire `lambda`.
> **NB ONESTO:** che non sia conservata si **dimostra** dalla formula; **quanto** non lo sia
> **non e' misurato**. La misura sarebbe `|SOMMA_i cross(B_i, nb_i)|` contro
> `SOMMA_i |cross(B_i, nb_i)|` — un numero, un campione, e chiude la domanda. **Non fatta oggi.**

---

## 4. `TW_SPINORE` — **e' a UN VERSO SOLO, ed e' SPENTO**

**Domanda del mandato:** la torsione a 4pi che pilota il Bloch e' **bidirezionale**?
**Risposta, dal codice: NO, ed e' anche spenta.**

- **`tw -> nb`**: esiste, riga **1990-1996**, ma **solo se `TW_SPINORE`**, che vale `False`
  (riga **705**) e **non e' acceso da nessun flag dei run di questo programma**.
  Stessa cosa per `SPIN_LARMOR` (riga **701**, `False`), che userebbe `tw` per costruire `Bg`.
- **`nb -> tw`**: **non esiste.** La dinamica di `tw` e' alle righe **2878-2883**:
  `self.tw += _w4(dph - self.twp) - dt_e * self.tw/_ttw` — e' guidata da **`dph`**, la differenza
  di **fase**, e non contiene `nb` ne' `omega_s`. Le altre occorrenze di `self.tw` sono
  estensione (1777), mitosi (3289, 3367) e **letture**.

> **Quindi non e' «un canale aperto in un verso solo»: e' un canale CHIUSO in entrambi.**
> Il reperto c'e' lo stesso, ed e' diverso da quello ipotizzato: **la doppia copertura non e'
> agganciata al Bloch in nessuno dei run di questo programma.** *(Distinto da **C11**: li' era la
> FASE 5, l'**orologio** a 4pi in `ritmo()`, cablata ma inerte per un difetto e poi curata. Qui e'
> `TW_SPINORE`, il **torque** a 4pi, che e' **spento di proposito**. Due cose diverse con lo stesso
> «4pi» nel nome: **non confonderle.**)*
> **Conseguenza operativa, e vale per la MISURA F appena cablata:** poiche' entrambi sono spenti,
> la ricostruzione della catena di `omega` **non deve** contenere `Bg` ne' `_otw` — ed e' la
> ragione per cui `SPIN_LARMOR` e `TW_SPINORE` sono ora **colonne del CSV** (P6): chi legge quei
> dati deve poter verificare che erano spenti, non crederci.

---

## 5. L'ENERGIA — **non c'e' nulla da chiamare**

`grep -i "energ"` su tutto il file: **nessuna funzione**. Ci sono solo commenti e due cose che
**non** sono un bilancio:

- **`lambda_vuoto(net)`** (riga **487**): `Lam = <|Psi|^2>`, la **densita' d'energia
  d'interferenza del vuoto**. E' una **scala di stato**, usata per costruire l'ampiezza del rumore.
  Non e' un integrale primo, e non c'e' nessun posto in cui venga confrontata fra due istanti.
- **Il termostato Nose-Hoover** (righe **2767-2806**), che sarebbe l'unico **bagno** del file:
  `xi > 0` frena, `xi < 0` **RIFORNISCE** — il commento lo dice esplicitamente. **Ma:**
  * e' gated su **`REGIME == "deterministico"`**, e **tutti i run di questo programma girano in
    stocastico** (`--calore-scal`, `SCUOTIMENTO=True`): **e' SPENTO**;
  * agisce su **`phivel`** (energia cinetica di **fase**), **non** su `omega_s`. Anche acceso,
    **non sarebbe il bagno dello spin.**
- E lo spinore e' **normalizzato a `|psi| = 1` in modo atomico a ogni passo** (righe
  **2128-2129**): **non ha ampiezza**, quindi **non ha energia** da scambiare. Tutto il contenuto
  dinamico dello spin sta in `omega_s`, e `omega_s` non e' conservato (§3).

> **Il test di sanita' «il sistema conserva l'energia?» non e' stato «mai fatto»: e' oggi
> IMPOSSIBILE da porre**, perche' non esiste una funzione di energia da valutare. Costruirne una
> sarebbe **esattamente** la voce **L** del registro (l'azione unica / la lagrangiana), e per la
> regola 3 quella non e' un fronte: e' la direzione.

---

## 6. COSA NE SEGUE, in termini operativi

| esito previsto dal mandato | quale si e' verificato |
|---|---|
| «trovi un accoppiamento ⇒ la dissipazione e' derivabile **da li'**» | **NO.** Gli accoppiamenti ci sono e sono molti (§1), ma sono **modulazioni**: nessuno trasferisce una grandezza conservata. Da una modulazione non esce un coefficiente. |
| «non ne trovi ⇒ lo spin e' **isolato**» | **NO, ed e' il contrario:** lo spin e' uno dei settori piu' connessi. |
| — | **IL TERZO ESITO, che il mandato non prevedeva: ACCOPPIATO MA SENZA BILANCIO.** Lo spin **parla con tutti e non deve niente a nessuno.** |

**Quindi la risposta alla domanda di partenza e': `lambda` non si deriva.** Non perche' manchi un
canale, ma perche' **manca la grammatica** — nessuna quantita' conservata attraversa i canali che
ci sono. **Cablare Gilbert resterebbe una manopola (§3), e questo documento e' la terza ragione
indipendente** dopo il FDT troppo debole (`doc/ANALISI_gilbert_fdt.md`) e la FASE 1 gia' chiusa
(`doc/FASE1_gilbert_llg.md`).

**E il presidio, per non rifare il giro:** *«manca un freno»* era gia' falso (il freno e'
`-omega/tau`, misurato, col ginocchio previsto `7.059e4` contro osservato `7.271e4`). Ora e' anche
chiaro **perche' non se ne possa aggiungere un altro per derivazione**. La domanda vera resta
quella di `CLAUDE.md` §9: **non l'uscita, l'INGRESSO — `sigma` e' grande.**

---

## 7. LE DUE MISURE CHE CHIUDEREBBERO DAVVERO QUESTA VOCE (non fatte oggi, dichiarate)

1. **L'ampiezza della violazione del torque:** `|SOMMA_i cross(B_i, nb_i)| / SOMMA_i |cross(B_i, nb_i)|`.
   Se fosse ~`1/sqrt(n)` sarebbe **rumore di somma**; se fosse O(1) la violazione e' **strutturale
   e grande**. **Gli ingredienti ci sono gia'** in `_tracing_omega.ingredienti` (`B` e `nb`):
   costa una decina di righe, **zero run nuovi**.
2. **Il peso reale di U7:** la distribuzione di `<nbg_i . nbg_j>` sugli archi. Se e' centrata su
   zero, la gravita' del fork e' modulata **da rumore**; la misura di `chi` lo suggerisce
   (`90.0 +- 39.2` = il nullo esatto) ma **`nbg` non e' `nb`** quando `--campo-spinoriale` e'
   acceso — e' il Bloch del **campo emesso** — quindi **non e' la stessa misura** e non va
   spacciata per tale.

---

*Scritto per Claude web e per chi riprende il repo. Nessun codice toccato da questo documento.*
