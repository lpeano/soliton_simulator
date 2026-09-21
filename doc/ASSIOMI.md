# ASSIOMI — vincoli sulla forma delle leggi

**Stato: BOZZA, non ancora passata al vaglio.** Nessuno di questi e' derivato da un principio piu'
alto. **Non sono generativi** (gli assiomi di Peano lo sono: cinque enunciati da cui l'aritmetica
discende): **questi sono RESTRITTIVI** — dicono cosa una legge **non puo'** essere. **Finche' non
esiste l'azione unica da cui le leggi si derivano, questo e' un CODICE DEONTOLOGICO, non un sistema
assiomatico.** *(Ed e' cio' che sta trovando i difetti: senza, l'azione unica verrebbe costruita su
fondamenta incoerenti.)*

## A1 — LA LEGGE, NON IL NUMERO
Una grandezza dinamica si esprime come **relazione fra grandezze di stato**, mai come costante
scelta. Se una costante serve, dev'essere **derivata** da grandezze gia' presenti. **Se va scelta,
la legge non e' quella giusta.**
*Perche':* un numero resta fermo mentre il sistema cambia; una relazione lo segue. E ogni numero
scelto e' un grado di liberta' che **assorbe l'errore** e rende la teoria non falsificabile.
*Casi:* `GAMMA = 0.05` in `cs_floor` (implicava una densita' critica `I = 400`; sostituito con `Lam`:
**fattore 1300**) · il muro `0.05` su `d0` (→ `PAV_COM`) · il pavimento `1e-6` sull'inerzia · la
soglia `0.15` di un criterio di sigillo, **inventata e poi derivata dal nullo** · `ELAST_C = 100`.
*Falsificazione:* esibire una legge del sistema che funziona **e** richiede una costante non
derivabile.
**⚠ A1 vieta i NUMERI SCELTI, non i VINCOLI DERIVATI.** Un limite posto **esattamente al confine
fisico** (causale, dimensionale, di conservazione) **non e' una taratura**: e' la legge che dichiara
il proprio dominio. La domanda che distingue: **«questo valore si puo' spostare?»** Se si' ed e'
stato scelto → manopola. **Se e' l'unico valore possibile perche' oltre c'e' una violazione → legge.**

## A2 — NESSUNA SCORCIATOIA GLOBALE
Una grandezza **locale** non puo' dipendere da una **statistica dell'intero sistema**. La scala di
riferimento va costruita da un **intorno raggiungibile**.
*Perche':* in un modello relazionale una media globale e' informazione che nessun nodo possiede.
**E' la Legge I gia' scritta nel codice** (`:265`).
*Casi:* `median(rho)` in `ZETA_LOC` · `dens_rif` in `_tau` · `median(d0)` in `spinta` e `_floor_d0` ·
`median(I_nodi)` in `fattore_elasticita`.
**TENSIONE APERTA, DICHIARATA:** `Lam = mean(I)` **e' globale**, ed e' stato accettato in `cs_floor`
come *«da globale e arbitraria a globale e derivata»*. **A2 e' quindi violato da una correzione che
ha funzionato.** Va risolto: **o A2 ammette le medie globali DERIVATE, o `cs_floor` va rifatto con
`peq`.** Non si possono tenere entrambe.
**ECCEZIONE VERIFICATA:** le grandezze che **sono globali per costruzione** (il termostato
Nose-Hoover: `T_target`, `xi_termo`, `E_cin`) **non ricadono sotto A2** — un termostato e' per
definizione un accoppiamento a un bagno globale.

## A3 — NIENTE SI NORMALIZZA SUL PROPRIO INSIEME
Non si normalizza una grandezza su una **statistica di POSIZIONE del proprio insieme** (mediana,
media dei primi vicini): il centro diventa **1 per identita'**, e il centro e' dove sta meta' dei
nodi. **La grandezza non puo' variare dove sta la maggioranza.**
*Distinzione misurata:* su **coda pesante** media e mediana **non coincidono** — `I/Lam` ha mediana
**3.2e-4** e **funziona**; `I/median(I)` vale **1.000** e non funziona. **La media resta una scala
ESTERNA al nodo tipico; la mediana E' il nodo tipico.**
**⚠ E IL CONTRARIO E' ALTRETTANTO GRAVE — l'errore di POPOLAZIONE.** `rho_arco` (per ARCO) diviso
`median(I_nodi)` (per NODO) **non da' 1**: da' **8830**, perche' gli archi sovracampionano il denso.
**Un rapporto ha senso solo se numeratore e denominatore vivono sulla STESSA popolazione.**
*Corollario A3c — **A3 VALE ANCHE PER I CRITERI, non solo per la fisica** (2026-09-17):*
**prima di confrontare due numeri, verificare che vivano sulla STESSA POPOLAZIONE e nella STESSA
UNITA'.** **Un RAPPORTO non si confronta con un MASSIMO; una MEDIA DI RAPPORTI non si confronta con
un RAPPORTO DI MEDIE; una grandezza per ARCO non si confronta con una per NODO.**
*Tre casi reali in due giorni:* la **media delle mediane per seme** dava **19** contro i **~4089**
della popolazione unita · `rho_arco` (per ARCO) diviso `median(I_nodi)` (per NODO) dava **8830**,
non 1 · e un **rapporto massimo** (115) stampato accanto a **due massimi presi in passi diversi**,
come se fosse il loro quoziente. **Nessuno dei tre era un errore di fisica: erano errori di
CONFRONTO, e producono diagnosi sbagliate con numeri giusti.**

