# -*- coding: utf-8 -*-
"""PARTE C + §S -- IL CENSIMENTO DELLA FAMIGLIA "4pi DICHIARATO, 2pi USATO", con le classi T/L/E.

Mandato di Luca, 2026-09-22. **SOLA LETTURA: nessuna cura, nessuna proposta in codice.**

LA REGOLA DI FONDO, che questo strumento applica:
    Lo spinore ha periodo 4pi; tutto cio' che si OSSERVA da lui ha periodo 2pi;
    un ACCUMULO non ha periodo.
  `np.angle`, `|psi|^2`, `exp(i phi)`, `cos`, `sin` hanno **periodo 2pi**: NON vedono il segno
  dello spinore. Un avvolgimento su 4pi applicato a una grandezza a periodo 2pi **non avvolge
  niente**; un "+2pi = antifase" letto attraverso `exp(i phi)` **e' un'identita'**.

COSA CERCA (AST, non grep):
  `W4`  un avvolgimento `% (4 pi)` -- e SE il valore avvolto viene da una OSSERVABILE
  `W2`  un avvolgimento `% (2 pi)`
  `OSS` una funzione a periodo 2pi applicata a una grandezza che vive su 4pi
        (`exp(1j*phi)`, `cos(phi_i - phi_j)`, `np.angle(...)`)
  `A2P` un `+ 2*np.pi` usato come "antifase" / "opposto"

LE CLASSI (§S), e la distinzione e' il punto:
  `T` AVVOLGIMENTO DI UNA FASE (topologia). **NON si leviga.** Il salto da 2pi a 0 e' un
      artefatto della COORDINATA, non una discontinuita' fisica: levigarlo inventerebbe valori
      che non esistono. La cura e' usare IL PERIODO GIUSTO.
  `L` SOGLIA / TETTO / CLIP di una LEGGE. **SI LEVIGA**, coi tre obblighi del corollario 7 di
      `A11`, e **la larghezza DERIVATA**: una levigatura con larghezza scelta a mano e' un
      parametro nuovo (`A1`), **peggio dello spigolo**.
  `E` EVENTO DISCRETO. L'evento resta discreto (il grafo e' discreto), **ma la sua PROBABILITA'
      o il suo TASSO dev'essere liscio** nella grandezza che lo governa.

⚠ IL CASO NASCOSTO che il collaudo deve prendere: **un `np.angle` messo in una VARIABILE e
  avvolto PIU' AVANTI, in un'altra riga.** Una ricerca riga-per-riga non lo vede; qui si
  propaga il "periodo" delle variabili dentro la funzione.

⚠ CIO' CHE QUESTO STRUMENTO NON FA, dichiarato: **non decide**. Ogni punto esce con la sua
  classe e con `attivo/dormiente`; **la proposta e' un campo a parte, e per i punti che non ho
  capito dice `DA DECIDERE`.**
ASCII PURO.
"""
import ast
import hashlib
import io
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SORGENTE = os.path.join(RADICE, "soliton_simulator.py")
OUT = os.path.join(_QUI, "_diag_D", "CENSIMENTO_FASI.md")

# Grandezze che VIVONO su 4pi (dichiarato dal codice: avvolte con `% (4 pi)` o dominio doppio).
SU_4PI = {"phi", "phi0", "fm", "anti"}
# Funzioni a periodo 2pi: qualunque cosa ci entri, la doppia copertura NON si vede.
PERIODO_2PI = {"angle", "exp", "cos", "sin", "cos2", "sin2"}


def flag_di_riga(albero, righe_testo):
    """Il flag che governa una riga: il piu' interno `if <FLAG>` che la contiene."""
    fuori = {}
    for nodo in ast.walk(albero):
        if not isinstance(nodo, ast.If):
            continue
        nomi = [x.id for x in ast.walk(nodo.test)
                if isinstance(x, ast.Name) and x.id.isupper()]
        if not nomi:
            continue
        a = nodo.lineno
        b = getattr(nodo, "end_lineno", a) or a
        for r in range(a, b + 1):
            pre = fuori.get(r)
            if pre is None or a > pre[1]:
                fuori[r] = (",".join(sorted(set(nomi))), a)
    return dict((r, v[0]) for r, v in fuori.items())


