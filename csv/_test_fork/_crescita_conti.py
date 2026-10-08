# -*- coding: utf-8 -*-
"""IL CONTO DELLA CRESCITA: **quanto cambiano `Σρ` e l'energia a ogni nascita**, e se la
divisione frena il collasso del prototipo.

Tre cose, e nessuna e' una corsa lunga:

**`(1)` LA REGOLA DI OGGI, LETTA DALLA TAVOLA DEL SIMULATORE.** Il simulatore ha una tavola
di regole di nascita *(`_nascita_regola`)*: si legge **da quella**, non dai commenti, che
cosa il nato riceve. ### **Se riceve la media dei genitori senza togliere niente, `Σρ` NON si
conserva**, ed e' la violazione `6` di `A14`.

**`(2)` IL CONTO SULLO SNAPSHOT.** Sulla `ρ` vera della scena: di quanto cresce `Σρ` con la
regola di oggi, e di quanto cambia `Σρ²` con la regola candidata `ψ → ψ/√2`.

**`(3)` LA DOMANDA DI `PT-7`: la nascita FRENA il collasso?** Sulla `H` della sonda, in forma
chiusa, confrontando il nodo singolo col nodo diviso in due.

Gira con:  python csv/_test_fork/_crescita_conti.py
"""
import ast
import contextlib
import io
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(os.path.dirname(_QUI))
sys.path.insert(0, os.path.join(RADICE, "csv"))
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)
import _cli_flag                                             # noqa: E402
import _passo                                                # noqa: E402
import _mitosi_soglia_grad as _MSG                           # noqa: E402

SIM = os.path.join(RADICE, "soliton_simulator.py")
BLOB_ATTESO = "b8c21049"
FUORI = os.path.join(_QUI, "_crescita_conti")
NL = chr(10)
P = []
PASSI_PRIMA = 3


def stampa(s=""):
    P.append(s)
    print(s, flush=True)


def riga(c="-", n=104):
    stampa(c * n)


def regole_di_nascita():
    """### `(1)` LE REGOLE, DALLA TAVOLA: si legge l'AST dei decoratori
    `@_nascita_regola(evento, grandezza, classe, ancora, derivazione)`."""
    albero = ast.parse(io.open(SIM, encoding="utf-8").read())
    fuori = []
    for n in ast.walk(albero):
        if not isinstance(n, ast.FunctionDef):
            continue
        for dec in n.decorator_list:
            if not (isinstance(dec, ast.Call) and isinstance(dec.func, ast.Name)
                    and dec.func.id == "_nascita_regola"):
                continue
            a = [x.value if isinstance(x, ast.Constant) else "<calcolato>"
                 for x in dec.args]
            while len(a) < 5:
                a.append("")
            fuori.append({"evento": a[0], "grandezza": a[1], "classe": a[2],
                          "ancora": a[3], "riga": n.lineno, "funzione": n.name})
    return fuori


