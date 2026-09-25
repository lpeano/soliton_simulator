# -*- coding: utf-8 -*-
"""**CON QUALE `argv` GIRAVA OGNI MISURA?** (mandato di Luca, 2026-09-25)

> **La configurazione di una misura non e' un ricordo: e' nel sorgente dello strumento.**

Dopo il `FAIL` di `A2` (`RAMPA-1`) si sa che **la configurazione CAMBIA il verdetto**: lo stesso
criterio dava `PASS` sui **default di modulo** (`CS_DINAMICO = False`, `cs` costante) e `FAIL`
sull'**argv del driver** (`cs` vivo, `cs_std/cs = 19 %`). **Quindi ogni misura va marcata con la
configurazione in cui e' stata presa**, e quelle **fuori** dalla configurazione del driver non
sono sbagliate: sono **misure di un altro sistema**, e vanno dette cosi'.

**COME LO DECIDE, e non da un `grep`** (`STANDARD 9`): **per AST**, cercando
* un `import _cli_flag` (o un uso del nome) -> **argv del DRIVER, catturata**;
* un lancio del **driver** per `subprocess` (`_scena_video.py`) -> **argv del DRIVER, vera**;
* le **assegnazioni di attributi MAIUSCOLI su un modulo importato** (`S.X = ...`) -> **default
  del sorgente PIU' flag impostati a mano**, e **li elenca tutti**.

**LA POPOLAZIONE NON LA SCELGO IO:** i sei strumenti che Luca nomina **piu'** ogni `.py` di
`csv/_test_fork/` e `csv/_seal_fork/` **committato oggi** (`git log --since`), cosi' quello che
avrei dimenticato entra da se'.

ASCII puro. Sola lettura.
"""
import ast
import io
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
DEST = os.path.join(RADICE, "doc", "CONFIGURAZIONE_misure_2026-09-25.md")
NL = chr(10)

# I SEI che Luca nomina, col nome della misura come lui la chiama
NOMINATI = [
    ("SCALE-TW pieno", "csv/_test_fork/_scale_tw2.py"),
    ("chi comprime d0", "csv/_test_fork/_chi_comprime_d0.py"),
    ("figli della mitosi", "csv/_test_fork/_figli_della_mitosi.py"),
    ("limite di accoppiamento", "csv/_test_fork/_limite_accoppiamento.py"),
    ("A13 relazionale", "csv/_test_fork/_a13_relazionale.py"),
    ("omega estremo", "csv/_test_fork/_dove_sta_omega.py"),
]
# LE DUE da cui dipende una decisione (priorita' dichiarata da Luca)
PRIORITA = {"csv/_test_fork/_chi_comprime_d0.py", "csv/_test_fork/_limite_accoppiamento.py"}

ALIAS = {"S", "S2", "_S", "SIM", "_S5", "sim"}


def committati_oggi():
    q = subprocess.run(["git", "log", "--since=midnight", "--name-only", "--format="],
                       cwd=RADICE, capture_output=True, text=True)
    fuori = []
    for r in (q.stdout or "").split(NL):
        r = r.strip().replace(chr(92), "/")
        if (r.startswith(("csv/_test_fork/", "csv/_seal_fork/")) and r.endswith(".py")
                and "/_tmp/" not in r and "_sim_vecchio" not in r and "._sim." not in r):
            fuori.append(r)
    return sorted(set(fuori))


