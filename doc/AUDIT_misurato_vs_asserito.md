# AUDIT — che cosa nel corpus e' MISURATO, che cosa solo ASSERITO, che cosa e' SMENTITO

> Sola lettura, 2026-09-14. Branch `fork-su2`, blob **2277e9a0**.
> **Questo documento NON corregge le fonti.** Elenca e basta: la correzione e' una decisione
> successiva di Luca. I documenti auditati restano com'erano.
>
> Legenda:
> **[MISURATO]** c'e' un run / un sigillo / un numero a supporto — citato.
> **[ASSERITO]** scritto senza una misura a monte, o citando una riga `# APERTO` / un condizionale.
> **[SMENTITO]** i dati contraddicono l'affermazione — col numero che la smentisce.
> **[INCOMPLETO]** vero ma parziale: descrive meta' del codice e induce in errore sull'altra meta'.

---

## PERCHE' QUESTO AUDIT ESISTE

In un giorno solo sono emerse due affermazioni forti, scritte come fatti, che fatti non erano:
l'isotropia "gia' verificata" (che citava un `# APERTO`) e la premessa della firma di W(r) ("nel
centro i Bloch sono allineati"), che i dati smentiscono. Entrambe erano a monte di decisioni
operative — una serviva a saltare un sigillo, l'altra a giustificare ore di lavoro sul W(r).
Il rischio non e' avere documenti imprecisi: e' **pianificare su un'asserzione credendola una
misura.** Da qui l'elenco.

---

## 1. SCUOTIMENTO DEL VUOTO

| # | affermazione | fonte | esito |
|---|---|---|---|
| 1.1 | *"ISOTROPIA GIA' VERIFICATA: «il momento angolare netto NON dipende dal vuoto stocastico» (riga ~114)"* | `doc/ROADMAP_fork_SU2.md:46` | **[ASSERITO]** |
| 1.2 | *"Isotropia GIA' verificata (riga ~114)"* | `doc/BUSSOLA_TECNICA_dev-spinoriale.md:142` | **[ASSERITO]** (stessa citazione, ripetuta) |
| 1.3 | *"Gia' nel codice (righe ~1884-1885), **gated da SYNC_UPDATE and SCUOTIMENTO**"* | `doc/ROADMAP_fork_SU2.md:42` | **[INCOMPLETO]** |
| 1.4 | *"senza [SYNC_UPDATE/SCUOTIMENTO], la degenerazione dei Bloch non si rompe"* | `STATO_CLAUDE_fork-su2.md:112` e `:433`; `ROADMAP:48-49` | **[SMENTITO]** |
| 1.5 | *"amp = sqrt(Lam)/(1+I2/Lam) → forte nel vuoto, debole nella materia"* | `ROADMAP:44` | **[MISURATO]** |
| 1.6 | *"RUMORE INDIPENDENTE per nodo → rompe la degenerazione senza correlare i vicini"* | `ROADMAP:45` | **[MISURATO]** la prima meta', **[ASSERITO]** la seconda |

**1.1 / 1.2 — perche' ASSERITO.** Le righe 113-114 di `soliton_simulator.py` sono:
```
# APERTO: la PRECESSIONE fra due masse persiste in regime deterministico? Se si', il momento
#         angolare netto NON dipende dal vuoto stocastico (risultato forte).
```
Marcate **`# APERTO:`**, in forma **condizionale** (*"Se si', ... risultato forte"*): una domanda
aperta con la sua conseguenza ipotetica. I due documenti hanno citato l'**apodosi** di un periodo
ipotetico come se fosse un risultato. E la ROADMAP stessa, otto righe piu' sotto (`:54`), elenca
l'isotropia fra i **sigilli da fare**: *"SIGILLI DISTINTI: scuotimento → isotropia (⟨n⟩ nel tempo)"*.
Il documento si contraddice da solo a otto righe di distanza.
→ **Oggi e' [MISURATO]**, per la prima volta: vedi §3.2.

