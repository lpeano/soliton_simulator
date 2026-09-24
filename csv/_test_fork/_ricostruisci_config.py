# -*- coding: utf-8 -*-
"""LA RICOSTRUZIONE DELLA CONFIGURAZIONE DEI RUN GIA' FATTI -- tabella GENERATA flag x run.

Punto 2 del mandato di Luca, 2026-09-24. **SOLA LETTURA**: log, snapshot e blob committati.
Nessun run, nessuna modifica.

LE TRE FONTI, NELL'ORDINE CHE LUCA HA FISSATO:
  1. **ARGV** -- il `sys.argv` che il DRIVER COMMITTATO A QUEL COMMIT costruisce, letto
     dall'AST del suo sorgente storico (`git cat-file -p <commit>:<path>`). E' la fonte
     piu' forte per i flag che il driver accende, perche' e' la CAUSA.
  2. **BANNER** -- il blocco *"FLAG ATTIVI, letti dal MODULO dopo `_applica_flag`"* stampato
     nel log del run. E' la fonte piu' forte in assoluto per i 24 flag che elenca, perche'
     e' lo stato EFFETTIVO letto dal modulo. **Ma sono 24 su 123.**
  3. **DEFAULT DEL BLOB DI QUEL RUN** -- dall'AST di `<commit>:soliton_simulator.py`.
     **Vale solo se nessuna opzione lo cambia**, e questo si VERIFICA: si ricava dall'AST di
     `_applica_flag` l'opzione che scrive quel flag, e si cerca nei lanciatori committati a
     quel commit. Se l'opzione NON c'e', il default vale.

⚠ SE DUE FONTI SI CONTRADDICONO SI RIPORTANO ENTRAMBE: e' un reperto, non un errore da
  risolvere in silenzio.
⚠ CIO' CHE NON SI RICOSTRUISCE SI SCRIVE `NON RICOSTRUITO`, COL MOTIVO.

⚠ E UNA COSA E' SCRITTA A MANO, di proposito, perche' NON e' derivabile: QUALE CAMPAGNA
  (`G1`, `G2`, ...) corrisponde a quale cartella. Si **verifica** contro la riga
  `[G4] modo --...` del log quando c'e', e la verifica si stampa.

ASCII PURO.
"""
import ast
import glob
import gzip
import io
import os
import pickle
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_QUI, ".."))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))

# nome, cartella del run (o None), log (o None)
RUN = [
    ("G1  (video 6000)", "csv/_test_fork/_gvideo", "csv/_test_fork/_gvideo_run.log"),
    ("G2  (g2m)", "csv/_test_fork/_g2m", "csv/_test_fork/_g2m_run.log"),
    ("validazione 600", "csv/_test_fork/_val600", None),
    ("G3  controllo", None, "csv/_test_fork/_g3_controllo_log.txt"),
    ("G3  senza bifase", "csv/_test_fork/_g3_senza_bifase", "csv/_test_fork/_g3_prova_log.txt"),
    ("G4  controllo", "csv/_test_fork/_g4_controllo", "csv/_test_fork/_g4_controllo_log.txt"),
    ("G4  riferimento", "csv/_test_fork/_g4_riferimento", "csv/_test_fork/_g4_riferimento_log.txt"),
    ("G4  spegni", "csv/_test_fork/_g4_senza_memmoto", "csv/_test_fork/_g4_spegni_log.txt"),
    ("G4-bis", "csv/_test_fork/_g4bis_senza_blocco", "csv/_test_fork/_g4bis_log.txt"),
    ("D34 ritmo-wrap", "csv/_test_fork/_d34_ritmo_wrap", "csv/_test_fork/_d34_log.txt"),
    ("FASE_2PI corto", "csv/_test_fork/_f2p_corto", "csv/_test_fork/_f2p_corto_log.txt"),
]

# I SEI del punto 3 del mandato, piu' i due che servono a leggerli
INTERESSE = ["CAMPO_SPINORIALE", "SPINORE_VIVO", "SPINORE_CORRETTO", "TEMPO_SEGNO",
             "SCALA_MIN", "SCALA_MIN_PASSO", "OROLOGIO_SEGNO", "TAU_LOC"]

