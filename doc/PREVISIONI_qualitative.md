# PREVISIONI QUALITATIVE — bonifica 2026-09-17

**Scritte PRIMA del cablaggio** delle correzioni a cui si riferiscono, come ordina il mandato
(§5, §7.3). **Senza numeri, di proposito**: una previsione numerica su questo sistema richiede semi,
passi e barre d'errore, e questo giro **non prevede run di misura**.

> **A COSA SERVE UN DOCUMENTO DI PREVISIONI, e perche' e' scritto prima.**
> Non a indovinare. Serve a rendere **falsificabile** il cablaggio: se dopo la correzione si osserva
> il contrario di quanto scritto qui, **non si puo' riscrivere la previsione a posteriori**. E' lo
> stesso presidio gia' scritto in CLAUDE.md §9 contro le ipotesi che rigenerano la propria scusa:
> *«il criterio si scrive prima, e non si proroga»*.

---

## 0. UNA VOCE NON E' UNA PREVISIONE, E VA DETTO

**`d_arco` (§1 del mandato) e' gia' stato cablato** (commit `00adcd9`, sigillo V1 8/8) **prima che
questo documento esistesse**, perche' l'ordine del mandato (§7) mette la correzione al punto 2 e le
previsioni al punto 3. Quindi quanto segue su `d_arco` e' **descrizione a posteriori, non
previsione**, e **il suo valore predittivo e' nullo**. Le voci §2, ①, ②, ③, ⑤ sono invece
genuinamente **ex ante**: nessuna di esse e' cablata mentre scrivo.

---

## 1. `d_arco` — *(a posteriori, vedi §0)*

Il tempo-luce che entra in `tau_p_loc` **diventa quello dell'arco giusto**. **Non e' un
raffinamento:** prima non era una versione imprecisa della lunghezza d'arco, era **la lunghezza di
altri archi**, scelti dagli indici dei nodi. Misurato sui quattro semi: **il segno della sua
correlazione con la lunghezza vera non e' nemmeno concorde**.

**Conseguenza attesa sul comportamento:** ogni arco vede finalmente il **proprio** tempo di
attraversamento. Gli archi lunghi rilassano piu' lentamente degli archi corti — **relazione che
prima non esisteva affatto**, non che esisteva sbagliata.

---

## 2. `tau_p` CAUSALE — la plasticita' *(ex ante)*

```
t_luce    = d_arco / cs_arco
t_visco   = t_luce * (rho_arco / peq)
tau_p_loc = max(t_luce, t_visco)
```

