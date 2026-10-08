# -*- coding: utf-8 -*-
"""IL TETTO PER NODO e LA LUNGHEZZA MINIMA -- i due pezzi della decisione `(C)`.

**PARTE `1` — L'ARITMETICA DEL TETTO.** Si rifa' la cascata del bilancio *(`b6cba2f`)* con un
### **tetto per nodo** `C` *(la capacita')*, e si risponde a due domande:
`(a)` il ### **collasso su un nodo resta lo stato piu' basso?**
`(b)` a che livello ### **si ferma la cascata**, e ### **quale dei due limiti prevale** — il
calore o il tetto?
### ⛔ **`C` NON si sceglie: si SCANDISCE**, perche' l'unita' di stato e' un punto APERTO.

**PARTE `2` — IL CENSIMENTO DI `LAM` COME LIMITE DI LUNGHEZZA**, per FORMA e non per nome:
confronti, `clip`, `maximum`/`minimum` e assegnamenti in cui compare `LAM` o `2*LAM`, con la
riga, che cosa limita, ### **se la lunghezza e' la `d` RELAZIONALE o viene da `pos`** *(`A17`)*,
e se e' un ### **TAGLIO**, un ### **CANCELLO** o un'### **ENERGIA**.

Gira con:  python csv/_test_fork/_tetto_e_lam.py
"""
import ast
import io
import json
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(os.path.dirname(_QUI))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. La parte `1` e' aritmetica sui
# numeri del `_bilancio_nascita` (che ha dichiarato la sua configurazione), la parte `2` e'
# una lettura dell'AST del sorgente: il risultato non dipende da nessun flag.
SIM = os.path.join(RADICE, "soliton_simulator.py")
FUORI = os.path.join(_QUI, "_tetto_e_lam")
NL = chr(10)
P = []


def stampa(s=""):
    P.append(s)
    print(s, flush=True)


def riga(c="-", n=104):
    stampa(c * n)


