r"""IL PUNTO DELLA SITUAZIONE — generato **DALL'INDICE**, non dal Markdown e non a memoria.

**Convertito il 2026-09-26** *(decisione di Luca, punto 2 di `LETTORI-INDICE`)*: prima leggeva
`doc/STATO_RUN.md` e doveva **inferire** che cosa fosse una riga e quale fosse il suo marcatore; ora
legge **soltanto `doc/INDICE_ID.tsv`**, dove `id`, `titolo_breve`, `tipo`, `stato` e **`avanzamento`**
sono **campi dichiarati**.

**`avanzamento` e' il campo aggiunto per questa conversione** *(`IN CORSO` / `IN CODA` / `FATTO` /
`BLOCCATO` / `CON RISERVA`)*, e porta con se' **il difetto che questo strumento aveva gia' curato:
vince il PRIMO MARCATORE NEL TESTO, non il primo di una lista** — senno' una riga `▶ IN CORSO` che
contiene tre `✅` dei pezzi fatti risulterebbe `FATTO` **mentre il run sta girando**.

## ⚠ CHE COSA CAMBIA NELL'OUTPUT, e va detto

- **i DIFETTI si raggruppano per il campo `stato` dell'indice** *(`aperto`/`chiuso`/`non-difetto`/
  `da-decidere`)* e non piu' per le parole della prosa *(`CURA INEFFICACE`, `DA RIMISURARE`…)*: **il
  raggruppamento e' piu' grossolano ma DICHIARATO**, e chi vuole il dettaglio legge la fonte.
- **una voce che vive nel Markdown ma NON ha un ID non compare**: e' il prezzo della fonte unica, ed
  e' **il caso che il collaudo verifica** *(`CONTAGIO`: un'etichetta di una sola parola maiuscola,
  che per la specifica di Luca non e' un ID)*.

⚠ **SOLA LETTURA.** Legge `doc/INDICE_ID.tsv` e `git log`. Non esegue niente e non tocca nessun run.
"""
# ESENTE-P5: non importa il simulatore e non lo fa girare. Legge un TSV e `git log`.
import io
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
FONTE = os.path.join(RADICE, "doc", "INDICE_ID.tsv")
OUT = os.path.join(RADICE, "doc", "PUNTO_DELLA_SITUAZIONE.md")
NL = chr(10)
TAB = chr(9)

TIPI_DIFETTO = ("difetto", "sospetto")
ORDINE = ["IN CORSO", "CON RISERVA", "IN CODA", "(senza marcatore)", "BLOCCATO", "FATTO"]
#   i tipi che NON sono lavoro da elencare qui: etichette locali e teoria
TIPI_FUORI = ("criterio-locale", "assioma", "standard")


def leggi():
    r = io.open(FONTE, encoding="utf-8", newline="").read().split(NL)
    col = [c.strip() for c in r[0].split(TAB)]
    fuori = []
    for x in r[1:]:
        if not x.strip():
            continue
        c = (x.split(TAB) + [""] * len(col))[:len(col)]
        fuori.append(dict(zip(col, [y.strip() for y in c])))
    return fuori


def ultimo_commit(chiave):
    """L'ultimo commit che NOMINA la chiave nel messaggio. Se non c'e', si dice."""
    try:
        r = subprocess.run(["git", "log", "-1", "--format=%h %cd", "--date=format:%H:%M",
                            "--grep=%s" % chiave, "-i"],
                           cwd=RADICE, capture_output=True, text=True)
        s = (r.stdout or "").strip()
        return s if s else "—"
    except Exception:
        return "—"


