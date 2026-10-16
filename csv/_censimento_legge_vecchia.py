# -*- coding: utf-8 -*-
"""Il CENSIMENTO classificato: ogni coppia file/simbolo, col suo verdetto.

Il documento SI GENERA: i conteggi escono dai file, i verdetti stanno qui, e una
coppia SENZA verdetto FA ALZARE -- cosi' un uso nuovo non entra in silenzio.
"""
import glob
import io
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
os.chdir(os.path.dirname(_QUI))
import _presidio                                              # noqa: E402

_presidio.avvia(__file__)
NL = chr(10)
# ### ⚠ **E QUESTO FILE ESCE DAL PERIMETRO**, dichiarato qui: i ### **verdetti**
# ### nominano i simboli cercati, quindi il generatore ### **troverebbe se stesso** e
# ### chiederebbe un verdetto sul proprio elenco di verdetti.
FUORI = ("_archivio", "_seal_", "_test_fork", "_censimento_legge_vecchia")
CHIAVI = (("elicita", re.compile(r"\belicita\b")),
          ("CAMM-SATURAZIONE", re.compile(r"CAMM-SATURAZIONE")),
          ("SAT.", re.compile(r"\bSAT\.")),
          ("x^3/3", re.compile(r"x\^3/3|x\*\*3\s*/\s*3")),
          ("import saturazione", re.compile(r"import saturazione")))