**1.3 — perche' INCOMPLETO.** Le righe citate descrivono **solo il ramo sincrono**. Esiste un ramo
complementare, `soliton_simulator.py:1796`:
```python
if SCUOTIMENTO and not SYNC_UPDATE:      # :1796
    self._nb = self._nb + self.rng.normal(0, 1.0, (n, 3)) * amp[:, None]   # :1803
```
Il gate non e' una congiunzione che spegne: e' un **dispatch** fra due implementazioni della stessa
legge, una per schema di aggiornamento (le ragioni sono nel codice, `:2023`: *"il rumore e' un
aggiornamento t→t+1: non puo' contaminare il campo B letto dalla snapshot"*). Descrivere meta' del
meccanismo ha indotto in errore l'esecutore: vedi 1.4.

**1.4 — perche' SMENTITO.** Poiche' `SCUOTIMENTO=True` di default e il ramo `:1796` gira quando
`SYNC_UPDATE=False`, **lo scuotimento dei Bloch ha girato in tutta la config certificata**. Sonda
diretta sui globali vivi: `DURANTE il run → SCUOTIMENTO=True, SYNC_UPDATE=False` con il ramo `:1796`
attivo. La frase e' falsa in entrambi i sensi: il vuoto non era spento, e i risultati passati **non**
sono "senza vuoto".
*(Nota onesta: questo errore l'esecutore l'ha prima commesso e poi corretto — vedi
`doc/INDAGINE_scuotimento.md` §0. La fonte documentale lo ha indotto, non giustificato.)*

**1.6 — la seconda meta'.** Che il rumore sia indipendente per nodo e' **[MISURATO]** (si legge dal
codice: `n` estrazioni distinte). Che *"rompa la degenerazione"* e' **[ASSERITO]**: e' una
previsione sull'esito dinamico, e fino a oggi nessuno aveva misurato la distribuzione di `chi`.
→ Oggi e' misurata: vedi §3.1. E la risposta non e' quella che il documento dava per scontata.

---

## 2. BLOCH, ORDINE, STRUTTURA

| # | affermazione | fonte | esito |
|---|---|---|---|
| 2.1 | *"CENTRO (r≈0): W basso — **massa coerente → Bloch allineati → χ≈0** → olonomia banale"* | `doc/PROTOCOLLO_test_olonomia.md:41` | **[SMENTITO]** |
| 2.2 | *"BORDO (r≈R): W MASSIMO — i Bloch cambiano direzione (dentro→fuori) → χ grande"* | `PROTOCOLLO:42` | **[ASSERITO]**, e la premessa e' caduta |
| 2.3 | *"FIRMA della non-abelianita' fisica = PICCO di W(r) sul bordo, con centro e vuoto bassi"* | `PROTOCOLLO:44` | **[ASSERITO]** — non falsificabile come scritto se χ e' uniforme |
| 2.4 | *"χ resta SPARSA → il rumore vince, degenerazione rotta, settore non-abeliano vivo"* | `ROADMAP:59` | **[MISURATO]**, ma la dicotomia e' incompleta |
| 2.5 | *"U_ij derivato dai soli Bloch e' «schiavo» della materia (no gradi di liberta' propri)"* | `BUSSOLA:69` | **[MISURATO]**, e in forma piu' forte |
| 2.6 | *"Il verdetto (B) abeliano e' STRUTTURALE, non dinamico"* | `BUSSOLA:23` | **[MISURATO]** |
| 2.7 | *"Misure gauge-robuste concordi: spin_ovl=0.5000, segno_ov~2/pi ovunque"* | `STATO:463` | **[MISURATO]**, ma **letto come un'altra cosa** |

**2.1 — perche' SMENTITO, col numero.** Misurato oggi (osservatore sigillato pure-read, 150 passi,
braccio ON), sugli archi **piu' densi** del sistema (p90 di `|Psi|^2`):
> **χ = 90.14° di media, std 39.35°, mediana 90.00°**

Per direzioni **casuali indipendenti** sulla sfera l'atteso analitico e' **90.000° / 39.171°**. Gli
archi piu' densi sono casuali **quanto il vuoto** (90.13° / 39.10°). La premessa *"massa coerente →
Bloch allineati"* **non vale in questo sistema**.

**2.3 — la conseguenza operativa.** Se χ e' uniforme ovunque, **W(r) e' piatto per costruzione** e
la gobba non puo' esserci, qualunque cosa faccia il fork. Il PROTOCOLLO prevede il caso (`:47`,
*"W(r) piatto ~2 ovunque → connessione ABELIANA anche col fork"*) ma lo interpreta come verdetto
**sul fork**; con χ uniforme sarebbe invece un verdetto **sulla distribuzione dei Bloch**, cioe' un
test che non puo' discriminare. Da sapere **prima** di spendere ore sul W(r).

**2.4 — la dicotomia incompleta.** La ROADMAP offre due esiti: χ *sparsa* (rumore vince, sano) o
*collassata su 0/π* (allineamento domina). **Manca il terzo, che e' quello osservato:** χ
distribuita **esattamente come direzioni casuali**, cioe' nessuna struttura **da nessuna parte**,
nemmeno dove la densita' e' massima. "Sparsa" viene letto come buona notizia, ma *sparsa ovunque
allo stesso modo* significa che non c'e' niente da trasportare.

**2.5 — piu' forte del previsto.** Il caveat "schiavi" e' diventato **inerzia dimostrata** (teorema,
`csv/_seal_fork/_reperto_inerzia.py`, 1.570e-15 su 200000 coppie): non solo schiavi, **inerti** —
poi risolto dallo Strato 1.

**2.7 — il reperto piu' importante di questo audit.** `spin_overlap_arco` e'
`<|<psi_i|psi_j>|^2>` pesato sugli archi (`soliton_simulator.py:5394`), cioe'
`<cos^2(χ/2)> = (1 + <cos χ>)/2`. Per direzioni casuali `<cos χ> = 0`, quindi **l'atteso e'
esattamente 0.5000**. La campagna 5.3c misuro' **spin_ovl = 0.5000 su tutti e tre i bracci a 800
passi** (`STATO:457-463`) e lo registro' come *"misura gauge-robusta concorde col verdetto (B)
abeliano"*.

