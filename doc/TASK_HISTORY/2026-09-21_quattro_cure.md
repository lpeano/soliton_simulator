# 2026-09-21 — **LE QUATTRO CURE: derivazioni PRIMA del codice**

> **MANDATO GLOBALE del 2026-09-21.** **Questo file si committa PRIMA del codice** (par.5-septies):
> l'ordine dev'essere **verificabile da git**, non asserito da me.
> **Regola ④ del mandato: zero coefficienti e zero pavimenti SCELTI. Ogni forma si DERIVA, e la
> derivazione sta qui.**

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di scrivere una riga*

### Cosa e' gia' MISURATO (non lo ri-derivo)
- picco al passo **1126**, arco **`3352-506`**, **`peq = -4.85e-04`**, `anom = 1.807e+06`,
  `n1 = nsub = 22591`, costo del solo passo **2032 s** *(`Z93`, `Z94`)*;
- **senza** il pavimento `max(peq,1e-9)` quello stesso arco darebbe `anom = -3.72`, `n1 = 1`:
  **il pavimento ribalta il segno e moltiplica per `3.7e5`**;
- `min(peq)` decade **geometricamente** `×0.825`/passo *(⇒ `dt_e/tau_bg_loc ≈ 0.175` su QUELL'arco:
  **li' il rilassamento e' stabile**)* mentre `median(peq)` **sale**;
- `SCALA_MIN`: **sei** scritture di `d0` per passo *(misurate: `_g_sm_d0` = `6.000`/passo)*, e su `d`
  **`nsub`** scritture *(`_g_sm_d` = `4.00`/passo fino al 1080, `196.8` fra 1080 e 1200)*;
- `_g_coes_max = 0.00269725` **costante** su tutti gli snapshot, `_g_coes_satura = 0`.

### Cosa NON so, e lo dichiaro
- **quanti** archi abbiano `peq < 0` — **uno o mille cambia la diagnosi**;
- **quale** dei due termini di `:4206` scavalchi: il rilassamento o `flusso/TAU_DIFF`;
- **il valore di `dt_e/tau_bg_loc`** sull'arco colpevole. *(Il `0.175` dedotto sopra vale su
  `2773-4158`, **non** su `3352-506`: trasportarlo sarebbe P1.)*
- **se `dt_e` sia scalare o per-arco** nel ramo `TAU_LOCALI`. **Va letto dal codice, non ricordato.**

### L'aspettativa, scritta per poterla smentire
Mi aspetto che sia il **rilassamento** a scavalcare, perche' e' quello con `tau_bg_loc` **al
pavimento `1e-3`** *(`:4204`)*: con `dt_e ~ 1e-2`, `dt_e/tau_bg_loc ~ 10`, **dieci volte oltre la
soglia di stabilita' `1`**. **Se invece fosse la diffusione, la cura ① come e' disegnata NON
basterebbe**, e va detto.

---

## 2. PROGETTAZIONE — *le derivazioni, e cosa decide ciascuna*

### ① `PEQ_ESATTO`

**IL DIFETTO, in una riga:** `peq += dt_e*(rho - peq)/tau_bg_loc` e' un **Eulero esplicito**; per
`dt_e/tau_bg_loc > 1` **scavalca**, per `> 2` **oscilla divergendo**.

**LA FORMA, DERIVATA e non scelta.** L'equazione e' `dpeq/dt = (rho - peq)/tau`. Con `rho` e `tau`
costanti **sul passo** — che e' esattamente l'ipotesi gia' fatta dall'Eulero — la soluzione e'
**esatta**:
```
peq(t+dt) = rho + (peq(t) - rho) * exp(-dt/tau)
```
**Zero coefficienti nuovi.** `exp(-dt/tau)` e' la **stessa forma** gia' cablata nello Strato 1
(`alpha = 1 - exp(-dt_n/tau)`, par.4: *«per il RILASSAMENTO di primo ordine usa il passo ESATTO,
NON Verlet»*). **La regola c'era gia' e non era applicata a `peq`.**

**PERCHE' NON PUO' USCIRE DAL DOMINIO, ed e' una dimostrazione, non una speranza:**
posto `a = exp(-dt/tau) ∈ (0, 1]` per `dt >= 0, tau > 0`, si ha `peq_new = a*peq + (1-a)*rho`:
**una COMBINAZIONE CONVESSA** di `peq` e `rho`. Quindi
```
min(peq, rho) <= peq_new <= max(peq, rho)
```
**per QUALUNQUE `dt`**. Con `peq >= 0` e `rho >= 0` *(e `rho = 0.5(I_i+I_j)` con `I = |psi|^2` lo e'
sempre)*, **`peq_new >= 0`. Sempre. Senza pavimenti.**
**E si riduce all'Eulero nel limite:** `exp(-x) = 1 - x + O(x^2)`, quindi per `dt/tau -> 0` la
differenza e' `O((dt/tau)^2)`. **E' la riduzione al limite del sigillo.**

