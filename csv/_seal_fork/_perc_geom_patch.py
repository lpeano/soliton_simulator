# -*- coding: utf-8 -*-
"""**LA PATCH DEL `COMMIT 5`, e serve DUE VOLTE: per curare e per COSTRUIRE i casi.**

### Una sostituzione alla volta, con l'ancora CONTATA e il fallimento se non e' unica
*(`P1-quater`)*. Un `assert` globale del tipo *«il testo e' cambiato»* sarebbe soddisfatto
dalle ALTRE sostituzioni e lascerebbe passare in silenzio quella che non ha attaccato.

### E NIENTE ESCAPE NEI LETTERALI *(`P1-quater`)*: dove serve un carattere si usa `chr()`.

## LE OPZIONI

| | |
|---|---|
| *(nessuna)* | ### **la cura intera**: vincolo 4 + la derivazione + le due regole |
| `--solo-ordine` | ### **SOLO il vincolo 4**, eredita' INVARIATA — e' il braccio `A` del sigillo |
| `--solo-divisione` | solo la DIVISIONE derivata: lo ### **Schwinger EREDITA ancora** |
| `--solo-schwinger` | solo lo SCHWINGER derivato: la ### **divisione EREDITA ancora** |
| `--inietta-tw=N` | i nuovi archi nascono con ### **`tw = N`** invece di `0` — ### **il caso COSTRUITO** dei bracci `D` ed `E` |

### 📌 **PERCHE' `--inietta-tw` ESISTE, e non e' un trucco:** eredita' e derivazione danno
### **lo stesso valore oggi** *(1225 nati, tutti `-1`: censimento `e12158b`)*, quindi un
controllo che confronta le due ### **non puo' fallire.** Con `tw` sopra `PHI_CRIT` la
derivazione da' `+1` e l'eredita' resta `-1`: ### **allora la differenza SI VEDE.**
### **E' la tecnica dell'ulp iniettato: il caso che serve non si spera, si COSTRUISCE.**

**USO:** `python csv/_seal_fork/_perc_geom_patch.py --file=<copia> [opzioni]`
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
NL = chr(10)

P = None
SOLO_ORDINE = SOLO_DIV = SOLO_SCH = False
INIETTA = None
for _a in sys.argv[1:]:
    if _a.startswith("--file="):
        P = _a.split("=", 1)[1]
    elif _a == "--solo-ordine":
        SOLO_ORDINE = True
    elif _a == "--solo-divisione":
        SOLO_DIV = True
    elif _a == "--solo-schwinger":
        SOLO_SCH = True
    elif _a.startswith("--inietta-tw="):
        INIETTA = float(_a.split("=", 1)[1])
    else:
        raise SystemExit("** opzione sconosciuta: %s **" % _a)
if not P or not os.path.isfile(P):
    raise SystemExit("** serve `--file=<copia del simulatore>` **")

t = io.open(P, encoding="utf-8").read()
fatte = []


def sost(ancora, nuovo, etichetta):
    """### CONTA l'ancora e FALLISCE se non e' unica. Una per volta."""
    global t
    n = t.count(ancora)
    if n != 1:
        raise SystemExit("** %s: ancora trovata %d volte, non 1 **" % (etichetta, n))
    t = t.replace(ancora, nuovo)
    fatte.append(etichetta)


# ========================================================== 1. IL VINCOLO 4 NELL'ORDINE
A1 = """    fuori = []
    for blocco in (REGISTRO_METRI, REGISTRO_STATO, REGISTRO_FINESTRA):
        for voce in blocco:
            fuori.append(voce[0])
            if voce[0] == "peq":
                fuori.append("_peqn_idx")   # vincolo 2: DOPO `peq`
    return tuple(fuori)"""

