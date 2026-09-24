# -*- coding: utf-8 -*-
"""SIGILLO DI `E4-LAM`: la legge `d >= LAM` si verifica SEMPRE, e `cs > 0` e' un invariante.

Decisione di Luca, 2026-09-24: *«la lunghezza degli archi non puo' scendere sotto la lunghezza
tipica del sistema» e' una LEGGE, non una garanzia che dipende da un flag.*

COSA CAMBIA NEL CODICE, ed e' poco e mirato:
  * `verifica_invarianti`: la forma `'lam'` non e' piu' dentro `if _lam_attivo`. Prima, a
    `SCALA_MIN` e `SCALA_MIN_PASSO` spenti, **degradava a `d > 0`**;
  * `_lam_attivo` **tolto** (era il suo unico uso: lasciarlo sarebbe codice morto);
  * `'_cs_nodo_prev'` aggiunto ai `DOMINI` come `'pos'`, perche' **`cs > 0` e' DERIVATO**
    *(`cs_floor > 0` e `transizione ∈ (0,1)` stretto)*, e una proprieta' derivata e' un
    **invariante**, non un caso da contare.

⚠ IL TEST CHE CONTA E' `T3`: **un arco sotto `LAM`, a flag SPENTI, DEVE fermare il run.**
  Prima non lo fermava. E `T4` e' il controllo che rende `T3` leggibile: **con `d >= LAM` non
  deve fermarsi**, senno' `T3` passerebbe perche' il controllo si ferma SEMPRE.

ASCII PURO.
"""
import io
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, RADICE)
SORGENTE = os.path.join(RADICE, "soliton_simulator.py")
DRIVER = os.path.join(RADICE, "csv", "_test_fork", "_scena_video.py")
RIF120 = os.path.join(RADICE, "csv", "_test_fork", "_cura1_corto", "scena_000120.pkl.gz")
DEST = os.path.join(_QUI, "_sig_e4lam")
INERTE = os.path.join(DEST, "inerte")
COMUNE = ["--sep=4.0", "--serie=20", "--chi-basc=on", "--chi-coop=on", "--scala-min=off",
          "--coes-adim=on", "--peq-esatto=on", "--peq-nascita-locale=on",
          "--scala-min-passo=on", "--coes-causale=on", "--anom-simm=on", "--invarianti=on"]


def confronta_snap(p_a, p_b, W):
    import gzip
    import pickle

    def leggi(p):
        return pickle.load(gzip.open(p, "rb"))["attrs"]
    A, B = leggi(p_a), leggi(p_b)
    ug = dv = nc = 0
    diversi = []
    for k in sorted(set(A) | set(B)):
        if k not in A or k not in B:
            nc += 1
            continue
        a, b = A[k], B[k]
        try:
            if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
                a, b = np.asarray(a), np.asarray(b)
                if a.shape != b.shape:
                    dv += 1
                    diversi.append("%s(shape %s!=%s)" % (k, a.shape, b.shape))
                    continue
                if a.size == 0 or np.array_equal(a, b):
                    ug += 1
                else:
                    dv += 1
                    try:
                        diversi.append("%s(max|d|=%.3e)" % (k, float(np.max(np.abs(a - b)))))
                    except Exception:
                        diversi.append(k)
            elif a == b:
                ug += 1
            else:
                dv += 1
                diversi.append("%s(%r != %r)" % (k, a, b))
        except Exception:
            nc += 1
    W("  campi UGUALI %d   DIVERSI %d   non confrontati %d\n" % (ug, dv, nc))
    if diversi:
        W("  i diversi: %s\n" % ", ".join(diversi[:8]))
    return ug, dv


class FintoArco(object):
    """Il minimo che `verifica_invarianti` legge. Gli attributi ASSENTI vengono SALTATI
    (`getattr(..., None) -> continue`), quindi si controlla solo cio' che si mette.

    !! TRE VOLTE IL BANCO E' STATO PIU' POVERO DELL'INGRESSO VERO, e OGNI volta l'ha
       preso il collaudo. Vale la pena elencarle, perche' e' la stessa forma:
         1. mancavano `i` e `j`: la VIA DI VIOLAZIONE li legge per dire QUALE arco ha
            violato (`extra['arco'] = '%d-%d'`) -> arrivava un `AttributeError` invece di
            `DominioViolato`, e `K2` falliva **per un difetto del banco**;
         2. `K3` accettava `m is not None`, cioe' QUALUNQUE eccezione -- e riceveva
            proprio quell'`AttributeError`. **Un criterio che accetta tutto passa sempre**;
         3. `j = arange(n) + 1` contiene `n`, che VIOLA il dominio `0 <= j < n`: il
            controllo si fermava su `j` prima di arrivare a `d`, e `K1` falliva.
       **Ora il grafo e' VALIDO: un anello, `j = (i + 1) % n`.**
    """

    def __init__(self, d):
        self.d = np.asarray(d, dtype=float)
        self.n = len(self.d)
        self.i = np.arange(self.n)
        self.j = (np.arange(self.n) + 1) % self.n     # un ANELLO: tutti gli indici < n


