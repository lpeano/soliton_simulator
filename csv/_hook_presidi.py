# -*- coding: utf-8 -*-
"""**I PRESIDI CHE IMPEDISCONO** — `P3`, `P5`, `P8` come hook `pre-commit`.

*(Anticipati dal mandato sui presidi automatici, su ordine di Luca del 2026-09-25, perche' i tre
difetti che coprono sono **accaduti oggi**: `CLI-1`, `CONFIG-1`, `ANCORE-1`.)*

> ### `A9` — UN PRESIDIO CHE NON IMPEDISCE NON E' UN PRESIDIO.
> Le tre regole esistevano gia' **come prosa**, e tutte e tre sono state violate **dopo essere
> state scritte**. Qui **rifiutano il commit**.

| presidio | cosa impedisce | il difetto REALE da cui nasce |
|---|---|---|
| **`P3`** | un **sigillo** che configura il modulo **a mano** invece di passare dal CLI | `CLI-1`: `7/7` e `8/8` **con i flag MORTI da riga di comando** |
| **`P5`** | un referto che **non dichiara la configurazione INTERA** | `CONFIG-1`: sei misure con **28 leggi su 31 spente**, e ogni referto dichiarava i **4 flag accesi da me** |
| **`P8`** | un confronto che prende **il codice di prima da `HEAD`** | `ANCORE-1`: **25 sigilli**, e `A1` confrontava **il ramo spento con se stesso** |

**LA VIA D'USCITA ESISTE E OBBLIGA A DICHIARARE** *(la forma di `[SENZA-RELAZIONE]`)*:
`ESENTE-P3: <motivo>` in un commento del file *(col cancelletto davanti; qui non si scrive
per intero, perche' **questo scanner scandisce anche se stesso** -- ed e' giusto che lo
faccia: escludere un file dal proprio controllo e' il buco che `A9` descrive)*.
**E l'esenzione va ELENCATA** in `doc/ESENZIONI_presidi.md`,
generato da `--elenca`: **un'esenzione che non compare nell'elenco fa fallire il commit**, cosi'
non se ne accumulano di invisibili.

**COLLAUDO** *(`P1-sexies`)*: `--collaudo` prova **SEI** casi sintetici a risposta nota, **tre che
DEVONO bloccare e tre che NON devono**. **Il caso che deve fallire e' il piu' importante:** un
presidio che non blocca mai e' una nota.

ASCII puro.
"""
import ast
import io
import os
import re
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

NL = chr(10)
_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
ELENCO = os.path.join(RADICE, "doc", "ESENZIONI_presidi.md")
ALIAS = {"S", "S2", "_S", "_S5", "sim", "SIM"}
NOMI_PRIMA = ("vecchi", "prima", "_old", "old_", "pre_", "_pre", "precedent", "senza_cura")
ESENTE = re.compile(r"#\s*ESENTE-(P\d)\s*:\s*(.+)")


def _ast_sicuro(t):
    try:
        return ast.parse(t)
    except SyntaxError:
        return None


def _assegna_flag(arb):
    """Le assegnazioni `S.FLAG = ...` (MAIUSCOLE su un alias di modulo), anche nei FIGLI."""
    fuori = []

    def scan(a):
        for nd in ast.walk(a):
            if isinstance(nd, ast.Assign):
                for tg in nd.targets:
                    if (isinstance(tg, ast.Attribute) and isinstance(tg.value, ast.Name)
                            and tg.value.id in ALIAS and tg.attr.isupper()):
                        fuori.append(tg.attr)
    scan(arb)
    for nd in ast.walk(arb):
        if (isinstance(nd, ast.Constant) and isinstance(nd.value, str)
                and len(nd.value) > 120 and "import" in nd.value):
            sub = _ast_sicuro(nd.value)
            if sub is not None:
                scan(sub)
    return sorted(set(fuori))


def _usa(t, nome):
    return nome in t


def _scrive_referto(t, arb):
    """Il file SCRIVE un referto? (una `io.open(...).write` su un `DEST`/`REFERTO`)"""
    for nd in ast.walk(arb):
        if isinstance(nd, ast.Name) and nd.id in ("DEST", "REFERTO", "DEST_TXT"):
            if "io.open(" in t and ".write(" in t:
                return True
    return False


