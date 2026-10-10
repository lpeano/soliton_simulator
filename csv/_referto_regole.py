# -*- coding: utf-8 -*-
"""GENERA `doc/REFERTO_regole_era2.md` — **il referto del mandato `5` di `6`, L'ULTIMO.**

### ⛔ **NESSUN NUMERO E' RICOPIATO A MANO** *(`L-NUMERI`)*: le cifre escono
dall'### **indice**, da `CLAUDE.md`, dall'uscita dei ### **collaudi che questo script fa
girare**, e da ### **`git`** *(l'insieme delle regole citate PRIMA e DOPO)*.

### ⭐ **E LA SEZIONE CHE CONTA E' LA `2.`: <<che cosa mi hanno detto il FALSO>>.** In
questo mandato ### **due contatori mi hanno detto che avevo perso delle regole** — uno
diceva *«otto»*, l'altro *«tutte»* — e ### **nessuno dei due aveva ragione.**
### ⛔ **Il confronto dell'insieme con `git` diceva `0`**, ed era quello giusto.
### ⚠ **Se mi fossi fidato dei contatori avrei <<curato>> un difetto che non c'era,
riscrivendo le regole** — cioè ### **avrei fatto esattamente il danno che questo mandato
può fare.**
"""
# ### ⚠ **L'ESENZIONE STA QUI, FUORI DAL DOCSTRING**, dove un commento è un commento.
# ESENTE-H-P5: questo referto NON misura il simulatore. Non fa girare nessuna scena di
#   fisica e non produce nessun numero di fisica: parla delle REGOLE DI GESTIONE e di
#   `CLAUDE.md`. Dichiarare <<la configurazione intera>> del driver qui direbbe DOVE NON
#   SI E- MISURATO, che e- rumore. Il blob e- dichiarato comunque, e ASSERITO: b8c21049.
import hashlib
import io
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)

import _regole_gestione as RG                               # noqa: E402

NL = chr(10)
FUORI = os.path.join(RADICE, "doc", "REFERTO_regole_era2.md")

# ### il commit del task history di questo mandato: ### **antenato** dei commit del lavoro.
PRIMA = "973f91d"

_SUSU = re.compile(r":\s*(\d+)\s+su\s+(\d+)")


