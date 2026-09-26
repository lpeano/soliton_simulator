r"""**COLLAUDO DELLE ISTRUZIONI D'USO** — la sezione dell'INDICE DEI DIFETTI di `CLAUDE.md` basta, da sola?

**Punto 5 del mandato (Luca, 2026-09-26):** *«una sessione che legge SOLO questa sezione deve saper
aggiungere un difetto finto (poi rimosso) e farlo passare dal hook»*.

## COME LO PROVO, e perche' cosi'

**Non uso cio' che so: uso cio' che la sezione DICE.** Lo script

1. **estrae la sezione dell'INDICE DEI DIFETTI** da `CLAUDE.md` (cercata PER NOME, non per numero) e **legge da li'** — le **colonne**, i **vocabolari**, i
   **comandi** *(ogni `python csv/...` fra apici)*, i **nomi dei file**;
2. **costruisce la riga** del difetto finto **dalle colonne dichiarate nella sezione**, non da una
   lista scritta qui;
3. prova **i due versi**: solo in `STATO_RUN` → **deve essere RIFIUTATO**; **con la riga
   nell'indice** → **deve PASSARE**;
4. **rigenera le viste** coi comandi estratti dalla sezione, e **rilancia il validatore**;
5. **ripristina tutto** e verifica per **sha1** che i file siano tornati identici.

> **Se la sezione non basta, questo collaudo FALLISCE** — ed e' l'unico modo di dire «abbastanza»
> senza fidarsi di chi l'ha scritta *(`A9`)*.

ASCII puro nell'output.
"""
# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Collauda una sezione di documentazione.
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
DEST = os.path.join(RADICE, "doc", "COLLAUDO_istruzioni_indice.txt")
NL = chr(10)
TAB = chr(9)
R = []


def P(s=""):
    R.append(s)
    print(s)


