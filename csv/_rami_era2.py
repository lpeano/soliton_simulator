# -*- coding: utf-8 -*-
"""PUNTO `2`, seconda parte — **OGNI RAMO DELLA FISICA DELL'ERA `2` E' DICHIARATO.**

> ### ⛔ **`A8`: UN RAMO SILENZIOSO NON E' UN RAMO.** E `P5`: *«ogni ramo `else` /
> fallback / `getattr(..., default)` su un percorso fisico ### **va CONTATO**»*.

### ⭐ **E LA PARTE CHE CONTA NON E' CONTARLI: E' DIRE A CHE SERVONO.** Un `if` non
e' un difetto — ### **un `if` NON DICHIARATO lo e'**, perche' nessuno sa se smista,
valida, o ### **sceglie in silenzio un pezzo di fisica.**

| il ruolo | che cosa significa | e' un difetto? |
|---|---|---|
| **`smistamento`** | sceglie ### **quale** operazione fare, da ### **un campo dichiarato** *(`TIPO`, il nome nella composizione)* | ### ✅ **no:** la decisione viene da un campo, non da un indovinello |
| **`validazione`** | costruisce ### **un messaggio di errore** e non cambia nessun valore | ### ✅ **no:** e' il presidio stesso |
| **`iterazione`** | ### **ferma un ciclo** *(convergenza, fine lista)* | ### ✅ **no**, ma ### **la soglia va DICHIARATA** |
| **`default`** | sceglie un valore ### **quando il chiamante non lo passa** | ### ⚠ **SI', ed e' il punto `15(b)`:** *«un parametro non presente e' un ERRORE»* |
| **`guardia`** | protegge da uno stato ### **che non dovrebbe esistere** | ### ⛔ **SI':** `A11` dice ### **cerca l'errore**, e `P5` che ### **va CONTATA** |

### ⚠ **IL LIMITE, dichiarato:** la classificazione ### **la scrivo io**, il
### **conteggio** no — quello lo misura l'AST. ### **Quindi il presidio garantisce
che un ramo NUOVO non passi inosservato, NON che la mia etichetta sia giusta.**
"""
import ast
import glob
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)

NL = chr(10)
PRESIDIO = "P-R1"

RUOLI = ("smistamento", "validazione", "iterazione", "default", "guardia")

# ### ⛔⛔ **LE RADICI DEL NUCLEO, DICHIARATE E PROVVISORIE** *(decisione di Luca
# ### del `2026-10-16` alle `19:33`)*. ### **Sono gli INGRESSI DEL PASSO** -- `tick.py` per
# ### la camminata, `passo.py` per la via di `H` -- ### **piu' il motore e i moduli delle
# ### leggi.**
# ### ⚠ **PERCHE' <<PROVVISORIE>>:** i moduli delle leggi ### **dovrebbero venire dal
# ### campo `modulo` della tabella**, che ### **non esiste ancora** *(pezzo `6` della
# ### coda)*. ### **Finche' non c-e-, la radice la dichiaro qui e lo scrivo.**
RADICI = ("tick", "passo", "motore", "materia_vuoto", "saturazione")


def nucleo(base=None):
    """### IL NUCLEO DELLA FISICA: la ### **CHIUSURA DEGLI IMPORT** dalle radici.

    ### ⭐⭐ **SI DERIVA, non si scrive a mano** *(mandato del `2026-10-16`)*: la
    lista si legge da `primo_ordine/_mappa.yaml`, che ### **`P-MOD` tiene allineata al
    codice** -- quindi ### **un import nuovo allarga il nucleo DA SOLO**, e un modulo che
    smette di essere importato ### **ne esce da solo.**

    ### ⚠ **E LA CHIUSURA SI LIMITA A `primo_ordine/`, dichiarato:** `motore.py`
    importa `_presidio`, che vive in `csv/` ed e- ### **il timbro del blob**, non fisica.
    ### **Il perimetro della fisica e- quello di `H-FISICA-FUORI-LISTA`.**

    ### ⛔ **COSA FA GRATIS:** `crescita.py` e `vuoto.py` sono regole `NON-H`
    ### **che nessuno importa** -- oggi non girano, quindi ### **non sono nel nucleo**, e
    ### **ci rientreranno DA SOLE il giorno in cui il passo le importera-.**
    """
    import yaml
    base = base or RADICE
    testo = io.open(os.path.join(base, "primo_ordine", "_mappa.yaml"),
                    encoding="utf-8").read()
    mappa = yaml.safe_load(testo)
    per = {r["nome"][:-3]: list(r.get("importa") or [])
           for r in mappa["moduli"] if str(r["nome"]).endswith(".py")}
    visti, coda = set(), list(RADICI)
    while coda:
        x = coda.pop()
        if x in visti:
            continue
        visti.add(x)
        for y in per.get(x, []):
            if y not in visti:
                coda.append(y)
    fuori = []
    for x in sorted(visti):
        rel = "primo_ordine/%s.py" % x
        if os.path.exists(os.path.join(base, rel)):
            fuori.append(rel)
    return fuori


# =====================================================================================
#   LA TABELLA -- (file, funzione) -> (quanti, ruolo, perche')
# -------------------------------------------------------------------------------------
#   ### ⛔ **MISURATA il 2026-10-09: `27` rami in `12` funzioni.** Il conteggio lo
#   ### fa l'AST; ### **il ruolo e il perche- li ho scritti io, leggendoli.**
# =====================================================================================
# ### ⭐ **LA MOTIVAZIONE DEI LEGAMI E- UNA SOLA, e sta in UNA COSTANTE:** i
# ### sette moduli generati hanno ### **lo STESSO ramo**, perche- vengono ### **dalla
# ### stessa riga del generatore** -- e scriverla sette volte vorrebbe dire ### **sette
# ### copie che possono divergere.**