N1 = """    fuori = []
    visto_pgeom = False
    for blocco in (REGISTRO_METRI, REGISTRO_STATO, REGISTRO_FINESTRA):
        for voce in blocco:
            if voce[0] == "perc_geom":
                # ### VINCOLO 4: `perc_geom` si colloca DOPO `tw`, non qui.
                visto_pgeom = True
                continue
            fuori.append(voce[0])
            if voce[0] == "peq":
                fuori.append("_peqn_idx")   # vincolo 2: DOPO `peq`
            if voce[0] == "tw":
                fuori.append("perc_geom")   # vincolo 4: la DERIVAZIONE legge `tw`
    # ### I DUE PRESIDI DEL VINCOLO 4, e non sono decorativi: senza di loro un cambio
    #   nei registri romperebbe il vincolo IN SILENZIO, e la derivazione leggerebbe un
    #   `tw` che non c'e' ancora -- cioe' tornerebbe a essere la costante `-1`
    #   travestita. `A9`: un vincolo SCRITTO non e' un presidio.
    if not visto_pgeom:
        raise RuntimeError(
            "`perc_geom` NON sta nei registri, ma il vincolo 4 la colloca dopo `tw`: "
            "l'ordine di nascita conterrebbe una grandezza che il registro non "
            "dichiara. Il vincolo 4 va rifatto insieme al registro.")
    if "perc_geom" not in fuori:
        raise RuntimeError(
            "`tw` NON sta nei registri, quindi il vincolo 4 non ha dove collocare "
            "`perc_geom`, e la grandezza SPARIREBBE dall'ordine di nascita -- cioe' il "
            "presidio del punto unico la segnalerebbe come non dichiarata. Il vincolo 4 "
            "va rifatto insieme al registro.")
    return tuple(fuori)"""

A1D = '''    """L'ORDINE in cui la nascita scrive, e si DERIVA dai registri.

    L'ordine del REGISTRO -- `METRI`, poi `STATO`, poi `FINESTRA` -- con
    ### `_peqn_idx` DICHIARATO subito dopo `peq`, che e' il vincolo 2 del
    contratto. ### Si DERIVA e non si scrive a mano, cosi' una voce nuova nel
    registro fa scattare il presidio invece di passare inosservata.
    """'''

N1D = '''    """L'ORDINE in cui la nascita scrive, e si DERIVA dai registri.

    L'ordine del REGISTRO -- `METRI`, poi `STATO`, poi `FINESTRA` -- con DUE
    grandezze COLLOCATE da un vincolo dichiarato:

    | | il vincolo | perche' |
    |---|---|---|
    | **2** | `_peqn_idx` subito **dopo `peq`** | l'indice segue la grandezza che indicizza |
    | **4** | `perc_geom` **dopo `tw`** | ### **la sua DERIVAZIONE LEGGE `tw`** |

    ### IL VINCOLO 4, E PERCHE' NON E' UN RIORDINO DI COMODO (`COMMIT 5`, 2026-10-03):
    `perc_geom` si DERIVA dalla sua definizione -- la media di `|tw|` sugli archi del
    nodo contro `PHI_CRIT`, la stessa di `chi_basc`. Nell'ordine del registro
    `perc_geom` cadeva **PRIMA di `tw`** (posto 17 contro 31), cioe' ### **prima che i
    nuovi archi avessero una torsione**: una derivazione scritta la' avrebbe letto lo
    stato VECCHIO e avrebbe dato `-1` ### **per il motivo sbagliato** -- la costante
    `-1` travestita da derivazione. ### E' una DIPENDENZA DI LETTURA, non una manopola.

    ### Si DERIVA e non si scrive a mano, cosi' una voce nuova nel registro fa scattare
    il presidio invece di passare inosservata.
    """'''

# ### IL VINCOLO 4 SI APPLICA SEMPRE, E IL COLLAUDO HA PROVATO CHE SERVE.
#   La prima stesura lo saltava con `--solo-divisione`/`--solo-schwinger`: la
#   derivazione finiva al posto 17, cioe' ### PRIMA che `tw` fosse scritto, e leggeva
#   lo stato VECCHIO. ### Con `--inietta-tw` il `tw = 20` NON SI SAREBBE VISTO, la
#   derivazione avrebbe dato `-1`, e io avrei letto quel `-1` come <<il braccio D
#   funziona>>. ### Un caso costruito che non arriva al bersaglio e' PEGGIO di un caso
#   mancante: sembra una misura.
sost(A1, N1, "vincolo 4: `perc_geom` DOPO `tw`, coi due presidi")
sost(A1D, N1D, "il docstring dell'ordine: il vincolo 4 dichiarato")

# ====================================================== 2. LA FUNZIONE DI DERIVAZIONE
A2 = """def nascita(net, evento, c):"""

