# -*- coding: utf-8 -*-
r"""**LA PROVA: IL SOLITONE SUL MASSIMO DI `B` A `Gamma`** *(UNA PROVA, NESSUNA MODIFICA AL NUCLEO; il mandato di Luca delle `11:51` del `2026-10-31`, sull'esito di `e92a7f9c`;
[[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il task history `doc/TASK_HISTORY/2026-10-31_massimo_di_B.md`)*:
### **lo stato di `_energia_del_legame.stato` con lo stato di Bloch del massimo di `B` a `Gamma` al posto di quello di `A` a `K`; `S1`, `N 1e6`, `s 0.15`, il congelato vero, `g 1`, `r 1`;**
### **`eps 0.5` (il PRINCIPALE) e `eps 0`, l'`eps` messo IN MEMORIA su `z["par"]`; Newton di `_livelli_piatti.newton`, invariato, con la scena a `eps` al posto di `LP.scena`.**

    python csv/_massimo_di_B.py --previsioni > doc/referti_l2/massimo_di_B/previsioni.txt
    python csv/_massimo_di_B.py --cerca e05 > doc/referti_l2/massimo_di_B/cerca_e05_L81.txt      # idem e0; con --L 120 se largo
    python csv/_massimo_di_B.py --breve e05 > doc/referti_l2/massimo_di_B/breve_e05.txt          # idem e0
    python csv/_massimo_di_B.py --lunga                 # un pezzo (eps 0.5); si ripete finche' dice "finita"
    python csv/_massimo_di_B.py --referto > doc/referti_l2/massimo_di_B.txt
"""
import contextlib
import itertools
import math
import os
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

import _chiudere_le_uscite as CU                               # noqa: E402
import _livelli_piatti as LP                                   # noqa: E402

S = LP.S
N = 1e6
R_, G_ = 1.0, 1.0               # ### i pesi di oggi (a_n = b_a = pi) e g 1 (S1 come oggi)
CASI = {"e05": 0.5, "e0": 0.0}  # ### l'eps della moneta; e05 il PRINCIPALE (Luca 11:51)
L_SCENA = LP.L_SCENA
L_GRANDE = 120
T_LUNGA = 40000                 # ### 6000 unita' di tempo a s 0.15
PEZZO = 4000
OGNI = LP.OGNI                  # ### il cuore, la larghezza, l'alone
OGNI_D = LP.OGNI_LUNGA_D        # ### |D| e le bande di D
ESAME = 40                      # ### le rotazioni per banda sui D dei 40 tick prima della fine del pezzo (l'esame di _scatola)
SOGLIA = 1e-2                   # ### la vita: il primo tau con |D|/|psi0| >= 1e-2 (decisa, MAPPA decisione 9)
SEME_LUCA = 1e-9
TOLL_CONTROLLO = 1e-12          # ### l'inviluppo per Q_K e la fase di K rifa' lo stato di A a K della scena
TOLL_BLOCH = 1e-10
TOLL_E0 = 1e-5                  # ### E0 della scena contro quello del tick ricomposto di _chiudere_le_uscite
TOLL_NORMA = LP.TOLL_NORMA
DIR_JSON = os.path.join(RADICE, "doc", "referti_l2", "massimo_di_B")
DIR_NPZ = os.path.join(RADICE, "db", "massimo_di_B")
_SCENA_LP = LP.scena            # ### quella vera, presa all'import: la sostituzione in memoria la chiama
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


# ====================================================================== LA SCENA E LO STATO
@contextlib.contextmanager
def scena(N_, L, eps):
    """### **La scena di `_livelli_piatti` con `z["par"]["eps"] = eps` in memoria** *(il dizionario e' della scena: `_energia_del_legame.stato` lo copia)*."""
    with _SCENA_LP(N_, L) as (rec, z, phi0, p):
        z["par"]["eps"] = eps
        yield rec, z, phi0, p


@contextlib.contextmanager
def newton_a(eps):
    """### **`LP.newton` invariato, con la scena a `eps` al posto di `LP.scena`;** ### **rimessa all'uscita.**"""
    LP.scena = lambda N_, L: scena(N_, L, eps)
    try:
        yield
    finally:
        LP.scena = _SCENA_LP


