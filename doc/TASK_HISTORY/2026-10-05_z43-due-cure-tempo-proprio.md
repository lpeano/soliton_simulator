# `Z43` — **LE DUE CURE DEL TEMPO PROPRIO**, decise da Luca il 2026-10-05

## STATO: **NON INIZIATO** — in coda dopo `MEM-HEBB-VERSO` passo (2)

*(Messo al sicuro nel repo il **2026-10-05**. ### **Nessun lavoro e' stato fatto su questo
mandato.**)*

> ### ⛔ **PERCHE' NON PARTE SUBITO, e non e' una mia scelta: lo dice il mandato stesso** —
> *«Si esegue DOPO `MEM-HEBB-VERSO` passo (2) (lo spegnimento della fase), che e' in coda
> prima di questo»*. ### **E `L-UN-PROMPT` dice la stessa cosa dall'altro lato.**

> ### ⛔ **E LA `PARTE B` PARTE SOLO SE IL SIGILLO DELLA `PARTE A` PASSA: altrimenti
> ### `FERMO`.** *(Parola del mandato, non mia.)*

> ### ⛔ **LA SEZIONE `LA STELLA POLARE` NON E' QUI, E NON PER DIMENTICANZA:** il mandato
> chiede **due** task history, *«ciascuna con `LA STELLA POLARE` prima del codice»*, e si
> scrivono **quando ciascuna cura parte**. ### **Scritte adesso sarebbero risposte date
> prima di aver letto il codice, cioe' la ricostruzione che il par.8 esiste per impedire.**

> ### ⚠ **E IL TESTO QUI SOTTO E' COPIATO PAROLA PER PAROLA:** non e' riassunto ne'
> riformulato. Se una riga sembra ambigua, l'ambiguita' e' **nell'originale** e va risolta
> con Luca, non da me.

---

## IL MANDATO, verbatim

MANDATO: Z43 — LE DUE CURE DEL TEMPO PROPRIO, DECISE DA LUCA IL 2026-10-05. Si esegue DOPO MEM-HEBB-VERSO passo (2) (lo spegnimento della fase), che e' in coda prima di questo. Due cure, in ordine, ciascuna con il suo task history (LA STELLA POLARE prima del codice), il suo sigillo con criteri committati PRIMA, e i suoi commit. La PARTE B parte SOLO se il sigillo della PARTE A passa: altrimenti FERMO.

DECISIONI DI LUCA, da registrare in Z43, COMPONENTI:A1/B9 (STEP2) e nel task history, senza reinterpretarle:
 (1) L'orologio di Compton conta r DUE volte: omega_clk = coerenza * r_node * (cs/CS_M)^2 (:5926, :5970) e poi la fase avanza di omega_clk * dt_n, con dt_n = DT*r (:5971). Un orologio avanza di frequenza PROPRIA per tempo PROPRIO: r va UNA volta sola, in dt_n. SI TOGLIE r_node dalla frequenza. Motivo misurato: il BRACCIO A (66a798d) ha tolto proprio quel fattore e l'altalena e' crollata (|f| 5.283 -> 1.034, C0 7.185 -> 1.031).
 (2) r = cs_nodo / CS_M (esponente p = 1, "orologio a luce": un tic e' il tempo di attraversamento, la stessa legge del tempo-luce d/cs), con cs da |psi|^2 COME OGGI, letto dalla cache del passo PRECEDENTE (_cs_nodo_prev, la stessa che usa l'orologio), per rispettare A6. r non legge piu' la fase. D32 resta: r e' il tempo proprio unico; cambia come si calcola.
 (3) L'unificazione delle densita' (cs da rho_spin) NON si fa ora: resta una decisione separata.

FATTO DEL GUARDIANO, da registrare come VOCE NUOVA e da NON curare ora (decisione di Luca: si cura dopo):
 _cs_nodo non e' del tutto locale. La transizione e' locale (u_nodo = I / media dei VICINI), ma il pavimento usa _Lam = mean(|psi|^2) su TUTTA la rete (_scala, cs_floor). Quindi cs, e con la (2) anche r, porta un riferimento globale. Lo stesso termine tocca gia' oggi il tetto causale, il tempo-luce e l'orologio.
 LA STORIA, da citare: e' la cura del 2026-09-16 (48d5ce2), che tolse la densita' critica ASSOLUTA (GAMMA = 0.05, cioe' 400) sostituendola con Lam, l'energia del vuoto calcolata dal sistema. Tolse un numero a mano e introdusse un riferimento globale: lo STESSO scambio fatto per il gauge di r (mediana globale). Registralo come schema ricorrente, non come incidente.
 Verifica dall'AST e registra la voce (per esempio CS-LAMBDA-GLOBALE), collegata a INVARIANZA-LOCALE-CS, Z43 e VUOTO-LOCALE-DETERMINISTICO: Lam rappresenta "il vuoto", e la cura naturale e' un vuoto LOCALE per nodo, che e' la proposta di Luca del 2026-10-02 (che richiede prima un'energia definita, ENERGIA-NON-DEFINITA).