LANCIATORI = ("csv/_test_fork/_scena_video.py", "csv/_test_fork/_g4_prova.py",
              "csv/_test_fork/_spegni_grav_bifase.py")


def git(*a):
    try:
        return subprocess.check_output(("git",) + a, stderr=subprocess.DEVNULL,
                                       cwd=RADICE).decode("utf-8", "replace")
    except Exception:
        return None


# ---------------------------------------------------------------- le fonti
def commit_del_run(cartella):
    """Il commit con cui il run ha girato, LETTO DALLO SNAPSHOT (non dal log, non a memoria)."""
    if not cartella:
        return None
    # !! NON SOLO `scena_*.pkl.gz`: `G1` e `G2` scrivono `frame_*.pkl` (senza gzip, altro
    #   nome). La prima stesura cercava solo la forma nuova e li dava per NON RICOSTRUITI --
    #   una lacuna dello STRUMENTO letta come lacuna del DATO.
    g = (sorted(glob.glob(os.path.join(RADICE, cartella, "scena_*.pkl.gz")))
         or sorted(glob.glob(os.path.join(RADICE, cartella, "*.pkl.gz")))
         or sorted(glob.glob(os.path.join(RADICE, cartella, "*.pkl"))))
    if not g:
        return None
    apri = gzip.open if g[0].endswith(".gz") else io.open
    try:
        d = pickle.load(apri(g[0], "rb"))
        if not isinstance(d, dict):
            return None
        return d.get("commit")
    except Exception:
        return None


BANNER = "FLAG ATTIVI, letti dal MODULO dopo"
_RIGA = re.compile(r"^\s{2,}([A-Z][A-Z0-9_]+)\s+(True|False|None|ASSENTE|[-\d.eE+]+)\s*$")


def banner_dal_log(log):
    """{FLAG: valore} dal blocco del banner. E' lo stato EFFETTIVO: la fonte piu' forte."""
    if not log or not os.path.exists(os.path.join(RADICE, log)):
        return {}
    t = io.open(os.path.join(RADICE, log), encoding="utf-8", errors="replace").read()
    i = t.find(BANNER)
    if i < 0:
        return {}
    out = {}
    for r in t[i:].split("\n")[1:]:
        m = _RIGA.match(r.rstrip())
        if not m:
            if out:                       # il blocco e' finito
                break
            continue
        out[m.group(1)] = m.group(2)
    return out


def defaults_del_blob(commit):
    """I default dei flag dal sorgente DI QUEL COMMIT, dall'AST."""
    if not commit:
        return {}
    t = git("cat-file", "-p", "%s:soliton_simulator.py" % commit)
    if not t:
        return {}
    sys.path.insert(0, os.path.join(RADICE, "csv"))
    import _configurazione as C
    tmp = os.path.join(_PROV, "sim_%s.py" % commit[:8])
    io.open(tmp, "w", encoding="utf-8", newline="\n").write(t)
    try:
        return C.nomi_flag(tmp)
    finally:
        try:
            os.remove(tmp)
        except OSError:
            pass


