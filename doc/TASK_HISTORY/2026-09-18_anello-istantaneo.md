# TASK HISTORY — **rompere l'anello istantaneo in `ritmo()`: lo snapshot di `med`**

**Data:** 2026-09-18 · **Branch** `fork-su2` · **HEAD alla scrittura** `3cdaa8e`
**Blob:** `f8f46683` · **Nessuna cura cablata finché il §1 non è riportato.**

---

## 1. RAGIONAMENTO PRELIMINARE

### 1.1 Il difetto è reale e l'ho verificato: `:2075-2076`

```python
med = max(float(np.median(np.abs(f))), 1e-9)     # calcolato DA f
x   = f / med                                     # e usato SU f
```

**A6** (uno specchio istantaneo) e **A3** (`median(x) = 1` per identità) nella stessa riga.
**E il terzo mestiere che ho misurato in `3cdaa8e` è esattamente questa circolarità.**
**La cura proposta — leggere `med` del passo PRIMA — scioglie entrambi senza toccare il gauge.**
**Sono d'accordo con la diagnosi. Tre cose del §2 però non tornano col disco.**

### 1.2 ⚠ PRIMO — **il blocco di snapshot non è a `:2944-2947`: è a `:3116-3121`**

`:2944-2947` cade dentro il **docstring di `_bloch_ritardato`**. Il blocco vero è in `step()`:

```python
:3116   # --- EVALUATE-THEN-COMMIT: Snapshot rigoroso di inizio passo (tempo t) ---
:3118   _phi_t = self.phi.copy() ; _tw_t = self.tw.copy()
:3120   _phivel_t = self.phivel.copy() ; _peq_t = self.peq.copy()
:3124   r = self.ritmo()
:3129   self._psi_prec = self.psi.copy()
:3131   self._psi_spin_prec = self.psi_spin.copy()
```

**Ed è un'informazione che cambia il progetto, non una pedanteria:** il blocco `_phi_t…` sta
**PRIMA** di `ritmo()`, mentre **gli snapshot che `ritmo()` CONSUMA** (`_psi_prec`,
`_psi_spin_prec`) sono promossi **DOPO**, a `:3129-3131`. **Sono due posti diversi, e il secondo è
quello giusto per noi.**

### 1.3 ⚠ SECONDO — **il mandato cita `Z33` col segno rovesciato, e l'ho misurato io**

Il §2 dice: *«`Z33` è nata esattamente così: `_psi_spin_prec` aggiornato DOPO il consumo»*.

**`680d069` ha misurato il contrario:** l'aggiornamento **dopo** il consumo è **ciò che fa valere
A6** — il consumo a `:3124` legge lo stato `t-1`. **Spostarlo prima confronterebbe `psi_spin` con sé
stesso: `f = 0` per costruzione, SEMPRE.** *(È il §1 del referto `Z33`: «se avessi eseguito il
mandato alla lettera avrei introdotto il difetto che dovevo curare».)*
**Il difetto di `Z33` erano 4 passi su 126 in cui i due snapshot erano LEGITTIMAMENTE identici, e la
cura è stata il CONTATORE.**

> **Conseguenza operativa, ed è il contrario di quel che il presidio ① suggerisce: il pattern di
> `:3129-3131` — promuovere DOPO il consumo — è quello da SEGUIRE, non da evitare.**

### 1.4 ⚠ TERZO, e nessuno l'ha nominato — **`ritmo()` ha TRE call-site, due dei quali DIAGNOSTICI**

```
:3124   r   = self.ritmo()     <- LA FISICA, dentro step()
:6263   tau = net.ritmo()      <- _diag_completa  (DIAGNOSTICO)
:6921   tau = net.ritmo()      <- DIAGNOSTICO
```

**Se lo snapshot venisse aggiornato DENTRO `ritmo()`, ogni chiamata diagnostica lo farebbe
avanzare** — un diagnostico che muta lo stato fisico. **Sarebbe il quinto difetto della famiglia, e
violerebbe par.2.3** *(purezza pure-read)*.

> **QUESTO decide il progetto, e la decisione non è di stile:**
> **`ritmo()` LEGGE `_med_f_prec` e NON lo scrive mai** *(sola lettura: i diagnostici vedono lo
> stesso gauge della fisica, ed è giusto così)*;
> **`ritmo()` REGISTRA ciò che ha calcolato in `_med_f_ultimo`** — un promemoria che nessuno
> consuma;
> **`step()` PROMUOVE `_med_f_prec = _med_f_ultimo`, a `:3129-3131`, accanto a `_psi_prec` e
> `_psi_spin_prec`.**

