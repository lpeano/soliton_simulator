# -*- coding: utf-8 -*-
"""**LA SCOMPOSIZIONE DEL FATTORE `2.6`** *(mandato del guardiano, Luca 2026-09-28)*

*«ψ ricalcolato subito prima e subito dopo mitosi, sostituendo UN ingrediente alla volta (`w`,
`_mat(w)`, `φ`, archi e nodi del nato) per identificare quale produce il `2.6x`. Se il fattore viene
da uno stato a meta' costruzione, dillo: cambia la forma della cura.»*

**Il rilievo di fisica che orienta tutto:** le due formule sono **LA STESSA**
*(`satura(M(w) @ e^{i phi})`, `:4250` e `:5750`)*, quindi ### **una nascita su 12802 nodi non puo'
spostare il campo di TUTTI di `2.6x` se lo stato e' coerente.**

**I CRITERI sono fissati nel task history `9176216`, PRIMA di questi numeri.**

### ⚠ UNO SCOSTAMENTO DALLA LETTERA DEI CRITERI, E LO DICHIARO
Le varianti `V0`-`V5` erano scritte come *«`w` pre con struttura pre»* e simili. **Non sono tutte
definite**: prima della mitosi il grafo ha `m` archi e `n` nodi, dopo `m+1` e `n+1`, e un `w` POST
non entra in una struttura PRE. **Il task history lo prevedeva** *(«non e' sempre definito, e lo
dichiaro invece di far finta»)*. **Quindi si sostituisce UN ingrediente alla volta SUL GRAFO POST**,
che e' quello su cui il flash accade, e si misura `mean|psi|` ### **sui SOLI NODI VECCHI**:

| | variante | che cosa isola |
|---|---|---|
| **P0** | `psi` che `step` ha lasciato *(nessun ricalcolo)* | ### **il livello SENZA flash** |
| **P5** | ricalcolo POST completo | ### **il flash: deve riprodurre il fattore** |
| **Pw** | POST, ma `w` dei **soli archi sopravvissuti** riportato al valore PRE | ### **i PESI** |
| **Pf** | POST, ma `phi` dei **soli nodi vecchi** riportato al valore PRE | ### **la FASE** *(il rinculo)* |
| **Pn** | POST, ma **il nodo nato e i suoi archi messi a peso ZERO** | ### **il contributo del NATO** |

COMANDO:  python csv/_test_fork/_flash_scomposizione.py [--passi=42] [--sim=<percorso>]
USCITA:   0 se il banco e' sano (`P0` coincide con `psi` di `step`), 1 se no.
"""
import io
import json
import os
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)
import numpy as np  # noqa: E402
import _cli_flag  # noqa: E402
import _passo  # noqa: E402

VECCHIO = os.path.join(RADICE, "csv", "_seal_fork", "_sig_nascita_atomica", "_sim_e203f9a8.py")
FUORI = os.path.join(RADICE, "csv", "_seal_fork", "_sig_nascita_atomica")


def _psi_da(S, net, w, phi, n_vecchi):
    """`satura(M(w) @ (amp * e^{i phi}))`, **la formula, riusata dal modulo**."""
    amp = getattr(S, "SCALA_AMP", 1.0)
    F = net._mat(w) @ (amp * np.exp(1j * np.asarray(phi)))
    psi = net.satura(F)
    return psi, float(np.mean(np.abs(psi[:n_vecchi])))


