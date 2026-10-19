# -*- coding: utf-8 -*-
r"""**`D4`: IL VERSO E IL PROFILO DI `cs`, COI TRE RAPPORTI** — *il passo di oggi.*

> ### ⛔ **I criteri sono quelli del task history `2026-10-17_D_cs_lambda_nel_motore.md`**,
> copiati senza modifiche in `2026-10-19_D4_verso_e_profilo.md`, che fissa anche ### **le
> cinque letture operative** e ### **le protezioni** *(prima del codice, `a632e866`)*.

## ⭐ LE LETTURE, in breve *(il perche' sta nel task history)*

- ### **il passo:** la legge DEL MOTORE *(`statica_protocollo.SOSTITUISCI = False`)*, con
  `cs` dinamico *(`tick.tick_con_cs`)*;
- ### **la sorgente fotografata:** `congela = "pezzo"` -- `rho` ferma in ogni istante;
- ### **`cs`:** `mot.cs` dopo ogni tick, cioe' ### **quello che il passo ha USATO**;
- ### **CALA:** la media dei blocchi di `delta cs` sui nodi del grumo ### **negativa con `>= 3`
  barre**;
- ### **LINEARE:** sulla scansione in `x`, `R = <delta cs>/<delta Lambda>/cs'(Lambda_m)` con
  `|R - 1|` che ### **non cresce** quando `x` cala, e al `x` piu' piccolo
  `|R - 1| <= |delta Lambda|/(Lambda_m + Lambda_c) + 3 barre` *(la curvatura della forma)*;
- ### **il caso che DEVE fallire:** senza sorgente, ### **`max - min` di `mot.cs` e' `0`
  esatto a ogni tick.**

## ⛔ LE PROTEZIONI

### `(a)` **se un punto fisso non converge, il braccio si registra «non converge»** col
tick, `Lambda` minimo, `Lambda_c` e ### **QUALE punto fisso** *(`cs` o `Omega`: il giro
corto ha fatto alzare `Omega` a `x` piccolo, `a59994b9`)*, e si va avanti. ### `(b)` **per ogni corsa, il minimo
di `Lambda/Lambda_c`.** ### `(c)` **nessuna osservabile di `G`** in questa misura.

## ⭐ COME GIRA

### **Un processo per braccio** *(`STANDARD 1`)*, e ### **ogni braccio finito si scrive SUBITO**
in `doc/referti_l2/d4_bracci.jsonl` *(i risultati si salvano durante la corsa)*.

Gira con:  python csv/_misura_d4.py
Il giro corto (STANDARD 7, non per il referto):  python csv/_misura_d4.py --corto
Un braccio:  python csv/_misura_d4.py --braccio RAPPORTO DTAU X TICK ACCESO sorgente|base
"""
import hashlib
import io
import json
import os
import subprocess
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

RAPPORTI = (0.1, 1.0, 10.0)          # il task history del 2026-10-17
JSONL = os.path.join(RADICE, "doc", "referti_l2", "d4_bracci.jsonl")


# =====================================================================================
#   UN BRACCIO
# =====================================================================================
def lambda_medio(dtau):
    """### `Lambda_medio` ### **dalla scena, UNA volta** *(mappa sez.`20`)*."""
    import scena_l2 as SC
    import statica_protocollo as PR
    _i, mot, st, _p, _c, _per = SC.scena(dtau, PR.VUOTO, 0.0, PR.RAGGIO, False, True,
                                         False, PR.SEME, 1, lati=PR.LATI)
    return float(np.mean(mot.densita_vuoto(st)))