def collaudo(W, voci):
    """`P1-sexies`, NEI DUE VERSI: una voce dell'indice compare; una che NON c'e' non compare."""
    W("COLLAUDO (`P1-sexies`) -- I DUE VERSI" + NL + "-" * 90 + NL)
    e = []
    _ids = set(v["id"] for v in voci)
    _campi = set(voci[0].keys()) if voci else set()

    ok0 = {"id", "titolo_breve", "tipo", "stato", "avanzamento"} <= _campi
    W("K0 l'indice porta i campi che servono (`avanzamento` compreso) -> %s%s"
      % ("OK" if ok0 else "*** MANCA un campo: " + str(
          {"id", "titolo_breve", "tipo", "stato", "avanzamento"} - _campi), NL))
    e.append(ok0)

    ok1 = "SCALE-TW" in _ids
    W("K1 DEVE COMPARIRE: una voce NOTA dell'indice (`SCALE-TW`) -> %s%s"
      % ("OK" if ok1 else "*** una voce dell'indice non arriva ***", NL))
    e.append(ok1)

    # il caso che DEVE fallire: una voce che vive SOLO nel Markdown
    _md = os.path.join(RADICE, "doc", "STATO_RUN.md")
    _nel_md = "CONTAGIO" in io.open(_md, encoding="utf-8", errors="replace").read()
    ok2 = _nel_md and ("CONTAGIO" not in _ids)
    W("K2 IL CASO CHE DEVE FALLIRE: `CONTAGIO` e' nel Markdown (%s) e NON nell'indice (%s) -> %s%s"
      % ("si'" if _nel_md else "NO", "corretto" if "CONTAGIO" not in _ids else "*** c'e' ***",
         "OK: una voce SENZA ID non compare, ed e' il prezzo DICHIARATO della fonte unica"
         if ok2 else "*** il collaudo non misura niente ***", NL))
    e.append(ok2)

    ok3 = any(v["tipo"] in TIPI_DIFETTO for v in voci) and \
        any(v["tipo"] not in TIPI_DIFETTO for v in voci)
    W("K3 i difetti si distinguono dai task **per il campo `tipo`**, non per una regex sull'id -> %s%s"
      % ("OK" if ok3 else "*** NO ***", NL))
    e.append(ok3)

    ok4 = all(v.get("avanzamento") for v in voci)
    W("K4 nessuna voce senza `avanzamento` («(senza marcatore)» e' un VALORE, non un vuoto) -> %s%s"
      % ("OK" if ok4 else "*** ci sono voci col campo VUOTO ***", NL))
    e.append(ok4)

    ok = all(e)
    W("-" * 90 + NL + "  -> %s%s%s" % ("si genera" if ok else "*** NON genero ***", NL, NL))
    return ok