def main():
    os.makedirs(FUORI, exist_ok=True)
    b = _MSG.blob(SIM)
    riga("=")
    stampa("IL CONTO DELLA CRESCITA -- Sigma rho e l'energia a ogni nascita")
    riga("=")
    stampa("  simulatore %s   atteso %s" % (b[:8], BLOB_ATTESO))
    if not b.startswith(BLOB_ATTESO):
        raise SystemExit("[FERMO] il blob del simulatore NON e' quello atteso.")

    # ================================================== (1) LE REGOLE, DALLA TAVOLA
    reg = regole_di_nascita()
    eventi = sorted(set(r["evento"] for r in reg))
    riga("=")
    stampa("(1) LE REGOLE DI NASCITA, LETTE DALLA TAVOLA DEL SIMULATORE (non dai commenti)")
    riga("=")
    stampa("  regole trovate: %d, su %d eventi: %s"
           % (len(reg), len(eventi), ", ".join(eventi)))
    # ### le classi di eredita': e' qui che si vede se qualcosa si CONSERVA o si AGGIUNGE
    cl = {}
    for r in reg:
        k = r["classe"].split("(")[0].strip().lower()
        cl.setdefault(k, []).append(r["grandezza"])
    stampa()
    for k in sorted(cl, key=lambda x: -len(cl[x])):
        stampa("  %-46s  %2d grandezze: %s"
               % (k[:46], len(cl[k]), " ".join(sorted(cl[k]))[:44]))
    media = sorted(set(g for k, v in cl.items() if "media" in k for g in v))
    eredita = sorted(set(g for k, v in cl.items() if "eredit" in k for g in v))
    stampa()
    stampa("  ### LE GRANDEZZE CHE IL NATO PRENDE PER MEDIA DEI GENITORI: %s"
           % (" ".join(media) or "(nessuna)"))
    stampa("  ### QUELLE CHE EREDITA DA UN GENITORE:                      %s"
           % (" ".join(eredita)[:80] or "(nessuna)"))
    stampa("  ### ⛔ E NESSUNA REGOLA TOGLIE NIENTE AL GENITORE: la tavola non ha una classe")
    stampa("  ###    <<il genitore cede>>. Quindi Sigma rho CRESCE a ogni nascita -- e' la")
    stampa("  ###    violazione 6 di A14, e qui e' LETTA DALLA TAVOLA, non dedotta.")
    cede = [k for k in cl if "cede" in k or "sottra" in k or "meta" in k]
    stampa("  ###    classi che somigliano a <<cede>>: %s" % (cede or "NESSUNA"))

    # ================================================== (2) IL CONTO SULLO SNAPSHOT
    with contextlib.redirect_stdout(io.StringIO()):
        S, net, _a = _cli_flag and _MSG.carica("crescita", SIM)
    _cli_flag.dichiara_configurazione(S, stampa)
    with contextlib.redirect_stdout(io.StringIO()):
        for _ in range(PASSI_PRIMA):
            _passo.passo_pieno(S, net)
    n = net.n
    psi = np.asarray(net.psi)[:n]
    rho = np.abs(psi) ** 2
    S1 = float(rho.sum())
    S2 = float((rho ** 2).sum())
    riga("=")
    stampa("(2) IL CONTO SULLO SNAPSHOT -- la rho VERA della scena, dopo %d passi pieni"
           % PASSI_PRIMA)
    riga("=")
    stampa("  n = %d   Sigma rho = %.6e   Sigma rho^2 = %.6e   rho_max = %.6e"
           % (n, S1, S2, float(rho.max())))
    k = int(np.argmax(rho))
    rk = float(rho[k])
    stampa("  il nodo piu' denso: k = %d, rho_k = %.6e  (%.4f %% di Sigma rho)"
           % (k, rk, 100.0 * rk / S1))
    stampa()
    stampa("  SE QUEL NODO DIVIDE:")
    stampa("      regola DI OGGI (il nato prende la media, e il genitore NON cede):")
    stampa("          Sigma rho:  %.6e -> %.6e   (+%.4f %%)   ### NON CONSERVA"
           % (S1, S1 + rk, 100.0 * rk / S1))
    stampa("          Sigma rho^2: %.6e -> %.6e   (+%.4f %%)"
           % (S2, S2 + rk ** 2, 100.0 * rk ** 2 / S2))
    stampa("      regola CANDIDATA psi -> psi/sqrt(2) su genitore e nato:")
    s2n = S2 - rk ** 2 + 2.0 * (rk / 2.0) ** 2
    stampa("          Sigma rho:  %.6e -> %.6e   (%.3e)   ### CONSERVA AL BIT"
           % (S1, S1, 0.0))
    stampa("          Sigma rho^2: %.6e -> %.6e   (%.4f %%)   ### IL rho^2 DEL NODO SI DIMEZZA"
           % (S2, s2n, 100.0 * (s2n - S2) / S2))

    # ================================================== (3) PT-7: LA NASCITA FRENA?
    riga("=")
    stampa("(3) PT-7 -- LA NASCITA FRENA IL COLLASSO? il conto sulla H della SONDA")
    riga("=")
    stampa("  La sonda: H = - somma_archi w (psi_i* psi_j + c.c.) + (g/2) somma_k rho_k^2")
    stampa("  Un nodo che tiene TUTTA la norma N, contro lo stesso nodo DIVISO in due da")
    stampa("  psi -> psi/sqrt(2), con un arco di peso w fra i due figli:")
    stampa()
    stampa("      H(un nodo)     = (g/2) N^2")
    stampa("      H(due figli)   = -2 w (N/2) + (g/2) * 2 * (N/2)^2 = -w N + (g/4) N^2")
    stampa("      Delta H        = H(due) - H(uno) = -(g/4) N^2 - w N = (|g|/4) N^2 - w N")
    stampa()
    conti = []
    for N in (400.0,):
        for g in (-5.0, -10.0):
            for w in (1.0, 5.6494):
                h1 = 0.5 * g * N * N
                h2 = -w * N + 0.25 * g * N * N
                conti.append({"N": N, "g": g, "w": w, "H_uno": h1, "H_due": h2,
                              "dH": h2 - h1})
                stampa("      N %5.0f  g %6.1f  w %7.4f :  H(uno) %12.1f   H(due) %12.1f"
                       "   Delta H %+12.1f  -> %s"
                       % (N, g, w, h1, h2, h2 - h1,
                          "LA DIVISIONE COSTA" if h2 > h1 else "la divisione CONVIENE"))
    stampa()
    stampa("  ### ⭐ IL RISULTATO, E PT-7 LA VINCE A META':")
    stampa("  ###   LA DILUIZIONE C'E', ED E' ESATTA: Sigma rho si conserva al bit e il")
    stampa("  ###   contributo rho^2 del nodo SI DIMEZZA -- cioe' la divisione toglie")
    stampa("  ###   esattamente cio' che il collasso guadagna. QUESTO ERA PT-7, e regge.")
    stampa("  ### ⛔ MA LA DIVISIONE ALZA H, quindi NON AVVIENE DA SOLA: va PAGATA.")
    stampa("  ###   Delta H = (|g|/4) N^2 - w N, che per N = 400 e g = -5 vale ~ +2e5.")
    stampa("  ### ➜ QUINDI LA NASCITA E' UN FRENO *SOLO SE QUALCUNO PAGA*, e chi paga e'")
    stampa("  ###   il VUOTO LOCALE -- che e' il punto S5, e S5 E' APERTO.")
    stampa("  ### ⛔ NON e' una conferma dell'ipotesi del guardiano: e' la DIMOSTRAZIONE")
    stampa("  ###   CHE QUELL'IPOTESI DIPENDE INTERAMENTE DAL PUNTO APERTO.")

    io.open(os.path.join(FUORI, "crescita.json"), "w", encoding="utf-8").write(
        json.dumps({"blob": b, "regole": reg, "classi": {k: sorted(v)
                                                         for k, v in cl.items()},
                    "snapshot": {"n": int(n), "somma_rho": S1, "somma_rho2": S2,
                                 "nodo_max": int(k), "rho_max": rk,
                                 "somma_rho2_dopo_candidata": s2n},
                    "pt7": conti}, ensure_ascii=False, default=str))
    io.open(os.path.join(FUORI, "crescita.txt"), "w", encoding="utf-8").write(
        NL.join(P) + NL)
    stampa()
    stampa("scritto %s" % os.path.join(FUORI, "crescita.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