RAMI = {
    # ### ⛔⛔ **I RAMI DELLE DUE LETTURE DEI PESI** *(errore `n.12` del guardiano,
    # ### `2026-10-18`)*: ### **nessuno dei due scegle un valore** -- dicono ### **con
    # ### quali pesi si sta leggendo.**
    ("primo_ordine/energia_pesata.py", "g_dello_stato"): (
        2, "smistamento",
        "### DUE RAMI, e sono LO SMISTAMENTO SULLA FORMA. ### (1) a forma SPENTA "
        "(`mot.cs is None` oppure `mot.lambda_c is None`) i pesi sono `1` e `G` e- "
        "`H_tot`: calcolare i pesi vorrebbe dire DIVIDERE `s_nodo` per se- stesso. "
        "### (2) altrimenti si leggono i pesi DELLO STATO. ### E questa funzione "
        "esiste perche- `g_pesata` leggeva `mot.cs`, che DOPO UN TICK e- il `cs` "
        "del CENTRO: un-osservabile che lo usa confronta DUE ISTANTI, e sbaglia "
        "di `O(dtau)` -- e- l-errore n.12, e mi ha fatto misurare 1.002 dove il "
        "passo dava 2.091"),
    ("primo_ordine/energia_pesata.py", "pesi_dello_stato"): (
        1, "guardia",
        "### UN RAMO, ed e- il `finally` che RIMETTE `mot.cs` com-era. ### Questa "
        "funzione mette il `cs` dello STATO nel motore per il tempo di una "
        "lettura, e se lo lasciasse dentro ### IL PASSO DOPO GIREREBBE CON UN "
        "ALTRO PESO -- in silenzio. ### Un-osservabile che cambia la dinamica non "
        "e- un-osservabile"),
    # ### ⛔⛔ **I RAMI DEL PUNTO MEDIO PER PEZZO** *(`2026-10-18`, la decisione di
    # ### Luca delle `12:07`)*: ### **nessuno dei tre scegle un valore** -- due dicono
    # ### ### **quale SCHEMA gira**, e uno ### **quale REGOLA del punto medio.**
    ("primo_ordine/motore.py", "_spostamento_scalare"): (
        2, "smistamento",
        "### DUE RAMI, e sono LO SMISTAMENTO SULLO SCHEMA. ### (1) senza la forma "
        "`cs` (oppure senza `lambda_c`), oppure col peso BLOCCATO (`regola_punto_medio "
        "is None`), si fa IL PASSO DI PRIMA: il peso non dipende dallo stato, "
        "quindi non c-e- niente da risolvere -- ed e- cio- che tiene il braccio 0 "
        "AL BIT. ### (2) altrimenti il peso si valuta AL PROPRIO PUNTO MEDIO. "
        "### E il ramo del peso BLOCCATO NON e- una via d-uscita: e- IL CASO CHE "
        "DEVE FALLIRE di `C1`, e serve a far vedere che il punto medio cambia "
        "qualcosa"),
    ("primo_ordine/flussi_parziali.py", "hop_phi_punto_medio"): (
        2, "iterazione",
        "### DUE RAMI, e sono IL PUNTO FISSO. ### (1) la REGOLA: `ii` prende la "
        "media dei due `Lambda` (quella dichiarata nel task history), `i` prende "
        "`Lambda` del `phi` MEDIO e si misura come INFORMAZIONE -- e un `assert` "
        "rifiuta tutto il resto, perche- un valore di comodo renderebbe "
        "illeggibile quale delle due ha prodotto un numero. ### (2) la "
        "CONVERGENZA: si ferma quando due giri coincidono AGLI ULP, e oltre il "
        "tetto ALZA invece di fermarsi a un valore qualunque. ### E il punto "
        "fisso ACCOPPIA LA RETE INTERA, perche- `Lambda_k` somma i semiarchi di "
        "piu- archi: i giri misurano quanto e- accoppiata la rete, non la "
        "difficolta- di un arco"),
    ("primo_ordine/flussi_parziali.py", "s_arco_da_lambda"): (
        1, "guardia",
        "### UN RAMO, e non e- uno smistamento: e- il `finally` che RIMETTE `cs` "
        "com-era. ### Questa funzione mette `cs` di una `Lambda` DATA nel motore "
        "per il tempo di una lettura, e se lo lasciasse dentro ### IL PASSO DOPO "
        "GIREREBBE CON UN ALTRO PESO -- in silenzio. ### Il `finally` e- la "
        "garanzia che la lettura non ha effetti"),
    # ### ⛔⛔ **I RAMI DELLA LEGGE NUOVA** *(`CAMM-FASE-VUOTO`, `2026-10-18`,
    # ### la strada `(d)`)*: tutti e tre ### **decidono se un pezzo ESISTE o no**, e
    # ### ### **nessuno scegle un valore.**
    ("primo_ordine/energia_pesata.py", "applica"): (
        4, "guardia",
        "### QUATTRO RAMI, e sono TUTTI GUARDIE. ### (1) LA FORMA SPENTA: con "
        "`mot.cs is None` oppure `mot.lambda_c is None` il pezzo NON ESISTE -- e "
        "i due casi sono UN ramo solo per un motivo ESATTO: un `cs` messo A MANO "
        "come COSTANTE non e- una funzione di `Lambda`, quindi `cs'` e- ZERO PER "
        "DEFINIZIONE. ### (2) `dtau` UNIFORME: il tempo di questo pezzo e- IL "
        "TICK, e un tick per nodo non e- definito -- ALZA invece di prenderne uno. "
        "### (3) la CONVERGENZA del punto medio: si ferma quando due giri "
        "coincidono agli ulp, oppure quando la scala e- zero (e la- qualunque "
        "fase e- la stessa). ### (4) il tetto `GIRI_MAX_OMEGA`: ALZA, perche- la "
        "regola dice di RELAZIONARE e non di scegliere un altro schema"),
    ("primo_ordine/energia_pesata.py", "termini_di_h"): (
        1, "smistamento",
        "### UN RAMO, e non e- un pavimento: `rho_k = 0` vuol dire `psi = 0` "
        "in quel nodo, e la- `N = rho ln(rho/(rho+Lambda))` PRENDE il valore "
        "`0` (`x ln x -> 0`). ### E- LA STESSA SINGOLARITA- ELIMINABILE di "
        "`materia_vuoto`, e il ramo esiste perche- `np.log(0)` darebbe `-inf` "
        "-- non perche- il valore sia in dubbio"),
    ("primo_ordine/energia_pesata.py", "g_pesata"): (
        1, "smistamento",
        "### UN RAMO: a forma SPENTA i pesi sono `1`, e `G` e- `H_tot` -- "
        "chiamare `pesi()` la- dentro vorrebbe dire DIVIDERE `s_nodo` per se- "
        "stesso, cioe- fare un conto per ottenere `1`. ### E il confronto fra i "
        "due casi e- IL BRACCIO che tiene onesta questa funzione"),
    ("primo_ordine/stato.py", "nuovo"): (
        4, "smistamento",
        "### QUATTRO RAMI, e sono UNO SMISTAMENTO SUI TIPI: i due di NODO (lo spinore "
        "`C^2` e il reale), i due di ESTREMITA- D-ARCO (lo spinore della camminata e il "
        "vuoto, che hanno taglia `2 m` e non `n`), e il ramo finale che "
        "### SOLLEVA per cio- che non sa costruire. ### Il ramo che solleva NON sceglie "
        "un valore: DICHIARA CHE NON SA FARLO -- ed e- il segnaposto ONESTO della "
        "decisione 13. ### E i due rami di estremita- sono nati col pezzo 2 del "
        "simulatore, quando lo stato della camminata e- entrato in tabella"),
    # ### ⛔ **I LEGAMI GENERATI: UN RAMO CIASCUNO, e lo stesso in tutti**, perche-
    # ### ### **sono generati dalla stessa riga di codice.** ### ⭐ **E il ramo e- una
    # ### GUARDIA, non uno smistamento:** se il motore non ha l-operatore, il legame
    # ### ### **ALZA** invece di tornare un risultato finto.
    ("primo_ordine/stato.py", "controlla_domini"): (
        2, "validazione",
        "i DUE controlli di dominio (punto 1): le componenti FINITE, e `> 0` per la "
        "forma `finito-pos`. ### SOLLEVANO e NON TRONCANO -- troncare nasconderebbe "
        "la violazione e cambierebbe la fisica in silenzio, fermare LA MOSTRA"),
    ("primo_ordine/hamiltoniana.py", "carica_termini"): (
        3, "smistamento",
        "salta i file che non sono `.py` e quelli senza `LEGGE`: ### la decisione viene "
        "da UN CAMPO (`LEGGE` esiste o no), non da un indovinello"),
    ("primo_ordine/passo.py", "strati"): (
        1, "iterazione",
        "cerca ### il primo strato libero per un arco: ferma il ciclo quando lo trova. "
        "### Nessuna soglia: e- una ricerca ESATTA"),
    ("primo_ordine/passo.py", "valida_composizione"): (
        6, "validazione",
        "### SONO IL PRESIDIO STESSO: i quattro controlli della composizione "
        "(vocabolario, palindromo di nomi e pesi, doppioni, pesi a 1). Non cambiano "
        "nessun valore: ### costruiscono messaggi"),
    ("primo_ordine/passo.py", "mezzo_implicito"): (
        2, "iterazione",
        "ferma il punto fisso quando lo scarto scende sotto `toll`. ### LA SOGLIA "
        "VIENE DALLA CONFIGURAZIONE (punto 15(a)), e ### IL CONO DEL GLOBALE DIPENDE "
        "DA LEI -- misurato, e il referto lo dice"),
    ("primo_ordine/passo.py", "passo_locale"): (
        2, "smistamento",
        "smista sul nome dell-operazione, che viene ### DALLA COMPOSIZIONE DICHIARATA, "
        "e sceglie lo strato per indice. ### Nessun default: `gli_strati` SI PASSA"),
    ("primo_ordine/passo.py", "_costanti_di_modulo"): (
        2, "smistamento",
        "salta i nomi `__dunder__` e i callable: ### smista su un TIPO, non su un valore"),
    ("primo_ordine/passo.py", "senza_cache"): (
        1, "smistamento",
        "confronta i nomi prima e dopo: ### e- un confronto, non una scelta"),
}

