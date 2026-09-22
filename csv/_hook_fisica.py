# -*- coding: utf-8 -*-
"""IMPEDIMENTO `REG-R` -- **nessuna legge cambia senza che cambi la SUA scheda.**

Decisione di Luca, 2026-09-22, **nella forma giusta**:

    Un commit che modifica una LEGGE del simulatore deve modificare LA SCHEDA DI QUELLA LEGGE.
    Se la scheda NON ESISTE, prima si crea la scheda.
    I commit che non toccano la fisica usano l'eccezione  [SENZA-FISICA: <motivo>].

!! PERCHE' QUESTA FORMA E NON "tocca il registro": un hook che chiedesse soltanto di toccare
  `doc/REGISTRO_FISICA.md` sarebbe soddisfatto da UNA RIGA QUALSIASI in fondo al file. Questo
  chiede che **la diff del registro cada DENTRO la sezione della legge toccata**. E' la
  differenza fra un presidio e una formalita' (`A9`).

COME SA QUALE SCHEDA. Ogni scheda porta un marcatore leggibile da codice:

    <!-- SCHEDA nome=freno-scala-min funzioni=_smorza,_smp_chiudi flag=SCALA_MIN,SCALA_MIN_PASSO -->

La sezione di una scheda va dal suo marcatore al marcatore successivo (o a fine file).

!! FRAGILITA' DICHIARATA: un ESEMPIO di marcatore scritto dentro la documentazione
  verrebbe letto come un marcatore VERO. Oggi non succede perche' l'esempio in
  `REGISTRO_FISICA.md` usa i puntini di sospensione, che non matchano `[\w-]+` --
  cioe' PER FORTUNA, non per progetto. Se un giorno l'esempio diventasse realistico,
  spezzerebbe la mappa delle sezioni. VERIFICATO OGGI: il hook vede 5 schede su 5.

COME SA COSA E' CAMBIATO. Dalla diff **in cache** di `soliton_simulator.py`:
  * le righe toccate -> la FUNZIONE che le contiene, per **nome**, via AST della versione
    **in cache** *(par.0: i nomi non si spostano, le righe si')*;
  * le righe toccate a livello di MODULO -> il **flag** assegnato su quella riga.

!! IL LIMITE, DICHIARATO INVECE DI ESSERE NASCOSTO: **questo hook non distingue una modifica di
  LEGGE da una modifica di COMMENTO.** Distinguerle richiederebbe un confronto di AST fra le due
  versioni, e un commento che descrive una legge **e' parte della legge** (par.0: i commenti
  stale sono un difetto documentato di questo repo). **Quindi ogni tocco dentro una funzione o
  a un flag conta**, e le modifiche davvero non fisiche passano per `[SENZA-FISICA: ...]`.
  **E' piu' severo del necessario, e va detto.**

ASCII PURO.
"""
import ast
import io
import os
import re
import subprocess
import sys

SIM = "soliton_simulator.py"
REGISTRO = "doc/REGISTRO_FISICA.md"
MARCATORE = re.compile(
    r"<!--\s*SCHEDA\s+nome=([\w\-]+)\s+funzioni=([^\s]*)\s+flag=([^\s]*)\s*-->")
FUGA = re.compile(r"\[SENZA-FISICA:\s*(.+?)\]", re.I)


def _git(*a):
    return subprocess.check_output(["git"] + list(a), text=True, errors="replace")


