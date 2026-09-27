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

---

# 4. **PREVISIONE DAL CODICE** — scritta **PRIMA** di leggere il referto del pilota

> **Mandato di Luca, 2026-09-27.** *«Cosa faranno le masse nella scena `(ii)`(a) con la
> configurazione del driver?»* — **dal CODICE, non dai risultati.**
>
> **COMMITTATA MENTRE IL PILOTA GIRA**, quindi il commit e' **antenato** del referto: l'ordine e'
> verificabile da git, non asserito da me. **Nessun numero del pilota e' stato letto.**
>
> **⚠ CHE COSA AVEVO GIA' VISTO, e lo dichiaro invece di lasciarlo implicito:** la
> **calibrazione al passo 0** *(contaminazione, richiamo, zone)* e il **giro corto d'impianto a
> 4 passi**, dove tutti gli `A(t)` valgono `~1e-5`. **Nessun checkpoint a 40/80/120.**

---

## 4.1 ⚠ **LE LEGGI CHE SCRIVONO `d0`** — *tutte VERIFICATE dal sorgente, con riga*

**`d0` e' la lunghezza di RIPOSO dell'arco. `d` la insegue** *(par. 4.2)*, quindi **e' qui che si
decide se il sistema si contrae.**

| sito | riga | la legge | SEGNO | da che cosa dipende | **DOVE agisce** |
|---|--:|---|---|---|---|
| `S02_rilass_visco` | `:5880` | `d0 += dt_e (d - d0)/tau_p_loc` | **insegue `d`** | `tau_p_loc = max(d/cs, (d/cs)(rho/peq))` | **ovunque** |
| `S03_diff_guscio` | `:5891` | `d0 += dt_e cs d lap(d0)`, clip causale | **liscia** | `lap(d0)` | **solo dove `d0` ha un gradiente: i GUSCI** *(il commento lo dice: «`lap(d0) ~ 0` nel nucleo uniforme, grande al bordo ripido»)* |
| `S05_spinta_locale` | `:6152` | `d0 += 0.02 d0 * _rep_mem` | **`+` = REPULSIVO** | eventi di repulsione, con memoria esponenziale | dove c'e' repulsione |
| `S08_proj` | `:6661` | `d0[mask] += proj` | segno di `mem_mot . dirarc` | memoria del moto, corretta dal **gradiente di torsione** | dove la torsione ha un gradiente |
| **`S09_spinta_med`** | **`:6808`** | `d0[mask] += spinta * median(d0[mask])` | **`grav = -tanh(s) * ampiezza`** | `s = \|tw\|/PHI_CRIT - 1`; `ampiezza`; `<n_i.n_j> * sign(dpozzo)` | **par. 4.3** |
| `S11_flusso` | `:6837` | `K_FRANGE = 0.0` | — | — | **MORTO PER COSTANTE** *(contatore `_g_k_frange_spento`)* |
| **`S12_coesione`** | **`:6987`** | `d0[mask] += passo_causale * tanh(F + richiamo) * filtro_portata` | **`richiamo_elastico = -(d0 - LAM)/LAM`: NEGATIVO ovunque `d0 > LAM`** | densita' locale **e** `d0` stesso | **OVUNQUE**, pesato da `filtro_portata = 1 - tanh(d/LAM)` |
| il FRENO | `:4431` | `d0 = v + _smorza(v, dx, 'd0_passo')` | **attenua SOLO le discese** | fattore `max(0, 1 - LAM/d0)` | ovunque |
| il PAVIMENTO | `_pav_d0` | **NO-OP col driver** | — | `SCALA_MIN_PASSO` acceso -> `return v` | **non morde** |
| nascite | `:6305`,`:6308`,`:6416`,`:6419` | concatenazioni | — | mitosi `d/2`+`d/2`; Schwinger `2*dd` **in parallelo** | alle nascite |

### ⚠ **IL TERMINE PIU' GROSSO E' UNIFORME, E NON E' LA GRAVITA'**

