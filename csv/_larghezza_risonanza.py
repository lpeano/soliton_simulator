# -*- coding: utf-8 -*-
r"""**LA LARGHEZZA DELLA RISONANZA** *(UNA DIAGNOSI, NON UNA CURA; i mandati di Luca delle `14:51` e delle `17:15` del `2026-10-29`; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]];
i task history `doc/TASK_HISTORY/2026-10-29_larghezza_risonanza.md`, `doc/TASK_HISTORY/2026-10-29_larghezza_stati_fermi.md`)*: ### **uno strumento di DIAGNOSI, mai nel nucleo.**
### **La mappa spostata: il tick di `S1` a `s 0.15`, poi le componenti sulle piatte** *(`P0`, `Ppi`: gli autovettori del tick libero, per impulso)* **moltiplicate per `e^{-i delta_p s}`:**
### **`ph_p` sale di `delta_p` per unita' di tempo; lo scarto della coppia di `delta_P0 + delta_Ppi`.**
### **Per ogni spostamento lo stato fermo della mappa spostata** *(Newton, per continuazione lungo tre catene)*, **poi la corsa da quello stato.**
*(Il referto delle `14:51`, col riferimento ruotato: `git checkout e679e2ea`.)*

    python csv/_larghezza_risonanza.py --cerca <nome>          # uno stato; i nomi: STATI
    python csv/_larghezza_risonanza.py --referto > doc/referti_l2/larghezza_stati_fermi.txt
"""
import io
import json
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

CASO = "S1_s0.150"
P0 = (6, 7, 8, 9)
PPI = (0, 1, 2, 3)
# ### (nome, delta_P0, delta_Ppi, la catena), nell'ordine della catena
STATI = (("stessa+0.05", 0.05, 0.05, "piu"), ("stessa+0.2", 0.2, 0.2, "piu"), ("stessa+0.8", 0.8, 0.8, "piu"), ("soloP0+0.8", 0.8, 0.0, "piu"),
         ("stessa-0.05", -0.05, -0.05, "meno"), ("stessa-0.2", -0.2, -0.2, "meno"), ("stessa-0.8", -0.8, -0.8, "meno"),
         ("opposte0.8", 0.8, -0.8, "opposte"))
MAX_NEWTON = 30
TOLL_RES = 1e-9
T_FIS = 180.0
T_DA_FIS = 60.0
PASSO_FIS = 3.0
TASSO_DFB = 0.15108            # ### dfb5ab7e, s 0.15
TOLL_DFB = 1e-3
TOLL_NORMA = 1e-10
DIR_NPZ = os.path.join(RADICE, "db", "larghezza")
DIR_JSON = os.path.join(RADICE, "doc", "referti_l2", "larghezza")
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


class Spostamento:
    """### **Le componenti piatte moltiplicate per `e^{-i delta_p s}`** *(per impulso: `fft2`, `Z(k)^H`, la fase, `Z(k)`, `ifft2`)*."""

    def __init__(self, Z, L, s, d_p0, d_ppi):
        self.Z, self.L = Z, L
        self.f = np.ones(12, dtype=complex)
        self.f[list(P0)] = np.exp(-1j * d_p0 * s)
        self.f[list(PPI)] = np.exp(-1j * d_ppi * s)

    def __call__(self, psi_h):
        L = self.L
        f = np.fft.fft2(psi_h.reshape(L, L, 12), axes=(0, 1))
        c = np.einsum("abji,abj->abi", self.Z.conj(), f) * self.f
        g = np.fft.ifft2(np.einsum("abij,abj->abi", self.Z, c), axes=(0, 1))
        return g.reshape(psi_h.shape)

    def matrice(self, A):
        """### **`Z diag(f) Z^H A(k)`**: il tick libero seguito dallo spostamento, per impulso *(per il precondizionatore)*."""
        S = np.einsum("abij,abkj->abik", self.Z * self.f, self.Z.conj())
        return np.einsum("abik,abkl->abil", S, A)


