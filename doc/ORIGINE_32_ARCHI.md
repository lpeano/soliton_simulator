# DA DOVE NASCE LA LUNGHEZZA DI `32` ARCHI DELL'INSTABILITA' DI `S1`

> **Mandato di Luca del `2026-10-22` alle `17:42`**; task history `doc/TASK_HISTORY/2026-10-22_origine_32_archi.md`. ### **SU CARTA:
> nessuna corsa nuova, nessuna scelta.** ### **Ogni numero esce da `python csv/_origine_32_archi.py`** *(solo i `jsonl` committati;
> referto `doc/referti_l2/origine_32_archi.txt`)*, ### **o e' citato col suo commit.** ### ⚠ **I conti a mano sono DICHIARATI.**

---

## 1. IL CONTESTO

- ### **`S1` cresce a `0.0057` / `0.0058`, col massimo a `k = 0.0625 pi`, fisso in archi a lato `32` e `64`** *(`cb846b2a`)*; ### **la
  crescita e' la stessa nel tempo fisico.** ### **Quindi, raffinando, l'artefatto si sposta a scale fisiche piu' corte con lo stesso
  ritmo: una catastrofe ultravioletta discreta.**
- ### **LE DUE LETTURE DI LUCA, alla lettera** *(dal mandato)*:
  - ### **`(A)`** «l'arco del simulatore e' un arco dell'automa (Planck): `32` archi sarebbero fisica»;
  - ### **`(B)`** «l'arco e' un campionamento grossolano dell'automa iperfine (la visione di Luca del `2026-10-20`): una scala fissa in
    archi e' un artefatto».
- ### **Lettura di lavoro: `(B)`.** ### **La decisione fra `(A)` e `(B)` e' di Luca** *(la domanda aperta sotto `L1`)*.

## 2. IL MECCANISMO *(dai dati committati)*

### 2.1 La dispersione della camminata a onde lunghe

| | lato `32` *(`dtau 0.125`)* | lato `64` *(`dtau 0.0625`)* |
|---|---|---|
| ### **`c = v_g(1)/k(1)`** *(i rami dispersivi, mediana)* | ### **`0.3894`** | ### **`0.3882`** |
| `v_g(2)/v_g(1)` *(una parabola: `2`)* | `1.975` | `1.994` |
| `v_g(3)/v_g(1)` *(una parabola: `3`)* | `2.900` | `2.976` |

