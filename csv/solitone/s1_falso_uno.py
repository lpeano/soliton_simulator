# -*- coding: utf-8 -*-
r"""**S1: IL FALSO-UNO DI F1-V** *(sul ramo laterale; Luca `2026-11-10` `19:37`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `28.1`)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/s1_falso_uno.py > doc/referti_l2/s1_falso_uno.txt

**(v0a)** il vuoto F3 a fase `1`, senza seme, F1, `1000` tick; **(v0b)** lo stesso con un seme bianco `1e-14` ortogonale a F3 *(la norma conservata)*; **(v0c)** `c(10000) F3` senza seme, `400` tick:
**DEVE ridare (v0) di H4 al bit** *(lo stato contro `h4_vuoto.corsa` rigirato, e le righe ai tick `200`, `400` contro il referto `h4_vuoto_disturbato.txt`, al carattere)*.
**Ogni `10` tick:** la rms di `Lambda`, `cs` min, la frazione sotto `1e-2`. **Il tasso:** la pendenza di `ln` della rms di `Lambda` sui campioni fra `1e-12` e `1e-4`. **Le letture (z1), (z2).**
"""
import hashlib
import io
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)
from solitone import carta_f1 as F1  # noqa: E402
from solitone import carta_f1_lunga as F1L  # noqa: E402
from solitone import carta_punto_fisso as CPF  # noqa: E402
from solitone import h4_vuoto as H4  # noqa: E402

OGNI = 10                      # ### Luca: ogni 10 tick
N_A, N_B, N_C = 1000, 1000, 400   # ### Luca: (v0a), (v0b) 1000 tick; (v0c) ai tick 200 e 400
TICK_C = (200, 400)            # ### Luca: (v0c) al bit ai tick 200 e 400
SEME_A = 1e-14                 # ### Luca: il seme 1e-14
UNIFORME = 1e-13               # ### Luca (z1): la rms di Lambda sotto 1e-13
FIN = (1e-12, 1e-4)            # ### mio (sez. 28.1): la finestra del tasso
TOLL_T = 0.05                  # ### Luca (z1): entro il 5%
REFERTO_H4 = os.path.join(os.path.dirname(os.path.dirname(_QUI)), "doc", "referti_l2", "h4_vuoto_disturbato.txt")
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-104s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:104], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return buono


def sha(a):
    return hashlib.sha1(np.ascontiguousarray(a).tobytes()).hexdigest()[:16]


def corsa(st, mot, par, lc, cs0, n_tick, fermi=()):
    """### **Il ciclo di `h4_vuoto.corsa` con F1** *(le stesse operazioni, nello stesso ordine)*, **campionato ogni `OGNI`**; `fermi`: i tick a cui si tiene `sha(phi)` e la riga di `h4_vuoto.stampa`."""
    import composizione as CM
    import flussi_parziali as FP
    import tick as TK
    fp = np.zeros(mot.inc.n)
    cs = cs0.copy()
    camp, foto = [], {}
    t0 = time.time()
    with F1.cs_primo_zero(True):
        for k in range(1, n_tick + 1):
            phi0 = st["phi_h"].copy()
            mot.cs = cs.copy()
            mot.lambda_c = float(lc)
            TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
            lam = mot.densita_vuoto(st).copy()
            L = FP.cs(lam, lc, fp).copy()
            r = 1.0 - np.exp(-F1.omega_v(phi0, st["phi_h"], mot.inc.nodo, mot.inc.n))
            cs = F1.rilassa(cs, L, r)
            if float(cs.min()) <= 0.0:
                raise F1L.Muro("tick %d: cs min %.3e <= 0" % (k, float(cs.min())))
            if k % OGNI == 0:
                camp.append({"t": k, "rms": float(np.std(lam)), "cs_min": float(cs.min()), "f2": float(np.mean(cs < 1e-2)), "cs_media": float(cs.mean()), "lam_media": float(lam.mean())})
            if k in fermi:
                c = H4.statistiche(cs, lam)
                riga = "    %6d %10.3e %10.3e %10.3e %10.3e %10.3e %9.2e %9.2e %10.3e %10.3e %20.10f %10.3e %10s" % (
                    k, c["cs_min"], c["q"][0], c["q"][1], c["q"][2], c["q"][3], c["f3"], c["f2"], c["lam_min"], c["lam_rms"],
                    float(np.sum(np.abs(st["phi_h"]) ** 2)), float(np.sum(np.abs(st["psi_h"]) ** 2)), "-")
                foto[k] = {"sha": sha(st["phi_h"]), "riga": riga}
    return {"camp": camp, "foto": foto, "s": time.time() - t0}


