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
