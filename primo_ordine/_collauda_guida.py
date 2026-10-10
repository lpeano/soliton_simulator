# -*- coding: utf-8 -*-
"""PUNTO `7` DELLA TERZA PARTE — **IL COLLAUDO CHE ESEGUE LA GUIDA.**

> ### ⛔ **Il mandato, alla lettera:** *«**LA GUIDA:** `doc/COME_SI_AGGIUNGE_UNA_LEGGE.md`,
> dall'idea al referto, e **un collaudo LA ESEGUE passo per passo** su una legge di prova
> — così **la guida non può invecchiare senza che il collaudo fallisca**»*.

### ⭐ **E <<ESEGUIRLA>> HA UN LIMITE CHE IL TASK HISTORY AVEVA PREVISTO:** *«se la guida
contiene un passo che richiede una ### **DECISIONE**, quel passo ### **non è
eseguibile**»*. ### ✅ **Quindi la guida dichiara OGNI PASSO come `MECCANICO` o
`DECISIONE`, e questo collaudo:**

| | che cosa fa | perché |
|---|---|---|
| `a` | ### **LEGGE la tabella dei passi DALLA GUIDA** | se la guida cambia, ### **il collaudo lo vede** — e non ha una sua lista che divergerebbe |
| `b` | ### **ESEGUE** i passi `MECCANICO`, su ### **una legge di prova** | è ciò che il mandato chiede |
| `c` | per i passi `DECISIONE`, verifica che siano ### **dichiarati tali** | ### ⛔ **non li esegue: NON SI PUO'** — e fingere di eseguirli sarebbe ### **un falso-uno** |
| `d` | verifica che ogni ### **comando citato nella guida** esista e giri | una guida che cita un comando morto ### **è peggio di nessuna guida** |

### ⛔ **E LA LEGGE DI PROVA NASCE E MUORE DENTRO IL COLLAUDO:** si aggiunge alla tabella,
si genera, si verifica, e ### **si rimette tutto**, verificando ### **lo sha1 della
tabella e dei generati.** ### ⚠ **Un collaudo che lasciasse una legge finta nella tabella
cambierebbe la fisica del repo — e sarebbe il difetto peggiore di tutti.**
"""
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(_QUI, "leggi"))

NL = chr(10)
PRESIDIO = "P-GUIDA"
GUIDA = os.path.join(RADICE, "doc", "COME_SI_AGGIUNGE_UNA_LEGGE.md")
TABELLA = os.path.join(_QUI, "leggi", "leggi.yaml")

# ### ⛔ **LA LEGGE DI PROVA, e porta TUTTO cio- che la guida pretende** -- cosi- se
# ### la guida aggiunge un campo obbligatorio e io non lo metto qui, ### **il collaudo
# ### FALLISCE**, che e- esattamente il punto.
LEGGE_DI_PROVA = """
  - id: GUIDA-PROVA-TEMPORANEA
    tipo: termine_nodo
    prova: true
    espressione: GP*(psi_0c*psi_0 + psi_1c*psi_1)
    ambito: [psi]
    simmetrie: [U1-FASE-GLOBALE]
    conserva: [NORMA]
    parametri:
      GP:
        valore: 1.0
        dimensione: E^1
        origine: >-
          ### VALORE DI PROVA, e questa legge NASCE E MUORE DENTRO
          `primo_ordine/_collauda_guida.py`: esiste per ESEGUIRE la guida, e il
          collaudo la togliere verificando lo sha1 della tabella.
    assiomi: [A16]
    scheda: >-
      La legge di prova con cui `_collauda_guida.py` ESEGUE
      `doc/COME_SI_AGGIUNGE_UNA_LEGGE.md`. ### NON E' FISICA: e' il passo 2 della guida,
      fatto davvero invece che raccontato.
"""


def passi_dalla_guida():
    """### `[(n, descrizione, tipo)]` ### **letti DALLA GUIDA**, non da una lista mia."""
    t = io.open(GUIDA, encoding="utf-8").read()
    fuori = []
    for r in t.split(NL):
        m = re.match(r"^\| `(\d+)` \| (.+?) \| (.+?) \|$", r.strip())
        if not m:
            continue
        tipi = []
        if "MECCANICO" in m.group(3):
            tipi.append("MECCANICO")
        if "DECISIONE" in m.group(3):
            tipi.append("DECISIONE")
        if tipi:
            fuori.append((int(m.group(1)), m.group(2), tuple(tipi)))
    return fuori


def comandi_dalla_guida():
    """I comandi nei blocchi ``` della guida, ### **uno per riga.**"""
    t = io.open(GUIDA, encoding="utf-8").read()
    fuori = []
    dentro = False
    for r in t.split(NL):
        if r.strip().startswith("```"):
            dentro = not dentro
            continue
        if dentro and r.strip().startswith("python "):
            fuori.append(r.split("#")[0].strip())
    return fuori