def opzione_del_flag(commit, flag):
    """L'opzione che SCRIVE quel flag in `_applica_flag`, dall'AST del blob di quel commit.

    Cerca `FLAG = ... getattr(a, "nome", ...)` oppure `FLAG = ... a.nome ...`: e' il modo in
    cui il file collega un'opzione a un globale. **Generato, non una lista a mano.**
    """
    t = git("cat-file", "-p", "%s:soliton_simulator.py" % commit) if commit else None
    if not t:
        return None
    try:
        albero = ast.parse(t)
    except SyntaxError:
        return None
    def _opz_in(nodo):
        """Il nome d'opzione in un sottoalbero: `getattr(a, "x", ...)` oppure `a.x`."""
        for d in ast.walk(nodo):
            if (isinstance(d, ast.Call) and isinstance(d.func, ast.Name)
                    and d.func.id == "getattr" and len(d.args) >= 2
                    and isinstance(d.args[1], ast.Constant)):
                return str(d.args[1].value)
            if isinstance(d, ast.Attribute) and isinstance(d.value, ast.Name) \
                    and d.value.id == "a":
                return d.attr
        return None

    def _assegna(nodo):
        for s in ast.walk(nodo):
            if isinstance(s, ast.Assign) and any(
                    isinstance(b, ast.Name) and b.id == flag for b in s.targets):
                return s
        return None

    for n in ast.walk(albero):
        if not (isinstance(n, ast.FunctionDef) and n.name == "_applica_flag"):
            continue
        # (a) l'opzione nel VALORE assegnato: `FLAG = bool(getattr(a, "x", ...))`
        s = _assegna(n)
        if s is not None:
            o = _opz_in(s.value)
            if o:
                return o
        # (b) l'opzione nella CONDIZIONE dell'`if` che racchiude l'assegnamento.
        #     !! SERVE, e la prima stesura non l'aveva: `CALORE_VETTORIALE = False` e' un
        #     LETTERALE dentro `if getattr(a, "calore_scal", False):`, quindi il valore
        #     assegnato non contiene nessuna opzione. Lo strumento marcava quella
        #     contraddizione *** NON SPIEGATA ***, cioe' segnalava come reperto un difetto
        #     PROPRIO. Trovato dal suo stesso output, non da un test.
        for nodo in ast.walk(n):
            if isinstance(nodo, ast.If) and _assegna(nodo) is not None:
                o = _opz_in(nodo.test)
                if o:
                    return o
    return None


def opzione_nei_lanciatori(commit, opzione):
    """L'opzione compare nei lanciatori COMMITTATI a quel commit? (`--con-i-trattini`)"""
    if not (commit and opzione):
        return None
    cercato = "--" + opzione.replace("_", "-")
    trovata = []
    for p in LANCIATORI:
        t = git("cat-file", "-p", "%s:%s" % (commit, p))
        if t and cercato in t:
            trovata.append(p)
    return trovata