def braccio(rapporto, dtau, x, tick, acceso, quale):
    import energia_pesata as EP
    import flussi_parziali as FP
    import statica_protocollo as PR
    import tick as TK
    PR.SOSTITUISCI = False
    lm = lambda_medio(dtau)
    lc = rapporto * lm
    stato = {"cs": [], "t": 0, "lam_min": float("inf"), "chi": None}
    vero = TK.tick_con_cs
    vero_om = EP.applica

    # ### ⛔⛔ **QUALE PUNTO FISSO ALZA** *(il giro corto del `2026-10-19`)*: a `x`
    # ### piccolo alza ### **`energia_pesata.applica`** *(`Omega`)*, non `cs_al_centro`.
    # ### ### **Si registra chi e' stato**, invece di chiamarli tutti «di `cs`».
    def omega(mot, st, par, frazione):
        try:
            return vero_om(mot, st, par, frazione)
        except AssertionError:
            stato["chi"] = stato["chi"] or "Omega (energia_pesata.applica)"
            raise

    def avvolto(st, mot, par, lambda_c, salta):
        lam = mot.densita_vuoto(st)
        stato["lam_min"] = min(stato["lam_min"], float(np.min(lam)))
        stato["t"] += 1
        g = vero(st, mot, par, lambda_c, salta)
        stato["cs"].append(np.array(mot.cs, copy=True))
        stato["lam_min"] = min(stato["lam_min"], float(np.min(mot.densita_vuoto(st))))
        return g
    TK.tick_con_cs = avvolto
    EP.applica = omega
    fuori = {"rapporto": rapporto, "dtau": dtau, "x": x, "tick": tick, "acceso": acceso,
             "quale": quale, "lambda_medio": lm, "lambda_c": lc}
    try:
        centri = (0,) if quale == "sorgente" else ()
        lam, drho, dtot, per = PR.corri(dtau, x, "S3", tick, acceso, centri,
                                        congela="pezzo", lambda_c=lc)
    except AssertionError as e:
        fuori.update({"non_converge": True, "tick_alza": stato["t"],
                      "punto_fisso": stato["chi"] or "cs (tick.cs_al_centro)",
                      "lam_min": stato["lam_min"], "lam_min_su_lc": stato["lam_min"] / lc,
                      "msg": str(e)[:140]})
        return fuori
    finally:
        TK.tick_con_cs = vero
        EP.applica = vero_om
    cs = np.vstack([FP.cs(lam[0], lc, np.empty(lam.shape[1])).reshape(1, -1),
                    np.array(stato["cs"])])
    i0 = PR.inizio_finestra(acceso)
    bl_cs = PR.blocchi(cs, i0, PR.FINESTRE)
    bl_lam = PR.blocchi(lam, i0, PR.FINESTRE)
    anelli = {}
    for d in sorted(per):
        nodi = per[d]
        anelli[str(d)] = {"n": len(nodi),
                          "cs": [float(v) for v in np.mean(bl_cs[:, nodi], axis=1)],
                          "lam": [float(v) for v in np.mean(bl_lam[:, nodi], axis=1)]}
    fuori.update({
        "non_converge": False,
        "lam_min": float(np.min(lam)), "lam_min_su_lc": float(np.min(lam)) / lc,
        "cs_spread_max": float(np.max(np.max(cs, axis=1) - np.min(cs, axis=1))),
        "dlam_tick_max": float(np.max(np.abs(np.diff(lam, axis=0)))),
        "drho": drho, "dtot": dtot, "anelli": anelli})
    return fuori


def lancia(*arg):
    out = subprocess.run([sys.executable, os.path.abspath(__file__), "--braccio"]
                         + [str(a) for a in arg], capture_output=True)
    righe = out.stdout.decode("utf-8", "replace").strip().splitlines()
    assert out.returncode == 0 and righe, ("il braccio %r e' morto: %s"
                                           % (arg, out.stderr.decode("utf-8", "replace")
                                              [-600:]))
    return json.loads(righe[-1])


# =====================================================================================
#   LA LETTURA
# =====================================================================================
def _barra(v):
    import statica_protocollo as PR
    return PR.barra(v)


def delta(src, base, chiave, anelli_sel):
    """### `<delta>` per blocco ### **mediato sui nodi degli anelli scelti** (pesato)."""
    tot = sum(src["anelli"][d]["n"] for d in anelli_sel)
    v = np.zeros(len(src["anelli"][anelli_sel[0]][chiave]))
    for d in anelli_sel:
        n = src["anelli"][d]["n"]
        v += n * (np.array(src["anelli"][d][chiave]) - np.array(base["anelli"][d][chiave]))
    return v / tot


def cs_primo(lm, lc):
    return lc / (lm + lc) ** 2