- **La forma di riposo torna ad adattarsi.** Oggi `fattore_elasticita` ha mediana **~1e6**: il
  tempo plastico e' circa un milione di volte il tempo-luce dell'arco, cioe' `d0` **non si muove**.
  Sostituendo `median(I_nodi)` con `peq` il fattore cade di ordini di grandezza, e la plasticita'
  **smette di essere congelata**. *(Che sia gia' misurato in GATE D non rende questa una previsione
  numerica: qui si prevede il **verso**, non la quantita'.)*
- **Ma mai piu' in fretta del tempo-luce.** Il `max` non e' un clamp tarato: e' il confine oltre il
  quale la forma di riposo inseguirebbe la forma attuale **piu' in fretta di quanto un segnale
  attraversi l'arco**. Quindi **il mezzo resta elastico** — non diventa un fluido che dimentica.
- **Lo stress sopravvive.** Se `d0` inseguisse `d` istantaneamente, `q = d - d0` sarebbe sempre
  nullo e la sorgente elastica sparirebbe. Con un tempo di rilassamento finito e limitato dal basso,
  **la differenza fra forma attuale e forma di riposo persiste**: il sistema puo' portare memoria
  meccanica.
- **Il rilassamento e' piu' lento dove l'arco e' piu' denso del proprio sfondo.** E' la definizione
  di **viscoelasticita'**: nel denso il mezzo si comporta da solido (ricorda la forma), nel rarefatto
  da fluido (la dimentica). **Dove il vuoto e' cosi' profondo che non c'e' niente da rilassare, il
  vincolo causale prende il posto della viscoelasticita'** — ed e' li' che il `max` scatta.

**COSA FALSIFICHEREBBE QUESTA PREVISIONE:** se `d0` inseguisse `d` fino ad annullare lo stress, o se
il vincolo causale scattasse sul **corpo** del sistema invece che sulle sue **valli** — cioe' se la
frazione di archi in cui `t_luce > t_visco` fosse grande e la loro densita' **non** fosse
sistematicamente piu' bassa. **In quel caso non sarebbe una legge che dichiara il proprio dominio:
sarebbe un pavimento come gli altri, e A3b lo condannerebbe.** *(Il sigillo V5 guarda esattamente
questo.)*

---

## 3. ① `inerzia` — *(ex ante)*

`inerzia = (rho_sorgente / peq_nodo) * (d_nodo / cs_nodo)**2`

Oggi l'inerzia e' la densita' **nuda**, con un pavimento `1e-6` attivo sul **99.7 %** dei nodi: cioe'
per la quasi totalita' dei nodi **l'inerzia non e' una grandezza fisica, e' una costante**.

**Previsione:** la grandezza **torna a variare da nodo a nodo**, perche' il rapporto `rho/peq`
confronta il nodo col **proprio sfondo locale** invece che con una soglia assoluta, e il fattore
`(d/cs)^2` ha la dimensione di un tempo al quadrato — che e' cio' che un'inerzia deve avere.
Di conseguenza `omega = coppia/inerzia` **smette di essere dominato dalla regolarizzazione**.
**Non prevedo che il settore di spin si ordini**, e questo va detto chiaramente: e' gia' misurato
che `omega` e' un random walk smorzato, e cambiare l'ingresso **sposta il plateau, non lo abolisce**.

---

## 4. ② `spinta` — *(ex ante)*

`spinta = 0.02 * self.d0 * _rep` invece di `0.02 * median(self.d0) * _rep`

**Previsione:** la repulsione smette di essere **la stessa lunghezza per tutti** e diventa
**proporzionale alla scala locale dell'arco**. Un arco corto riceve una spinta piccola, uno lungo una
grande: oggi ricevono la stessa, indipendentemente dalla propria dimensione. Questo **toglie una
scorciatoia globale** (A2) e **toglie il punto fisso** della normalizzazione sulla mediana (A3).

---

## 5. ③ `_rep` — memoria *(ex ante)*

**Previsione:** il cricchetto si chiude. Oggi `rep` e' **istantaneo** e `d0 += spinta` e'
**irreversibile**: un processo che aggiunge senza togliere e senza memoria integra il rumore in
crescita monotona (A7). Dando a `_rep` uno **stato** con rilassamento su `tau_pp`, il contributo
**puo' anche decrescere**, e la grandezza **puo' conservare qualcosa** invece di accumulare soltanto.
**Non prevedo che il sistema smetta di espandersi:** prevedo che **quella particolare crescita
smetta di essere a senso unico per costruzione**.

---

## 6. ⑤ `spin_locale` — *(ex ante)*

**Nessuna previsione fisica: e' codice morto.** La funzione non e' mai chiamata (GATE C). La
rimozione dev'essere **esattamente inerte**, e il sigillo e' **assoluto**: `max|A-B| = 0.000e+00`
con shape **uguali** — la condizione che manca a un confronto vuoto, e che va verificata prima di
leggere lo zero (§9, *«`0.000e+00` puo' significare "nessun confronto"»*).

**Se la rimozione NON fosse inerte, la conclusione non sarebbe "ho rotto qualcosa": sarebbe che
GATE C aveva torto**, cioe' che una via di chiamata esiste e non e' stata trovata.

---

# ① `inerzia` — previsioni *(ex ante, 2026-09-17)*

**Scritte PRIMA di qualunque cablaggio, e il cablaggio NON e' avvenuto** (verifica preliminare
fallita, `doc/REFERTO_inerzia_transitorio.md`). **Restano valide per quando avverra'**: scriverle
adesso, prima che la via sia sbloccata, e' piu' forte che scriverle dopo.

`inerzia = (rho_sorgente / peq_nodo) * (d_nodo / cs_nodo)**2`

- **Il pavimento `1e-6` smette di essere il valore dominante.** Non perche' venga tolto — **resta** —
  ma perche' l'inerzia lo supera da sola. **E' la FIRMA che la diagnosi dimensionale era giusta:**
  se restasse dominante, la forma non avrebbe alzato l'inerzia e la causa sarebbe altrove.
- **`sigma = coppia/inerzia` CALA**, e con essa l'ampiezza di `omega`.
- **L'inerzia diventa PIU' GRANDE dove `cs` e' piu' basso**, cioe' **nei pozzi densi**: la materia
  compressa resiste di piu' alla rotazione. *(Segue da `(d/cs)^2`: `cs` piccolo → `T` grande.)*
- **Il lavoro sul `cs` relazionale arriva finalmente allo spin.** Oggi non ci arriva, ed e' misurato:
  `_fatt_cs` vale fino a **6.43**, ma l'inerzia resta `1e-6` **sul 100.00 % dei nodi**. Il fattore
  esiste e non serve a nulla.

**COSA NON PREVEDO, e va scritto adesso perche' non sia rivendicato dopo:** **non prevedo che il
settore di spin si ordini**, ne' che l'aliasing sia risolto. E' gia' stabilito che `omega` e' un
random walk smorzato: **cambiare l'ingresso sposta il plateau, non lo abolisce**. Che il plateau si
sposti abbastanza da uscire dall'aliasing **e' una domanda quantitativa**, e la risposta si scrive
**a bonifica completa, contro una predizione numerica scritta prima** — non qui.

**COSA LA FALSIFICHEREBBE:** se dopo il cablaggio il pavimento restasse dominante, **la forma non
avrebbe fatto il suo lavoro** e la diagnosi dimensionale andrebbe riaperta, non raffinata.

---

# ① `inerzia` — **seconda stesura, con A6** *(ex ante, 2026-09-17)*

**La prima stesura resta sopra e non si tocca.** Questa la integra col fatto nuovo: la cura del
blocco non e' una rete, e' **A6** — *l'inerzia si valuta sullo stato PRECEDENTE*.

- **Il `NaN` non raggiunge piu' la memoria persistente** — **e non perche' sia filtrato**, ma
  perche' l'inerzia **non guarda piu' uno stato non calibrato**. *(Filtrare sarebbe stata la quarta
  rete sopra lo stesso buco; diluire non funziona affatto, perche' `NaN` e' **assorbente**:
  `0.9*x + 0.1*NaN = NaN`. Diluire cura un valore **cattivo**, non un valore **assente**.)*