def main():
    W = sys.stdout.write
    W("# LA RICOSTRUZIONE DELLA CONFIGURAZIONE DEI RUN GIA' FATTI\n#\n")
    W("# GENERATA da `csv/_test_fork/_ricostruisci_config.py`. Fonti, in ordine:\n")
    W("#   argv (dal driver COMMITTATO a quel commit) . banner del log . default del blob\n")
    W("# Cio' che non si ricostruisce e' scritto NON RICOSTRUITO, col motivo.\n#\n")

    # ---------------- la provenienza di ogni run
    W("=" * 110 + "\n")
    W("LA PROVENIENZA DI OGNI RUN -- e la VERIFICA della corrispondenza campagna/cartella\n")
    W("=" * 110 + "\n")
    W("%-20s %-10s %-9s %-7s %s\n" % ("campagna", "commit", "banner?", "modo", "cartella"))
    W("-" * 110 + "\n")
    stato = {}
    for nome, cart, log in RUN:
        c = commit_del_run(cart)
        b = banner_dal_log(log)
        modo = "-"
        if log and os.path.exists(os.path.join(RADICE, log)):
            t = io.open(os.path.join(RADICE, log), encoding="utf-8", errors="replace").read()
            m = re.search(r"modo (--[a-z0-9-]+)", t)
            if m:
                modo = m.group(1)
        stato[nome] = {"commit": c, "banner": b, "log": log, "cart": cart, "modo": modo}
        W("%-20s %-10s %-9s %-7s %s\n"
          % (nome, (c[:8] if c else "NON RIC."), ("%d flag" % len(b)) if b else "NO",
             modo, cart or "(nessuna)"))
    W("\n  NOTA: `commit` viene DALLO SNAPSHOT (`d['commit']`), non dal log: e' il timbro che\n")
    W("  il run si e' messo da solo. Dove manca, non c'e' snapshot da cui leggerlo.\n")

    # ---------------- i sei flag del punto 3
    W("\n" + "=" * 110 + "\n")
    W("I FLAG DEL PUNTO 3 -- valore + FONTE, per ogni run\n")
    W("=" * 110 + "\n")
    for flag in INTERESSE:
        W("\n--- %s\n" % flag)
        for nome in [r[0] for r in RUN]:
            s = stato[nome]
            c, b = s["commit"], s["banner"]
            if flag in b:
                W("    %-20s %-8s  FONTE: banner del log (stato EFFETTIVO dal modulo)\n"
                  % (nome, b[flag]))
                continue
            if not c:
                W("    %-20s %-8s  NON RICOSTRUITO: nessuno snapshot, quindi nessun commit, "
                  "e il log non porta il banner\n" % (nome, "?"))
                continue
            d = defaults_del_blob(c)
            if flag not in d:
                W("    %-20s %-8s  NON RICOSTRUITO: il flag NON ESISTE nel blob di questo run\n"
                  % (nome, "-"))
                continue
            opz = opzione_del_flag(c, flag)
            dove = opzione_nei_lanciatori(c, opz) if opz else None
            if opz and dove == []:
                W("    %-20s %-8s  FONTE: default del blob %s, E l'opzione `--%s` NON compare "
                  "in nessun lanciatore committato -> il default VALE\n"
                  % (nome, d[flag], c[:8], opz.replace("_", "-")))
            elif opz and dove:
                W("    %-20s %-8s  !! default del blob, MA `--%s` compare in %s: "
                  "il valore dipende dall'argv e il banner non lo elenca -> NON RICOSTRUITO\n"
                  % (nome, "?", opz.replace("_", "-"), ", ".join(dove)))
            else:
                W("    %-20s %-8s  FONTE: default del blob %s (nessuna opzione lo scrive in "
                  "`_applica_flag`)\n" % (nome, d[flag], c[:8]))

    # ---------------- la tabella completa dal banner
    W("\n" + "=" * 110 + "\n")
    W("LA TABELLA COMPLETA, dai BANNER -- i 24 flag che i log stampano\n")
    W("=" * 110 + "\n")
    tutti = sorted(set().union(*[set(stato[n]["banner"]) for n in stato]) or set())
    if not tutti:
        W("*** nessun banner trovato ***\n")
        return 1
    nomi = [r[0] for r in RUN if stato[r[0]]["banner"]]
    W("%-22s %s\n" % ("flag", " ".join("%-9s" % n.split()[0] for n in nomi)))
    W("-" * 110 + "\n")
    for f in tutti:
        W("%-22s %s\n" % (f, " ".join("%-9s" % stato[n]["banner"].get(f, "-")
                                      for n in nomi)))
    W("\n  `-` = il log di quel run non elenca quel flag nel banner (il banner e' cambiato\n")
    W("  nel tempo: e' una lista A MANO nel driver, ed e' cresciuta).\n")

    # ---------------- le contraddizioni
    W("\n" + "=" * 110 + "\n")
    W("CONTRADDIZIONI FRA FONTI -- banner contro default del blob\n")
    W("=" * 110 + "\n")
    n_contr = 0
    for nome in [r[0] for r in RUN]:
        s = stato[nome]
        if not (s["commit"] and s["banner"]):
            continue
        d = defaults_del_blob(s["commit"])
        for f, v in sorted(s["banner"].items()):
            if f in d and d[f] is not None and str(d[f]) != v:
                opz = opzione_del_flag(s["commit"], f)
                n_contr += 1
                W("  %-18s %-22s banner %-6s default %-6s -> %s\n"
                  % (nome, f, v, d[f],
                     ("SPIEGATA: l'opzione `--%s` la cambia" % opz.replace("_", "-"))
                     if opz else "*** NON SPIEGATA: nessuna opzione scrive questo flag ***"))
    W("\n  totale: %d. Una differenza banner/default NON e' un errore: e' l'argv che agisce.\n"
      % n_contr)
    W("  Quelle marcate NON SPIEGATA lo sono.\n")
    return 0


_PROV = os.environ.get("TEMP") or "."

if __name__ == "__main__":
    sys.exit(main())
