# REFERTO — **le due finestre a 6 passi: `ritmo()` NON nasce saturo, e la mitosi NON c'entra**

**Blob `7c4dec1d`** · seme **42** · sigillo della rigiocata **3/3**
(`csv/_seal_fork/_rigioca_finestre.txt`, script `d4b32fae`) · dati in `csv/_test_fork/_fin_A`
(10 snapshot) e `_fin_B` (11) · cronologie in `_fin_A_cronologia.txt` e `_fin_B_cronologia.txt`.

> **RISOLUZIONE 6 PASSI, NON 5, e dichiarato PRIMA di misurare:** il driver campiona in **frame**,
> e `PASSI_PER_FRAME = 6`. **Dieci istanti per finestra invece di dodici** — comunque **dieci volte**
> più fine dei 60 passi dell'archivio.
> **Driver:** `_scena_video_ripresa.py`, perché quello del run è tornato a `f14ea4bd` e non ha
> `--riprendi`. **`--tau-luce` sigillo 6/7. UN SEME, UNA SCENA.**

---

## 0. IL SIGILLO PASSA, E DICE UNA COSA IN PIÙ

```
SA  da ZERO -> passo 60  : 113 campi confrontati, 0 diversi   IDENTICO
SB  da 180  -> passo 240 : 113 campi confrontati, 0 diversi   IDENTICO
SC  due istanti diversi risultano diversi: il confronto NON e' cieco
```

> **`SA` non era nel mandato: viene gratis con la finestra A, ed è la prima verifica che il run sia
> riproducibile DA CAPO.** Ripartendo da zero, stesso seme e stesso blob, si riottiene
> **esattamente** lo stato del passo 60. **Finora era solo argomentato.**

## 1. FINESTRA `0 → 60` — **`ritmo()` NON nasce saturo. Satura in 24 passi**

**Era la domanda:** *«`r` al passo 6 è già a `√2`?»*

```
passo  6:  r p25 = 0.1330   p50 = 0.8569   p75 = 0.8965      <- NON saturo
passo 12:  r p25 = 0.0731   p50 = 1.2004   p75 = 1.2735
passo 18:  r p25 = 0.1644   p50 = 1.3783   p75 = 1.3851
passo 24:  r p25 = 1.3986   p50 = 1.4141   p75 = 1.4141      <- AL TETTO
passo 30..60: p50 = p75 = 1.4141 / 1.4142                    <- ci resta
```

> **NO.** `r` parte a `0.857` di mediana e **raggiunge il tetto `√2` al passo 24**, cioè in
> **quattro frame**. **Poi non lo lascia più** fino al 180.

**Quindi la lettura *«nasce fuori scala, è un difetto di forma»* NON è sostenuta:** c'è una
**transizione vera, datata, di 24 passi**. Il sistema **ci arriva**, non ci nasce.

**E in quella finestra `omega_s` max DECRESCE**, monotonamente: `1.61 → 1.12`. **Nessuna mitosi**
(`nati = 0` per tutti i 60 passi). **Archi e nodi immobili.**

## 2. FINESTRA `180 → 240` — **l'evento è al passo 198, e la MITOSI non c'entra**

```
passo   om max     r p50     nati
180      0.35      1.2731     2
186      0.329     1.4110     2
192      0.31      1.4092     3
198    401         0.4919     3     <- omega x1300 in 6 passi, r CROLLA, NATI FERMO
204    371         0.3539     4
210    334         1.3084     6
216   7470         0.4973     9
222   3.07e+04     1.0156     9
228   3.53e+04     1.2905    14
234   5.77e+04     0.2771    23
240   7.58e+04     0.3529    26
```

### ⚠ IL FATTO: a 60 passi mitosi ed evento coincidevano. **A 6 passi si separano.**

**Fra il passo 192 e il 198 `nati` resta a `3`: non nasce nemmeno un nodo**, e in quei sei passi
`omega_s` max fa **×1300**. **La mitosi comincia a correre DOPO** (`4, 6, 9, 9, 14, 23, 26`).

> **L'osservazione del referto precedente — *«l'esplosione coincide con l'inizio della mitosi»* —
> era un artefatto della risoluzione a 60 passi. A 6 passi cade.**

### E il secondo fatto solido: **i picchi crescono in modo monotono**

```
omega_s max:  0.35 · 0.329 · 0.31 | 401 · 371 · 334 | 7470 · 3.07e4 · 3.53e4 · 5.77e4 · 7.58e4
```

**Dopo il 198 non torna mai indietro: cresce di ~190 volte in 42 passi.**

## 3. ⚠ UNO SCHEMA CHE AVEVO VISTO, MISURATO, E CHE NON REGGE

Guardando la tabella sembrava che `r` e `omega_s` oscillassero **in antifase** *(r crolla → omega
sale; r risale → omega cala)*. **L'ho misurato invece di scriverlo:**

```
corr(r_p50, log10(omega_max))              = -0.6166     11 campioni
corr delle VARIAZIONI                      = -0.5781     10 intervalli
nullo su n = 10:  sigma ~ 1/sqrt(n)        =  0.316   ->  1.8 sigma
intervalli con segno OPPOSTO               =  5 su 10  ->  ESATTAMENTE il caso
```

> **NON È SOSTENUTO.** `1.8 σ` su dieci punti, e il conteggio dei segni dà **il valore sotto
> ipotesi nulla**. **L'antifase resta un'impressione visiva, e non la scrivo come risultato.**

## 4. ⚠ E UN LIMITE CHE IMPEDISCE DI DIRE DI PIÙ

`r` cambia **fra campioni adiacenti** (`1.41 → 0.49 → 0.35 → 1.31 → 0.50`), cioè su **6 passi**.
**Il periodo vero è ≤ 12 passi e NON è risolto: siamo al limite di Nyquist.**

> **Non dichiaro un periodo, e non chiamo «oscillazione» ciò che potrebbe essere aliasing**
> (`CLAUDE.md` §4: *un sistema campionato a intervalli costanti può sembrare fermo o andare a
> velocità falsa*). **Per risolverlo servirebbe una rigiocata a 1 frame o meno** — e il driver non
> scende sotto il frame.

---

## 5. COSA QUESTE DUE FINESTRE HANNO CAMBIATO

| prima | dopo |
|---|---|
| *«`r` era già saturo al primo snapshot: forse nasce fuori scala»* | **`r` satura in 24 passi. È una transizione, non una condizione iniziale** |
| *«l'esplosione di `omega_s` coincide con l'inizio della mitosi»* | **falso a 6 passi: fra 192 e 198 non nasce nessun nodo** |
| *«l'evento è nell'intervallo 180-240»* | **l'evento è AL PASSO 198** |

**Cosa resta aperto:** **cosa accade al passo 198**, e **perché** `r` cambi su scale di 6 passi —
per entrambe servirebbe una risoluzione sotto il frame, che questo driver non dà.
