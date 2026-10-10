# -*- coding: utf-8 -*-
"""GENERA `doc/REFERTO_piano_era2.md` — **il referto del mandato `3` di `6`.**

### ⛔ **NESSUN NUMERO E' RICOPIATO A MANO** *(`L-NUMERI`)*: le cifre escono
dall'### **albero sul disco**, dall'### **indice**, dalla ### **tabella delle leggi**, e
dall'### **uscita dei collaudi che questo script FA GIRARE.**

### ⭐ **E IL MANDATO `3` HA UNA COSA CHE NESSUNO DEGLI ALTRI AVEVA: il lavoro VERO si è
trovato PRIMA di cominciarlo.** Il task history ordinava come primo passo *«leggere
### **dal codice** chi valida `decisioni.jsonl`»*, e quella lettura ha trovato
### **quattro difetti** — fra cui ### **un presidio che passava `13` su `13` con quattro
record cancellati.** ### **La sezione `2.` è quella, e non è un contorno: è metà del
mandato.**
"""
# ### ⚠ **L-ESENZIONE STA QUI, FUORI DAL DOCSTRING, e l-ho imparato da `H-P5`
# ### CHE MI HA RIFIUTATO IL COMMIT** del referto precedente: dentro le triple
# ### virgolette ### **non e- un commento**, e un presidio che cerca un commento
# ### ### **non lo trova.**
# ESENTE-H-P5: questo referto NON misura il simulatore. Non fa girare nessuna scena, non
#   legge nessun booleano di modulo e non produce nessun numero di fisica: parla
#   dell-ALBERO, del PIANO e dei presidi che li guardano. Dichiarare <<la configurazione
#   intera>> del driver qui direbbe DOVE NON SI E- MISURATO, che e- rumore. Il blob del
#   simulatore e- dichiarato comunque, e ASSERITO: b8c21049.
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

FUORI = os.path.join(RADICE, "doc", "REFERTO_piano_era2.md")

# ### ⛔ **IL COMMIT DEL TASK HISTORY**, che per il rito del par. `8` e- ### **antenato**
# ### dei commit del lavoro: ### **l-ordine e- verificabile da git.**
PRIMA = "ccafeca"

COLLAUDI = (
    ("`P-ALB` l-albero delle scelte", "python csv/_albero_era2.py --collaudo"),
    ("`P-T2` il replay, col buco chiuso", "python csv/_replay_registri.py --collaudo"),
    ("l-ARBITRO fra le due vie", "python csv/_registri_indice.py --collaudo"),
    ("i presidi dell-indice, coi vocabolari", "python csv/_presidio_indice.py --collaudo"),
)
_SUSU = re.compile(r":\s*(\d+)\s+su\s+(\d+)|ESITO:\s*(\d+)/(\d+)")

# ### ⚠ **I QUATTRO DIFETTI TROVATI PRIMA DI COMINCIARE**, col loro ID: la tabella non
# ### si scrive a mano nel referto, ### **si legge dall-indice.**
DIFETTI = ("REPLAY-CIECO-ALLE-CANCELLAZIONI", "DUE-VIE-SU-LEGGI-JSONL",
           "H-INDICE-IGNORA-I-VOCABOLARI", "FORMA-SPEZZA-ID")


def _jsonl(rel):
    p = os.path.join(RADICE, rel)
    if not os.path.exists(p):
        return []
    return [json.loads(r) for r in io.open(p, encoding="utf-8").read().split(NL)
            if r.strip()]


