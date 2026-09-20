# REFERTO — **il bivio non e' un bivio: `d0` ha DIECI scrittori, e nessuno e' contato**

> Mandato: *«gli otto salti di `d0`: mitosi o `t_visco`?»* — **dai dati gia' girati.**
> **Nessuna rigiocata nuova. Nessuna cura. Simulatore `edb8f844`, non toccato.**
> Dati: `csv/_test_fork/_d0_chi_lo_muove.txt`, `_rigiocata_0_120.txt`, gli snapshot dei due rami.
> **⚠ E una premessa del mandato e' scaduta: il ramo A NON «continua» — ha FINITO alle 20:20**
> *(3000 passi, intatto, `1d511be`)*. Non c'era nulla da non toccare.

---

## 1. ⚠ PRIMA DI TUTTO: **`d0` NON HA DUE SCRITTORI. NE HA DIECI.**

Enumerati dal codice, **non dedotti**:

| dove | cosa fa | tipo |
|---|---|---|
| `:2083` | `d0 = concat([d0, dd])` — archi nuovi da `semina`/`nuova_massa` | **discreto** |
| **`:4067`** | **`d0 += dt_e*(d - d0)/tau_p_loc`** — **il rilassamento viscoelastico** | **continuo** |
| `:4077` | `d0 += clip(dt_e*cs*d_arco*lap(d0), ...)` — diffusione di superficie (`GUSCIO_MORBIDO`) | **continuo** |
| `:4254` | `d0 = d0 + spinta` — *«Locale pura»* | **continuo** |
| `:4379` | `d0 = concat([d0[keep], d0new])` — **la mitosi** | **discreto** |
| `:4466` | `d0 = concat([d0, dd, dd])` — Schwinger | **discreto** |
| `:4669` | `d0[mask] += proj` | **continuo** |
| `:4812` · `:4816` | `d0[mask] += spinta*median(d0)` · `+= grav*median(d0)` | **continuo** |
| `:4835` | `d0[mask] += flusso` | **continuo** |
| `:4877` | `d0[mask] += clip(coesione_relazionale, ...)` | **continuo** |
| `:4080` `:4255` `:4670` `:4817` `:4836` `:4878` `:4917` | `d0 = max(d0, _floor_d0())` — **sette pavimenti** | vincolo |

> **SEI aggiornamenti CONTINUI per passo, TRE discreti, SETTE pavimenti.**
> **Il bivio «mitosi o `t_visco`» presuppone due candidati: ce ne sono dieci, e NESSUNO e' contato.**

---

## 2. ⚠ CANDIDATO ① — **LA MITOSI: REFUTATO DAL CODICE**

