# MARE `v2` — **LO STATO DI PARTENZA CHE IL MANDATO CHIEDE NON ESISTE COME STATO PIÙ BASSO, E IL CONTO LO DICE**

*Referto generato da `proto_primo_ordine/diagnosi_v2.py`. Criteri e previsioni: `doc/TASK_HISTORY/2026-10-08_proto-mare-v2.md`, committato ### **prima** in `9baf4a1`.*

> ### ⛔ **Simulatore `b8c21049`, `ASSIOMI.md` non toccato, e il prototipo NON importa il simulatore.** ### **Solo `U = I`**, come il mandato chiede.

> ### ⚠ **E LA `H` DI QUESTO BANCO È UNA SONDA MINIMA SCELTA DAL GUARDIANO** *(precisazione di Luca, 2026-10-08)*: `hopping + (g/2)|ψ|⁴` è una ### **forma DA MANUALE** *(Schrödinger non lineare discreta)*, ### **NON una decisione di Luca e NON una traduzione delle sue leggi** — quella è il lavoro di `doc/TRADUZIONE_IN_H.md`. ### ⛔ **E il GRAFO FISSO è un'IMPALCATURA DEL TEST, non il modello di Luca:** nello spazio di Luca nodi e archi ### **nascono** *(`doc/RISCRITTURA_PRIMO_ORDINE.md` §⑤)*.

---

# ⛔ `①` **L'ESITO: `LO STATO PIÙ BASSO È GIÀ UNA MASSA`, E SCATTA SUBITO SOTTO `g = 0`**

Il mandato prevede questo esito *(«se il ramo esteso finisce prima di `g = -10`: riportalo come esito a sé, con il `g` in cui finisce»)*. ### ➜ **Finisce prima di quanto l'esito previsto lasciasse immaginare: NON c'è nessun `g < 0` in cui lo stato più basso sia esteso.**

| | |
|---|---|
| il conto | a norma totale fissa `Σψ² = N`, lo stato su ### **un solo nodo** ha `ρ = N` e quindi `H = (g/2)·N²`; lo stato ### **esteso** ha `H ≈ −λ_max·N + (g/2)·N²/n_eff` |
| ### ➜ **perché vince sempre** | ### **`(g/2)N²` va come `N²`, l'esteso come `N`.** Con `N = n = 400` il primo è più basso del secondo di ### **ordini di grandezza**, per ### **ogni** `g < 0` |

| braccio | `g` | `H` su ### **un nodo** | `H` ### **esteso** | ### **vince** |
|---|--:|--:|--:|---|
| `NON-NORM` | `-5.0` | ### **-400000.0** | -18533.8 | ### **UN NODO** |
| `NON-NORM` | `-10.0` | ### **-800000.0** | -34807.9 | ### **UN NODO** |
| `NORM` | `-5.0` | ### **-400000.0** | -1548.7 | ### **UN NODO** |
| `NORM` | `-10.0` | ### **-800000.0** | -2697.4 | ### **UN NODO** |

> ### ✔ **E LA MISURA LO CONFERMA, non solo il conto:** la continuazione dal Perron, con la discesa a tempo immaginario, collassa a ### **`PR = 1.00`** *(tutta la norma su `UN` nodo, `max/media = 400`)* già al ### **primo** passo sotto `g = 0`, in ### **entrambi** i bracci e per ### **entrambi** i passi di continuazione provati.

| braccio | seme | `PR` lungo il ramo, dal Perron in giu' | ### **dove Newton si ferma** |
|---|--:|---|--:|
| `NON-NORM` | `11` | ### **24.6** → 1.0 → 1.0 → 1.0 → 1.0 → 1.0 | non si ferma *(ma e' gia' su UN nodo)* |
| `NON-NORM` | `12` | ### **18.1** → 1.0 → 1.0 → 1.0 → 1.0 → 1.0 | non si ferma *(ma e' gia' su UN nodo)* |
| `NON-NORM` | `13` | ### **19.8** → 1.0 → 1.0 → 1.0 → 1.0 → 1.0 | non si ferma *(ma e' gia' su UN nodo)* |
| `NORM` | `11` | ### **348.2** → 1.0 → 1.0 → 1.0 → 1.0 → 1.0 | ### **`g = -2.25`** |
| `NORM` | `12` | ### **351.1** → 1.0 → 1.0 → 1.0 → 1.0 → 1.0 | ### **`g = -2.50`** |
| `NORM` | `13` | ### **348.4** → 1.0 → 1.0 → 1.0 → 1.0 → 1.0 | ### **`g = -1.75`** |

> ### ⚠ **E NEL BRACCIO `NORM` NEWTON SI FERMA ANCHE LUI**, fra `g = -1.75` e `g = -2.50` ### **dopo** essere gia' collassato: non e' «il ramo esteso che finisce», e' ### **il ramo di UN NODO che smette di convergere.** ### ⛔ **Leggere quel `g` come «il ramo esteso finisce qui» sarebbe un FALSO-UNO**, e lo dico perche' il criterio del mandato chiede proprio quel numero.

# ⛔ `②` **E NON ESISTE UN `ρ_0` CHE SALVI IL MARE: LE DUE CONDIZIONI SI ESCLUDONO**

Lo stato su un nodo vince se `N > 2·λ_max / (|g|·(1 − 1/n_eff))`. ### ➜ **Sotto quella soglia il mare sopravvive come stato più basso — ma a quella densità la non linearità è TRASCURABILE:**