def main():
    voci = leggi()
    if not collaudo(sys.stdout.write, voci):
        return 1
    vv = [v for v in voci if v["tipo"] not in TIPI_FUORI]
    # ⚠ SOLO LE VOCI CON UN MARCATORE: senza questo filtro il documento elencava **438 righe**,
    #   di cui quasi tutte `(senza marcatore)` -- cioe' **ogni ID dell'indice**, compresi quelli che
    #   non sono lavoro *(`AAAA-MM-GG`, `AUTO-MANUTENZIONE`…)*. **Un documento che elenca tutto non
    #   dice niente**: il "punto della situazione" e' il LAVORO, e il lavoro porta un marcatore.
    task = [v for v in vv if v["tipo"] not in TIPI_DIFETTO
            and v.get("avanzamento") != "(senza marcatore)"]
    _muti = [v for v in vv if v["tipo"] not in TIPI_DIFETTO
             and v.get("avanzamento") == "(senza marcatore)"]
    dif = [v for v in vv if v["tipo"] in TIPI_DIFETTO]
    o = io.open(OUT, "w", encoding="utf-8", newline=NL)
    W = o.write
    W("# IL PUNTO DELLA SITUAZIONE — **generato dall'INDICE**" + NL + NL)
    W("> **SOLA LETTURA.** Generato da `csv/_punto_della_situazione.py` leggendo **soltanto**" + NL)
    W("> `doc/INDICE_ID.tsv`. **Non e' scritto a memoria e non fa piu' parsing di Markdown**:" + NL)
    W("> se un task manca qui, **manca dall'indice** — e quello e' il difetto da correggere." + NL)
    W("> **⚠ Una voce senza ID non compare**: e' il prezzo dichiarato della fonte unica, e il" + NL)
    W("> collaudo lo verifica *(il caso `CONTAGIO`)*." + NL + NL)
    W("```" + NL)
    W("voci nell'indice   %4d" % len(voci) + NL)
    W("elencate qui       %4d   (tolte le etichette locali, gli assiomi e gli standard)" % len(vv)
      + NL)
    W("  di cui task      %4d" % len(task) + NL)
    W("  di cui difetti   %4d   (tipo `difetto` o `sospetto`)" % len(dif) + NL)
    W("  senza marcatore  %4d   NON elencate: non sono lavoro in corso" % len(_muti) + NL)
    W("```" + NL + NL)
    W("> ## ⚠ **DUE LIMITI DICHIARATI, e vengono dalla FONTE UNICA**" + NL)
    W("> ① **le voci senza marcatore non si elencano** *(%d)*: nell'indice ci sono **tutti** gli"
      % len(_muti) + NL)
    W("> ID, anche quelli che non sono lavoro. **Il punto della situazione e' il LAVORO.**" + NL)
    W("> ② **alcune voci della coda NON HANNO UN ID che l'indice riconosca**, e quindi non possono"
      + NL)
    W("> comparire: **`S-MIT1`/`S-MIT2`** *(stem di UNA lettera prima del trattino)*, **`FAMIGLIE`**,"
      + NL)
    W("> **`PROVE`**, **`PATTERN`** *(una parola sola)*, **`4-bis`**, **`8-bis`**, **`G4-bis`**"
      + NL)
    W("> *(suffisso minuscolo)*, **`V`** *(una lettera)*. **Sono `8` righe della coda unica: se"
      + NL)
    W("> devono comparire, gli serve un ID** — e non e' una regex piu' larga, e' una rinomina."
      + NL + NL)
    for s in ORDINE:
        gruppo = [x for x in task if x.get("avanzamento") == s]
        if not gruppo:
            continue
        W("## %s — %d" % (s, len(gruppo)) + NL + NL)
        W("| id | cosa | tipo | ultimo commit che lo nomina |" + NL + "|---|---|:--:|---|" + NL)
        for x in sorted(gruppo, key=lambda y: y["id"]):
            cosa = re.sub(r"\s+", " ", x.get("titolo_breve", ""))[:130].replace("|", "/")
            W("| **`%s`** | %s | `%s` | `%s` |"
              % (x["id"], cosa, x.get("tipo", ""), ultimo_commit(x["id"])) + NL)
        W(NL)
    st = {}
    for x in dif:
        st.setdefault(x.get("stato", "?"), []).append(x["id"])
    W("## DIFETTI E SOSPETTI — %d righe" % len(dif) + NL + NL)
    W("> **Il raggruppamento e' per il campo `stato` dell'indice**, non per le parole della prosa:"
      + NL)
    W("> piu' grossolano di prima *(non distingue `CURA INEFFICACE` da `DA RIMISURARE`)*, ma"
      + NL + "> **dichiarato**. Il dettaglio sta nella fonte." + NL + NL)
    W("| stato | quanti | quali |" + NL + "|---|--:|---|" + NL)
    for k in sorted(st):
        W("| `%s` | %d | %s |" % (k, len(st[k]), " ".join("`%s`" % y for y in sorted(st[k]))) + NL)
    _d = [x["id"] for x in dif if re.fullmatch(r"D\d\d", x["id"])]
    _s = [x["id"] for x in dif if re.fullmatch(r"S\d\d?", x["id"])]
    W(NL + "**ID massimo usato:** difetti `%s` · sospetti `%s`. **Gli ID non si riusano.**"
      % (max(_d or ["—"]), max(_s or ["—"])) + NL)
    o.close()
    print(io.open(OUT, encoding="utf-8").read()[:1400])
    return 0


if __name__ == "__main__":
    sys.exit(main())
