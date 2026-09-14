# PREDIZIONE — Kuramoto SU(2) produce DOMINI, o e' il collasso rinominato?

> **Scritta e committata PRIMA di girare i run**, perche' l'esito non sia razionalizzabile a
> posteriori. Branch `fork-su2`, blob **2277e9a0**. Data: 2026-09-14.
> Un solo meccanismo nuovo acceso: `--kuramoto-su2` (flag gia' esistente, nessuna modifica al `.py`).

---

## 0. DA DOVE SI PARTE (misurato, non assunto)

Test A/B chiuso (commit `a04ee3d`, 300 passi, seme 1, osservatore sigillato pure-read):

| | chi (materia / vuoto / p90) | \|⟨n⟩\| |
|---|---|---|
| scuotimento **ON** | 90.04 / 90.06 / 89.86 gradi | 0.007 – 0.025 (~1/sqrt(N)) |
| scuotimento **OFF** | **0.00 / 0.00 / 0.00** | **1.000000 esatto, su (0,0,+1)** |

Due soli stati, **entrambi senza struttura**: rumore bianco, o congelamento sulla condizione
iniziale. Il substrato non ha struttura di Bloch, quindi il fork trasporta **rumore** (ON) o
**identita'** (OFF).

**Ipotesi da testare:** `--kuramoto-su2` allinea lo spinore alla media SU(2) dei **vicini** — una
forza **locale**, non globale. Una forza di allineamento locale, in competizione con un rumore, e'
la ricetta classica dei **DOMINI**: regioni coerenti separate da bordi, ed e' proprio sui bordi che
`grad(n)` — cioe' cio' che l'olonomia richiede — sarebbe grande.

---

## 1. LA TRAPPOLA, E PERCHE' CAMBIA IL DISEGNO DELL'ESPERIMENTO

Il rischio dichiarato nel mandato: *"Kuramoto e' una forza di allineamento; OFF i Bloch sono GIA'
allineati; rischio che Kuramoto dia lo STESSO collasso globale con un nome nuovo."*

**Verificato dal codice, ed e' peggio (o meglio) di cosi'.** Il torque di Kuramoto e'
(`soliton_simulator.py:1988-1991`):

```python
_crx  = np.cross(nb[:n], _nb_bar)          # nb x nb_bar
_sink = np.linalg.norm(_crx, axis=1)
_amp  = np.arcsin(np.clip(_sink, 0.0, 1.0))
_Om   = (forza_sync * _amp)[:, None] * (_crx / max(_sink, 1e-12))
```

Se **tutti** gli `nb` sono identici — che e' esattamente lo stato del braccio OFF — allora
`nb_bar = nb`, quindi `_crx = 0`, `_sink = 0`, `_amp = 0`, `_Om = 0`: **nessuna rotazione.**

> **Lo stato allineato non e' solo un punto fisso della dinamica base: e' un punto fisso ANCHE per
> Kuramoto.** Una forza di allineamento non ha nulla da allineare quando tutto e' gia' allineato.

**Conseguenza sul disegno.** Il mandato consigliava il braccio K **senza** scuotimento, per isolare
l'allineamento locale dal rumore. Ma per l'algebra qui sopra quel braccio e' **gia' predetto
inerte**, e non testerebbe nulla: darebbe l'esito NO-collasso per una ragione banale (il sistema
non si e' mai mosso), non per una ragione fisica.

**Quindi si girano DUE bracci, e la scelta e' dichiarata qui prima del dato:**

- **K-frozen** = `--kuramoto-su2` + `--regime deterministico` (scuotimento OFF).
  **Predetto INERTE**, identico al braccio OFF gia' misurato (chi = 0.00, `|⟨n⟩| = 1.000000` su
  `(0,0,+1)`). Serve come **controprova dell'algebra**: se invece si muovesse, il mio ragionamento
  sul punto fisso e' sbagliato e va rifatto. E' una predizione falsificabile, non un riempitivo.
- **K-noise** = `--kuramoto-su2` + scuotimento ON (config certificata).
  **E' l'esperimento vero.** Il rumore fornisce le perturbazioni, Kuramoto le organizza o non le
  organizza. La domanda fisica e': *l'allineamento locale vince sul rumore abbastanza da formare
  domini?*