def bloch_B(z, phi0):
    """### **La coppia del livello piu' alto di `A(Gamma)`, base QR, la PRIMA colonna** *(come `coppia_K` per `A` a `K`)*: `(q, E0, la separazione dal livello sotto, il residuo, A)`."""
    import _dove_va_la_materia as DV
    import _triangoli_forza as TF
    A = DV.matrice(z, phi0, DV.AMP)
    G = A[0, 0]
    lam, V = np.linalg.eig(G)
    E = -np.angle(lam) / S
    o = np.argsort(E)
    top = [int(o[-2]), int(o[-1])]
    deg = float(abs(E[top[0]] - E[top[1]]))
    assert deg <= TF.TOLL_DEG, "il massimo di B a Gamma non e' doppio: %.2e" % deg
    Q = np.linalg.qr(V[:, top])[0]
    q = Q[:, 0]
    E0 = float(np.mean(E[top]))
    res = float(np.linalg.norm(G @ q - np.exp(-1j * E0 * S) * q))
    return q, E0, float(E[top].min() - E[o[-3]]), deg, res, A


def partenza(nome, L):
    """### **L'inviluppo** *(la norma per nodo dello stato di `A` a `K` della scena)* **per lo stato di Bloch di `B` a `Gamma`, normalizzato a `N`;** ### **e il controllo positivo.**"""
    import _triangoli_forza as TF
    eps = CASI[nome]
    with scena(N, L, eps) as (_rec, z, phi0, pK):
        n = z["inc"].n
        c = pK.reshape(n, 12)
        inv = np.linalg.norm(c, axis=1)
        QK = TF.coppia_K(0.0, S)[0]["Q"][:, 0]
        ri = inv[:, None] * QK[None, :] * np.exp(2j * np.pi * (z["m1"] + z["m2"]) / 3.0)[:, None]
        ri *= math.sqrt(N / float(np.sum(np.abs(ri) ** 2)))
        dK = float(np.linalg.norm(ri - c) / np.linalg.norm(c))
        q, E0, sep, deg, res, _A = bloch_B(z, phi0)
        pB = inv[:, None] * q[None, :]
        pB *= math.sqrt(N / float(np.sum(np.abs(pB) ** 2)))
        nn = abs(float(np.sum(np.abs(pB) ** 2)) / N - 1.0)
        return pB.reshape(pK.shape), {"controllo_K": dK, "E0": E0, "separazione": sep, "degenere": deg, "residuo_bloch": res, "norma": nn, "eps": eps, "L": L}


def nome_cerca(nome, L):
    return "cerca_%s_L%d" % (nome, L)


def stato(nome):
    """### **Lo stato che si usa:** quello di `L 120` se c'e' *(il caso largo)*, altrimenti `L 81`; ### **lo sha1 DEVE coincidere.**"""
    import _stato_fermo as SFM
    for L in (L_GRANDE, L_SCENA):
        fj = os.path.join(DIR_JSON, nome_cerca(nome, L) + ".json")
        if os.path.exists(fj):
            cj = LP.leggi(fj)
            with np.load(os.path.join(DIR_NPZ, "fermo_%s_L%d.npz" % (nome, L))) as fe:
                psi, mu = fe["psi_h"].copy(), float(fe["mu"])
            assert SFM.sha(psi) == cj["sha"], "lo stato di %s L %d sul disco NON e' quello della ricerca" % (nome, L)
            return psi, mu, cj
    return None


def misure(z, phi0, rec, psi):
    """### **`w`, il cuore `f_win` entro `w_in`, il picco, `alpha` del cuore e della coda** *(le righe del referto di `_livelli_piatti`)*."""
    import _congelato_lungo as CL
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    w0 = rec["larghezza"]
    with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
        w_in = DC.forma(z, w0)[0]
        z["st"]["psi_h"][...] = psi
        pt = CL.punto(z, 0, w_in, w0)
    _ra, am = LP.SL.anelli(z, psi, LP.FORMA)
    return {"w": pt["w"], "w_in": w_in, "f_win": pt["f_win"], "f_3w0": pt["f_3w0"], "picco": pt["picco"], "alpha_cuore": float(am[0]), "alpha_coda": float(am[LP.SL.R_MAX])}


# ====================================================================== (0) LE PREVISIONI
def altre(E0, g, sp, mu=None):
    """### **(n3)** `3 mu - F_i - F_j - F_k` in `[0, 3 g]`; ### **le coppie di onde dispersive:** **(c0)** libere, `2 mu`; **(c1)** una col legame, `2 mu - alpha`; **(c2)** tutte e due, `2 mu - 2 alpha`; ### tutto modulo `Omega` *(`CU.distanza`)*."""
    m0, m1 = (E0, E0 + g) if mu is None else (mu, mu)
    out = {}
    for tr in itertools.combinations_with_replacement(CU.PIATTE, 3):
        lo = sum(sp[p][0] for p in tr)
        hi = sum(sp[p][1] for p in tr)
        out["(n3) %s" % " + ".join(tr)] = CU.distanza((3 * m0 - hi, 3 * m1 - lo), (0.0, 3 * g))
    for c, d in itertools.combinations_with_replacement(CU.DISPERSIVE, 2):
        som = (sp[c][0] + sp[d][0], sp[c][1] + sp[d][1])
        for k, sott in (("c0", 0.0), ("c1", g), ("c2", 2 * g)):
            out["(%s) %s + %s" % (k, c, d)] = CU.distanza((2 * m0 - sott, 2 * m1), som)
    return out