N2 = '''def _derivazione_perc_geom(net, c):
    """### LA DERIVAZIONE DI `perc_geom` PER I NATI, DALLA SUA DEFINIZIONE.

    ### `+1` se la media di `|tw|` sugli archi del nodo supera `PHI_CRIT`, altrimenti
    `-1`. ### E' la STESSA definizione di `chi_basc`, non una regola parallela:
    `chi_basc` la riapplica a TUTTA la rete al passo dopo, e ### **se il nato nascesse
    con un valore che la definizione non da', il sistema si contraddirebbe per un
    passo** -- e quel passo il frame-drag lo LEGGE.

    ### PERCHE' UNA DERIVAZIONE E NON LA COSTANTE `-1` *(decisione di Luca, 2026-09-29)*:
    oggi il nato ha archi con `tw = 0`, quindi la derivazione ### **da' `-1` sempre** --
    e scrivere `-1` darebbe lo STESSO numero. ### Ma `DIVISIONE-AUTOCONSISTENTE`, se
    decidera' che i figli nascono con una torsione, ### **cambierebbe la risposta**: una
    costante resterebbe `-1` e sarebbe ### **sbagliata in silenzio**, una derivazione
    segue. ### E i contatori `_g_pgeom_der_m1`/`_p1` esistono per questo: dicono
    ### **quante volte la derivazione ha davvero DECISO**, invece di far credere a una
    costante che ha deciso.

    ### LE DUE DIFFERENZE DA `chi_basc`, DICHIARATE e non nascoste:

    | | `chi_basc` | qui, alla nascita |
    |---|---|---|
    | il grado | `self._deg` | ### **RICALCOLATO da `i`/`j`** -- `_grado()` e' `collocata` e gira **DOPO** `nascita()`, quindi dentro la nascita `_deg` e' **STANTIO** |
    | la torsione | `_tw_t`, uno ### **SNAPSHOT** preso prima nel passo | ### **`net.tw`** -- alla nascita non esiste nessuno snapshot |

    ### E NON LEGGE `self.n` *(vincolo 3 del contratto)*: il numero dei nodi del DOPO si
    ricava da `c["n0"] + c["quante"]`.
    """
    n0 = int(c["n0"])
    quante = int(c["quante"])
    n = n0 + quante
    if quante <= 0 or n <= 0 or not len(net.i):
        return np.zeros(0, dtype=net.perc_geom.dtype)
    # il GRADO, come lo calcola `_grado()` -- che qui non e' ancora girato
    deg = np.maximum(np.bincount(net.i, minlength=n) +
                     np.bincount(net.j, minlength=n), 1)[:n]
    twabs = np.abs(net.tw)
    twn = np.zeros(n)
    np.add.at(twn, net.i, twabs)
    np.add.at(twn, net.j, twabs)
    twn = twn / deg
    nuovi = np.where(twn[n0:n] > PHI_CRIT, 1, -1).astype(net.perc_geom.dtype)
    net._g_pgeom_der_m1 = getattr(net, "_g_pgeom_der_m1", 0) + int(np.sum(nuovi < 0))
    net._g_pgeom_der_p1 = getattr(net, "_g_pgeom_der_p1", 0) + int(np.sum(nuovi > 0))
    return nuovi


def nascita(net, evento, c):'''

if not SOLO_ORDINE:
    sost(A2, N2, "la funzione `_derivazione_perc_geom`, con le due differenze dichiarate")

# ================================================ 3. LE DUE REGOLE, una per volta
A3 = '''@_nascita_regola("divisione", "perc_geom", "eredita la geometria del genitore `a`",
                 "self.perc_geom = np.concatenate([self.perc_geom, self.perc_geom[a]])",
                 "[CHI_COOP] la geometria NON e' coniugata: e' un giro compiuto o no, e si "
                 "eredita tale")
def _rn_div_perc_geom(net, c):
    net.perc_geom = np.concatenate([net.perc_geom, net.perc_geom[c["a"]]])'''

N3 = '''@_nascita_regola("divisione", "perc_geom", "DERIVATA dalla definizione (non eredita)",
                 "self.perc_geom = np.concatenate([self.perc_geom, "
                 "_derivazione_perc_geom(self, c)])",
                 "[COMMIT 5, decisione di Luca del 2026-09-29] ### NON SI EREDITA PIU': la "
                 "geometria e' *<<il giro e' compiuto o no>>*, e questo si LEGGE dagli archi "
                 "del nodo -- la media di `|tw|` contro `PHI_CRIT`, la STESSA definizione di "
                 "`chi_basc`. Un valore EREDITATO poteva CONTRADDIRE la definizione, e per un "
                 "passo il frame-drag lo leggeva. ### Il nato ha archi con `tw = 0`, quindi "
                 "OGGI la derivazione da' `-1`; scritta come DERIVAZIONE e non come costante "
                 "resta giusta quando `DIVISIONE-AUTOCONSISTENTE` dara' ai figli una torsione")
def _rn_div_perc_geom(net, c):
    net.perc_geom = np.concatenate([net.perc_geom, _derivazione_perc_geom(net, c)])'''

