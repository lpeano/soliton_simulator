# PREDIZIONE — SHAKE-THEN-FREEZE: qual e' l'attrattore della sola precessione?

> **Scritta e committata PRIMA dei run.** Branch `fork-su2`. Data: 2026-09-14.
> Domanda di Luca: *"potrebbe servire un periodo di scuotimento caotico prima del test?"*

## 0. PERCHE' — e perche' NON e' il ricottura

**Nella lettura "ricottura": NO, dimostrato.** Il ricottura funziona quando un accoppiamento
ordinante `J` compete con un rumore `T`. Qui **`J = 0`** (FDT: `E[n'] - n = -a^2 n`, senza `{n_k}`),
e la diffusione sulla sfera ha **una sola distribuzione stazionaria, l'uniforme**.

**MA la domanda apre un esperimento mai fatto.** Il braccio OFF si e' congelato al polo **solo
perche' PARTIVA dal polo** (`:1778`), che e' lo stato **piu' degenere possibile** e un punto fisso
esatto per simmetria. Scuotere **e poi smettere** congela una configurazione **casuale**, che **non
e' nel punto fisso**. E il FDT ha mostrato che **la precessione mutua ha una dinamica propria**.

> **LA DOMANDA: qual e' l'ATTRATTORE della sola precessione, da una configurazione CASUALE?**
> Mai misurato nel sistema. Solo su **due nodi isolati**.

**Non e' una manopola (par.3):** cambiare la **condizione iniziale** non e' tarare un **parametro
della dinamica**, e quella attuale e' gia' una scelta arbitraria del codice — la piu' speciale che
esista. Partire da Bloch casuali e' **meno** particolare, non di piu'.

## 1. IL PROTOCOLLO — costo zero di codice sul simulatore

- **Fase 1 (SHAKE):** config certificata, scuotimento ON, 300 passi -> i Bloch diventano casuali.
  `--sync-db` salva lo stato.
- **Fase 2 (FREEZE):** **resume dallo STESSO DB** con `--regime deterministico`, che spegne **solo**
  `SCUOTIMENTO` (sigillato O2). Altri 600 passi.

**Verificato dal sorgente:** la guardia del DB confronta **solo il git blob dei byte del codice**,
**non i flag**. Stesso `.py`, flag diversi -> resume **accettato**.

**Caveat dichiarato:** il blob sul disco e' `c0803713` (STEP 2 cablato, **non sigillato**). Il flag
Step 2 e' **OFF**, e **S1 ha provato che a flag spento e' byte-identico a `2277e9a0`**. L'esperimento
gira quindi su un blob non certificato, **con quella prova a sostegno**. Scritto, non taciuto.

## 2. IL PRIOR QUANTITATIVO (misurato, non scommesso)

Il test FDT 3b dipendeva forte da `|B|`. **Misurato nel sistema reale** (braccio ON, 3536 nodi):