# ### ⛔ **E QUATTRO FUNZIONI HANNO PERSO TUTTI I LORO RAMI** *(punto `15(b)`)*:
# ### `energia`, `gradiente`, `gradiente_grezzo` e `passo_globale`. Avevano
# ### ### **un default** *(`termini=None`)* e ### **uno smistamento su `TIPO`**;
# ### togliere il default ha portato via il primo, e ### **rendere UNIFORME la firma
# ### dei generati** *(`energia(st, ii, jj)` per tutti)* ha portato via il secondo.
# ### ⭐ **UNA FIRMA UNIFORME E- UN RAMO IN MENO** *(`A8`)*, e non l-avevo
# ### previsto: ### **cercavo di pagare un debito, e ne ho pagati due.**

# =====================================================================================
#   IL NUCLEO, DICHIARATO UNO PER UNO -- **decisione di Luca del `2026-10-16`, `19:33`**
# -------------------------------------------------------------------------------------
# ### ⛔⛔ **`15` FUNZIONI, `27` RAMI, `0` DEFAULT.** ### ⚠ **Il conteggio lo misura
# ### l'AST; il RUOLO e il PERCHE' li ho scritti io LEGGENDOLI** -- ed e' il limite
# ### dichiarato in testa a questo file.
# ### 📌 **E UNA FUNZIONE HA UN SOLO RUOLO**, anche quando i suoi rami ne mescolano due:
# ### allora il ruolo e' **quello dominante**, e il `perche'` **nomina tutti i rami.**

# ------------------------------------------------------------------ `grafo.py`
RAMI[("primo_ordine/grafo.py", "errori")] = (
    5, "validazione",
    "le CINQUE forme malformate di un grafo, una per ramo: `ii` e `jj` di forma diversa, "
    "grafo VUOTO, indice FUORI dal numero dei nodi, AUTOANELLO, ARCO DOPPIO. ### Ogni "
    "ramo COSTRUISCE UN MESSAGGIO e non cambia nessun valore: e' il presidio stesso")