# ==========================================================================
#   PARTE 1 -- L'ARITMETICA DEL TETTO
# ==========================================================================
def parte1():
    bil = json.load(io.open(os.path.join(_QUI, "_bilancio_nascita", "bilancio.json"),
                            encoding="utf-8"))
    N = float(bil["scena"]["N"])
    g = float(bil["scena"]["g"])
    w = 1.0
    liberata = float(bil["liberata"])
    k_calore = int(bil["livello_di_arresto"])
    rho_calore = N / (2.0 ** k_calore)

    riga("=")
    stampa("PARTE 1 -- L'ARITMETICA DEL TETTO PER NODO")
    riga("=")
    stampa("  la scena: N = %.0f, g = %.1f, w = %.1f; il calore disponibile %.1f"
           % (N, g, w, liberata))
    stampa("  SENZA tetto la cascata si ferma al livello %d, cioe' a %d nodi da rho = %.1f"
           % (k_calore, 2 ** k_calore, rho_calore))
    stampa()
    stampa("  (a) IL COLLASSO SU UN NODO RESTA LO STATO PIU' BASSO?")
    stampa("      Con un tetto C per nodo, un nodo solo e' AMMESSO solo se C >= N = %.0f." % N)
    stampa("      Se C < N la norma deve stare su almeno ceil(N/C) nodi, e il minimo diventa")
    stampa("          H_min = -w*(archi) + (g/2) * (N/C) * C^2 = -w*(archi) + (g/2) * N * C")
    stampa("      cioe' il fattore C/N di quello senza tetto, (g/2) N^2.")
    stampa()
    stampa("      C      nodi minimi   H_min (senza hopping)   H(un nodo)      un nodo ammesso?")
    stampa("      " + "-" * 88)
    tab = []
    for C in (400.0, 100.0, 50.0, 25.0, 10.0, 4.0, 2.0, 1.0):
        nodi = N / C
        hmin = 0.5 * g * N * C
        huno = 0.5 * g * N * N
        amm = C >= N
        tab.append({"C": C, "nodi_minimi": nodi, "H_min": hmin, "H_un_nodo": huno,
                    "un_nodo_ammesso": amm})
        stampa("      %6.1f  %11.1f   %21.1f   %12.1f      %s"
               % (C, nodi, hmin, huno, "SI" if amm else "### NO"))
    stampa()
    stampa("      ### -> IL COLLASSO SU UN NODO NON E' PIU' LO STATO PIU' BASSO per nessun")
    stampa("      ###    C < %.0f: E' VIETATO. Lo stato piu' basso diventa <<la norma spalmata" % N)
    stampa("      ###    sul MINIMO numero di nodi che il tetto consente>>, cioe' esattamente")
    stampa("      ###    <<compressa al limite SENZA collassare>>.")
    stampa("      ### -> E IL TETTO ALZA IL MINIMO DEL FATTORE N/C: con C = 25 il minimo passa")
    stampa("      ###    da %.1f a %.1f, cioe' 16 volte piu' alto."
           % (0.5 * g * N * N, 0.5 * g * N * 25.0))
    stampa()
    stampa("  (b) A CHE LIVELLO SI FERMA LA CASCATA, E QUALE LIMITE PREVALE?")
    stampa("      il CALORE si esaurisce al livello %d: %d nodi da rho = %.1f"
           % (k_calore, 2 ** k_calore, rho_calore))
    stampa("      il TETTO chiede N/2^k <= C, cioe' k >= log2(N/C):")
    stampa()
    stampa("      C      livello richiesto dal tetto   quale limite PREVALE")
    stampa("      " + "-" * 76)
    due = []
    import math
    for C in (400.0, 100.0, 50.0, 25.0, 10.0, 4.0, 2.0, 1.0):
        k_tetto = max(0, math.ceil(math.log2(N / C))) if C < N else 0
        if k_tetto <= k_calore:
            quale = "IL CALORE (il tetto e' gia' soddisfatto a %d)" % k_calore
        else:
            quale = ("### IL TETTO: chiede %d livelli, il calore ne paga %d"
                     % (k_tetto, k_calore))
        due.append({"C": C, "livello_tetto": k_tetto, "livello_calore": k_calore,
                    "prevale": "calore" if k_tetto <= k_calore else "tetto"})
        stampa("      %6.1f  %27d   %s" % (C, k_tetto, quale))
    stampa()
    stampa("      ### -> I DUE LIMITI DANNO FERMATE DIVERSE, e il discrimine E' UN NUMERO:")
    stampa("      ###    rho = %.1f per nodo, cioe' dove il calore si esaurisce." % rho_calore)
    stampa("      ###    SE C >= %.1f: prevale IL CALORE. Le nascite si fermano prima che il"
           % rho_calore)
    stampa("      ###       tetto morda, e la materia resta a rho = %.1f senza toccare il"
           % rho_calore)
    stampa("      ###       tetto -- la barriera NON lavora, e il freno e' la nascita.")
    stampa("      ###    SE C < %.1f: prevale IL TETTO. Il calore NON basta a frammentare"
           % rho_calore)
    stampa("      ###       quanto il tetto chiede, quindi LA MATERIA RESTA COMPRESSA AL")
    stampa("      ###       LIMITE -- ed e' esattamente il terzo caso di Luca.")
    stampa("      ### -> QUINDI NON <<PREVALE>> SEMPRE LO STESSO: prevale IL PIU' STRETTO, e")
    stampa("      ###    quale sia dipende DALL'UNITA' DI STATO, che e' APERTA.")
    return {"N": N, "g": g, "w": w, "liberata": liberata,
            "livello_calore": k_calore, "rho_calore": rho_calore,
            "tabella_a": tab, "tabella_b": due}


# ==========================================================================
#   PARTE 2 -- IL CENSIMENTO DI `LAM`
# ==========================================================================
# ### le forme di un LIMITE: un confronto, un `clip`, un `maximum`/`minimum`
FORME = {"maximum": "PAVIMENTO (taglio a senso unico)",
         "minimum": "TETTO (taglio a senso unico)",
         "clip": "TAGLIO (a senso unico o doppio)"}