def main(argv):
    if argv[:1] == ["--braccio"]:
        a = argv[1:]
        r = braccio(float(a[0]), float(a[1]), float(a[2]), int(a[3]), int(a[4]), a[5])
        sys.stdout.write(json.dumps(r) + "\n")
        return 0
    import _presidio
    _presidio.avvia(__file__)
    import _censimento_punti_fissi as CPF
    import composizione as CM
    import statica_protocollo as PR
    acceso = PR.T_ACCENSIONE[1]
    corto = argv[:1] == ["--corto"]
    # ### ⚠ **IL GIRO CORTO** *(`STANDARD 7`)*: un rapporto, due `x`, e i tick appena
    # ### sopra la finestra -- ### **collauda l'impianto, NON e' una misura.**
    cfg = {"rapporti": (1.0,) if corto else RAPPORTI,
           "tick": (PR.inizio_finestra(acceso) + 4 * PR.FINESTRE) if corto else PR.TICK,
           "x_scan": (0.01, 0.1) if corto else PR.X_SCAN,
           "tick_scan": ((PR.inizio_finestra(PR.T_SCAN) + 4 * PR.FINESTRE) if corto
                         else PR.TICK_SCAN)}
    print("=" * 100)
    print("`D4`: IL VERSO E IL PROFILO DI `cs`, COI TRE RAPPORTI -- il passo di oggi")
    print("=" * 100)
    print("### LA CONFIGURAZIONE INTERA")
    print("  il passo: la legge DEL MOTORE (SOSTITUISCI = False), cs dinamico"
          " (tick.tick_con_cs), impronta %s" % CM.IMPRONTA)
    print("  la scena: lati %s, VUOTO %.1f, SEME %d, RAGGIO %d, un grumo al nodo 0"
          % (PR.LATI, PR.VUOTO, PR.SEME, PR.RAGGIO))
    print("  la sorgente FOTOGRAFATA: congela = pezzo;  l'accensione: %d tick, UGUALE"
          " per tutti;  la finestra da T+%d, %d blocchi" % (acceso, PR.TRANSITORIO,
                                                          PR.FINESTRE))
    print("  i corsi principali: x = %.2f, %d tick, dtau %s;  la scansione: x in %s,"
          " %d tick, accensione %d, dtau %.2f%s"
          % (PR.X_RIF, cfg["tick"], list(PR.DTAU), list(cfg["x_scan"]), cfg["tick_scan"],
             PR.T_SCAN, PR.DTAU[0], "   ### GIRO CORTO: NON E' UNA MISURA" if corto else ""))
    lm = lambda_medio(PR.DTAU[0])
    print("  Lambda_medio = %.6f (dalla scena, UNA volta); Lambda_c = %s"
          % (lm, ", ".join("%.6f (rapporto %g)" % (r * lm, r) for r in RAPPORTI)))
    print("  i file del percorso del tick, sha1 dei BYTE:")
    for rel in sorted(CPF.chiusura_import(CPF.RADICI_TICK)):
        print("     %-36s %s" % (rel, hashlib.sha1(io.open(os.path.join(RADICE, rel),
                                                         "rb").read()).hexdigest()[:8]))
    print("  i bracci si salvano mentre corrono in %s" % os.path.relpath(JSONL, RADICE))
    sys.stdout.flush()
    piano = []
    for r in cfg["rapporti"]:
        for dt in PR.DTAU:
            piano.append((r, dt, PR.X_RIF, cfg["tick"], acceso, "base"))
            piano.append((r, dt, PR.X_RIF, cfg["tick"], acceso, "sorgente"))
    for r in cfg["rapporti"]:
        piano.append((r, PR.DTAU[0], 0.0, cfg["tick_scan"], PR.T_SCAN, "base"))
        for x in cfg["x_scan"]:
            piano.append((r, PR.DTAU[0], x, cfg["tick_scan"], PR.T_SCAN, "sorgente"))
    dove = JSONL + (".corto" if corto else "")
    io.open(dove, "w", encoding="utf-8").close()
    bracci = {}
    print("-" * 100)
    print("### I BRACCI (%d), uno per processo:" % len(piano))
    for k, arg in enumerate(piano, 1):
        t0 = time.time()
        b = lancia(*arg)
        bracci[arg] = b
        with io.open(dove, "a", encoding="utf-8") as f:
            f.write(json.dumps(b) + "\n")
        print("  %2d/%d  rapporto %-5g dtau %-5g x %-5g tick %-5d %-9s %s  min Lambda/Lc %.3f"
              "  [%.0f s]"
              % (k, len(piano), arg[0], arg[1], arg[2], arg[3], arg[5],
                 "### NON CONVERGE al tick %d [%s]" % (b["tick_alza"], b["punto_fisso"])
                 if b["non_converge"]
                 else "converge", b["lam_min_su_lc"], time.time() - t0))
        sys.stdout.flush()
    esito = leggi_e_giudica(bracci, lm, acceso, cfg)
    if corto:
        os.remove(dove)
    return esito


