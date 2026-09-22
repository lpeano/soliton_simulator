# `D27` e `D25` — LE COMPONENTI e IL TEMPO, **senza nessun run**

> **SOLA LETTURA** su snapshot gia' scritti: `i`, `j` e `_r_corrente` ci sono gia'.
> Generato da `csv/_test_fork/_componenti_e_tempo.py`. **Nessuna cura, nessuna fisica.**

## G1/G3 riferimento (`_val600`)

| passo | comp. | la piu' grande: nodi / archi | le altre | masse in comp. diverse? |
|--:|--:|---|---|---|
| 120 | **1** | 2647 / 526282 | — | no, tutte in `0` |
| 240 | **1** | 2694 / 526336 | — | no, tutte in `0` |
| 360 | **1** | 2761 / 526418 | — | no, tutte in `0` |
| 480 | **1** | 2836 / 526512 | — | no, tutte in `0` |
| 600 | **1** | 2959 / 526672 | — | no, tutte in `0` |

**All'ultimo snapshot (passo 600): `med d0` e `med d` PER COMPONENTE**, e la composizione per regione.

| comp. | nodi | archi | vuoto | massa | nato | `med d0` | `med d` | `med d/d0` |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 0 | 2959 | 526672 | 900 | 1491 | 568 | `3.3180` | `1.8823` | `0.7489` |

## G3 senza gravita' (`_g3_senza_bifase`)

| passo | comp. | la piu' grande: nodi / archi | le altre | masse in comp. diverse? |
|--:|--:|---|---|---|
| 120 | **1** | 2617 / 526246 | — | no, tutte in `0` |
| 240 | **1** | 2659 / 526300 | — | no, tutte in `0` |
| 360 | **1** | 2723 / 526376 | — | no, tutte in `0` |
| 480 | **1** | 2816 / 526491 | — | no, tutte in `0` |
| 600 | **1** | 3057 / 526784 | — | no, tutte in `0` |

**All'ultimo snapshot (passo 600): `med d0` e `med d` PER COMPONENTE**, e la composizione per regione.

| comp. | nodi | archi | vuoto | massa | nato | `med d0` | `med d` | `med d/d0` |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 0 | 3057 | 526784 | 900 | 1491 | 666 | `3.5951` | `1.9443` | `0.6258` |

## G4 riferimento (`_g4_riferimento`)

| passo | comp. | la piu' grande: nodi / archi | le altre | masse in comp. diverse? |
|--:|--:|---|---|---|
| 120 | **1** | 2647 / 526282 | — | no, tutte in `0` |
| 240 | **1** | 2694 / 526336 | — | no, tutte in `0` |

**All'ultimo snapshot (passo 240): `med d0` e `med d` PER COMPONENTE**, e la composizione per regione.

| comp. | nodi | archi | vuoto | massa | nato | `med d0` | `med d` | `med d/d0` |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 0 | 2694 | 526336 | 900 | 1491 | 303 | `1.7450` | `1.3632` | `0.7875` |

## G4 senza memoria del moto (`_g4_senza_memmoto`)

*(nessuno snapshot: l'archivio non c'e' ancora)*

## `D25` — IL TEMPO CHE NON SCORRE: la distribuzione di `_r_corrente`

> `dt_n = DT * r` e' **il tic dei processi locali** *(`CLAUDE.md` par.9)*. Un nodo con `r`
> trascurabile **non integra**: le leggi che vivono in `dt_n` non lo toccano.
> **Il confronto e' col nodo MEDIANO, non con una soglia scelta.**

| archivio | passo | nodi | `med r` | `r/med` < 0.01 | < 0.1 | quota del tempo nei fermi |
|---|--:|--:|--:|--:|--:|--:|
| G1/G3 riferimento (`_val600`) | 600 | 2952 | `1.4088e+00` | `0.0003` | `0.0041` | `0.000193` |
| G3 senza gravita' (`_g3_senza_bifase`) | 600 | 3055 | `3.7003e-01` | `0.0062` | `0.0576` | `0.001935` |
| G4 riferimento (`_g4_riferimento`) | 240 | 2694 | `5.9397e-01` | `0.0085` | `0.0694` | `0.002737` |

## ⚠ COSA LA MISURA HA DETTO, **prima** delle domande

**Le due premesse vanno verificate PRIMA di trarne conseguenze** *(par.9-bis: ogni
numero porta la sua epoca)*. Le tabelle qui sopra dicono **quante componenti** e **quanti
nodi fermi** ci sono DAVVERO negli archivi di QUESTA epoca. **Dove il numero di componenti
e' `1`, la premessa di `D27` NON REGGE**, e le domande `1` e `2` restano aperte **solo per
gli archivi in cui piu' componenti ci sono davvero.**

## ⚠ LE CONSEGUENZE SULLE TRE PROVE: **DOMANDE, non risposte**

1. **Se il grafo e' in piu' componenti, che cosa significa «distanza fra due masse»
   nella PROVA 1?** Un cammino minimo fra componenti diverse **non esiste**. Si misura
   dentro una componente? Si dichiara infinita? **La domanda non ha oggi una risposta.**
2. **La PROVA 2 chiede la pendenza contro la distanza.** Se le separazioni appartengono a
   componenti diverse, **su quale asse si mette il punto?**
3. **Se il `93 %` dei nodi non integra**, la PROVA 3 *(tutti i corpi cadono uguale)*
   **sta confrontando corpi che evolvono, o corpi fermi?**

**Nessuna di queste e' una cura, e nessuna e' una risposta.** Vanno al `CHK3`.