RAMI[("primo_ordine/grafo.py", "costo")] = (
    1, "smistamento",
    "sceglie fra il grafo PASSATO e la CATENA di prova. ### E dal `2026-10-16` l-argomento "
    "e' ESPLICITO (`costo(n, archi, giri)`, tetto zero sui default): `None` e' una SCELTA "
    "DICHIARATA del chiamante, non un valore mancante")
# ------------------------------------------------------------------ `incidenza.py`
RAMI[("primo_ordine/incidenza.py", "_allarga")] = (
    1, "smistamento",
    "il RADDOPPIO a capacita' preallocata: se la capacita' BASTA non si rialloca, e ### il "
    "ramo che NON FA NIENTE va dichiarato -- allargare <<per sicurezza>> sprecherebbe "
    "memoria senza che nessuno l-abbia deciso. ### Non protegge da un errore: EVITA un "
    "costo `O(m)` a ogni nascita, che su una corsa che cresce sarebbe `O(m^2)`")
RAMI[("primo_ordine/incidenza.py", "cresci")] = (
    2, "smistamento",
    "DUE rami: `tieni.dtype == bool` smista fra una MASCHERA e una lista di INDICI (due "
    "forme che il chiamante puo' avere), e l-`or` su `resta` VALIDA che gli indici "
    "superstiti stiano nel nuovo intervallo. ### Il secondo e' una validazione, il primo "
    "uno smistamento su un campo (il `dtype`), e nessuno dei due sceglie fisica")
RAMI[("primo_ordine/incidenza.py", "costo")] = (
    1, "smistamento",
    "scarta gli ARCHI DOPPI prima di misurare, tenendo la prima occorrenza di ogni coppia "
    "non ordinata. ### E' dentro un MISURATORE del costo: non tocca lo stato, e serve "
    "perche' misurare su un grafo con doppioni misurerebbe un grafo che non esiste")
RAMI[("primo_ordine/incidenza.py", "main")] = (
    1, "iterazione",
    "quanti GIRI di misura fare secondo la taglia (`50` sotto `10000` archi, `10` sopra). "
    "### La soglia e' DICHIARATA nel sorgente, e serve a non far durare la misura piu' "
    "del necessario: non entra in nessun risultato di fisica")
# ------------------------------------------------------------------ `materia_vuoto.py`
_SING = (
    "la SINGOLARITA' ELIMINABILE a `rho = 0`: dove non c-e- materia il valore si prende "
    "dal LIMITE, e NON e' un pavimento. ### E' FISICA GIA' DECISA, e il rimando e' la "
    "scheda della legge (`doc/leggi_era2/CAMM-MATERIA-VUOTO.md`): <<la fase di un vettore "
    "nullo non vuol dire niente>>, quindi la' `alpha = 0` ed e' il valore che "
    "l-espressione PRENDE dove e' definita. ### Il mandato del 2026-10-16 chiede "
    "esattamente questo: dichiararlo col rimando, senza deciderlo di nuovo")
RAMI[("primo_ordine/materia_vuoto.py", "N")] = (1, "smistamento", _SING)
RAMI[("primo_ordine/materia_vuoto.py", "alpha")] = (1, "smistamento", _SING)
RAMI[("primo_ordine/materia_vuoto.py", "beta")] = (1, "smistamento", _SING)
# ------------------------------------------------------------------ `motore.py`
RAMI[("primo_ordine/motore.py", "_b")] = (
    1, "smistamento",
    "il BUFFER si alloca UNA VOLTA per scena e poi si RIUSA: il ramo smista fra <<non "
    "c-e- ancora>> e <<c-e->>. ### E' il vincolo della memoria per tick PIATTA: allocare "
    "a ogni tick la farebbe crescere, e il conto e' misurato")
RAMI[("primo_ordine/motore.py", "cresci")] = (
    3, "smistamento",
    "TRE rami: `nuove` (due volte) smista fra <<in questo tick NON e' nato niente>> e "
    "<<sono nate delle estremita'>>, e `v is None` smista sulla VARIABILE ASSENTE -- una "
    "tabella che non dichiara `psi_h` o `phi_h` e' LEGITTIMA, e pretenderla qui vorrebbe "
    "dire che il motore sa quali leggi esistono, e NON LO SA")
RAMI[("primo_ordine/motore.py", "_somma_per_nodo")] = (
    3, "smistamento",
    "TRE rami: `self.sommatoria` scegli la VIA DELLA SOMMA, `ee.size == 0` il nodo senza "
    "estremita', `complesso` il tipo del campo. ### E LA VIA DELLA SOMMA CAMBIA I BIT (con "
    "tre addendi l-ordine conta), percio' NON e' un valore implicito: e' un ARGOMENTO "
    "ESPLICITO del motore (`Motore.__init__(self, inc, geo, st, dtau, sommatoria)`, senza "
    "default) -- verificato il 2026-10-16, come il mandato chiede")
# ### ⚠ **`motore.main` NON E' PIU' NEL NUCLEO** *(`2026-10-17`)*: era
# ### ### **un MISURATORE dentro un modulo del nucleo**, e `P-MOD` ha rifiutato il commit
# ### perche- `motore.py` era a ### **`699` righe su `700`.** ### **E' uscito in
# ### `_misura_costo_motore.py`**, e la sua riga ### **esce con lui.**
RAMI[("primo_ordine/saturazione.py", "pezzi")] = (
    1, "smistamento",
    "il LIMITE a `Lambda = 0` ESATTO: la' si usa la forma limite (`G' = 1`, "
    "`b = -(pi/2) sign(h)`), e NON e' un pavimento -- e' il valore che la funzione PRENDE "
    "la'. ### L-argomento sta nel docstring della funzione, con `A11`: un pavimento "
    "violerebbe `A11`, un LIMITE e' la funzione. ### ⚠ E la scheda della legge NON lo "
    "nomina: il buco e' riferito, e la legge e' fuori dall-ordine")