def sha(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()[:12]


# ================================================================== 1. LEGGO LA SEZIONE
t = io.open(os.path.join(RADICE, "CLAUDE.md"), encoding="utf-8", newline="").read()
# ⚠ L'ANCORA E' IL NOME, NON IL NUMERO (par.2 di `CLAUDE.md`: si cerca per nome, mai per riga).
#   Col riordino del 2026-09-26 la sezione e' passata da `11.` a `9.`: un'ancora sul NUMERO
#   avrebbe fatto **schiantare** il collaudo, che e' il modo piu' facile di non accorgersene.
#   La sezione finisce al titolo di secondo livello successivo, o a fine file.
m = re.search(r"^## \d+[\-a-z]*\. L'INDICE DEI DIFETTI.*?$(.*?)(?=^## |\Z)", t, re.S | re.M)
assert m, "la sezione dell'INDICE DEI DIFETTI non c'e': il collaudo non ha niente da provare"
SEZ = m.group(1)

_col = re.search(r"\*\*colonne:\*\*(.+)", SEZ)
COLONNE = [x.strip(" `") for x in _col.group(1).split("·")] if _col else []
_fonte = re.search(r"LA FONTE E' `([^`]+)`", SEZ)
FONTE = _fonte.group(1) if _fonte else ""
COMANDI = re.findall(r"`(python csv/[^`]+)`", SEZ)
_stati = re.search(r"\*\*`stato`:\*\*(.+)", SEZ)
STATI = [x.strip(" `") for x in _stati.group(1).split("|")] if _stati else []
_tipi = re.search(r"\*\*`tipo`:\*\*(.+?)· \*\*`famiglia", SEZ)
TIPI = [x.strip(" `") for x in _tipi.group(1).split("|")] if _tipi else []
_doc = re.findall(r"`(doc/[A-Za-z0-9_.\-]+)`", SEZ)

P("=" * 100)
P("COLLAUDO DELLE ISTRUZIONI D'USO (sezione dell'INDICE DEI DIFETTI di CLAUDE.md)   (2026-09-26)")
P("=" * 100)
P()
P("  LETTO DALLA SEZIONE, non da me:")
P("    la FONTE ............ %s" % (FONTE or "*** non dichiarata ***"))
P("    colonne ............. %d   %s" % (len(COLONNE), ", ".join(COLONNE)))
P("    stati ammessi ....... %s" % ", ".join(STATI))
P("    tipi ammessi ........ %d" % len(TIPI))
P("    comandi ............. %s" % " | ".join(COMANDI))
P("    documenti citati .... %s" % ", ".join(sorted(set(_doc))))
P()
esiti = []
ok_l = bool(FONTE) and len(COLONNE) == 13 and len(STATI) == 5 and len(COMANDI) >= 4
esiti.append(ok_l)
P("  K0 la sezione dichiara fonte, 13 colonne, 5 stati e i comandi -> %s"
  % ("OK" if ok_l else "*** INSUFFICIENTE: la sezione non basta ***"))

IX = os.path.join(RADICE, FONTE)
SR = os.path.join(RADICE, "doc", "STATO_RUN.md")
VISTE = [os.path.join(RADICE, x) for x in
         ("doc/LISTA_CHIUSA.md", "doc/SMISTAMENTO_run_base.md", "doc/PUNTO_DELLA_SITUAZIONE.md")]
_st = subprocess.run(["git", "diff", "--cached", "--name-only"], cwd=RADICE,
                     capture_output=True, text=True, encoding="utf-8", errors="replace")
if (_st.stdout or "").strip():
    P()
    P("  *** NON ESEGUITO: c'erano modifiche in STAGE, e non le tocco. Lo dichiaro.")
    io.open(DEST, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    sys.exit(2)

# ================================================================== 2. IL DIFETTO FINTO
ID = "QZ901"
_c, _r = None, None
_prima = {p: sha(p) for p in [IX, SR] + VISTE}
for p in [IX, SR] + VISTE:
    shutil.copy(p, p + ".bak")
_msg = os.path.join(RADICE, "doc", "_collaudo_istr_msg.tmp")
io.open(_msg, "w", encoding="utf-8", newline=NL).write("collaudo delle istruzioni" + NL)
try:
    # (a) SOLO in STATO_RUN -- la sezione dice che deve essere RIFIUTATO
    with io.open(SR, "a", encoding="utf-8", newline=NL) as f:
        f.write(NL + "| **%s** | difetto FINTO del collaudo delle istruzioni | — | `APERTO` |"
                % ID + NL)
    subprocess.run(["git", "add", "--", "doc/STATO_RUN.md"], cwd=RADICE, capture_output=True)
    a = subprocess.run([sys.executable, os.path.join(RADICE, "csv", "_presidio_indice.py"),
                        "--commit-msg", _msg], cwd=RADICE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    okA = a.returncode != 0
    # (b) con la RIGA nell'indice, costruita DALLE COLONNE della sezione
    righe = io.open(IX, encoding="utf-8", newline="").read().split(NL)
    intest = [x.strip() for x in righe[0].split(TAB)]
    assert intest == COLONNE, ("le colonne dell'indice non sono quelle della sezione:%s  %s%s  %s"
                               % (NL, intest, NL, COLONNE))
    campo = {"id": ID, "titolo_breve": "difetto FINTO del collaudo delle istruzioni",
             "fonte_principale": "doc/STATO_RUN.md::difetto FINTO",
             "stato": STATI[0], "blocca_run_base": "DA-DECIDERE",
             "tipo": TIPI[0] if TIPI else "difetto", "famiglia": "?",
             "avanzamento": "(senza marcatore)"}
    nuova = TAB.join([campo.get(c, "") for c in COLONNE])
    corpo = [x for x in righe[1:] if x.strip()]
    io.open(IX, "w", encoding="utf-8", newline=NL).write(
        TAB.join(COLONNE) + NL + NL.join(corpo + [nuova]) + NL)
    subprocess.run(["git", "add", "--", FONTE, "doc/STATO_RUN.md"], cwd=RADICE,
                   capture_output=True)
    b = subprocess.run([sys.executable, os.path.join(RADICE, "csv", "_presidio_indice.py"),
                        "--commit-msg", _msg], cwd=RADICE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    okB = b.returncode == 0
    # (c) il VALIDATORE e le VISTE, coi comandi ESTRATTI dalla sezione
    esiti_cmd = []
    for cmd in COMANDI:
        q = subprocess.run([sys.executable] + cmd.split()[1:], cwd=RADICE, capture_output=True,
                           text=True, encoding="utf-8", errors="replace")
        esiti_cmd.append((cmd, q.returncode))
    okC = all(rc == 0 for _c2, rc in esiti_cmd)
    # (d) il difetto finto compare in una vista?
    _sm = io.open(os.path.join(RADICE, "doc", "SMISTAMENTO_run_base.md"),
                  encoding="utf-8", errors="replace").read()
    okD = ID in _sm
finally:
    subprocess.run(["git", "reset", "-q", "--", FONTE, "doc/STATO_RUN.md"], cwd=RADICE,
                   capture_output=True)
    for p in [IX, SR] + VISTE:
        shutil.move(p + ".bak", p)
    if os.path.exists(_msg):
        os.remove(_msg)

_dopo = {p: sha(p) for p in [IX, SR] + VISTE}
okE = all(_prima[p] == _dopo[p] for p in _prima)
P()
P("  IL DIFETTO FINTO `%s`, seguendo SOLO la sezione:" % ID)
P("    K1 DEVE FALLIRE  solo in `STATO_RUN` ............. uscita %d   %s"
  % (a.returncode, "OK" if okA else "*** PASSA, e non deve ***"))
P("    K2 DEVE PASSARE  con la RIGA nell'indice ......... uscita %d   %s"
  % (b.returncode, "OK" if okB else "*** RIFIUTATO: la sezione non basta ***"))
P("    K3 i comandi della sezione girano tutti:")
for cmd, rc in esiti_cmd:
    P("         %-44s uscita %d" % (cmd, rc))
P("       -> %s" % ("OK" if okC else "*** un comando dichiarato NON gira ***"))
P("    K4 il difetto finto COMPARE nello smistamento .... %s   %s"
  % (okD, "OK" if okD else "*** la vista non lo prende ***"))
P("    K5 tutti i file sono tornati identici (sha1) ..... %s   %s"
  % (okE, "OK" if okE else "*** QUALCOSA E' RIMASTO SPORCO ***"))
esiti += [okA, okB, okC, okD, okE]
P()
tutto = all(esiti)
P("=" * 100)
P("ESITO: %s" % ("%d/%d PASS -- **LA SEZIONE DELL'INDICE BASTA DA SOLA**" % (len(esiti), len(esiti))
               if tutto else "FAIL -- la sezione NON basta, e va corretta"))
P("=" * 100)
P()
P("COSA QUESTO COLLAUDO *NON* DICE:")
P("  - **non dice che la sezione sia CHIARA per un umano**: dice che **contiene i dati e i comandi**")
P("    che servono a fare il lavoro, e che quei comandi girano.")
P("  - **la riga finta e' costruita dalle COLONNE della sezione**, e il collaudo si ferma se")
P("    l'intestazione dell'indice **non coincide** con quella dichiarata: se qualcuno cambia lo")
P("    schema e si dimentica la sezione, **questo collaudo lo denuncia**.")

io.open(DEST, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
sys.exit(0 if tutto else 1)
