# REFERTO — **`d0` non e' mosso dalla coesione: e' mosso dal SUO CLIP**

> Mandato: strumentare tutti gli scrittori di `d0`, sigillo bloccante, replay `0 -> 120` sul ramo B.
> **Nessuna cura.** Simulatore `edb8f844 -> d06219de`; flag `TRACCIA_D0`, **`False` di default**.
> Sigillo `csv/_seal_fork/_sigillo_traccia_d0.py` **4/4**; `Z3` = il sigillo interno della
> rigiocata, **`138/138` col flag ACCESO**.
> Dati: `csv/_test_fork/_traccia_d0_replay.txt`, `_clip_saturo.txt`.

---

## 1. LA STRUMENTAZIONE — **diciannove punti, e la mia lista era sbagliata**

Avevo scritto *«`d0` ha DIECI scrittori»* (`Z78`). **Sono DODICI**, piu' **sette** pavimenti:
```
SCRITTORI (12)  :2083  :4067  :4076  :4078  :4254  :4379  :4466  :4669  :4812  :4816  :4835  :4877
PAVIMENTI  (7)  :4080  :4255  :4670  :4817  :4836  :4878  :4917
```
Mi erano sfuggiti **`:4078`** *(il ramo `else` del rilassamento, con `TAU_P` costante)* e la
distinzione fra **`:4812`** e **`:4816`**, che sono **due** scritture.
**Tutti e 19 verificati riga per riga prima di toccarli** *(le sette righe dei pavimenti sono
IDENTICHE: si e' lavorato per numero di riga, dal basso, con un assert per sito)*.

### Il sigillo
```
Z0   blob in BYTE GREZZI:  edb8f844 -> d06219de     (NON `git hash-object`, C18)
Z1   [BLOCCANTE] flag SPENTO -> 10 campi su 10 BYTE-IDENTICI                     PASS
Z1b  flag ACCESO -> la FISICA non cambia comunque                                PASS
Z2   controllo positivo: 404 voci, 15 siti distinti, 8 con somma non nulla       PASS
Z2b  la traccia NON entra nello snapshot (0 campi passano il filtro)             PASS
Z3   [BLOCCANTE] la rigiocata resta fedele: 138/138 COL FLAG ACCESO              PASS
```

---

## 2. IL RIASSUNTO SULLA POPOLAZIONE — **competizione**

`1590` voci, `120` passi, sugli archi dei cinque nodi *(~3100)*:
```
sito                     giri   tocchi  SOMMA ALGEBRICA   max|delta|  tagliati
S12_coesione  (:4877)     120   372735    -3.683995e+03   9.53e-01         0
S09_spinta_med(:4812)     120   372735    -2.063045e+03   9.96e-03         0
S03_diff_guscio(:4076)    120   372729    -1.738649e+02   2.80e-02         0
S08_proj      (:4669)     120   372735    +1.125039e+03   8.80e-03         0
S02_rilass_visco(:4067)   120   370721    +2.128383e+03   3.67e-02         0
i SETTE pavimenti                          da 0 a +1.06                  0..185
```
**Tre spingono in giu' (`-5 921`), due in su (`+3 253`): netto `-2 668`.**
**I pavimenti sono TRASCURABILI:** il piu' attivo taglia `185` archi su `372 735` tocchi e
contribuisce `+1.06` contro `-3 684`. **La terza lettura del mandato — *«`d0` viene TAGLIATO»* —
e' ESCLUSA.**

**⚠ E QUATTRO SITI SU 19 NON SONO MAI SCATTATI in 120 passi** — `S04_rilass_TAU_P`,
`S10_grav_med`, `S11_flusso`, `P5_dopo_flusso`. **`A8`: rami che non girano.**

---

## 3. ⚠ IL DETTAGLIO SULL'ARCO — **e dice una cosa DIVERSA dal riassunto**

Sull'arco `16-481`, a ogni passo campionato, **i cinque siti attivi contribuiscono cosi'**:
```
S02_rilass_visco   da +0.001 a +0.016      \
S03_diff_guscio    ~ +-0.008                 >  tutti insieme: ~ +-0.01
S08_proj           ~ -0.008                 /
S09_spinta_med     ~ +-0.009               /
S12_coesione       da +-0.018 a +-0.64     <<-- DA SOLO, e con AMPIEZZA CRESCENTE
```

| passo | `d0` prima | `d0` dopo *(dopo `S12`)* | mossa |
|---|---|---|---|
| 10 | 0.721771 | 0.739725 | **+0.018** |
| 40 | 0.797560 | 0.954126 | **+0.157** |
| 60 | 1.000760 | 0.769010 | **−0.232** |
| 90 | 1.155616 | 0.671568 | **−0.484** |
| 100 | 1.033998 | 0.395456 | **−0.639** |
| 110 | 0.371759 | 0.743300 | **+0.372** |

> **SUL SINGOLO ARCO scatta la PRIMA lettura — «un solo scrittore» — non la seconda.**
> **`S12_coesione` vale da solo il `96-98 %` del movimento; gli altri quattro sono rumore.**
> **Il riassunto diceva «competizione» perche' SOMMA su 3100 archi: le due letture rispondono a
> due domande diverse, ed entrambe sono vere.**

---

## 4. ⚠⚠ IL REPERTO — **il clip e' SATURO SEMPRE: `d0` e' mosso dal suo LIMITE**

Il sito `:4877` e':
```python
stress_metrico  = np.abs(self.d[mask] - self.d0[mask]) / np.maximum(self.d0[mask], 1e-6)
tasso_dinamico  = np.tanh(stress_metrico) * self.d0[mask]
self.d0[mask]  += np.clip(coesione_relazionale, -tasso_dinamico, tasso_dinamico)
```

**IPOTESI VERIFICATA: se il clip satura, la mossa osservata vale ESATTAMENTE `+-tasso_dinamico`.**

```
passo    d0 prima    d0 dopo          d   mossa oss.  tasso calc.   |mossa|/tasso
10       0.721771   0.739725   0.739729    +0.017954     0.017954     0.999984
40       0.797560   0.954126   0.956185    +0.156566     0.156566     1.000000
60       1.000760   0.769010   1.236792    -0.231750     0.231751     0.999997
90       1.155616   0.671568   1.671386    -0.484048     0.484048     0.999999
100      1.033998   0.395456   1.779541    -0.638542     0.638542     1.000000
110      0.371759   0.743300   1.883838    +0.371541     0.371541     1.000000
                              scostamento massimo da 1.0:  2.92e-05
```

> **SATURO IN TUTTI E UNDICI I CAMPIONI, IN ENTRAMBE LE DIREZIONI.**
> **`coesione_relazionale` decide solo il SEGNO. L'AMPIEZZA e' interamente il CLIP.**

### 4.1 E il clip e' proporzionale a `d0` STESSO — **il meccanismo della fuga**

```
tasso = tanh(stress) * d0        con    stress = |d - d0| / d0
```
**Quando `d0` cala, `stress` CRESCE, `tanh(stress) -> 1`, e il passo consentito tende a `d0`
stesso: il 100 % del valore, in UN passo.**

| `d0` | `d` | `stress` | `tanh` | passo consentito |
|---|---|---|---|---|
| 1.0008 | 1.2368 | 0.236 | 0.232 | **23 %** di `d0` |
| 1.0340 | 1.7795 | 0.721 | 0.617 | **62 %** di `d0` |
| 0.5060 | 1.5072 | 1.979 | 0.963 | **96 %** di `d0` |

> **Il limite che dovrebbe frenare la variazione CRESCE insieme alla variazione che deve frenare.**
> **E' un'oscillazione ad ampiezza relativa crescente, e non e' un'instabilita' dell'integratore:
> e' un LIMITE mal scalato.**
> **E' la famiglia dei PUNTI FISSI gia' trovata quattro volte** *(`scala_p`, `median(|f|)` in
> `ritmo()`, `_dens_rif` in `_tau`, `u_nodo`)* **— qui col segno peggiore: non azzera una misura,
> la fa DIVERGERE.**

---

## 5. COSA CADE, E COSA RESTA

| | |
|---|---|
| **la mitosi** | gia' refutata per DIMOSTRAZIONE (`Z78`); **la traccia lo conferma: `S06_mitosi` non tocca `d0` degli archi vivi (somma `0`, solo cambi di lunghezza)** |
| **`t_visco` instabile** | gia' refutata per MISURA; **e `S02_rilass_visco` qui spinge IN SU (`+2128`), non in giu'** |
| **i pavimenti** | **REFUTATI per misura: `+1.06` contro `-3684`** |
| **la «competizione»** *(mia lettura del riassunto)* | **vera sulla POPOLAZIONE, FALSA sull'arco**: li' e' un colpevole solo |
| **il colpevole** | **`:4877`, e piu' precisamente il suo CLIP `tanh(stress)*d0`** |

---

## 6. COSA QUESTO REFERTO **NON** DICE

- **NON dice che il clip sia sbagliato.** Dice che **satura sempre** e che **scala con la grandezza
  che limita**. **Se sia un difetto o una scelta e' una decisione di FISICA**, e non la prendo;
- **NON dice perche' `coesione_relazionale` ecceda sempre il clip.** Il termine fisico non e'
  tracciato: si vede solo che viene tagliato. **Tracciarlo e' un giro a parte;**
- **NON spiega la SECONDA FASE del ramo B** *(`n1` che sostituisce `n3`, `nsub = 15594`)*: al passo
  120 non era cominciata;
- **UN SEME, UN ARCO, 120 passi.** L'arco `16-481` e' stato scelto perche' e' il peggiore del
  sistema al passo 240: **e' un caso ESTREMO, non un campione.**