def per_costruzione(k, c):
    """### **Le condizioni vere PER COSTRUZIONE:** la (n0) della banda di `E0` *(`mu` parte dal suo bordo)* e ### **la (c2) `c + c`: due quanti della banda col legame SONO il solitone.**"""
    return k in ("(n0) mu in %s" % c, "(c2) %s + %s" % (c, c))


def stampa_uscite(u, c):
    ap = [k for k, d in u.items() if d < 0 and not per_costruzione(k, c)]
    mm = min((d, k) for k, d in u.items() if not per_costruzione(k, c))
    print("      %s" % "; ".join("%s %+.4f%s" % (k, d, " (per costruzione)" if per_costruzione(k, c) else "") for k, d in u.items()))
    print("      ### %s; il margine minimo (senza quelle per costruzione) %s: %s" % (("APERTE: " + "; ".join(ap)) if ap else "TUTTE CHIUSE", mm[1], CU.giudizio(mm[0])))
    return ap, mm


def previsioni():
    fj = os.path.join(DIR_JSON, "previsioni.json")
    assert not os.path.exists(fj), fj
    print("### (0) LE PREVISIONI, PRIMA DI NEWTON: il tick libero di _chiudere_le_uscite (ricomposto) a s %g, r 1, g %g; J = [E0, E0 + g]; W %s; modulo Omega %.2f" % (S, G_, CU.W, CU.OMEGA))
    out = {}
    for nome, eps in CASI.items():
        lib = CU.Libero(eps)
        T = lib.tick(math.pi, math.pi)
        d = float(np.abs(T - lib.T_oggi).max())
        esito("DEVE PASSARE: %s (eps %g), il tick ricomposto ai pesi di oggi = il tick dei mezzi pezzi entro %g" % (nome, eps, LP.TOLL_RICOMPOSTO), d < LP.TOLL_RICOMPOSTO, "%.1e" % d)
        E = CU.BP.fasi(T, S)
        sp = CU.gruppi_di(E)
        E0 = float(E[0, 0, CU.BP.B_[-1]])
        esito("DEVE PASSARE: %s, il livello piu' alto di B a Gamma e' il MASSIMO di B sulla zona" % nome, E0 >= float(E[..., list(CU.BP.B_)].max()) - 1e-12, "E0 %+.5f, max %+.5f" % (E0, float(E[..., list(CU.BP.B_)].max())))
        dg = float(abs(E[0, 0, CU.BP.B_[0]] - E0))
        print("  --- %s, eps %g: E0 %+.5f (la coppia di B a Gamma a %.1e); la curvatura %+.4f; J [%+.5f, %+.5f]; le bande %s"
              % (nome, eps, E0, dg, CU.curvatura(E[..., CU.BP.B_[-1]], (0, 0), lib.L), E0, E0 + G_, "  ".join("%s [%+.5f, %+.5f]" % (k, v[0], v[1]) for k, v in sp.items())))
        u = CU.uscite(E0, G_, sp)
        u.update(altre(E0, G_, sp))
        print("    per ogni mu in J e alpha in [0, g]:")
        ap, mm = stampa_uscite(u, "B")
        print("    (c0) B + B: il margine e' 2 (mu - E0), zero al bordo basso di J: si rilegge al mu misurato")
        out[nome] = {"eps": eps, "E0": E0, "degenere": dg, "bande": {k: list(v) for k, v in sp.items()}, "uscite": u, "aperte": ap, "margine": [mm[1], mm[0]]}
    print("  ### LA PREVISIONE (Luca 11:51): nessun modo esponenziale.")
    os.makedirs(DIR_JSON, exist_ok=True)
    LP.scrivi_nuovo(fj, out)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