A4 = '''@_nascita_regola("schwinger", "perc_geom", "eredita NON invertita (la GEOMETRIA non si "
                 "coniuga)",
                 "self.perc_geom = np.concatenate([self.perc_geom, self.perc_geom[aa]])",
                 "[CHI_COOP via 3 di 3] ### SCELTA DICHIARATA, NON OVVIA: la CARICA nasce "
                 "opposta (e' antimateria); la GEOMETRIA no, copiata tale e quale, perche' "
                 "non e' una carica e non si coniuga. E `chi_basc` la riscrive al passo dopo")
def _rn_sch_perc_geom(net, c):
    net.perc_geom = np.concatenate([net.perc_geom, net.perc_geom[c["aa"]]])'''

N4 = '''@_nascita_regola("schwinger", "perc_geom", "DERIVATA dalla definizione (non eredita)",
                 "self.perc_geom = np.concatenate([self.perc_geom, "
                 "_derivazione_perc_geom(self, c)])",
                 "[COMMIT 5, decisione di Luca del 2026-09-29] ### LA SCELTA VECCHIA ERA "
                 "DICHIARATA E NON OVVIA -- la CARICA nasce opposta (e' antimateria), la "
                 "GEOMETRIA copiata tale e quale -- e la decisione di Luca la SUPERA ALLA "
                 "RADICE: la geometria non si EREDITA affatto, ne' diritta ne' coniugata, "
                 "perche' si LEGGE dagli archi del nodo (media di `|tw|` contro `PHI_CRIT`, "
                 "la definizione di `chi_basc`). ### Cosi' la domanda *<<si coniuga o no?>>* "
                 "non si pone: non e' una carica, e' una MISURA sugli archi")
def _rn_sch_perc_geom(net, c):
    net.perc_geom = np.concatenate([net.perc_geom, _derivazione_perc_geom(net, c)])'''

if not SOLO_ORDINE:
    if not SOLO_SCH:
        sost(A3, N3, "la regola della DIVISIONE: derivata, non ereditata")
    if not SOLO_DIV:
        sost(A4, N4, "la regola dello SCHWINGER: derivata, non ereditata")

# ============================================ 4. IL CASO COSTRUITO: `tw` sopra soglia
if INIETTA is not None:
    sost('''def _rn_div_tw(net, c):
    zz = np.zeros(c["quante"])
    net.tw = np.concatenate([net.tw[c["keep"]], zz, zz])''',
         '''def _rn_div_tw(net, c):
    # ### CASO COSTRUITO DEL SIGILLO: `tw` SOPRA `PHI_CRIT` sui nuovi archi, cosi' la
    #   derivazione di `perc_geom` deve dare `+1`. NON e' una cura: e' l'ulp iniettato.
    zz = np.full(c["quante"], %r)
    net.tw = np.concatenate([net.tw[c["keep"]], zz, zz])''' % INIETTA,
         "caso costruito: `tw = %g` sui nuovi archi della DIVISIONE" % INIETTA)
    sost('''def _rn_sch_tw(net, c):
    zz2 = np.zeros(c["nc"])
    net.tw = np.concatenate([net.tw, zz2, zz2])''',
         '''def _rn_sch_tw(net, c):
    # ### CASO COSTRUITO DEL SIGILLO, come sopra.
    zz2 = np.full(c["nc"], %r)
    net.tw = np.concatenate([net.tw, zz2, zz2])''' % INIETTA,
         "caso costruito: `tw = %g` sui nuovi archi dello SCHWINGER" % INIETTA)

io.open(P, "w", encoding="utf-8", newline=NL).write(t)
print("=" * 92)
for f in fatte:
    print("  OK  " + f)
if SOLO_ORDINE:
    print("  ### SOLO IL VINCOLO 4: l'eredita' NON e' toccata (braccio `A` del sigillo)")
if SOLO_DIV:
    print("  ### SOLO LA DIVISIONE derivata: lo SCHWINGER EREDITA ancora")
if SOLO_SCH:
    print("  ### SOLO LO SCHWINGER derivato: la DIVISIONE EREDITA ancora")
if INIETTA is not None:
    print("  ### E `tw = %g` INIETTATO: il caso COSTRUITO dei bracci `D` ed `E`" % INIETTA)