*(da `v_gruppo_m0` di `d0_risonanza_bis` e `d0_risonanza_64`; `c` in archi^2 per unita' di tempo proprio)*

- ### **A onde lunghe i rami dispersivi sono PARABOLICI:** `omega ~ (1/2) c k^2` *(rami «massivi»: `v_g -> 0` a `k = 0`)*.
- ### **A `k = 0.0625 pi` la camminata e' nel suo CONTINUO** *(lo scarto dalla parabola e' di poco piu' dell'`1%` a lato `32`)*: ### **i
  `32` archi NON vengono da un errore di discretizzazione della dispersione.**
- ### ⭐ **`c` e' LA STESSA in unita' d'arco alle due taglie** *(rapporto `0.997`)*: ### **la regola di scala** *(lato `x2`, `dtau /2`)* ### **lascia
  invariata la curvatura in archi**, ### **cioe' la curvatura FISICA cala come `a^2`.**

### 2.2 Il modello minimo, DICHIARATO come lettura

### **L'instabilita' modulazionale di una parabola** *(conto noto, riportato)*: ### **il massimo dove `(1/2) c k^2 = gamma`**, cioe' ###
**`k_max = sqrt(2 gamma / c)`.** ### **Contro i dati** *(la tabella intera nel referto)*:

| | `gamma` | `k` misurato *(pi)* | `k` previsto *(pi)* | scarto *(passi di griglia)* |
|---|---|---|---|---|
| `S1` `x 0.1` lato `32` | `0.00570` | `0.0625` | `0.0544` | `+0.13` |
| `S1` `x 0.1` lato `64` | `0.00576` | `0.0625` | `0.0548` | `+0.25` |
| `S1` `x 0.3` | `0.10500` | `0.2500` | `0.2337` | `+0.26` |
| `S1` `x 1` | `0.65291` | `0.6250` | `0.5829` | `+0.67` |
| `S3` `x 0.1` *(oggi)* | `0.40177` | `0.5000` | `0.4572` | `+0.68` |
| `S4` `x 0.1` lato `32` | `0.29705` | `0.4375` | `0.3932` | `+0.71` |
| `S4` `x 1` | `1.22888` | `1.0000` | `0.7997` | `+3.21` |

- ### **`12` casi su `18` entro `1` passo di griglia** *(tutti quelli di `S1`; `S2`, `S3`, `S4` a `x <= 0.1`)*. ### **Cade dove deve:** ### **a
  `gamma` grande** *(`S4` a `x >= 0.3`: la dispersione li' non e' piu' parabolica)* ### **e sul modo alternato** *(`S2`, `S3` a `x 1e-4`, a
  `(pi, pi)`: un'altra famiglia)*.
- ### **IL PERCHE' I `32` ARCHI:** per `S1` a `x 0.1` il modello da' ### **`k = 0.0545 pi`**, ### **cioe' una lunghezza d'onda di `~37`
  archi**, ### **che la griglia mette al punto piu' vicino: `0.0625 pi`, `32` archi, a tutte e due le taglie.**
- ### ⭐ **E PERCHE' E' NECESSARIAMENTE FISSA IN ARCHI** *(il criterio del mandato)*: ### **`L = 2 pi / k_max = 2 pi sqrt(c / (2 gamma))`**
  ### **e' un rapporto fra `c`** *(invariante in archi, sez. `2.1`)* ### **e `gamma`** *(invariante nel tempo proprio, `cb846b2a`)*: ### **solo
  grandezze in archi e in tempo proprio, invarianti sotto la regola di scala** -> ### **fissa in archi.**
- ### **UNA CORREZIONE A UN MIO DOCUMENTO** *(`doc/S3_RIPENSATA.md`, sez. `3.1`)*: ### **li' il modello minimo era «smentito» perche' la
  posizione non seguiva `sqrt(nu_S3)`**. ### **L'errore era mettere `gamma = nu_S3`:** ### **la relazione che regge e' fra la POSIZIONE e il
  `gamma` MISURATO** *(`k = sqrt(2 gamma/c)`)*, ### **e per `S3` a `x 0.1` e' entro `0.68` passi.** ### **Quel che resta smentito e' solo
  «`gamma` proporzionale a `nu`».**
- ### **CHE COSA LA SMENTIREBBE:** ### **un caso con `gamma` piccolo** *(regime parabolico)* ### **e il massimo lontano da `sqrt(2 gamma/c)`**
  *(nei dati non c'e')*; ### **una `c` che cambia raffinando** *(non cambia: `0.997`)*; ### **un modo con `gamma` piccolo che cresce su un
  ramo NON parabolico** *(`S-E`, `642dee6f`, ha trovato il modo misto fra rami: da guardare per `S1`)*.

## 3. LE STRADE PER ELIMINARLO NELLA LETTURA `(B)` *(schede, nessuna scelta)*

### `O-1` — **IL MIGLIORAMENTO DELLA CAMMINATA A ONDE LUNGHE** *(alla Symanzik)*
- **Definizione:** un operatore il cui scarto dal continuo cala piu' in fretta raffinando *(termini d'arco a raggio `2` che cancellano
  l'errore di ordine `k^4`)*.
- **Le cinque domande:** `A14` ### **raggio `2`**, locale; ### **aggiunge una legge e dei coefficienti** *(derivabili, alla Symanzik:
  non tarati)*; tocca la camminata, non `rho`; ### **non cambia il fenomeno, cambia la sua precisione.**
- ### **LA PROVA CHE LA CONFERMEREBBE:** il `k` del massimo cambia col miglioramento. ### **PREVISIONE dalla sez. `2.1`: NON cambia** --
  ### **a `k = 0.0625 pi` la dispersione e' gia' nel continuo** *(lo scarto `~1%`)*: ### **i `32` archi non sono errore di
  discretizzazione.** ### **NON TOCCA L'ARTEFATTO.**
- **Il costo:** una legge nuova e il suo collaudo; giorni.

### `O-2` — **UN TAGLIO DERIVATO DALLA QUANTIZZAZIONE DELL'OLONOMIA** *(`[[MITOSI-QUANTO-OLONOMIA]]`)*
- **Definizione:** ### **un quanto di olonomia sul ciclo piu' corto** *(il triangolo, `PROGETTO_TRIANGOLI` sez. `e`)* ### **che fissa
  una lunghezza MINIMA FISICA**: sotto di lei, nessun modo.
- **Le cinque domande:** `A14` ### **per ciclo** *(raggio `1`)*; ### **un numero: il quanto, DA DERIVARE** *(la voce)*; non tocca `rho`; ###
  **e' un taglio ULTRAVIOLETTO.**
- ### **LA PROVA, e il suo limite:** ### **il modo dei `32` archi e' un'onda LUNGA**: ### **a lato `32` e `64` un taglio UV non lo tocca.** ###
  **Ma raffinando ancora, la sua lunghezza FISICA cala come `a`** *(fissa in archi)*: ### **sotto la lunghezza del taglio, il taglio lo
  spegne.** ### **E' la sola strada che, in `(B)`, LIMITA la catastrofe**, ### **ma non a lato `32`-`64`.**
- **Il costo:** la derivazione del quanto *(aperta)*; poi una corsa a una taglia dove `32 a` scende sotto il taglio.

### `O-3` — **LA REGOLA DI SCALA CHE TIENE FISSA LA DISPERSIONE FISICA** *(STRADA MIA, dichiarata)*
- **Definizione:** ### **raffinando, `c` in archi cresce come `1/a^2`** *(la curvatura fisica resta fissa)*, ### **invece di restare
  `0.39`.** Con `gamma` fisso nel tempo, ### **`L` in archi raddoppia a ogni raffinamento: fissa in unita' FISICHE.**
- **Le cinque domande:** ### ⛔ **e' un cambio della REGOLA DI SCALA**, che e' ### **una decisione di Luca**; ### **chiede di dire QUALE
  grandezza fisica resta fissa** *(una scala esterna)*; il cono *(`s <= 1`)* va riverificato.
- ### **LA PROVA:** a lato `64` con la regola nuova, ### **il massimo di `S1` a `k` dimezzato** *(lettura `(b)` di `cb846b2a`)*.
- **Il costo:** la decisione; poi le corse di `cb846b2a` rifatte.

### `O-4` — **NESSUNA STRADA DENTRO `(B)` SENZA UNA SCALA ESTERNA** *(la sezione onesta, sotto)*

## 4. LA SEZIONE ONESTA: SI PUO' ELIMINARE, IN QUESTO TIPO DI MODELLO?

- ### **NIELSEN-NINOMIYA NON E' L'ARGOMENTO:** ### **riguarda i DOPPIONI dei fermioni chirali** *(i modi al bordo della zona che un reticolo
  locale, hermitiano e invariante per traslazione non puo' togliere)*. ### **Qui il suo cugino c'e', ed e' altrove:** ### **il modo
  ALTERNATO `(pi, pi)` del quadrato** *(che i triangoli tolgono: `bb0ef057`, `56608e8a`)*. ### **Il modo dei `32` archi e' a onda LUNGA**: ###
  **non e' un doppione.**
- ### ⭐ **L'ARGOMENTO CHE C'E', ed e' piu' semplice** *(conto di dimensioni, MIO)*: ### **il modello non ha costanti** *(`A1`: «la legge,
  non il numero»; `S3` e' omogenea, la scala e' relazionale)*; ### **l'unica lunghezza e' l'ARCO, l'unico tempo e' il TICK** *(e il tempo
  proprio, che ne discende)*. ### **Allora ogni lunghezza EMERGENTE e' un numero puro per l'arco**, ### **funzione dei soli rapporti
  adimensionali per arco e per tick.** ### **Una regola di raffinamento che tiene fissi quei rapporti** *(come quella di oggi: `c` in archi
  `0.997`, `gamma` nel tempo)* ### **tiene fissa in archi OGNI lunghezza emergente -- NECESSARIAMENTE.**
