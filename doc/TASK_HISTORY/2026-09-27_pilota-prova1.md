# PILOTA DELLA `PROVA 1` — **NON e' il run base**

> ## ⚠⚠ **QUESTO NON E' IL RUN BASE, E VA DETTO IN TESTA.**
> **Gli altri `SI` sono APERTI:** `doc/SMISTAMENTO_run_base.md` ne conta **5**. Questo e' un
> **PILOTA**: gira il driver con `POZZO_D` acceso per **vedere se le grandezze si misurano**, non
> per concludere sulla gravita'. **Nessuna conclusione sulla gravita' dal pilota: solo i numeri e
> i limiti** *(mandato di Luca, 2026-09-27)*.
>
> **COMMITTATO PRIMA DEL CODICE** (`CLAUDE.md` par.8).

---

## 1. RAGIONAMENTO PRELIMINARE

### 1.1 Da dove viene questo pilota

Da **due riscontri di ieri e oggi**, entrambi miei errori corretti da Luca:

1. **`W5`** ha misurato che la distanza fra le masse **cala** *(`−0.45` a `−0.89` su `~10.5`)*, e io
   l'avevo spiegata con *«piu' nodi = piu' scorciatoie»*. **E' FALSA**: la mitosi **sostituisce**
   l'arco `(a,b)` con `(a,m)`,`(m,b)` **lunghi `d/2`** *(`:6272`, `:6292-6293`)*, quindi il cammino
   attraverso il figlio e' lungo **quanto prima**. **Le nascite non accorciano il grafo:
   l'avvicinamento viene dalle LUNGHEZZE DEI FILI.**
2. **`AB-CONTROLLI`**: il braccio di `W5` **non ha salvato i punti di controllo**, e senza quelli
   *«i fili si accorciano fra le masse»* non si distingue da *«si accorciano ovunque»*.

### 1.2 ⚠ IL CRITERIO DI FASE **NON E' SCRITTO NEL CODICE**, e va detto prima di usarlo

Il mandato dice *«ridefinisci la regione dalla FASE (stesso criterio con cui la scena `(ii)` la
costruisce, scritto nel codice, non reinventato)»*. **Ho letto la scena, e il criterio con cui
costruisce la regione e' GEOMETRICO, non di fase:**

```python
# _semina_masse_coerenti
idx = np.where(np.linalg.norm(pos - c, axis=1) <= r)[0]     # <- la regione viene da `pos`
...
ph = net._dphi() / 2.0 + net.rng.normal(0, 0.05, len(idx))  # <- POI le assegna la fase
net.phi[idx] = ph % net._dphi()
```

> **La scena costruisce la regione da `pos` e POI le da' una fase.** Quindi **un criterio di fase
> da riusare non esiste**: cio' che esiste e' **la fase che la scena SCRIVE**, e da quella il
> criterio si **deriva**:
> **la regione e' `|wrap(phi − _dphi()/2)| <= k · 0.05`**, dove **`_dphi()/2` e `0.05` vengono dal
> codice della scena**, non da me. **L'unica scelta e' `k`.**

**E `k` non si tarda guardando i risultati: si CALIBRA al passo 0, dove la risposta e' NOTA** —
la scena dice **esattamente** quali nodi sono nella regione. **`P1-sexies`: un criterio si collauda
su un caso a risposta nota.** Si riportano **precisione e richiamo** per `k = 2, 3, 4`, e **si fissa
`k` PRIMA** dei checkpoint successivi.

**Cosa mi aspetto, e perche' potrebbe non funzionare:** il vuoto ha `phi` **uniforme su `[0, 4pi)`**,
quindi una frazione `2k·0.05/(4pi)` dei nodi di vuoto cade dentro **per caso** — con `k = 3` e' lo
`2.4 %` del vuoto, che essendo il `90 %` dei nodi vale **~`22 %` della taglia della regione**.
**Se la contaminazione e' quella, il criterio di fase NON basta da solo**, e va detto invece di
spacciarlo per una misura. *(Una via: richiedere ANCHE la contiguita' sul grafo. Non la scrivo
adesso: la decide la calibrazione.)*

