# LA MEMORIA PER *TUTTI* I PUNTI FISSI, E LA MATRICE DAL CODICE

> **Il mandato:** l'aggiunta di Luca al mandato della strada `(d)`, *«da fare DOPO le
> misure di `C1`»* — e `C1` e' misurata (`2.091`, commit `56dd95b7`). Piu' la **correzione
> del guardiano** (errore `n.11`): la matrice delle dipendenze **non si prende dalla
> tabella**, si ricava **dal CODICE**.

> **E NON C'E' «LA STELLA POLARE» QUI, e lo dichiaro invece di ometterlo in silenzio:**
> `L-STELLA` chiede le cinque domande **a ogni commit che cambia la fisica**, e questo
> mandato dice **«nessun codice di fisica»**. Censimenti, una matrice e una voce:
> `leggi.yaml` non si tocca, e l'impronta resta `2e7f795d2a52fbe7`. **Se durante il lavoro
> mi accorgessi di dover toccare il passo, mi FERMO e lo scrivo:** sarebbe un altro
> mandato.

## 1. RAGIONAMENTO PRELIMINARE — *che cosa credo PRIMA di guardare*

**LA PREVISIONE CHE CONTA, e la scrivo per poterla sbagliare: credo che i punti fissi
siano `3`, non `2`** — e il mandato dice *«al minimo due»*, nominando `cs` al centro e i
pesi al punto medio.

| | il punto fisso che credo di trovare | dove credo che stia | acceso oggi? |
|---|---|---|---|
| `1` | `cs` al **CENTRO** del palindromo (la scelta `D2`) | `tick.cs_al_centro` | **SI'**, con `cs` dinamico |
| `2` | la **fase del vuoto** a punto medio implicito | `energia_pesata.applica` | **SI'** — *e il mandato non la nomina* |
| `3` | i **pesi** al punto medio del pezzo | `flussi_parziali.hop_phi_punto_medio` | **NO**, il ramo e' spento |

**E IL `2` DEL MANDATO CREDO CHE SIA UNA SOTTOSTIMA MIA, NON SUA:** il secondo che Luca
nomina e' **quello spento**, e quello che **gira davvero a ogni tick** — la fase del vuoto
— **non e' in elenco**. Se e' cosi', l'elenco a mano aveva **gia' saltato il piu'
importante**, ed e' esattamente il motivo per cui il mandato chiede di **contarlo con uno
script**.

**CHE COSA CREDO SUL COSTO** (e qui sono meno sicuro): che **`cs_al_centro` domini**,
perche' ogni suo giro **rifa' un palindromo intero**, mentre il giro della fase **rifa' un
solo pezzo**. Se e' vero, la sua quota dovrebbe stare **sopra il `90%`**.

**E CHE COSA *NON* SO, detto per nome:**

- **(a) la quota del costo:** non l'ho mai misurata, e **i contatori che ho non bastano** —
  `mot.giri_omega` e `mot.giri_peso` contano i **giri**, non il **tempo**. Un giro di
  `cs_al_centro` e un giro della fase **non costano uguale**, quindi la quota **non si
  deriva dai contatori**: va misurata.
- **(b) se il mio strumento AST vedra' le letture IMPLICITE.** `CAMM-SPOSTAMENTO` legge
  `cs` **attraverso `dtau_nodo`**, cioe' a **due salti di funzione**. Un AST che guarda il
  corpo del pezzo e si ferma li' **non lo vede** — e il mandato ha messo esattamente quel
  caso come **caso che deve riuscire**. **Credo che la prima versione del mio strumento lo
  manchi**, e che serva la **chiusura delle chiamate**.
- **(c) se le due dipendenze siano incrociate nello stesso istante.** Non lo so, ed e' la
  domanda che decide se la leapfrog e' disponibile. Non ho una previsione onesta: ho un
  **sospetto**, cioe' che **lo siano**, perche' il tempo proprio entra in **ogni** pezzo,
  materia compresa.
- **(d) come si erediterebbe `cs` alla MITOSI.** Non ne ho idea, e non e' una cosa che si
  inventa in un referto: e' **una scelta di fisica**, e **torna a Luca**.

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *i passi, e cosa FERMA ciascuno*

| | il passo | che cosa DECIDE | che cosa mi FERMA |
|---|---|---|---|
| `A` | `csv/_censimento_punti_fissi.py`: conta i punti fissi **con l'AST** (cicli con condizione di convergenza, tetti di giri, soglie) | **quanti** sono, e dove | **se ne trova `< 3`**: lo strumento e' cieco su uno che **so** che c'e' |
| `B` | il **COSTO misurato** (non dedotto dai contatori): tick col punto fisso contro tick senza, piu' i giri | la **quota** di ciascuno | se la quota **non torna** col numero di giri: c'e' un costo che non ho capito |
| `C` | `csv/_matrice_dipendenze.py`: per ognuno dei `14` pezzi che cosa **LEGGE** e che cosa **SCRIVE**, con la **chiusura delle chiamate** | se le dipendenze sono **INCROCIATE** | **se non trova che `CAMM-SPOSTAMENTO` legge `cs`**: lo strumento e' **cieco**, e il suo numero non vale niente |
| `D` | il confronto con `ambito`: quante dipendenze la tabella **non** dichiara | l'**osservazione** del punto `3)` della correzione | — |
| `E` | la **voce** e la **mappa**: la scelta *una sola* («lo stato contiene il passato?») e l'ereditarieta' alla mitosi | **niente**: e' una **domanda per Luca** | **se mi trovo a SCEGLIERE**: mi fermo e la scrivo come domanda |

