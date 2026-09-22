# `A1` — IL TAGLIO A `+-pi` IN `ritmo()`: **la misura, PRIMA della correzione**

> Generato da `csv/_test_fork/_ritmo_taglio.py`. **Il simulatore NON e' toccato:**
> `ritmo()` e' avvolto e il valore restituito **non viene modificato**.
> 20 frame (= 120 passi), 339.2 s, 119 chiamate utili su 119.

## (1) FREQUENZA — quante volte si attraversa il taglio

| | valore |
|---|--:|
| chiamate misurate | 119 |
| **frazione di nodi con `|a| > pi`**, media | **4.4536e-05** |
| la stessa, massimo | 1.1355e-03 |
| chiamate con **almeno un** attraversamento | 12 su 119 |
| nodi tagliati per chiamata, media | 0.12 |
| nodi tagliati per chiamata, massimo | 3 |

## (2) ARRICCHIMENTO AL TETTO

> Sotto **ipotesi nulla** `f_a|tetto = f_a`. Il difetto **SPIEGA** il tetto se
> `f_a|tetto >= 5 * f_a` **e** `f_a|tetto >= 0.5`.

| | valore |
|---|--:|
| quota di nodi al TETTO (`r > 1.4142`), media | 8.6649e-04 |
| quota di nodi al PAVIMENTO (`r < 1e-5`), media | 2.7328e-04 |
| `f_a` medio *(il nullo)* | **4.4536e-05** |
| **`f_a|tetto` medio** | **3.2464e-02** |
| **arricchimento** | **728.94 x** |

**ESITO DEL CRITERIO (2): **contribuisce, NON spiega**.**

## (3) EFFETTO SUL GAUGE `median(|f|)`

| | valore |
|---|--:|
| `median(|f|)` col wrap **4pi** *(quello in vigore)*, mediana | 3.321471e-02 |
| `median(|f|)` col wrap **2pi** *(quello giusto)*, mediana | 3.321471e-02 |
| **rapporto `4pi / 2pi`**, mediana | **1.000000** |
| lo stesso, massimo | 1.000000 |

⚠ **LIMITE DICHIARATO PRIMA:** il ramo `2pi` e' calcolato **sui valori del ramo `4pi`**, cioe' su una traiettoria prodotta dal difetto. **Dice cosa sarebbe successo IN QUEL PASSO, non cosa succede in un run corretto.**

## E `r` NON HA UN CLIP A `1e6`

Dal codice (`:2643-2645`): `r = x/sqrt(1+x^2) + 1e-6`, poi `/(1/sqrt(2) + 1e-6)`.
**Tetto `~1.4142`, pavimento `~1.4142e-6`: il rapporto `max/min = 1e+06` e' `1/1e-6` PER COSTRUZIONE.**

| | misurato |
|---|--:|
| `min(r)` sul run | 1.414212e-06 |
| `max(r)` sul run | 1.414213e+00 |

**LIMITI: UN seme, UNA scena, 120 passi.**