def default_flag(testo, nome):
    m = re.search(r"^%s\s*=\s*(True|False)\b" % re.escape(nome), testo, re.M)
    return m.group(1) if m else None


def e_due_pi(nodo):
    """Il nodo e' `2*np.pi` (o `np.pi*2`)?"""
    if not isinstance(nodo, ast.BinOp) or not isinstance(nodo.op, ast.Mult):
        return False
    for x, y in ((nodo.left, nodo.right), (nodo.right, nodo.left)):
        if isinstance(x, ast.Constant) and x.value == 2 and _e_pi(y):
            return True
    return False


def e_quattro_pi(nodo):
    if not isinstance(nodo, ast.BinOp) or not isinstance(nodo.op, ast.Mult):
        return False
    for x, y in ((nodo.left, nodo.right), (nodo.right, nodo.left)):
        if isinstance(x, ast.Constant) and x.value in (4, 4.0) and _e_pi(y):
            return True
    return False


def _e_pi(n):
    return isinstance(n, ast.Attribute) and n.attr == "pi"


def periodo_delle_variabili(fn):
    """Propaga il PERIODO delle variabili dentro una funzione.

    ⚠ E' IL CASO NASCOSTO: `a = np.angle(x) - np.angle(y)` in una riga, e l'avvolgimento
      DUE RIGHE DOPO. Una ricerca riga-per-riga non lo vedrebbe.
    """
    per = {}
    for nodo in ast.walk(fn):
        if not isinstance(nodo, ast.Assign) or len(nodo.targets) != 1:
            continue
        t = nodo.targets[0]
        if not isinstance(t, ast.Name):
            continue
        fonti = set()
        for x in ast.walk(nodo.value):
            if isinstance(x, ast.Call) and isinstance(x.func, ast.Attribute):
                if x.func.attr in PERIODO_2PI:
                    fonti.add("2pi")
            elif isinstance(x, ast.Attribute) and x.attr in SU_4PI:
                fonti.add("4pi")
            elif isinstance(x, ast.Name):
                if x.id in per:
                    fonti.add(per[x.id])
                elif x.id in SU_4PI:
                    fonti.add("4pi")
        if "2pi" in fonti:
            per[t.id] = "2pi"
        elif "4pi" in fonti:
            per[t.id] = "4pi"
    return per


def censisci(testo):
    albero = ast.parse(testo)
    righe = testo.splitlines()
    gov = flag_di_riga(albero, righe)
    punti = []

    for fn in ast.walk(albero):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        per = periodo_delle_variabili(fn)
        for nodo in ast.walk(fn):
            r = getattr(nodo, "lineno", None)
            if r is None:
                continue
            src = righe[r - 1].strip()
            # --- avvolgimenti
            if isinstance(nodo, ast.BinOp) and isinstance(nodo.op, ast.Mod):
                quattro = e_quattro_pi(nodo.right)
                due = e_due_pi(nodo.right)
                if not (quattro or due):
                    continue
                # da dove viene il valore avvolto?
                fonte = "?"
                for x in ast.walk(nodo.left):
                    if isinstance(x, ast.Call) and isinstance(x.func, ast.Attribute) \
                            and x.func.attr in PERIODO_2PI:
                        fonte = "OSSERVABILE"; break
                    if isinstance(x, ast.Name) and per.get(x.id) == "2pi":
                        fonte = "OSSERVABILE (via `%s`)" % x.id; break
                    if isinstance(x, ast.Attribute) and x.attr in SU_4PI:
                        fonte = "grandezza su 4pi"
                    if isinstance(x, ast.Name) and per.get(x.id) == "4pi":
                        fonte = "grandezza su 4pi (via `%s`)" % x.id
                tipo = "W4" if quattro else "W2"
                grave = quattro and fonte.startswith("OSSERVABILE")
                punti.append(dict(riga=r, fn=fn.name, tipo=tipo, classe="T", fonte=fonte,
                                  grave=grave, src=src, flag=gov.get(r, "—")))
            # --- `+ 2*pi` come antifase
            elif isinstance(nodo, ast.BinOp) and isinstance(nodo.op, ast.Add) \
                    and e_due_pi(nodo.right):
                punti.append(dict(riga=r, fn=fn.name, tipo="A2P", classe="T",
                                  fonte="`+2pi` su una fase", grave=True, src=src,
                                  flag=gov.get(r, "—")))
            # --- funzione a periodo 2pi applicata a una grandezza su 4pi
            elif isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Attribute) \
                    and nodo.func.attr in PERIODO_2PI:
                su4 = None
                for x in ast.walk(nodo):
                    if isinstance(x, ast.Attribute) and x.attr in SU_4PI:
                        su4 = x.attr
                    elif isinstance(x, ast.Name) and per.get(x.id) == "4pi":
                        su4 = x.id
                if su4:
                    punti.append(dict(riga=r, fn=fn.name, tipo="OSS", classe="T",
                                      fonte="`%s` (4pi) dentro `%s` (periodo 2pi)"
                                            % (su4, nodo.func.attr),
                                      grave=True, src=src, flag=gov.get(r, "—")))
    # de-duplica per (riga, tipo)
    visti, out = set(), []
    for p in punti:
        k = (p["riga"], p["tipo"])
        if k in visti:
            continue
        visti.add(k)
        out.append(p)
    return sorted(out, key=lambda p: p["riga"])