def collaudo(W, S):
    W("COLLAUDO DEI CRITERI su casi a RISPOSTA NOTA (`P1-sexies`), PRIMA di misurare\n")
    W("-" * 96 + "\n")
    e = []
    LAM = S.LAM

    def scatta(d, scala_min, scala_min_passo):
        """`verifica_invarianti` solleva? Si rimettono i flag come erano, sempre."""
        v_sm, v_smp = S.SCALA_MIN, S.SCALA_MIN_PASSO
        S.SCALA_MIN, S.SCALA_MIN_PASSO = scala_min, scala_min_passo
        try:
            S.Rete.verifica_invarianti(FintoArco(d), dove="collaudo")
            return None, None
        except S.DominioViolato as ex:
            return "DominioViolato", str(ex)
        except Exception as ex:
            # !! NON si confonde con una violazione: un'eccezione QUALUNQUE e' un difetto
            #    del BANCO, e `K3` prima passava proprio per questo (accettava tutto).
            return type(ex).__name__, str(ex)
        finally:
            S.SCALA_MIN, S.SCALA_MIN_PASSO = v_sm, v_smp

    sopra = [LAM, LAM * 1.5, LAM * 2.0]
    sotto = [LAM, LAM * 0.5, LAM * 2.0]        # il secondo e' SOTTO la legge

    tipo, m = scatta(sopra, False, False)
    ok1 = (tipo is None)
    W("K1 `d >= LAM` a flag SPENTI non deve fermarsi -> %s  (%s)\n"
      % ("OK" if ok1 else "*** si ferma ***", tipo or "nessuna eccezione"))
    e.append(ok1)

    tipo, m = scatta(sotto, False, False)
    ok2 = (tipo == "DominioViolato" and "LAM" in (m or ""))
    W("K2 IL CASO CHE DEVE FERMARSI: `d < LAM` a flag SPENTI -> %s  (%s)\n"
      % ("OK: `DominioViolato`, e la regola nomina LAM" if ok2
         else "*** non e' `DominioViolato`, o il messaggio non nomina LAM ***", tipo))
    if m:
        W("     messaggio: %s\n" % m[:220])
    e.append(ok2)

    tipo, m = scatta(sotto, False, True)
    ok3 = (tipo == "DominioViolato")
    W("K3 e `d < LAM` a flag ACCESI si ferma come prima -> %s  (%s)\n"
      % ("OK" if ok3 else "*** NO: serve `DominioViolato`, non un'eccezione qualunque ***",
         tipo))
    e.append(ok3)

    # IL CASO CHE DEVE FALLIRE: la regola VECCHIA, a flag spenti, ACCETTAVA `d < LAM`
    vecchia = float(min(sotto)) > 0.0
    ok4 = vecchia
    W("K4 IL CASO CHE DEVE FALLIRE: la regola VECCHIA a flag spenti era `d > 0`, e "
      "`min(d) = %.4f > 0` -> %s\n"
      % (min(sotto), "OK: il difetto e' riprodotto (prima PASSAVA)" if ok4 else "*** NO ***"))
    e.append(ok4)

    # K5/K6: i due criteri NUOVI, sui casi a risposta NOTA.
    #   Nascono da `Z142`: `T1` cercava nel TESTO e `D37` era una chiave duplicata. Entrambi
    #   si collaudano su sorgenti sintetici, dove la risposta e' nota in anticipo.
    import ast as _a
    import collections as _c

    def rif_codice(src):
        return [n.lineno for n in _a.walk(_a.parse(src))
                if isinstance(n, _a.Name) and n.id == "_lam_attivo"]

    def dup_dominio(src):
        for nodo in _a.walk(_a.parse(src)):
            if isinstance(nodo, _a.Assign) and any(
                    isinstance(b, _a.Name) and b.id == "DOMINI" for b in nodo.targets):
                ch = [k.value for k in nodo.value.keys if isinstance(k, _a.Constant)]
                return sorted(k for k, n2 in _c.Counter(ch).items() if n2 > 1)
        return None

    solo_commento = "# qui si parla di _lam_attivo ma e' un COMMENTO\nx = 1\n"
    ok5 = (rif_codice(solo_commento) == []) and ("_lam_attivo" in solo_commento)
    W("K5 IL CASO CHE DEVE FALLIRE: `_lam_attivo` SOLO in un commento -> l'AST dice %s "
      "mentre un `in` sul testo direbbe TROVATO -> %s\n"
      % (rif_codice(solo_commento) or "[]",
         "OK: il criterio vecchio sbagliava" if ok5 else "*** NO ***"))
    e.append(ok5)

    con_codice = "if _lam_attivo:\n    pass\n"
    ok6 = (len(rif_codice(con_codice)) == 1)
    W("K6 e un riferimento VERO si trova: righe %s -> %s\n"
      % (rif_codice(con_codice), "OK" if ok6 else "*** NO ***"))
    e.append(ok6)

    doppio = "DOMINI = {\n    'a': 1,\n    'b': 2,\n    'a': 3,\n}\n"
    ok7 = (dup_dominio(doppio) == ["a"])
    W("K7 SECONDO CASO CHE DEVE FALLIRE: un `DOMINI` con la chiave `'a'` DUE volte -> "
      "duplicate %s -> %s\n" % (dup_dominio(doppio), "OK" if ok7 else "*** NO ***"))
    e.append(ok7)

    pulito = "DOMINI = {\n    'a': 1,\n    'b': 2,\n}\n"
    ok8 = (dup_dominio(pulito) == [])
    W("K8 e un `DOMINI` pulito non da' falsi allarmi: duplicate %s -> %s\n"
      % (dup_dominio(pulito) or "NESSUNA", "OK" if ok8 else "*** NO ***"))
    e.append(ok8)

    ok = all(e)
    W("-" * 96 + "\n  -> %s\n\n" % ("i criteri PASSANO" if ok else "*** NON PASSANO ***"))
    return ok