**LA DIFFUSIONE, e qui NON ho una forma esatta: ho un vincolo.** `flusso/TAU_DIFF` e' un laplaciano
sulla topologia, **non** un rilassamento a bersaglio fisso: non si integra in forma chiusa.
**Cosa DERIVO invece:** con `campo = peq` *(`DIFF_RES == 0`)* il termine e' `(c_arco - peq)/TAU_DIFF`
con `c_arco` **media pesata dei `peq` dei vicini**, quindi **anch'esso** ha forma di rilassamento
verso un bersaglio `>= 0`, e la **stessa** esponenziale lo rende convesso.
**⚠ MA I DUE TERMINI SOMMATI NON SONO UNA COMBINAZIONE CONVESSA**: due passi esatti applicati
insieme possono uscire. **Forma che propongo, e la dichiaro come SCELTA DI SPLITTING, non come
derivazione:** i due rilassamenti si applicano **in sequenza**, ciascuno in forma esatta — un
**Lie-Trotter splitting**, che preserva la convessita' di ciascun fattore e quindi la positivita'.
**COSTO: l'ordine di accuratezza resta 1**, come l'Eulero di oggi. **Non peggiora nulla, e non
introduce numeri.**
**⚠ E SE `DIFF_RES != 0`** il campo e' `(rho - peq)` e il bersaglio **non** e' `>= 0`: **li' la
dimostrazione NON vale, e va detto.** *(Verificare dal disco quanto vale `DIFF_RES` nei run del
fork.)*

**IL PAVIMENTO AL DENOMINATORE (`:4215`).** Con `peq >= 0` garantito resta **un solo** caso
patologico: **`peq = 0` esatto con `rho > 0`** → divisione per zero.
**Non propongo un pavimento**: propongo di **derivare il caso**. `peq = 0` significa *«questo arco
non ha ancora un vuoto di sfondo»*; `rho > 0` significa *«ma ha densita'»*. **L'anomalia relativa
non e' definita li'** — e la forma **simmetrica** (`cura` non richiesta in questo giro ma gia'
derivata, `csv/_deriva_anom_simm.py`) **la definisce a `+2`**, che e' il suo massimo.
**PROPOSTA MINIMA, senza numeri scelti:** con `peq >= 0` garantito, il pavimento `1e-9` **non e' piu'
una regolarizzazione del segno** ma solo dello zero. **Lo lascio dov'e' e lo DICHIARO**, perche'
toglierlo richiede la forma simmetrica, che e' **un'altra cura** e ha **il suo polo** (`Z95` da
aprire). **Dichiaro che questa cura NON toglie il pavimento, e perche'.**
**Il caso `0/0`** *(`rho = peq = 0`)* oggi da' `0/1e-9 = 0`, **che e' il valore giusto** — dove non
c'e' densita' non c'e' anomalia — **e la cura non lo cambia.**

**SIGILLI (bloccanti):**
- **P1** flag spento ⇒ **byte-identico** *(`max|A-B| = 0.000e+00` su tutti i campi)*;
- **P2** riduzione al limite: per `dt/tau -> 0`, `|esatto - eulero| = O((dt/tau)^2)` **misurato**;
- **P3** **`peq >= 0` su ogni arco a ogni passo** su un run di prova;
- **P4** **controllo positivo**: con `dt/tau > 1` costruito a mano, l'Eulero va **negativo** e
  l'esatto **no**. *(Senza questo, P3 passerebbe anche su codice morto.)*
- **P5** **il passo 1126 del ramo D, rigiocato con `PEQ_ESATTO` acceso, NON produce il picco.**