**`richiamo_elastico = -(d0 - LAM)/LAM`** (`:6894`) **tira OGNI arco verso `LAM`**, dappertutto,
**masse e vuoto allo stesso modo**. E' *«l'ancora elastica verso la scala nativa `LAM`»*, ed e'
**una legge globale per costruzione** — non perche' usi una statistica globale, ma perche' `LAM`
e' **la stessa costante ovunque**.
**PREVISIONE DIRETTA: il vuoto si contrae DA SOLO**, e **i punti di controllo lo vedranno**.

### ⚠ **E UN RESIDUO `A2` CHE NON SAPEVO, TROVATO LEGGENDO: `S09` USA LA MEDIANA GLOBALE**

```python
:6808   self.d0[mask] += self._sd0(spinta * float(np.median(self.d0[mask])), mask)
```

**E' esattamente il difetto che e' stato CURATO in `S05` il 2026-09-17**, e il codice lo dice
quattro righe sopra il suo fratello: *«Era: `spinta = 0.02 * np.median(self.d0) * rep` … `median`
e' una STATISTICA GLOBALE dentro un termine che si dichiara "Locale pura": `A2` violato»*
(`:6142-6150`). **In `S09` quella forma c'e' ancora**: ogni arco riceve **la stessa scala di
lunghezza**, indipendentemente dalla propria.
**Non e' il mandato di oggi e non lo curo qui** *(un prompt alla volta)*: **va in coda** come
**`S09-MEDIANA`**. **Ma conta per la previsione:** la spinta **non scala con l'arco su cui
scrive**.

---

## 4.2 `d` — **un'onda smorzata che insegue `d0`, piu' una sorgente**

```
:5776   vd += dts * (cs^2 * lap(d - d0) + src - beta * vd)
:5778   d  += dts * vd                          (poi il freno UNA VOLTA, :5789)
:5645   src = ALPHA_M * anom                    (ALPHA_NAT = 0)
:5620   anom = 2 (rho - peq) / (rho + peq)      in [-2, +2]
```

**SEGNO, e va letto al contrario dell'intuizione:** `src > 0` **dove `rho > peq`**, cioe' **dove la
densita' SUPERA l'equilibrio locale l'arco si ALLUNGA**. E' il termine che il codice chiama *«la
sorgente che espande il vuoto»* (`:359`). **Non e' un termine di attrazione.**
**E si SPEGNE da solo:** `peq` rilassa **verso `rho`** in forma esatta, quindi `anom -> 0`.
**INFERENZA:** a 120 passi `src` e' un **transitorio**, non un motore.

---

## 4.3 **LA SPINTA (`S09`): segno, ampiezza, e dove agisce**

```python
:6710   s        = |tw|/PHI_CRIT - 1                       # eccesso di torsione, FIRMATO
:6713   ampiezza = tanh( |dpozzo| / (0.5*(phi_g_i + phi_g_j)) )
:6724   grav     = -tanh(s) * ampiezza
:6744   proiez   = <n_i . n_j> * sign(dpozzo);   grav *= proiez
:6791   radiale  = grav*cos2;  tangenz = |grav|*sin2*sign(circ_arc)
:6805   spinta   = clip(radiale + tangenz, +-c_sistema*DT)
:6808   d0[mask] += spinta * median(d0[mask])
```