def collaudo(W):
    """`P1-sexies`, col CASO NASCOSTO e col caso che DEVE fallire."""
    W("COLLAUDO (`P1-sexies`), PRIMA di censire\n" + "-" * 96 + "\n")
    e = []
    nascosto = ("import numpy as np\n"
                "class R(object):\n"
                "    def f(self):\n"
                "        a = np.angle(self.psi) - np.angle(self.psi_prec)\n"
                "        b = a * 1.0\n"
                "        s = ((b + 2 * np.pi) % (4 * np.pi) - 2 * np.pi)\n"
                "        return s\n")
    p = censisci(nascosto)
    g = [x for x in p if x["tipo"] == "W4"]
    ok1 = len(g) == 1 and g[0]["grave"] and "via" in g[0]["fonte"]
    W("K1 IL CASO NASCOSTO: `np.angle` in una VARIABILE, passata per UN'ALTRA, e avvolta\n")
    W("     TRE righe dopo -> %s  (%s)\n"
      % ("OK: il periodo si propaga" if ok1 else "*** NON lo vede ***",
         g[0]["fonte"] if g else "nessun punto"))
    e.append(ok1)

    innocuo = ("import numpy as np\n"
               "class R(object):\n"
               "    def f(self):\n"
               "        return (self.phi + 0.1) % (4 * np.pi)\n")
    p2 = censisci(innocuo)
    g2 = [x for x in p2 if x["tipo"] == "W4"]
    ok2 = len(g2) == 1 and not g2[0]["grave"]
    W("K2 IL CASO CHE NON DEVE ALLARMARE: `phi` (che VIVE su 4pi) avvolta su 4pi ->\n")
    W("     segnalata ma NON grave -> %s  (grave=%s)\n"
      % ("OK" if ok2 else "*** allarme falso ***", g2[0]["grave"] if g2 else "?"))
    e.append(ok2)

    osserv = ("import numpy as np\n"
              "class R(object):\n"
              "    def f(self):\n"
              "        return np.exp(1j * self.phi)\n")
    p3 = censisci(osserv)
    ok3 = any(x["tipo"] == "OSS" and x["grave"] for x in p3)
    W("K3 `phi` (4pi) dentro `exp` (periodo 2pi) -> segnalato GRAVE -> %s\n"
      % ("OK" if ok3 else "*** NO ***"))
    e.append(ok3)

    a2p = ("import numpy as np\n"
           "class R(object):\n"
           "    def f(self):\n"
           "        return (self.fm + 2 * np.pi) % (4 * np.pi)\n")
    p4 = censisci(a2p)
    ok4 = any(x["tipo"] == "A2P" for x in p4)
    W("K4 `+2pi` usato come ANTIFASE -> segnalato -> %s\n" % ("OK" if ok4 else "*** NO ***"))
    e.append(ok4)

    pulito = ("import numpy as np\n"
              "class R(object):\n"
              "    def f(self):\n"
              "        a = np.angle(self.psi) - np.angle(self.psi_prec)\n"
              "        return ((a + np.pi) % (2 * np.pi) - np.pi)\n")
    p5 = censisci(pulito)
    ok5 = not any(x["grave"] for x in p5)
    W("K5 IL CASO CHE DEVE DARE ZERO ALLARMI: osservabile avvolta su `2pi` (il caso GIUSTO)\n")
    W("     -> nessun punto grave -> %s\n"
      % ("OK: non inventa difetti" if ok5 else "*** ne inventa ***"))
    e.append(ok5)

    ok = all(e)
    W("-" * 96 + "\n  -> %s\n\n" % ("i criteri PASSANO" if ok else "*** NON PASSANO ***"))
    return ok