PARTE A — CURA (1).
 Censisci dall'AST TUTTI i siti in cui r (o r_node, dt_n/DT) moltiplica una FREQUENZA che viene poi moltiplicata per dt_n, compreso il ramo legacy di omega_clk (rho/rho_c * r_node, che oggi non gira). Se trovi siti oltre a questi due, FERMATI e riporta: non estendere la cura da solo. Applica la stessa correzione al ramo legacy (e' la stessa legge), dichiarandolo.
 Sigillo, criteri fissati PRIMA:
  - braccio 0: prima + patch committata = blob nuovo;
  - IDENTITA' AL BYTE nei passi 1 e 2 (lockstep su TUTTI gli attributi di net, scena del driver, seme 11): li' r = 1 esatto per costruzione, quindi togliere r_node non cambia niente. Se divergono, la patch tocca altro: FERMATI;
  - CASO CHE DEVE FALLIRE: dal passo 3 lo stato DEVE divergere. Se non diverge, la cura non agisce: FERMATI;
  - STEP2 intatto: omega_clk / coerenza = (cs_prec/CS_M)^2 al bit, su ogni nodo e ogni passo;
  - L'ALTALENA SPARISCE nel simulatore vero, 150 passi: rapporto dispari/pari della mediana di |f| e di C0 <= 1.2 (il braccio A aveva dato 1.03). Misura con lo strumento di Z43 (7b71aa48), rigirato sul blob nuovo;
  - la corsa arriva a 150 passi senza FERMO di invarianti. Riporta che cosa cambia a valle (n, archi, divisioni, Schwinger), senza giudicarlo.

PARTE B — CURA (2), solo se A passa.
 ritmo() resta l'UNICA fonte di r (i chiamanti non cambiano): con TAU_LOC > 0 restituisce cs_nodo_prev / CS_M per nodo. Il ramo che leggeva la fase (f, il gauge _med_f_prec e la sua promozione, la saturazione x/sqrt(1+x^2)) esce dalla fisica secondo le regole del repo per sostituire una legge (par.10, archivio dei rami come per CURA 2). Dichiara che cosa diventa ciascun contatore e ciascun registro (_med_f_ultimo, _med_f_prec, _ritmo_*). Se la cache non esiste (passo 1) o non e' allineata: r = 1, CONTATO e dichiarato.
 Note da dichiarare: cs <= CS_M per costruzione di _cs_nodo, quindi r e' in (0, 1] e il tempo proprio non supera mai quello coordinato; cs dipende da r attraverso i sotto-passi della metrica (dt_e/nsub), quindi c'e' un anello r <-> cs sfasato di un passo.
 Sigillo, criteri fissati PRIMA:
  - braccio 0;
  - FEDELTA': r restituito = _cs_nodo_prev / CS_M AL BIT, su ogni nodo e ogni passo in cui la cache e' allineata;
  - NIENTE ALTALENA: rapporto dispari/pari della mediana di r <= 1.2, e autocorrelazione a ritardo 1 della mediana di r non fortemente negativa (riportala). Se l'anello r <-> cs oscilla, FERMATI e riporta;
  - SEGNO: r mediano nella "materia" (5% di |psi|^2 piu' alto) MINORE di quello nel vuoto (25% piu' basso). Atteso dalla legge; se non torna, riportalo come risultato e non nasconderlo;
  - LOCALITA', da misurare e non da presumere: perturbando lo stato di UN nodo lontano, di quanto cambia r di un nodo distante nello stesso passo. Atteso: non zero, per il termine globale di _Lam, ma dell'ordine 1/n. Riporta il numero e collegalo alla voce CS-LAMBDA-GLOBALE;
  - CASO CHE DEVE FALLIRE: lo stato diverge da quello della PARTE A dal passo in cui r smette di valere 1 (riporta quale);
  - 150 passi senza FERMO; riporta che cosa cambia a valle (n, archi, divisioni, il tetto causale che ora legge il nuovo dt_e).
 Dopo la PARTE B, nel TODO di Z43: i prossimi sono il passo (2) di TETTO-CAUSALE e la cura (1) di MEM-HEBB-VERSO (con la sostituzione del taglio 0.01 col limite causale cs*dt_e, da valutare). La decisione (1) di MEM-HEBB-VERSO resta DA RICONFERMARE da Luca. CS-LAMBDA-GLOBALE si cura dopo, insieme a VUOTO-LOCALE-DETERMINISTICO.