E' vero che K-noise ha due meccanismi attivi — ma **non e' un A/B sporco**: il braccio di confronto
(scuotimento ON senza Kuramoto) e' **gia' misurato** (chi = 90 gradi, rumore puro), quindi
l'**unica variabile** fra i due e' Kuramoto. Un interruttore alla volta e' rispettato.

---

## 2. LE TRE FIRME, E I VALORI DI RIFERIMENTO (fissati PRIMA)

Ogni firma va letta contro i **due esiti-no**, non a occhio:

| firma | RUMORE (null) | COLLASSO globale | DOMINI (l'esito SI) |
|---|---|---|---|
| **chi** fra vicini | 90.000 gradi, std 39.171 | 0 gradi, std 0 | **intermedio**, ne' 0 ne' 90 |
| **\|⟨n⟩\| globale** | ~1/sqrt(N) | **~1** | **NON ~1** (i domini si cancellano fra loro) |
| **⟨n_i·n_j⟩ vs distanza** | ~0 a ogni distanza | **~1 a ogni distanza** | **parte alta e DECADE a scala finita** |

**La firma che smaschera il collasso e' `|⟨n⟩|` globale + l'autocorrelazione, NON chi da solo.**
Un chi basso e' compatibile sia coi domini sia col collasso: e' la **decorrelazione a distanza** a
distinguerli. Se `|⟨n⟩| -> 1`, c'e' **una direzione unica per tutto il sistema** = degenerazione,
qualunque cosa faccia chi.

---

## 3. I TRE ESITI, E LA DICHIARAZIONE DI FALSIFICABILITA'

- **SI (struttura):** chi **intermedio** + `|⟨n⟩|` **non** -> 1 + autocorrelazione che **decade a
  una scala finita**.
- **NO-collasso:** chi -> 0 + `|⟨n⟩|` -> 1 + autocorrelazione ~1 a ogni distanza. **E' il regime OFF
  rinominato.** Kuramoto refutato come sorgente di struttura.
- **NO-rumore:** chi -> 90 gradi + autocorrelazione ~0. Kuramoto non ha vinto sul rumore. Refutato.

> **DICHIARAZIONE: Kuramoto e' confermato come sorgente di struttura SOLO nell'esito SI.**
> Un chi che si abbassa, da solo, **non basta** e non verra' chiamato "struttura".

**Predizione dell'esecutore, messa per iscritto perche' possa risultare sbagliata:**
- K-frozen → **inerte** (per l'algebra del §1);
- K-noise → **non lo so, ed e' per questo che si gira.** Se devo scommettere: piu' probabile
  NO-rumore che SI, perche' il calcio del vuoto e' ~1.29 gradi/passo nel vuoto
  (`doc/INDAGINE_scuotimento.md` §3) mentre il torque di Kuramoto e' `O(dt^1)` e proporzionale a
  `forza_sync`, la stessa del Kuramoto-phi. Ma **e' una scommessa, non un'analisi**: non ho
  calcolato il rapporto delle due scale, e se l'esito fosse SI sarei contento di sbagliare.

---

## 4. ONESTA' SULLA PROVENIENZA (vale qualunque sia l'esito)

Se l'esito fosse **SI**, la struttura sarebbe ottenuta **CON un accoppiamento di allineamento
AGGIUNTO** — Kuramoto — e **non** emersa dalla dinamica base, che da' soltanto collasso o rumore.
Andra' scritto cosi': **"struttura semi-imposta da Kuramoto"**, mai *"struttura emergente"*.
Non e' squalificante — Kuramoto e' un meccanismo fisico noto e senza parametri nuovi qui — ma il
principio del progetto e' **emerge, non si impone**, e qui si e' a meta' strada. La provenienza si
dichiara.

---

## 5. COSA QUESTO ESPERIMENTO NON DIRA'

Non dira' nulla su **olonomia**, `W(r)` o gravita': quello e' il passo dopo, **solo** se l'esito e'
SI. Non concludera' sulla fisica (par.2.7: 300 passi, un seme): **ATTRIBUISCE** l'effetto di
Kuramoto fra tre possibilita'. E non dira' che il fork funziona o non funziona: dira' se il
**substrato** puo' avere struttura di Bloch quando si accende un allineamento locale.


---

# 6. ESITO — aggiunto il 2026-09-14 DOPO i run

> Tutto quanto sta SOPRA questa riga e' stato scritto e committato (`1e0a82c`) **prima** di lanciare
> i run. Qui sotto c'e' solo il risultato, e il confronto con la predizione.

## 6.1 — K-frozen: **INERTE, ed esattamente come predetto**

Non "quasi uguale" al braccio OFF: **byte-identico**.

| confronto K-frozen vs OFF | esito |
|---|---|
| array confrontabili (stessa shape) | **34 / 34** — il confronto ESISTE |
| `max\|A-B\|` | **0.000e+00** |
| N | 3576 = 3576 |

Kuramoto non ha fatto **letteralmente nulla**. L'algebra del §1 era giusta: sullo stato allineato
`nb_bar = nb`, quindi `cross(nb, nb_bar) = 0`, quindi torque nullo. **Lo stato allineato e' un punto
fisso anche per Kuramoto.** La predizione era falsificabile e non e' stata falsificata.
*(Il controllo "34/34 stessa shape" e' li' apposta: senza, uno `0.000e+00` potrebbe voler dire
"nessun confronto" — presidio di `CLAUDE.md` par.9.)*

## 6.2 — K-noise: **NO-rumore. Kuramoto non vince sul vuoto.**

| firma | RUMORE (null) | COLLASSO | **K-noise misurato** | verdetto |
|---|---|---|---|---|
| chi materia | 90.000 +- 39.171 | 0 +- 0 | **89.91 +- 39.23** | rumore |
| chi p90 (densi) | 90.000 | 0 | **89.80** | rumore |
| \|⟨n⟩\| / (1/sqrt(N)) | ~1 | ~60 | **0.91** | rumore |
| ⟨n_i·n_j⟩ vicino (d~0.22) | ~0 | 1.0 | **0.0022** | rumore |
| ⟨n_i·n_j⟩ lontano (d~13.9) | ~0 | 1.0 | **0.0007** | rumore |
| calo vicino→lontano | ~0 | 0 | **0.0015** | nessun decadimento |

Nessuna scala di dominio: la correlazione e' **piatta a zero** su tutte e 14 le distanze, da 0.22 a
13.9. E stabile nel tempo: `|⟨n⟩|` oscilla fra 0.009 e 0.016 dai passi 50 a 300 senza tendenza.

## 6.3 — MA Kuramoto NON e' inerte con il rumore: e' INEFFICACE

Distinzione da non perdere. Con lo scuotimento acceso, Kuramoto **cambia la dinamica**:

> N a 300 passi: ON (senza Kuramoto) = 3536 ; **K-noise = 4114** (**+578, +16.3%**)

Il torque agisce e cambia la traiettoria — semplicemente **non organizza le direzioni di Bloch**.
Non "non fa niente": **perde**. Coerente con l'ordine di grandezza scritto nella scommessa del §3:
calcio del vuoto ~1.29 gradi/passo contro un torque `O(dt^1)`.

## 6.4 — VERDETTO contro la PREDIZIONE

| | predetto al §3 | misurato | coincide? |
|---|---|---|---|
| K-frozen | inerte | **byte-identico a OFF** | **SI** |
| K-noise | "piu' probabile NO-rumore che SI" | **NO-rumore** | **SI** |

> **Esito: NO su entrambi i bracci. Kuramoto e' REFUTATO come sorgente di struttura** in questa
> configurazione, secondo il criterio dichiarato prima del dato.

**Non c'e' nulla da dichiarare sulla provenienza** (§4): quel paragrafo serviva solo in caso di SI.
Non essendoci struttura, non c'e' struttura semi-imposta di cui discutere l'onesta'.

## 6.5 — Cosa resta aperto, e cosa NO

Chiuso: Kuramoto non produce domini qui. I tre stati misurati del substrato sono ora **tre e tutti
senza struttura**: congelato (chi=0), rumore (chi=90), rumore+Kuramoto (chi=90).

**NON chiuso, e va detto:** 300 passi, **un seme**, e — soprattutto — **Kuramoto e' stato provato
SOLO contro il rumore a piena ampiezza.** Il §6.3 dice che perde; non dice che perderebbe sempre.
Se il calcio del vuoto fosse piu' debole, l'allineamento locale potrebbe vincere. Ma **abbassare
l'ampiezza dello scuotimento sarebbe TARARE UNA MANOPOLA per ottenere l'effetto voluto** — esattamente
il par.3 — e non si fa. Se un giorno l'ampiezza cambiasse per una ragione *derivata*, questa misura
andrebbe rifatta.