*Corollario A3b — i PAVIMENTI sono la stessa cosa dall'altro lato:* un clamp tarato **sopra** i
valori tipici congela cio' che dovrebbe proteggere (`1e-6` sull'inerzia: **99.7 %**). **Un ramo di
fallback che scatta quasi sempre non e' un fallback: e' il comportamento principale.**

*I CASI MISURATI, ognuno col suo numero* — **senza la tabella un assioma torna a essere
un'opinione**, ed e' la ragione per cui **A8** ne ha trovati di piu': porta i suoi numeri.

| caso | il numero | che cosa e' andato storto |
|---|---|---|
| `rho_arco / median(I_nodi)` | **8830**, non 1 | grandezza per **ARCO** su statistica per **NODO**: gli archi sovracampionano il denso |
| media-di-mediane contro popolazione unita | **19** contro **4089** | la media delle mediane per seme **non e'** la mediana della popolazione |
| **A3c** — un RAPPORTO confrontato con un MASSIMO | (115, accanto a due massimi di **passi diversi**) | grandezze **non commensurabili**, stampate come se fossero un quoziente |
| l'estensivita' confusa con l'eta' | — | grado ed `eta` **correlati per costruzione**: il confronto non poteva dire niente |
| **la mediana in `ritmo()`** | **`median(x) = 1` per IDENTITA'** | **il gauge del TEMPO e' pinnato**: il nodo tipico non puo' muoversi, e su di lui non si misura nulla |

> **L'ultimo caso e' il piu' grave dei cinque, perche' non produce un numero sbagliato: produce un
> numero GIUSTO che non significa niente.** *(Voci `Z9`, `Z38` del registro.)*

## A4 — STRATIFICAZIONE CAUSALE
**Cio' che DEFINISCE la struttura causale non puo' evolvere DENTRO di essa**: avanza nel tempo di
**coordinata** (il contatore di stati), non in tempo proprio.
*Perche':* sarebbe circolare. **E' la teoria dei tipi applicata alla fisica**, ed e' la stessa
stratificazione che in relativita' generale separa **tempo coordinata** (etichetta) e **tempo
proprio** (fisico).
*Conseguenza verificabile:* **`cs` e' l'unico punto dove `DT` nudo e' legittimo. Ovunque altro serve
`dt_n = DT*r`.** *(Precedente: lo Strato 1 aveva esattamente quel bug, e solo S7 l'ha beccato.)*
*Conseguenza gia' verificata:* `cs` **non deve accumulare** — si adegua in **un tick**, che e' il
comportamento attuale. **A4 non chiede una modifica: fornisce la giustificazione che mancava.**

## A5 — CAUSALITA' DELLA MEDIAZIONE
**Ogni grandezza che media un'interazione fra punti distanti deve propagare a velocita' finita.**
Una funzione istantanea di materia lontana viola il cono di luce.
*Livelli ammissibili:* **0** nessuna memoria — solo per i **VINCOLI** (`rho = |psi|^2`, le norme:
sono definizioni); **1** rilassamento esponenziale — **non propaga, diffonde**: ammesso **solo se
`tau` e' gia' un tempo causale** (`d/cs`); **2** second'ordine (onda) — **l'unico che propaga**;
**3** kernel non-Markoviano — solo se cio' che si e' integrato via **non e' veloce**.
*Criterio misurabile:* `tau_veloce` (autocorrelazione della grandezza trattata come istantanea)
contro `tau_lento` (la dinamica che la usa). `<<` → l'istantaneo basta; `~` → almeno l'esponenziale;
`>~` → kernel lungo.
**TENSIONE con A4:** `cs` media un'interazione a distanza e non propaga — **A5 lo condannerebbe, A4
lo assolve.** A4 ha precedenza perche' `cs` **e'** cio' che definisce la velocita'. **Ma la
precedenza va motivata, non assunta.**

## A6 — INERZIA (TEOREMA, non assioma)
**Nessuna funzione istantanea di X puo' agire dinamicamente su X.**
**DIMOSTRATO**, non postulato (`<psi_i|N|psi_j> = 2<psi_i|psi_j>`, residuo **1.57e-15**). Una
connessione costruita dagli stessi stati che trasporta e' **uno specchio**. *(Sta qui perche' e' il
piu' usato, ma e' di natura diversa dagli altri.)*