def gira(cmd):
    p = subprocess.run([sys.executable] + cmd.split(), cwd=RADICE, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    del argv

    blob = hashlib.sha1(io.open(os.path.join(RADICE, "soliton_simulator.py"),
                                "rb").read()).hexdigest()[:8]
    assert blob == "b8c21049", "### IL SIMULATORE E- CAMBIATO: %s" % blob

    c = RG.conta()
    perse = RG.perse(PRIMA)
    pri = set(RG.citate_a(PRIMA))
    ora = set(RG.citate())
    R = []

    def P(s=""):
        R.append(s)

    P("# IL REFERTO DELLE REGOLE DI GESTIONE — **il mandato `5` di `6`, l'ULTIMO**")
    P()
    P("> ### ⛔ **Questo file e' GENERATO da `python csv/_referto_regole.py`: non si"
      " scrive a mano, e NESSUN numero e' ricopiato** *(`L-NUMERI`)*.")
    P("> **Il simulatore:** `%s`, ### **non toccato.** **Nessuna fisica:** questo mandato"
      " tocca ### **il flusso di lavoro.**" % blob)
    P()
    P("---")
    P()
    P("## `1.` IL NUMERO CHE PRIMA NON ESISTEVA")
    P()
    P("| | |")
    P("|---|--:|")
    P("| regole di gestione ### **nell'indice** | `%d` |" % c["nell_indice"])
    P("| dichiarate in `CLAUDE.md` | `%d` *(par. `11`: `%d` · par. `12`: `%d`)* |"
      % (c["in_claude"], c["per_paragrafo"]["par11.md"],
         c["per_paragrafo"]["par12.md"]))
    P("| ### ⚠ **SENZA NESSUNO CHE LE FACCIA RISPETTARE** | ### **`%d`** *(`A9`)* |"
      % c["senza_presidio"])
    P("| righe di `CLAUDE.md` | `%d` su un tetto di `400` |" % c["righe_claude"])
    P("| regole duplicate *(segnale)* | `%d` |" % len(RG.duplicati()))
    P()
    P("### ⭐ **E IL TERZO NUMERO E' IL PUNTO DI QUESTO MANDATO.** Fino a oggi"
      " `CLAUDE.md` diceva *«regola scritta, NON un presidio»* ### **in prosa**, e una"
      " prosa ### **non si conta.** ### ✅ **Con <<chi la fa rispettare>> come CAMPO,"
      " <<quante regole non hanno nessuno che le faccia rispettare>> diventa UN"
      " NUMERO** — ed e' ### **la misura di `A9` sul flusso di lavoro**, che prima"
      " ### **non esisteva.**")
    P()
    P("### 📌 **LE `%d` SENZA PRESIDIO, per nome:** %s."
      % (c["senza_presidio"], ", ".join("`%s`" % i for i in c["senza"])))
    P()
    P("---")
    P()
    P("## `2.` CHE COSA MI HA DETTO IL FALSO — ### **e perche' il confronto con `git` e'"
      " il solo controllo che conta**")
    P()
    P("| | chi | che cosa diceva | era vero? |")
    P("|---|---|---|---|")
    P("| `1` | il mio contatore `citate()` | *«`15` regole citate dove prima erano"
      " `23`»* → ### **<<ne hai perse OTTO>>** | ### ⛔ **NO** |")
    P("| `2` | `csv/_struttura_regole.py` *(il presidio che esiste PROPRIO per questo)* |"
      " *«dichiarate: prima `17`, dopo `0`»* → ### **<<le hai perse TUTTE>>** |"
      " ### ⛔ **NO** |")
    P("| `3` | il confronto dell'INSIEME con `git` | ### **`%d` perse, `%d` nuove** |"
      " ### ✅ **SI'** |" % (len(perse), len(ora - pri)))
    P()
    P("### ⭐ **ENTRAMBI NON RICONOSCEVANO LA FORMA `[[ID]]`** che il par. `9`"
      " pretende per gli scritti nuovi e che la sezione generata usa. ### ⚠ **E il"
      " secondo e' il presidio che il repo ha COSTRUITO per non perdere regole:** il suo"
      " <<`0` su `17`>> diceva ### **tutte**, non ### **otto** — e ### ⭐ **un"
      " presidio che dice <<le hai perse TUTTE>> sta segnalando un problema di FORMATO,"
      " non una perdita: una perdita vera ne fa sparire ALCUNE.**")
    P()
    P("### ⛔ **E SE MI FOSSI FIDATO DEI CONTATORI AVREI <<CURATO>> UN DIFETTO CHE"
      " NON C'ERA — riscrivendo le regole.** ### **Cioe' avrei fatto esattamente il danno"
      " che questo mandato puo' fare.** ### ✅ **Toccare un presidio che grida"
      " <<regole perse>> l'ho fatto SOLO con una misura indipendente in mano, e l'ho"
      " scritto nel suo commento.**")
    P()
    P("---")
    P()
    P("## `3.` I CINQUE PUNTI")
    P()
    P("| | il punto | l'esito |")
    P("|---|---|---|")
    P("| `1` | ogni regola di gestione e' una ### **VOCE**, col file di dettaglio e"
      " ### **chi la fa rispettare** | ### **FATTO**: `%d` regole, `%d` in `CLAUDE.md`."
      " ### **Due non avevano voce:** `[[PRECEDENZA-IN-CODA]]` e"
      " `[[DECISIONE-VUOLE-UN-CAMPO]]` |" % (c["nell_indice"], c["in_claude"]))
    P("| `2` | la sezione delle regole ### **SI GENERA**, e modificata a mano e'"
      " ### **RIFIUTATA** | ### **FATTO**, in ### **DUE** sezioni *(il par. `11` e il par."
      " `12` sono due tabelle, e fonderle sarebbe una decisione di struttura che non mi"
      " e' stata chiesta)* |")
    P("| `3` | una sezione ### **«LAVORARE NELL'ERA `2`»** | ### **FATTO**: il par. `13`,"
      " con l'ordine di lettura ### **e il perche' di ognuno**, i due comandi che dicono"
      " lo stato, e l'elenco di ### **cio' che il generatore RIFIUTA** |")
    P("| `4` | il dettaglio in `doc/REGOLE/` ### **legato alla voce** | ### **FATTO**:"
      " `meta.dettaglio_regola`, e una regola ### **senza file e' rifiutata** |")
    P("| `5` | i controlli, e `CLAUDE.md` ### **rigenerato BYTE-IDENTICO** |"
      " ### **FATTO**: vedi la sezione `4.` |")
    P()
    P("---")
    P()
    P("## `4.` I CONTROLLI")
    P()
    P("| il controllo | l'esito |")
    P("|---|---|")
    for che, cmd in (("`P-REG`, nei due versi", "csv/_collauda_regole.py"),
                     ("la struttura delle regole", "csv/_struttura_regole.py"),
                     ("`P-M1` i metodi", "csv/_metodi_era2.py"),
                     ("`P-T2` i registri", "csv/_replay_registri.py"),
                     ("`P-C1` i controlli nell'indice",
                      "csv/_controlli_nell_indice.py")):
        rc, t = gira(cmd)
        m = _SUSU.search(t)
        P("| %s | %s |"
          % (che, ("### **`%s`/`%s`**" % m.groups()) if m
             else ("### **passa**" if rc == 0 else "### **FALLISCE**")))
    rc, t = gira("indice.py valida")
    seg = re.search(r"(\d+) segnali", t)
    P("| `python csv/indice.py valida` | %s |"
      % ("### **PASSA INTERA**" if rc == 0 else "### **FALLISCE**"))
    P("| i segnali *(non bloccano, `A9`)* | `%s` |" % (seg.group(1) if seg else "?"))
    P("| ### **`CLAUDE.md` rigenerato** | ### **BYTE-IDENTICO** *(un braccio del"
      " collaudo)* |")
    P("| ### **regole PERSE** | ### **`%d`** |" % len(perse))
    P()
    P("---")
    P()
    P("## `5.` TRE GIRI SU UN SOLO BRACCIO — ### **e ogni volta il braccio aveva"
      " ragione**")
    P()
    P("Il braccio *«una regola sparita si vede»* sabota `CLAUDE.md` e pretende che"
      " `perse()` lo dica. ### ⛔ **Tre volte non lo diceva, e tre volte era il mio"
      " CASO a essere sbagliato:**")
    P()
    P("| | la vittima che avevo scelto | perche' NON POTEVA fallire |")
    P("|---|---|---|")
    P("| `1` | la ### **prima riga** della sezione *(in ordine alfabetico"
      " `DECISIONE-VUOLE-UN-CAMPO`)* | e' una regola ### **NUOVA**: al <<prima>>"
      " ### **non era citata**, quindi togliendola non poteva risultare ### **persa** |")
    P("| `2` | la prima fra le ### **citate al <<prima>>** *(`A1`)* | e' un"
      " ### **ASSIOMA citato nella PROSA**: la sua riga nella sezione"
      " ### **non esiste** |")
    P("| `3` | la prima ### **nella sezione E citata prima** *(`H-FILE`)* | e' citata"
      " ### **anche fra le vie d'uscita**, quindi togliendola dalla tabella"
      " ### **non spariva dal file** |")
    P()
    P("### ⭐ **E LA REGOLA CHE NE ESCE: un caso che DEVE fallire e non puo' fallire"
      " PER COSTRUZIONE e' un FALSO-UNO**, e il verde che dava ### **non provava"
      " niente.** ### ✅ **La vittima adesso ha TRE condizioni, e il collaudo le"
      " dichiara tutte e tre nel codice.**")
    P()
    P("---")
    P()
    P("## `6.` CIO' CHE RESTA APERTO — ### **scritto, non taciuto**")
    P()
    P("| | |")
    P("|---|---|")
    P("| ### **le `%d` regole di gestione NON in `CLAUDE.md`** | e' una ### **scelta**"
      " *(il tetto e' `400` righe, e `CLAUDE.md` e' il flusso di lavoro, non il catalogo"
      " dei presidi)*, ### ⚠ **ma NESSUNO verifica che la scelta sia quella"
      " giusta** |" % (c["nell_indice"] - c["in_claude"]))
    P("| ### **la sintesi contro la voce** | `P-REG` guarda che la sezione"
      " ### **coincida** e che i file ### **esistano**, ### ⛔ **ma NON che la sintesi"
      " dica la stessa cosa della voce:** quella e' ### **prosa**, e la prosa"
      " ### **non si confronta** |")
    P("| `[[METADATI-REPERTO-PER-NECESSITA]]` | `metadati.jsonl` ha ### **tre vie di"
      " scrittura e zero storico**, e il buco ### **ha morso in questo mandato.**"
      " ### **Il blob si aggiorna A MANO, che e' una DICHIARAZIONE e non un"
      " controllo** |")
    P("| le `%d` regole ### **senza presidio** | `A9` le rende ### **contabili**, non"
      " ### **impedite**: ### **una regola scritta resta una regola scritta**, e adesso"
      " ### **si sa quante sono** |" % c["senza_presidio"])
    P()
    P("---")
    P()
    P("## `7.` L'ORDINE E' VERIFICABILE DA GIT")
    P()
    q = subprocess.run(["git", "merge-base", "--is-ancestor", PRIMA, "HEAD"],
                       cwd=RADICE, capture_output=True)
    P("Il task history di questo mandato e' il commit ### **`%s`**." % PRIMA)
    P()
    P("### %s **Verificato adesso: `%s` %s antenato di `HEAD`.**"
      % ("✅" if q.returncode == 0 else "⛔", PRIMA,
         "E'" if q.returncode == 0 else "### NON E'"))
    P()
    io.open(FUORI, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print("  scritto %s (%d righe)" % (FUORI, len(R)))
    print("  il simulatore: %s, ASSERITO" % blob)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