L, S = "LEGITTIMO", "SCADUTO"
# ### il verdetto, e il MOTIVO: `L` vuol dire *parla della saturazione perche' E' della
# ### saturazione, o e' un confronto storico DICHIARATO*; `S` vuol dire *nel perimetro
# ### attivo, oggi, misurerebbe o salterebbe o sostituirebbe LA LEGGE SBAGLIATA*.
V = {
 ("primo_ordine/saturazione.py", "x^3/3"): (L, "e- la legge stessa: `G(x) = x - arctan x`"),
 ("primo_ordine/termini/camm_saturazione.py", "CAMM-SATURAZIONE"):
    (L, "e- il legame GENERATO della legge: si rigenera dalla tabella"),
 ("primo_ordine/termini/camm_materia_vuoto.py", "CAMM-SATURAZIONE"):
    (L, "il testo GENERATO dice che SOSTITUISCE la saturazione"),
 ("primo_ordine/_collauda_saturazione.py", "elicita"):
    (L, "il collaudo DELLA saturazione: la sua variabile e- `|h|/Lambda`"),
 ("primo_ordine/_collauda_saturazione.py", "CAMM-SATURAZIONE"):
    (L, "il collaudo DELLA saturazione"),
 ("primo_ordine/_collauda_saturazione.py", "SAT."):
    (L, "il collaudo DELLA saturazione"),
 ("primo_ordine/_collauda_saturazione.py", "import saturazione"):
    (L, "il collaudo DELLA saturazione"),
 ("primo_ordine/_collauda_materia_vuoto.py", "CAMM-SATURAZIONE"):
    (L, "dichiara nel titolo CHE COSA sostituisce"),
 ("primo_ordine/materia_vuoto.py", "CAMM-SATURAZIONE"):
    (L, "dichiara nel titolo CHE COSA sostituisce"),
 ("primo_ordine/materia_vuoto.py", "elicita"):
    (L, "il motivo PER CUI la sorgente e- `rho` e NON l-elicita-"),
 ("primo_ordine/motore.py", "CAMM-SATURAZIONE"):
    (L, "il motore REGISTRA entrambi gli operatori: la legge resta in tabella"),
 ("primo_ordine/motore.py", "elicita"): (L, "il metodo `elicita`, e l-operatore della saturazione"),
 ("primo_ordine/motore.py", "SAT."): (L, "l-operatore della saturazione, che resta"),
 ("primo_ordine/motore.py", "import saturazione"): (L, "serve all-operatore della saturazione"),
 ("primo_ordine/deriva_variabile.py", "elicita"):
    (L, "`satura_elicita`: la variabile VECCHIA, tenuta SOLO per il caso che DEVE fallire"),
 ("primo_ordine/statica_protocollo.py", "CAMM-SATURAZIONE"):
    (L, "il commento che RACCONTA il difetto curato il `2026-10-15`"),
 ("primo_ordine/_misura_theta_n.py", "CAMM-SATURAZIONE"):
    (L, "il commento che RACCONTA il difetto curato: oggi filtra per TIPO (`MO.FLUSSI`)"),
 ("primo_ordine/_collauda_deriva.py", "SAT."):
    (L, "`(1-bis)` CONFRONTA le due leggi: serve il numero della saturazione"),
 ("primo_ordine/_collauda_deriva.py", "import saturazione"):
    (L, "serve a `(1-bis)`, che confronta le due leggi"),
 ("primo_ordine/_collauda_deriva.py", "x^3/3"):
    (L, "la prosa che spiega PERCHE- `(1-bis)` si e- capovolto"),
 ("primo_ordine/_misura_mb2.py", "CAMM-SATURAZIONE"):
    (L, "`ORDINE_VECCHIO`: un confronto STORICO dichiarato"),
 ("primo_ordine/_misura_verso_l2.py", "CAMM-SATURAZIONE"):
    (L, "`ORDINE_VECCHIO`: un confronto STORICO dichiarato"),
 ("primo_ordine/_misura_spettro_l1.py", "CAMM-SATURAZIONE"):
    (S, "`ORDINE_VECCHIO` e- storico, ma `ordine_lineare` FILTRA PER NOME: oggi"
        " non toglie niente, e la <<parte lineare>> conterrebbe il flusso"),
 ("primo_ordine/bande.py", "CAMM-SATURAZIONE"):
    (S, "`salta = () if enne else (<nome>,)`: oggi `enne=False` NON SPEGNE NIENTE,"
        " cioe- un FALSO-ZERO dello strumento"),
 ("primo_ordine/bande.py", "elicita"): (L, "`somma_k h_k` come OSSERVABILE della serie"),
 ("primo_ordine/bande_floquet.py", "elicita"): (L, "`somma_k h_k` come OSSERVABILE della serie"),
 ("primo_ordine/scena_l2.py", "elicita"):
    (S, "il PARAMETRO della scena resta buono, ma la prosa dice che `beta` CAMBIA SEGNO"
        " con `h`: con `S3` `beta = -rho/(rho+Lambda)` ha SEMPRE lo stesso segno"),
 ("primo_ordine/_misura_pari_l2.py", "elicita"):
    (S, "l-affermazione `h = 0 => beta = 0` e- della saturazione: con `S3` e- FALSA"),
 ("primo_ordine/_misura_pari_l2.py", "SAT."): (S, "misura le forme della saturazione"),
 ("primo_ordine/_misura_pari_l2.py", "import saturazione"): (S, "come sopra"),
 ("primo_ordine/_misura_verso_l2.py", "elicita"):
    (S, "il <<verso>> si misurava sulla dipendenza da `h`, che `S3` NON HA"),
 ("primo_ordine/_misura_verso_l2.py", "SAT."): (S, "misura le forme della saturazione"),
 ("primo_ordine/_misura_verso_l2.py", "import saturazione"): (S, "come sopra"),
 ("primo_ordine/_misura_forme_l2.py", "elicita"):
    (S, "le QUATTRO FORME candidate erano tutte funzioni di `|h|/Lambda`"),
 ("primo_ordine/_misura_forme_l2.py", "CAMM-SATURAZIONE"):
    (S, "SOSTITUISCE l-operatore PER NOME: oggi sostituirebbe un pezzo che non gira"),
 ("primo_ordine/_misura_mb1.py", "CAMM-SATURAZIONE"):
    (S, "`PEZZI` e- una LISTA A MANO di `6` id: la legge nuova NON E- COPERTA, e la"
        " lista non ALZA"),
 ("primo_ordine/_collauda_tempo_proprio.py", "CAMM-SATURAZIONE"):
    (S, "il braccio `(2)` chiede che la SATURAZIONE dipenda da `dtau`: e- il controllo"
        " positivo del braccio `(1)`, e parla di una legge che non gira"),
 ("primo_ordine/_misura_mb2.py", "elicita"):
    (S, "misura sulla variabile vecchia, nel confronto `M-B2`"),
 ("primo_ordine/_misura_mb2.py", "import saturazione"):
    (S, "IMPORT MORTO: `SAT` non e- usato da nessuna parte nel file"),
 ("primo_ordine/energia.py", "import saturazione"):
    (S, "IMPORT MORTO: `SAT` non e- usato da nessuna parte nel file"),
 ("primo_ordine/deriva.py", "CAMM-SATURAZIONE"):
    (L, "`OPERATORE` registra ENTRAMBI, e il commento dice PERCHE- la riga resta"),
 ("primo_ordine/deriva.py", "elicita"):
    (S, "serve a `nat2`, la SCALA NATURALE del termine del vuoto"),
 ("primo_ordine/deriva.py", "SAT."):
    (S, "`nat2 = somma|h| + (pi/2) somma Lambda` e- l-asintoto DELLA SATURAZIONE:"
        " con `S3` quella scala NON vale, e la forma giusta va DERIVATA"),
 ("primo_ordine/deriva.py", "import saturazione"): (S, "serve solo a `nat2`"),
 ("primo_ordine/deriva.py", "x^3/3"):
    (S, "la prosa dice <<la saturazione era SPENTA>>: con `S3` il termine NON e- spento"
        " *(il braccio `(1-bis)` misura `337` volte piu- grande)*"),
}

righe = []
for p in sorted(glob.glob("primo_ordine/**/*.py", recursive=True)
                + glob.glob("csv/**/*.py", recursive=True)):
    rel = p.replace(os.sep, "/")
    if any(x in rel for x in FUORI):
        continue
    testo = io.open(p, encoding="utf-8").read()
    for nome, rx in CHIAVI:
        n = len(rx.findall(testo))
        if n:
            assert (rel, nome) in V, (
                "### LA COPPIA `%s` / `%s` NON HA UN VERDETTO: un uso nuovo della legge"
                " vecchia NON entra in silenzio -- si classifica, oppure questo"
                " generatore ALZA" % (rel, nome))
            righe.append((rel, nome, n) + V[(rel, nome)])
