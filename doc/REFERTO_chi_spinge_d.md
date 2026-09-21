# REFERTO — **è `cs²·lap` che allunga l'arco: la TENSIONE DEI VICINI, diffusa**

> Mandato: *«perché un arco si allunga centocinquanta volte?»* — **misura, nessuna cura.**
> Simulatore `01146a16 -> b46835bd` *(solo `TRACCIA_VD`, byte-inerte)*. Sigillo `4/4`
> *(`Z1` byte-identico a flag spento)*. Rigiocata `0 -> 120` del ramo B.
> Dati: `csv/_test_fork/_traccia_vd_replay.txt`.

---

## 1. LA RISPOSTA — **`cs²·lap`, 409 volte su 488**

```
CHI DOMINA sull'arco 16-481, passo per passo (488 sotto-passi):
    cs2*lap     409   (83.8 %)      <- e spinge VERSO L'ESTERNO
    -beta*vd     79   (16.2 %)      <- e' sempre un FRENO
    src           0   ( 0.0 %)      <- MAI
```

**Le mie tre aspettative, scritte prima** *(task history `77ed65c`)*:
- *«mi aspetto che domini `cs²·lap`»* -> **CENTRATA;**
- *«mi aspetto che `src` sia piccolo in questa finestra»* -> **CENTRATA, e piu' di cosi': non
  domina MAI, e vale `10^-3`-`10^-2` contro il `3.7` di `lap`;**
- *«mi aspetto che `beta·vd` sia un freno reale ma non sufficiente»* -> **CENTRATA: e' sempre di
  segno opposto a `vd`, e non basta.**

---

## 2. IL MECCANISMO — **`lap` è il laplaciano dell'ALLUNGAMENTO, non di `d`**

```python
q   = self.d - self.d0                       # l'ALLUNGAMENTO dell'arco
med = (bincount(i,q) + bincount(j,q)) / _deg # la media di `q` sui vicini di ogni nodo
lap = 0.5*(med[i] + med[j]) - q              # quanto l'arco e' MENO teso dei suoi vicini
```
> **`lap > 0` significa: i vicini sono piu' tesi di me.** **E `acc += cs²·lap` mi allunga fino a
> raggiungerli.**
> **Non e' una forza esterna: e' la TENSIONE DEI VICINI che si DIFFONDE.** E' la terza lettura del
> mandato — *«la propagazione stessa allunga l'arco»* — **e `lap` è di `q`, non di `d`.**

**Sull'arco `16-481` nei primi 70 passi:**
```
passo    cs2*lap        d        d0    (q = d-d0)
10      +3.7267     0.7381    0.7381     ~0        <- l'arco NON e' teso, i vicini SI'
30      +3.5283     0.8428    0.8427     ~0
70      +2.2543     1.3600    1.1730     0.187
```
> **Il nostro arco parte NON TESO (`q ≈ 0`) in un vicinato TESO, e viene tirato.**

---

## 3. ⚠ E IL SEGNO SI RIBALTA QUANDO `d0` CROLLA — **i due meccanismi sono ACCOPPIATI**

```
passo    d0        q = d-d0      cs2*lap
70     1.1730       0.187        +2.2543
80     0.4949       0.995        -0.9174     <- d0 CROLLA, q SALTA, lap si RIBALTA
90     1.1590       0.502        +0.7637
100    1.0310       0.734        -0.2040
110    0.3610       1.514        -3.0320     <- d0 = 0.36, q = 1.51, lap FORTEMENTE negativo
```
> **Quando `d0` crolla, `q = d - d0` salta, l'arco diventa il PIU' TESO del vicinato, e `lap`
> cambia segno.**
> **Il crollo di `d0` (`Z79`/`Z80`) RIENTRA in `lap` e ne ribalta la spinta.**
> **Non sono due difetti separati: sono un ANELLO.** *(E `A6` riguarda le letture istantanee; qui
> il ciclo passa per `q`, ed e' dentro lo stesso passo.)*

---

## 4. ⚠ E IL FRENO SI INDEBOLISCE — **misurato, `9.4x`**

`beta = 2·ZETA_M·cs / max(d, 1e-6)`: **inversamente proporzionale a `d`.**

```
passo      beta      d
10        1.740    0.738
40        0.514    0.946
70        0.347    1.360
110       0.186    1.875     <- il freno e' 9.4 VOLTE piu' debole che al passo 10
```
> **Mentre l'arco si allunga, la forza che dovrebbe frenarlo si indebolisce nella stessa
> proporzione.** **Era leggibile dalla formula; ora e' misurato.**

---

## 5. ⚠ POPOLAZIONE E ARCO DICONO IL CONTRARIO — **la lezione di `Z79`, di nuovo**

```
                      cs2*lap mediana        sull'arco 16-481
popolazione (5 nodi)  -0.846 -> -0.368       +3.727 -> -3.032
```
**Sulla POPOLAZIONE `cs²·lap` è NEGATIVO: il grosso degli archi viene COMPRESSO.**
**Sul NOSTRO arco è POSITIVO per 70 passi: viene TIRATO.**

> **Il sistema medio si contrae; questo arco si allunga.** **Guardando solo il riassunto avrei
> concluso «`lap` comprime», che è vero sulla popolazione e falso sull'arco che è esploso.**
> **È la terza volta in due giorni che le due letture divergono ed è la seconda volta che il
> riassunto, da solo, avrebbe dato la risposta sbagliata.**

---

## 6. COSA CADE, E COSA RESTA

| candidato | esito |
|---|---|
| **`src` come motore** | **REFUTATO: domina `0` volte su `488`**, e vale `10^-3`-`10^-2` contro `3.7`. *(Resta il sospetto sulla SECONDA FASE di B — `n1 = 15594` — ma quella e' DOPO il passo 390, e questa finestra non la vede: dichiarato prima di misurare.)* |
| **`-beta*vd` troppo debole** | **CONFERMATO in parte**: e' sempre un freno, domina il `16 %` dei passi, **e si indebolisce di `9.4x` mentre l'arco cresce** |
| **`cs²·lap` allunga** | **CONFERMATO: `84 %` dei passi**, ed e' la **tensione dei vicini diffusa** |
| **`d0` e `d` sono due problemi separati** | **REFUTATO: sono un ANELLO.** `d0` crolla -> `q` salta -> `lap` si ribalta |

---

## 7. COSA QUESTO REFERTO **NON** DICE

- **NON dice che `cs²·lap` sia sbagliato.** Un laplaciano dell'allungamento **è** un meccanismo di
  propagazione legittimo: dice che **è lui a muovere `d`**, e che **nessuno lo frena** quando `beta`
  si indebolisce;
- **NON vede la seconda fase di B** *(`src`/`n1`)*: al passo 120 non era cominciata. **Dichiarato
  nel task history PRIMA di misurare;**
- **NON spiega perche' il VICINATO fosse gia' teso al passo 10.** L'arco viene tirato da vicini
  gia' tesi: **da dove viene la loro tensione non e' misurato**, ed e' la domanda successiva;
- **UN seme, UN arco, 120 passi**, e `16-481` e' **il peggiore del sistema**: caso estremo.