NON CHIUDERE IL TURNO A META': ti fermi solo con "FERMO: <motivo>" su un controllo fallito o su una decisione di Luca. Chiudi con "PUSHATO: <hash>". STOP.

---

## CHE COSA MANCA, PRIMA CHE QUESTO LAVORO POSSA PARTIRE

*(Nessuna di queste righe interpreta il mandato: sono **cose da fare** che il mandato stesso
elenca, in ordine, perche' alla ripresa non si debba ri-leggerlo per capire da dove
cominciare.)*

0. ### **`MEM-HEBB-VERSO` passo (2)**, che sta **prima** *(il suo file e'
   `doc/TASK_HISTORY/2026-10-05_mem-hebb-verso-cura2-fase.md`)*;
1. le **tre decisioni** registrate in **`Z43`**, in **`COMPONENTI:A1`/`COMPONENTI:B9`**
   *(`STEP2`)* e nel task history;
2. la **voce nuova** per il fatto del guardiano *(`CS-LAMBDA-GLOBALE`)*, **verificata
   dall'AST**, collegata a `INVARIANZA-LOCALE-CS`, `Z43` e `VUOTO-LOCALE-DETERMINISTICO`,
   e ### **da NON curare ora**;
3. **`PARTE A`:** il **censimento dall'AST** di tutti i siti in cui `r` moltiplica una
   frequenza poi moltiplicata per `dt_n`; ### ⛔ **se ne trovo oltre a quei due: FERMO**;
4. **`PARTE A`:** task history con `LA STELLA POLARE`, i **sei criteri** del sigillo
   committati **prima**, la cura, il sigillo, la corsa, il referto;
5. **`PARTE B`:** la stessa sequenza, ### **e SOLO se il sigillo di `A` passa**;
6. il **`TODO` di `Z43`** aggiornato come il mandato lo detta.

### ⚠ **TRE COSE DEL MANDATO CHE VANNO LETTE DUE VOLTE**

1. ### **IL RAMO LEGACY DI `omega_clk` NON GIRA OGGI** *(`DEPARAM_OROLOGIO = True`)*, e il
   mandato dice di ### **applicargli la stessa correzione, dichiarandolo** — *«e' la stessa
   legge»*. ### **Quindi la cura tocca un ramo che nessun sigillo puo' misurare girando**,
   e questo va detto nel referto.
2. ### **LA `PARTE A` HA UN CRITERIO CHE E' UN'IDENTITA' E UNO CHE E' UNA DIVERGENZA:**
   identita' al byte ai passi **1-2** *(dove `r = 1` per costruzione)* e divergenza
   **obbligatoria** dal passo **3**. ### **Sono le due meta' dello stesso controllo**, e
   ### **se l'identita' non tiene la patch tocca altro; se la divergenza non arriva la cura
   non agisce.**
3. ### **LA `PARTE B` CHIEDE UNA MISURA DI LOCALITA' <<da misurare e non da presumere>>**,
   con un atteso dichiarato *(`~1/n`, non zero, per il termine globale di `_Lam`)*.
   ### **E' il primo criterio di sigillo di questo repo che misura la LOCALITA' di una
   legge invece della sua identita'**, e va costruito con cura.

### 📌 **E UNA COSA CHE QUESTO MANDATO CAMBIA RISPETTO AL REFERTO `9cec5d8`**

Il referto di `Z43` riportava **sei vie** e ### **non ne scegliva nessuna**, come il mandato
del passo (1) prescriveva. ### **Qui Luca SCEGLIE:** la `(2)` e' la via **`(d)`** *(`r` da
`cs` con `|psi|^2`)* con ### **esponente `p = 1`**, che ### **nessuna delle sei vie
nominava** — le `C5` misurate erano `p = 2` *(`STEP2`)* e `p = 0.5` *(coordinate isotrope)*.
### **`p = 1` e' una DECISIONE, col suo motivo scritto: <<orologio a luce, un tic e' il
tempo di attraversamento, la stessa legge del tempo-luce `d/cs`>>.** ### **Non l'ho
proposta io e non la reinterpreto.**