vuote = [k for k in V if k not in set((r[0], r[1]) for r in righe)]
assert not vuote, "verdetti che non corrispondono a nessuna coppia: %s" % (vuote,)

sca = [r for r in righe if r[3] == S]
leg = [r for r in righe if r[3] == L]
fil = sorted(set(r[0] for r in righe))
T = ["# IL CENSIMENTO DELLA LEGGE VECCHIA — **chi parla ancora di `|h|/Lambda`**",
     "",
     "*(punto `4` dell'integrazione del guardiano del `2026-10-16` sul `2-quater`. Il"
     " documento **si genera**: i conteggi escono dai file, e una coppia senza verdetto"
     " **fa ALZARE il generatore**.)*",
     "",
     "> ### \u26d4 **IL PERIMETRO:** `primo_ordine/**` e `csv/**`, **meno** `_archivio`,"
     " `_seal_*` e `_test_fork` *(che sono repertI: non si riscrivono)*.",
     "> ### **I SIMBOLI CERCATI:** `elicita` · `CAMM-SATURAZIONE` · `SAT.` · `x^3/3` ·"
     " `import saturazione`.",
     "",
     "## IL CONTO",
     "",
     "| | quante |",
     "|---|---|",
     "| coppie file/simbolo | **`%d`** |" % len(righe),
     "| file | **`%d`** |" % len(fil),
     "| ### **`SCADUTE`** | ### **`%d`** |" % len(sca),
     "| `LEGITTIME` | `%d` |" % len(leg),
     "",
     "### \u26a0 **`SCADUTO` non vuol dire <<rotto>>:** vuol dire che **nel perimetro"
     " attivo, OGGI**, quel codice misurerebbe, salterebbe o sostituirebbe **la legge"
     " sbagliata**. ### **Un referto gia' committato resta valido AL SUO COMMIT**"
     " *(`CLAUDE.md` \u00a79: un sigillo si rigira al commit che ha sigillato)*.",
     "",
     "## LE `%d` SCADUTE" % len(sca),
     "",
     "| file | simbolo | quanti | perche' e' SCADUTO |",
     "|---|---|---|---|"]
for rel, nome, n, _v, m in sca:
    T.append("| `%s` | `%s` | `%d` | %s |" % (rel, nome, n, m))
T += ["",
      "## LE `%d` LEGITTIME" % len(leg),
      "",
      "| file | simbolo | quanti | perche' e' LEGITTIMO |",
      "|---|---|---|---|"]
for rel, nome, n, _v, m in leg:
    T.append("| `%s` | `%s` | `%d` | %s |" % (rel, nome, n, m))
T += ["",
      "## \u26d4\u26d4 LE DUE COSE CHE QUESTO CENSIMENTO HA FATTO USCIRE, e che NON sono curate qui",
      "",
      "### \u2460 **`deriva.nat2` E' L'ASINTOTO DELLA SATURAZIONE, e per `S3` non esiste"
      " nella stessa forma** \u2014 ### **e' una DOMANDA PER LUCA**, non una scelta mia:",
      "",
      "```",
      "la scala naturale del termine del vuoto era   somma|h| + (pi/2) somma Lambda",
      "perche'   Lambda G(h/Lambda) -> h - (pi/2) Lambda sign(h)   a grande x,",
      "cioe' la saturazione e' LIMITATA da una funzione affine di h e Lambda.",
      "",
      "N = rho ln(rho/(rho+Lambda)) = -rho ln(1 + Lambda/rho)   NON e' limitata cosi':",
      "a Lambda/rho -> infinito DIVERGE come un logaritmo.",
      "```",
      "",
      "> ### \u26d4 **Quindi <<quale e' la scala naturale di `N`>> e' una scelta che cambia"
      " il DENOMINATORE di ogni numero relativo dei referti della deriva**, e"
      " ### **non la prendo io** *(`A1`: la legge, non il numero)*.",
      "",
      "### \u2461 **`bande.py` E `_misura_spettro_l1.py` SPENGONO `N` PER NOME** \u2014 cioe'"
      " oggi ### **non spengono niente**, e il braccio <<senza `N`>> misurerebbe"
      " ### **lo stesso sistema due volte.** ### \u2705 **La cura e' meccanica**"
      " *(filtrare per `MO.FLUSSI`, come `_misura_theta_n.py` dal `2026-10-16`)*, e sta"
      " ### **in coda**: non si tocca qui, perche' un interruttore alla volta.",
      ""]
dati = NL.join(T).encode("utf-8")
io.open("doc/CENSIMENTO_legge_vecchia.md", "wb").write(dati)
print("doc/CENSIMENTO_legge_vecchia.md:", len(righe), "coppie su", len(fil),
      "file --", len(sca), "SCADUTE e", len(leg), "LEGITTIME")
