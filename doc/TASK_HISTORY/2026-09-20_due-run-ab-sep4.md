# 2026-09-20 -- DUE RUN COMPLETI A/B a `sep = 4.0`, 3000 passi, in parallelo

Mandato: *"NON usare gli snapshot vecchi. DUE RUN COMPLETI a `sep = 4.0`, in parallelo."*
Simulatore all'avvio: sha1 grezzo `edb8f844` (blob git `b44f50ce`). HEAD all'avvio: `a47ebfd`.

---

## 1. RAGIONAMENTO PRELIMINARE -- cosa credo PRIMA di guardare

### 1.1 Perche' questo run esiste, e cosa lo ha reso necessario

L'A/B corto di `chi_basc` e' stato fatto DUE volte e la seconda ha ribaltato la prima. Dalla
semina dava *"0 nati in A contro 103 in B, olonomia netta x8.7"*; rifatto dal passo 192 -- dove la
mitosi e' gia' attiva -- dava **215 contro 260 (+21 %)**, `tw` **identici allo 0.4 %**, e olonomia
netta di **segno opposto fra le due finestre**. **Ho ritirato la conclusione forte** (`Z73`).

**L'unico effetto sopravvissuto a entrambe le finestre e' `-30 %` sulle coppie di Schwinger.**

E il limite che avevo dichiarato allora e' esattamente cio' che questo run toglie di mezzo: lo
snapshot di partenza era stato prodotto **con `chi_basc` ACCESO**, quindi il braccio B ereditava un
`perc_chi` gia' omogeneizzato (`Nm1 ~ 2580`). **L'A/B rifatto misurava la DINAMICA successiva, non
la CARICA.** Due run completi dalla semina misurano anche la carica.

### 1.2 Cosa NON so, e lo dico prima

- **non so se 3000 passi bastino.** Al `sep = 8` il sistema arrivava a `n ~ 9500` al 2700 e non
  aveva ancora smesso di crescere. A `sep = 4.0` cresce piu' in fretta (misurato sotto), quindi 3000
  passi vedranno una fase diversa -- **piu' avanzata, non necessariamente conclusa;**
- **non so se i due rami resteranno confrontabili fino in fondo.** Il sistema e' caotico: due
  traiettorie che divergono a `1e-16` danno numeri diversi anche a codice invariato (par.9). **Con
  UN seme per ramo, il nullo di un confronto NON e' zero** -- e questo run **non lo misura**. E'
  gia' scritto nel par.2.6 delle non-conclusioni;
- **non so se `chi_basc` faccia qualcosa di diverso a geometria connessa.** Tutti i numeri finora
  vengono da una scena a QUATTRO componenti separate (`Z65`). Questa e' la prima volta che
  `chi_basc` viene misurato su un sistema che interagisce davvero;
- **non so perche' il run a 6000 si sia piantato al 2700** con processo vivo al 99.6 % di CPU.
  **Resta non spiegato**, ed e' il rischio numero uno di questo run.

### 1.3 Cosa mi aspetto (e se mi sbaglio, questa sezione NON si riscrive)

- **mi aspetto che i due rami si somiglino di piu' di quanto diceva l'A/B corto.** La ragione e'
  che l'unico effetto sopravvissuto a due finestre e' il `-30 %` su Schwinger, e quello e' un
  effetto su un ramo raro, non sulla crescita totale;
- **mi aspetto che l'olonomia vada per conto suo.** L'ho gia' misurato: `|L|` e olonomia netta
  hanno cambiato rapporto (`x0.066` -> `x3.78`) fra due finestre dello stesso A/B. **Li riporto
  separati, e non costruisco una lettura che li tenga insieme;**
- **mi aspetto che `tw` NON sia confrontabile fra i rami**, per la ragione strutturale di `Z70`:
  con `chi_basc` acceso `tw` e' dentro l'anello di periodo 2 e `perc_chi` ne e' schiava; spento,
  l'anello si rompe. **Riporto `tw`, ma la conclusione non ci si appoggia;**