# ====================================================================== (1), (2) LO STATO DI PARTENZA E NEWTON
def cerca(nome, L):
    import _stato_fermo as SFM
    fj = os.path.join(DIR_JSON, nome_cerca(nome, L) + ".json")
    assert not os.path.exists(fj), fj
    eps = CASI[nome]
    p0, info = partenza(nome, L)
    print("### (1) LO STATO DI PARTENZA: %s, eps %g, L %d, N %.0e; l'inviluppo di S1 (quello di _energia_del_legame.stato) per la prima colonna QR della coppia di B a Gamma" % (nome, eps, L, N))
    esito("DEVE PASSARE: il controllo positivo -- l'inviluppo per Q_K e la fase di K rifa' lo stato di A a K della scena entro %g relativo" % TOLL_CONTROLLO, info["controllo_K"] < TOLL_CONTROLLO, "%.1e" % info["controllo_K"])
    esito("DEVE PASSARE: A(Gamma) q = e^{-i E0 s} q entro %g" % TOLL_BLOCH, info["residuo_bloch"] < TOLL_BLOCH, "%.1e" % info["residuo_bloch"])
    lib = CU.Libero(eps)
    E0_lib = float(CU.BP.fasi(lib.tick(math.pi, math.pi), S)[0, 0, CU.BP.B_[-1]])
    esito("DEVE PASSARE: E0 della scena = E0 del tick ricomposto di _chiudere_le_uscite entro %g" % TOLL_E0, abs(info["E0"] - E0_lib) < TOLL_E0, "%+.6f contro %+.6f" % (info["E0"], E0_lib))
    esito("DEVE PASSARE: la norma dello stato di partenza = N entro %g relativo" % TOLL_CONTROLLO, info["norma"] < TOLL_CONTROLLO, "%.1e" % info["norma"])
    print("  la coppia di B a Gamma: E0 %+.6f, degenere a %.1e, separata dal livello sotto di %.5f" % (info["E0"], info["degenere"], info["separazione"]))
    print("### (2) NEWTON (_livelli_piatti.newton invariato; il criterio di 26300537: residuo < %g entro %d passi)" % (LP.SB.TOLL_RES, LP.SB.MAX_NEWTON))
    with newton_a(eps):
        psi, mu, rf, storia, sec = LP.newton(R_, G_, N, p0, "%s-L%d" % (nome, L), LP.SB.MAX_NEWTON, L)
    with scena(N, L, eps) as (rec, z, phi0, _p):
        m_in = misure(z, phi0, rec, p0)
        m = misure(z, phi0, rec, psi)
    os.makedirs(DIR_NPZ, exist_ok=True)
    tmp = os.path.join(DIR_NPZ, "fermo_%s_L%d_tmp.npz" % (nome, L))
    np.savez(tmp, psi_h=psi, mu=mu)
    os.replace(tmp, os.path.join(DIR_NPZ, "fermo_%s_L%d.npz" % (nome, L)))
    largo = m["w"] > L * LP.FRAZ_LARGO
    riga = {"nome": nome, "eps": eps, "L": L, "N": N, "r": R_, "g": G_, "partenza": info, "mu": mu, "mu_meno_E0": mu - info["E0"], "residuo_finale": rf, "convergito": rf < LP.SB.TOLL_RES,
            "largo": largo, "sha": SFM.sha(psi), "storia": storia, "secondi": sec, "misure_partenza": m_in, "misure": m}
    LP.scrivi_nuovo(fj, riga)
    print("  %s L %d: %s (residuo %.3e), mu %+.9f (mu - E0 %+.5f); w %.3f (L/6 %.2f: %s), cuore f_win %.5f, picco %.2f; alpha del cuore %.5f (g %g), della coda %.5f"
          % (nome, L, "FERMO" if riga["convergito"] else "NON CONVERGE: lo stato migliore, dichiarato", rf, mu, mu - info["E0"], m["w"], L * LP.FRAZ_LARGO,
             "### OLTRE: L 120" if largo else "dentro", m["f_win"], m["picco"], m["alpha_cuore"], G_, m["alpha_coda"]))
    print("  la partenza: w %.3f, cuore %.5f, picco %.2f; la storia del residuo %s" % (m_in["w"], m_in["f_win"], m_in["picco"], " ".join("%.1e" % p["residuo"] for p in storia)))
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