- **Il pavimento `1e-6` smette di essere il valore dominante** — resta, ma l'inerzia lo supera da
  sola. **E' la firma che la diagnosi dimensionale era giusta.**
- **`sigma = coppia/inerzia` CALA.**
- **L'inerzia diventa piu' grande dove `cs` e' piu' basso** — nei pozzi densi.
- **Il lavoro sul `cs` relazionale arriva finalmente allo spin.**

**E una previsione sul FALLBACK, che e' la parte falsificabile in piu':** il ramo del primo passo
(nessuno sfondo disponibile → contrasto neutro) **deve scattare solo nel transitorio e poi mai**.
**Se scattasse a regime, non sarebbe un fallback: sarebbe il comportamento principale, e A8 lo
condannerebbe.** *(Sigillo Y5.)*

**COSA NON PREVEDO, ripetuto perche' non sia rivendicato dopo:** **non prevedo che il settore di
spin si ordini**, ne' che l'aliasing sia risolto. `omega` e' un random walk smorzato: cambiare
l'ingresso **sposta il plateau, non lo abolisce**.

---

# `calcola_psi` TEMPO 2 — previsioni *(ex ante, 2026-09-17)*

Passare `w` ai due chiamanti **eseguiti** dentro `step` (`:3006`, `:3118`).

