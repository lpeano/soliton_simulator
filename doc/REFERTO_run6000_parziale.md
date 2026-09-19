# REFERTO PARZIALE — **il run a 6000 passi, letto al frame 450 su 1000**

> **⚠ IL RUN NON È FINITO.** Questo è un referto **a metà**, scritto perché i dati parziali dicono
> già qualcosa e perché servano a Claude web **prima** della fine. **Nessuna conclusione di fisica:
> i numeri e la forma** *(mandato ③)*.

**Data** 2026-09-19 · **blob del simulatore** `7c4dec1d` *(sigillato 12/12)* · **driver**
`f14ea4bd` · **seme effettivo `42`** *(letto da `Rete.__init__`; `SEME_INIZIALE = 900` è il **numero
di nodi**, non il seme — solo il `--batch` lo riusa come seme)*.

**Provenienza dei numeri:** `csv/_test_fork/_g6000/prog.csv`, scritto dal driver a ogni 5 frame, con
blob, seme e i 20 flag **dentro il file** (P6). **Nessuno snapshot è stato aperto per questo
referto:** tutto viene dal CSV di progresso, a costo zero per il run che sta ancora girando.

```
CAMPO_SPINORIALE=1 SPINORE_VIVO=1 SPINORE_CORRETTO=1 CHI_CORE=1 CS_DINAMICO=1 TAU_LUCE=1
CHI_BASC=1 FORK_SU2=1 FORK_SU2_MEM=1 STEP2_OROLOGIO=1 SPIN_FEEDBACK=1 PLAST_DIN=1 VERLET=1
RUMORE_COLORATO=1 PAV_COM=1 GUSCIO_MORBIDO=1 ZETA_VIR=1 VIRIALE=1 OLON_PART=1 CALORE_VETTORIALE=0
```

> **⚠ `--tau-luce` è attivo e il suo sigillo è 6/7** *(`T3` è un risultato dichiarato, `T4`/`T5`
> dicono che la legge è sana)*. **Ogni numero qui sotto lo eredita.**
> **⚠ `--chi-basc` riscrive `perc_chi` a ogni passo: non è un'etichetta di lignaggio.**

---

## 1. I DATI

| frame | passo | n | archi | coer_l | dil % |
|---|---|---|---|---|---|
| 1 | 6 | 2391 | 429498 | 0.6394 | +7.88 |
| 25 | 150 | 2391 | 429498 | 0.4223 | +23.25 |
| 50 | 300 | 2576 | 429724 | 0.2859 | +25.14 |
| 75 | 450 | 3046 | 430319 | 0.3420 | +20.44 |
| 100 | 600 | 3433 | 430813 | 0.3749 | +15.76 |
| 150 | 900 | 3907 | 431418 | 0.4217 | +20.13 |
| 200 | 1200 | 4445 | 432102 | 0.4756 | +18.16 |
| 250 | 1500 | 5143 | 433007 | 0.5482 | +12.32 |
| 300 | 1800 | 5938 | 434010 | 0.6084 | +5.67 |
| 350 | 2100 | 6924 | 435249 | 0.6215 | **−3.12** |
| 400 | 2400 | 8018 | 436636 | 0.6691 | −1.13 |
| 425 | 2550 | 8696 | 437497 | 0.6661 | −4.89 |
| 450 | 2700 | 9511 | 438532 | 0.6867 | **−13.25** |

**Tempi:** `7013 s` al frame 450 (`1.95 h`). Costo per frame da `14.35` a `15.77 s` (**+10 %**).
**Fine stimata intorno alle 6 h totali** *(la stima dal pilota diceva 7.5 h: era prudente)*.

---

## 2. IL FATTO STRUTTURALE — **il sistema aggiunge NODI ma quasi non aggiunge ARCHI**

```
n           x3.98    (2391 -> 9511)
archi       x1.021   (429498 -> 438532)     <- QUASI FERMI
grado medio x0.26    (359.3 -> 92.2)
archi nuovi per nodo nuovo: 1.27
```

| frame | n | archi | **grado medio** |
|---|---|---|---|
| 1 | 2391 | 429498 | **359.3** |
| 110 | 3544 | 430955 | 243.2 |
| 225 | 4789 | 432556 | 180.6 |
| 340 | 6708 | 434978 | 129.7 |
| 450 | 9511 | 438532 | **92.2** |

> **Il grado medio è crollato di un fattore 4 mentre la popolazione quadruplicava.** Il sistema
> cresce **per accrescimento periferico**: i nodi nuovi nascono con **due** archi verso i genitori
> — misurati **1.27 netti**, quindi qualche arco viene anche **rimosso** — mentre il nucleo
> originale ne ha centinaia.

**Non è un fatto nuovo, è l'estensione di uno già misurato:** `Z9` aveva trovato che *«i nati dopo
sono il 70.2 % dei NODI ma portano l'1.37 % degli ESTREMI D'ARCO — grado mediano 496 contro 2»*.
**Qui si vede la stessa cosa come TENDENZA nel tempo, su 450 frame.**

**E spiega un numero che altrimenti sorprenderebbe:** il costo per frame è cresciuto solo del
**10 %** mentre `n` **quadruplicava**. Il costo è dominato dagli **archi**, non dai nodi — ed è la
stessa ragione per cui il peso di uno snapshot è passato da `28.7` a `30.8 MB` *(+7 %)* nello
stesso intervallo.

---

## 3. LE DUE GRANDEZZE CHE SI MUOVONO

**La coerenza locale crolla e poi RISALE, monotonamente.** Da `0.6394` (frame 1) al minimo
**`0.2840`** (frame 40), poi su fino a **`0.6867`** al frame 450 — **il massimo del run, e sta
ancora salendo**.