def stato(nome):
    return [x for x in STATI if x[0] == nome][0]


def carica(nome):
    """### **Lo stato, `mu`, il `.json`, e se lo sha1 coincide** *(`None` se non c'e')*."""
    import _stato_fermo as SFM
    fj = os.path.join(DIR_JSON, "cerca_%s.json" % nome)
    if not os.path.exists(fj):
        return None
    cj = json.loads(io.open(fj, encoding="utf-8").read())
    fe = np.load(os.path.join(DIR_NPZ, "fermo_%s.npz" % nome))
    return fe["psi_h"].copy(), float(fe["mu"]), cj, SFM.sha(fe["psi_h"]) == cj["sha"]


def partenza(nome):
    """### **Lo stato convergito piu' vicino** *(distanza euclidea su `(delta_P0, delta_Ppi)`)* **fra `delta 0` e gli stati gia' risolti della stessa catena.**"""
    import _modo_al_variare_di_s as MS
    _n, d0, d1, cat = stato(nome)
    cand = [("delta0", 0.0, 0.0)]
    for x in STATI:
        if x[0] == nome:
            break
        if x[3] == cat:
            c = carica(x[0])
            if c is not None and c[3] and c[2]["convergito"]:
                cand.append((x[0], x[1], x[2]))
    best = min(cand, key=lambda c: math.hypot(c[1] - d0, c[2] - d1))
    if best[0] == "delta0":
        psi, mu, cj, ok = MS.carica(CASO)
        assert ok, "lo stato a delta 0 NON e' quello di dfb5ab7e"
        return best[0], psi, mu, cj["sha"]
    psi, mu, cj, _ok = carica(best[0])
    return best[0], psi, mu, cj["sha"]