- **mi aspetto che `N(+1) - N(-1)` si muova in B SOLO per nascite**, ed e' la verifica diretta di
  `Z71`. Se si muove per altro, ho sbagliato a enumerare i punti di scrittura di `perc_chi`.

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO -- come ci arrivo, e cosa mi ferma

### 2.1 L'ordine, e cosa decide ciascun passo

| passo | cosa decide | cosa mi FERMA |
|---|---|---|
| **par.2 geometria alla semina** | se la scena e' quella chiesta | **componenti != 1, o archi massa-vuoto = 0 -> STOP** |
| **par.3 disco** | se i 50 snapshot ci stanno | **stima > spazio libero -> STOP e lo dico PRIMA** |
| **par.3 CPU** | se il parallelo conviene | nulla: e' una stima, non un cancello |
| **il braccio B** | come si spegne `chi_basc` senza toccare il simulatore | **il sigillo a default non byte-identico -> STOP** |
| **il lancio** | -- | **un ramo che si pianta -> riporto SUBITO, l'archivio parziale vale** |
| **le componenti a ogni snapshot** | se il run resta valido | **se si scollegano -> il run perde validita' e lo dico SUBITO** |

### 2.2 Come si ottiene il braccio B -- e perche' NON e' una modifica al simulatore

Il mandato dice **"nessuna modifica al simulatore"**. Il simulatore **non si tocca**: `CHI_BASC`
e' gia' `False` di DEFAULT (`:746`), ed e' **il DRIVER** che lo accende, cablato a `:109`.

La modifica e' quindi **nel driver**, nell'idioma che il driver gia' usa per `--serie=`,
`--csv-progresso=` e `--sep=`: **`--chi-basc=on|off` NOMINALE, default `on`**.

**Il default e' `on` e non `off`, ed e' una scelta, non una svista.** Nel giro precedente avevo
progettato default `off`, quando la decisione sembrava gia' presa. **Non lo e' piu': questo run
serve proprio a deciderla.** Finche' non e' decisa, il default deve riprodurre il comportamento
attuale **VERBATIM**, cosi' il comando di `Z49` resta riproducibile e il sigillo di byte-identita'
ha senso. Il default seguira' la decisione, non la anticipa.

**Il sigillo**, stessa forma di `_sigillo_sep_driver.py` (4/4):
- **C1** default -> **byte-identico** al driver di prima (bloccante);
- **C2** `--chi-basc=off` -> gli stati **DEVONO** differire (controllo positivo: un sigillo di sola
  byte-identita' passerebbe anche su codice morto, par.10.2);
- **C3** e differiscono **per la cosa giusta**: `CHI_BASC` letto **dal modulo** deve valere `1` a
  default e `0` con `off`. C2 dice che il flag cambia QUALCOSA, C3 che cambia LA COSA GIUSTA.

### 2.3 Dove si misurano le letture del par.4 -- **dagli snapshot, DOPO, e non dal driver**

**Decisione, e la ragione conta:** i contatori di nascita `_g_nati_mitosi`/`_g_nati_schwinger` sono
`int`, e il filtro di `salva_stato` (`:3063`) accetta `int` -> **finiscono nello snapshot**.
Verificato dal codice, non dedotto. Quindi **tutte** le letture del par.4 si possono misurare
**offline sui 25 snapshot per ramo**, e questo ha un vantaggio preciso:

> **NESSUNO script sul percorso in uso viene modificato mentre i run girano.**
> E' il presidio del par.9 sul driver toccato a meta' run del 19/9 -- applicato **prima** invece che
> constatato **dopo**.

Il progresso leggibile da fuori (par.3.3 del mandato) viene da `--csv-progresso=`, che il driver
**ha gia'** e che scrive `frame,passo,n,archi,coer_l,dil,elapsed_s,s_per_frame` con blob/seme/flag
in testa (P6). **Niente polling attivo** (par.5): i controlli si fanno a intervalli, non in un loop.

### 2.4 LE LETTURE, fissate QUI e prima di vedere i numeri

Agli **stessi passi** nei due rami, per ciascuno dei 25 snapshot:

1. **I NATI PER RAMO** -- `_g_nati_mitosi` (`:4294`, eredita UGUALE) contro `_g_nati_schwinger`
   (`:4415`, antinodo OPPOSTO), coi rispettivi contatori di EVENTI. **Il totale non basta:** un ramo
   che scatta di rado con molti nodi e uno che scatta spesso con pochi danno lo stesso totale.
2. **`N(+1)`, `N(-1)`, e la DIFFERENZA.** **In B la differenza deve muoversi SOLO per nascite** --
   e' la verifica diretta di `Z71`. Il valore atteso: ogni nato da `:4294` la sposta di `+-1`, ogni
   coppia da `:4415` la lascia INVARIATA.
3. **L'OLONOMIA NETTA FIRMATA** (`olonomia_media`), **e `berry_spin_media` accanto.**
   **Se divergono e' un reperto**, e va scritto come tale. Le assolute (`olonomia_max`,
   `olonomia_media_assoluta`, `olonomia_rms`) si riportano **accanto, non al posto**: non
   distinguono somma da cancellazione.