```python
:4379   self.d0 = np.concatenate([self.d0[keep], d0new])
```
**Gli archi in `keep` conservano il loro `d0` ESATTAMENTE.** Gli archi **divisi** (`sel`) **NON sono
in `keep`: vengono RIMOSSI** e sostituiti da due archi nuovi con `d0new = dh` *(la meta')*.

> **Quindi la mitosi NON PUO' dimezzare il `d0` di un arco che sopravvive: o l'arco sparisce, o il
> suo `d0` non viene toccato.**

**E l'arco `16-481` NON e' mai stato diviso:** l'ho seguito **per coppia di nodi** a tutti e 120 i
passi e **c'era sempre** — se fosse stato diviso, la ricerca avrebbe restituito `-1` e `d` sarebbe
stato `NaN`. **Non e' mai successo.**

**Il candidato ① cade, e cade PER DIMOSTRAZIONE, non per misura.**
*(E il mandato lo sospettava gia': «la mitosi DIMEZZA, non allunga, e i rapporti sopra 1 non possono
venire da lei». La refutazione e' piu' forte: non puo' venire da lei nemmeno quelli sotto 1.)*

---

## 3. CANDIDATO ② — **`t_visco`: il MECCANISMO e' quello giusto, ma l'INSTABILITA' NON C'E'**

Il codice governa `d0` proprio con `t_visco`, e **dichiara da solo la propria soglia di stabilita'**
*(`:4060-4063`, e la soglia quindi non la scelgo io)*:

```python
# PRESIDIO DI STABILITA', permanente: il rilassamento d0 += dt_e*(d-d0)/tau_p e' un
# Eulero esplicito, e DIVERGE OSCILLANDO se dt_e/tau_p >= 1.
self._taup_cfl_max = max(..., dt_e / tau_p_loc)
self.d0 += dt_e * (self.d - self.d0) / tau_p_loc          # tau_p_loc = max(t_luce, t_visco)
```

**MISURATO dagli snapshot — il contatore ESISTE GIA':**
```
_taup_cfl_max      ramo A, passo 3000:  0.5656
                   ramo B, passo  360:  0.5650
```
> **Entrambi `0.565`, praticamente IDENTICI, ed entrambi SOTTO la soglia `1` che il codice dichiara.**
> **Il rilassamento di `d0` NON sta divergendo, in nessuno dei due rami.**

### 3.1 E c'e' un argomento di SEGNO che chiude il punto

`d0 += dt_e*(d - d0)/tau_p` **muove `d0` VERSO `d`**. Sull'arco `16-481`, `d` **cresce** (`0.73 ->
1.97`) mentre `d0` **cala** (`0.73 -> 0.24`): **`d0` si allontana da `d`.**

> **Il rilassamento del `:4067` NON PUO' essere cio' che spinge `d0` in giu': va nella direzione
> opposta.** **Il colpevole sta fra i SEI aggiornamenti continui del par.1**, e nessuno di essi
> e' contato.

---

## 4. ⚠ MA UNA DIFFERENZA FRA I RAMI C'E', ed e' su `peq` — **e il codice aveva gia' il contatore giusto**

Il codice, a `:4034-4039`, spiega **perche'** tiene DUE contatori e non uno:
> *«il contatore cumulativo da solo non distingue "un difetto sempre presente" da "un transitorio di
> accensione moltiplicato per il numero di archi": sono diagnosi OPPOSTE, e senza questo secondo
> contatore si sceglie quella che si ha in mente.»*

**MISURATO:**
```
                     peq_degenere (cumulativo)     deg_passi (PASSI DISTINTI)
ramo A   passo  120        527 088                          1
ramo A   passo 3000        527 088   <- FERMO               1   <- FERMO su 3000 passi
ramo B   passo  120        527 088                          1
ramo B   passo  240        527 191                         14
ramo B   passo  360        527 580                         30   <- e CRESCE
```

> **RAMO A: `peq` degenera in UN SOLO passo — il primo — e MAI PIU', per 3000 passi.**
> **E' il TRANSITORIO DI ACCENSIONE** *(`Z6`: `psi` non e' calcolato prima del primo `step`)*.
> **RAMO B: degenera in `1 -> 14 -> 30` passi distinti, e il numero CRESCE. E' RICORRENTE.**

**E la frazione causale:**
```
caus/tot (cumulativa)    ramo A: 0.0436 (p120)  ->  0.4823 (p3000)
                         ramo B: 0.4085 (p120)  ->  0.4986 (p360)
```
**Al passo 120 B sta gia' a `0.409` dove A sta a `0.044`: DIECI VOLTE.**

### 4.1 ⚠ Ma cosa fa `peq` degenere a `d0`: **CONGELA, non spinge**

```python
_peq = np.where(_peq_ok, self.peq, 1e-30)
t_visco = t_luce * (rho_arco / _peq)        # peq = 1e-30  ->  t_visco ENORME
tau_p_loc = np.maximum(t_luce, t_visco)     # ->  tau_p ENORME
self.d0 += dt_e * (self.d - self.d0) / tau_p_loc     # ->  incremento ~ ZERO
```
> **Su un arco con `peq` degenere il rilassamento di `d0` si SPEGNE.**
> **Se `peq` degenera a INTERMITTENZA, `d0` si muove A SCATTI — il che e' esattamente il profilo
> osservato — ma NON spiega il SEGNO: spiega perche' si muove a tratti, non perche' vada in giu'.**

**⚠ E questa resta un'IPOTESI:** i contatori di `peq` sono **GLOBALI**, non per arco.
**Non posso dire se `peq` sia degenerato sull'arco `16-481` nei passi dei salti.**

---

## 5. §1 DEL MANDATO — **il test proposto NON discrimina, e si vede dai numeri**

Il test era: *«`n` SALE nel campione del salto -> mitosi; `n` e' FERMO -> non mitosi»*.

**`n` sale in OGNI finestra di 5 passi**, dal primo all'ultimo:
```
n:  2391  2460  2516  2547 ... 2802  2814  2820  2828 ... 2975  2982  2998
```
**607 nascite in 120 passi su ~528 000 archi.** Una nascita **da qualche parte** e' l'evento normale:
**cio' che conterebbe e' una nascita SU QUELL'ARCO**, e quella la mitosi non la fa (par.2).

> **Il test non separa niente, e non e' un difetto del mandato: e' che la domanda presupponeva due
> candidati, e i candidati sono dieci.**

---

## 6. COSA SERVIREBBE, col costo — **e NON lo faccio di mia iniziativa**

**NON serve una rigiocata piu' fine.** Campionare ogni passo invece che ogni cinque **non direbbe
CHI ha mosso `d0`**: direbbe solo **quando**, e lo so gia'.

**Serve strumentare i DIECI scrittori**, byte-inerti, come i quindici gia' cablati:
```
per ogni sito: quante volte ha toccato `d0`, e la SOMMA ALGEBRICA del delta che ha prodotto
                (la somma col SEGNO, non il conteggio: il conteggio non dice chi spinge in giu')
```
**E per l'arco singolo serve una versione per-arco su un sottoinsieme dichiarato** *(i cinque nodi)*,
se no sono `528 000` accumulatori.

**COSTO:** **il simulatore cambia**, quindi **blob nuovo**, **sigillo di byte-identita'**, e
**tutti i sigilli della riproducibilita' da rigirare** *(la stessa spesa che il mandato attribuiva
alla cura ①)*. **E' un giro serio, e la decisione e' di Luca.**

---

## 7. LO STATO, onesto

| | |
|---|---|
| **① mitosi** | **REFUTATO per DIMOSTRAZIONE** — gli archi che sopravvivono conservano `d0` esatto |
| **② `t_visco`, instabilita' numerica** | **REFUTATO per MISURA** — `_taup_cfl_max = 0.565 < 1` in **entrambi** i rami |
| **② `peq` degenere** | **DIFFERENZA REALE FRA I RAMI** *(`1` passo contro `30` e in crescita)*, **ma spiega il «a scatti», non il SEGNO**, e i contatori sono **globali** |
| **chi spinge `d0` in giu'** | **NON DETERMINATO.** Sta fra i **sei** aggiornamenti continui, e **nessuno e' contato** |

> **Nessuna cura, come il mandato chiede. E nessuna delle due cure descritte nel §3 del mandato e'
> giustificata da questi numeri:** la rampa bifase cura un meccanismo **refutato**, e la caccia a
> `peq` cura un meccanismo **reale ma del segno sbagliato**.