**LE LETTURE SI FISSANO QUI, PRIMA DI VEDERE I NUMERI:**

1. **il caso che DEVE riuscire e' «`CAMM-SPOSTAMENTO` legge `cs`»** — e lo scrivo come
   **un'asserzione dentro lo strumento**, cosi' che **lo strumento cieco FALLISCA** invece
   di dare un numero bello.
2. **e aggiungo un caso che DEVE FALLIRE, che il mandato non chiede:** un pezzo che **non**
   scrive `phi_h` non deve risultare scrittore di `phi_h`. Un grafo in cui tutto dipende da
   tutto e' un **falso uno**, e senza questo caso non me ne accorgerei.
3. **«incrociate» si decide su una definizione scritta PRIMA:** le dipendenze sono
   incrociate **se** esiste un pezzo che scrive `Lambda` e legge la materia **E** un pezzo
   che scrive la materia e legge `cs`, **e i due stanno nello stesso palindromo**. Non «a
   occhio sulla matrice».

**ANNOTAZIONE DEL 2026-10-18 SERA, PRIMA DEI NUMERI (precisazione del guardiano):** la definizione di 'incrociate' del punto 3 si estende all'AUTO-DIPENDENZA. Un solo pezzo che scrive Lambda e legge cs (come CAMM-SPOSTAMENTO-VUOTO) basta a rendere le dipendenze incrociate: anche la variante sfalsata alla leapfrog diventerebbe implicita. La matrice riporta quindi, per ogni pezzo, anche le coppie (scrive X, legge una funzione di X) dentro lo stesso pezzo.

**ANNOTAZIONE DEL 2026-10-19, PRIMA DEI NUMERI NUOVI (decisione di Luca delle 11:14, strada (a), con la precisazione del guardiano): IL CRITERIO NUOVO DEL CONTROLLO DEL PASSO `B`.** Il controllo di `ec0d5f7f` e' caduto in due versi (un braccio che non torna, e il caso che deve fallire che torna con una soglia di `327` ms); il criterio si cambia **qui, prima della corsa nuova**, e **non** guardando i numeri di quella.
- **La statistica e' ROBUSTA.** Per ogni braccio: **`6` ripetizioni**, di cui **la prima di riscaldamento, SCARTATA**; sulle `5` restanti la **MEDIANA**, e la dispersione e' la **MAD scalata**, `1.4826 * MAD`. La soglia e' **`3` volte quella dispersione**, combinata fra misura e previsto come prima: `3 sqrt(s_misura^2 + s_previsto^2)`.
- **UN BRACCIO E' INFORMATIVO solo se la soglia e' MINORE della distanza** fra il previsto giusto (`giri * c(giro)`) e il previsto del caso che deve fallire (il conto di `C5`). Altrimenti e' **NON INFORMATIVO**: **si conta a parte e non vale MAI come «torna».**
- **IL VERDETTO:** «torna» se **tutti i bracci informativi tornano** e **i casi che devono fallire falliscono**. Se per un punto fisso, in una taglia, **nessun braccio e' informativo**, il verdetto e' **NON DECIDIBILE**, non PASSA.
- **IL REFERTO** stampa per ogni braccio `r = misura/previsto`, la soglia, e l'etichetta **informativo / non informativo**.
- **IL COLLAUDO DEL CRITERIO** resta sui due casi noti (uno che torna, uno che non torna), e se ne aggiunge un **terzo: un caso NON INFORMATIVO** (soglia larga apposta), che deve uscire **etichettato come tale, e non come «torna».**

**ANNOTAZIONE DEL 2026-10-19 (decisione di Luca delle 12:36): IL PASSO `B` SI CHIUDE CON LE QUOTE.** *(Si annota, non si riscrive.)*
- **IL RISULTATO DEL PASSO `B` SONO LE QUOTE**, che non dipendono dal controllo *(referto `costo_punti_fissi.txt`, `8b2bdb16`)*: **`cs_al_centro` `76`-`92%` del tick**, **`Omega` `69`-`84%`**, di cui **`52`-`77%` dentro i giri di `cs`**. **Il costo del tick e' il punto fisso di `Omega` annidato in quello di `cs`.** La previsione del par.`1` *(«`cs_al_centro` sopra il `90%`»)* **vale in `3` casi su `13`**.
- **IL MODELLO `giri * c(giro)` NON TORNA in `12` bracci su `26`** *(`r` fra `0.92` e `1.26`, piu' i due anomali a `32` / `Lambda_c = 2.4`: `0.663` e `0.502`)*. E' registrato come **NON SPIEGATO e NON BLOCCANTE**: lo scarto **non puo' cambiare la conclusione sulle quote.** Le due ipotesi *(un costo fisso per chiamata; `c(giro)` misurato solo sullo stato iniziale)* **restano scritte come ipotesi**, da riprendere **solo se un giorno servira' il costo di un singolo giro**.

## 3. TODO DEL NEXT STEP — *operativo*

1. `csv/_censimento_punti_fissi.py`, con il caso che deve riuscire (`>= 3`).
2. la misura del **COSTO**: quota per punto fisso, **due taglie**.
3. `csv/_matrice_dipendenze.py`, con la **chiusura delle chiamate**, il caso che deve
   riuscire e quello che deve fallire.
4. il confronto con `ambito`, **contato**.
5. la **voce** nuova: i `3` punti fissi, l'ereditarieta' alla mitosi, e la scelta che torna
   a Luca.
6. la **mappa**: la sezione della memoria corretta col numero vero.
7. il **referto**, dal blob committato, e la **relazione**.