- **Il numero di ricalcoli dentro il passo va a ZERO**, e le letture diventano **coerenti `t`/`t+1`**
  — come il commento a `:2959` gia' prescrive e come oggi non accade.
- **Sull'EFFETTO NON HO UNA PREVISIONE, e lo scrivo prima.** Potrebbe **non cambiare nulla** (se i
  pesi ricalcolati coincidono con quelli di `step`) **oppure cambiare molto** (se non coincidono).
  **E' una MISURA — Q4 — non un'attesa.**
  > **E se non cambia nulla, NON e' un fallimento:** significa che **il difetto era teorico**, e la
  > correzione **resta giusta** perche' chiude un ramo il cui esito non era garantito. **Lo
  > registrero' come tale, e non forzero' una differenza.**
- **Il terzo punto (`:3037`) NON viene toccato:** e' l'`elif` sotto `REPULS_LEGGE`, **non eseguito**
  col default. **Il difetto li' resta LATENTE**, e la previsione e' che **nessun sigillo possa
  vederlo** — perche' quel ramo non gira.

**COSA FALSIFICHEREBBE LA CORREZIONE:** se `Q3` (forzando i chiamanti a non passare `w`) **non**
tornasse byte-identico, la modifica avrebbe toccato piu' del previsto. E se `Q6` trovasse `len(w)`
disallineato dagli archi in un punto, `w` non sarebbe valido li' — **misurato ora: topologia
invariata nel 100 % di 40 chiamate, su entrambi i punti.**

---

# ESPERIMENTO `SPIN_FEEDBACK` con `TAU_A = 2.0` — previsioni *(ex ante, 2026-09-17)*

**A/B a variabile singola:** il confronto e' contro il run gia' fatto `TAU_A = 2.0`, quindi **l'unica
differenza e' `SPIN_FEEDBACK`.**

**L'IPOTESI:** il **-32 % di nodi** osservato con `TAU_A = 2.0` dipende dal fatto che **lo spinore
matura in fretta ma NON RETROAGISCE** sulla geometria — un motore acceso con la trasmissione
staccata. Con la trasmissione attaccata, il sistema potrebbe reggere meglio.

- **Se l'ipotesi regge**, la perdita di nodi **si riduce in modo netto**.
- **Se cade**, la perdita **resta uguale**, e il candidato diventa **`Z10`**: `TAU_A` e' **anche** la
  vita media della memoria spinoriale, e a `2.0` quella memoria muore **25 volte piu' in fretta**.
  **Un numero per due leggi: una crescita e un decadimento.**
- **Se peggiora o diverge**, la trasmissione e' staccata **per una ragione che nessuno aveva
  scritto**, ed e' un reperto.

**SULL'AMPIEZZA NON HO UNA PREVISIONE, ed e' il punto che decide se l'esperimento vale:** se il
contributo del feedback fosse **trascurabile rispetto a `coppia`**, l'esperimento sarebbe **NULLO**,
e qualunque differenza osservata andrebbe attribuita ad altro. **E' la misura E4, non un'attesa.**

**COSA NON PREVEDO, e va scritto adesso:** **non prevedo che il sistema «stia bene».** Il run A
regge ma con `psi x91` e `d0 x17`; **nulla fa pensare che il feedback li riporti a posto**, e se
anche i nodi si stabilizzassero **quello resterebbe un altro sistema.**

**E UNA COSA CHE VALE A PRESCINDERE DALL'ESITO:** **`SPIN_FEEDBACK` NON HA UN SIGILLO** — nessuna
riduzione al limite, nessun controllo positivo. **Qualunque cosa esca, il passo successivo sarebbe
SIGILLARLO, non accenderlo.**