def _ancora_head(t, arb):
    """Prende «il codice di prima» da `HEAD`? (estrazione git + un nome che dice «vecchio»)"""
    righe = t.split(NL)
    for nd in ast.walk(arb):
        if not (isinstance(nd, ast.Constant) and isinstance(nd.value, str)):
            continue
        if not any(x in nd.value for x in ("HEAD:", "rev-parse HEAD", "cat-file")):
            continue
        # ⚠ LA FINESTRA GUARDA ANCHE INDIETRO, e non e' un dettaglio: il collaudo del caso
        #   «DEVE bloccare» **NON bloccava** perche' guardavo solo in AVANTI, e `VECCHIO = ...`
        #   sta tipicamente **PRIMA** dell'estrazione. **Il caso che deve fallire ha trovato un
        #   buco nel rilevatore** -- ed e' la ragione per cui `P1-sexies` lo pretende.
        i = max(0, (nd.lineno or 1) - 1)
        intorno = NL.join(righe[max(0, i - 3):i + 4]).lower()
        if any(x in intorno for x in NOMI_PRIMA):
            return nd.lineno
    return 0


def esamina(rel, t):
    """I guasti di UN file: lista di `(presidio, motivo)`. Le esenzioni sono a parte."""
    arb = _ast_sicuro(t)
    if arb is None:
        return [], {}
    esenzioni = dict((m.group(1).upper(), m.group(2).strip())
                     for m in ESENTE.finditer(t))
    g = []
    base = os.path.basename(rel)
    sotto_csv = rel.replace(chr(92), "/").startswith("csv/")
    # ---------------------------------------------------------------- P3
    if sotto_csv and (base.startswith("_sigillo") or base.startswith("_sig_")):
        am = _assegna_flag(arb)
        if am and not _usa(t, "_cli_flag"):
            g.append(("P3", "sigillo che configura il modulo A MANO (%s) senza passare dal CLI: "
                            "prova LA LEGGE, non IL FLAG" % ", ".join(am[:6])))
    # ---------------------------------------------------------------- P5
    if sotto_csv and _scrive_referto(t, arb):
        if not (_usa(t, "dichiara_configurazione") or _usa(t, "esigi_configurazione")):
            g.append(("P5", "scrive un referto senza dichiarare LA CONFIGURAZIONE INTERA "
                            "(`_cli_flag.dichiara_configurazione`)"))
    # ---------------------------------------------------------------- P8
    lin = _ancora_head(t, arb)
    if lin and not _usa(t, "sim_prima_del_flag"):
        g.append(("P8", "prende «il codice di prima» da `HEAD` (:%d): DIVENTA VUOTO appena la "
                        "cura e' committata" % lin))
    return g, esenzioni


def staged():
    q = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                       cwd=RADICE, capture_output=True, text=True)
    return [r.strip().replace(chr(92), "/") for r in (q.stdout or "").split(NL)
            if r.strip().endswith(".py")]


def elenco_attuale():
    try:
        return io.open(ELENCO, encoding="utf-8").read()
    except Exception:
        return ""


def controlla(coppie, elenco=None):
    """`coppie` = [(rel, testo)]. Restituisce (guasti, esenti_non_elencate)."""
    el = elenco_attuale() if elenco is None else elenco
    guasti, non_elencate = [], []
    for rel, t in coppie:
        g, es = esamina(rel, t)
        for pres, motivo in g:
            if pres in es:
                if ("%s|%s" % (rel, pres)) not in el:
                    non_elencate.append((rel, pres, es[pres]))
                continue
            guasti.append((pres, rel, motivo))
        for pres, mot in es.items():
            if ("%s|%s" % (rel, pres)) not in el:
                if (rel, pres, mot) not in non_elencate:
                    non_elencate.append((rel, pres, mot))
    return guasti, non_elencate


