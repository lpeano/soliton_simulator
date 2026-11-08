# -*- coding: utf-8 -*-
"""`R60` -- **LE ROTAZIONI DEL RETICOLO COMMUTANO COL TICK DI OGGI**

> ### ⛔ **La decisione di Luca del `2026-11-08` `14:19` (v1):** `R180 x sigma_z` e `R60 x S60`
> nella suite, coi loro DEVE FALLIRE. **Il task history:**
> `doc/TASK_HISTORY/2026-11-08_zero_simmetrico_nel_nucleo.md`, sez. `2`; **la carta che li ha
> misurati per prima:** `csv/solitone/carta_r60.py` *(`doc/referti_l2/simmetria_r60.txt`)*.

## I CASI *(fissati prima)*

- **(s)** le mappe di `csv/_simmetrie_reticolo.py` danno la `S` DERIVATA: sulla parte lineare
  del tick *(senza i pezzi che leggono `rho`)* il nucleo delle `S` `12 x 12` che commutano ha
  dimensione `1` e coseno `1` con `P x S60` *(la seconda copia delle mappe CONFRONTA)*;
- **(a)** `R60 x S60` commuta col tick INTERO, `N_T` tick, sui semi dichiarati: `r <= SOGLIA`;
- **(b)** `R180 x sigma_z` lo stesso;
- **(c)** ### **DEVE FALLIRE:** `R60` con la sola permutazione *(`S = I` sullo spin)*;
- **(d)** ### **DEVE FALLIRE:** `R180` con `U = 1`.

**La scena:** `csv/_vuoto_vivo_B.scena` a `L 12` *(la corsa `BG-F-0.15`: `s 0.15`, `eps` della
corsa, `cs` spento, `U = I`)*, il vuoto `F3` da `_solitone_dal_fondo.fondo_con_fasi`.
**`SOGLIA = 2 x 14 x N_T x 10 eps`** *(due corse, `14` pezzi, al piu' `10` operazioni per
componente: la sez. `2` del task history della carta)*.

Gira con:  python primo_ordine/_collauda_r60.py
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import _presidio                                              # noqa: E402

CORSA = "BG-F-0.15"            # la scena delle corse dell'era 2 (corsa_accensione.NOME)
L_R60 = 12
SEMI = (1, 2)
N_T = 10
FLOP_PEZZO = 10
EPS = float(np.finfo(float).eps)
SOGLIA = 2 * 14 * N_T * FLOP_PEZZO * EPS
SV_REL = 1e-10
OK = [0, 0]


def esito(che, passa, nota):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-96s %s   %s" % (che[:96], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def main(argv):
    del argv
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _simmetrie_reticolo as SR
    import _solitone_dal_fondo as SDF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    import composizione as CM
    import tick as TK
    _presidio.avvia(__file__)
    _sol, vuoto, s = V.CORSE[CORSA]
    print("=" * 100)
    print("R60: LE ROTAZIONI DEL RETICOLO COMMUTANO COL TICK DI OGGI (L %d, %s, s %g, N_T %d, semi %s, SOGLIA %.3e)" % (L_R60, CORSA, s, N_T, SEMI, SOGLIA))
    print("=" * 100)
    ids = [i for i, _f, _t in CM.ORDINE]
    vero_L = V.L
    V.L = L_R60
    try:
        with V.scena(s, vuoto, V.EPS) as (rec, z, _phi0, _pK):
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                DC.forma(z, rec["larghezza"])
            st, inc, mot, par = z["st"], z["inc"], z["mot"], z["par"]
            L = int(z["L"])
            assert L == L_R60, (L, L_R60)
            ext = SR.estremita_per_direzione(inc, mot.geo.n)
            st["phi_h"][...] = SDF.fondo_con_fasi(inc, L, dict(SDF.FASI)["F3"])
            chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
            base = {k: st[k].copy() for k in chiavi}

            def rimetti():
                for k in chiavi:
                    st[k][...] = base[k]

            salta = tuple(i for i in ("CAMM-MATERIA-VUOTO", "CAMM-FASE-VUOTO") if i in ids)

            def lineare(x):
                st["psi_h"][...] = x
                mot.apri_tick()
                for idl, fr, _t in CM.ORDINE:
                    if idl in salta:
                        continue
                    nome, vp = TK.OPERATORE[idl]
                    mot.operatori[nome](st, par if vp else {}, fr)
                mot.chiudi_tick()
                return st["psi_h"].copy()

            def tick_n(x):
                st["psi_h"][...] = x[0]
                st["phi_h"][...] = x[1]
                with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                    for _ in range(N_T):
                        TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                return st["psi_h"].copy(), st["phi_h"].copy()

            def R(x, k, spin):
                nm = SR.mappa_nodi(L, k)
                return (SR.applica(x[0], ext, nm, SR.S_derivata(k, spin)),
                        SR.applica(x[1].reshape(-1, 1), ext, nm, SR.S_derivata(k, np.eye(1))).reshape(-1))

            # ---------------------------------------------------------- (s) la S derivata
            rng = np.random.default_rng(SEMI[0])
            xs = [rng.normal(size=st["psi_h"].shape) + 1j * rng.normal(size=st["psi_h"].shape) for _ in SEMI]
            nm1 = SR.mappa_nodi(L, 1)
            righe = []
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                for x in xs:
                    rimetti()
                    Tx = lineare(x)
                    col = []
                    for a in range(12):
                        for b in range(12):
                            E = np.zeros((12, 12))
                            E[a, b] = 1.0
                            rimetti()
                            col.append((lineare(SR.applica(x, ext, nm1, E)) - SR.applica(Tx, ext, nm1, E)).ravel())
                    righe.append(np.array(col).T)
            _u, sv, vh = np.linalg.svd(np.vstack(righe), full_matrices=False)
            dim = int(np.sum(sv <= sv[0] * SV_REL))
            Sd = SR.S_derivata(1, SR.S60)
            Sf = np.conj(vh[-1]).reshape(12, 12)
            cos_ = abs(np.vdot(Sd.ravel(), Sf.ravel())) / (np.linalg.norm(Sd) * np.linalg.norm(Sf))
            esito("(s) il nucleo di R60 sulla parte lineare ha dimensione 1 ed e' la S derivata (entro 1e-10)", dim == 1 and abs(cos_ - 1.0) <= 1e-10,
                  "dim %d, coseno %.15f" % (dim, cos_))
            # ---------------------------------------------------------- (a)-(d) il tick intero
            casi = (("(a) R60 x S60", 1, SR.S60, True), ("(b) R180 x sigma_z", 3, SR.SZ, True),
                    ("### (c) DEVE FALLIRE: R60 con la sola permutazione", 1, np.eye(2, dtype=complex), False),
                    ("### (d) DEVE FALLIRE: R180 con U = 1", 3, np.eye(2, dtype=complex), False))
            res = {c[0]: [] for c in casi}
            for seme in SEMI:
                rg = np.random.default_rng(seme)
                x = ((rg.normal(size=st["psi_h"].shape) + 1j * rg.normal(size=st["psi_h"].shape)) / math.sqrt(2.0), base["phi_h"].copy())
                nx = math.sqrt(float(np.sum(np.abs(x[0]) ** 2) + np.sum(np.abs(x[1]) ** 2)))
                rimetti()
                Tx = tick_n(x)
                for nome, k, spin, _deve in casi:
                    rimetti()
                    a = tick_n(R(x, k, spin))
                    b = R(Tx, k, spin)
                    res[nome].append(math.sqrt(float(np.sum(np.abs(a[0] - b[0]) ** 2) + np.sum(np.abs(a[1] - b[1]) ** 2))) / nx)
            rimetti()
            for nome, _k, _s, deve in casi:
                if deve:
                    esito("%s commuta col tick intero, %d tick, ogni seme: r <= %.2e" % (nome, N_T, SOGLIA), max(res[nome]) <= SOGLIA, "il massimo %.2e" % max(res[nome]))
                else:
                    esito("%s: r <= %.2e" % (nome, SOGLIA), min(res[nome]) > SOGLIA, "il minimo %.2e" % min(res[nome]))
    finally:
        V.L = vero_L
    print("=" * 100)
    print("R60: %d su %d  %s" % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
