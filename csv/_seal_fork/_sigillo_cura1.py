# -*- coding: utf-8 -*-
"""SIGILLO DI `CURA 1` -- L'OROLOGIO: `RITMO_WRAP_2PI` approvata, `TW_SPINORE` BLOCCATO.

Mandato di Luca, 2026-09-24. Due cose in una cura, perche' sono lo stesso pezzo:

  (a) **`RITMO_WRAP_2PI` E' APPROVATA** -- il wrap del ritmo sul periodo GIUSTO (`2pi`).
      Il suo sigillo esiste gia' (`_sigillo_ritmo_wrap.py`, `4/4`) e la sua prova anche
      (`Z123`, 600 passi). **Qui si sigilla che il DRIVER LA ACCENDE**, che e' la cosa nuova:
      un flag approvato che nessun run accende non e' una cura, e' un ramo morto.
  (b) **`TW_SPINORE` E' BLOCCATO** -- il simulatore RIFIUTA DI PARTIRE se e' acceso.
      E' il **ponte inverso**: la torsione, che prende la scala da `phi`, scrive lo SPINORE.
      Il codice resta, spento, e ora anche **impedito**.

⚠ COSA QUESTO SIGILLO DEVE PROVARE, e la parte che conta e' la seconda:
  * che il RIFIUTO SCATTA quando il flag e' acceso  -- senza questo, il presidio e' una nota;
  * che NON scatta quando e' spento -- **ed e' il controllo che rende leggibile il primo**:
    un rifiuto che scatta sempre bloccherebbe ogni run, e un rifiuto che non scatta mai
    passerebbe il primo test per caso.
  * che l'aggiunta e' **BYTE-INERTE** a `TW_SPINORE` spento E `RITMO_WRAP_2PI` spento, cioe'
    nella configurazione di PRIMA: e' l'unico modo di dire che il presidio non ha effetti
    collaterali, separandolo dall'effetto VOLUTO di `(a)`.

ASCII PURO.
"""
import ast
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SORGENTE = os.path.join(RADICE, "soliton_simulator.py")
DRIVER = os.path.join(RADICE, "csv", "_test_fork", "_scena_video.py")
RIF120 = os.path.join(RADICE, "csv", "_test_fork", "_val600", "scena_000120.pkl.gz")
DEST = os.path.join(_QUI, "_sig_cura1")
INERTE = os.path.join(DEST, "inerte")
COMUNE = ["--sep=4.0", "--serie=20", "--chi-basc=on", "--chi-coop=on", "--scala-min=off",
          "--coes-adim=on", "--peq-esatto=on", "--peq-nascita-locale=on",
          "--scala-min-passo=on", "--coes-causale=on", "--anom-simm=on", "--invarianti=on"]
# la ragione che il rifiuto DEVE nominare: si cerca nel messaggio, non si spera che ci sia
PAROLE_RAGIONE = ("ponte", "inverso")


def confronta_snap(p_a, p_b, W):
    """206 campi contro 206: uguali, diversi, non confrontati. Copiato da `_sigillo_fase_2pi`."""
    import gzip
    import pickle
    import numpy as np

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
                if a.size == 0:
                    ug += 1
                    continue
                if np.array_equal(a, b):
                    ug += 1
                else:
                    dv += 1
                    try:
                        diversi.append("%s(max|d|=%.3e)"
                                       % (k, float(np.max(np.abs(a - b)))))
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


def rifiuti_nel_sorgente():
    """DALL'AST: i `raise SystemExit` che stanno dentro un test su `TW_SPINORE`."""
    albero = ast.parse(io.open(SORGENTE, encoding="utf-8").read())
    fuori = []
    for n in ast.walk(albero):
        if not isinstance(n, ast.If):
            continue
        nomi = {x.id for x in ast.walk(n.test) if isinstance(x, ast.Name)}
        if "TW_SPINORE" not in nomi:
            continue
        for s in ast.walk(n):
            if isinstance(s, ast.Raise) or (
                    isinstance(s, ast.Call) and isinstance(s.func, ast.Name)
                    and s.func.id == "SystemExit"):
                fuori.append(getattr(s, "lineno", -1))
    return sorted(set(fuori))


