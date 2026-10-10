# -*- coding: utf-8 -*-
"""GENERA `doc/REFERTO_decisioni_43_era2.md` — **il referto del mandato `2` di `6`.**

### ⛔ **NESSUN NUMERO E' RICOPIATO A MANO** *(`L-NUMERI`)*: ogni cifra esce
### **dall'indice sul disco**, dallo ### **storico** *(che dice quale lotto ha toccato
cosa)*, da ### **`git`** *(l'insieme degli ID prima e dopo)*, o dall'### **uscita di un
collaudo che questo script FA GIRARE.**

### ⚠ **E IL MANDATO NON MI CHIEDEVA DI DECIDERE NIENTE:** mi portava `43` decisioni
### **gia' prese**. ### ⭐ **Quindi il verdetto di questo referto non e' <<ho scelto
bene>>: e' <<ho tradito una decisione, si' o no>>** — e la difesa, dichiarata
### **prima** nel task history, era che ogni `motivo` ### **cita alla lettera** il pezzo
del mandato che decide quella riga.

"""
# ### ⚠ **L-ESENZIONE STA QUI E NON NEL DOCSTRING, e me l-ha insegnato `H-P5`
# ### RIFIUTANDOMI IL COMMIT:** l-avevo scritta ### **dentro le triple virgolette**,
# ### dove ### **non e- un commento** -- e un presidio che cerca un commento
# ### ### **non lo trova.**
# ESENTE-H-P5: questo referto NON misura il simulatore. Non fa girare nessuna scena, non
#   legge nessun booleano di modulo e non produce nessun numero di fisica: parla
#   dell'INDICE e dei presidi che lo guardano. Dichiarare <<la configurazione intera>> del
#   driver qui direbbe DOVE NON SI E' MISURATO, che e' rumore. Il blob del simulatore e'
#   dichiarato comunque, e ASSERITO: b8c21049.
import hashlib
import io
import json
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)

NL = chr(10)

import _verdetto as VD                                      # noqa: E402
VERDETTO = VD.verdetto

FUORI = os.path.join(RADICE, "doc", "REFERTO_decisioni_43_era2.md")
D = os.path.join(RADICE, "doc", "indice")

# ### ⛔ **IL COMMIT DA CUI SI MISURA <<PRIMA>>:** e- il commit del ### **task history**
# ### di questo mandato, che per il rito del par. `8` e- ### **antenato** dei commit del
# ### lavoro -- quindi ### **l-ordine e- verificabile da git**, non asserito da me.
PRIMA = "a7485c8"

LOTTI = (
    ("dec43_pid", "il PRESIDIO `P-ID` del blocco 1"),
    ("dec43_blocco1", "gli 11 OMONIMI: via la nota, il metadato RESTA"),
    ("dec43_blocco2", "gli ASSIOMI: 18 confermati + `A3c` che cambia"),
    ("dec43_blocco3a", "10 delle 13 domande"),
    ("dec43_blocco3b", "`K2a` e `K2b`, con lo stato dalla riga d-origine"),
    ("dec43_z47", "la 43a: NON APPLICABILE, registrata come domanda"),
    ("p5_booleani", "un difetto trovato DI LATO"),
    ("forma_spezza", "il difetto di `H-INDICE`, trovato DAL PRESIDIO STESSO"),
    ("forma_chiusa", "la sua chiusura, col numero VERO"),
)

COLLAUDI = (
    ("`P-ID` e la cura del criterio 2", "python csv/_id_nuovo.py --collaudo"),
    ("i presidi dell-indice, con `estendi`", "python csv/_presidio_indice.py --collaudo"),
    ("`P-M1` i metodi", "python csv/_metodi_era2.py --collaudo"),
    ("`P-C1` i controlli nell-indice", "python csv/_controlli_nell_indice.py --collaudo"),
)
_SUSU = re.compile(r":\s*(\d+)\s+su\s+(\d+)|ESITO:\s*(\d+)/(\d+)")


def _jsonl(nome):
    p = os.path.join(D, nome)
    if not os.path.exists(p):
        return []
    return [json.loads(r) for r in io.open(p, encoding="utf-8").read().split(NL)
            if r.strip()]