# ------------------------------------------------------------------ `tick.py`
RAMI[("primo_ordine/flussi_parziali.py", "dtau_nodo")] = (
    1, "smistamento",
    "il ramo della forma `cs` (`D0`, 2026-10-17): `mot.cs is None` vuol dire ### LA FORMA "
    "NON C-E-, e allora si ritorna `mot.dtau` TALE E QUALE -- cioe- il passo di oggi AL "
    "BIT, senza una moltiplicazione e senza un ulp. ### E `None` NON e- <<`Lambda_c` vale "
    "zero>>: la scala zero la funzione `cs` la RIFIUTA, e spegnere si fa NON ACCENDENDO")
RAMI[("primo_ordine/tick.py", "cs_al_centro")] = (
    2, "iterazione",
    "il PUNTO FISSO di `D2` (2026-10-17): `cs` si legge sullo stato AL CENTRO del"
    " palindromo, e per arrivare al centro serve `cs` -- quindi si itera. ### I DUE rami"
    " sono la CONDIZIONE DI ARRESTO (due giri che coincidono agli ulp, soglia RELATIVA al"
    " massimo di `cs` perche- un assoluto su una grandezza in [0,1) sarebbe una scala"
    " nascosta) e il ramo del `salta`, che qui e- vuoto. ### LA SOGLIA E- DICHIARATA e i"
    " GIRI SI RIPORTANO: massimo 47 misurato su 6 regimi, con contrazione fra 0.04 e 0.49,"
    " e il tetto di 120 e- IL NUMERO OLTRE IL QUALE SI DICHIARA CHE NON CONVERGE -- non una"
    " manopola")
RAMI[("primo_ordine/tick.py", "percorri_tick")] = (
    3, "smistamento",
    "TRE rami, tutti su CAMPI DICHIARATI: `idl not in salta` toglie dei pezzi per `id` "
    "(e `salta` lo passa il chiamante, esplicito), `k == 0 and al_primo is not None` "
    "chiama la FOTOGRAFIA dopo il primo pezzo, e `vuole_par` dice se l-operatore prende i "
    "parametri -- e viene dalla tabella `OPERATORE`, non da un indovinello. ### Nessuno "
    "dei tre scegli una legge: l-ordine e le frazioni vengono da `composizione.py`, che "
    "SI GENERA dalla tabella")


def _conta(p, base=None):
    """### I rami per funzione, ### **contati dall-AST.**"""
    arb = ast.parse(io.open(os.path.join(base or RADICE, p), encoding="utf-8").read(),
                    filename=p)
    fuori = {}
    for fn in [n for n in ast.walk(arb) if isinstance(n, ast.FunctionDef)]:
        c = 0
        for n in ast.walk(fn):
            if isinstance(n, (ast.If, ast.IfExp, ast.Try)):
                c += 1
            elif isinstance(n, ast.BoolOp) and isinstance(n.op, ast.Or):
                c += 1
        if c:
            fuori[fn.name] = c
    return fuori


def default_nelle_firme(p, base=None):
    """### I parametri con ### **un valore di default** in un file di fisica.

    ### ⛔ **IL PUNTO `15(b)`:** *<<un parametro non presente e- un ERRORE, e un
    controllo sull-AST RIFIUTA i valori di default nei moduli di fisica>>*.
    ### ⭐ **E la ragione e- `CONFIG-1`:** un default e- ### **un valore che gira
    senza che nessuno l-abbia scelto**, e `CONFIG-1` ha misurato dove porta --
    ### **`28` leggi su `31` che giravano SPENTE** senza che nessuno lo sapesse.
    """
    arb = ast.parse(io.open(os.path.join(base or RADICE, p), encoding="utf-8").read(),
                    filename=p)
    fuori = []
    for fn in [n for n in ast.walk(arb) if isinstance(n, ast.FunctionDef)]:
        a = fn.args
        nomi = [x.arg for x in a.args][len(a.args) - len(a.defaults):]
        nomi += [x.arg for x, v in zip(a.kwonlyargs, a.kw_defaults) if v is not None]
        for x in nomi:
            fuori.append((fn.name, x))
    return fuori


def controlla(base=None):
    """### ⛔ **SI APPLICA AL NUCLEO E BASTA**, e la regola lo dice: ### **fuori dal
    nucleo `P-R1` NON si applica** -- ### **niente eccezioni file per file** *(mandato di
    Luca del `2026-10-16`)*. ### **Chi vuole i numeri di fuori usa il CENSIMENTO**
    *(`csv/_censimento_rami.py`)*, che ### **non blocca.**
    """
    err = []
    visti = set()
    dentro = set(nucleo(base))
    # ### ⛔ **IL `15(b)`, PRIMA DI TUTTO:** nessun default nelle firme, ### **tetto
    # ### ZERO** -- e nel nucleo e' ### **rispettato** dal `2026-10-16`.
    for p in nucleo(base):
        for fn, arg in default_nelle_firme(p, base):
            err.append("`P-R1` `%s::%s`: il parametro `%s` HA UN VALORE DI DEFAULT. "
                       "### Il punto 15(b): un parametro NON PRESENTE e- un ERRORE, non "
                       "un comportamento a sorpresa -- e viene DALLA CONFIGURAZIONE. "
                       "### `CONFIG-1` ha misurato dove porta un valore che gira senza "
                       "che nessuno l-abbia scelto: 28 leggi su 31 SPENTE"
                       % (p, fn, arg))
    for p in nucleo(base):
        for fn, c in sorted(_conta(p, base).items()):
            visti.add((p, fn))
            riga = RAMI.get((p, fn))
            if riga is None:
                err.append("`P-R1` `%s::%s`: ha %d rami e NON E- DICHIARATO. "
                           "### `A8`: un ramo silenzioso non e- un ramo -- si dice "
                           "QUANTI e A CHE SERVONO, con un ruolo di %s"
                           % (p, fn, c, list(RUOLI)))
                continue
            quanti, ruolo, perche = riga
            if ruolo not in RUOLI:
                err.append("`P-R1` `%s::%s`: ruolo %r fuori vocabolario: %s"
                           % (p, fn, ruolo, list(RUOLI)))
            if quanti != c:
                err.append("`P-R1` `%s::%s`: dichiara %d rami e l-AST ne conta %d. "
                           "### Un ramo e- NATO o MORTO senza che nessuno lo dicesse"
                           % (p, fn, quanti, c))
            if len(str(perche or "")) < 30:
                err.append("`P-R1` `%s::%s`: il `perche-` e- di %d caratteri. "
                           "### Dire QUANTI senza dire A CHE SERVONO non e- dichiararli"
                           % (p, fn, len(str(perche or ""))))
    # ### ⚠ **UNA RIGA DICHIARATA PER UN FILE CHE NON E' PIU' NEL NUCLEO non e' un
    # ### errore:** il nucleo ### **si deriva**, e un modulo puo' uscirne perche' nessuno
    # ### lo importa piu'. ### **Resta un errore se il file E' nel nucleo e la funzione
    # ### non c'e' piu'.**
    for k in sorted(set(RAMI) - visti):
        if k[0] not in dentro:
            continue
        err.append("`P-R1` `%s::%s`: DICHIARATO e l-AST non lo trova. ### O la funzione "
                   "e- sparita, o non ha piu- rami: la riga va tolta" % k)
    return err