> **La casualita' dei Bloch era nei dati da allora, a 800 passi e su tre bracci. E' stata letta
> come conferma di una tesi diversa.**

*Precisione doverosa:* `spin_ovl = 0.5` e' **necessario ma non sufficiente** per l'uniformita' —
qualunque distribuzione simmetrica in `cos χ` da' 0.5. Quindi quel numero da solo **non
dimostrava** la casualita': la rendeva compatibile. E' la distribuzione **completa** misurata oggi
(media, deviazione standard, **entrambe le code**) a fissarla. Ma il segnale c'era, e nessuno gli
ha fatto quella domanda.

---

## 3. CHE COSA E' [MISURATO] DA OGGI (per la prima volta)

**3.1 — Distribuzione di χ.** Osservatore `csv/_test_fork/_osserva_vuoto.py`, sigillato pure-read
(`_sigillo_osservatore.py`, 6/6 PASS, byte-identita' `0.000e+00`). 150 passi, seme 1, braccio ON:

| χ (gradi) | MATERIA | VUOTO | p90 (densi) | atteso, direzioni casuali |
|---|---|---|---|---|
| media | 90.04 | 90.13 | 90.14 | **90.000** |
| std | 39.23 | 39.10 | 39.35 | **39.171** |
| mediana | 89.95 | 90.05 | 90.00 | **89.98** |
| frazione < 10° | 0.0074 | 0.0077 | 0.0073 | **0.0076** |
| frazione > 170° | 0.0075 | 0.0075 | 0.0078 | **0.0076** |

Stabile ai passi 50, 100, 150. Combacia con la densita' `sin(χ)/2` entro 0.1° su media e std.

**3.2 — Isotropia ⟨n⟩ (chiude il `# APERTO` di §1.1).** `|⟨n⟩| / (1/sqrt(N))` fra **0.39 e 1.17**
in tutte le regioni e a tutti gli istanti, senza crescita nel tempo. **Nessun verso preferito.**
Controprova che l'osservatore legge stato vero: al passo 1 misura `|⟨n⟩| = 1.0` esatto in
`(0,0,1)` — la condizione iniziale con tutti i nodi al polo — che poi si randomizza.

**3.3 — Ampiezza dello scuotimento** (`doc/INDAGINE_scuotimento.md` §3): `Lam = 1.688e-04`;
`amp` vuoto `1.2993e-02` (calcio ~1.29°/passo sul Bloch) contro picco `1.4928e-03` (~0.148°/passo);
rapporto **8.70**. Conferma 1.5 con i numeri.

**Limiti di tutto il §3:** 150 passi, **un seme**, **un solo braccio** (ON). Per il par.2.7 nulla di
questo conclude sulla fisica. L'attribuzione — se sia lo scuotimento a randomizzare o la dinamica a
non organizzare — richiede il braccio OFF.

---

## 4. IL FILO COMUNE (perche' questi errori si somigliano)

Tre episodi in due giorni, stessa forma:

1. **2026-09-13** — `N = 3164 → 3209` a 150 passi letto come effetto del fork. Era **rumore a 1e-16
   amplificato dal caos**. (Numero grande scambiato per segnale.)
2. **2026-09-14** — `max|A-B| = 0.000e+00` letto come identita'. Era **mancanza di confronto**: i
   due run avevano 3209 e 3073 nodi, 32 shape su 32 divergenti. (Zero scambiato per identita'.)
3. **2026-09-14** — `spin_ovl = 0.5000` letto come conferma del verdetto (B). Era **anche** il
   valore atteso per Bloch casuali, e nessuno gli ha posto quella domanda. (Numero giusto, domanda
   sbagliata.)

**La regola che li copre tutti e tre: prima di leggere una statistica riassuntiva, chiedersi che
valore avrebbe se NON ci fosse niente.** N a 150 passi, uno zero, un 0.5: in tutti e tre i casi il
valore-sotto-ipotesi-nulla era calcolabile in due righe, e avrebbe fermato l'errore.

---

## 5. COSA QUESTO AUDIT NON FA

Non corregge le fonti: `ROADMAP`, `BUSSOLA`, `BUSSOLA_TECNICA`, `PROTOCOLLO` e `STATO` restano
com'erano, e le correzioni sono decisioni di Luca (in particolare `ROADMAP:46` e `:42`,
`PROTOCOLLO:41-44`, `STATO:112` e `:433`). Non giudica la fisica: dice solo quali affermazioni
hanno una misura sotto e quali no. E non chiude la domanda aperta di oggi — **se i Bloch siano
casuali per colpa dello scuotimento o perche' la dinamica non organizza** — che richiede il
confronto ON/OFF.