**La dilatazione fa l'opposto.** Sale al massimo **`+26.28 %`** (frame 35), poi scende **senza
fermarsi**, passa in negativo intorno al frame 350, e arriva a **`−13.25 %`**.

### ⚠ IL FATTO NUOVO: oltre dove `Z49` si fermava, la dilatazione NON rimbalza

`Z49` arrivava a 400 frame e aveva visto la dilatazione **rimbalzare**:
`−7.44 → −2.70 → −4.21 → +2.80 → −1.13 %`.

**Da lì in poi:**

```
frame 400   -1.13 %
frame 425   -4.89 %
frame 450  -13.25 %
```

**Non rimbalza: accelera verso il basso.** **È la prima volta che questa scena viene guardata oltre
i 2400 passi**, ed è esattamente ciò per cui il run esiste.

---

## 4. LA TRAIETTORIA COINCIDE CON `Z49` SU UN BLOB DIVERSO

```
frame 400   QUI: n=8018, coer_l=0.6691, dil=-1.132 %      blob 7c4dec1d
            Z49: n=8018, coer_l=0.669,  dil=-1.13  %      blob a1ae5090
```

**Tre grandezze identiche.** Le cure entrate fra i due blob **non hanno spostato questa scena di
una cifra**.

> **Lo riporto come OSSERVAZIONE, non come misura controllata.** Sono due run con **codice
> diverso**, ed è la situazione in cui `A3c` dice di non trasportare i numeri. Quello che si può
> dire è che **coincidono**; *perché* coincidano non l'ho misurato, e non lo invento.

---

## 5. LE MIE CONSIDERAZIONI — **separate dai dati, e dichiarate come tali**

**① Il sistema si sta CONTRAENDO, e la contrazione accelera.** Dei tre segnali, due vanno nella
stessa direzione: la dilatazione scende sempre più in fretta e la coerenza locale sale. **Se sono
la stessa cosa vista da due lati, non lo so**: non ho misurato la loro relazione, e correlare due
curve nel tempo su **un seme** non sarebbe una misura.

**② La previsione `P10` non è ancora decidibile.** Avevo previsto *«almeno un secondo minimo dei
nodi interni»*. La dilatazione che scende **suggerisce** una nuova contrazione, ma `P10` parla di
**nodi nella regione interna in unità comoventi**, che stanno **negli snapshot**. **Usare `dil`
come sostituto sarebbe cambiare la grandezza dopo aver visto i dati.**

**③ La struttura che emerge è un nucleo denso più una periferia rarefatta**, e il grado medio che
si divide per 4 lo dice meglio di `n`. **Ma "nucleo" e "periferia" sono parole mie**: il dato è
`grado medio 359 → 92`, e la distinzione fra due popolazioni **non l'ho misurata qui** — `Z46` e
`Z9` l'hanno misurata su altre scene.

**④ Quello che mi aspetto di sbagliare.** La mia estrapolazione dal pilota diceva `n ≈ 8400` a 1000
frame: al frame 450 siamo già a **9511**. **Era sbagliata di un fattore 3-5**, e la ragione era
dichiarata — il pilota misurava i primi 60 frame, in cui `n` **non cresceva affatto**. Le stime
attuali (**24 000 lineare, 48 000 esponenziale**) vengono dallo stesso tipo di estrapolazione e
**meritano la stessa diffidenza**.

**⑤ Il rischio che vedo sul risultato principale.** `Z9-a` dava `passi(ramp = 1) = 5098` con un
margine del **18 %** sui 6000 del run, e `r` si era mosso del **+149 % in 120 passi**. **Se `r`
scendesse, `Z9-b` smetterebbe di crescere** — ed è il modo in cui `Z9` resterebbe aperta per
sempre. **Questo si legge solo dagli snapshot**, e finché non li apro non so da che parte stia
andando.

---

## 6. COSA MANCA, E PERCHÉ NON L'HO MISURATO

**`Z9-b`, `ramp` per coorte, `p95/p05` del kernel, le conseguenze (`base`, `psi`, `rho_spin`, `cs`)
e il ciclo dei nodi interni sono tutti DENTRO gli snapshot**, non nel CSV di progresso.

L'analizzatore è **scritto, committato e pronto** (`csv/_test_fork/_misure_run6000.py`), legge in
**sola lettura** e non tocca l'archivio. **Non l'ho girato perché costa CPU al run che sta ancora
girando**, e oggi il run ha già condiviso la macchina in due finestre *(il sigillo della ripresa,
~7 min; la verifica della finestra della patch, ~3 min)*.

**Due avvertenze sui tempi, da non leggere come fisica:** in quelle due finestre il costo per frame
è salito da `14.85` a `15.54 s`. **Non è il sistema che rallenta: è la macchina condivisa.**

---

## 7. I LIMITI, tutti insieme

- **il run NON è finito**: frame 450 su 1000;
- **UN SEME, UNA SCENA**. Nessuna identificazione *(bounce, oscillone, protone, confinamento)*;
- **`--tau-luce` ha sigillo 6/7**: ogni numero lo eredita;
- **`--chi-basc` riscrive `perc_chi`**: se comparisse antimateria verrebbe dal **basculamento**,
  non dalla generazione;
- il confronto con `Z49` è fra **blob diversi**;
- **le previsioni sono committate PRIMA** in `doc/PREVISIONI_run6000_scena.md`: quando il run
  finisce si confrontano con quelle, **non con quelle che sembreranno ragionevoli allora**.
