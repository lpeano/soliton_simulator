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
*Corollario A3b — i PAVIMENTI sono la stessa cosa dall'altro lato:* un clamp tarato **sopra** i
valori tipici congela cio' che dovrebbe proteggere (`1e-6` sull'inerzia: **99.7 %**). **Un ramo di
fallback che scatta quasi sempre non e' un fallback: e' il comportamento principale.**

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

## APERTO — cosa manca perche' siano assiomi
1. **Non sono generativi.** Serve **l'azione unica `S`**: allora diventerebbero **i vincoli che `S`
   deve soddisfare.**
2. **Non sono indipendenti.** ~~**A3 e' forse un caso particolare di A2.**~~ **RISOLTO il
   2026-09-17: A3 E' INDIPENDENTE**, per controesempio — `u_nodo = I / media_dei_VICINI` (`:2607`)
   **soddisfa A2** (la media e' sui vicini topologici: nessuna scorciatoia globale) e **viola A3**
   (che nomina esplicitamente «media dei primi vicini»). *(`u_nodo` non va percio' corretto: sta
   dentro `_cs_nodo`, cioe' dentro cio' che **definisce** la causalita', e **A4** giudica quel
   livello a parte. Voce **Z5** del registro.)* **A4 e A5 restano in tensione** su `cs`.
   **A2 resta violato da `Lam = mean(I)`, che funziona.**
3. **A6 e' un teorema**, e **A8 e' metodologico** (dice come si STRUMENTA, non cosa una legge puo'
   essere): **due voci su otto non sono assiomi nel senso degli altri sei.**
4. **Nessuno e' derivato:** sono **regolarita' induttive**, e **potrebbero non valere fuori dai casi
   che le hanno generate.**

## SCANSIONI MAI FATTE
**A5** (grandezze istantanee che mediano a distanza: `w`, `psi`, `B`, `lambda_nodi`) ·
**A7** (altri cricchetti senza stato) · **A1** (enumerazione di TUTTE le costanti nei percorsi
fisici: `0.02`, `3.0`, `TAU_DIFF`, `TAU_BG`, `M_PH`, `G_PH`…).