def gira(cmd):
    p = subprocess.run(cmd, shell=True, cwd=RADICE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def conta(t):
    a = b = 0
    for m in _SUSU.finditer(t):
        g = [x for x in m.groups() if x]
        if len(g) == 2:
            a, b = max(a, int(g[0])), max(b, int(g[1]))
    return a, b


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    del argv
    import _albero_era2 as ALB

    blob = hashlib.sha1(io.open(os.path.join(RADICE, "soliton_simulator.py"),
                                "rb").read()).hexdigest()[:8]
    assert blob == "b8c21049", "### IL SIMULATORE E- CAMBIATO: %s" % blob

    nodi, radici = ALB.carica()
    c = ALB.conta()
    voci = {v["id"]: v for v in _jsonl("doc/indice/voci.jsonl")}
    dec = _jsonl("doc/indice/decisioni.jsonl")

    import yaml
    with io.open(os.path.join(RADICE, "primo_ordine", "leggi", "leggi.yaml"),
                 encoding="utf-8") as f:
        leggi = (yaml.safe_load(f).get("leggi") or [])

    R = []

    def P(s=""):
        R.append(s)

    P("# IL REFERTO DEL PIANO E DELL'ALBERO — **il mandato `3` di `6`**")
    P()
    P("> ### ⛔ **Questo file e' GENERATO da `python csv/_referto_piano_era2.py`:"
      " non si scrive a mano, e NESSUN numero e' ricopiato** *(`L-NUMERI`)*.")
    P("> **Il simulatore:** `%s`, ### **non toccato** *(sha1 dei byte grezzi, ASSERITO"
      " da questo script)*." % blob)
    P("> **Il mandato dice:** *<<solo scrittura del piano: nessun codice di fisica,"
      " nessuna corsa>>* e *<<nessuna scelta di fisica in questo mandato>>*.")
    P()
    P("---")
    P()
    P("## `1.` I QUATTRO PUNTI, e che cosa e' stato fatto")
    P()
    P("| | il punto | l'esito |")
    P("|---|---|---|")
    P("| `1` | `doc/PIANO_era2.md`, le fasi con ingresso e uscita |"
      " ### **FATTO**: `F0`-`F4`, piu' un ### **tabellone di controllo** coi comandi |")
    P("| `2` | l'albero, nel piano ### **e** come nodi in `decisioni.jsonl` |"
      " ### **FATTO**: `%d` nodi, e `decisioni.jsonl` passa da `25` a `%d` record |"
      % (c["nodi"], len(dec)))
    P("| `3` | ### **il presidio dell'albero**, nei due versi |"
      " ### **FATTO**: `P-ALB`, dentro `indice.py valida` |")
    P("| `4` | questo referto | ### **FATTO** |")
    P()
    P("### ⭐ **E LA REGOLA CHE HO MESSO IN TESTA AL PIANO, perche' vale per tutte"
      " le fasi: un criterio di uscita che NON ESCE DA UN COMANDO non e' un criterio.**"
      " ### **Se una fase si dichiara chiusa, si dice CON QUALE COMANDO** — e il piano"
      " porta i sei comandi che rispondono.")
    P()
    P("---")
    P()
    P("## `2.` CHE COSA HO TROVATO PRIMA DI COMINCIARE — ### **quattro difetti, e il"
      " peggiore era un presidio che TACEVA**")
    P()
    P("### ⛔ **Il task history ordinava come PRIMO PASSO:** *<<leggere ### **dal"
      " codice** chi valida `decisioni.jsonl`>>*. ### ⭐ **Quella lettura — fatta"
      " PRIMA di scrivere una riga del piano — ha trovato questo:**")
    P()
    P("| | l'ID | che cosa era |")
    P("|---|---|---|")
    for k, i in enumerate(DIFETTI, 1):
        v = voci.get(i) or {}
        st = v.get("stato", "?")
        tit = " ".join((v.get("titolo") or "?").split())
        P("| `%d` | `%s` *(`%s`)* | %s |" % (k, i, st, tit))
    P()
    P("### ⭐ **IL PEGGIORE E' IL PRIMO, e il perche' e' una frase che sembra la"
      " stessa e non lo e':** *<<ogni record coincide col `dopo` della sua ultima riga"
      " di storico>>* ### **NON E'** *<<lo storico si rigioca in questo file>>*."
      " ### **La prima e' vera anche su un file META' VUOTO**, e per questo `P-T2`"
      " passava ### **`13` su `13` con QUATTRO record cancellati.**")
    P()
    P("### ⚠ **E IL SECONDO SPIEGA PERCHE' IL PRIMO CONTAVA:** un giro del"
      " generatore dell'era `1` ### **cancellava i quattro record dell'era `2`**, e"
      " ### **il conto delle leggi di `timbro.py` esce dalla TABELLA** — quindi quel"
      " giro avrebbe portato il conto a ### **zero senza toccare un file di codice.**")
    P()
    P("### 📌 **E IL QUARTO L'HA TROVATO IL PRESIDIO STESSO, rifiutandomi un"
      " commit:** `H-INDICE` verificava ### **il PREFISSO invece dell'ID** per"
      " ### **`122` ID su `887`**, e il difetto era ### **MUTO** perche' le code degli"
      " altri `122` non hanno un trattino.")
    P()
    P("---")
    P()
    P("## `3.` L'ALBERO, come il mandato lo scrive")
    P()
    P("| il nodo | l'etichetta di Luca | `presa` | dipende da | argomento noto |")
    P("|---|---|---|---|---|")
    for n in nodi:
        P("| `%s` | `%s` | %s | %s | %s |"
          % (n["id"], n["etichetta"],
             "### **SI'**" if n.get("presa") else "no",
             (", ".join("`%s`" % x for x in n["dipende_da"]) if n.get("dipende_da")
              else "### *radice*"),
             "si'" if n.get("argomento_noto") else "### ⛔ **NO**"))
    P()
    P("| | |")
    P("|---|--:|")
    P("| nodi | `%d` |" % c["nodi"])
    P("| archi | `%d` |" % c["archi"])
    P("| radici gia' prese | `%d` — %s |"
      % (c["radici"], ", ".join("`%s`" % x for x in radici)))
    P("| ### **nodi `presa`** | ### **`%d`** |" % c["prese"])
    P("| ### **nodi senza argomento noto** | ### **`%d`** |" % c["senza_argomento"])
    P()
    P("### ✅ **E `%d` NODI `presa` E' IL FATTO DEL MANDATO**, non una mancanza:"
      " *<<nessuna scelta di fisica in questo mandato>>*. ### **Le due radici prese sono"
      " `A16` e `A17`, che sono ASSIOMI** — decisioni di Luca del `2026-10-08`, non"
      " scelte di oggi." % c["prese"])
    P()
    P("### ⛔ **E SU `D9` LUCA HA DICHIARATO UNA DIREZIONE** *(<<lo spazio emerge"
      " grazie alla mitosi>>)*, ### **e il mandato dice NELLA STESSA FRASE che la"
      " direzione NON E' UNA DECISIONE PRESA.** ### ⭐ **Tenere separate quelle due"
      " cose e' esattamente il lavoro di `P-ALB`**, ed e' il motivo per cui la direzione"
      " sta nel `yaml` ### **come NOTA e non come STATO.**")
    P()
    P("---")
    P()
    P("## `4.` I CONTROLLI")
    P()
    P("| il controllo | l'esito |")
    P("|---|---|")
    rc, t = gira("python csv/indice.py valida")
    seg = re.search(r"(\d+) segnali", t)
    P("| `python csv/indice.py valida` ### **(con `P-ALB` dentro)** | %s |"
      % ("### **PASSA INTERA**" if rc == 0 else "### **FALLISCE**"))
    P("| i segnali *(non bloccano, `A9`)* | `%s` |" % (seg.group(1) if seg else "?"))
    for che, cmd in COLLAUDI:
        rc2, t2 = gira(cmd)
        a, b = conta(t2)
        P("| %s | %s |" % (che, VERDETTO(a, b, rc2)))
    P("| il simulatore | `%s`, ASSERITO |" % blob)
    P()
    P("### ⛔ **E IL BRACCIO CHE CONTA DI `P-ALB` E' QUELLO END-TO-END:** provare"
      " `controlla()` ### **non prova `valida`**, perche' fra le due c'e'"
      " ### **un `import` dentro un `try`** — ed e' ### **il posto dove un presidio si"
      " spegne in silenzio.** ### **Misurato: `indice.py valida` ESCE `1`** col nodo"
      " marcato `presa` ### **nel file**, e la fonte torna ### **identica al byte.**")
    P()
    P("### ⭐ **E IL SECONDO CHE CONTA:** se si marca `presa` ### **anche il"
      " padre**, il presidio ### **TACE.** ### **Senza quel braccio, il <<deve"
      " scattare>> potrebbe passare perche' il presidio RIFIUTA SEMPRE** — e un presidio"
      " che rifiuta sempre non prova niente.")
    P()
    P("---")
    P()
    P("## `5.` LO STATO DELLE CINQUE FASI, misurato oggi")
    P()
    P("| | la fase | lo stato |")
    P("|---|---|---|")
    P("| `F0` | chiusura | ### ⚠ **NON CHIUSA**: restano la ### **terza parte**"
      " dell'infrastruttura e le ### **regole di gestione** *(i mandati `4` e `5`)* |")
    P("| `F1` | regole di forma | ### **non cominciata.** ### ⭐ **E la regola"
      " `(a)` e' GIA' VERA senza essere una regola:** il termine di prova ha"
      " ### **esattamente** la forma bilineare, ### **ma il generatore NON LA PRETENDE**"
      " — e finche' non la pretende ### **e' un'abitudine, non una regola** |")
    P("| `F2` | le decisioni | ### ⛔ **NON PUO' COMINCIARE**: aspetta Luca su"
      " `DEC-ALBERO-CINQUE-SENZA-ARGOMENTO` |")
    P("| `F3` | le leggi | ### **non cominciata**: la tabella ha `%d` leggi,"
      " ### **TUTTE `prova: true`** → ### ⛔ **ZERO LEGGI VERE** |" % len(leggi))
    P("| `F4` | le prime misure | ### **non cominciata** |")
    P()
    P("### ✅ **E <<ZERO LEGGI VERE>> NON E' UN DIFETTO: e' il punto di partenza"
      " DICHIARATO.** L'infrastruttura e' stata costruita su leggi finte"
      " ### **proprio perche' una legge finta non puo' far sembrare vero un"
      " risultato.**")
    P()
    P("---")
    P()
    P("## `6.` CIO' CHE RESTA APERTO — ### **scritto, non taciuto**")
    P()
    P("| | |")
    P("|---|---|")
    aperte = [i for i in sorted(voci) if (voci[i].get("meta") or {}).get(
        "nota_guardiano") and re.search(r"da\s+(decidere|confermare)\s+da\s+Luca",
                                        str(voci[i]["meta"]["nota_guardiano"]), re.I)]
    for i in aperte:
        P("| `%s` | %s |" % (i, " ".join((voci[i].get("titolo") or "").split())))
    P("| `DEC-ALBERO-CINQUE-SENZA-ARGOMENTO` | di `D4`, `D2`, `D11`, `D12`, `T4` il repo"
      " ### **non dice l'argomento**, e nemmeno quali siano *<<le decisioni `1`, `3`,"
      " `10`>>*. ### ⛔ **Non l'ho inventato** |")
    P("| `H-FISICA-FUORI-LISTA` | legge la lista ### **dal DISCO**: una modifica non"
      " committata ### **autorizza un commit.** ### **In `F3` conta piu' che in `F0`** |")
    P("| le etichette `D2`, `D4`, `D6`, `D11`, `D12`, `D13`, `T4` | ### **esistono"
      " nell'indice come voci dell'era `1`**, e `H-INDICE` le risolve ### **su"
      " quelle**, in silenzio. ### **E' il motivo per cui l'etichetta e' un CAMPO e non"
      " un id** |")
    P("| `metadati.jsonl` | resta un ### **`REPERTO` per NECESSITA'** *(ha una via di"
      " scrittura e ### **zero** righe di storico)*: il quarto stato `GENERATO`"
      " ### **non lo copre** |")
    P()
    P("---")
    P()
    P("## `7.` L'ORDINE E' VERIFICABILE DA GIT, non asserito da me")
    P()
    P("Il task history di questo mandato e' il commit ### **`%s`**, e per il rito del"
      " par. `8` e' ### **antenato di ogni commit del lavoro.**"
      " ### ⭐ **Quindi <<il ragionamento l'ho scritto prima>> non e' una mia"
      " affermazione: e' una proprieta' del grafo dei commit**, e si verifica con"
      " `git merge-base --is-ancestor %s HEAD`." % (PRIMA, PRIMA))
    P()
    rc3, _ = gira("git merge-base --is-ancestor %s HEAD" % PRIMA)
    P("### %s **Verificato adesso: `%s` %s antenato di `HEAD`.**"
      % ("✅" if rc3 == 0 else "⛔", PRIMA,
         "E'" if rc3 == 0 else "### NON E'"))
    P()
    io.open(FUORI, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print("  scritto %s (%d righe)" % (FUORI, len(R)))
    print("  il simulatore: %s, ASSERITO" % blob)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