def rapporto():
    per_ruolo = {}
    for (p, fn), (q, r, _x) in RAMI.items():
        per_ruolo.setdefault(r, [0, 0])
        per_ruolo[r][0] += 1
        per_ruolo[r][1] += q
    return per_ruolo


def _finto_default():
    """Il caso che DEVE fallire: un default, su una ### **COPIA** del sorgente."""
    import tempfile
    t = io.open(os.path.join(RADICE, "primo_ordine", "passo.py"),
                encoding="utf-8").read()
    t2 = t.replace("def senza_cache(moduli, azione):",
                   "def senza_cache(moduli, azione=None):", 1)
    assert t2 != t
    d = tempfile.mkdtemp()
    p = os.path.join(d, "finto.py")
    io.open(p, "w", encoding="utf-8", newline=NL).write(t2)
    arb = ast.parse(io.open(p, encoding="utf-8").read())
    trovati = []
    for fn in [n for n in ast.walk(arb) if isinstance(n, ast.FunctionDef)]:
        a = fn.args
        if a.defaults:
            trovati.append(fn.name)
    os.remove(p)
    os.rmdir(d)
    return "senza_cache" in trovati


# =====================================================================================
#   I QUATTRO BRACCI DEL NUCLEO -- **su un albero FINTO, fuori dal repo**
# -------------------------------------------------------------------------------------
# ### ⛔⛔ **PERCHE' FUORI DAL REPO** *(punto `6` del mandato del `2026-10-16`)*: due
# ### collaudi di presidio che scrivevano nel repo e poi ripristinavano i byte hanno
# ### lasciato l'albero sporco ### **due volte** (`OSError: [Errno 22]`). ### ✅ **Qui non
# ### c'e' niente da ripristinare**, e il controllo e' `git status`.
# ### ⭐ **E si puo' fare perche' `nucleo()` e `controlla()` prendono `base`:** la mappa e
# ### i file si leggono da la', e la DERIVAZIONE e' la stessa che gira sul repo.
_MAPPA_FINTA = """versione: 1
tetto_righe: 700
moduli:
  - nome: tick.py
    responsabilita: finto
    importa: []
  - nome: passo.py
    responsabilita: finto
    importa: []
  - nome: motore.py
    responsabilita: finto
    importa: [%s]
  - nome: materia_vuoto.py
    responsabilita: finto
    importa: []
  - nome: saturazione.py
    responsabilita: finto
    importa: []
  - nome: nuovo.py
    responsabilita: finto
    importa: []
  - nome: _collauda_finto.py
    responsabilita: finto
    importa: []
"""


def _albero_finto(base, motore_importa, motore_src, passo_src, nuovo_src, coll_src):
    po = os.path.join(base, "primo_ordine")
    if not os.path.isdir(po):
        os.makedirs(po)
    io.open(os.path.join(po, "_mappa.yaml"), "wb").write(
        (_MAPPA_FINTA % motore_importa).encode("utf-8"))
    for nome, src in (("tick.py", "X = 1" + NL), ("materia_vuoto.py", "X = 1" + NL),
                      ("saturazione.py", "X = 1" + NL), ("motore.py", motore_src),
                      ("passo.py", passo_src), ("nuovo.py", nuovo_src),
                      ("_collauda_finto.py", coll_src)):
        io.open(os.path.join(po, nome), "wb").write(src.encode("utf-8"))
    return po