---

# CURA DEL DENOMINATORE DI `SPIN_FEEDBACK` — previsioni *(ex ante, 2026-09-17)*

**Scritte PRIMA di toccare il codice.** Cura: si tolgono i due denominatori nodali asimmetrici
(`/grado[ii]`, `/grado[jj]`) e **non si mette nulla al loro posto** — variante `nudo`, zero scelte.
Il difetto e le quattro varianti sono in `doc/REFERTO_denominatore.md` e nel commit `eaa402b`.

## Cosa mi aspetto, e con quale sicurezza

**CERTO — perché è algebra, non statistica:**
- **`G1`** `|sum(out)|/max|out|` passa da **mediana 1.112 / MAX 8.441** a **~1e-16**, su **ogni**
  invocazione. Se non ci arriva, **la cura è sbagliata**: si committa e ci si ferma.
- **`G5`** `+flusso` e `−flusso` esattamente opposti: banale una volta tolto il denominatore, ma va
  verificato **esplicitamente** perché è la proprietà che `G1` misura in forma aggregata.

**ATTESO, e già misurato su una variante in-process (un seme):**
- **`G3` controllo positivo:** coi gradi veri la forma nuova **deve** differire. Sui numeri di
  `eaa402b` differisce: `|out|` mediano `0.0400 → 0.0223`, `max|out|` `0.816 → 0.590`.
- **Il termine NON esplode.** È il contrario dell'intuizione «senza denominatore accumula cento
  volte»: misurato, è **più piccolo**. Ragione plausibile ma **non verificata**: `grado` è il grado
  **pesato** (somma dei `w`), non il conteggio, e dividere per un numero minore di uno **amplifica**.
  **Se questa spiegazione fosse giusta, il vecchio `/grado` non normalizzava affatto: amplificava.**
  Non la do per buona: è una previsione, e `G3` la mette alla prova.

**INCERTO, e lo dico prima invece di spiegarlo dopo:**
- **`G2` (riduzione al limite).** Forzando `grado[i] = grado[j] = g`, la vecchia forma dà `±f/g` e la
  nuova `±f`. **Non sono uguali: differiscono per il fattore `g`.** Quindi `G2` **NON può** essere
  una byte-identità come scritto nel mandato — sarebbe tale solo per `g = 1`.
  **Il limite giusto per `nudo` è `g = 1`**, e lo scriverò così. *(Per le varianti `media`/`linea`
  il limite del mandato avrebbe avuto senso; per `nudo` no. Lo dichiaro **prima** di girare il
  sigillo, non dopo averlo visto fallire.)*
- **`G4` (conservazione).** `sum(phivel)` dovrebbe conservarsi meglio, **ma non so di quanto e non
  lo predico**: le varianti **divergono** fra loro (n finale 548/564/539/543 su un seme), quindi il
  confronto di ampiezza **non ha barra**. Riporterò i numeri **senza interpretarli**.
- **`G6` (cucitura di fase).** **Non ho previsioni.** Nessuno ha mai misurato se `imag(ov)` sia
  continuo fra passi consecutivi. **Entrambi gli esiti sono informativi**, e quello negativo — salti
  di segno — sarebbe **il reperto più grosso di questo giro**, perché renderebbe il termine rumore
  di gauge. **Non tifo per nessuno dei due.**

## Cosa la cura **NON** risolve, e va detto adesso

- **Non restituisce al termine la proprietà che il docstring dichiara.** `out[k]` resta una **somma**
  su un numero di termini che cresce col grado. **Se sia un difetto NON È STATO MISURABILE**: il
  ~77 % dei nodi ha grado **esattamente 2** e le mediane per grado sono **non monotone**. Resta un
  fronte aperto, non una cosa risolta.
- **Non tocca gli altri tre punti con lo stesso schema** (`:2082`, `:2294`, `:3154`). Fronte nuovo.
- **Non promuove nulla:** `SPIN_FEEDBACK` resta **OFF di default**.