def scrivi_elenco():
    """Genera `doc/ESENZIONI_presidi.md` da TUTTO `csv/` (non dal solo staged)."""
    righe = ["# LE ESENZIONI DICHIARATE AI PRESIDI — **generato**", "",
             "*(`csv/_hook_presidi.py --elenca`. Un'esenzione che NON compare qui **fa fallire il",
             "commit**: cosi' non se ne accumulano di invisibili.)*", "",
             "| file\\|presidio | motivo dichiarato |", "|---|---|"]
    n = 0
    for base, _dd, ff in os.walk(os.path.join(RADICE, "csv")):
        if "/_tmp" in base.replace(chr(92), "/") or "__pycache__" in base:
            continue
        for f in sorted(ff):
            if not f.endswith(".py"):
                continue
            p = os.path.join(base, f)
            rel = os.path.relpath(p, RADICE).replace(chr(92), "/")
            t = io.open(p, encoding="utf-8", errors="replace").read()
            for m in ESENTE.finditer(t):
                righe.append("| `%s|%s` | %s |" % (rel, m.group(1).upper(), m.group(2).strip()))
                n += 1
    righe += ["", "```", "esenzioni dichiarate   %d" % n, "```"]
    io.open(ELENCO, "w", encoding="utf-8", newline=NL).write(NL.join(righe) + NL)
    return n


def arretrato():
    """Cosa fallirebbe su TUTTO `csv/`: **una MISURA, non un blocco.**"""
    coppie = []
    for base, _dd, ff in os.walk(os.path.join(RADICE, "csv")):
        b = base.replace(chr(92), "/")
        if "/_tmp" in b or "__pycache__" in b:
            continue
        for f in sorted(ff):
            if not f.endswith(".py") or f.startswith("_old_sim_pre_") or f.endswith("._sim.py"):
                continue
            p = os.path.join(base, f)
            coppie.append((os.path.relpath(p, RADICE).replace(chr(92), "/"),
                           io.open(p, encoding="utf-8", errors="replace").read()))
    g, _ = controlla(coppie, elenco="")
    per = {}
    for pres, rel, _m in g:
        per.setdefault(pres, []).append(rel)
    return per, len(coppie)


# ============================================================================== IL COLLAUDO
SORG = {
    # --- P3: DEVE bloccare / NON deve
    "blocca_P3": ("csv/_seal_fork/_sigillo_finto.py",
                  "import x" + NL + "S.SEMINA_MATURA = True" + NL),
    "passa_P3": ("csv/_seal_fork/_sigillo_finto2.py",
                 "import _cli_flag" + NL + "S.SEMINA_MATURA = True" + NL),
    # --- P5: DEVE bloccare / NON deve
    "blocca_P5": ("csv/_test_fork/_misura_finta.py",
                  "import io" + NL + "DEST = 'x.txt'" + NL
                  + "io.open(DEST, 'w').write('ciao')" + NL),
    "passa_P5": ("csv/_test_fork/_misura_finta2.py",
                 "import io" + NL + "import _cli_flag" + NL + "DEST = 'x.txt'" + NL
                 + "_cli_flag.dichiara_configurazione(S, print)" + NL
                 + "io.open(DEST, 'w').write('ciao')" + NL),
    # --- P8: DEVE bloccare / NON deve
    "blocca_P8": ("csv/_seal_fork/_sigillo_finto3.py",
                  "import subprocess" + NL
                  + "VECCHIO = 'v.py'" + NL
                  + "g = subprocess.run(['git', 'cat-file', '-p', 'HEAD:soliton_simulator.py'])"
                  + NL),
    "passa_P8": ("csv/_seal_fork/_sigillo_finto4.py",
                 "import _cli_flag" + NL + "VECCHIO = 'v.py'" + NL
                 + "_cli_flag.sim_prima_del_flag('X', VECCHIO)" + NL
                 + "# l'ancora e' il PADRE del commit, non `HEAD:soliton_simulator.py`" + NL),
}