**⚠ IL COLLEGAMENTO CHE MANCAVA (2026-09-17): A6 SI VIOLA ANCHE SENZA TOCCARE LA FORMULA.**
A6 dice che una funzione **istantanea** di X non puo' agire su X. **Ma la violazione puo' stare
nell'ORDINE DELLE CHIAMATE invece che nella forma della legge — e allora NON SI VEDE LEGGENDO LA
FORMULA.** **Quattro casi misurati** (`doc/RAMIFICAZIONI.md`, *«il tempo di valutazione e' esso
stesso una grandezza fisica»*): `_cs_nodo_prev` (**71.88 %**), `_psi_spin_prec` (**95.33 %**), i due
`theta` (**C19**), lo **sfasamento `eta`** (il neonato pesava `2e-4` invece di 0).
**Conseguenza per chi applica A6:** non basta guardare *quali* grandezze entrano in una legge.
**Va guardato A QUALE TEMPO ciascuna e' valutata, e se quel tempo e' garantito dalla STRUTTURA o
solo dall'ORDINE.** *(Un caso reale di garanzia d'ordine: l'inerzia legge `peq`, `cs` e `d` prima
che vengano aggiornati — e' corretto **oggi**, ma si romperebbe **in silenzio** se il blocco venisse
spostato. Voce **Z17**.)*

## A7 — CONSERVAZIONE E STATO
**Una grandezza senza stato non puo' conservare nulla.** Un processo che **aggiunge** senza
**togliere**, e senza memoria, e' un **cricchetto**: il rumore vi si integra in crescita
irreversibile.
*Caso:* `spinta` — `rep` istantaneo, `d0 += spinta` irreversibile.

### A7b — COROLLARIO: **uno stato non nasce indefinito** *(aggiunto 2026-09-17)*
**Uno stato non deve mai nascere indefinito. O si eredita da chi lo genera, o si costruisce da cio'
che esiste nel punto in cui nasce.** `NaN` dice *«non lo so»*, e quasi sempre **si sa**: un arco
appena nato sta in un posto che esiste gia', coi suoi due nodi. **Lo sfondo non e' ignoto: e' quello
che c'e' li'.**
*Perche' discende da A7:* una grandezza che nasce indefinita **non ha stato**, e finche' non ce
l'ha non puo' conservare nulla. Ogni lettura in quella finestra legge un buco, e **ogni copertura
messa sopra ne nasconde un'altra** *(caso reale: `NaN` -> `np.maximum(peq, 1e-30)` -> il vincolo
causale `max(t_luce, t_visco)`: **tre reti sopra lo stesso buco**)*.
*Riferimento di stile, gia' nel codice:* `:3598`, dove i due archi figli **ereditano `peq` dall'arco
padre** — locale, immediato, nessun `NaN`.

**⚠ E IL LIMITE DEL COROLLARIO, MISURATO PRIMA DI APPLICARLO** (`doc/REFERTO_peq_nascita.md`).
Il corollario dice *«si costruisce da cio' che esiste nel punto in cui nasce»*. **Ma va verificato
che qualcosa esista davvero**, e in un caso reale **non esisteva**: alla costruzione della scena
`self.psi` e' **identicamente zero** (viene popolato solo dentro `step()`), quindi
`0.5*(I[a]+I[b])` vale **esattamente 0** su **4555 archi su 4555**. Inizializzare li' avrebbe
scritto **uno zero al posto di un `NaN`**, cioe' **un valore degenere travestito da valore**.
**In quel punto il `NaN` era l'unica cosa onesta**: la grandezza non era indefinita per
trascuratezza, era **non ancora definita**.
**QUINDI IL COROLLARIO SI APPLICA COSI':** prima si verifica **che cosa esiste** nel punto di
nascita. Se esiste uno stato da cui costruire (i nodi hanno densita' vera, l'arco padre ha `peq`) →
**si costruisce o si eredita, e il `NaN` e' un difetto.** **Se non esiste nulla, il `NaN` e'
corretto e il difetto sta altrove** — nel fatto che qualcuno legga quella grandezza prima che
esista. **Sostituire un indefinito con uno zero non e' inizializzare: e' nascondere.**