**IL SEGNO — `VERIFICATO`:** `grav < 0` *(l'arco si ACCORCIA)* **dove la torsione SUPERA il quanto
critico**, `|tw| > PHI_CRIT`; `grav > 0` **dove sta sotto**. **Il verso non e' «verso l'altra
massa»: e' «verso la torsione critica».**

**L'AMPIEZZA — `VERIFICATO`:** e' una **RIPIDEZZA RELATIVA** del pozzo, `|dpozzo| / pozzo_d'arco`,
**adimensionale e LOCALE**, limitata a `tanh(2) = 0.964` per costruzione *(il commento lo dimostra:
`|phi_g_j - phi_g_i| <= phi_g_i + phi_g_j`)*. **NON contiene la distanza da una massa**, e non
contiene la direzione dell'altra massa.

> ### 🎯 **RISPOSTA ALLA DOMANDA 2: la spinta NON accorcia i fili «fra le masse» in modo specifico.**
> **Non c'e' nessun termine che guardi la congiungente.** L'ampiezza e' un **gradiente relativo**
> — grande **dove il pozzo e' RIPIDO RISPETTO A QUANTO E' PROFONDO**, che e' una proprieta'
> **locale**, tipicamente **delle SUPERFICI** *(dove `phi_g` cambia in fretta)*, non del varco.
> **E il segno e' moltiplicato da `<n_i . n_j>`**, il prodotto scalare di due direzioni di Bloch.
> **`CLAUDE.md` par.9 misura `spin_ovl = 0.5000`, cioe' DIREZIONI CASUALI** — quindi `<n_i . n_j>`
> ha **media ~0 e segno che cambia da arco ad arco**.
> **INFERENZA, ed e' la mia previsione centrale: la spinta si MEDIA VIA sulle scale lunghe.**
> *(Con una riserva dichiarata: `_nb_grav()` in FASE 2 restituisce la direzione NATIVA del campo
> emesso, che potrebbe essere piu' correlata di quanto lo siano i Bloch. **Non l'ho misurato.**)*

---

## 4.4 **LA FASE: che cosa tiene coerente una massa**

**`VERIFICATO`:**
* l'accoppiamento che **allinea** i vicini e' `K_C` attraverso `cos(phi_i - phi_j)` *(potenziale
  delle fasi, `:373-375`; forza `:5095-5099`)*: **tende a tenere insieme cio' che e' gia' vicino**;
* **ogni MITOSI da' un calcio di fase CASUALE** ai due estremi dell'arco che si divide
  *(`:6268-6270`, ramo stocastico, che il commento chiama «canonico, validato: DEFAULT»)*:
  `phi[g] += normal(0,1) * KICK_TW * sciolta`;
* la scena scrive la fase **una volta sola**, a `_dphi()/2` con `sigma = 0.05`, e **non c'e'
  nessuna legge che la RIMETTA li'**.

> ### 🎯 **RISPOSTA ALLA DOMANDA 3 — `INFERENZA`:**
> **non esiste un termine che RECLUTI nodi nuovi nella fase della massa.** C'e' un accoppiamento
> che **allinea i vicini** e un **rumore che disallinea alle nascite**. Quindi il regime atteso e'
> **DIFFUSIVO**: la coerenza **si allarga di poco e si abbassa**, invece di **traslare**.
> **Previsione: SI SCIOGLIE, non migra.**

---

## 4.5 🎯 **RISPOSTA ALLA DOMANDA 4 — UNIFORMI contro SPECIFICI**

| | legge | perche' |
|---|---|---|
| **UNIFORMI** *(devono comparire ANCHE nei controlli)* | **`richiamo_elastico` -> `LAM`** (`S12`) | `LAM` e' la stessa costante ovunque |
| | il **freno** `_smorza` | attenua ogni discesa, ovunque |
| | `S02` *(`d0` insegue `d`)* | nessuna dipendenza dalla massa |
| | **`S09`**, **se** l'ampiezza e' davvero relativa | non contiene la distanza da una massa |
| **SPECIFICI DELLE MASSE** | **`forza_campo`** della coesione (`:6884`, `:6919`) | vive sul **gradiente di densita'**: massimo alle **SUPERFICI** |
| | **`S03_diff_guscio`** | `lap(d0)` e' grande **solo sui gusci** |
| | le **NASCITE** | la mitosi scatta sull'**eccesso di torsione**, che segue la materia |

---

## 4.6 🎯 **LE TRE PREVISIONI, con fiducia e con la misura che le FALSIFICA**

### **(a) Le masse si avvicinano PIU' dei controlli?** — **PREVEDO DI NO** *(o sotto la barra)*

**Fiducia: MEDIA-ALTA.** **Ragione, tutta dal codice:** **nessuno** dei termini che accorciano `d0`
contiene la **direzione dell'altra massa**; il termine piu' grosso (`richiamo_elastico`) e'
**uniforme**; la spinta ha **ampiezza relativa** e **segno modulato da un prodotto di Bloch che e'
misurato casuale**.
**Quindi il calo di `-4.3 %`/`-8.5 %` misurato in `W5`** *(da `-0.45` a `-0.89` su `~10.5`)*
**dovrebbe comparire QUASI TUTTO anche nei punti di controllo.**
**FALSIFICANTE:** `A(t) = (masse - controlli fissi)` a 120 passi, IC95 fra 4 semi. **Se `A < 0`
oltre la barra su almeno 2 coppie su 3, la previsione CADE** — e sarebbe il risultato piu'
interessante del pilota.

### **(b) Forma e allungamento mareale?** — **PREVEDO UN ALLUNGAMENTO, MA NON MAREALE**

**Fiducia: MEDIA.** **Ragione:** la coesione `forza_campo` vive sul **gradiente di densita'**, che
e' massimo **alle superfici**; `S03` liscia **solo i gusci**. **Quindi le SUPERFICI si muovono piu'
dei CENTRI per una ragione che non ha nulla a che vedere con la marea**, e il criterio `V6` —
*«superfici piu' dei centri oltre la barra -> ALLUNGAMENTO»* — **scattera' comunque**.
**⚠ E LO DICO PRIMA: il pilota NON PUO' distinguere le due cause.** Misura `insieme-insieme`, che e'
gia' **la superficie affacciata**; per separare marea da coesione servirebbe la **superficie
OPPOSTA**, che non e' misurata. **Se `V6` riporta un allungamento, NON si potra' chiamarlo mareale**
— e questa e' una lacuna del disegno, non un esito.
**FALSIFICANTE della mia spiegazione:** se il raggio e i quantili interni **NON** si muovono mentre
le superfici si avvicinano, la coesione di superficie non basta a spiegarlo.

### **(c) La coerenza migra o si scioglie?** — **PREVEDO CHE SI SCIOGLIE**

**Fiducia: MEDIA-ALTA.** **Previsione quantitativa:** `coer_campo` **scende** da `0.9988`
*(passo 0)*; la **sovrapposizione resta ALTA** *(`>= 90 %`)* e lo **spostamento del medoide resta
PICCOLO** *(`< LAM`)*, perche' non c'e' un termine di trasporto della fase.
**Quindi `V5` dovrebbe dire «LA MASSA SEGUE I NODI»** — **ma per la ragione sbagliata**: non perche'
la coerenza sia salda, **perche' non ha dove andare**.
**FALSIFICANTE:** sovrapposizione `< 90 %` **oppure** spostamento del medoide `>= LAM` su una
qualunque massa. **E se `coer_campo` NON scendesse**, cadrebbe la mia lettura del calcio di fase
alle nascite.

---

## 4.7 **CHE COSA HO VERIFICATO E CHE COSA HO INFERITO** *(la separazione che Luca chiede)*

| | |
|---|---|
| **VERIFICATO dal sorgente** *(riga citata)* | l'elenco dei siti che scrivono `d0` e i loro segni; `richiamo_elastico` e' uniforme; `src` ha segno **espansivo** dove `rho > peq`; `ampiezza` e' un gradiente **relativo** e **non contiene** la distanza da una massa; `grav` e' pilotata dall'**eccesso di torsione**, non dalla congiungente; `K_FRANGE = 0` e il pavimento `_pav_d0` e' **NO-OP** col driver; il calcio di fase casuale alla mitosi; **il residuo `A2` in `S09`** |
| **MISURATO ALTROVE, non da me oggi** | `spin_ovl = 0.5000` = direzioni casuali (`CLAUDE.md` par.9); `min(d) = 0.8000377` contro `LAM = 0.8` (`W3`); il calo `W5` di `-0.45`/`-0.89`; la barra fra semi `sd 0.146`-`0.510` |
| **INFERENZA** *(e va trattata come candidato, `P1`)* | che la spinta **si medi via** su scala lunga; che `src` sia un **transitorio**; che la coerenza **si sciolga invece di migrare**; che il calo di `W5` sia **quasi tutto uniforme** |
| **NON SO, e non fingo di sapere** | quanto valga `median(d0)` rispetto a `LAM` *(se fosse `~LAM`, il freno `1 - LAM/d0` congela le discese e TUTTO il quadro cambia)*; se `_nb_grav()` in FASE 2 sia piu' correlato dei Bloch; se la torsione supercritica sia **concentrata nel varco** — **se lo fosse, la previsione (a) cade**, ed e' la via piu' probabile per cui cada |

> **E LA PARTE PIU' UTILE SARA' DOVE HO SBAGLIATO.** Il confronto con il referto va scritto
> **accanto a questa pagina, senza riscriverla.**

---

# 5. **IL CONFRONTO: DOVE LA PREVISIONE HA SBAGLIATO** *(2026-09-27, dopo il referto)*

> **La previsione del par.4 NON E' RISCRITTA.** Sta nel commit **`1486cac`**, **antenato** del
> referto: l'ordine e' verificabile da git. Questa sezione le sta **accanto**.
>
> **I numeri escono da `csv/_test_fork/_confronto_previsione.py`** (`L-NUMERI`), referto in
> `csv/_test_fork/_pilota_prova1/CONFRONTO_previsione.txt`. **4 semi, IC95 con `t(3) = 3.182`.**

## 📊 IL BILANCIO IN UNA TABELLA

| | previsione | esito |
|---|---|---|
| **(a)** | le masse **NON** si avvicinano piu' dei controlli | ### ❌ **FALSIFICATA** ai passi `40` e `80`, **dal falsificante che avevo scritto io** |
| **(a-bis)** | il calo di `W5` *«quasi tutto uniforme»* | ### ❌ **FALSIFICATA a `40` e `80`**, **giusta a `120`** |
| **(b)** | un **allungamento** si', ma non mareale | ### ❌ **FALSIFICATA**: `0` allungamenti su `9` oltre la barra |
| **(c)** | la coerenza **si scioglie, non migra** | ### ✅ **MECCANISMO CONFERMATO**, ❌ **soglie sbagliate** |
| | la via per cui `(a)` sarebbe caduta: torsione **nel varco** | ### ❌ **NO**: `0` nascite nel varco. **`(a)` e' caduta per una ragione che non avevo previsto** |

---

## ❌ (a) — **LE MASSE SI AVVICINANO PIU' DEI CONTROLLI, MISURATO**

| passo | coppia | `A(t)` | IC95 | oltre la barra? |
|--:|---|--:|---|---|
| **40** | `massa_0\|massa_1` | **`-0.00296`** | `[-0.00376, -0.00215]` | ### **SI** |
| 40 | `massa_0\|massa_2` | `-0.00287` | `[-0.00898, +0.00324]` | no |
| **40** | `massa_1\|massa_2` | **`-0.00379`** | `[-0.00696, -0.00062]` | ### **SI** |
| **80** | `massa_0\|massa_1` | **`-0.01408`** | `[-0.02158, -0.00657]` | ### **SI** |
| **80** | `massa_0\|massa_2` | **`-0.01047`** | `[-0.01625, -0.00469]` | ### **SI** |
| 80 | `massa_1\|massa_2` | `-0.01230` | `[-0.02609, +0.00148]` | no |
| 120 | tutte e tre | `-0.0006` / `-0.0346` / `-0.0279` | tutti contengono lo zero | no |

**Il falsificante che avevo scritto era: «`A < 0` oltre la barra su almeno 2 coppie su 3».
Scatta a `40` (2 su 3) e a `80` (2 su 3). LA PREVISIONE (a) E' FALSIFICATA.**

### ⚠ **E A 120 NON SCATTA — NON PERCHE' L'EFFETTO SVANISCA, MA PERCHE' LA BARRA ESPLODE**

| passo | `sd` masse | `sd` controlli | rapporto |
|--:|--:|--:|--:|
| 40 | `0.0015`-`0.0021` | `0.0012`-`0.0019` | `x1.1`-`x1.3` |
| 80 | `0.0018`-`0.0073` | `0.0021`-`0.0047` | `x0.4`-`x2.7` |
| **120** | **`0.023`-`0.065`** | `0.009`-`0.011` | ### **`x2.1`-`x7.6`** |

**La dispersione fra semi della distanza fra le MASSE cresce di un fattore ~30 da 40 a 120 passi,
mentre quella dei CONTROLLI cresce di ~6.** **Il segnale non svanisce: affoga.**
**Questo e' un LIMITE DI RISOLUZIONE, e va scritto cosi':** a 120 passi *«non misurato»*, con
limite `|A| < 0.05`-`0.14`; a 40 e 80 passi **misurato**.
**→ conseguenza per il run base: 4 semi bastano a 40-80 passi e NON bastano a 120.**

## ❌ (a-bis) — **A 40 PASSI IL VUOTO SI ESPANDE MENTRE LE MASSE SI CONTRAGGONO**

| passo | masse | controlli | quanto e' uniforme |
|--:|--:|--:|---|
| **40** | `-0.0013` / `-0.0011` / `-0.0020` | **`+0.0016` / `+0.0018` / `+0.0017`** | ### **segno OPPOSTO** |
| 80 | `-0.0177` / `-0.0143` / `-0.0175` | `-0.0036` / `-0.0038` / `-0.0052` | **`20`-`30 %`** |
| 120 | `-0.0422` / `-0.0660` / `-0.0723` | `-0.0416` / `-0.0314` / `-0.0445` | `48`-`99 %` |

**Avevo previsto «quasi tutto uniforme». A 40 passi il vuoto va nell'ALTRA DIREZIONE**, e a 80
l'uniforme e' solo il `20`-`30 %`. **La mia previsione e' giusta solo a `120`**, cioe' **dove la
barra non permette di concluderlo.**
**Il contrasto piu' pulito e' a 40 passi, ed e' l'opposto di quello che avevo scritto.**

## ❌ (b) — **NESSUN ALLUNGAMENTO: `0` su `9`**

Centri e superfici si muovono **insieme** entro la barra, a tutti e tre i checkpoint e su tutte e
tre le coppie. **La mia spiegazione — la coesione di superficie — non ha nulla da spiegare.**
**E la lacuna che avevo dichiarato prima (non poter distinguere marea da coesione) NON si e'
presentata**, perche' non c'e' niente da distinguere.

## ✅❌ (c) — **IL MECCANISMO GIUSTO, LE SOGLIE SBAGLIATE**

| passo | `coer_campo` | `n_fase` | sovrapposizione | max spost. medoide | raggio |
|--:|--:|--:|--:|--:|--:|
| 0 | `0.99877` | `499.1` | `0.9976` | `1.036` | `3.153` |
| 40 | `0.62990` | `196.6` | `0.2472` | `1.971` | `3.161` |
| 80 | `0.34035` | `136.3` | `0.0827` | `3.710` | `3.180` |
| **120** | **`0.19555`** | **`124.7`** | `0.0491` | `7.250` | `3.175` |

**IL MECCANISMO E' CONFERMATO, e con un margine enorme:** `coer_campo` **crolla da `0.9988` a
`0.1956`** e `n_fase` perde il **`75 %`**. **La coerenza SI SCIOGLIE.**
**MA LE SOGLIE CHE AVEVO SCRITTO SONO SBAGLIATE:** prevedevo sovrapposizione `>= 0.90`
*(misurata `0.049`)* e spostamento `< LAM = 0.8` *(misurato fino a `7.25`)*.

### ⚠ **E IL CRITERIO `V5` CONFONDE DUE COSE — e' un difetto del CRITERIO, non del sistema**

`V5` legge *«sovrapposizione bassa + medoide spostato»* come **MIGRAZIONE**. **Ma qui la
sovrapposizione cala perche' L'INSIEME SI SVUOTA** (`n_fase 499 -> 125`), **non perche' si sposti.**
**E il metro dello spostamento e' sbagliato:** `LAM = 0.8` e' la scala **minima** del sistema, non
la scala della **regione**, che ha **raggio `3.15`**. Un medoide che si muove di `3.7` su un raggio
di `3.15` **si e' mosso dentro la propria regione**.
**→ voce `V5-SOGLIA`.** *(E' `P1-sexies`: il criterio era scritto dal mio modello mentale, non da
una misura.)*

## ❌ **LA VIA CHE AVEVO INDICATO NON E' QUELLA**

Avevo scritto: *«se la torsione supercritica fosse concentrata NEL VARCO, `(a)` cade, ed e' la via
piu' probabile per cui cada»*. **Le nascite dicono dove sta la torsione supercritica** *(la mitosi
scatta sull'eccesso di torsione)*:

| passo | mitosi (massa / varco / vuoto) | schwinger (massa / varco / vuoto) |
|--:|---|---|
| 40 | `0` / `0` / `0.2` | `0` / `0` / `0` |
| 80 | `0` / `0` / `52.2` | `0` / `0` / `10.0` |
| 120 | `0` / **`0`** / `526.5` | `0` / **`0`** / `122.2` |

### **ZERO nascite nelle masse e ZERO nel varco, a ogni checkpoint: TUTTE nel vuoto.**
**Quindi `(a)` e' caduta per una ragione che NON avevo previsto**, e questa e' la parte piu' utile
del confronto: **avevo indicato la via sbagliata pur avendo la conclusione giusta sul fatto che
cadesse.**

## 📌 **`V4`: LE SCORCIATOIE DI SCHWINGER CI SONO, E ORA SONO QUANTIFICATE**

| passo | coppie | scorciatoie | frazione | `2*dd/d` mediano | minimo |
|--:|--:|--:|--:|--:|--:|
| 80 | `10.0` | `2.5` | `25.00 %` | `1.0077` | `0.8916` |
| **120** | `122.2` | `47.8` | ### **`39.06 %`** | `1.0131` | `0.6256` |

**Il ritiro di ieri resta giusto per la MITOSI** *(l'arco `(a,b)` diventa `(a,m)`,`(m,b)` lunghi
`d/2`: il cammino e' lungo **quanto prima**)*, **e la coda Schwinger e' ora misurata: il `39 %`
delle coppie ACCORCIA il grafo**, col rapporto minimo `0.63`. **→ `SCHW-CORTI`**, che raffina
`FILI-CORTI`.

## ⚠ **DUE RIGHE DEL REFERTO NON PORTANO INFORMAZIONE, E LO DICO** *(`P4`, `A8`)*

1. **`n` in `forma_passo0` e' COSTANTE per costruzione**: e' l'insieme **congelato** del passo 0.
   Misurarlo e' un **test vuoto**. L'`n` informativo e' **`n_fase`**. **→ `FORMA-N-VUOTO`.**
2. **`foglio_0 = 0.50384` AL PASSO 0** — cioe' **il suo valore sotto ipotesi nulla**, non un
   risultato: la scena scrive `phi = _dphi()/2 = 2 pi` **esattamente sul confine** fra i due fogli
   di `floor(phi/2pi)`, e la gaussiana `sigma = 0.05` **lo attraversa**. **Il diagnostico dei fogli,
   cosi' com'e', su questa scena non misura nulla** — ed e' il presidio del *«quanto varrebbe se non
   ci fosse niente»*. **→ `FOGLIO-NULLO`.**

---

> ## 🛑 **E IL PILOTA NON CONCLUDE SULLA GRAVITA', COME DETTO IN TESTA**
> **`5 SI` sono aperti**, i controlli sono **punti di vuoto** e non masse di prova, e l'osservabile
> **non separa** *«spinta»* da *«qualunque altra cosa acceleri la contrazione dove c'e' materia»*.
> **Cio' che il pilota dice e' che la grandezza SI MISURA, a 40-80 passi e con 4 semi** — ed e'
> **esattamente il suo scopo.**