def leggi_e_giudica(bracci, lm, acceso, cfg):
    import statica_protocollo as PR
    grumo = None
    esiti = {"cala": [], "fallire": [], "lineare": []}
    # ---------------------------------------------------------- il caso che deve fallire
    print("-" * 100)
    print("### IL CASO CHE DEVE FALLIRE: SENZA sorgente, max - min di mot.cs a ogni tick")
    for arg, b in sorted(bracci.items()):
        if arg[5] != "base":
            continue
        if b["non_converge"]:
            print("  rapporto %-5g dtau %-5g tick %-5d  ### NON CONVERGE" % (arg[0], arg[1],
                                                                          arg[3]))
            continue
        ok = b["cs_spread_max"] == 0.0
        esiti["fallire"].append(ok)
        print("  rapporto %-5g dtau %-5g tick %-5d  max(max - min) = %.3e   %s"
              % (arg[0], arg[1], arg[3], b["cs_spread_max"],
                 "uniforme AL BIT -- PASSA" if ok else "### NON uniforme -- FALLISCE"))
    # ---------------------------------------------------------- CALA, e il profilo
    print("-" * 100)
    print("### `cs` CALA VICINO ALLA MATERIA? (x = %.2f, sui nodi del grumo r <= %d)"
          % (PR.X_RIF, PR.RAGGIO))
    profili = {}
    for r in cfg["rapporti"]:
        for dt in PR.DTAU:
            b0 = bracci[(r, dt, PR.X_RIF, cfg["tick"], acceso, "base")]
            b1 = bracci[(r, dt, PR.X_RIF, cfg["tick"], acceso, "sorgente")]
            if b0["non_converge"] or b1["non_converge"]:
                nc = b1 if b1["non_converge"] else b0
                print("  rapporto %-5g dtau %-5g  ### NON CONVERGE al tick %d [%s]: Lambda"
                      " min %.4f, Lambda_c %.4f (min Lambda/Lc %.3f)"
                      % (r, dt, nc["tick_alza"], nc["punto_fisso"], nc["lam_min"],
                         nc["lambda_c"], nc["lam_min_su_lc"]))
                continue
            dist = sorted(b1["anelli"], key=int)
            grumo = [d for d in dist if int(d) <= PR.RAGGIO]
            m, s = _barra(delta(b1, b0, "cs", grumo))
            ok = m < 0 and abs(m) >= 3 * s
            esiti["cala"].append(ok)
            print("  rapporto %-5g dtau %-5g  delta cs = %+.6e +- %.2e (%.1f barre)  %s"
                  "   min Lambda/Lc %.3f"
                  % (r, dt, m, s, abs(m) / s if s > 0 else float("nan"),
                     "CALA -- PASSA" if ok else "### FALLISCE", b1["lam_min_su_lc"]))
            profili[(r, dt)] = (b0, b1, dist)
    print("-" * 100)
    print("### IL PROFILO RADIALE delta cs(r) (media dei blocchi; tra parentesi le barre)")
    chiavi = sorted(profili)
    if chiavi:
        print("  %4s %5s  %s" % ("r", "nodi", "  ".join("%-24s" % ("rap %g dt %g" % k)
                                                       for k in chiavi)))
        dist = profili[chiavi[0]][2]
        for d in dist:
            celle = []
            for k in chiavi:
                b0, b1, _ = profili[k]
                m, s = _barra(delta(b1, b0, "cs", [d]))
                celle.append("%+.3e (%5.1f)" % (m, abs(m) / s if s > 0 else 0.0))
            print("  %4s %5d  %s" % (d, profili[chiavi[0]][1]["anelli"][d]["n"],
                                     "  ".join("%-24s" % c for c in celle)))
    # ---------------------------------------------------------- L2, informazione
    print("-" * 100)
    print("### IL CRITERIO DI USCITA DI `L2` (mappa sez.1), come INFORMAZIONE e non verdetto")
    for k in chiavi:
        b0, b1, dist = profili[k]
        fuori = []
        alone = 0
        for d in dist:
            m, s = _barra(delta(b1, b0, "cs", [d]))
            if s > 0 and abs(m) >= 3 * s:
                alone = max(alone, int(d))
            if int(d) > PR.RAGGIO and m < 0 and s > 0 and abs(m) >= 3 * s:
                fuori.append(int(d))
        print("  rap %-5g dt %-5g  (1) max|Lambda(t+1)-Lambda(t)|: sorgente %.3e, base %.3e"
              "   (2) l'alone: |delta cs| >= 3 barre fino a r = %d   (3) anelli FUORI dal"
              " grumo con cs che CALA a >= 3 barre: %d (%s)"
              % (k[0], k[1], b1["dlam_tick_max"], b0["dlam_tick_max"], alone, len(fuori),
                 ", ".join(str(q) for q in fuori[:8]) + (" ..." if len(fuori) > 8 else "")))
    # ---------------------------------------------------------- LINEARE
    print("-" * 100)
    print("### `delta cs` LINEARE IN `delta Lambda` PER x PICCOLO (dtau %.2f, sul grumo)"
          % PR.DTAU[0])
    for r in cfg["rapporti"]:
        lc = r * lm
        cp = cs_primo(lm, lc)
        b0 = bracci[(r, PR.DTAU[0], 0.0, cfg["tick_scan"], PR.T_SCAN, "base")]
        righe = []
        for x in cfg["x_scan"]:
            b1 = bracci[(r, PR.DTAU[0], x, cfg["tick_scan"], PR.T_SCAN, "sorgente")]
            if b0["non_converge"] or b1["non_converge"]:
                nc = b1 if b1["non_converge"] else b0
                print("  rapporto %-5g x %-5g  ### NON CONVERGE al tick %d [%s] (min"
                      " Lambda/Lc %.3f)" % (r, x, nc["tick_alza"], nc["punto_fisso"],
                                           nc["lam_min_su_lc"]))
                continue
            g = [d for d in b1["anelli"] if int(d) <= PR.RAGGIO]
            dc = delta(b1, b0, "cs", g)
            dl = delta(b1, b0, "lam", g)
            rb = (dc / dl) / cp
            mr, sr = _barra(rb)
            mdl = float(np.mean(dl))
            curv = abs(mdl) / (lm + lc)
            righe.append((x, mr, sr, mdl, curv))
            print("  rapporto %-5g x %-5g  <delta Lambda> = %+.4e  R = %.6f +- %.1e"
                  "   |R-1| = %.3e   curvatura %.3e"
                  % (r, x, mdl, mr, sr, abs(mr - 1), curv))
        if len(righe) >= 2:
            dev = [abs(q[1] - 1) for q in sorted(righe)]
            monot = all(dev[i] <= dev[i + 1] + 3 * sorted(righe)[i][2]
                        for i in range(len(dev) - 1))
            x0 = sorted(righe)[0]
            dentro = abs(x0[1] - 1) <= x0[4] + 3 * x0[2]
            ok = monot and dentro
            esiti["lineare"].append(ok)
            print("  rapporto %-5g  |R-1| non cresce quando x cala: %s;  al x = %g |R-1| ="
                  " %.3e <= curvatura %.3e + 3 barre %.1e: %s   -> %s"
                  % (r, "si" if monot else "### NO", x0[0], abs(x0[1] - 1), x0[4],
                     3 * x0[2], "si" if dentro else "### NO",
                     "LINEARE -- PASSA" if ok else "### FALLISCE"))
        else:
            print("  rapporto %-5g  ### NON DECIDIBILE: meno di due x convergono" % r)
    # ---------------------------------------------------------- i verdetti
    print("=" * 100)
    print("### I VERDETTI (sui bracci che convergono; i NON CONVERGE sono contati a parte)")
    tutti = True
    for k, che in (("fallire", "il caso che DEVE fallire: senza sorgente cs uniforme AL BIT"),
                   ("cala", "cs CALA vicino alla materia (>= 3 barre)"),
                   ("lineare", "delta cs LINEARE in delta Lambda per x piccolo")):
        v = esiti[k]
        stato = ("PASSA" if v and all(v) else
                 ("NON DECIDIBILE" if not v else "### FALLISCE"))
        tutti &= stato == "PASSA"
        print("  %-62s %d su %d   %s" % (che, sum(v), len(v), stato))
    nc = sorted(set((a[0], a[1], a[2], b["punto_fisso"]) for a, b in bracci.items()
                    if b["non_converge"]))
    print("  bracci NON CONVERGE (protezione a): %d  %s" % (len(nc), nc))
    print("### ⛔ NESSUNA SCELTA di Lambda_c: i numeri vanno nella voce, la decisione e' di Luca.")
    print("=" * 100)
    return 0 if tutti else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