def collaudo(W):
    W("COLLAUDO DEI CRITERI su casi a RISPOSTA NOTA (`P1-sexies`), PRIMA di misurare\n")
    W("-" * 96 + "\n")
    e = []

    def conta(src):
        albero = ast.parse(src)
        out = []
        for n in ast.walk(albero):
            if not isinstance(n, ast.If):
                continue
            nomi = {x.id for x in ast.walk(n.test) if isinstance(x, ast.Name)}
            if "TW_SPINORE" not in nomi:
                continue
            for s in ast.walk(n):
                if isinstance(s, ast.Raise):
                    out.append(s.lineno)
        return out

    buono = "if TW_SPINORE:\n    raise SystemExit('ponte inverso')\n"
    ok1 = (len(conta(buono)) == 1)
    W("K1 trova UN rifiuto dentro `if TW_SPINORE` -> %s  (%s)\n"
      % ("OK" if ok1 else "*** NO ***", conta(buono)))
    e.append(ok1)

    # IL CASO CHE DEVE FALLIRE: un `if` su un ALTRO flag non conta
    altro = "if FASE_2PI:\n    raise SystemExit('altro')\n"
    ok2 = (len(conta(altro)) == 0)
    W("K2 IL CASO CHE DEVE FALLIRE: un rifiuto sotto un ALTRO flag -> %d trovati -> %s\n"
      % (len(conta(altro)), "OK: non lo conta" if ok2 else "*** conta il flag sbagliato ***"))
    e.append(ok2)

    # SECONDO CASO CHE DEVE FALLIRE: un `if TW_SPINORE` che NON solleva
    muto = "if TW_SPINORE:\n    print('acceso')\n"
    ok3 = (len(conta(muto)) == 0)
    W("K3 SECONDO CASO CHE DEVE FALLIRE: `if TW_SPINORE` che NON solleva -> %d -> %s\n"
      % (len(conta(muto)), "OK: un avviso non e' un rifiuto"
         if ok3 else "*** conta un avviso come rifiuto ***"))
    e.append(ok3)

    # TERZO: la ragione. Un messaggio che non la nomina NON deve passare.
    ok4 = all(p in "il ponte inverso: la torsione scrive lo spinore" for p in PAROLE_RAGIONE)
    ok5 = not all(p in "TW_SPINORE non e' supportato" for p in PAROLE_RAGIONE)
    W("K4 il criterio sulla RAGIONE accetta un messaggio che la nomina -> %s\n"
      % ("OK" if ok4 else "*** NO ***"))
    W("K5 TERZO CASO CHE DEVE FALLIRE: un messaggio SENZA la ragione -> %s\n"
      % ("OK: non passa" if ok5 else "*** passa un messaggio muto ***"))
    e.extend([ok4, ok5])

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

    P("# SIGILLO -- `CURA 1`: l'orologio\n#\n")
    if not collaudo(P):
        ref.close()
        return 1

    import hashlib
    blob = hashlib.sha1(io.open(SORGENTE, "rb").read()).hexdigest()[:8]
    P("blob simulatore ORA (sha1 byte grezzi) %s\n" % blob)
    P("riferimento `_val600/scena_000120.pkl.gz` (blob `9557a867`)\n\n")

    esiti = []
    sorg = io.open(SORGENTE, encoding="utf-8").read()
    drv = io.open(DRIVER, encoding="utf-8").read()

    # ---------------- T1: il flag CLI esiste e il DRIVER lo passa
    ha_opzione = ('"--ritmo-wrap-2pi"' in sorg or "'--ritmo-wrap-2pi'" in sorg)
    lo_passa = "--ritmo-wrap-2pi" in drv
    ok = ha_opzione and lo_passa
    P("T1    %s L'OPZIONE ESISTE E IL DRIVER LA PASSA: opzione nel simulatore %s, "
      "nel driver %s\n" % ("PASS" if ok else "FAIL", ha_opzione, lo_passa))
    P("      -> un flag approvato che nessun run accende non e' una cura: e' un ramo morto.\n")
    esiti.append(ok)

    # ---------------- T2: dopo `_applica_flag` con l'argv del driver, e' ACCESO
    os.chdir(RADICE)
    sys.path.insert(0, RADICE)
    import soliton_simulator as S
    vecchio = list(sys.argv)
    ARGV_DRV = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "2", "--sep", "4.0",
                "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
                "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet",
                "--fork-su2", "--fork-su2-mem", "--cs-dinamico", "--tau-luce",
                "--rumore-colorato", "--pav-com", "--guscio-morbido", "--zeta-vir",
                "--ritmo-wrap-2pi"]
    try:
        sys.argv = list(ARGV_DRV)
        a = S._cli()
        S._applica_flag(a)
        acceso = bool(S.RITMO_WRAP_2PI)
    finally:
        sys.argv = vecchio
    P("T2    %s `RITMO_WRAP_2PI` DOPO `_applica_flag` con l'argv del driver = %s\n"
      % ("PASS" if acceso else "FAIL", acceso))
    esiti.append(acceso)

    # ---------------- T3: `TW_SPINORE` default spento
    import re
    m = re.search(r"^TW_SPINORE\s*=\s*(True|False)\b", sorg, re.M)
    ok = (m is not None and m.group(1) == "False")
    P("T3    %s IL DEFAULT DI `TW_SPINORE` E' SPENTO: letto dal sorgente = %s\n"
      % ("PASS" if ok else "FAIL", m.group(1) if m else "ASSENTE"))
    esiti.append(ok)

    # ---------------- T4: IL RIFIUTO SCATTA, e nomina la ragione
    righe = rifiuti_nel_sorgente()
    msg = ""
    scattato = False
    try:
        sys.argv = list(ARGV_DRV) + ["--tw-spinore"]
        a = S._cli()
        S._applica_flag(a)
    except SystemExit as ex:
        scattato = True
        msg = str(ex)
    except Exception as ex:
        scattato = True
        msg = "%s: %s" % (type(ex).__name__, ex)
    finally:
        sys.argv = vecchio
    ragione = all(p.lower() in msg.lower() for p in PAROLE_RAGIONE)
    ok = scattato and ragione
    P("T4    %s IL RIFIUTO SCATTA con `--tw-spinore`, e NOMINA LA RAGIONE\n"
      % ("PASS" if ok else "FAIL"))
    P("      scattato: %s   la ragione (%s) c'e': %s\n"
      % (scattato, "/".join(PAROLE_RAGIONE), ragione))
    P("      messaggio: %s\n" % (msg[:300] if msg else "(nessuno)"))
    P("      rifiuti trovati dall'AST dentro `if TW_SPINORE`: righe %s\n" % righe)
    esiti.append(ok)

    # ---------------- T5: e NON scatta senza il flag (il controllo che rende T4 leggibile)
    pulito = True
    err = ""
    try:
        sys.argv = list(ARGV_DRV)
        a = S._cli()
        S._applica_flag(a)
    except BaseException as ex:
        pulito = False
        err = "%s: %s" % (type(ex).__name__, ex)
    finally:
        sys.argv = vecchio
    P("T5    %s E NON SCATTA SENZA IL FLAG: `_applica_flag` passa liscio -> %s\n"
      % ("PASS" if pulito else "FAIL", "si'" if pulito else err[:200]))
    P("      -> e' il controllo che rende `T4` leggibile: un rifiuto che scatta SEMPRE\n")
    P("         bloccherebbe ogni run, e passerebbe `T4` senza essere un presidio.\n")
    esiti.append(pulito)

    # ---------------- T6: BYTE-INERZIA nella configurazione di PRIMA
    P("\n" + "-" * 96 + "\n")
    P("T6 -- BYTE-INERZIA: 120 passi con `RITMO_WRAP_2PI` FORZATO SPENTO e `TW_SPINORE`\n")
    P("      spento, contro `_val600`. Isola il PRESIDIO dall'effetto VOLUTO di (a).\n")
    P("-" * 96 + "\n")
    if not os.path.exists(RIF120):
        P("*** manca il riferimento `%s`: T6 NON SI FA ***\n" % RIF120)
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
        orig = S._applica_flag

        def _spegni(a):
            r = orig(a)
            S.RITMO_WRAP_2PI = False      # la configurazione di PRIMA
            return r
        S._applica_flag = _spegni
        t0 = time.time()
        sys.argv = ["_scena_video.py", "20", INERTE] + COMUNE
        try:
            runpy.run_path(DRIVER, run_name="__main__")
        finally:
            S._applica_flag = orig
            sys.argv = vecchio
        P("  (%.1f s)   RITMO_WRAP_2PI durante il giro: %s\n"
          % (time.time() - t0, S.RITMO_WRAP_2PI))
        p = os.path.join(INERTE, "scena_000120.pkl.gz")
        if not os.path.exists(p):
            P("*** lo snapshot non c'e': il giro non e' arrivato a 120 ***\n")
            esiti.append(False)
        else:
            ug, dv = confronta_snap(RIF120, p, P)
            ok = (dv == 0 and ug > 100)
            P("T6    %s BYTE-INERTE: %d campi identici, %d diversi\n"
              % ("PASS" if ok else "FAIL", ug, dv))
            esiti.append(ok)

    n = sum(1 for x in esiti if x)
    P("\n" + "=" * 96 + "\nESITO: %d/%d\n" % (n, len(esiti)) + "=" * 96 + "\n")
    if n == len(esiti):
        P("*** SIGILLO PASSATO. Il giro corto di `CURA 1` puo' partire. ***\n")
    else:
        P("*** SIGILLO FALLITO: si committa il reperto e si FERMA (par.5). ***\n")
    P("\n!! E IL SIGILLO NON DICE CHE LA CURA SIA GIUSTA: dice che (a) il driver la accende\n")
    P("   davvero e (b) il ponte inverso e' impedito, non solo sconsigliato.\n")
    ref.close()
    return 0 if n == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