def cerca(nome):
    """### **Newton sulla mappa spostata** *(il metodo di `_modo_al_variare_di_s.cerca`; il precondizionatore `Z diag(f) Z^H A(k) e^{-i alpha(0) s}`)*."""
    from scipy.sparse.linalg import LinearOperator, gmres
    import _diagnosi_s4 as D
    import _dove_va_la_materia as DV
    import _modo_al_variare_di_s as MS
    import _stato_fermo as SFM
    fj = os.path.join(DIR_JSON, "cerca_%s.json" % nome)
    if os.path.exists(fj):
        print("  %s: il .json c'e' gia' (%s): non si ricalcola" % (nome, fj))
        return
    _n, d0, d1, cat = stato(nome)
    _c, forma, s, N = MS.caso(CASO)
    da, p0, mu_da, sha_da = partenza(nome)
    print("  %s: dP0 %+.3f dPpi %+.3f, la catena %s; la partenza %s (sha1 %s, mu %+.9f)" % (nome, d0, d1, cat, da, sha_da[:8], mu_da))
    sys.stdout.flush()
    with D.configura(forma, s, N):
        _rec, z, phi0, _p = MS.scena(forma, s, N)
        A0 = DV.matrice(z, phi0, DV.AMP)
        _ph, Z = DV.autovettori(A0)
        L = MS.L
        sp = Spostamento(Z, L, s, d0, d1)
        A = sp.matrice(A0) * np.exp(-1j * MS.ALPHA0[forma] * s)
        n = z["inc"].n
        Nn = float(np.sum(np.abs(p0) ** 2))
        fo = p0.shape
        m = p0.size

        def T(psi):
            return sp(MS.tick(z, phi0, psi, forma))
        lam = complex(np.vdot(p0, T(p0)) / np.vdot(p0, p0))
        mu = -math.atan2(lam.imag, lam.real) / s

        def da_x(x):
            return (x[:m] + 1j * x[m:2 * m]).reshape(fo), float(x[2 * m])

        def F(x):
            psi, mu_ = da_x(x)
            R = (T(psi) - np.exp(-1j * mu_ * s) * psi).ravel() / math.sqrt(Nn)
            return np.concatenate([R.real, R.imag, [(float(np.sum(np.abs(psi) ** 2)) - Nn) / Nn]])

        def residuo(psi, mu_):
            return float(np.linalg.norm(T(psi) - np.exp(-1j * mu_ * s) * psi) / np.linalg.norm(psi))

        x = np.concatenate([p0.ravel().real, p0.ravel().imag, [mu]])
        F0 = F(x)
        storia = [{"passo": 0, "residuo": residuo(p0, mu), "mu": mu, "gmres": 0, "dimezzamenti": 0}]
        print("  %s: passo 0, residuo %.3e, mu %+.9f" % (nome, storia[0]["residuo"], mu))
        sys.stdout.flush()
        s0 = time.time()
        for it in range(1, MAX_NEWTON + 1):
            if storia[-1]["residuo"] < TOLL_RES:
                break
            nx = float(np.linalg.norm(x))
            B = np.linalg.inv(A - np.exp(-1j * float(x[2 * m]) * s) * np.eye(12))
            conti = [0]

            def prec(y):
                c = (y[:m] + 1j * y[m:2 * m]).reshape(n, 12)
                f = np.fft.fft2(c.reshape(L, L, 12), axes=(0, 1))
                g = np.fft.ifft2(np.einsum("abij,abj->abi", B, f), axes=(0, 1)).reshape(-1)
                return np.concatenate([g.real, g.imag, [y[2 * m]]])

            def jv(y):
                v = prec(y)
                nv = float(np.linalg.norm(v))
                if nv == 0.0:
                    return np.zeros_like(v)
                h = MS.H_REL * (1.0 + nx) / nv
                conti[0] += 1
                return (F(x + h * v) - F(x - h * v)) / (2.0 * h)
            Aop = LinearOperator((2 * m + 1, 2 * m + 1), matvec=jv, dtype=float)
            y, _info = gmres(Aop, -F0, rtol=MS.GMRES_RTOL, restart=MS.GMRES_RESTART, maxiter=MS.GMRES_MAXITER)
            dx = prec(y)
            nf0 = float(np.linalg.norm(F0))
            passo, k = 1.0, 0
            while True:
                xn = x + passo * dx
                Fn = F(xn)
                if float(np.linalg.norm(Fn)) < nf0 or k >= MS.DIMEZZA:
                    break
                passo *= 0.5
                k += 1
            x, F0 = xn, Fn
            psi, mu = da_x(x)
            storia.append({"passo": it, "residuo": residuo(psi, mu), "mu": mu, "gmres": conti[0], "dimezzamenti": k})
            print("  %s: passo %d, residuo %.3e, mu %+.9f, GMRES %d, dimezzamenti %d (%.0f s)" % (nome, it, storia[-1]["residuo"], mu, conti[0], k, time.time() - s0))
            sys.stdout.flush()
        psi, mu = da_x(x)
        psi *= math.sqrt(Nn / float(np.sum(np.abs(psi) ** 2)))
        r = residuo(psi, mu)
    os.makedirs(DIR_NPZ, exist_ok=True)
    os.makedirs(DIR_JSON, exist_ok=True)
    f = os.path.join(DIR_NPZ, "fermo_%s.npz" % nome)
    tmp = os.path.join(DIR_NPZ, "fermo_%s_tmp.npz" % nome)
    np.savez(tmp, psi_h=psi, mu=mu)
    os.replace(tmp, f)
    riga = {"caso": nome, "delta_P0": d0, "delta_Ppi": d1, "catena": cat, "partenza": da, "partenza_sha": sha_da, "forma": forma, "s": s, "N": Nn, "mu": mu,
            "residuo_finale": r, "storia": storia, "secondi": time.time() - s0, "sha": SFM.sha(psi), "convergito": r < TOLL_RES}
    dati = (json.dumps(riga, sort_keys=True) + "\n").encode("utf-8")
    with open(fj, "xb") as fh:
        fh.write(dati)
    print("  %s: residuo finale %.3e, mu %+.9f; %s" % (nome, r, mu, "CONVERGE" if r < TOLL_RES else "NON CONVERGE"))