def main():
    W = sys.stdout.write
    if not collaudo(W):
        return 1
    testo = io.open(SORGENTE, encoding="utf-8").read()
    blob = hashlib.sha1(open(SORGENTE, "rb").read()).hexdigest()[:8]
    punti = censisci(testo)
    try:
        os.makedirs(os.path.dirname(OUT))
    except OSError:
        pass
    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    Wf = o.write
    Wf("# CENSIMENTO — **la famiglia «`4π` dichiarato, `2π` usato»**\n\n")
    Wf("> Generato da `csv/_test_fork/_censimento_fasi.py`. **Blob simulatore `%s`.**\n" % blob)
    Wf("> **Sola lettura: nessuna cura, nessuna proposta in codice.**\n>\n")
    Wf("> **LA REGOLA DI FONDO:** *lo spinore ha periodo `4π`; tutto ciò che si OSSERVA da "
       "lui ha periodo `2π`; un ACCUMULO non ha periodo.*\n\n")
    Wf("**PUNTI TROVATI: %d**, di cui **GRAVI: %d**.\n\n"
       % (len(punti), sum(1 for p in punti if p["grave"])))
    Wf("| riga | funzione | tipo | **grave** | classe | flag che lo governa | che cosa |\n")
    Wf("|--:|---|:--:|:--:|:--:|---|---|\n")
    for p in punti:
        Wf("| `%d` | `%s` | `%s` | %s | **`%s`** | `%s` | %s |\n"
           % (p["riga"], p["fn"], p["tipo"], "⚠ **SÌ**" if p["grave"] else "no",
              p["classe"], p["flag"], p["fonte"]))
    Wf("\n## LE CLASSI, e la distinzione è il punto *(§S)*\n\n")
    Wf("| classe | che cos'è | che si fa |\n|:--:|---|---|\n")
    Wf("| **`T`** | **avvolgimento di una FASE** *(topologia)* | **NON si leviga.** Il salto da "
       "`2π` a `0` è un artefatto della **coordinata**, non una discontinuità fisica: "
       "**levigarlo inventerebbe valori che non esistono.** La cura è **usare il periodo "
       "giusto** |\n")
    Wf("| **`L`** | soglia, tetto, `clip` di una **LEGGE** | **si leviga**, coi tre obblighi del "
       "corollario 7 di `A11` e la **larghezza DERIVATA**. *Una levigatura con larghezza scelta "
       "a mano è un parametro nuovo: peggio dello spigolo* |\n")
    Wf("| **`E`** | **evento discreto** | l'evento **resta discreto** *(il grafo è "
       "discreto)*, **ma la sua PROBABILITÀ o il suo TASSO dev'essere liscio** |\n")
    Wf("\n**⚠ TUTTI i punti di questo censimento sono di CLASSE `T`**: sono avvolgimenti e "
       "letture di fasi. **Le classi `L` ed `E` appartengono al censimento delle SCALE** "
       "*(`SCALE-TW`: soglia della mitosi, `discesa`, il punto di inversione, `tanh(3·…)`)*, "
       "**che è un lavoro diverso e non si fa qui.**\n")
    Wf("\n## CHE COSA QUESTO STRUMENTO NON FA\n\n")
    Wf("**Non decide.** Ogni punto esce con la sua classe e col flag che lo governa; **la "
       "proposta è un lavoro a parte**, e per i punti non capiti si scrive `DA DECIDERE`.\n")
    Wf("**E non distingue ATTIVO da DORMIENTE da solo:** riporta **il flag**, e il default si "
       "legge dal sorgente. *(Un flag `False` non garantisce che il ramo non giri: il driver ne "
       "accende molti — è il fatto che la sezione `CURE VERIFICATE` ha reso visibile.)*\n")
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