# ====================================================================== (3) LE CORSE BREVI
def breve(nome):
    """### **Le righe di `_livelli_piatti.breve`, con lo stato e la scena di qui.**"""
    import _dove_va_la_materia as DV
    import _modo_al_variare_di_s as MS
    fj = os.path.join(DIR_JSON, "breve_%s.json" % nome)
    assert not os.path.exists(fj), fj
    psi0, mu, cj = stato(nome)
    eps, L = cj["eps"], cj["L"]
    with scena(N, L, eps) as (_rec, z, phi0, _p):
        Z = DV.autovettori(DV.matrice(z, phi0, DV.AMP))[1]
        n0 = float(np.linalg.norm(psi0))
        Q0, M0 = LP.ML.q_s(psi0)
        t_fine = int(round(LP.T_BREVE / S))
        ogni = int(round(LP.PASSO_BREVE / S))
        psi = psi0.copy()
        t3, nD3, t5, nD5, Ds, cons = [], [], [], [], {}, 0.0
        s0 = time.time()
        for t in range(1, t_fine + 1):
            psi = MS.tick(z, phi0, psi, LP.FORMA)
            if t % LP.OGNI_D == 0 or t % ogni == 0:
                D = np.exp(1j * mu * S * t) * psi - psi0
                nd = float(np.linalg.norm(D)) / n0
                if t % ogni == 0:
                    t3.append(t)
                    nD3.append(nd)
                    Q, M = LP.ML.q_s(psi)
                    cons = max(cons, abs(Q - Q0) / M0, abs(M - M0) / M0)
                if t % LP.OGNI_D == 0:
                    t5.append(t)
                    nD5.append(nd)
                    Ds[t] = D.astype(np.complex64).astype(np.complex128)
        sec = time.time() - s0
        print("  %s: %d tick in %.0f s; Q_S e M entro %.1e" % (nome, t_fine, sec, cons))
        riga = {"nome": nome, "eps": eps, "L": L, "r": R_, "g": G_, "N": N, "s": S, "sha": cj["sha"], "residuo": cj["residuo_finale"], "convergito": cj["convergito"], "mu": mu, "dn": cons,
                "t": t3, "nD": nD3, "t5": t5, "nD5": nD5, "secondi": sec}
        riga.update(LP.SL.giudica(riga))
        att = cj["residuo_finale"] / S
        riga["analisi"] = LP.ML.analizza(t5, nD5, sorted(Ds), Ds, S, psi0, LP.ML.Bande(Z, z["L"]), MS.Vista(z, psi0), lambda x: LP.FATTORE_DEROGA * att * max(x, S), nome)
    riga["forma_nuova"] = LP.forma_pendenze(np.array(t3, dtype=float) * S, np.array(nD3))
    LP.scrivi_nuovo(fj, riga)
    LP.stampa_breve(riga)
    LP.stampa_pendenze(riga["forma_nuova"], riga.get("forma"))


# ====================================================================== (4) LA CORSA LUNGA (eps 0.5)
LUNGA = "e05"
F_RIPRESA = os.path.join(DIR_NPZ, "lunga_%s.npz" % LUNGA)


def nome_pezzo(t0):
    return os.path.join(DIR_JSON, "lunga_%s_%05d.jsonl" % (LUNGA, t0))