- ### **CHE COSA SIGNIFICA PER `(A)` E `(B)`:**
  - ### **in `(A)`** *(l'arco e' l'arco dell'automa)* ### **una lunghezza in archi E' fisica**: ### **nessun artefatto da togliere.**
  - ### **in `(B)`** *(l'arco campiona l'automa iperfine)* ### **NESSUNA lunghezza emergente puo' essere fisica senza una SCALA ESTERNA** --
    ### **la lunghezza dell'automa iperfine in archi del simulatore** *(cioe' come `c`, `gamma` e ogni rapporto devono cambiare raffinando:
    la strada `O-3`)*, ### **o un quanto fisico** *(la strada `O-2`)*. ### **Senza, `(B)` chiama artefatto OGNI scala che il modello
    produce, per costruzione.**
- ### **QUINDI la scelta fra `(A)` e `(B)` e' anche la scelta se la teoria ha una scala esterna all'arco.** ### **Non la faccio.**

## 5. LA SINTESI

- ### **I `32` archi sono la lunghezza dell'instabilita' modulazionale `2 pi sqrt(c/(2 gamma))`** *(`12` casi su `18` entro un passo)*, ###
  **con la camminata NEL CONTINUO a quella scala.**
- ### **E' fissa in archi perche' `c` e `gamma` lo sono sotto la regola di scala di oggi**; ### **non e' un errore di discretizzazione**
  *(Symanzik non la tocca)*.
- ### **In `(B)` si toglie solo con una scala esterna** *(`O-2`, `O-3`)*; ### **in `(A)` non c'e' niente da togliere.**

## 6. LE DOMANDE PER LUCA *(una alla volta, nella relazione)*

1. ### **La regola di scala:** si tiene *(allora ogni lunghezza emergente e' in archi, e `(B)` la chiama artefatto per costruzione)*, ###
   **o si cambia in una che tenga fissa una grandezza FISICA** *(`O-3`: una scala esterna, da derivare)*?
2. *(dopo)* ### **Il quanto di olonomia** *(`O-2`)*: si apre la sua derivazione?
3. *(dopo)* ### **La decisione fra `(A)` e `(B)`.**