def bracci_del_nucleo(esito):
    import shutil
    import tempfile
    PULITO = "X = 1" + NL
    RAMO = ("def finta(x):" + NL + "    if x:" + NL + "        return 1" + NL
            + "    return 0" + NL)
    DFLT = ("def finta2(x, quanti=3):" + NL + "    return x * quanti" + NL)
    base = tempfile.mkdtemp(prefix="pr1_")
    try:
        # ### ⛔⛔ **I BRACCI SONO DIFFERENZIALI, e il motivo e' MISURATO:** sul
        # ### l-albero finto `controlla` da' ### **`15` errori DI FONDO**, perche' le righe
        # ### VERE di `RAMI` nominano funzioni che ### **il finto non ha.** ### ✅ **Quindi
        # ### si guarda la DIFFERENZA da un albero PULITO**: cosi' il braccio dice
        # ### ### **<<questo errore e' NATO dal mio caso finto>>**, e non
        # ### ### **<<ci sono errori>>**.
        _albero_finto(base, "", PULITO, PULITO, PULITO, PULITO)
        fondo = controlla(base)

        def nuovi():
            return [x for x in controlla(base) if x not in fondo]

        esito("### il FONDO dell-albero finto e' noto, e i bracci guardano la DIFFERENZA",
              bool(fondo) and not nuovi(),
              "### %d errori di fondo (le righe vere citano funzioni che il finto non ha),"
              " e sul pulito la differenza e' VUOTA" % len(fondo))
        # ### ⛔ **① UN RAMO NUOVO NON DICHIARATO IN UN FILE DEL NUCLEO.**
        _albero_finto(base, "", RAMO, PULITO, PULITO, PULITO)
        e = nuovi()
        esito("### ① DEVE fallire: un ramo NUOVO non dichiarato in un file del NUCLEO",
              any("motore.py::finta" in x and "NON E- DICHIARATO" in x for x in e),
              "### %d errori NUOVI, e il nucleo derivato dalla mappa finta e' %d file"
              % (len(e), len(nucleo(base))))
        # ### ⛔ **② UN DEFAULT IN UN FILE DEL NUCLEO: il tetto e' ZERO.**
        _albero_finto(base, "", PULITO, DFLT, PULITO, PULITO)
        e = nuovi()
        esito("### ② DEVE fallire: un `default` in una firma del NUCLEO (tetto ZERO)",
              any("passo.py::finta2" in x and "VALORE DI DEFAULT" in x for x in e),
              "### %d errori NUOVI" % len(e))
        # ### ⛔⛔ **③ UN FILE CHE ENTRA NEL NUCLEO PER IMPORT, e porta rami non
        # ### dichiarati.** ### **E' la prova che la DERIVAZIONE lavora**: il file non e'
        # ### in nessuna lista, e ### **ci entra perche' il motore lo importa.**
        _albero_finto(base, "", PULITO, PULITO, RAMO, PULITO)
        prima = nuovi()
        _albero_finto(base, "nuovo", PULITO, PULITO, RAMO, PULITO)
        dopo = nuovi()
        esito("### ③ DEVE fallire: un file che ENTRA nel nucleo per import, coi suoi rami",
              not prima and any("nuovo.py::finta" in x for x in dopo),
              "### senza l-import: %d errori nuovi; con l-import: %d. ### Il file e' lo"
              " STESSO: cambia solo CHI LO IMPORTA" % (len(prima), len(dopo)))
        # ### ⭐⭐ **IL CASO CHE DEVE PASSARE: un ramo nuovo in un COLLAUDO fuori dal
        # ### nucleo.** ### **Senza questo, <<fuori dal nucleo non si applica>> sarebbe
        # ### una frase e non un fatto.**
        _albero_finto(base, "", PULITO, PULITO, PULITO, RAMO)
        e = nuovi()
        esito("### (c) DEVE PASSARE: un ramo nuovo in un COLLAUDO fuori dal nucleo",
              not e,
              "### %d errori nuovi: fuori dal nucleo `P-R1` NON si applica, e il collaudo"
              " finto ha 1 ramo" % len(e))
    finally:
        shutil.rmtree(base, ignore_errors=True)