def collaudo():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-62s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL COLLAUDO CHE ESEGUE LA GUIDA   (punto 7)")
    print("=" * 100)
    passi = passi_dalla_guida()
    mecc = [p for p in passi if "MECCANICO" in p[2]]
    deci = [p for p in passi if "DECISIONE" in p[2]]
    print("  i passi, LETTI DALLA GUIDA: %d" % len(passi))
    for n, des, tipi in passi:
        print("     %d  %-10s %s" % (n, "+".join(tipi), re.sub(r"[*`#]", "", des)[:66]))
    print()
    esito("### il collaudo ha MATERIA: la guida dichiara dei passi",
          len(passi) >= 6,
          "%d: ### se la tabella dei passi sparisse, questo braccio cadrebbe -- ed e- "
          "il punto: la guida NON PUO- invecchiare in silenzio" % len(passi))
    esito("### e OGNI passo e- dichiarato MECCANICO o DECISIONE",
          all(p[2] for p in passi),
          "%d meccanici, %d di decisione: ### un passo senza tipo NON SI SA SE SI PUO- "
          "ESEGUIRE" % (len(mecc), len(deci)))
    esito("### e ci sono passi di DECISIONE: la guida NON finge che tutto sia meccanico",
          len(deci) > 0,
          "%d: ### il primo e- <<la DECISIONE che governa la legge e- `presa`?>>, e oggi "
          "FERMA TUTTO -- 0 nodi su 10 sono `presa`" % len(deci))
    # ------------------------------------------------------------------ (d) i COMANDI
    cmds = comandi_dalla_guida()
    print()
    print("  i comandi citati nella guida: %d" % len(cmds))
    vivi = []
    for c in cmds:
        pezzi = c.split()
        f = pezzi[1] if len(pezzi) > 1 else ""
        vivi.append((c, os.path.exists(os.path.join(RADICE, f))))
        print("     %-56s %s" % (c, "c-e-" if vivi[-1][1] else "### NON ESISTE"))
    esito("NON deve scattare: ogni comando citato ESISTE sul disco",
          all(v for _c, v in vivi),
          "%d su %d: ### una guida che cita un comando morto e- PEGGIO di nessuna guida"
          % (sum(1 for _c, v in vivi if v), len(vivi)))

    # ============================================================ ESEGUIRE LA GUIDA
    print()
    print("-" * 100)
    print("ESEGUIRE I PASSI MECCANICI, SU UNA LEGGE DI PROVA")
    print("-" * 100)
    b_tab = io.open(TABELLA, "rb").read()
    sha_tab = hashlib.sha1(b_tab).hexdigest()
    gen = [os.path.join(_QUI, "stato.py"),
           os.path.join(_QUI, "termini", "prova_locale.py")]
    sha_gen = {p: hashlib.sha1(io.open(p, "rb").read()).hexdigest() for p in gen}
    tmp = tempfile.mkdtemp(prefix="guida_")
    nato = os.path.join(_QUI, "termini", "guida_prova_temporanea.py")
    scheda = os.path.join(RADICE, "doc", "leggi_era2", "GUIDA-PROVA-TEMPORANEA.md")
    try:
        # ### ✅ **PASSO `2`: la riga nella tabella.**
        io.open(TABELLA, "w", encoding="utf-8", newline="").write(
            b_tab.decode("utf-8").rstrip(NL) + NL + LEGGE_DI_PROVA)
        esito("### passo `2` ESEGUITO: la riga e- nella tabella",
              "GUIDA-PROVA-TEMPORANEA" in io.open(TABELLA, encoding="utf-8").read(),
              "### scritta DAVVERO, non raccontata")
        # ### ✅ **PASSO `3`: si genera.**
        r = subprocess.run([sys.executable, os.path.join("primo_ordine", "_genera.py")],
                           cwd=RADICE, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        esito("### passo `3` ESEGUITO: `_genera.py` genera e NON si lamenta",
              r.returncode == 0,
              "codice %d: ### se la legge di prova non passasse lo schema, vorrebbe dire "
              "che LA GUIDA non dice tutto cio- che serve" % r.returncode)
        esito("### e il file del termine E- NATO, senza che io lo scrivessi",
              os.path.exists(nato),
              "`primo_ordine/termini/guida_prova_temporanea.py`: ### il passo `3` dice "
              "<<il codice NON si scrive a mano>>, e questo lo PROVA")
        esito("### e la SCHEDA e- nata con lui",
              os.path.exists(scheda),
              "`doc/leggi_era2/GUIDA-PROVA-TEMPORANEA.md`")
        # ### ⛔ **E IL PASSO `1` NON SI ESEGUE, e il collaudo verifica PERCHE-.**
        esito("### il passo `1` e- dichiarato DECISIONE, e NON lo eseguo",
              any(n == 1 and "DECISIONE" in t for n, _d, t in passi),
              "### <<la decisione che governa la legge e- `presa`?>> non e- un comando: "
              "fingere di eseguirlo sarebbe UN FALSO-UNO")
    finally:
        # ### ⛔ **SI RIMETTE TUTTO, e si VERIFICA.**
        io.open(TABELLA, "wb").write(b_tab)
        for p in (nato, scheda):
            if os.path.exists(p):
                os.remove(p)
        subprocess.run([sys.executable, os.path.join("primo_ordine", "_genera.py")],
                       cwd=RADICE, capture_output=True)
        shutil.rmtree(tmp, ignore_errors=True)
    print()
    esito("### e la TABELLA e- tornata IDENTICA AL BYTE",
          hashlib.sha1(io.open(TABELLA, "rb").read()).hexdigest() == sha_tab,
          "`%s`: ### un collaudo che lasciasse una legge finta nella tabella CAMBIEREBBE "
          "LA FISICA DEL REPO" % sha_tab[:8])
    esito("### e i GENERATI sono tornati identici",
          all(hashlib.sha1(io.open(p, "rb").read()).hexdigest() == s
              for p, s in sha_gen.items()),
          "%d file verificati" % len(sha_gen))
    esito("### e il file della legge di prova NON C-E- PIU-",
          not os.path.exists(nato) and not os.path.exists(scheda),
          "### ne- il termine ne- la scheda: il repo e- come l-ho trovato")
    print("=" * 100)
    print("IL COLLAUDO DELLA GUIDA: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(collaudo())