### ② `PEQ_NASCITA_LOCALE`
**IL DIFETTO:** `:4846` scrive `np.full(2*nc, median(self.peq))` — **una statistica GLOBALE**, che
viola `A2`. **`_allaccia`+`:4189` fanno gia' la cosa giusta**: `peq[nuovi] = rho[nuovi]`, che da'
`anom = 0` **esatto** alla nascita.
**LA CURA:** gli archi di Schwinger prendono **la `rho` del loro arco**, come gli altri.
**Zero parametri.** **Una sola legge di nascita, locale.**
**DA VERIFICARE E DIRE:** che la mitosi (`:4752`, eredita' dal genitore) sia **coerente** con questa
legge — eredita' ≠ nascita, e potrebbe essere giusta com'e'.
**SIGILLI:** byte-identita' a flag spento; **`anom = 0` esatto sugli archi di Schwinger appena nati**;
controllo positivo *(i due rami DEVONO differire quando Schwinger produce archi)*.

### ③ `SCALA_MIN_PASSO`
**LA FORMA, gia' dimostrata** *(referto §1.3)*: con `a > 0`, `b < 0`, `a+b = 0`, applicare il freno
**una volta sul totale** da' **bias ZERO esatto** e **non contiene l'ordine**.
**IL DISEGNO:** si memorizza `d0` e `d` a **inizio passo**; le sei scritture di `d0` e le `nsub`
scritture di `d` avvengono **senza freno**; a **fine passo** si applica `_smorza` **una volta**, sulla
differenza `fine - inizio`.
**⚠ UN PUNTO CHE NON HO ANCORA RISOLTO, e lo scrivo prima di scoprirlo col codice:** il freno a fine
passo **non impedisce a `d` di scendere sotto `LAM` DURANTE i sotto-passi**. **Se il valore
intermedio entra in un'altra legge** *(e `d` entra in `beta_new`, `:4298-4300, np.maximum(d_new,
1e-6)`)* **il vincolo non e' piu' garantito istante per istante.** **Va MISURATO quanto scende, non
assunto.**
**SIGILLO NUOVO, ed e' quello che manca oggi (`A9`):** **LA COMPOSIZIONE** — si iniettano spinte a
somma zero dentro un passo e **`d0` a fine passo dev'essere identico a quello di inizio**. Oggi
**ogni singola scrittura e' corretta e la somma no**, e nessun criterio lo guarda.

### ④ `COES_CAUSALE`
**DUE difetti, due correzioni:**
- **ingressi di INIZIO passo**: `richiamo_elastico` (`:5259`) legge `self.d0[mask]` **gia' spostato da
  sette scritture**. Si legge invece la copia di inizio passo *(la stessa che serve a `③`)*;
- **il tetto dal cono LOCALE**: `LAM*sqrt(K_C)*DT` (`:5292`) e' **globale** e vale `1.1314`, contro un
  cono locale misurato fino a `0.566`. **Si sostituisce con `cs` dell'arco** — il **piu' lento dei
  due nodi**, che e' la scelta conservativa e non e' un parametro.
  **⚠ E VA DICHIARATO: `cs_arco` esiste gia' nel codice** (ramo `CS_DINAMICO`), quindi **zero
  grandezze nuove**; ma **a `CS_DINAMICO` spento `cs = CS_M = 2.0`**, che e' **piu' grande** di
  `c_sistema = 1.1314`: **in quel caso la cura ALLENTEREBBE il tetto.** **Va gestito e detto.**
**SIGILLO:** nessuno spostamento di `d0` piu' veloce del cono locale — **e il controllo positivo**:
con un `cs` locale piccolo costruito a mano, il tetto **deve** stringere.

---

## 3. TODO DEL NEXT STEP
1. **§1** — contatori `TRACCIA_PEQ` byte-inerti + stop dopo `nsub`; rigiocata `1080 -> 1126`;
   **CHECKPOINT 1** *(informazione, non domanda: si prosegue)*;
2. **C1 `PEQ_ESATTO`** → sigilli `P1`-`P5`;
3. **C2 `PEQ_NASCITA_LOCALE`** → sigilli;
4. **C3 `SCALA_MIN_PASSO`** → sigillo della **COMPOSIZIONE**;
5. **C4 `COES_CAUSALE`** → sigillo del cono locale;
6. **§3 validazione 600 passi** → **CHECKPOINT 2: FERMARSI.**

**⚠ LE COSE CHE POTREBBERO FARMI FERMARE PRIMA, scritte adesso:**
- se **la diffusione** e non il rilassamento porta `peq` sotto zero → **la cura ① non basta**;
- se `DIFF_RES != 0` nei run del fork → **la dimostrazione di positivita' non vale**;
- se `d` scende sotto `LAM` dentro i sotto-passi con `③` acceso → **il vincolo non e' piu' garantito
  istante per istante**, e va deciso da Luca se conta;
- **qualunque sigillo di byte-identita' che fallisca.**