| braccio | `g` | ### **`ρ_0` di soglia** | la non linearità lì: `\|g\|·ρ_0` | contro `λ_max` |
|---|--:|--:|--:|--:|
| `NON-NORM` | `-5.0` | ### **0.005889** | ### **0.02944** | `5.6494` |
| `NON-NORM` | `-10.0` | ### **0.002944** | ### **0.02944** | `5.6494` |
| `NORM` | `-5.0` | ### **0.001003** | ### **0.00501** | `1.0000` |
| `NORM` | `-10.0` | ### **0.000501** | ### **0.00501** | `1.0000` |

> ### ⛔ **QUINDI: «il mare è lo stato più basso» e «la non linearità conta» NON possono valere insieme in QUESTA `H`.** ### **Non è un difetto del metodo né una scelta sbagliata di `ρ_0`: è una proprietà della forma di `H`**, e vale per ### **ogni** `ρ_0`.

> ### ⚠ **E IL RAMO ESTESO ESISTE ANCORA — come SELLA, non come minimo.** Seguirlo serve un metodo che ### **non scenda**; una discesa ci cade fuori ### **per costruzione**, e infatti ci cade. ### ➜ **Un esperimento sul ramo esteso misurerebbe «una sella instabile decade», che NON è «l'interferenza fa nascere le masse».**

# ⭐ `③` **CHE COSA SI È MISURATO LUNGO LA STRADA**

| | `NON-NORM` | `NORM` |
|---|--:|--:|
| `λ_max` | 5.6494 | 1.0000 |
| ### **`PR` dell'autovettore di Perron** *(a `g = 0`)* | ### **24.58** | ### **348.22** |
| ### **`max/media` del Perron** | ### **29.38** | ### **2.25** |
| `s_k` ### **del braccio**: media | 3.4841 | ### **0.9828** |
| `s_k` ### **del braccio**: deviazione relativa | 0.3856 | ### **0.1160** |
| `s_k`: `max/min` | 16.66 | ### **2.82** |

> ### ⭐ **IL NUMERO CHE VALE È IL `PR` DEL PERRON A `g = 0`:** nel braccio ### **`NON-NORM`** lo stato più basso ### **LINEARE** è già concentrato su ### **24.6** nodi su `400` *(`max/media` = 29.38)*. ### ➜ **La geometria da sola, senza nessuna non linearità, concentra quasi tutto.** Nel braccio ### **`NORM`** il `PR` è ### **348.2**: la normalizzazione ### **toglie quasi tutta** quella concentrazione.

> ### ⚠ **E LA NORMALIZZAZIONE TOCCA `A3`, con la precisione che serve:** `s_k` è una ### **SOMMA** sul proprio intorno, non una mediana né una media, quindi il meccanismo che `A3` nomina — *«il centro diventa `1` per identità»* — ### **non scatta**: dopo la normalizzazione `s̃_k` ha deviazione relativa ### **0.1160** contro `0.3856` di prima, e `max/min` ### **2.82** contro `16.66` -- ### **CALA, ma NON va a `1` per identita'**, e la media resta ### **0.9828**, non `1`. ### ⛔ **La scelta fra le due forme resta una DECISIONE DI LUCA.**

# ⛔ `④` **TRE METODI PROVATI, E I PRIMI DUE ERANO SBAGLIATI — MISURATO, NON ARGOMENTATO**

| metodo | che cosa ha fatto | come l'ho saputo |
|---|---|---|
| Newton ### **pieno** | ### ⛔ **SALTAVA**: `PR = 2.0` con `Δg = -0.25`, `1.0` con `-0.05` | ### **rifacendo la continuazione con un `Δg` più fine**: un risultato che dipende dal passo ### **non sta sul ramo** |
| Newton ### **smorzato** | non saltava più, ma ### **non convergeva** *(si fermava al primo `g`)* | il residuo restava sopra la soglia |
| ### **discesa a tempo immaginario + Newton** | ### **coerente fra i passi**, e collassa a `PR = 1` | i due `Δg` danno ### **lo stesso** risultato |

> ### ⚠ **E UN DIFETTO MIO NEL CRITERIO, che era `A3c`:** misuravo il residuo del vincolo `\|Σψ² − n\|` in ### **assoluto** contro `1e-12`, ma quella somma vale `400` e la precisione macchina su `400` termini è già `~1e-12`. ### **Un `1.82e-12` assoluto è `4.5e-15` relativo, cioè ZERO** — e il ramo «finiva» per un confronto fra grandezze ### **non commensurabili**. ### **Ora il residuo è relativo.**

---

# ⛔ **CHE COSA QUESTO REFERTO NON DICE**

| | |
|---|---|
| che l'interferenza ### **non** faccia nascere le masse | ### ⛔ **NO.** Dice che ### **in questa `H`, a norma fissa, non esiste un mare da cui farle nascere**: lo stato più basso è già una massa |
| i ### **criteri** del mandato | ### **non sono stati valutati**: l'esperimento richiede uno stato di partenza ### **fermo ed esteso**, e quello ### **non esiste** |
| che la colpa sia di ### **`ρ_0`** | ### ⛔ **no, ed è misurato:** per ogni `ρ_0` che salva il mare la non linearità scende a `~1e-2`, cioè ### **sparisce** |
| che cosa fare | ### ⛔ **è una DECISIONE DI LUCA.** Le strade che il conto lascia aperte: una `H` con un termine che ### **penalizzi** la concentrazione *(un `ρ²` repulsivo, o un vincolo locale)*; oppure studiare il ramo esteso ### **come sella**, dichiarando che si misura un decadimento; oppure un `g` ### **positivo** |
| l'esperimento del ### **pacchetto** | ### ⛔ **non girato**, come nel `v1` |