**E la contaminazione da diagnostico è chiusa PER COSTRUZIONE, non per attenzione:** un diagnostico
può sovrascrivere `_med_f_ultimo`, ma **il `step()` successivo chiama `ritmo()` PRIMA di promuovere**,
quindi **il valore promosso è sempre quello della chiamata fisica.**

### 1.5 I presidi ②, ④, ⑤ — dove sto col mandato

- **② lo SCALARE:** d'accordo, e senza riserve. **`med` è uno scalare: non ha lunghezza, quindi
  l'intera classe A8b (estensione alla mitosi) sparisce PER COSTRUZIONE.** Non salvo `f`.
- **④ il primo passo:** **la convenzione esiste già DENTRO `ritmo()`** — `:2021-2026`, quando
  `_psi_prec` manca si **restituisce `np.ones(n)`** *(«non esiste un prima»)* e **si conta**
  (`_ritmo_sicurezza`). **Riuso quella, non ne invento una.** ⚠ **E NON userò `median(|f|)` corrente
  come fallback: sarebbe il difetto stesso, al primo passo.**
- **⑤ la confrontabilità:** `med_prec` e `f` sono entrambi `Δangle/DT`, quindi `[1/T]`. **Da
  verificare nel codice, non da assumere.**

### 1.6 Cosa mi aspetto, e cosa NON so

**Mi aspetto che `median(x)` NON valga più 1** — numeratore e denominatore di istanti diversi.
**Ma NON so di quanto si sposta**, ed è il §1.

**⚠ E una cosa che mi preoccupa, scritta prima:** `median(|f|)` oscilla del **62 %** fra passi. Con
`med` sfasato di uno, **`x` eredita quell'oscillazione invece di dividerla via**. **La mediana di
`x` non sarà 1, ma potrebbe oscillare del 62 % lei stessa** — e allora **l'anello è rotto ma il
metro resta ballerino**. **Non è un'obiezione alla cura** *(l'anello va rotto comunque: A6 non è
negoziabile)* **ma il referto deve dirlo, e `P7` da solo non lo vedrebbe.**

**E NON so** se `Z33` sparirà (`P6`): se un passo ha `f` tutto nullo, ora `med_prec` è ancora buono,
quindi `x = 0` per tutti e **`r` cade sul pavimento lo stesso**. **La degenerazione potrebbe
cambiare forma invece di sparire.**

---

## 2. PROGETTAZIONE

**§1 — LA MISURA PRELIMINARE, senza cablare nulla.** Con la stessa sonda-spia già usata:
- **A** — `median(|f|)_t / median(|f|)_{t-1}`: mediana, p05, p95, **e la traiettoria**;
- **B** — **`median(x)` col `med` sfasato**: vale ancora 1? **E con quante cifre?**
- **C** — **quanti nodi cambiano regime** (da sopra a sotto `x = 1`), per passo;
- **D** *(mio)* — **la dispersione di `median(x)` FRA PASSI**: è il §1.6, e `P3` da solo non lo
  vedrebbe.

**LE LETTURE, FISSATE ADESSO:**
- **rapporto ~1 con dispersione trascurabile** → **cura cosmetica: si dice e ci si ferma;**
- **`median(x)` resta 1 a dieci cifre** → **l'anello non è rotto: FERMARSI e capire perché;**
- **`median(x)` si stacca da 1** → **A3 si scioglie: si procede alla cura;**
- **⚠ `median(x)` oscilla quanto `median(|f|)`** (≈ 62 %) → **si procede lo stesso** *(A6 viene
  prima)* **ma si DICHIARA che il metro resta ballerino, e diventa un fronte nuovo.**

**§2 — la cura**, col progetto di §1.4 e i cinque presidi. **§3 — i sigilli P0-P10**, con `P1`, `P3`,
`P6`, `P7` decisivi.

**⚠ COME FARÒ `P1` (riduzione al limite), e dichiaro il rischio:** il limite è
`med_prec = med_corrente`. Nel **SIGILLO** avvolgerò `ritmo()` con un wrapper che ricostruisce `f`
con la stessa legge, calcola `median(|f|)` e **lo inietta in `_med_f_prec` prima di chiamare il
`ritmo()` NUOVO**. **Il rischio è che il wrapper ricostruisca `f` male** — ma in quel caso **`P1`
FALLISCE**, non passa in silenzio: **l'errore si denuncia da solo.** *(Il wrapper sta nel sigillo,
mai nel simulatore.)*