def collaudo():
    print("=" * 96)
    print("COLLAUDO DEI PRESIDI -- sei casi a risposta NOTA (`P1-sexies`)")
    print("=" * 96)
    ok = True
    for nome, (rel, t) in sorted(SORG.items()):
        atteso_blocca = nome.startswith("blocca")
        g, _ = controlla([(rel, t)], elenco="")
        pres = nome.split("_")[-1]
        blocca = any(p == pres for p, _r, _m in g)
        buono = (blocca == atteso_blocca)
        ok = ok and buono
        print("  %-11s %-34s atteso %-9s ottenuto %-9s %s"
              % (nome, os.path.basename(rel), "BLOCCA" if atteso_blocca else "passa",
                 "BLOCCA" if blocca else "passa", "OK" if buono else "!! SBAGLIATO"))
    # e l'ESENZIONE: dichiarata e NON elencata -> deve fallire; elencata -> passa
    rel, t = SORG["blocca_P3"]
    # il marcatore si COMPONE, cosi' non compare per intero nel sorgente dello scanner
    t_es = t + chr(35) + " ESENTE-P3: motivo di prova" + NL
    _g, non_el = controlla([(rel, t_es)], elenco="")
    print("  %-11s %-34s atteso %-9s ottenuto %-9s %s"
          % ("esenz_nuda", os.path.basename(rel), "BLOCCA", "BLOCCA" if non_el else "passa",
             "OK" if non_el else "!! SBAGLIATO"))
    ok = ok and bool(non_el)
    _g2, non_el2 = controlla([(rel, t_es)], elenco="%s|P3" % rel)
    print("  %-11s %-34s atteso %-9s ottenuto %-9s %s"
          % ("esenz_elenc", os.path.basename(rel), "passa",
             "BLOCCA" if non_el2 else "passa", "OK" if not non_el2 else "!! SBAGLIATO"))
    ok = ok and not non_el2
    print()
    print("COLLAUDO: %s" % ("8/8 OK" if ok else "FALLITO"))
    return 0 if ok else 1


HOOK = NL.join([
    "#!/bin/sh",
    "# [presidi P3/P5/P8] installato da csv/_hook_presidi.py --installa",
    'python "$(git rev-parse --show-toplevel)/csv/_hook_presidi.py" --pre-commit || exit 1',
    ""])


def installa():
    p = os.path.join(RADICE, ".git", "hooks", "pre-commit")
    io.open(p, "w", encoding="utf-8", newline=NL).write(HOOK)
    print("installato: %s" % p)
    print("⚠ I HOOK NON SONO VERSIONATI DA GIT: un clone nuovo NON ce l'ha finche' non lo")
    print("  installa. E' meno di un presidio completo, e va detto invece di chiamarlo tale.")
    return 0


def pre_commit():
    coppie = []
    for rel in staged():
        p = os.path.join(RADICE, rel)
        if os.path.exists(p):
            coppie.append((rel, io.open(p, encoding="utf-8", errors="replace").read()))
    g, non_el = controlla(coppie)
    if not g and not non_el:
        return 0
    sys.stderr.write(NL + "[PRESIDI] *** COMMIT RIFIUTATO ***" + NL + NL)
    for pres, rel, motivo in g:
        sys.stderr.write("  %s  %s" % (pres, rel) + NL + "      %s" % motivo + NL + NL)
    for rel, pres, mot in non_el:
        sys.stderr.write("  ESENZIONE NON ELENCATA  %s|%s: %s" % (rel, pres, mot) + NL
                         + "      rigenera l'elenco:  python csv/_hook_presidi.py --elenca"
                         + NL + NL)
    sys.stderr.write("  CHE FARE: passare dal CLI (`_cli_flag`), dichiarare la configurazione" + NL
                     + "  intera, ancorare al PADRE del commit -- oppure dichiarare" + NL
                     + "  'ESENTE-<Pn>: <motivo>' (col cancelletto davanti) nel file E"
                     + " rigenerare l'elenco." + NL + NL)
    return 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--collaudo" in a:
        sys.exit(collaudo())
    if "--installa" in a:
        sys.exit(installa())
    if "--elenca" in a:
        print("esenzioni elencate: %d" % scrivi_elenco())
        sys.exit(0)
    if "--arretrato" in a:
        per, quanti = arretrato()
        print("ARRETRATO su %d file di csv/ (una MISURA, non un blocco):" % quanti)
        for k in sorted(per):
            print("  %-4s %d file" % (k, len(per[k])))
            for r in per[k][:40]:
                print("       %s" % r)
        sys.exit(0)
    if "--pre-commit" in a:
        sys.exit(pre_commit())
    print(__doc__)
    sys.exit(0)