def analizza(rel):
    """Restituisce (verdetto, flag_a_mano, note) LEGGENDO L'AST."""
    p = os.path.join(RADICE, rel)
    if not os.path.exists(p):
        return "ASSENTE", [], "il file non c'e' piu'"
    t = io.open(p, encoding="utf-8").read()
    try:
        arb = ast.parse(t)
    except SyntaxError as e:
        return "NON ANALIZZABILE", [], "SyntaxError: %s" % e
    usa_cli, lancia_driver, a_mano = False, False, []
    for nd in ast.walk(arb):
        if isinstance(nd, ast.Import):
            for al in nd.names:
                if al.name == "_cli_flag":
                    usa_cli = True
        if isinstance(nd, ast.ImportFrom) and (nd.module or "") == "_cli_flag":
            usa_cli = True
        if isinstance(nd, ast.Name) and nd.id == "_cli_flag":
            usa_cli = True
        if isinstance(nd, ast.Constant) and isinstance(nd.value, str):
            if "_scena_video.py" in nd.value:
                lancia_driver = True
        if isinstance(nd, ast.Assign):
            for tg in nd.targets:
                if (isinstance(tg, ast.Attribute) and isinstance(tg.value, ast.Name)
                        and tg.value.id in ALIAS and tg.attr.isupper()):
                    a_mano.append(tg.attr)
    # E LE ASSEGNAZIONI DENTRO I SORGENTI-FIGLIO (stringhe): un sigillo scrive il figlio come
    # TESTO, quindi le sue assegnazioni non sono nell'AST del padre. Si parsano le stringhe
    # lunghe che si lasciano parsare -- e se non si lasciano, SI DICE.
    non_parsate = 0
    for nd in ast.walk(arb):
        if (isinstance(nd, ast.Constant) and isinstance(nd.value, str)
                and len(nd.value) > 200 and ("import" in nd.value)):
            try:
                sub = ast.parse(nd.value)
            except SyntaxError:
                non_parsate += 1
                continue
            for s2 in ast.walk(sub):
                if isinstance(s2, ast.Name) and s2.id == "_cli_flag":
                    usa_cli = True
                if isinstance(s2, ast.Assign):
                    for tg in s2.targets:
                        if (isinstance(tg, ast.Attribute) and isinstance(tg.value, ast.Name)
                                and tg.value.id in ALIAS and tg.attr.isupper()):
                            a_mano.append(tg.attr)
    a_mano = sorted(set(a_mano))
    note = []
    if non_parsate:
        note.append("%d sorgenti-figlio non parsabili" % non_parsate)
    if usa_cli and lancia_driver:
        v = "DRIVER (argv catturata) + lancio del driver"
    elif usa_cli:
        v = "DRIVER (argv catturata via `_cli_flag`)"
    elif lancia_driver:
        v = "DRIVER (lanciato per subprocess)"
    elif a_mano:
        v = "DEFAULT DEL SORGENTE + flag a mano"
    else:
        v = "DEFAULT DEL SORGENTE (nessun flag toccato)"
    return v, a_mano, "; ".join(note)


R = []


def P(s=""):
    R.append(s)


oggi = committati_oggi()
nominati_rel = [r for _, r in NOMINATI]
tutti = nominati_rel + [r for r in oggi if r not in nominati_rel]

P("# CON QUALE `argv` GIRAVA OGNI MISURA — **generato**, non ricopiato")
P()
P("*(`csv/_config_delle_misure.py`. Mandato di Luca, 2026-09-25, punto 1. Sola lettura:")
P("il verdetto si legge **per AST** dal sorgente dello strumento, non da un `grep` e non da")
P("un ricordo. **La popolazione sono i sei strumenti nominati da Luca piu' ogni `.py` di")
P("`csv/_test_fork/` e `csv/_seal_fork/` committato oggi**, cosi' quello che avrei")
P("dimenticato entra da se'.)*")
P()
P("> ### PERCHE' QUESTA TABELLA ESISTE")
P("> Il `FAIL` di `A2` (`RAMPA-1`) ha dimostrato che **la configurazione cambia il")
P("> verdetto**: lo stesso criterio da' `PASS` sui **default di modulo** (`CS_DINAMICO =")
P("> False`, `cs` costante) e `FAIL` sull'**argv del driver** (`cs` vivo, `cs_std/cs = 19 %`).")
P("> **Una misura fuori dalla configurazione del driver non e' sbagliata: e' la misura di un")
P("> ALTRO SISTEMA**, e va marcata cosi'.")
P()
P("| misura | strumento | **configurazione** | flag impostati A MANO | priorita' |")
P("|---|---|---|---|---|")
nomi = dict((r, n) for n, r in NOMINATI)
conta = {}
for rel in tutti:
    v, am, note = analizza(rel)
    conta[v] = conta.get(v, 0) + 1
    nome = nomi.get(rel, "*(committato oggi)*")
    pr = "**DA RIFARE**" if rel in PRIORITA else ""
    P("| %s | `%s` | %s%s | %s | %s |"
      % (nome, rel.split("/")[-1], v, (" *(%s)*" % note if note else ""),
         (", ".join("`%s`" % x for x in am) if am else "—"), pr))
P()
P("## IL CONTO")
P()
P("```")
for k in sorted(conta):
    P("%-46s %d" % (k, conta[k]))
P("%-46s %d" % ("TOTALE", sum(conta.values())))
P("```")
P()
P("## COSA QUESTA TABELLA **NON** DICE")
P()
P("- **non dice che una misura sia sbagliata.** Dice **in quale sistema** e' stata presa.")
P("- **non e' un presidio** (`A9`): non impedisce a nessuno di scrivere domani un altro")
P("  strumento che imposta i flag a mano. Il presidio corrispondente e' `P2 FLAG VIVI`")
P("  del mandato sui presidi automatici, **ancora da cablare**.")
P("- **le assegnazioni dentro i sorgenti-figlio** (i sigilli scrivono il figlio come TESTO)")
P("  si leggono parsando quelle stringhe: quando una stringa non si lascia parsare **il")
P("  numero e' dichiarato nella riga**, invece di essere contata come «nessuna assegnazione».")

T = NL.join(R) + NL
io.open(DEST, "w", encoding="utf-8", newline=NL).write(T)
print(T)