**COSA MI FA FERMARE:** `median(x)` ancora 1 esatto (l'anello non è rotto), oppure `P7` che mostra
il tetto spostato (**allora è un cambio di gauge e decide Luca**).

**E una cosa che NON farò:** non cambio il riferimento, non introduco sotto-passi, non salvo un
array, non tocco `+1e-6` / `max(...,1e-9)` / `x/sqrt(1+x²)` / `TAU_LOC`, e **nessun fallback su
`med` corrente**.

---

## 3. TODO DEL NEXT STEP

- [x] **§1 A/B/C/D** — la misura preliminare → **riporta**
- [x] previsioni qualitative → commit
- [x] **§2** — la cura: `ritmo()` legge `_med_f_prec` e registra `_med_f_ultimo`; `step()` promuove
      a `:3129-3131`; contatori; fallback `np.ones(n)` contato
- [x] **§3** — `P0-P10`, con `P1`, `P3`, `P6`, `P7` decisivi
- [x] registro + relazione + **CHECKPOINT**
- [x] **⚠ NON toccato:** il riferimento, `+1e-6`, `max(...,1e-9)`, `x/sqrt(1+x²)`, `TAU_LOC`

---

## 4. ESITO

**PRESO, ed erano tre correzioni al mandato, tutte dal disco:**
1. **il blocco di snapshot non è a `:2944-2947`** (è un docstring) **ma a `:3116-3121`** — e la
   distinzione contava: gli snapshot **consumati** da `ritmo()` si promuovono a **`:3129-3131`**,
   cioè **dopo**;
2. **il mandato citava `Z33` col segno rovesciato**, e l'avevo misurato io (`680d069`);
3. **`ritmo()` ha TRE call-site, due diagnostici** — **nessuno l'aveva nominato, e ha DECISO il
   progetto**: `ritmo()` legge, `step()` promuove.

**PRESO, e ha cambiato la cura:** la previsione che **`Z33` si sarebbe ROVESCIATA** invece di
sparire. **Il rapporto `med_t/med_{t-1}` ha `max = 4.81e+07`, ed è esattamente il passo dopo un
gauge degenere.** **Da lì è nato il presidio «non si promuove un `med` sul pavimento», che non era
nel mandato — e ha sparato 2 volte su 2.**

**PRESO, §1.6 e previsione 5:** il metro sarebbe rimasto ballerino. **Confermato più forte della
stima** (`0.326 / 2.997` contro `0.53 / 2.10` previsti) → **`Z43`**.

**NON PRESO, ed è un errore mio nel SIGILLO:** estraevo il blob di riferimento con **`HEAD:`** invece
che per SHA. `HEAD` era già il commit della cura: **ho confrontato il codice curato con sé stesso**,
e `P2` ha dato **`max|A-B| = 0.000e+00` con shape UGUALI** — la trappola già catalogata **col segno
rovesciato**. **Committato il fallimento PRIMA di aggiustare** (par.5, `c818208`).
**È un difetto di STRUTTURA:** un riferimento ancorato a `HEAD` si sposta col lavoro.

**E UNA SVISTA DI PROCESSO, la quarta volta:** ho usato `git commit -m` con dei backtick nel
messaggio, e la shell ne ha eseguito uno (`b98c5d1` ha perso la parola «`f`» in una riga; i numeri
sono intatti). **La regola «si usa `git commit -F` con un file scritto a parte» esiste già — ed è un
caso di A9: una nota che non impedisce il ripetersi non è un presidio.** Da qui in avanti **`-F`
sempre**, senza eccezioni per i messaggi corti.

## 5. TODO DEL PROSSIMO PASSO

- [ ] **`Z43` — DECIDE LUCA:** un gauge che oscilla del **62 % fra passi** è il metro che vogliamo?
      Le strade assolute sono chiuse (`Z41`), la cucitura pure (`Z37`): **resta `f = Δangle/dt_n`**
- [ ] **`Z9` su ≥ 4 semi:** `P8` su un seme non è interpretabile (previsione 6)
- [ ] **il gate:** il blob certificato è ancora `c0803713` e resta indietro (par.0); `a1ae5090`
      porta una cura **sigillata 10/10**, ma il gate si timbra **dopo** il rigiro completo
- [ ] **⚠ NON toccato:** il riferimento, `+1e-6`, `max(...,1e-9)`, `x/sqrt(1+x^2)`, `TAU_LOC`, `r_unit`