def main():
    W = sys.stdout.write
    try:
        os.makedirs(DEST)
    except OSError:
        pass
    ref = io.open(os.path.join(DEST, "REFERTO.txt"), "w", encoding="utf-8", newline="\n")

    def P(s):
        W(s)
        ref.write(s)

    P("# SIGILLO -- `E4-LAM`: la legge `d >= LAM` si verifica SEMPRE\n#\n")
    os.chdir(RADICE)
    import soliton_simulator as S
    import hashlib
    P("blob simulatore ORA (sha1 byte grezzi) %s\n"
      % hashlib.sha1(io.open(SORGENTE, "rb").read()).hexdigest()[:8])
    P("LAM = %s\n\n" % S.LAM)
    if not collaudo(P, S):
        ref.close()
        return 1

    esiti = []
    sorg = io.open(SORGENTE, encoding="utf-8").read()

    # T1: il gate e' sparito -- DALL'AST, non dal testo.
    #   !! LA PRIMA STESURA CERCAVA `"_lam_attivo" not in sorg`, cioe' NEL TESTO, e trovava
    #   le DUE occorrenze nei COMMENTI che SPIEGANO che il gate e' stato tolto: `FAIL` falso
    #   su codice corretto. **Un `FAIL` falso costa piu' di un sigillo mancante, perche' si
    #   porta dietro una diagnosi.** La misura giusta e' l'AST: un `Name` di CODICE.
    import ast as _ast
    _alb = _ast.parse(sorg)
    _rif = sorted({n.lineno for n in _ast.walk(_alb)
                   if isinstance(n, _ast.Name) and n.id == "_lam_attivo"})
    _testo = sorg.count("_lam_attivo")
    ok = (len(_rif) == 0)
    P("T1    %s `_lam_attivo` non ha piu' RIFERIMENTI DI CODICE: dall'AST %s\n"
      % ("PASS" if ok else "FAIL", _rif or "[] (nessuno)"))
    P("      (nel TESTO compare %d volte, e sono COMMENTI: per questo il criterio guarda\n"
      "       l'AST e non un `in`.)\n" % _testo)
    esiti.append(ok)

    # T1b: NESSUNA CHIAVE DUPLICATA nei `DOMINI` -- e' la cura di `D37`, dall'AST.
    import collections as _co
    _chiavi, _dup = [], []
    for nodo in _ast.walk(_alb):
        if isinstance(nodo, _ast.Assign) and any(
                isinstance(b, _ast.Name) and b.id == "DOMINI" for b in nodo.targets):
            _chiavi = [k.value for k in nodo.value.keys if isinstance(k, _ast.Constant)]
            _dup = sorted(k for k, c in _co.Counter(_chiavi).items() if c > 1)
            break
    ok = (len(_chiavi) > 0 and not _dup)
    P("T1b   %s `DOMINI` NON ha chiavi duplicate: %d chiavi, duplicate %s\n"
      % ("PASS" if ok else "FAIL", len(_chiavi), _dup or "NESSUNA"))
    P("      -> e' la cura di `D37`. In un letterale di dict la chiave duplicata vince\n"
      "         l'ULTIMA, quindi una voce duplicata e' CODICE MORTO **in silenzio**.\n")
    esiti.append(ok)

    # T2: `_cs_nodo_prev` e' fra i DOMINI, come `pos`
    ok = (S.DOMINI.get("_cs_nodo_prev", (None,))[0] == "pos")
    P("T2    %s `_cs_nodo_prev` e' nei DOMINI come `pos`: %r\n"
      % ("PASS" if ok else "FAIL", S.DOMINI.get("_cs_nodo_prev")))
    P("      -> `cs > 0` e' DERIVATO (cs_floor > 0, transizione in (0,1) stretto), quindi e'\n")
    P("         un INVARIANTE e non un caso da contare.\n")
    esiti.append(ok)

    # T3/T4: i due casi, dal collaudo, rifatti qui come TEST
    def scatta(d, sm, smp):
        v1, v2 = S.SCALA_MIN, S.SCALA_MIN_PASSO
        S.SCALA_MIN, S.SCALA_MIN_PASSO = sm, smp
        try:
            S.Rete.verifica_invarianti(FintoArco(d), dove="sigillo")
            return None
        except S.DominioViolato as ex:
            return "DominioViolato: %s" % ex
        except BaseException as ex:
            return "*** ECCEZIONE ESTRANEA *** %s: %s" % (type(ex).__name__, ex)
        finally:
            S.SCALA_MIN, S.SCALA_MIN_PASSO = v1, v2

    L = S.LAM
    m = scatta([L, L * 0.5, L * 2.0], False, False)
    ok = (m is not None and m.startswith("DominioViolato") and "LAM" in m)
    P("T3    %s IL CASO CHE DEVE FERMARSI: un arco sotto `LAM` a FLAG SPENTI ferma il run\n"
      % ("PASS" if ok else "FAIL"))
    P("      %s\n" % (m or "(non si e' fermato)")[:240])
    esiti.append(ok)

    m = scatta([L, L * 1.5, L * 2.0], False, False)
    ok = (m is None)
    P("T4    %s E IL CONTROLLO: con `d >= LAM` NON si ferma -> %s\n"
      % ("PASS" if ok else "FAIL", "non si ferma" if ok else m[:160]))
    P("      -> senza `T4`, `T3` passerebbe anche se il controllo si fermasse SEMPRE.\n")
    esiti.append(ok)

    # T5: BYTE-INERZIA sui run di oggi
    P("\n" + "-" * 96 + "\n")
    P("T5 -- BYTE-INERZIA: 120 passi nella configurazione dei run, contro `_cura1_corto`.\n")
    P("      L'invariante LEGGE soltanto: non deve cambiare un bit.\n")
    P("-" * 96 + "\n")
    if not os.path.exists(RIF120):
        P("*** manca il riferimento: T5 NON SI FA ***\n")
        esiti.append(False)
    else:
        import runpy
        import time
        try:
            os.makedirs(INERTE)
        except OSError:
            pass
        for f in os.listdir(INERTE):
            if f.endswith(".pkl.gz"):
                os.remove(os.path.join(INERTE, f))
        vecchio = list(sys.argv)
        sys.argv = ["_scena_video.py", "20", INERTE] + COMUNE
        t0 = time.time()
        try:
            runpy.run_path(DRIVER, run_name="__main__")
        finally:
            sys.argv = vecchio
        P("  (%.1f s)\n" % (time.time() - t0))
        p = os.path.join(INERTE, "scena_000120.pkl.gz")
        if not os.path.exists(p):
            P("*** lo snapshot non c'e' ***\n")
            esiti.append(False)
        else:
            ug, dv = confronta_snap(RIF120, p, P)
            ok = (dv == 0 and ug > 100)
            P("T5    %s BYTE-INERTE: %d campi identici, %d diversi\n"
              % ("PASS" if ok else "FAIL", ug, dv))
            esiti.append(ok)

    n = sum(1 for x in esiti if x)
    P("\n" + "=" * 96 + "\nESITO: %d/%d\n" % (n, len(esiti)) + "=" * 96 + "\n")
    P("*** %s ***\n" % ("SIGILLO PASSATO." if n == len(esiti)
                        else "SIGILLO FALLITO: reperto, commit, STOP (par.5)."))
    P("\n!! COSA QUESTO SIGILLO NON DICE: che `d >= LAM` sia la REALIZZAZIONE giusta della\n")
    P("   legge. Dice che la legge e' ora VERIFICATA SEMPRE. La realizzazione di oggi e' il\n")
    P("   freno a senso unico, cioe' `D31`, e la sua cura e' un lavoro a parte.\n")
    ref.close()
    return 0 if n == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
