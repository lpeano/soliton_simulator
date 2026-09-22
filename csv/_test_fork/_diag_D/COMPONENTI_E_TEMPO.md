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
| 360 | **1** | 2761 / 526418 | — | no, tutte in `0` |
| 480 | **1** | 2836 / 526512 | — | no, tutte in `0` |
| 600 | **1** | 2959 / 526672 | — | no, tutte in `0` |

**All'ultimo snapshot (passo 600): `med d0` e `med d` PER COMPONENTE**, e la composizione per regione.

| comp. | nodi | archi | vuoto | massa | nato | `med d0` | `med d` | `med d/d0` |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 0 | 2959 | 526672 | 900 | 1491 | 568 | `3.3180` | `1.8823` | `0.7489` |

## G4 senza memoria del moto (`_g4_senza_memmoto`)

| passo | comp. | la piu' grande: nodi / archi | le altre | masse in comp. diverse? |
|--:|--:|---|---|---|
| 120 | **1** | 2670 / 526318 | — | no, tutte in `0` |
| 240 | **1** | 2703 / 526357 | — | no, tutte in `0` |
| 360 | **1** | 2737 / 526398 | — | no, tutte in `0` |
| 480 | **1** | 2799 / 526476 | — | no, tutte in `0` |
| 600 | **1** | 2914 / 526619 | — | no, tutte in `0` |

**All'ultimo snapshot (passo 600): `med d0` e `med d` PER COMPONENTE**, e la composizione per regione.

| comp. | nodi | archi | vuoto | massa | nato | `med d0` | `med d` | `med d/d0` |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 0 | 2914 | 526619 | 900 | 1491 | 523 | `2.2559` | `1.6382` | `0.8546` |

## `D25` — IL TEMPO CHE NON SCORRE: `_r_corrente` contro il riferimento ESTERNO `r = 1`

> `dt_n = DT * r` e' **il tic dei processi locali** *(`CLAUDE.md` par.9)*. Un nodo con `r`
> trascurabile **non integra**: le leggi che vivono in `dt_n` non lo toccano.
>
> **⚠ IL RIFERIMENTO E' `r = 1`, ED E' ESTERNO ALLA DISTRIBUZIONE.** `r = 1` e' il nodo il
> cui tempo proprio vale **il tempo di coordinata `DT`**: non e' una soglia scelta, e'
> **l'unita' della grandezza stessa**.
>
> **⚠ PERCHE' NON LA MEDIANA, e l'errore era mio:** se i fermi sono la MAGGIORANZA, **la
> mediana e' essa stessa un nodo fermo**, e `r/med` non vede niente — i fermi sembrano
> normali e quelli che scorrono sembrano anomalie. **Il criterio sarebbe cieco proprio sul
> caso che deve misurare** *(`CLAUDE.md` `P4`, `C12`; reperto in `944064a`)*.

| archivio | passo | nodi | `med r` | `r < 0.01` | `r < 0.1` | quota del tempo nei fermi |
|---|--:|--:|--:|--:|--:|--:|
| G1/G3 riferimento (`_val600`) | 600 | 2952 | `1.4088e+00` | `0.0000` | `0.0030` | `0.000108` |
| G3 senza gravita' (`_g3_senza_bifase`) | 600 | 3055 | `3.7003e-01` | `0.0160` | `0.1869` | `0.018276` |
| G4 riferimento (`_g4_riferimento`) | 600 | 2952 | `1.4088e+00` | `0.0000` | `0.0030` | `0.000108` |
| G4 senza memoria del moto (`_g4_senza_memmoto`) | 600 | 2913 | `1.1094e+00` | `0.0031` | `0.0498` | `0.002774` |

### Le MASSE: lette dalla semina, **non supposte**

> Chiesto da Luca: *«quante sono e quali nodi appartengono a ciascuna, dal codice che
> semina la scena»*. **Non si puo', e lo dichiaro invece di aggirarlo.**

- **G1/G3 riferimento (`_val600`)**: `masse_info` ha **0** voci · `conc_nodi` ha **0** nodi con una coorte su 2959.
- **G3 senza gravita' (`_g3_senza_bifase`)**: `masse_info` ha **0** voci · `conc_nodi` ha **0** nodi con una coorte su 3057.
- **G4 riferimento (`_g4_riferimento`)**: `masse_info` ha **0** voci · `conc_nodi` ha **0** nodi con una coorte su 2959.
- **G4 senza memoria del moto (`_g4_senza_memmoto`)**: `masse_info` ha **0** voci · `conc_nodi` ha **0** nodi con una coorte su 2914.

**LA CAUSA, dal sorgente (`:6209`):** `_massa` chiama
`net.semina(n, raggio=r, centro=centro, fase=fase)` **SENZA `mass_id`**, quindi
`masse_info` **non viene mai popolato** e `_registra_concorrenza` **non parte**. La coorte
finisce in `test["dati"]`, un dizionario **di modulo** che **non sta nello snapshot**.
**→ difetto `D30`.**

> **✅ MA LA DOMANDA «le tre masse stanno in componenti diverse?» HA COMUNQUE
> RISPOSTA, e non dipende da nessuna assunzione:** poiche' **la componente e' UNA SOLA**,
> **qualunque** partizione dei nodi finisce dentro quella. **La risposta e' NO.**

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
3. **IL `93 %` NON REGGE SU QUESTI ARCHIVI, e lo dice la tabella qui sopra:** i nodi
   con `r < 0.1` sono fra lo **`0.30 %`** e il **`18.69 %`**, e la QUOTA DI TEMPO che
   sta nei fermi e' fra lo **`0.01 %`** e l'**`1.83 %`**. **La premessa di `D25` cade
   qui come quella di `D27`.** Resta la domanda, ma con un numero diverso: **una quota
   di tempo cosi' piccola basta a falsare la PROVA 3** *(tutti i corpi cadono uguale)*,
   **o e' trascurabile?** **Non e' deciso, e non lo decide questa misura.**

**Nessuna di queste e' una cura, e nessuna e' una risposta.** Vanno al `CHK3`.