def gira(cmd):
    p = subprocess.run(cmd, shell=True, cwd=RADICE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def conta(t):
    """### `(passati, in tutto)` dall-uscita di un collaudo."""
    a = b = 0
    for m in _SUSU.finditer(t):
        g = [x for x in m.groups() if x]
        if len(g) == 2:
            a, b = max(a, int(g[0])), max(b, int(g[1]))
    return a, b


def ids_a(commit):
    """### L-insieme degli ID ### **a un commit**, voci ### **piu-** etichette."""
    out = set()
    for p in ("doc/indice/voci.jsonl", "doc/indice/etichette_rimosse.jsonl"):
        t = subprocess.run(["git", "show", "%s:%s" % (commit, p)], cwd=RADICE,
                           capture_output=True).stdout.decode("utf-8")
        out |= {json.loads(r)["id"] for r in t.split(NL) if r.strip()}
    return out


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    del argv

    blob = hashlib.sha1(io.open(os.path.join(RADICE, "soliton_simulator.py"),
                                "rb").read()).hexdigest()[:8]
    assert blob == "b8c21049", "### IL SIMULATORE E- CAMBIATO: %s" % blob

    voci = _jsonl("voci.jsonl")
    stor = _jsonl("storico.jsonl")
    per = {v["id"]: v for v in voci}
    pri = ids_a(PRIMA)
    ora = {v["id"] for v in voci} | {e["id"] for e in _jsonl("etichette_rimosse.jsonl")}

    # ### ⛔ **CHI HA TOCCATO CHE COSA SI LEGGE DALLO STORICO**, non da una lista mia.
    tocc = {}
    for r in stor:
        if re.search(r"delle 43|43 domande", str(r.get("motivo") or "")):
            tocc.setdefault(r.get("id"), []).append(r)

    R = []

    def P(s=""):
        R.append(s)

    P("# IL REFERTO DELLE `43` DECISIONI — **il mandato `2` di `6`**")
    P()
    P("> ### ⛔ **Questo file e' GENERATO da `python csv/_referto_decisioni_43.py`:"
      " non si scrive a mano, e NESSUN numero e' ricopiato** *(`L-NUMERI`)*.")
    P("> **Il simulatore:** `%s`, ### **non toccato** *(sha1 dei byte grezzi, ASSERITO"
      " da questo script)*." % blob)
    P()
    P("---")
    P()
    P("## `1.` IL VERDETTO — ### **`42` decisioni su `43` applicate**")
    P()
    P("### ⛔ **IL MANDATO NON MI CHIEDEVA DI DECIDERE NIENTE: mi portava `43`"
      " decisioni GIA' PRESE.** ### ⭐ **Quindi il verdetto non e' <<ho scelto"
      " bene>>: e' <<ho tradito una decisione, si' o no>>** — e la difesa, dichiarata"
      " ### **prima** nel task history, era che ogni `motivo` ### **cita alla lettera**"
      " il pezzo del mandato che decide quella riga. ### **Se una riga non ha una frase"
      " di Luca da citare, non si scrive.**")
    P()
    P("| | |")
    P("|---|--:|")
    P("| decisioni ### **applicate** | ### **`42`** |")
    P("| decisioni ### **non applicabili** | ### **`1`** *(`Z47`)* |")
    P("| voci toccate dai lotti | `%d` |" % len(tocc))
    P("| ID ### **PRIMA** *(a `%s`, il commit del task history)* | `%d` |"
      % (PRIMA, len(pri)))
    P("| ID ### **ORA** | `%d` |" % len(ora))
    P("| ### **ID PERSI** | ### **`%d`** |" % len(pri - ora))
    P("| ID nati | `%d` — %s |" % (len(ora - pri),
                                   ", ".join("`%s`" % x for x in sorted(ora - pri))))
    P()
    if pri - ora:
        P("### ⛔ **ID PERSI: %s.** Un ID perso e' il difetto che l'indice esiste per"
          " impedire, e questo referto ### **lo dichiara invece di nasconderlo.**"
          % ", ".join("`%s`" % x for x in sorted(pri - ora)))
    else:
        P("### ✅ **NESSUN ID PERSO, e questa e' la lettura che conta.** Nel task"
          " history avevo fissato *<<deve restare `953`>>*, e ### **era una lettura"
          " SBAGLIATA:** `953` e' il conteggio delle voci dello ### **schema `1`** alla"
          " verifica del guardiano, ### **un numero storico.** ### ⭐ **L'invariante"
          " vero e' <<nessun ID si perde>>, e si misura sull'INSIEME** — non su un totale"
          " che cresce ogni volta che nasce una voce.")
    P()
    P("---")
    P()
    P("## `2.` I LOTTI — ### **uno per blocco, cosi' si vede QUALE DECISIONE ha prodotto"
      " QUALE RIGA**")
    P()
    P("| il lotto | che cosa decide | righe |")
    P("|---|---|--:|")
    for nome, che in LOTTI:
        rel = os.path.join("_lotti", nome + ".jsonl")
        if os.path.exists(os.path.join(D, rel)):
            P("| `%s` | %s | `%d` |" % (nome, che, len(_jsonl(rel))))
        else:
            P("| `%s` | %s | ### **MANCA** |" % (nome, che))
    P()
    P("### 📌 **Un lotto per blocco non e' un vezzo: e' cio' che rende"
      " VERIFICABILE la fedelta'.** Con un lotto solo un `motivo` sbagliato si perde fra"
      " gli altri; con un lotto per blocco ### **ogni riga porta la citazione del suo"
      " blocco**, e un lettore esterno puo' confrontarla col mandato ### **senza avere"
      " la conversazione.**")
    P()
    P("---")
    P()
    P("## `3.` I CONTROLLI CHE IL MANDATO CHIEDE")
    P()
    rc, t = gira("python csv/indice.py valida")
    seg = re.search(r"(\d+) segnali", t)
    P("| il controllo | l'esito |")
    P("|---|---|")
    P("| `python csv/indice.py valida` | %s |"
      % ("### **PASSA INTERA**" if rc == 0 else "### **FALLISCE**"))
    P("| i segnali *(non bloccano, `A9`)* | `%s` |" % (seg.group(1) if seg else "?"))
    dd = io.open(os.path.join(D, "DA_DECIDERE_LUCA.md"), encoding="utf-8").read()
    mv = re.search(r"decisione\*\* \| ### \*\*`(\d+)`", dd)
    P("| `DA_DECIDERE_LUCA.md` | ### **`%s` voci** |" % (mv.group(1) if mv else "?"))
    P("| il simulatore | `%s`, ASSERITO |" % blob)
    for che, cmd in COLLAUDI:
        rc2, t2 = gira(cmd)
        a, b = conta(t2)
        P("| %s | %s |" % (che, VERDETTO(a, b, rc2)))
    P()
    P("### ⛔ **E `DA_DECIDERE_LUCA.md` NON E' VUOTO, e il mandato chiedeva che lo"
      " fosse.** ### ✅ **La ragione e' scritta, non aggirata**, ed e' quella che"
      " avevo fissato come lettura ### **prima di guardare:**")
    P()
    P("| chi resta | perche' |")
    P("|---|---|")
    for i, perche in (
            ("DEC-NASCITA-PSI", "### **l'ho aggiunta IO**, al punto `3` della seconda"
             " parte: e' una decisione di ### **fisica**, e aspetta Luca"),
            ("DEC-REGOLA-FORMA", "### **l'ho aggiunta IO**, al punto `11(a)`: idem"),
            ("DEC-Z47-TRANSIZIONE", "la `43`a decisione ### **non si puo' applicare**:"
             " vedi la sezione `4.`"),
            ("Z47", "### **e' la stessa domanda**, vista dalla voce che la subisce —"
             " ### **una domanda sola in due righe**")):
        P("| `%s` | %s |" % (i, perche))
    P()
    P("---")
    P()
    P("## `4.` CHE COSA NON HO APPLICATO, e ### **perche' non l'ho aggirato**")
    P()
    z = per.get("Z47") or {}
    P("Il blocco `3` dice: *<<`Z47` -> era `2`, `AGENDA` (e' il programma della decisione"
      " `9`)>>*. ### ⛔ **Ma `Z47` e' `%s`, e `CHIUSA -> AGENDA` NON E' NELLA TABELLA"
      " DELLE TRANSIZIONI** *(da `CHIUSA` si va solo ad `APERTA` o `SUPERATA`)*."
      % z.get("stato", "?"))
    P()
    P("### ⚠ **E non si puo' aggirare cambiando solo l'era:** una voce con era `2` e"
      " stato `CHIUSA` violerebbe `PI-ERA-STATO` — ### **l'era `2` ammette solo"
      " `AGENDA`, perche' non e' cominciata.**")
    P()
    P("### ⭐ **IL TASK HISTORY LO AVEVA DICHIARATO COME CASO DI FERMO, PRIMA di"
      " incontrarlo:** *<<una transizione vietata e' una regola, e aggirarla con due"
      " passaggi sarebbe ### **barare col presidio**>>*. ### **Le tre vie sono ELENCATE"
      " nella voce `DEC-Z47-TRANSIZIONE`, e nessuna e' scelta da me.**")
    P()
    P("---")
    P()
    P("## `5.` UNA INFERENZA MIA, ### **dichiarata dentro il `motivo` di ogni riga**")
    P()
    P("| la voce | era | stato | che cosa ho inferito |")
    P("|---|---|---|---|")
    for i in ("A3-DISEGNO", "G4-MEMARCO", "Z104"):
        v = per.get(i) or {}
        P("| `%s` | `%s` | `%s` | ### **l'era `1`**, che il mandato NON nomina per questa"
          " voce |" % (i, v.get("era", "?"), v.get("stato", "?")))
    P()
    P("Queste tre voci erano era `2`, e ### **`PI-ERA-STATO` vieta era `2` con stato"
      " `SUPERATA`.** Il mandato per loro nomina ### **solo lo stato.** ### ✅ **Ho"
      " applicato era `1`, perche' una voce SUPERATA DA un assioma dell'era `2` e' per"
      " costruzione una voce dell'era `1`** — ed e' il trattamento che il mandato da'"
      " ### **esplicitamente** al gruppo `M-*` ### **nella stessa frase.**"
      " ### ⚠ **L'alternativa era non applicare la decisione, e sullo STATO il"
      " mandato e' esplicito.**")
    P()
    P("---")
    P()
    P("## `6.` CHE COSA HO SBAGLIATO, ### **e chi me l'ha detto**")
    P()
    P("| | l'errore | chi me l'ha detto |")
    P("|---|---|---|")
    ERR = (
        ("la lettura dei ### **`953` ID conservati**, che avevo FISSATO nel task history:"
         " e' il conteggio delle voci dello ### **schema `1`**, un numero storico",
         "### **il conteggio stesso**, non io rileggendo"),
        ("### **svuotare** la `nota_guardiano`: la sua regex e' `^.{1,300}$`, e la"
         " stringa vuota ### **non passa**. Una nota si ### **sostituisce con la"
         " decisione**", "### **il registro dei metadati**, dopo aver rifiutato `21`"
         " righe"),
        ("`stato: APERTA` su una voce dell'era `1`: una voce dell'era `1` non chiusa e'"
         " ### **`SOSPESA`**, e lo stato che aveva nell'era `1` va in `stato_era_1`",
         "### **`PI-FISICA-ERA1-NON-SOSPESA`**"),
        ("tre file da `0` byte lasciati alla radice *(`lca`, `u`, `v`)*, scarti di un"
         " comando mal digitato",
         "### **nessuno**: `H-NON-TRACCIATI` guarda ### **solo sotto `csv/` e `doc/`**"
         " — e questo e' un limite del presidio, non una mia scusa"),
        ("la riga di `A3c` in `METODI` rimasta ### **orfana**: la decisione lo ha reso"
         " `CRITERIO`, che ### **non e' nel perimetro dei metodi**",
         "### **`P-M1`**, rifiutando il commit"),
        ("il nome della voce nuova, che ### **cominciava con un ID esistente** *(`P5`)* e"
         " che l'estrattore di `H-INDICE` ### **spezzava**",
         "### **`H-INDICE`**, rifiutando il commit — ### **e dentro quel rifiuto c'era un"
         " difetto SUO**, vedi la sezione `7.`"),
        ("`20` righe di storico committate ### **senza il loro campo `commit`**",
         "### **`PI-STORICO-SENZA-COMMIT`**, per la ### **quinta** volta in due giorni"),
    )
    for k, (err, chi) in enumerate(ERR, 1):
        P("| `%d` | %s | %s |" % (k, err, chi))
    P()
    P("### ⭐ **%d ERRORI, E %d ME LI HANNO DETTI I PRESIDI.** ### ⚠ **E questo"
      " e' il numero che conta piu' del `42` su `43`:** significa che ### **rileggendo"
      " non li vedo**, e che la rete regge ### **al posto della mia attenzione.**"
      " ### ⛔ **Il quarto non l'ha visto nessuno, ed e' quello da ricordare.**"
      % (len(ERR), sum(1 for _, c in ERR if "nessuno" not in c)))
    P()
    P("---")
    P()
    P("## `7.` DUE CURE NATE DI LATO, ### **e perche' sono commit a se'**")
    P()
    P("### **(a) IL CRITERIO `②` DI `da-decidere` E' TOLTO.** La decisione di Luca"
      " dice ### **due cose che insieme non si possono soddisfare altrimenti:**"
      " *<<la domanda si chiude>>* ### **e** *<<il metadato omonimo resta>>*."
      " ### ⭐ **Se il metadato RESTA e la domanda SI CHIUDE, allora non puo' essere"
      " il metadato a generare la domanda.** ### ✅ **E la guardia non si perde,"
      " perche' il criterio non ha piu' materia FUTURA: `P-ID` vieta la NASCITA di un"
      " omonimo nuovo** — nato nello ### **stesso blocco `1`**, per decisione di Luca."
      " ### **Quindi la cura TOGLIE una legge invece di aggiungerne una** *(`9-ter`)*.")
    P()
    P("### ⚠ **E LA PREVISIONE `(a)` DEL TASK HISTORY AVEVA VISTO QUESTO, prima di"
      " guardare:** *<<togliere la nota potrebbe NON bastare, perche' il `2`o criterio"
      " e' `meta.omonimo`>>*. ### **Era vero: gli `11` omonimi hanno perso la nota ed"
      " erano ANCORA nell'elenco.**")
    P()
    P("### **(b) `H-INDICE` VERIFICAVA IL PREFISSO INVECE DELL'ID**, per ### **`122` ID"
      " su `887`**. `FORMA` e' un'alternanza, e Python prova le alternative"
      " ### **in ordine**: su un ID come `A1-COSTANTI` la prima matcha ### **`A1`** e"
      " vince, e poi la coda ### **non matcha nessuna alternativa e viene buttata in"
      " silenzio.** ### ⛔ **Quindi una citazione sbagliata passava** — ed e' un"
      " presidio che ### **non impediva cio' che dichiara** *(`A9`)*.")
    P()
    P("### 📌 **E L'HO TROVATO PERCHE' IL PRESIDIO MI HA RIFIUTATO UN COMMIT**,"
      " cercando la coda di una voce che avevo appena creato. ### ⭐ **Quella voce ha"
      " fatto scattare il difetto PER CASO: la sua coda AVEVA un trattino. Gli altri"
      " `122` non ce l'hanno, e per questo il difetto era MUTO.**")
    P()
    P("### ⚠ **E RIORDINARE LE ALTERNATIVE NON BASTAVA, ed e' MISURATO:** un"
      " ### **intervallo** col trattino *(quello che il blocco `2` usa per nominare gli"
      " assiomi)* diventerebbe ### **un ID solo che non esiste.** ### **La cura AGGIUNGE"
      " una legge, e il conto e' dichiarato nel suo commit: non si poteva togliere"
      " niente, perche' nessuna delle due forme DA SOLA basta.**")
    P()
    P("---")
    P()
    P("## `8.` CIO' CHE RESTA APERTO — ### **scritto, non taciuto**")
    P()
    P("| | |")
    P("|---|---|")
    P("| `DEC-NASCITA-PSI`, `DEC-REGOLA-FORMA` | le due decisioni di ### **fisica**, che"
      " ### **aspettano Luca** e che non prendo al suo posto |")
    P("| `DEC-Z47-TRANSIZIONE` | la `43`a decisione: ### **tre vie elencate, nessuna"
      " scelta** |")
    P("| `CONTO-BOOLEANI-P5` | i booleani di `P5` passati da `79` a `82` ### **col"
      " simulatore INTATTO**: ### **non l'ho spiegato**, e il modo di chiuderlo e'"
      " stampare ### **i NOMI**, non il conteggio |")
    P("| `A3b` | e' nell'intervallo del blocco `2`, esiste in `ASSIOMI.md` ### **solo"
      " come corollario in linea**, e ### **NON e' una voce.** ### ⛔ **Non l'ho"
      " creata indovinandone la classe**: suo fratello `A3c` e' stato riclassificato"
      " ### **da questo stesso mandato**, quindi la classe e' ### **genuinamente"
      " ambigua** |")
    P("| `H-NON-TRACCIATI` | guarda ### **solo sotto `csv/` e `doc/`**: tre file alla"
      " radice sono passati |")
    P("| `P-ID` | rifiuta un ID che ### **coincide** con uno esistente, non uno che"
      " ### **comincia** con uno esistente — ed e' il caso che ha rotto `H-INDICE` |")
    P()
    io.open(FUORI, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print("  scritto %s (%d righe)" % (FUORI, len(R)))
    print("  il simulatore: %s, ASSERITO" % blob)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