4. **`L` e il suo VERSO** (le tre componenti, non solo il modulo).
5. **`tw`, `twn`, `omega_s`, `coer_l`, `_deg`, `n`** agli stessi percentili (p25/p50/p75/p95).
   **`tw` si riporta ma non regge una conclusione** (`Z70`, par.1.3).
6. **LE COMPONENTI CONNESSE a OGNI snapshot** -- presidio di `Z65`. **Se si scollegano, il run
   perde validita' e va saputo SUBITO, non alla fine.**

### 2.5 Le quattro letture del par.5 del mandato, fissate ora

- **A resta fermo e B cresce, per 3000 passi** -> `chi_basc` **blocca** davvero: si toglie;
- **A parte piu' tardi ma parte** -> **non blocca: RITARDA.** Conclusione diversa, e va scritta cosi';
- **i due si somigliano** -> l'esito corto era **un artefatto della finestra** (e sarebbe il secondo
  artefatto di finestra dello stesso esperimento);
- **l'olonomia puo' andare per conto suo** -> si riporta **SEPARATA** dalle nascite.

### 2.6 Cosa questo run NON potra' dire, e si scrive PRIMA

- **UN SEME PER RAMO.** Il par.2.7 vieta conclusioni su un solo seme, e il par.9 dice che su questo
  sistema il nullo di un confronto fra rami **non e' zero**: e' la dispersione FRA SEMI, che qui
  **non e' misurata**. **Quindi nessuna differenza fra A e B si potra' dichiarare significativa.**
  Si potranno dichiarare **le differenze GRANDI e MONOTONE** -- e si dovra' dire che il termine di
  paragone manca.
- **NON e' un verdetto su `chi_basc`.** E' una misura. La decisione e' di Luca.
- **3000 passi non sono l'asintoto** (par.1.2).

---

## 3. TODO DEL NEXT STEP

- [x] par.2 geometria alla semina col simulatore attuale -> **comp = 1, mv = 97590, mm = 0. PASSA.**
- [x] par.3 disco misurato (**14 GB liberi**) e stima (**~1.95 GB per i due run**) -> **ci sta**
- [x] par.3 CPU misurata (**6 fisici / 12 logici**; singolo **19.574 s/frame**, parallelo
      **26.032 s/frame** -> `x1.330` di rallentamento, `x1.50` di resa) -> **~3.8-4.5 h**
- [ ] task history committato e pushato **PRIMA** del lavoro
- [ ] `--chi-basc=on|off` nel DRIVER, default `on`
- [ ] sigillo `_sigillo_chibasc_driver.py` (C1/C2/C3) -> **se C1 fallisce, STOP**
- [ ] commit + push del driver e del sigillo **PRIMA** del lancio (par.5)
- [ ] `R.apri()` per i due run in `doc/STATO_RUN.md`, commit e push **senza aspettare la fine**
- [ ] lancio dei due run in parallelo, cartelle `_ab_A` / `_ab_B`, **fuori da qualunque `finally`**
- [ ] controlli periodici che il progresso AVANZI + componenti connesse a ogni snapshot
- [ ] a fine run: le sei letture del par.2.4 -> CHECKPOINT a Luca