def principale():
    passi, sim = 42, VECCHIO
    for x in sys.argv[1:]:
        if x.startswith("--passi="):
            passi = int(x.split("=", 1)[1])
        elif x.startswith("--sim="):
            sim = x.split("=", 1)[1]
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    import contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                            dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome="sim_scomp", sim=sim)
        # ⚠ `nmasse` e `sep` SI LEGGONO DA `a`, come fa il pilota: scriverli a mano e' l'errore
        #   che ha fatto misurare TUTTO sulla scena piccola (2107 nodi invece di 12802).
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
        net = S.net
    print("simulatore ....... %s" % os.path.basename(sim))
    print("esecutore ........ %s" % ("`esegui_passo`" if hasattr(S, "esegui_passo")
                                     else "ASSENTE -> fallback pre-T1 di `_passo.passo_pieno`"))
    print("scena ............ nmasse %d, sep %.4f  ->  n = %d, archi = %d"
          % (S._NMASSE_VIDEO["n"], S._NMASSE_VIDEO["sep"], net.n, len(net.i)))
    print("")
    print("### CRITERIO 5, IL PRIMO NUMERO: SCALA_AMP = %r" % getattr(S, "SCALA_AMP", None))
    print("    (`calcola_psi` moltiplica per SCALA_AMP, `step` no: se e' 1.0 la differenza fra le")
    print("     due formule e' INERTE, e il fattore va cercato altrove.)")
    print("")

    # ---- `pozzo_grafo` e' LINEARE in `I`? L'assunzione che io e la voce abbiamo ereditato ----
    with contextlib.redirect_stdout(io.StringIO()):
        _passo.passo_pieno(S, net)
    I = np.abs(net.psi[:net.n]) ** 2
    with contextlib.redirect_stdout(io.StringIO()):
        g1 = net.pozzo_grafo(I)[0]
        g2 = net.pozzo_grafo(2.0 * I)[0]
    r_lin = float(np.mean(np.abs(g2))) / max(float(np.mean(np.abs(g1))), 1e-300)
    print("### `pozzo_grafo` e' LINEARE in I?  mean|phi_g(2I)| / mean|phi_g(I)| = %.6f" % r_lin)
    print("    (2.000000 = lineare, e allora un %.3fx su phi_g e' la RADICE su |psi|)" % 2.631)
    lineare = abs(r_lin - 2.0) < 1e-6
    print("    ### ➜ %s" % ("LINEARE: il passaggio 2.6 -> 1.62 su |psi| E' LEGITTIMO." if lineare
                            else "NON LINEARE: il passaggio 2.6 -> 1.62 NON E' LEGITTIMO, e la "
                                 "voce PSI-FLASH lo assumeva."))
    print("")

    # ---- fino al passo della nascita, intercettando `mitosi` -------------------------------
    stato = {"passo": 1, "preso": None}
    _mit = net.mitosi

    def mitosi_spiata():
        p = stato["passo"]
        pre = {"n": int(net.n), "m": int(len(net.i)),
               "d": net.d.copy(), "eta": net.eta.copy(), "phi": net.phi.copy(),
               "i": net.i.copy(), "j": net.j.copy(),
               "psi_step": net.psi.copy() if hasattr(net, "psi") else None}
        nati = _mit()
        if stato["preso"] is None and int(net.n) > pre["n"]:
            stato["preso"] = {"passo": p, "nati": int(nati or 0), "pre": pre,
                              "post": {"n": int(net.n), "m": int(len(net.i)),
                                       "d": net.d.copy(), "eta": net.eta.copy(),
                                       "phi": net.phi.copy(), "i": net.i.copy(),
                                       "j": net.j.copy()}}
        return nati
    net.mitosi = mitosi_spiata

    t0 = time.time()
    for k in range(2, passi + 1):
        stato["passo"] = k
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(S, net)
        if stato["preso"]:
            print("### PRIMA NASCITA al passo %d: %d nati, n %d -> %d  (%.0f s dal via)"
                  % (stato["preso"]["passo"], stato["preso"]["nati"],
                     stato["preso"]["pre"]["n"], stato["preso"]["post"]["n"], time.time() - t0))
            break
    net.mitosi = _mit
    if not stato["preso"]:
        print("### NESSUNA NASCITA in %d passi: la scomposizione non si fa." % passi)
        return 1

    P, Q = stato["preso"]["pre"], stato["preso"]["post"]
    nv = P["n"]                                  # i NODI VECCHI
    print("")
    print("=" * 92)
    print("LA SCOMPOSIZIONE, su `mean|psi|` dei %d NODI VECCHI" % nv)
    print("=" * 92)

    # gli archi SOPRAVVISSUTI: la mitosi scrive `i = concatenate([i[keep], a, m])`, quindi i
    # primi `len(keep)` archi POST sono i PRE sopravvissuti, nello stesso ordine relativo.
    m_post = Q["m"]
    n_surv = None
    for cand in range(m_post, 0, -1):
        if np.array_equal(Q["i"][:cand], P["i"][np.isin(np.arange(P["m"]),
                                                        np.arange(P["m"]))][:0]):
            break
    # il numero di sopravvissuti si ricava dalla forma: m_post = (m_pre - k) + 2k = m_pre + k
    k_div = m_post - P["m"]
    n_surv = P["m"] - k_div
    print("  archi: PRE %d -> POST %d   ->  divisi %d, sopravvissuti %d"
          % (P["m"], m_post, k_div, n_surv))

    def _con(d, eta, i, j, phi, w_over=None, phi_over=None, zeri=None):
        """Mette lo stato, forza la ricostruzione della struttura, calcola `w` e `psi`."""
        net.d, net.eta, net.i, net.j, net.phi = d, eta, i, j, phi
        net._S = None                     # la struttura si RICOSTRUISCE da `i`/`j`
        net._grado() if hasattr(net, "_grado") else None
        w = net._pesi()
        if w_over is not None:
            w = np.asarray(w, float).copy()
            w[:len(w_over)] = w_over
        if zeri is not None:
            w = np.asarray(w, float).copy()
            w[zeri] = 0.0
        ph = phi if phi_over is None else phi_over
        return _psi_da(S, net, w, ph, nv)

    salva = dict(d=net.d, eta=net.eta, i=net.i, j=net.j, phi=net.phi, S=net._S)
    fuori = {}
    try:
        # P0: il livello che `step` ha lasciato, senza ricalcolare niente
        p0 = float(np.mean(np.abs(P["psi_step"][:nv]))) if P["psi_step"] is not None else None
        # il banco e' sano? `P0` ricalcolato sullo stato PRE deve coincidere con `psi` di `step`
        _, v0 = _con(P["d"], P["eta"], P["i"], P["j"], P["phi"])
        fuori["P0_psi_di_step"] = p0
        fuori["V0_ricalcolo_su_stato_PRE"] = v0
        sano = p0 is not None and abs(v0 - p0) / max(p0, 1e-300) < 1e-9
        print("  P0  `psi` che `step` ha lasciato ............ mean|psi| = %.6f" % p0)
        print("  V0  ricalcolo sullo STATO PRE .............. mean|psi| = %.6f   (rapporto %.9f)"
              % (v0, v0 / p0))
        print("      ### CRITERIO 4 -- il banco e' sano? %s" % ("SI" if sano else "NO: MI FERMO"))
        print("")
        # P5: il ricalcolo POST completo -- il flash
        _, p5 = _con(Q["d"], Q["eta"], Q["i"], Q["j"], Q["phi"])
        fuori["P5_ricalcolo_POST"] = p5
        print("  P5  ricalcolo POST completo (IL FLASH) ..... mean|psi| = %.6f   -> %.4f x P0"
              % (p5, p5 / p0))
        # Pw: pesi dei sopravvissuti riportati al PRE
        w_pre_surv = None
        _, _ = _con(P["d"], P["eta"], P["i"], P["j"], P["phi"])
        w_pre = net._pesi()
        keep_pos = np.arange(P["m"])
        w_pre_surv = np.asarray(w_pre, float)[:n_surv]
        _, pw = _con(Q["d"], Q["eta"], Q["i"], Q["j"], Q["phi"], w_over=w_pre_surv)
        fuori["Pw_pesi_al_PRE"] = pw
        print("  Pw  POST, pesi dei sopravvissuti = PRE ..... mean|psi| = %.6f   -> %.4f x P0"
              % (pw, pw / p0))
        # Pf: fase dei nodi vecchi riportata al PRE
        ph_mix = np.asarray(Q["phi"], float).copy()
        ph_mix[:nv] = P["phi"][:nv]
        _, pf = _con(Q["d"], Q["eta"], Q["i"], Q["j"], Q["phi"], phi_over=ph_mix)
        fuori["Pf_fase_al_PRE"] = pf
        print("  Pf  POST, fase dei nodi vecchi = PRE ....... mean|psi| = %.6f   -> %.4f x P0"
              % (pf, pf / p0))
        # Pn: il nato e i suoi archi a peso ZERO
        zeri = np.arange(n_surv, m_post)
        _, pn = _con(Q["d"], Q["eta"], Q["i"], Q["j"], Q["phi"], zeri=zeri)
        fuori["Pn_nato_a_peso_zero"] = pn
        print("  Pn  POST, archi del nato a peso ZERO ....... mean|psi| = %.6f   -> %.4f x P0"
              % (pn, pn / p0))
    finally:
        net.d, net.eta, net.i, net.j, net.phi = (salva["d"], salva["eta"], salva["i"],
                                                 salva["j"], salva["phi"])
        net._S = None

    print("")
    print("=" * 92)
    r = dict((k, (v / p0 if p0 else None)) for k, v in fuori.items() if v is not None)
    for k in ("P5_ricalcolo_POST", "Pw_pesi_al_PRE", "Pf_fase_al_PRE", "Pn_nato_a_peso_zero"):
        print("  %-26s %.4f x P0" % (k, r[k]))
    print("=" * 92)
    fuori.update({"rapporti_su_P0": r, "pozzo_lineare": lineare, "pozzo_rapporto_2I_su_I": r_lin,
                  "scala_amp": getattr(S, "SCALA_AMP", None), "banco_sano": bool(sano),
                  "passo_nascita": stato["preso"]["passo"], "nati": stato["preso"]["nati"],
                  "n_pre": nv, "n_post": Q["n"], "m_pre": P["m"], "m_post": m_post,
                  "archi_divisi": int(k_div), "archi_sopravvissuti": int(n_surv),
                  "blob_sim": os.path.basename(sim),
                  "nmasse": S._NMASSE_VIDEO["n"], "sep": S._NMASSE_VIDEO["sep"]})
    OUT = os.path.join(FUORI, "_flash_scomposizione.json")
    io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(
        json.dumps(fuori, indent=1, ensure_ascii=False, sort_keys=True, default=float))
    print("")
    print("scritto: " + OUT)
    return 0 if sano else 1


if __name__ == "__main__":
    sys.exit(principale())