def stampa(nome, ris):
    print("  %s: %d campioni, %.0f s" % (nome, len(ris["camp"]), ris["s"]))
    print("    %6s %12s %12s %10s %14s %20s" % ("tick", "rms Lambda", "cs min", "f<1e-2", "cs medio", "Lambda medio"))
    for c in ris["camp"]:
        print("    %6d %12.4e %12.6e %10.3e %14.10f %20.15f" % (c["t"], c["rms"], c["cs_min"], c["f2"], c["cs_media"], c["lam_media"]))
    sys.stdout.flush()


def tasso(ris):
    """### la pendenza di `ln` della rms di `Lambda` sui campioni nella finestra `FIN`: `(tasso, n campioni, primo tick, ultimo tick)`."""
    tt = np.array([c["t"] for c in ris["camp"]], dtype=float)
    rr = np.array([c["rms"] for c in ris["camp"]])
    ok = (rr > FIN[0]) & (rr < FIN[1])
    if np.sum(ok) < 3:
        return float("nan"), int(np.sum(ok)), None, None
    return F1L.pendenza(tt[ok], np.log(rr[ok])), int(np.sum(ok)), int(tt[ok][0]), int(tt[ok][-1])


def main():
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    import flussi_parziali as FP
    from solitone import bordo as BO
    from solitone import corsa_accensione as CA
    for m in ("__init__", "corsa_accensione", "toro", "bordo", "carta_punto_fisso", "carta_f1", "carta_f1_lunga", "h4_vuoto"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("tick", "flussi_parziali", "energia_pesata"):
        _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab, omega, K = d["c"].copy(), float(d["omega"]), int(d["K"])
    c = BO.c_di(CPF.TICK_D4, tab, K, omega)
    t00 = time.time()
    print("=" * 130)
    print("S1 (sez. 28.1), il falso-uno di F1-V: F1 (q2), il bordo spento; ogni %d tick; la finestra del tasso %s; c(%d) = %+.12f %+.12fi" % (OGNI, FIN, CPF.TICK_D4, c.real, c.imag))
    print("=" * 130)
    with CA.con_L(CA.LCORSA.get(CPF.CORSA)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        phi_v = CA.vuoto_della_corsa(z, CPF.CORSA)
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, mot, par, inc = z["st"], z["mot"], z["par"], z["inc"]
        n = inc.n
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        st["psi_h"][...] = 0.0
        st["phi_h"][...] = phi_v
        lam0 = mot.densita_vuoto(st).copy()
        lc = float(np.mean(lam0)) * (1.0 - s) / s
        print("### Lambda_c = %.12f; Lambda del vuoto %.17g; s %g" % (lc, float(lam0.mean()), s))
        print("### F3 a fase 1: max |Im phi_v| = %.3e; max |Re phi_v| = %.17g; i valori distinti di phi_v: %d (%s)"
              % (float(np.max(np.abs(phi_v.imag))), float(np.max(np.abs(phi_v.real))), len(np.unique(phi_v)), ", ".join("%+.6f%+.6fi" % (x.real, x.imag) for x in np.unique(phi_v)[:8])))
        print("### c(10000) F3: i valori distinti %d; la parte immaginaria max %.6f" % (len(np.unique(c * phi_v)), float(np.max(np.abs((c * phi_v).imag)))))

        def vuoto_con(ph):
            for k in chiavi:
                st[k][...] = salvato[k]
            st["psi_h"][...] = 0.0
            st["phi_h"][...] = ph

        def cs_di():
            return FP.cs(mot.densita_vuoto(st), lc, np.zeros(n)).copy()
        ris = {}
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            # ------------------------------------------------------------ (v0a) F3 a fase 1, senza seme
            print("### LA CORSA (v0a): F3 a fase 1, senza seme, %d tick" % N_A)
            vuoto_con(phi_v)
            ris["a"] = corsa(st, mot, par, lc, cs_di(), N_A)
            stampa("(v0a)", ris["a"])
            # ------------------------------------------------------------ (v0b) lo stesso piu' un seme 1e-14
            rg = np.random.default_rng(CPF.SEME)
            dlt = rg.normal(size=phi_v.size) + 1j * rg.normal(size=phi_v.size)
            n3 = float(np.vdot(phi_v, phi_v).real)
            dlt -= (np.vdot(phi_v, dlt) / n3) * phi_v
            dlt *= SEME_A / float(np.sqrt(np.mean(np.abs(dlt) ** 2)))
            al = math.sqrt(1.0 - float(np.vdot(dlt, dlt).real) / n3)
            phb = al * phi_v + dlt
            print("### LA CORSA (v0b): F3 a fase 1 piu' il seme bianco: rms %.3e per estremita'; 1 - alpha %.3e; la norma %.10f contro %.10f; |<F3, delta>| / |F3|^2 %.2e; %d tick"
                  % (float(np.sqrt(np.mean(np.abs(dlt) ** 2))), 1.0 - al, float(np.vdot(phb, phb).real), n3, abs(complex(np.vdot(phi_v, dlt))) / n3, N_B))
            vuoto_con(phb)
            ris["b"] = corsa(st, mot, par, lc, cs_di(), N_B)
            stampa("(v0b)", ris["b"])
            # ------------------------------------------------------------ (v0c) c(10000) F3 senza seme, contro h4_vuoto.corsa e il referto
            print("### LA CORSA (v0c): c(10000) F3 senza seme, %d tick" % N_C)
            vuoto_con(c * phi_v)
            ris["c"] = corsa(st, mot, par, lc, cs_di(), N_C, fermi=TICK_C)
            stampa("(v0c)", ris["c"])
            righe_ref = {}
            with io.open(REFERTO_H4, encoding="utf-8") as f:
                dentro = False
                for riga in f:
                    if riga.startswith("### LA CORSA (v0)"):
                        dentro = True
                    elif riga.startswith("### LA CORSA (v1)"):
                        dentro = False
                    if dentro:
                        p = riga.split()
                        if p and p[0].isdigit() and int(p[0]) in TICK_C:
                            righe_ref[int(p[0])] = riga.rstrip("\n")
            print("### (v0c) contro h4_vuoto.corsa (il codice di (v0), rigirato a %s tick) e contro il referto %s" % (TICK_C, os.path.basename(REFERTO_H4)))
            for t in TICK_C:
                vuoto_con(c * phi_v)
                H4.corsa(st, mot, par, lc, cs_di(), t, True)
                sh = sha(st["phi_h"])
                print("    tick %d: sha(phi) S1 %s, h4_vuoto.corsa %s" % (t, ris["c"]["foto"][t]["sha"], sh))
                print("      la riga di S1:    %s" % ris["c"]["foto"][t]["riga"])
                print("      la riga del referto: %s" % righe_ref.get(t, "### MANCA"))
                esito("(v0c) tick %d: lo stato phi di S1 = quello di h4_vuoto.corsa AL BIT" % t, sh == ris["c"]["foto"][t]["sha"])
                esito("(v0c) tick %d: la riga = quella di (v0) nel referto di H4, AL CARATTERE" % t, righe_ref.get(t) == ris["c"]["foto"][t]["riga"])
            esito("(v0c) il controllo sa dire di no: la riga del tick %d contro quella del tick %d del referto" % TICK_C, righe_ref.get(TICK_C[1]) == ris["c"]["foto"][TICK_C[0]]["riga"], deve=False)
    print("-" * 130)
    ta, na, a0, a1 = tasso(ris["a"])
    tb, nb, b0, b1 = tasso(ris["b"])
    tc, nc, c0, c1 = tasso(ris["c"])
    rms_a = max(c_["rms"] for c_ in ris["a"]["camp"])
    print("  (v0a): la rms di Lambda massima %.3e (al tick %d); alla fine %.3e" % (rms_a, max(ris["a"]["camp"], key=lambda c_: c_["rms"])["t"], ris["a"]["camp"][-1]["rms"]))
    for nome, t_, nn, p0, p1 in (("(v0a)", ta, na, a0, a1), ("(v0b)", tb, nb, b0, b1), ("(v0c)", tc, nc, c0, c1)):
        print("  %s: il tasso (ln della rms di Lambda, i campioni fra %g e %g) %s per tick, su %d campioni (dal tick %s al %s)" % (nome, FIN[0], FIN[1], "%.5f" % t_ if t_ == t_ else "-", nn, p0, p1))
    rel = abs(tb / tc - 1.0) if (tb == tb and tc == tc) else float("nan")
    print("  (v0b) contro (v0c): il rapporto dei tassi %.5f (lo scarto %.4f; la soglia %g); (v0c) contro il 0.158 di 27.11: %.4f" % (tb / tc if tc == tc else float("nan"), rel, TOLL_T, tc / 0.158 if tc == tc else float("nan")))
    z1a = rms_a < UNIFORME
    z1b = rel == rel and rel <= TOLL_T
    print("  (z1) i due pezzi: (v0a) uniforme (la rms sotto %g per %d tick) %s; (v0b) col tasso di (v0) entro il %g%% %s" % (UNIFORME, N_A, z1a, 100 * TOLL_T, z1b))
    if z1a and z1b:
        print("  LA LETTURA: (z1) IL FALSO-UNO E' CONFERMATO: senza seme il vuoto F3 a fase 1 resta uniforme; con un seme di %g cresce col tasso di (v0): l'instabilita' c'era anche in T2, senza seme" % SEME_A)
    else:
        print("  LA LETTURA: (z2) non (z1): si scrive senza interpretare")
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