def corsa(ctx, nome, d0, d1, psi0, mu, r1):
    """### **`1200` tick con la mappa spostata dallo stato fermo; `D` rispetto a quello stato; l'esame di `dfb5ab7e`.**"""
    import _filtro_bande_piatte as FB
    import _modo_al_variare_di_s as MS
    z, phi0, s, forma, Z = ctx
    L = MS.L
    sp = Spostamento(Z, L, s, d0, d1)
    n0 = math.sqrt(float(np.sum(np.abs(psi0) ** 2)))
    ogni = int(round(PASSO_FIS / s))
    t_fine = int(round(T_FIS / s))
    t_da = int(round(T_DA_FIS / s))
    psi = psi0.copy()
    dn = 0.0
    Dd = {}
    s0 = time.time()
    for t in range(1, t_fine + 1):
        psi = MS.tick(z, phi0, psi, forma)
        prima = float(np.sum(np.abs(psi) ** 2))
        psi = sp(psi)
        dn = max(dn, abs(float(np.sum(np.abs(psi) ** 2)) / prima - 1.0))
        if t % ogni == 0 and t >= t_da:
            Dd[t] = np.exp(1j * mu * s * t) * psi - psi0
    print("  [%s] la norma conservata dallo spostamento: %.1e; %.0f s" % (nome, dn, time.time() - s0))
    v = MS.Vista(z, psi0)
    tasso = FB.esame(nome, sorted(Dd), Dd, n0, r1, s, v, Z, L, nome)
    return tasso, dn