| | |
|---|---|
| grado **mediana** | **2** (la *media* e' 119: distribuzione estremamente asimmetrica) |
| `n_eff = (sum w)^2 / sum w^2`, mediana | **1.99** |
| **`\|B\|` mediana** | **0.5299** (media 0.478, p90 0.916) |
| `1/sqrt(n_eff)` | 0.709 — **torna** |

> **Il sistema reale sta nella regione `|B| ~ 0.5`** del test FDT 3b — quella della **DERIVA LENTA**
> (60 -> 62.5 gradi in 2000 passi). Il punto fisso anti-allineante richiedeva `|B| ~ 10`, **venti
> volte tanto**.

*(Nota: "grado medio 119" era la MEDIA e mi aveva ingannato; la mediana e' 2. La media da sola
inganna quando la distribuzione e' asimmetrica — errore fatto e corretto sul posto.)*

## 3. I TRE ESITI (definiti prima)

| | chi nel tempo (fase 2) | autocorrelazione | lettura |
|---|---|---|---|
| **A — STRUTTURA** | si sposta a un valore **intermedio** stabile | **decade a scala finita** | domini dalla sola precessione |
| **B — CONGELATO** | resta ~90 gradi | resta ~0 | la configurazione casuale e' (quasi) stazionaria |
| **C — ANTI-ALLINEAMENTO** | **sale** sopra 90 verso 180 | ~0 o negativa | la precessione spinge verso l'antipodale |

> **DICHIARAZIONE: "struttura" SOLO nell'esito A, e solo con `|<n>|` che NON va a 1** — un chi
> intermedio col sistema tutto allineato sarebbe collasso, non domini (lezione Kuramoto).

**PREDIZIONE, dal prior del §2:** **esito B con una lenta deriva verso C**. Con `|B| ~ 0.53` il test
a due nodi dava `+2.5 gradi in 2000 passi`; in 600 passi ci si aspetta **una frazione di grado**.
Quindi: chi ~90 gradi, praticamente fermo. **Se invece si muovesse molto, il prior a due nodi non
descrive il sistema a molti corpi** — e quello sarebbe il reperto.

## 4. COSA QUESTO NON DIRA'

Non dira' che la struttura c'e' o non c'e' **in generale**: dira' cosa fa **la sola precessione** da
uno stato casuale, su 600 passi e un seme (par.2.7). Non tocca il codice del simulatore. Non accende
altro. E se l'esito e' B, **e' il quinto lato dello stesso fatto**, non una sorpresa.

**Limite del prior:** viene da un test a **due nodi** applicato a un sistema a molti corpi con
`n_eff ~ 2`. E' plausibile ma **non dimostrato** che si trasferisca: e' un prior, non una predizione
derivata.


---

# 5. ESITO — aggiunto il 2026-09-14 DOPO i run

> Tutto sopra e' stato scritto e committato (`d0f3de6`) **prima**. Qui solo il risultato.

## 5.1 — Il protocollo ha funzionato

```
[osserva] RESUME da csv/_test_fork/_stf_seed.pkl
[db] resume: 300 passi gia' fatti, ne mancano 600 per arrivare a 900
[osserva-flag] tag=stf_freeze  FORK_SU2=True FORK_SU2_MEM=True SCUOTIMENTO=False
```

Resume accettato con flag diversi, come previsto dalla lettura del sorgente. **Zero modifiche al
simulatore.**

## 5.2 — La premessa e' confermata: NON si congela piu' al polo

Il braccio OFF precedente si congelava a `|<n>| = 1.000000` su `(0,0,+1)`. **Qui no:** partendo da
una configurazione casuale, `|<n>|` resta **~1/sqrt(N)** per tutti i 600 passi. Quindi il
congelamento di prima **era** la condizione iniziale speciale, non una proprieta' della dinamica.

## 5.3 — FASE 2 (600 passi, scuotimento OFF, da stato casuale)

| passo | n | chi materia | \|⟨n⟩\| / (1/sqrt N) |
|---|---|---|---|
| 50 | 3611 | 90.13 +- 39.23 | 0.96 |
| 150 | 3779 | 90.06 +- 39.20 | 0.58 |
| 300 | 4026 | 89.96 +- 39.21 | 1.20 |
| 450 | 4337 | 90.03 +- 39.16 | 1.60 |
| **600** | **4679** | **89.80 +- 39.30** | **1.27** |

*(riferimento casuale: 90.000 +- 39.171)*

**Deriva di chi su 600 passi: 90.13 -> 89.80 = `-0.33 gradi`.** Il sistema resta
**indistinguibile dal casuale** per tutta la fase.

**Autocorrelazione a fine fase 2:** `+0.0050` da vicino (d~0.39) a `+0.0014` da lontano (d~14.1),
**piatta a zero su tutte e 14 le distanze**. Nessuna scala di dominio.

`|n_ret| - 1 = 2.22e-16` a ogni campione. N cresce 3611 -> 4679: **il sistema non e' fermo**,
evolve e fa mitosi. Solo, **non organizza i Bloch**.

## 5.4 — VERDETTO: **ESITO B**, e la predizione quantitativa ha retto

| | predetto (par.3) | misurato |
|---|---|---|
| esito | **B (congelato)**, deriva di **una frazione di grado** | **B**, deriva **-0.33 gradi** |
| `\|<n>\|` | non -> 1 | resta ~1/sqrt(N) |
| autocorrelazione | ~0 | piatta a zero |

**Il prior a due nodi si e' trasferito al sistema a molti corpi.** Il segno e' diverso da quello del
test FDT (`+2.5` in 2000 passi li', `-0.33` in 600 qui), ma la deriva e' **dentro la dispersione dei
campioni** (`|<n>|` oscilla fra 0.38 e 1.60 in unita' del casuale): **non e' una deriva
significativa, e' rumore statistico attorno a 90**.

> **La configurazione casuale e' (quasi) stazionaria sotto la sola precessione.**
> Ne' ordine ne' anti-ordine: resta casuale.

## 5.5 — Il quinto lato dello stesso fatto

Era scritto prima che, se l'esito fosse B, sarebbe stato **il quinto lato**, non una sorpresa. Lo e':

1. teorema di inerzia (la connessione e' uno specchio);
2. frozen-o-noise (cio' che specchia e' rumore);
3. Kuramoto refutato (l'allineamento locale aggiunto non basta);
4. FDT (nel rumore non c'e' dissipazione compagna — **dimostrato**);
5. **shake-then-freeze (da uno stato casuale, la sola precessione non organizza).**

Il 5 chiude l'ultima scappatoia: *"forse era solo la condizione iniziale degenere"*. **Non lo era.**
Il polo era davvero un punto fisso speciale, ma toglierlo **non rivela struttura sotto**: rivela che
non c'e' struttura.

## 5.6 — Cosa questo NON dice

600 passi, **un seme**, un solo punto di partenza casuale (par.2.7). Nulla su olonomia, `W(r)` o
gravita'. E non dice che la struttura non possa esistere **in generale**: dice che **le cinque vie
provate non la producono**, e che la sesta — se c'e' — non e' nessuna di queste.