**⚠ E IL CASO SPECULARE, misurato il 2026-09-17** (`doc/REFERTO_psi_zero_ramp.md`): **uno ZERO puo'
essere il valore CORRETTO di una legge, e allora A7b NON si applica.** `psi = 0` alla costruzione
della scena sembrava «assenza di inizializzazione» — ed e' invece il valore giusto di
`ramp = min(1, eta/TAU_A)` con `eta = 0`: **un nodo appena nato non pesa ancora**, e nascere con
eta' zero e' **corretto**. *(`calcola_psi()` era gia' chiamato: la chiamata non mancava.)*
**LA DOMANDA CHE DISTINGUE I DUE CASI:** *«esiste una legge per cui questo valore e' quello
giusto?»* Se si', non e' un indefinito travestito: e' uno stato. **Se no, e' un buco.**

## A8 — UN RAMO SILENZIOSO NON E' UN RAMO

**Ogni fallback su un percorso fisico deve essere CONTATO.** Un ramo che scatta senza segnalarlo
**non produce un errore: produce una FISICA DIVERSA, silenziosa, che sembra funzionare.**

**Criterio di lettura:** **se un fallback scatta spesso, non e' un fallback — e' il comportamento
principale.**

*Casi che l'hanno generato, tutti MISURATI:*

| grandezza | ramo | scattava | conseguenza |
|---|---|---|---|
| `_cs_nodo_prev` | cache scartata a ogni mitosi | **71.88 %** | `cs = CS_M` costante |
| `_psi_spin_prec` | cache non estesa alla mitosi | **95.33 %** | **FASE 5 / 4pi inerte per mesi** |
| `inerzia` | pavimento `1e-6` | **99.70 %** | il fattore `cs^-2` mangiato dal clamp |
| `_tau` | ramo `dens/dens_rif` | — | il nodo mediano ancorato a `TAU_A` |

**Perche' e' un assioma e non una buona pratica:** un ramo non contato rende il codice **NON
VERIFICABILE**. **I sigilli passano** — il sistema gira, i test sono verdi — **e si misura un'altra
fisica.** *(I sei lati sullo spin sono stati presi cosi'.)*

**⚠ STATUS, dichiarato:** **A8 e' piu' DEBOLE degli altri.** A1-A5 dicono cosa una legge **puo'
essere**; **A8 dice come va STRUMENTATA.** **E' metodologico, non fisico.** Sta qui perche' questo
documento e' gia' dichiarato **codice deontologico**, non sistema generativo — **ed e' l'assioma che
ne ha trovati di piu'.**

### A8b — COROLLARIO: le cache CROSS-PASSO
**Una cache cross-passo va estesa a TUTTI i punti di crescita, e l'estensione va verificata DOVE
AVVIENE, non dove si usa.**
*`_cs_nodo_prev` era estesa in un punto e scartata in un altro:* **il difetto non era nel consumo,
era nella NASCITA.** **Un consumatore che trova la cache corta non si accorge di niente: prende il
fallback.**

> **NOTA DI MISURA, aggiunta dopo la stesura (2026-09-17) e NON parte dell'enunciato.**
> La riga **`inerzia` / `99.70 %`** viene da `CLAUDE.md` §9 e resta valida per lo scenario su cui fu
> presa. **Rimisurata dentro `_passo_spinoriale` sui valori veri** (`csv/_test_fork/
> _verifiche_inerzia.txt`, commit `654aaea`, scena a 3 masse) la frazione al pavimento e'
> **100.00 %, a ogni passo**, con `inerzia` = **`1e-6` esatto**. **Il caso e' piu' forte di come la
> tabella lo scrive, non piu' debole** — ma i due numeri vengono da scenari diversi e **non si
> sovrascrivono a vicenda**: si citano entrambi, con la loro provenienza. *(§9, presidio: una soglia
> su un sistema che cresce va dichiarata con l'istante in cui si misura.)*

## A9 — UN PRESIDIO CHE NON IMPEDISCE NON E' UN PRESIDIO

**Una nota, un commento o una regola scritta che non impedisce STRUTTURALMENTE il ripetersi di un
difetto non e' un presidio: e' una TESTIMONIANZA.**

*Il criterio e' secco:* **se il difetto si e' ripetuto DOPO che la nota esisteva, la nota ha
fallito.** Va sostituita da un **meccanismo** — non rafforzata, non ripetuta piu' in grande, non
spostata piu' in alto nel documento.

*Perche':* una regola che dipende dal fatto che qualcuno la ricordi, al momento giusto, sotto
pressione, **non e' una regola: e' una speranza.** E chi la violera' non sara' distratto: **sara'
impegnato.**

*LA SOGLIA OPERATIVA:* **alla TERZA occorrenza dello stesso difetto si smette di scrivere e si cerca
il meccanismo che lo rende IMPOSSIBILE** — un controllo automatico, un default che non si puo'
sbagliare, un tipo che non compila, un test che fallisce.

| caso | la regola esisteva? | quante volte si e' ripetuto |
|---|---|---|
| encoding cp1252 nei sigilli | si', *«ASCII PURO (tre script gia' morti)»* | **SEI** |
| `par.5-quinquies` (il codice di una misura dev'essere recuperabile) | si', scritta | violata, e **il riavvio l'ha dimostrato** |
| `:2959` *«non ricalcolare psi in punti diversi del passo»* | si', **nel codice** | **~20 chiamanti** |

**⚠ E vale sul documento stesso:** *un termine di paragone disallineato non protegge.*

> **A9 E' L'UNICO ASSIOMA CHE HA GIA' FALSIFICATO SE STESSO, e per questo e' il piu' solido:** la
> **settima** occorrenza dell'encoding colpi' **lo script che stava CONTANDO le sei precedenti.**
> **Una nota che non impedisce il ripetersi non e' un presidio — e la prova e' che ha ucciso il suo
> stesso contatore.**

**⚠ E A9 SI APPLICA A SE STESSO:** finche' resta **una riga in un documento**, **A9 e' una
violazione di A9**. *(Per il suo caso capofila il meccanismo esiste gia': `csv/_presidio.py`
— `avvia(__file__)` forza utf-8, timbra lo script con git, e **rifiuta di girare** se lo script non
e' committato e pulito. E' un MECCANISMO, non una nota.)*

**⚠ DICHIARAZIONE ONESTA — la soglia «alla TERZA» e' SCELTA, non derivata.** Non discende da nulla:
e' il punto in cui, su questo repo, ripetere ha smesso di funzionare. **Nessun caso misurato la
giustifica come numero**; i tre della tabella la superano tutti. **Va detto, altrimenti A9 diventa
esso stesso un numero scelto — cioe' una violazione di A1.**

## A10 — UNA SOLA GRANDEZZA PUO' LEGARE DUE DOMINI

**Dove due domini devono parlarsi — materia e geometria, geometria e tempo — il PONTE dev'essere
UNO SOLO, e le leggi che li collegano devono passare tutte da li'.**
**Se due leggi collegano gli stessi due domini attraverso ponti DIVERSI, uno dei due e' sbagliato —
anche quando entrambi funzionano.**

*Perche':* due ponti fra gli stessi domini sono **una contraddizione**, non una ridondanza. Se
entrambi funzionano, il sistema sta dando **due risposte diverse alla stessa domanda**, e la
differenza si accumula in silenzio **dove i due si moltiplicano**.

*IL CASO, misurato:*

```
r          ancorato a  median(|f|)   ->  LA MATERIA (il nodo tipico, x = 1 per identita')
omega_clk  ancorato a  CS_M          ->  IL VUOTO   (cs -> CS_M dove I -> 0)
e a `:2458` si MOLTIPLICANO:   omega_clk = coerenza * r_node
```

**Lo stesso orologio, due riferimenti incompatibili, nella stessa riga.**
*(E `STEP2_OROLOGIO`, l'unica voce della sezione A di `doc/COMPONENTI_PROMOSSE.md`, usa gia'
`(cs/CS_M)^2` a `:2502`: **il gauge del vuoto E' gia' nel sistema, ed e' gia' certificato. `r` e'
l'unico che non lo usa.**)*

**E LA DIFFERENZA FRA I DUE PONTI E' MISURATA, non solo argomentata** (`Z38`, 2026-09-18, blob
`f8f46683`, 1 seme, 120 passi): il nodo mediano di `f` — cioe' **il punto a cui `r` e' ancorato** —
ha **`cs/CS_M = 0.801`**, dunque **`(cs/CS_M)^2 = 0.64`** nel fattore di `STEP2`.
**I due ponti non coincidono, e lo scarto ha un numero.**

*PARENTI, non istanze:* `d_arco` (due popolazioni nello stesso prodotto) · `TAU_A` (un numero per
una crescita **e** un decadimento) · il denominatore del feedback (normalizzazione **NODALE** su una
grandezza d'**ARCO**).

*RAPPORTO CON A3c:* **A3c e' sul CONFRONTO** — *«non confrontare grandezze di popolazioni diverse»*.
**A10 e' sull'ARCHITETTURA** — *«non collegarle con ponti diversi»*. **A10 dice di piu'.**

*COROLLARIO OPERATIVO:* **quando una legge nuova deve collegare due domini, la prima domanda non e'
«quale forma» ma «QUALE PONTE ESISTE GIA', e perche' non lo sto usando?»** Se la risposta e'
«nessuno», **stai creando un secondo ponte, e va giustificato.**

*STATO DELLA VERIFICA EMPIRICA, dichiarato:* **il caso forte e' UNO**; gli altri tre sono **parenti,
non istanze**. **L'assioma vale per la sua RAGIONE — come A1, che non e' vera perche' si sono trovate
cinque costanti sbagliate — ma la tabella dice quanto lo si e' visto agire, ed e' onesto scriverlo.**

**⚠ E UN LIMITE CHE LA MISURA HA AGGIUNTO, ed e' del 2026-09-18 (`Z38`):** A10 dice **che** uno dei
due ponti e' sbagliato; **NON dice QUALE, e sceglierlo non e' una sua conseguenza.** Misurato: se si
sposta `r` sul ponte del vuoto (`CS_M/d_nodo`), **la frazione di nodi nella banda utile del
bottleneck passa da `87.1 %` a `15.1 %`**, e **`r` cambia SIGNIFICATO** — da *«ritmo relativo al
nodo tipico»* a *«ritmo relativo al vuoto»*. **Sono due letture entrambe legittime — degenerazione
o dilatazione gravitazionale reale — e la misura non le separa.**
> **A10 e' una DIAGNOSI, non una prescrizione. Un assioma che dicesse anche quale ponte tenere
> starebbe scegliendo la fisica, e non e' il suo mestiere.**

## ⚠ DICHIARAZIONE — **dove il modello ha ancora uno SFONDO** *(2026-09-18)*

> **Il modello e' relazionale nella DINAMICA. La nascita della TOPOLOGIA e le DIREZIONI usano un
> embedding euclideo in 3D (`self.pos`) come ausilio computazionale. In quel punto NON e'
> background-independent. L'errore dell'embedding NON e' misurato.**

**Va scritta perche' oggi il repo non la dice da nessuna parte**, ed e' emersa da una domanda di
Luca — *«ma io posso evitare questa retroazione?»* — non da un difetto trovato in una misura.
**Detta cosi' e' onesta, e non e' squalificante.**

**COSA E' RELAZIONALE, e non e' poco:** `psi`, `cs`, `d`, `phi`, le forze, il tempo proprio, la
mitosi e il settore spinoriale **non leggono MAI `pos`**. La dinamica gira sulle **distanze
relazionali `d`** e sul grafo.

**COSA PASSA DALL'EMBEDDING — quattro punti VIVI, verificati riga per riga dal disco:**

| punto | cosa fa | conseguenza |
|---|---|---|
| `:1958` `_allaccia` | `cKDTree(self.pos)` | **decide LA TOPOLOGIA** |
| `:4230` / `:4267` `memoria_hebbiana_moto` | `v = pos[j] - pos[i]` → `dirarc`, `grad_tw` | **scrive `mem_mot` e `_nb`** |
| `:4425` `memoria_hebbiana_moto` | `v_rel` → `dir_radiale`, `dir_laterale` | **gravita', frame-drag** |
| `:1498-1499` `chiralita_core_locale` | **sfera EUCLIDEA** di raggio `r` | il core locale (`--chi-core` attivo) |
| `:3409-3410` Kuramoto | `cmv`, `r_cm` dal centro di massa | **sotto `K_SYNC != 0`, e `K_SYNC = 1.0` di DEFAULT (`:199`): E' VIVO** |

*(Davvero inerti: `:4338` sotto `LS_AZIM = False` e `:4199` sotto `L_CONSERVA = False`, quest'ultimo
marcato **«ERRATA, NON usare»**.)*

**E `pos` INSEGUE `d`** (`rilassa_disegno`, `EMB_IT = 3`): **esiste un ANELLO**

```
d  ->  pos (approssimato, 3D, 3 iterazioni)  ->  topologia + direzioni  ->  d
```

**TRE CONSEGUENZE, e la prima sorprende:**
1. **la DIMENSIONE 3 e' FISICAMENTE RILEVANTE:** `_allaccia` cerca per **RAGGIO**, non per `k`
   vicini, e `N_vicini ~ densita' * rc^D`. **In 6D il grado esploderebbe.** *(Con un `k`-NN la
   dimensione sarebbe stata indifferente: non lo e'.)*
2. **VIOLA `A5`:** due nodi si allacciano perche' **vicini NEL DISEGNO**, anche se sul grafo sono
   lontanissimi. **Un legame puo' nascere fra punti che non si sono MAI parlati.**
3. **un grafo arbitrario NON si rappresenta esattamente in 3D** *(gia' a cinque nodi le distanze
   sono sovradeterminate)*: **l'errore dell'embedding RIENTRA nella fisica.**

**Il progetto che la toglierebbe — la geometria ricostruita dalle sole `d` — e' REGISTRATO e NON
INIZIATO**, col suo costo e col criterio che deciderebbe se farlo: **`doc/RAMIFICAZIONI.md`, voce
`Z47`.** **Il criterio e' una MISURA** *(«quanto mente l'embedding?»)*, **non un'opinione.**

---

## APERTO — cosa manca perche' siano assiomi
1. **Non sono generativi.** Serve **l'azione unica `S`**: allora diventerebbero **i vincoli che `S`
   deve soddisfare.**
2. **Non sono indipendenti.** ~~**A3 e' forse un caso particolare di A2.**~~ **RISOLTO il
   2026-09-17: A3 E' INDIPENDENTE**, per controesempio — `u_nodo = I / media_dei_VICINI` (`:2607`)
   **soddisfa A2** (la media e' sui vicini topologici: nessuna scorciatoia globale) e **viola A3**
   (che nomina esplicitamente «media dei primi vicini»). *(`u_nodo` non va percio' corretto: sta
   dentro `_cs_nodo`, cioe' dentro cio' che **definisce** la causalita', e **A4** giudica quel
   livello a parte. Voce **Z5** del registro.)* **A4 e A5 restano in tensione** su `cs`.
   **⚠ A2 RESTA VIOLATO DA `Lam = mean(I)`, CHE FUNZIONA — e il 2026-09-18 la tensione e'
   diventata piu' forte, non piu' debole.** `_cs_nodo` (`:2914`, `:2921`) costruisce la scala di
   `cs` come **`mean(I)`, una media sulla PROPRIA popolazione**: e' esattamente **la scorciatoia
   globale che A2 vieta**. **E funziona:** `cs_std/cs` e' passato da **0.0086 %** (scala assoluta
   `1/GAMMA^2 = 400`) a **17.6 %** — **un fattore ~2050** — cioe' **`cs` e' passato da inchiodato a
   VIVO** *(`Z39`; il mandato che ha chiesto questa voce citava **1300**, da una misura precedente:
   **e' lo stesso fatto letto su due misure diverse, e qui si riporta quella del blob `f8f46683`**)*.
   **VA RISOLTO, e le due vie sono incompatibili:** **o A2 ammette le medie globali DERIVATE** —
   dichiarando cosa distingue `mean(I)` da una scorciatoia — **oppure `cs_floor` va rifatto con
   `peq`**, lo sfondo diffuso **locale**.
   > **Un documento che nasconde le proprie contraddizioni non e' un termine di paragone.**
   > **E questa e' la piu' scomoda che abbia: la violazione e' la ragione per cui il pezzo
   > funziona.**
3. **⚠ TRE VOCI SU DIECI NON SONO ASSIOMI NELLO STESSO SENSO DELLE ALTRE** *(aggiornato il
   2026-09-18 con A9 e A10; prima diceva «due su otto»)*. **A6 e' un TEOREMA**, non un assioma.
   **A8 e A9 sono METODOLOGICI**, e con loro il corollario **A3c**:

   > **A1-A5, A7 e A10 dicono COME UN SISTEMA DEVE ESSERE FATTO.**
   > **A8, A9 e A3c dicono come dev'essere OSSERVABILE (A8), come le sue regole vanno rese
   > EFFICACI (A9), e come i suoi numeri vanno CONFRONTATI (A3c).**
   > **E sono, in pratica, quelle che ne trovano di piu'.** *(A8 ha trovato `_cs_nodo_prev`,
   > `_psi_spin_prec` e il pavimento dell'inerzia; A9 ha trovato sette volte l'encoding e il
   > riavvio; A3c ha trovato cinque errori di popolazione in tre giorni.)*

   **Non e' un difetto del documento, ed e' gia' dichiarato in testa:** questo e' un **codice
   deontologico**, non un sistema generativo. **Ma la distinzione va tenuta visibile**, perche' il
   giorno in cui esistesse l'azione unica `S`, **A1-A5/A7/A10 diventerebbero vincoli su `S`, e
   A8/A9/A3c NO: resterebbero vincoli su CHI LA MISURA.**
4. **Nessuno e' derivato:** sono **regolarita' induttive**, e **potrebbero non valere fuori dai casi
   che le hanno generate.**

## A11 — UN LIMITE E' UNA LEGGE, NON UNA TOPPA

> **Decisione di Luca, 2026-09-21.** **Nasce da cinque difetti trovati in due giorni, tutti della
> stessa famiglia: un `clip`, un pavimento o un tetto messi per proteggere da un errore invece che
> per esprimere un vincolo.**

**Un clip, un pavimento o un tetto e' ammesso SOLO se esprime un VINCOLO FISICO DICHIARATO.**
**Se protegge da un errore, l'errore va corretto DOVE NASCE.**

### I SETTE COROLLARI, ciascuno col difetto REALE da cui nasce

**1. ORIGINE FISICA.** `LAM` e il limite di causalita' lo sono; **un numero scelto per non dividere
per zero NO.**
> **Da `Z94`:** `max(peq, 1e-9)` non e' un vincolo fisico su `peq` — e' una difesa dalla divisione.
> **Il vincolo fisico vero e' `peq >= 0`, e sta nell'aggiornamento, non nella divisione.**

**2. NON DIPENDE DA CIO' CHE LIMITA.** **Un pavimento che scende con la cosa che trattiene, o un
tetto che cresce con essa, la INSEGUE invece di fermarla.**
> **Da `Z79`:** il clip `tanh(stress)*d0` **cresce con `d0`** — a `d0 = 30` vale `8.7`, **770 volte**
> il tetto causale — quindi **piu' `d0` scappa, piu' il clip glielo consente.**
> **E dalla scala minima (`Z91`):** il pavimento comovente `f*median(d0)` **si muove con la
> popolazione che dovrebbe ancorare.**

**3. NON RIBALTA SEGNI E NON AMPLIFICA.** **Un limite puo' solo RIDURRE la distanza dal dominio, mai
trasformare un valore sbagliato in uno ENORME.**
> **Da `Z94`, ed e' il caso piu' netto:** con `peq = -4.85e-04`, il pavimento sostituisce un
> denominatore **negativo** con `1e-9`. L'anomalia vera sarebbe **`-3.72`** *(di richiamo)*; il
> pavimento la fa diventare **`+1.805e+06`**. **Ribalta il segno e moltiplica per `3.7e5`.**

**4. SIMMETRICO, SE LA FISICA LO E'.** **Frenare in un verso solo trasforma il RUMORE in DERIVA.**
> **Da `Z91`:** `SCALA_MIN` frena le **discese** e lascia intatte le **salite**. Con spinte opposte
> di **somma nulla** il risultato **non e' zero**: e' un **cricchetto**, e vicino a `LAM` annulla il
> **96 %** di ogni discesa.

**5. SI RIPARA ALL'ORIGINE, NON NEL PUNTO D'USO.** **Una grandezza che deve restare positiva si
tiene positiva DOVE VIENE AGGIORNATA, non dove la si DIVIDE.**
> **Da `Z94` e `Z95`:** il pavimento stava a `:4215` *(la divisione)*; il difetto stava a `:4206`
> *(l'Eulero esplicito che scavalca)*. **La cura `PEQ_ESATTO` agisce sull'aggiornamento, e li' la
> positivita' e' DIMOSTRATA** — combinazione convessa — **invece che imposta.**

**6. SE SATURA, E' UN ALLARME.** **Ogni limite ha un CONTATORE; in un sistema sano un limite tecnico
non scatta mai.**
> **Da `Z79`:** il clip era saturo nel **`98.86 %`** dei casi. **Un limite che morde quasi sempre
> non e' un limite: e' la legge**, e nessuno l'aveva scelta.

**7. UN LIMITE SECCO E' SOSPETTO, E SI IMPONE IN MODO MORBIDO. MA LA MORBIDEZZA HA TRE OBBLIGHI:**
**(a)** lontano dal confine e' l'**IDENTITA'**; **(b)** non crea **DERIVA** su spinte simmetriche;
**(c)** la sua **LARGHEZZA** viene dalla fisica, non da un numero scelto.
**Un limite morbido che viola uno dei tre e' PEGGIO di uno secco, perche' sbaglia OVUNQUE invece che
in un punto.**
> **Dal task history del ramo D** *(`doc/TASK_HISTORY/2026-09-21_ramo_D_tre_modifiche.md`)*, **tre
> forme morbide provate e CADUTE, una per ciascun obbligo:**
> * **`tanh`** come saturazione — **satura anche in ALTO**, dove non c'e' nessun vincolo: viola **(a)**;
> * **`LAM + x*exp(-LAM/x)`** — **non e' idempotente**: `L(x) > x` anche per `x >> LAM` *(+4.98 % a
>   `3*LAM`)*, e applicata **sette volte per passo** avrebbe **fabbricato l'espansione da misurare**:
>   viola **(a)**;
> * **`1 - LAM/x`** *(la forma in vigore)* — agisce su **tutta la fascia**, non solo al confine, e
>   frena **solo le discese**: viola **(b)**. **E' il cricchetto del corollario 4.**

### COSA A11 NON DICE
- **non dice che i limiti vadano tolti.** Dice che **ognuno deve dichiarare quale legge esprime**, e
  che **quelli che non ne esprimono nessuna sono lavoro arretrato**, non fisica;
- **non e' una scansione fatta:** il **censimento** di tutti i `clip`, pavimenti e tetti del
  simulatore **e' in CODA** *(mandato del 2026-09-21 §2)*. Finche' non e' fatto, **non si sa quante
  toppe ci siano ancora dentro** — e va detto cosi', non stimato.


## SCANSIONI MAI FATTE
**A5** (grandezze istantanee che mediano a distanza: `w`, `psi`, `B`, `lambda_nodi`) ·
**A7** (altri cricchetti senza stato) · **A1** (enumerazione di TUTTE le costanti nei percorsi
fisici: `0.02`, `3.0`, `TAU_DIFF`, `TAU_BG`, `M_PH`, `G_PH`…).