def lunga():
    """### **Le righe di `_scatola.pezzo`, con lo stato e la scena di qui;** ### **lo stato di ripresa DEVE essere la fine del pezzo prima** *(sha1)*."""
    import _congelato_lungo as CL
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    psi0, mu, cj = stato(LUNGA)
    eps, L = cj["eps"], cj["L"]
    with scena(N, L, eps) as (rec, z, phi0, _p):
        w0 = rec["larghezza"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            w_in = DC.forma(z, w0)[0]
        ph, Z = DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        bande = LP.ML.Bande(Z, z["L"])
        E = ph / S
        n0 = float(np.linalg.norm(psi0))
        t0 = 0
        punti, dd = [], []
        if os.path.exists(F_RIPRESA):
            with np.load(F_RIPRESA) as dati:
                t0 = int(dati["t"])
                z["st"]["psi_h"][...] = dati["psi_h"]
            prec = LP.leggi(nome_pezzo(t0 - PEZZO))
            assert prec["sha_fine"] == SFM.sha(z["st"]["psi_h"]), "lo stato salvato NON e' quello della fine del pezzo prima"
        else:
            assert not os.path.exists(nome_pezzo(0)), "pezzi scritti ma nessuno stato di ripresa"
            z["st"]["psi_h"][...] = psi0
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                p = CL.punto(z, 0, w_in, w0)
            p["tau"] = 0.0
            punti.append(p)
        if t0 >= T_LUNGA:
            print("  la corsa lunga %s: finita" % LUNGA)
            return
        t1 = min(t0 + PEZZO, T_LUNGA)
        Ds = {}
        s0 = time.time()
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            for t in range(t0 + 1, t1 + 1):
                CL.avanza(z, phi0, 1)
                if t % OGNI == 0:
                    p = CL.punto(z, t, w_in, w0)
                    p["tau"] = t * S
                    punti.append(p)
                if t % OGNI_D == 0 or t > t1 - ESAME:
                    D = np.exp(1j * mu * S * t) * z["st"]["psi_h"] - psi0
                    if t % OGNI_D == 0:
                        c = bande.coeff(D)
                        pk = np.abs(c) ** 2
                        tot = float(pk.sum())
                        dd.append({"t": t, "nD": float(np.linalg.norm(D)) / n0, "bande": {gn: float(pk[..., list(idx)].sum()) / tot for gn, idx in bande.gruppi.items()}})
                    if t > t1 - ESAME:
                        Ds[t] = D
        sha_fine = SFM.sha(z["st"]["psi_h"])
        tmp = F_RIPRESA.replace(".npz", "_tmp.npz")
        np.savez(tmp, psi_h=z["st"]["psi_h"], t=t1)
        ts = sorted(Ds)
        rot = {gr: [bande.rotazione(Ds[a], Ds[b], (gr,), S) for a, b in zip(ts, ts[1:])] for gr in ("Ppi", "A", "P0", "B")}
        esame = {"rot": {gr: {"media": float(np.mean(v)), "dev": float(np.std(v))} for gr, v in rot.items()},
                 "E": {gr: float(np.mean(v)) + mu for gr, v in rot.items()},
                 "bande_libere": {gr: [float(E[..., list(idx)].min()), float(E[..., list(idx)].max())] for gr, idx in bande.gruppi.items()}}
        riga = {"nome": LUNGA, "eps": eps, "L": L, "N": N, "t0": t0, "t1": t1, "s": S, "mu": mu, "w0": w0, "w_in": w_in, "punti": punti, "D": dd, "esame": esame,
                "sha_fine": sha_fine, "secondi": time.time() - s0}
        LP.scrivi_nuovo(nome_pezzo(t0), riga)
        os.replace(tmp, F_RIPRESA)
    print("  la corsa lunga %s: tick %d -> %d, w/w_in %.5f, cuore %.5f, |D|/|psi0| %.3e (%s); rot %s (%.0f s)"
          % (LUNGA, t0, t1, punti[-1]["w"] / w_in, punti[-1]["f_win"], dd[-1]["nD"], " ".join("%s %.3f" % kv for kv in dd[-1]["bande"].items()),
             " ".join("%s %+.4f" % (k, v["media"]) for k, v in esame["rot"].items()), riga["secondi"]))


# ====================================================================== IL REFERTO
def referto():
    import _stato_fermo as SFM
    print("=" * 130)
    print("LA PROVA: IL SOLITONE SUL MASSIMO DI B A Gamma (Luca 11:51): S1, N %.0e, s %g, r 1 (a_n = b_a = pi), g %g, il congelato vero; eps 0.5 (PRINCIPALE) e 0" % (N, S, G_))
    print("  la configurazione: CASI %s L_SCENA %d L_GRANDE %d FRAZ_LARGO %.4f T_LUNGA %d PEZZO %d OGNI %d OGNI_D %d ESAME %d SOGLIA %g SEME_LUCA %g TOLL_CONTROLLO %g TOLL_BLOCH %g TOLL_E0 %g TOLL_NORMA %g;"
          " da _livelli_piatti: T_BREVE %g PASSO_BREVE %g OGNI_D %d FATTORE_DEROGA %g SIGMA_FORMA %g; da _strada_b_r: MAX_NEWTON %d TOLL_RES %g; W %s"
          % (CASI, L_SCENA, L_GRANDE, LP.FRAZ_LARGO, T_LUNGA, PEZZO, OGNI, OGNI_D, ESAME, SOGLIA, SEME_LUCA, TOLL_CONTROLLO, TOLL_BLOCH, TOLL_E0, TOLL_NORMA,
             LP.T_BREVE, LP.PASSO_BREVE, LP.OGNI_D, LP.FATTORE_DEROGA, LP.SIGMA_FORMA, LP.SB.MAX_NEWTON, LP.SB.TOLL_RES, CU.W))
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: (b1) esiste, nessun modo esponenziale nella corsa lunga, il cuore regge: la prima uscita chiusa dall'energia confermata (il limite superiore del tasso);"
          " (b2) esiste ma decade: quale uscita; (b3) non esiste un legato su B a Gamma con S1; (b4) altro; eps 0 contro 0.5")
    print("=" * 130)
    prev = LP.leggi(os.path.join(DIR_JSON, "previsioni.json"))
    print("### (0) LE PREVISIONI (previsioni.json, committate prima di Newton)")
    for nome, x in prev.items():
        print("  %s (eps %g): E0 %+.5f; aperte per ogni mu in J: %s; il margine minimo %s %.4f" % (nome, x["eps"], x["E0"], x["aperte"] or "nessuna", x["margine"][0], x["margine"][1]))
    print("-" * 130)
    print("### (1), (2) GLI STATI")
    stati = {}
    for nome, eps in CASI.items():
        for L in (L_SCENA, L_GRANDE):
            fj = os.path.join(DIR_JSON, nome_cerca(nome, L) + ".json")
            if not os.path.exists(fj):
                continue
            cj = LP.leggi(fj)
            with np.load(os.path.join(DIR_NPZ, "fermo_%s_L%d.npz" % (nome, L))) as fe:
                ok = SFM.sha(fe["psi_h"]) == cj["sha"]
            esito("DEVE PASSARE: %s L %d, lo stato sul disco = la ricerca (sha1)" % (nome, L), ok, cj["sha"][:8])
            pa = cj["partenza"]
            esito("DEVE PASSARE: %s L %d, il controllo positivo dello stato di A a K entro %g; A(Gamma) q entro %g; la norma entro %g" % (nome, L, TOLL_CONTROLLO, TOLL_BLOCH, TOLL_CONTROLLO),
                  pa["controllo_K"] < TOLL_CONTROLLO and pa["residuo_bloch"] < TOLL_BLOCH and pa["norma"] < TOLL_CONTROLLO, "%.1e %.1e %.1e" % (pa["controllo_K"], pa["residuo_bloch"], pa["norma"]))
            m, mi = cj["misure"], cj["misure_partenza"]
            print("  %s L %d: %s (residuo %.3e in %d passi), mu %+.9f, mu - E0 %+.5f; w %.3f (partenza %.3f; L/6 %.2f: %s), cuore %.5f (partenza %.5f), picco %.2f; alpha del cuore %.5f, della coda %.5f"
                  % (nome, L, "FERMO" if cj["convergito"] else "NON FERMO", cj["residuo_finale"], len(cj["storia"]) - 1, cj["mu"], cj["mu_meno_E0"], m["w"], mi["w"], L * LP.FRAZ_LARGO,
                     "OLTRE" if cj["largo"] else "dentro", m["f_win"], mi["f_win"], m["picco"], m["alpha_cuore"], m["alpha_coda"]))
            print("    la storia del residuo: %s" % " ".join("%.1e" % p["residuo"] for p in cj["storia"]))
            stati[nome] = cj
        if nome in stati:
            cj = stati[nome]
            x = prev[nome]
            sp = x["bande"]
            u = CU.uscite(None, G_, sp, mu=cj["mu"])
            u.update(altre(None, G_, sp, mu=cj["mu"]))
            print("    le uscite AL mu MISURATO (alpha in [0, g]):")
            ap, _mm = stampa_uscite(u, "B")
            cj["aperte_mu"] = ap
    print("-" * 130)
    print("### (3) LE CORSE BREVI (%g unita' di tempo)" % LP.T_BREVE)
    brevi = {}
    for nome in CASI:
        fj = os.path.join(DIR_JSON, "breve_%s.json" % nome)
        if not os.path.exists(fj):
            print("  %s: nessuna corsa breve" % nome)
            continue
        fr = LP.leggi(fj)
        esito("DEVE PASSARE: %s, Q_S e M conservate entro %g nella corsa breve" % (nome, TOLL_NORMA), fr["dn"] < TOLL_NORMA, "%.1e" % fr["dn"])
        print("  --- %s (eps %g, L %d)" % (nome, fr["eps"], fr["L"]))
        LP.stampa_breve(fr)
        LP.stampa_pendenze(fr["forma_nuova"], fr.get("forma"))
        brevi[nome] = fr
    print("-" * 130)
    print("### (4) LA CORSA LUNGA (%s)" % LUNGA)
    pz = sorted([LP.leggi(os.path.join(DIR_JSON, n)) for n in os.listdir(DIR_JSON) if n.startswith("lunga_%s_" % LUNGA)], key=lambda x: x["t0"])
    lunga_ = None
    if not pz:
        print("  nessuna corsa lunga")
    else:
        for x, y in zip(pz, pz[1:]):
            assert x["t1"] == y["t0"], ("un buco fra i pezzi", x["t1"], y["t0"])
        pts = [p for x in pz for p in x["punti"]]
        dd = [d for x in pz for d in x["D"]]
        dM = max(abs(p["M"] - pts[0]["M"]) / pts[0]["M"] for p in pts)
        esito("DEVE PASSARE: %s, M entro %g relativo nella corsa lunga" % (LUNGA, TOLL_NORMA), dM <= TOLL_NORMA, "%.1e" % dM)
        w_in = pz[0]["w_in"]
        fin = pz[-1]["t1"] >= T_LUNGA
        print("  %s: %d pezzi, tick %d -> %d%s" % (LUNGA, len(pz), pz[0]["t0"], pz[-1]["t1"], "" if fin else " (NON FINITA)"))
        for x in pz:
            q = [p for p in x["punti"]]
            print("  tick %5d -> %5d (tau %5.0f -> %5.0f): w/w_in %.5f -> %.5f; cuore %.5f -> %.5f; alone %.5f -> %.5f; |D|/|psi0| %.3e -> %.3e (%s); rot %s"
                  % (x["t0"], x["t1"], x["t0"] * S, x["t1"] * S, q[0]["w"] / w_in, q[-1]["w"] / w_in, q[0]["f_win"], q[-1]["f_win"], 1.0 - q[0]["f_3w0"], 1.0 - q[-1]["f_3w0"],
                     x["D"][0]["nD"], x["D"][-1]["nD"], " ".join("%s %.3f" % kv for kv in x["D"][-1]["bande"].items()), " ".join("%s %+.4f" % (k, v["media"]) for k, v in x["esame"]["rot"].items())))
        td = np.array([d["t"] * S for d in dd])
        nD = np.array([d["nD"] for d in dd])
        sopra = np.nonzero(nD >= SOGLIA)[0]
        vita = float(td[sopra[0]]) if len(sopra) else None
        T = float(td[-1])
        sup = {"il primo campione %.2e" % nD[0]: math.log(SOGLIA / nD[0]) / T, "1e-9 (Luca)": math.log(SOGLIA / SEME_LUCA) / T}
        if vita is not None:
            print("  ### LA VITA: |D|/|psi0| >= %g al tau %.1f" % (SOGLIA, vita))
        else:
            print("  ### LA VITA: |D|/|psi0| non arriva a %g in %.0f unita' di tempo (massimo %.3e); IL LIMITE SUPERIORE DEL TASSO gamma < ln(%g/seme)/%.0f: %s; vale il piu' largo, %.5f"
                  % (SOGLIA, T, float(nD.max()), SOGLIA, T, "; ".join("seme %s: %.5f" % kv for kv in sup.items()), max(sup.values())))
        print("  il cuore: %.5f a tau 0, %.5f a tau %.0f (A a K, 26300537: 0.630 -> 0.454 in 3000)" % (pts[0]["f_win"], pts[-1]["f_win"], pts[-1]["tau"]))
        lunga_ = {"finita": fin, "vita": vita, "sup": max(sup.values()), "cuore": (pts[0]["f_win"], pts[-1]["f_win"])}
    print("-" * 130)
    print("### LE LETTURE")
    for nome in CASI:
        cj = stati.get(nome)
        if cj is None:
            print("  %s: nessuno stato" % nome)
            continue
        esiste = cj["convergito"] and not cj["largo"]
        fr = brevi.get(nome)
        forma = fr["forma_nuova"]["forma"] if fr else None
        if not esiste:
            lt = "(b3) candidata: Newton %s, w %.3f (L/6 %.2f)" % ("converge" if cj["convergito"] else "NON converge", cj["misure"]["w"], cj["L"] * LP.FRAZ_LARGO)
        elif fr is None:
            lt = "nessuna corsa breve"
        elif forma == "esponenziale":
            lt = "(b2): la breve e' ESPONENZIALE -- quale uscita: le bande e le rotazioni di D qui sopra"
        elif nome == LUNGA and lunga_ is not None and lunga_["finita"]:
            lt = ("(b2): la corsa lunga arriva a %g al tau %.1f -- quale uscita: le bande e le rotazioni di D qui sopra" % (SOGLIA, lunga_["vita"]) if lunga_["vita"] is not None else
                  "(b1) se il cuore regge (%.5f -> %.5f; A a K 0.630 -> 0.454 in 3000): nessun modo esponenziale in 6000, gamma < %.5f" % (lunga_["cuore"][0], lunga_["cuore"][1], lunga_["sup"]))
        else:
            lt = "la breve: %s; %s" % (forma, "senza corsa lunga (il mandato la chiede solo a eps 0.5)" if nome != LUNGA else "la corsa lunga non finita")
        print("  %s (eps %g): %s" % (nome, CASI[nome], lt))
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--previsioni" in argv:
        previsioni()
    elif "--cerca" in argv:
        nome = argv[argv.index("--cerca") + 1]
        L = int(argv[argv.index("--L") + 1]) if "--L" in argv else L_SCENA
        cerca(nome, L)
    elif "--breve" in argv:
        breve(argv[argv.index("--breve") + 1])
    elif "--lunga" in argv:
        lunga()
    elif "--referto" in argv:
        referto()
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
