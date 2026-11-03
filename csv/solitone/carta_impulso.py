# -*- coding: utf-8 -*-
r"""**L'IMPULSO DELLA PARTENZA: UN ARTEFATTO NOSTRO?** *(Luca `2026-11-03` `14:06`; il task history `doc/TASK_HISTORY/2026-11-03_impulso_partenza.md`)*:
### **sulla carta, sullo stato di partenza di BG-F-0.15** *(lo stesso di `TP1000` e `TF3`)*, **col vuoto `F0` e con `F3`.**
    python csv/solitone/carta_impulso.py > doc/referti_l2/impulso_partenza.txt
### **(p1)** l'impulso medio rispetto a `Gamma` *(`k . d = arg C_d`, `C_d = sum_e conj(psi[e]) . psi[T_d e]`)* e la corrente di materia totale `J = M dX/dt` *(un tick congelato)*;
### **(p2)** le stesse per lo stato ruotato di `180` gradi; ### **(p3)** il centro dopo `1`, `10`, `100` tick a vuoto CONGELATO; ### **(p4)** il ruotato uguale allo stato a meno di una
fase, per `U` in `{1, sigma_x, sigma_y, sigma_z}` sulle due componenti; la commutazione del tick congelato con la rotazione, per gli stessi `U`.
### **I DEVE:** `P0` lo stato e' quello di `TP1000` *(`mu`)*; `P0-C` l'arco `k` e' del nodo `k // 3` *(l'estremita' `2k` sul nodo, `2k + 1` sul vicino lungo l'asse `k % 3`)*;
`K+`, `K-` il controllo positivo dell'impulso *(`e^{i k0 . r}`, e il suo ruotato)*; `K-F` *(deve fallire)* lo stato senza spinta ridà `k0`; `R2` la rotazione due volte e' l'identita'; `V-F` *(deve fallire)* il tick congelato su `1.1 F0` uguale a quello
su `F0` *(il vuoto entra nel tick)*. ### **La rotazione:** attorno al centro d'inversione del reticolo piu' vicino al centro della densita' *(un nodo o il punto medio di un arco)*;
### **`U` lo decide la commutazione** *(le corse del ruotato solo per le `U` che commutano)*.
### **UN FALSO-ZERO, dichiarato prima:** l'impulso canonico di `inv(cella) x q` *(`inv` reale, `q` uguale su ogni cella)* e' nullo per costruzione.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

TICK = (1, 10, 100)            # ### (p3) Luca 14:06: dopo 1, 10, 100 tick a vuoto congelato
TOLL_K = 1e-9                  # ### K+, K-: arg C_d contro k0 . d (il task history, sez. 2)
TOLL_UGUALE = 1e-12            # ### (p4), la commutazione: come freccia_F0 (TOLL_UGUALE, TOLL_TICK)
SIGMA = {"1": np.eye(2, dtype=complex), "sx": np.array([[0, 1], [1, 0]], dtype=complex), "sy": np.array([[0, -1j], [1j, 0]], dtype=complex),
         "sz": np.array([[1, 0], [0, -1]], dtype=complex)}

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-120s %s   %s" % (che[:120], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def assi(inc, L):
    """### **`P0-C`:** l'arco `k` e' del nodo `k // 3`, l'estremita' `2k` sul nodo, `2k + 1` sul vicino lungo l'asse `k % 3`; `(vero, gli assi (d1, d2))`."""
    k = np.arange(inc.m)
    v, w = inc.nodo[0::2], inc.nodo[1::2]
    ok = inc.m == 3 * inc.n and bool(np.all(v == k // 3))
    dd = []
    for a in range(3):
        m = k % 3 == a
        d1 = ((w[m] // L - v[m] // L + L // 2) % L) - L // 2
        d2 = ((w[m] % L - v[m] % L + L // 2) % L) - L // 2
        ok = ok and bool(np.all(d1 == d1[0])) and bool(np.all(d2 == d2[0]))
        dd.append((int(d1[0]), int(d2[0])))
    return ok, dd


def nodo_di(L, m1, m2):
    return (m1 % L) * L + (m2 % L)


def trasla(inc, L, dd, d):
    """### **`T_d` sulle estremita':** l'estremita' dell'arco `(v, a)` va in quella dell'arco `(v + d, a)`, lo stesso lato."""
    v = np.arange(inc.n)
    tv = nodo_di(L, v // L + d[0], v % L + d[1])
    k = np.arange(inc.m)
    k2 = 3 * tv[k // 3] + k % 3
    e = np.empty(2 * inc.m, dtype=int)
    e[0::2], e[1::2] = 2 * k2, 2 * k2 + 1
    return e


def rotazione(inc, L, dd, m2):
    """### **`R180` attorno al centro d'inversione `m2 / 2`** *(`m -> m2 - m`, `m2` intero: un nodo o il punto medio di un arco)*: `out[dove[e]] = psi[e]`. L'arco `(v, a)` *(da `v` a `v + d_a`)* va nell'arco da `R v` a `R v - d_a`,
    cioe' l'arco `(R(v + d_a), a)` ROVESCIATO: l'estremita' su `v` va nella testa, quella su `v + d_a` nella coda."""
    k = np.arange(inc.m)
    v = k // 3
    a = k % 3
    d = np.array(dd)[a]
    rv = nodo_di(L, m2[0] - (v // L + d[:, 0]), m2[1] - (v % L + d[:, 1]))
    k2 = 3 * rv + a
    dove = np.empty(2 * inc.m, dtype=int)
    dove[0::2], dove[1::2] = 2 * k2 + 1, 2 * k2
    return dove


def applica(x, dove, U=None):
    out = np.empty_like(x)
    out[dove] = x if U is None else x @ U.T
    return out


def impulso(psi, inc, L, dd, tr):
    """### **`(k, args)`:** `args[a] = arg C_d` per i tre assi; `k` *(cartesiano)* dai minimi quadrati su `k . d = arg C_d`."""
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    args = []
    for e in tr:
        C = complex(np.sum(np.conj(psi) * psi[e]))
        args.append(math.atan2(C.imag, C.real))
    D = np.array([d[0] * A1 + d[1] * A2 for d in dd])
    k = np.linalg.lstsq(D, np.array(args), rcond=None)[0]
    return k, args


def centro(z, psi):
    import _energia_del_legame as EL
    from solitone import toro as TO
    L = z["L"]
    st = dict(z["st"])
    st["psi_h"] = psi
    rho, _l = EL.densita(z["inc"], st)
    v = np.arange(z["inc"].n)
    c1, c2, _x, _y = TO.centro(rho, v // L, v % L, L)
    return np.array([c1, c2]), rho


def sposta(c, c0, L):
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    d = ((c - c0 + 0.5 * L) % L) - 0.5 * L
    return d[0] * A1 + d[1] * A2


def vettore(v):
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    n = math.hypot(*v)
    cs = tuple(float(np.dot(v, a) / (n * math.hypot(*a))) if n > 0 else float("nan") for a in (A1, A2, A1 + A2))
    return "|.| %.4e a %+8.2f gradi, cos A1 / A2 / A1+A2 %+.3f / %+.3f / %+.3f" % (n, math.degrees(math.atan2(v[1], v[0])) if n > 0 else float("nan"), *cs)


def main(argv):
    del argv
    import _presidio
    import _modo_al_variare_di_s as MS
    import _solitone_dal_fondo as SD
    import _vuoto_vivo_B as V
    from solitone import carta_deriva as CD
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    for m in ("__init__", "toro", "corsa_accensione", "carta_deriva"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    sol, _vuoto, s = V.CORSE[CA.NOME]
    print("=" * 130)
    print("L'IMPULSO DELLA PARTENZA (Luca 2026-11-03 14:06): %s (sol %s, s %g, eps %g); TICK %s TOLL_K %g TOLL_UGUALE %g; la forma del tick congelato %s"
          % (CA.NOME, sol, s, V.EPS, TICK, TOLL_K, TOLL_UGUALE, V.LP.FORMA))
    print("  le letture di Luca, scritte prima: (q1) corrente e impulso nulli entro l'arrotondamento, l'inviluppo simmetrico: la partenza e' innocente; (q2) non nulli, verso -A1")
    print("  (circa): la spinta la diamo noi; (q3) non nulli in un'altra direzione: si scrive. ### UN FALSO-ZERO dichiarato: l'impulso CANONICO di inv x q e' nullo per costruzione")
    print("=" * 130)
    testa = V.LP.leggi(os.path.join(CA.dir_json("TP1000"), CA.nomi("TP1000")[0]))
    with V.scena(s, "fondo", V.EPS) as (_rec, z, phi0, pK):
        inc, L = z["inc"], z["L"]
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}

        def rimetti():
            for k, v in salvato.items():
                z["st"][k][...] = v

        p0, info = V.partenza(sol, z, phi0, pK, s)
        rimetti()
        esito("DEVE PASSARE: P0 lo stato di partenza e' quello di TP1000 (mu al bit di quello del primo pezzo)", info["mu"] == testa["info"]["mu"], "mu %.15f" % info["mu"])
        ok_a, dd = assi(inc, L)
        esito("DEVE PASSARE: P0-C l'arco k e' del nodo k // 3 (2k sul nodo, 2k+1 sul vicino lungo un asse fisso per k % 3)", ok_a, "gli assi (d1, d2) %s" % dd)
        print("  ### la riga v di reshape(n, 12) (protetto.inviluppo) = le 6 estremita' dei tre archi IN AVANTI di v, lungo %s: UNA CELLA ORIENTATA, non il nodo" % dd)
        vuoti = {"F0": phi0, "F3": SD.fondo_con_fasi(inc, L, tuple(dict(SD.FASI)["F3"]))}
        c0, rho0 = centro(z, p0)
        m2 = (int(round(2 * c0[0])), int(round(2 * c0[1])))
        print("  il centro della densita' di partenza (indici) (%.6f, %.6f); la rotazione di 180 gradi attorno al centro d'inversione piu' vicino (%.1f, %.1f) (lo scarto %+.3e, %+.3e)"
              % (c0[0], c0[1], 0.5 * m2[0], 0.5 * m2[1], c0[0] - 0.5 * m2[0], c0[1] - 0.5 * m2[1]))
        inv = np.linalg.norm(p0.reshape(inc.n, 12), axis=1) ** 2
        v_ = np.arange(inc.n)
        ci1, ci2, _x, _y = TO.centro(inv, v_ // L, v_ % L, L)
        print("  ### il centro dell'INVILUPPO (la riga v di reshape(n, 12) messa sul nodo v) (%.6f, %.6f); la densita' sui nodi meno l'inviluppo: %s"
              % (ci1, ci2, vettore(sposta(c0, np.array([ci1, ci2]), L))))
        tr = [trasla(inc, L, dd, d) for d in dd]
        dove = rotazione(inc, L, dd, m2)
        x = np.arange(2 * inc.m, dtype=float)
        esito("DEVE PASSARE: R2 la rotazione due volte e' l'identita' (al bit)", bool(np.all(applica(applica(x, dove), dove) == x)), "")
        # ------------------------------------------------------------ il tick congelato legge il vuoto? (il controllo positivo) e F0 contro F3
        uno = {}
        for nv, phv in list(vuoti.items()) + [("F0 x 1.1", 1.1 * phi0)]:
            rimetti()
            z["st"]["phi_h"][...] = phv
            uno[nv] = MS.tick(z, phv, p0, V.LP.FORMA)
        rimetti()
        esito("DEVE FALLIRE: V-F il tick congelato sul vuoto F0 scalato di 1.1 (|phi| diverso) e' uguale a quello su F0 (il vuoto ENTRA nel tick)",
              not np.array_equal(uno["F0"], uno["F0 x 1.1"]), "lo scarto %.3e" % (np.linalg.norm(uno["F0"] - uno["F0 x 1.1"]) / np.linalg.norm(uno["F0"])))
        print("  ### F0 CONTRO F3 (|phi| uguale, le fasi diverse): un tick congelato dallo stato di partenza uguale AL BIT? %s (lo scarto %.3e)"
              % (np.array_equal(uno["F0"], uno["F3"]), np.linalg.norm(uno["F0"] - uno["F3"]) / np.linalg.norm(uno["F0"])))
        # ------------------------------------------------------------ (p1), (p2): l'impulso; il controllo positivo
        m1n = (inc.nodo // L).astype(float)
        spinta = np.exp(2j * math.pi * m1n / L)[:, None]
        atteso = [2 * math.pi * d[0] / L for d in dd]
        k_p, a_p = impulso(p0, inc, L, dd, tr)
        k_b, a_b = impulso(p0 * spinta, inc, L, dd, tr)
        k_r, a_r = impulso(applica(p0 * spinta, dove), inc, L, dd, tr)
        k_pr, a_pr = impulso(applica(p0, dove), inc, L, dd, tr)
        esito("DEVE PASSARE: K+ lo stato per e^{i k0 . r} (k0 . A1 = 2 pi / L) ridà arg C_d = k0 . d entro %g" % TOLL_K,
              max(abs(a - b) for a, b in zip(a_b, atteso)) <= TOLL_K, "args %s, attesi %s" % (["%+.12f" % a for a in a_b], ["%+.12f" % a for a in atteso]))
        esito("DEVE PASSARE: K- il suo ruotato di 180 gradi ridà -k0 . d entro %g" % TOLL_K, max(abs(a + b) for a, b in zip(a_r, atteso)) <= TOLL_K,
              "args %s" % ["%+.12f" % a for a in a_r])
        esito("DEVE FALLIRE: K-F lo stato SENZA la spinta ridà k0 . d entro %g" % TOLL_K, max(abs(a - b) for a, b in zip(a_p, atteso)) > TOLL_K,
              "args %s" % ["%+.3e" % a for a in a_p])
        print("-" * 130)
        print("### (p1) L'IMPULSO MEDIO DELLO STATO DI PARTENZA, rispetto a Gamma (k = 0): arg C_d per gli assi %s = %s" % (dd, ["%+.3e" % a for a in a_p]))
        print("    k = (%+.3e, %+.3e): %s;  il passo di k sul toro 2 pi / L = %.4e" % (k_p[0], k_p[1], vettore(k_p), 2 * math.pi / L))
        print("### (p2) IL RUOTATO DI 180 GRADI: arg C_d %s; k = (%+.3e, %+.3e)  (il controllo positivo: %s -> %s)"
              % (["%+.3e" % a for a in a_pr], k_pr[0], k_pr[1], vettore(k_b), vettore(k_r)))
        # ------------------------------------------------------------ (p4) la commutazione: decide U (la simmetria del tick, non una scelta)
        print("-" * 130)
        print("### (p4) LO STATO CONTRO IL SUO RUOTATO (a meno di una fase), E LA COMMUTAZIONE DEL TICK CONGELATO CON R180, per U sulle due componenti")
        rr = applica(rho0, nodo_di(L, m2[0] - np.arange(inc.n) // L, m2[1] - np.arange(inc.n) % L))
        print("    la sola densita' per nodo: |rho(R v) - rho(v)| / |rho| = %.4e" % (np.linalg.norm(rr - rho0) / np.linalg.norm(rho0)))
        simm = []
        for nu, U in SIGMA.items():
            y = applica(p0, dove, U)
            c = complex(np.vdot(p0, y) / np.vdot(p0, p0))
            sc = float(np.linalg.norm(y - c * p0) / np.linalg.norm(p0))
            riga = "    U %-2s: |R psi - c psi| / |psi| = %.4e (c = %+.6f %+.6fi)" % (nu, sc, c.real, c.imag)
            comm = []
            for nv, phv in vuoti.items():
                rimetti()
                z["st"]["phi_h"][...] = phv
                b = applica(MS.tick(z, phv, p0, V.LP.FORMA), dove, U)
                rimetti()
                rph = applica(phv, dove)
                z["st"]["phi_h"][...] = rph
                a = MS.tick(z, rph, y, V.LP.FORMA)
                comm.append(float(np.linalg.norm(a - b) / np.linalg.norm(b)))
                riga += "; commuta su %s: %.4e" % (nv, comm[-1])
            print(riga)
            if max(comm) <= TOLL_UGUALE:
                simm.append(nu)
        rimetti()
        print("    ### LE U PER CUI R180 E' UNA SIMMETRIA DEL TICK CONGELATO (entro %g, su F0 e F3): %s" % (TOLL_UGUALE, simm or "NESSUNA"))
        # ------------------------------------------------------------ (p1), (p3): la corrente, i tick congelati
        print("-" * 130)
        print("### (p1), (p3) IL CENTRO A VUOTO CONGELATO (_modo_al_variare_di_s.tick, LP.FORMA): J = M dX/dt; la velocita' per 1000 unita' di tempo")
        M = float(rho0.sum())
        vel = {}
        for nv, phv in vuoti.items():
            casi = [("lo stato", (p0, phv))] + [("il ruotato (U = %s)" % nu, (applica(p0, dove, SIGMA[nu]), applica(phv, dove))) for nu in simm]
            for quale, (psi_in, ph_in) in casi:
                rimetti()
                z["st"]["phi_h"][...] = ph_in
                psi = psi_in.copy()
                ci, _r = centro(z, psi)
                t = 0
                for n in TICK:
                    while t < n:
                        psi = MS.tick(z, ph_in, psi, V.LP.FORMA)
                        t += 1
                    c, _r = centro(z, psi)
                    X = sposta(c, ci, L)
                    v1000 = X / (n * s) * 1000.0
                    vel[(nv, quale, n)] = v1000
                    print("    %s %-20s dopo %3d tick (tempo %7.3f): lo spostamento %s; v per 1000 %s%s"
                          % (nv, quale, n, n * s, vettore(X), vettore(v1000), ("; J = M dX/dt = %s" % vettore(M * X / s)) if n == 1 else ""))
        rimetti()
        for n_ in ("TP1000", "TF3"):
            tt, X, ww, fl, T_acc, _che, _R = CD.dati(n_)
            r = CD.finestre(n_, tt, X, ww, fl, 0.0, 1000.0, 1000.0, False)
            print("    accanto: %s, il primo blocco 0 .. 1000 della corsa (il vuoto vivo): v %.3f per 1000 a %+.2f gradi" % (n_, r[0][2], r[0][3]))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


if __name__ == "__main__":
    main(sys.argv[1:])