def parte2():
    sorgente = io.open(SIM, encoding="utf-8").read()
    righe = sorgente.split(NL)
    albero = ast.parse(sorgente)
    # ### la mappa riga -> funzione, per NOME (i numeri di riga non si citano da soli)
    mappa = {}
    for n in ast.walk(albero):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for ln in range(n.lineno, (getattr(n, "end_lineno", n.lineno) or n.lineno) + 1):
                mappa.setdefault(ln, n.name)

    riga("=")
    stampa("PARTE 2 -- IL CENSIMENTO DI `LAM` COME LIMITE DI LUNGHEZZA, per FORMA")
    riga("=")
    trovati = []
    for i, r in enumerate(righe, 1):
        if not re.search(r"\bLAM\b", r):
            continue
        nudo = r.split("#")[0]
        if not re.search(r"\bLAM\b", nudo):
            continue            # ### solo in un COMMENTO: non e' una legge
        due = bool(re.search(r"2\s*\*\s*LAM|LAM\s*\*\s*2|2\.0\s*\*\s*LAM", nudo))
        forma = [v for k, v in FORME.items() if (k + "(") in nudo]
        confronto = bool(re.search(r"[<>]=?\s*[^=]*LAM|LAM\s*[<>]=?", nudo))
        if not (forma or confronto or "clip" in nudo):
            continue            # ### LAM compare, ma NON come limite
        # ### la lunghezza e' RELAZIONALE o viene da `pos`? (A17)
        rel = bool(re.search(r"\bd\b|\bd0\b|self\.d|\.d\[|lung", nudo))
        # ### ⚠ **PRIMA SCRIVEVO `"pos" in nudo`, E PRENDEVA UN FALSO POSITIVO:** alla
        # ### riga 6547 di `_smorza` c'e' `pos = prima > 0.0`, cioe' un ### **booleano
        # ### LOCALE** che si chiama `pos` -- non `self.pos`. ### **Preso rileggendo il
        # ### sorgente, non dal banco.** Ora si chiede `self.pos`/`.pos` oppure una `norm`
        # ### su una differenza di punti.
        # ### IL CRITERIO, SENZA NESSUN ESCAPE: solo sottostringhe.
        # ### `pos` conta SOLO se e' un attributo (`self.pos`, `.pos`) oppure se la
        # ### riga calcola una NORMA su punti. Un `pos` NOME LOCALE non conta: alla
        # ### riga 6547 di `_smorza` c'e' `pos = prima > 0.0`, un booleano.
        _att = ("self.pos" in nudo) or (".pos" in nudo)
        _norma_su_punti = ("linalg.norm(" in nudo) and ("pos" in nudo
                                                       or "q -" in nudo
                                                       or "(sp" in nudo)
        da_pos = bool(_att or _norma_su_punti)
        tipo = (forma[0] if forma else ("CANCELLO (un confronto che decide)" if confronto
                                        else "?"))
        trovati.append({"riga": i, "funzione": mappa.get(i, "(modulo)"),
                        "due_lam": due, "tipo": tipo,
                        "relazionale": rel, "da_pos": da_pos,
                        "testo": nudo.strip()[:110]})
    stampa("  punti in cui `LAM` e' un LIMITE DI LUNGHEZZA: %d" % len(trovati))
    stampa("      di cui con 2*LAM: %d" % sum(1 for x in trovati if x["due_lam"]))
    stampa("      di cui su una lunghezza RELAZIONALE (`d`, `d0`): %d"
           % sum(1 for x in trovati if x["relazionale"]))
    stampa("      di cui su qualcosa calcolato da `pos`: %d   ### (A17)"
           % sum(1 for x in trovati if x["da_pos"]))
    stampa()
    for x in trovati:
        stampa("  riga %5d  %-26s %-34s %s%s"
               % (x["riga"], x["funzione"][:26], x["tipo"][:34],
                  "2*LAM " if x["due_lam"] else "", "DA-POS" if x["da_pos"] else
                  ("relazionale" if x["relazionale"] else "")))
        stampa("              %s" % x["testo"])
    return trovati


def main():
    os.makedirs(FUORI, exist_ok=True)
    uno = parte1()
    stampa()
    due = parte2()
    io.open(os.path.join(FUORI, "tetto_e_lam.json"), "w", encoding="utf-8").write(
        json.dumps({"tetto": uno, "lam": due}, ensure_ascii=False, default=str))
    io.open(os.path.join(FUORI, "tetto_e_lam.txt"), "w", encoding="utf-8").write(
        NL.join(P) + NL)
    stampa()
    stampa("scritto %s" % os.path.join(FUORI, "tetto_e_lam.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