def collaudo():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-64s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL COLLAUDO DI `P-R1` -- nei DUE VERSI")
    print("=" * 100)
    tot = sum(q for q, _r, _p in RAMI.values())
    esito("sul disco: `P-R1` TACE", controlla() == [],
          "%d rami in %d funzioni" % (tot, len(RAMI)))
    esito("### il braccio sopra HA MATERIA (ci sono rami da dichiarare)", tot >= 15,
          "%d rami: se fosse 0 il braccio sarebbe un FALSO-UNO. ### Erano 27, e il "
          "punto 15(b) ne ha tolti 8" % tot)
    # --- un ramo NUOVO non dichiarato
    salva = dict(RAMI)
    try:
        del RAMI[("primo_ordine/passo.py", "valida_composizione")]
        esito("### DEVE scattare: una funzione con rami e NON dichiarata",
              any("NON E- DICHIARATO" in e for e in controlla()),
              "`A8`: un ramo silenzioso non e- un ramo")
    finally:
        RAMI.clear()
        RAMI.update(salva)
    # --- un conteggio SBAGLIATO
    salva2 = RAMI[("primo_ordine/passo.py", "valida_composizione")]
    try:
        RAMI[("primo_ordine/passo.py", "valida_composizione")] = (99, "validazione",
                                                                  salva2[2])
        esito("### DEVE scattare: un CONTEGGIO che non coincide con l-AST",
              any("l-AST ne conta" in e for e in controlla()),
              "### un ramo NATO o MORTO senza che nessuno lo dicesse")
    finally:
        RAMI[("primo_ordine/passo.py", "valida_composizione")] = salva2
    # --- un ruolo fuori vocabolario, e un `perche'` troppo corto
    try:
        RAMI[("primo_ordine/passo.py", "valida_composizione")] = (6, "quasi-validazione",
                                                                  salva2[2])
        esito("### DEVE scattare: un RUOLO fuori vocabolario",
              any("fuori vocabolario" in e for e in controlla()))
        RAMI[("primo_ordine/passo.py", "valida_composizione")] = (6, "validazione", "x")
        esito("### DEVE scattare: un `perche-` troppo corto",
              any("non e- dichiararli" in e for e in controlla()),
              "### dire QUANTI senza dire A CHE SERVONO non e- dichiararli")
    finally:
        RAMI[("primo_ordine/passo.py", "valida_composizione")] = salva2
    # --- una riga ORFANA
    try:
        RAMI[("primo_ordine/passo.py", "funzione_che_non_esiste")] = (1, "guardia",
                                                                      "x" * 40)
        esito("### DEVE scattare: una riga DICHIARATA che l-AST non trova",
              any("l-AST non lo trova" in e for e in controlla()))
    finally:
        RAMI.pop(("primo_ordine/passo.py", "funzione_che_non_esiste"), None)
    esito("NON deve scattare: rimesso tutto a posto, `P-R1` TACE", controlla() == [],
          "### i bracci di sopra scattavano per i loro casi finti")
    # --- E IL RAPPORTO: i `default` erano NOVE, e il punto `15(b)` li ha TOLTI
    r = rapporto()
    # ### ⛔ **IL `15(b)`: i default sono ZERO, e il braccio che DEVE scattare.**
    esito("`15(b)` i DEFAULT nelle firme della fisica sono ZERO",
          not any("VALORE DI DEFAULT" in e for e in controlla()),
          "### erano NOVE il 2026-10-09, e il punto 15(b) li ha TOLTI")
    esito("### DEVE scattare: un default in una firma di fisica",
          _finto_default(),
          "### misurato su una COPIA del sorgente, non sul file vero")
    esito("### e i `default` NON sono piu- nella tabella dei ruoli",
          "default" not in rapporto(),
          "### il debito e- PAGATO: 27 rami -> 19, e 9 default -> 0")
    # ### ⛔ **QUESTO BRACCIO ASSERIVA <<ZERO GUARDIE>>, E DAL 2026-10-12 NON E-
    # ### PIU- VERO: ce ne sono SETTE**, una per ogni LEGAME generato della camminata.
    # ### ⭐ **E `A11` CHIEDE L-ERRORE DA CUI PROTEGGONO, non il permesso: eccolo.**
    # ### Un legame e- la riga di tabella di un `pezzo_unitario` o di un `flusso`, e
    # ### ### **il suo operatore vive nel MOTORE**: la guardia scatta quando
    # ### ### **la tabella dichiara un operatore che il motore NON HA**, cioe- quando la
    # ### biiezione ### **tabella <-> motore** e- rotta.
    # ### ⚠ **E oggi quell-errore E- LO STATO NORMALE, perche- il motore non c-e-
    # ### ancora** *(e- il pezzo `5` del simulatore)*: la guardia e- cio- che fa
    # ### ### **ALZARE** invece di far sembrare funzionante un legame vuoto.
    # ### ✅ **Quando il motore arrivera-, quell-errore diventera- un difetto di
    # ### COSTRUZIONE** *(una legge in tabella senza il suo operatore)*, e la guardia
    # ### restera- a nominarlo.
    # ### ⛔⛔ **E IL NUMERO NON SI SCRIVE A MANO, dal `2026-10-16`:** era
    # ### ### **`7`**, e quando `CAMM-MATERIA-VUOTO` e- entrata in tabella sono
    # ### diventati ### **`8`** -- cioe- il braccio ### **FALLIVA per una legge NUOVA**,
    # ### che e- esattamente cio- che NON deve segnalare. ### ✅ **Si CONTANO i legami
    # ### generati** *(`primo_ordine/termini/*.py`)*, cosi- una legge nuova entra da
    # ### sola. ### ⚠ **Non e- una soglia aggiustata: e- un numero che DEVE seguire la
    # ### tabella, e scritto a mano non la seguiva.**
    # ### ⚠ **E <<legame>> vuol dire <<ha `applica`>>, non <<sta in `termini/`>>:**
    # ### i due termini di PROVA (`PROVA-HOPPING`, `PROVA-LOCALE`) sono generati la-
    # ### dentro ma ### **non sono legami** -- hanno le DERIVATE, non un operatore del
    # ### motore. ### **Il primo conto diceva `10` contro `8` guardie, e il braccio lo
    # ### ha detto.**
    # ### ⛔⛔ **DAL `2026-10-16` I LEGAMI GENERATI SONO FUORI DAL NUCLEO**, e le
    # ### loro `8` righe di `RAMI` sono state ### **togliate**: una dichiarazione per un
    # ### file che il presidio non guarda piu' sarebbe ### **una riga morta.**
    # ### ✅ **MA IL CONTROLLO NON SI PERDE: DIVENTA DERIVATO.** Non chiede piu' una
    # ### riga per legame; chiede che ### **ogni legame generato abbia ESATTAMENTE la sua
    # ### guardia**, contata dall-AST. ### **Cosi' una legge nuova entra da sola, e una
    # ### guardia che spariva si vedrebbe.**
    # ### ⭐ **E `A11` HA IL SUO ERRORE, che resta quello di prima:** la guardia scatta
    # ### quando ### **la tabella dichiara un operatore che il MOTORE non ha**, cioe' quando
    # ### la biiezione ### **tabella <-> motore** e' rotta.
    # ### ⚠ **E <<legame>> vuol dire <<ha `applica`>>, non <<sta in `termini/`>>:** i
    # ### termini di PROVA sono generati la' dentro e ### **non sono legami** -- hanno le
    # ### derivate, non un operatore del motore.
    legami, senza = [], []
    for _x in sorted(glob.glob(os.path.join(RADICE, "primo_ordine", "termini", "*.py"))):
        _t = io.open(_x, encoding="utf-8").read()
        if "def applica(" not in _t:
            continue
        _rel = os.path.relpath(_x, RADICE).replace(os.sep, "/")
        legami.append(_rel)
        if _conta(_rel).get("applica") != 1:
            senza.append((_rel, _conta(_rel).get("applica")))
    esito("### ogni LEGAME generato ha ESATTAMENTE la sua guardia (contata, non dichiarata)",
          bool(legami) and not senza,
          "### %d legami generati, %d senza la loro guardia%s. ### L-errore che la guardia "
          "nomina: la tabella dichiara un operatore che il MOTORE non ha, cioe- la "
          "biiezione tabella <-> motore rotta" % (len(legami), len(senza),
                                                  ("   " + str(senza)) if senza else ""))
    bracci_del_nucleo(esito)
    print("=" * 100)
    print("IL COLLAUDO DI `P-R1`: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--collaudo" in argv:
        return collaudo()
    err = controlla()
    tot = sum(q for q, _r, _p in RAMI.values())
    n = nucleo()
    print("  `P-R1`: %d rami dichiarati in %d funzioni, sui %d file del NUCLEO"
          % (tot, len(RAMI), len(n)))
    print("     il nucleo, DERIVATO dalle radici %s: %s"
          % (" ".join(RADICI), " ".join(x.split("/")[-1] for x in n)))
    print("     ### e FUORI dal nucleo `P-R1` NON si applica: i numeri di fuori stanno"
          " nel CENSIMENTO (`csv/_censimento_rami.py`), che NON blocca")
    for r, (nf, nr) in sorted(rapporto().items()):
        print("     %-14s %2d funzioni, %2d rami%s"
              % (r, nf, nr,
                 "   ### un DEBITO: il punto 15(b) lo vietera-" if r == "default"
                 else ("   ### `A11`: cercare l-errore" if r == "guardia" else "")))
    for e in err[:14]:
        print("  ### %s" % e)
    print("  ### %d errori" % len(err))
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