def righe_toccate(diff):
    """Le righe del file NUOVO toccate da una diff `-U0`. Solo aggiunte e contesto zero.

    !! Una RIMOZIONE pura non ha righe nuove: si registra la riga a cui il taglio e' ancorato,
      altrimenti cancellare una legge intera non risulterebbe come 'toccata'.
    """
    out = set()
    for m in re.finditer(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", diff, re.M):
        ini = int(m.group(3))
        n = int(m.group(4)) if m.group(4) is not None else 1
        if n == 0:                      # rimozione pura: ancora la riga precedente
            out.add(max(1, ini))
        for k in range(n):
            out.add(ini + k)
    return out


def mappa_righe(sorgente):
    """riga -> (nome funzione piu' INTERNA, nome del flag assegnato a livello di modulo)."""
    albero = ast.parse(sorgente)
    di_chi = {}
    for nodo in ast.walk(albero):
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for x in ast.walk(nodo):
                ln = getattr(x, "lineno", None)
                if ln is None:
                    continue
                fine = getattr(x, "end_lineno", ln) or ln
                for r in range(ln, fine + 1):
                    pre = di_chi.get(r)
                    if pre is None or nodo.lineno > pre[1]:
                        di_chi[r] = (nodo.name, nodo.lineno)
    flag = {}
    for nodo in albero.body:            # SOLO livello di modulo
        if isinstance(nodo, ast.Assign):
            for t in nodo.targets:
                if isinstance(t, ast.Name) and t.id.isupper():
                    fine = getattr(nodo, "end_lineno", nodo.lineno) or nodo.lineno
                    for r in range(nodo.lineno, fine + 1):
                        flag[r] = t.id
    return dict((r, v[0]) for r, v in di_chi.items()), flag


def schede(testo):
    """nome -> (riga_inizio, riga_fine, set funzioni, set flag). Righe 1-based, estremi inclusi."""
    righe = testo.splitlines()
    trovate = []
    for i, r in enumerate(righe, 1):
        m = MARCATORE.search(r)
        if m:
            fu = set(x for x in m.group(2).split(",") if x)
            fl = set(x for x in m.group(3).split(",") if x)
            trovate.append([m.group(1), i, None, fu, fl])
    for k, v in enumerate(trovate):
        v[2] = (trovate[k + 1][1] - 1) if k + 1 < len(trovate) else len(righe)
    return dict((v[0], (v[1], v[2], v[3], v[4])) for v in trovate)


def controlla(staged, msg, leggi_git=True, _finti=None):
    """Ritorna `(codice, testo)`. `0` = passa.

    `_finti` serve al COLLAUDO: `dict` con `sim_diff`, `sim_testo`, `reg_diff`, `reg_testo`.
    """
    if SIM not in staged:
        return 0, ""
    if _finti is not None:
        sim_diff = _finti.get("sim_diff", "")
        sim_testo = _finti.get("sim_testo", "")
        reg_diff = _finti.get("reg_diff", "")
        reg_testo = _finti.get("reg_testo", "")
    elif leggi_git:
        sim_diff = _git("diff", "--cached", "-U0", "--", SIM)
        sim_testo = _git("show", ":" + SIM)
        reg_diff = _git("diff", "--cached", "-U0", "--", REGISTRO) if REGISTRO in staged else ""
        try:
            reg_testo = _git("show", ":" + REGISTRO)
        except subprocess.CalledProcessError:
            reg_testo = io.open(REGISTRO, encoding="utf-8").read() \
                if os.path.exists(REGISTRO) else ""
    else:
        return 0, ""

    tocc = righe_toccate(sim_diff)
    if not tocc:
        return 0, ""
    per_riga, per_flag = mappa_righe(sim_testo)
    colpite = set()
    for r in tocc:
        if r in per_riga:
            colpite.add(("funzione", per_riga[r]))
        elif r in per_flag:
            colpite.add(("flag", per_flag[r]))
    if not colpite:
        return 0, ""                    # nessuna funzione e nessun flag: non e' una legge

    sc = schede(reg_testo)
    reg_tocc = righe_toccate(reg_diff)
    senza_scheda, scheda_non_toccata = [], []
    for tipo, nome in sorted(colpite):
        trovata = None
        for s, (a, b, fu, fl) in sc.items():
            if (tipo == "funzione" and nome in fu) or (tipo == "flag" and nome in fl):
                trovata = (s, a, b)
                break
        if trovata is None:
            senza_scheda.append((tipo, nome))
            continue
        s, a, b = trovata
        if not any(a <= r <= b for r in reg_tocc):
            scheda_non_toccata.append((tipo, nome, s))

    if not senza_scheda and not scheda_non_toccata:
        return 0, ""

    m = FUGA.search(msg or "")
    if m:
        return 0, "[REG-R] eccezione DICHIARATA: %s\n" % m.group(1).strip()

    t = ["\n[REG-R] *** COMMIT RIFIUTATO: una LEGGE cambia e la sua SCHEDA no. ***\n\n"]
    if senza_scheda:
        t.append("  QUESTE LEGGI NON HANNO UNA SCHEDA. **Prima si crea la scheda:**\n")
        for tipo, nome in senza_scheda:
            t.append("    %-9s %s\n" % (tipo, nome))
        t.append("\n  Una scheda si apre in `%s` con il suo marcatore:\n" % REGISTRO)
        t.append("    <!-- SCHEDA nome=<slug> funzioni=<a,b,c> flag=<X,Y> -->\n")
    if scheda_non_toccata:
        t.append("\n  QUESTE HANNO UNA SCHEDA, e il commit NON la tocca:\n")
        for tipo, nome, s in scheda_non_toccata:
            t.append("    %-9s %-28s -> scheda `%s`\n" % (tipo, nome, s))
        t.append("\n  !! NON BASTA toccare il registro da qualche parte: la modifica deve cadere\n"
                 "    DENTRO la sezione di QUELLA scheda. Un hook soddisfatto da una riga\n"
                 "    qualsiasi in fondo al file sarebbe una formalita', non un presidio.\n")
    t.append(
        "\n  PERCHE': una cura deve NASCERE DALLA SCHEDA -- dalla formula, dalle dimensioni,\n"
        "  da cosa legge e cosa scrive, dai limiti classificati con `A11`. Senza scheda si\n"
        "  cura alla cieca, ed e' il modo in cui sono nati `D01`-`D33`.\n\n"
        "  CHE FARE:\n"
        "    1. aggiorna la scheda della legge che stai cambiando, e mettila nel commit; oppure\n"
        "    2. se il commit NON tocca la fisica, dichiaralo nel messaggio:\n"
        "         [SENZA-FISICA: <motivo>]\n\n")
    return 1, "".join(t)


# ------------------------------------------------------------------ COLLAUDO (`P1-sexies`)
_SIM = '''FLAG_A = True
FLAG_SENZA = False


def _smorza(x):
    y = x + 1
    return y


def altra_legge(x):
    return x * 2
'''
_REG = """# REGISTRO
<!-- SCHEDA nome=freno funzioni=_smorza flag=FLAG_A -->
# IL FRENO
testo del freno
ancora testo
<!-- SCHEDA nome=altra funzioni=zzz flag=FLAG_B -->
# ALTRA
testo altro
"""


def _diff(righe):
    """Una diff `-U0` finta che dichiara toccate le righe indicate."""
    return "".join("@@ -%d,1 +%d,1 @@\n" % (r, r) for r in righe)


def collaudo(W):
    e = []
    W("COLLAUDO `REG-R` su casi SINTETICI a risposta nota (`P1-sexies`)\n" + "-" * 94 + "\n")

    def prova(nome, righe_sim, righe_reg, msg, atteso, spiega):
        c, t = controlla([SIM, REGISTRO] if righe_reg else [SIM], msg, _finti=dict(
            sim_diff=_diff(righe_sim), sim_testo=_SIM,
            reg_diff=_diff(righe_reg), reg_testo=_REG))
        ok = (c == atteso)
        e.append(ok)
        W("%-4s %s -> %s  %s\n"
          % (nome, spiega, "RIFIUTA" if c else "passa", "OK" if ok else "*** NO ***"))
        return t

    prova("K1", [6], [4], "", 0,
          "tocco `_smorza` (riga 6) E la scheda `freno` (riga 4)")
    t2 = prova("K2", [6], [], "", 1,
               "**DEVE FALLIRE**: tocco `_smorza` e NON tocco il registro")
    prova("K3", [6], [8], "", 1,
          "**DEVE FALLIRE**: tocco `_smorza` e il registro, ma nella scheda SBAGLIATA")
    prova("K4", [11], [4], "", 1,
          "**DEVE FALLIRE**: tocco `altra_legge`, che NON HA una scheda")
    prova("K5", [6], [], "[SENZA-FISICA: solo un commento]", 0,
          "l'eccezione DICHIARATA fa passare")
    prova("K6", [1], [4], "", 0,
          "tocco `FLAG_A` (riga 1), che la scheda `freno` copre")
    prova("K7", [2], [4], "", 1,
          "**DEVE FALLIRE**: tocco `FLAG_SENZA`, che nessuna scheda copre")
    prova("K8", [3], [], "", 0,
          "tocco una riga VUOTA fuori da ogni funzione e flag: non e' una legge")

    # !! un rifiuto che non dice COSA toccare costringe a indovinare, e un presidio che si
    #   aggira per stanchezza non e' un presidio. Si verifica che il testo NOMINI la scheda
    #   e la funzione, non solo che rifiuti.
    ok9 = ("freno" in (t2 or "")) and ("_smorza" in (t2 or ""))
    e.append(ok9)
    W("K9   il rifiuto NOMINA la scheda (`freno`) E la funzione (`_smorza`) -> %s\n"
      % ("OK" if ok9 else "*** NO: %r ***" % (t2 or "")[:120]))
    ok = all(e)
    W("-" * 94 + "\n  -> %s\n" % ("i criteri PASSANO" if ok else "*** NON PASSANO ***"))
    return ok


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if "--collaudo" in sys.argv:
        sys.exit(0 if collaudo(sys.stdout.write) else 1)
    print(__doc__)