### 1.3 Cosa NON so

- **se la fase resti concentrata**: la scena la scrive con `sigma = 0.05`, ma la dinamica la muove.
  Se a 120 passi `sigma` e' cresciuta oltre `k·0.05`, il richiamo crolla — **e sarebbe un
  RISCONTRO**: direbbe che la coerenza **si disfa**, non che la massa migra.
- **se `2*dd < d` capiti mai** per lo Schwinger: e' una misura, non una deduzione.

---

## 2. PROGETTAZIONE — i criteri, **prima dei numeri**

**Strumento:** `csv/_test_fork/_pilota_prova1.py`. **Driver** con `POZZO_D` **acceso** *(ora e' il
default del driver)*, **scena `(ii)`(a)**, **4 semi**, **120 passi**, **`passo_pieno`** (`H-P9`),
**un processo per braccio** (`STANDARD 1`). **Checkpoint: `0, 40, 80, 120`.**

| # | criterio | che cosa decide | che cosa mi fa FERMARE |
|--:|---|---|---|
| **V1** | **masse E punti di CONTROLLO**, **FISSI**: scelti **una volta al passo 0** e poi **SEGUITI**, 4 coppie disgiunte per coppia di masse | **`AB-CONTROLLI` chiuso**: il braccio li **salva** | se i controlli non si trovano *(`K4` fallisce)*, la `PROVA 1` **non ha braccio di confronto** |
| **V2** | l'osservabile e' **`(masse − controlli)` RELATIVO alla distanza iniziale**, con **IC95 fra semi** `t(3)` | se il calo e' **specifico delle masse** o **globale** | se `masse` e `controlli` calano **uguale**, e' **contrazione globale e NON e' gravita'** — e va scritto cosi' |
| **V3** | **DOVE nascono i nodi** *(masse / varco fra le masse / vuoto)*, **mitosi e Schwinger SEPARATI** | e' la **misura `M1` di `SCALE-TW`**, quasi gratis | — *(e' una misura, non ha un fallire)* |
| **V4** | quante coppie Schwinger hanno **`2*dd < d`** dell'arco | le **scorciatoie** da `A3-DISEGNO`: sono **l'unico** cammino nuovo | se fossero molte, il grafo **si accorcia anche per nascita**, e `FILI-CORTI` cambia |
| **V5** | **`MASSA-MIGRA` (a)**: regione **ridefinita dalla FASE**; **sovrapposizione** coi nodi del passo 0 e **spostamento del medoide**; distanza calcolata **sui nodi del passo 0 E sulle regioni attuali** | **sovrapposizione `>= 90 %` E spostamento `< LAM`** → la massa **segue i nodi**, il metro attuale basta; **altrimenti MIGRA**, e la `PROVA 1` va misurata **sulle regioni** | se le due distanze **divergono**, il numero di `W5` **misurava un'altra cosa**: si dice, non si scegle la piu' comoda |
| **V6** | **`MASSA-MIGRA` (b) — LA FORMA**: `n` nodi, **raggio** *(distanza media dal medoide)*, **quantili `p10/p50/p90`** delle distanze interne, **coerenza** *(parametro d'ordine della fase)*; per coppia, **centri** e **superfici affacciate** *(insieme-insieme)* | la forma e' **«costante»** se **ogni** grandezza resta **entro la dispersione fra semi del passo 0** | **se le superfici si avvicinano PIU' dei centri oltre la barra: ALLUNGAMENTO** *(possibile effetto mareale)* — **e' un RISULTATO, non un difetto, e NON VA CORRETTO** |

### 2.1 Le letture si fissano QUI

- **❗ CORREZIONE DI LUCA, 2026-09-27 — I CONTROLLI SONO FISSI, NON RISCELTI.** **Cio' che il
  primo strumento faceva, e che lascio leggibile:** `OP.controlli()` cercava, **a ogni**
  **checkpoint**, la coppia di vuoto piu' vicina alla distanza **del momento** fra le masse.
  **Quindi `c(t) ~ m(t)` PER COSTRUZIONE e `A(t) -> 0` qualunque cosa faccia la gravita'**: `V2`
  perdeva **esattamente** cio' per cui esiste. **L'avevo scritto come «limite DICHIARATO»** nel
  referto e nel commit — **e dichiararlo non basta** (`A9`): **un osservabile che non puo'
  misurare la propria alternativa non e' un osservabile, e' un numero.** **L'ha visto Luca
  leggendo il mio stesso `COSA-RICONTROLLARE`.**
  **CURA:** `controlli_fissi()` al passo 0 *(vuoto, oltre `r_regione` di distanza di grafo da
  ogni nodo di massa, stessa distanza iniziale entro il `10 %`, **4 coppie disgiunte**)* piu'
  `segui_controlli()` a ogni checkpoint **sugli STESSI nodi**. **Le esclusioni si CONTANO e non
  si sostituiscono**: sostituirle rifarebbe la riscelta con un altro nome.
  **`K5` 2/2**, e **la riga che conta e' `K5b`**: su un effetto vero del **`-4.475 %`** i fissi
  stanno a **`+0.0000 %`** e l'osservabile lo vede tutto, mentre **la riscelta porta `A` a
  `+0.025 %`** — **l'effetto sparisce**. **`K5a` (tutto contratto del `5 %`) NON discrimina**, e
  lo dico: con una contrazione uniforme anche la riscelta legge `-5 %`, perche' bersaglio e
  candidati si scalano dello stesso fattore. **-> voce `CTRL-RISCELTA`.**


- **tutte le distanze sono LUNGO IL GRAFO pesato con `d`** *(`csv/_osservabile_p1.py`)*, **mai
  `pos`** — e il centro e' **il medoide di grafo** (`A3-DISEGNO`);
- **`V2` si scrive come frazione:** `[(m(t) − m(0)) − (c(t) − c(0))] / m(0)`, cosi' il numero e'
  adimensionale e la barra si confronta col nullo di `W5` *(`1.3`-`2.7 %`)*;
- **se un IC95 contiene lo zero si scrive il LIMITE**, non *«nessun effetto»*, **con la
  risoluzione accanto**;
- **LA COERENZA DELLA MASSA E' `|<e^{i phi}>|`**, e la ragione e' **misurata nel simulatore**, non
  scelta: il commento di `FASE_2PI` (`soliton_simulator.py:1300`) porta **`Z118`/`Z120`** —
  **in 31 righe su 31 il campo legge `phi` da `exp`/`cos`/`sin`**, e li'
  `exp(i(phi + 2 pi)) = exp(i phi)`. **Per la fisica del campo `phi` e `phi + 2 pi` sono LO STESSO
  STATO**; la doppia copertura vive nel **SEGNO** dello spinore (`_spinor_lift`, `sign(perc_chi)`)
  e nei **MEZZI ANGOLI**, **non in `phi`**. E `std(phi)` resta esclusa per la ragione che la scena
  da': su un cerchio legge **disordine massimo** dove la fase e' coerente (`std = 6.08` contro
  `0.05`).
- **IN PIU', SOLO COME DIAGNOSTICO, LA MISCELA DI FOGLI** *(richiesta di Luca)*: `coer_dominio =
  |<e^{i 2 pi phi / _dphi()}>|` e le frazioni **`foglio_0`/`foglio_1`** = `floor(phi / 2 pi)` dentro
  `_dphi()`. **La fisica del campo non li vede, ma la TORSIONE li distingue**, quindi sono
  un'informazione — **e non sono un criterio**.
- **COLLAUDATI SUL CASO NOTO, `K-FOGLIO` 4/4** *(`python csv/_test_fork/_pilota_prova1.py
  --collaudo`)*: meta' nodi a `2 pi` e meta' a `0` danno **`coer_campo = 1.000000`** *(per il campo
  sono lo stesso stato)* e **`coer_dominio = 0.000000`** *(i fogli sono mescolati)*, con
  `foglio_0 = 0.500`. **Il valore OPPOSTO e' la riga che conta** (`P1-sexies`): se i due numeri
  coincidessero, il diagnostico non diagnosticherebbe nulla. Fasi casuali sul dominio danno
  `0.0062` / `0.0123`, cioe' il nullo.

> ### ❗❗ **LA STORIA DI QUESTA RIGA, IN TRE STRATI, E RESTA TUTTA LEGGIBILE** *(2026-09-27)*
>
> **① CIO' CHE AVEVO SCRITTO** *(e che e' tornato a essere il criterio)*:
> *«la coerenza e' `|<e^{i phi}>|` sulla regione — non `std(phi)`, che su un cerchio legge il
> disordine massimo dove la fase e' coerente (e' scritto nella scena stessa: `std = 6.08` contro
> `0.05`)»*.
>
> **② LA CORREZIONE DI LUCA, la mattina** — **applicata, collaudata `3/3`, e POI ANNULLATA**:
> *«la coerenza `|<e^{i phi}>|` e' SBAGLIATA per il dominio attivo: con `_dphi() = 4 pi` le masse
> stanno a `2 pi` e un nodo a fase `0` (antifase) verrebbe contato come coerente. Usa
> `|<exp(i 2 pi phi / _dphi())>|`»*. **Il conto era giusto:** le due forme **danno davvero** `1` e
> `0` su quel caso. **Cio' che non reggeva era la PREMESSA FISICA** — che `phi` e `phi + 2 pi`
> fossero stati **diversi** per la dinamica.
>
> **③ IL RITIRO DI LUCA, il pomeriggio** *(«errore del guardiano»)*: `Z118`/`Z120` dicono che il
> campo **non li distingue**, quindi `|<e^{i phi}>|` **non confonde** due stati: **li identifica
> perche' la fisica li identifica.**
>
> **PERCHE' I TRE STRATI RESTANO QUI, e non e' pedanteria:** cancellare ② lascerebbe il repo senza
> il **numero** che distingue le due forme — che e' vero e utile, ed e' diventato il **diagnostico
> dei fogli**. E lascerebbe senza la lezione: **il conto era giusto e la premessa no**, cioe'
> esattamente il caso in cui una verifica numerica **non** protegge. **`P1`: l'associazione genera
> candidati, non conclusioni** — e vale anche quando il candidato arriva da Luca.
> **Ed e' la ragione per cui ho verificato `Z118`/`Z120` DAL SORGENTE prima di annullare**, invece
> di applicare il ritiro sulla fiducia: se la premessa del ritiro non avesse retto, avrei dovuto
> dirlo.
>
> **-> voce `COER-4PI` dell'indice.**

### 2.2 Che cosa questo pilota **NON** fa

**Non e' il run base** *(5 `SI` aperti)* e **non conclude sulla gravita'**. **Nessun run lungo:**
120 passi, gli stessi di `W5`.

---

## 3. TODO DEL NEXT STEP

- [ ] `csv/_test_fork/_pilota_prova1.py`: 4 semi x 1 braccio, checkpoint `0/40/80/120`;
- [ ] il braccio **salva** controlli, nascite *(per zona e per meccanismo)*, Schwinger `2*dd < d`,
      e per ogni massa **nodi/raggio/quantili/coerenza** e le due regioni *(passo 0 e attuale)*;
- [ ] la **calibrazione di `k`** al passo 0, con **precisione e richiamo** per `k = 2, 3, 4`;
- [x] **`K-FOGLIO` 4/4**: il criterio e' CIECO al foglio, il diagnostico NO *(collaudo su caso noto)*;
- [ ] il referto con gli IC95 fra semi e **i limiti** dove contengono lo zero;
- [ ] inventario + relazione **nello stesso commit**; `AB-CONTROLLI` chiuso;
- [ ] **STOP: nessuna conclusione sulla gravita'.**