def referto():
    import _diagnosi_s4 as D
    import _dove_va_la_materia as DV
    import _filtro_bande_piatte as FB
    import _modo_al_variare_di_s as MS
    print("=" * 130)
    print("LA LARGHEZZA DELLA RISONANZA CON LO STATO FERMO DI OGNI MAPPA SPOSTATA (Luca 17:15; UNA DIAGNOSI): %s, %g unita' di tempo per corsa" % (CASO, T_FIS))
    print("=" * 130)
    print("  la configurazione: CASO %s P0 %s PPI %s STATI %s MAX_NEWTON %d TOLL_RES %g T_FIS %g T_DA_FIS %g PASSO_FIS %g FATTORE_RUMORE %g SATURAZIONE %g TASSO_DFB %g TOLL_DFB %g TOLL_NORMA %g"
          % (CASO, P0, PPI, STATI, MAX_NEWTON, TOLL_RES, T_FIS, T_DA_FIS, PASSO_FIS, FB.FATTORE_RUMORE, FB.SATURAZIONE, TASSO_DFB, TOLL_DFB, TOLL_NORMA))
    print("  IL SEGNO: e^{-i delta_p s} sulle componenti della piatta p alza ph_p = -arg(lambda) di delta_p s per tick; lo scarto ph_P0 + ph_Ppi - 2 ph_sol cambia di delta_P0 + delta_Ppi per unita' di tempo")
    print("  D(t) = e^{i mu s t} psi(t) - psi_delta, psi_delta = lo stato fermo della mappa spostata (Newton, per continuazione)")
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: (w1) nella stessa direzione il tasso cala con |delta| e si spegne; (w2) non cala fino a 0.8; (w3) cala per un segno e cresce per l'altro; (w4) altro;"
          " (k1) opposte ~0.151 e solo P0 a 0.8 = la stessa direzione fra 0.2 e 0.8; (k2) no")
    _n, forma, s, N = MS.caso(CASO)
    psiz, muz, cjz, okz = MS.carica(CASO)
    esito("DEVE PASSARE: %s, lo stato a delta 0 = la ricerca (sha1), e fermo" % CASO, okz and cjz["convergito"], "%.3e" % cjz["residuo_finale"])
    a = psiz.ravel() / np.linalg.norm(psiz)
    print("-" * 130)
    print("### GLI STATI FERMI DELLE MAPPE SPOSTATE")
    trovati = [("delta0", 0.0, 0.0, psiz, muz, cjz["residuo_finale"])]
    tutti_sha = True
    for nome, d0, d1, cat in STATI:
        c = carica(nome)
        if c is None:
            print("  %-12s dP0 %+5.2f dPpi %+5.2f: NESSUNA RICERCA SUL DISCO" % (nome, d0, d1))
            continue
        psi, mu, cj, ok = c
        tutti_sha = tutti_sha and ok
        b = psi.ravel() / np.linalg.norm(psi)
        dist = 1.0 - abs(complex(np.vdot(a, b))) ** 2
        print("  %-12s dP0 %+5.2f dPpi %+5.2f (lo scarto %+5.2f), la catena %-7s dalla partenza %-12s: %d passi, residuo %.3e, %s; mu %+.9f (da delta 0 %+.3e); 1-|<a|b>|^2 %.3e; %.0f s"
              % (nome, d0, d1, d0 + d1, cat, cj["partenza"], len(cj["storia"]) - 1, cj["residuo_finale"], "CONVERGE" if cj["convergito"] else "NON CONVERGE", mu, mu - muz, dist, cj["secondi"]))
        if cj["convergito"]:
            trovati.append((nome, d0, d1, psi, mu, cj["residuo_finale"]))
    esito("DEVE PASSARE: lo sha1 di ogni stato = il suo .json", tutti_sha)
    print("-" * 130)
    print("### LE CORSE")
    tassi = {}
    dnmax = 0.0
    with D.configura(forma, s, N):
        _rec, z, phi0, _p = MS.scena(forma, s, N)
        A = DV.matrice(z, phi0, DV.AMP)
        _ph, Z = DV.autovettori(A)
        ctx = (z, phi0, s, forma, Z)
        for nome, d0, d1, psi, mu, r1 in trovati:
            print("  ## %s: dP0 %+.2f dPpi %+.2f, lo scarto %+.2f" % (nome, d0, d1, d0 + d1))
            t, dn = corsa(ctx, nome, d0, d1, psi, mu, r1)
            tassi[nome] = t
            dnmax = max(dnmax, dn)
    print("-" * 130)
    esito("DEVE PASSARE: lo spostamento conserva la norma entro %g (il massimo su tutte le corse)" % TOLL_NORMA, dnmax < TOLL_NORMA, "%.1e" % dnmax)
    t0 = tassi.get("delta0")
    esito("DEVE PASSARE: delta 0 ridà il tasso di dfb5ab7e (%.5f) entro %g relativo" % (TASSO_DFB, TOLL_DFB), t0 is not None and abs(t0 / TASSO_DFB - 1.0) < TOLL_DFB, "%s" % t0)
    print("### LA SINTESI (il tasso per unita' di tempo)")
    for nome, d0, d1, _psi, _mu, _r in trovati:
        print("  %-12s dP0 %+5.2f dPpi %+5.2f lo scarto %+5.2f: %s" % (nome, d0, d1, d0 + d1, ("%.5f" % tassi[nome]) if tassi[nome] is not None else "--"))
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import _deriva_congelato as DC
    import _solitone_vuoto_congelato as VC
    vero = (VC.FORMA, VC.S, DC.N)
    try:
        if argv[:1] == ["--referto"]:
            referto()
        elif argv[:1] == ["--cerca"] and len(argv) == 2:
            cerca(argv[1])
        else:
            raise SystemExit(__doc__)
    finally:
        VC.FORMA, VC.S, DC.N = vero
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
