r"""### ⛔ **GRIGLIA QUADRATA -- non eseguita (DECISIONE-SOLO-TRIANGOLI)** *(il quadrato: decisione di Luca del 2026-10-23, 16:14)*.

**LA PARTE C.3: LA DINAMICA DEI SOLITONI LARGHI IN UN GRADIENTE DI `cs`** *(la camminata intera col legame, eps 0, le due convenzioni; solo misure, in memoria)*.

> ### ⛔ **Il task history e' `2026-10-23_modi_pi_e_solitoni.md`, sez. `7`** *(i punti, la scena, l'assestamento, la tenuta, la forza, le previsioni, i criteri, fissati prima)*. ### **`leggi.yaml`,
> l'impronta, la convenzione nel repo e il nucleo intatti.** ### **Importati, non copiati:** `_modi_pi_e_solitoni` *(`largo`, `conv`)*, `_gravita_collettiva` *(`profilo`, `gruppi`, `c_di`)*,
> `_forza_da_cs` *(`rami`, `spazio_del_ramo`, `committata`)*, `_stabilita_lineare.passo`, `_screening_forme_s3.forma`, `scena_l2.scena`, `_universalita_massa.blob`.

### **Per ogni punto** *(forma, `s`, `N`; da `modi_pi_e_solitoni.jsonl`)* ### **e convenzione:** ### **lo stato iniziale dal profilo radiale, l'ASSESTAMENTO** *(`T0` a `cs` uniforme, la norma emessa)*,
### **la TENUTA** *(`64` tick: larghezza entro il `10%`, baricentro fermo)*, ### **la FORZA** *(`eta` `+-1e-3`, `+-1e-2`, dallo stato assestato)*, ### **la scomposizione `E_ramo` / `E_legame`.**

Gira con:  python csv/_solitoni_in_gradiente.py > doc/referti_l2/solitoni_in_gradiente.txt
"""
import io
import json
import os
import sys
import warnings

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

LX, LY = 256, 64
T_MIS = LX // 4
T0_MIN = 64
PERIODI_T0 = 10
ETA = (1e-3, -1e-3, 1e-2, -1e-2)
LARGHEZZA_TOLL = 0.10
SPECCHIO_TOLL = 0.05
MIN_PUNTI = 6
LAM0 = 4.0
CONV = ("oggi", "simm")
J_MP = os.path.join(RADICE, "doc", "referti_l2", "modi_pi_e_solitoni.jsonl")
JSONL = os.path.join(RADICE, "doc", "referti_l2", "solitoni_in_gradiente.jsonl")
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-82s %s   %s" % (che[:82], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scrivi(r):
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(r) + "\n")


def f_(x, fm="%+.4f"):
    return "--" if x is None else fm % x


def punti():
    """### I punti di `C.2`: per forma il primo `s` largo `>= 4` archi e le sue (al piu' due) norme piu' piccole."""
    import _forza_da_cs as F
    assert F.committata(J_MP), "il jsonl di 9a6955f3 non e' committato e pulito"
    out = []
    for r in (json.loads(l) for l in io.open(J_MP, encoding="utf-8")):
        if r.get("tipo") == "primo_s" and r["primo"]:
            for N in r["primo"]["N"][:2]:
                out.append((r["forma"], r["primo"]["s"], N))
    return out


def scena(s):
    import scena_l2 as SC
    import statica_protocollo as PR
    inc, mot, st, par, _c, _p = SC.scena(1.0, PR.VUOTO, 0.0, PR.RAGGIO, False, True, False, PR.SEME, 1, lati=(LX, LY))
    par["eps"] = 0.0
    mot.cs = np.full(inc.n, float(s))
    mot.lambda_c = None
    st["psi_h"][...] = 0
    return inc, mot, st, par


def coordinate(n):
    v = np.arange(n)
    return (v // LY).astype(float), (v % LY).astype(float)


def osserva(st, n, x, y, w0=None):
    """### Il baricentro circolare in `x` e `y`, la larghezza rms *(immagine minima)*, la frazione oltre `3 w0`."""
    p = st["psi_h"].reshape(n, 8)
    w = np.sum(np.abs(p) ** 2, axis=1)
    tot = float(np.sum(w))
    cx = (LX / (2.0 * np.pi) * np.angle(np.sum(w * np.exp(2j * np.pi * x / LX)))) % LX
    cy = (LY / (2.0 * np.pi) * np.angle(np.sum(w * np.exp(2j * np.pi * y / LY)))) % LY
    dx = (x - cx + LX / 2.0) % LX - LX / 2.0
    dy = (y - cy + LY / 2.0) % LY - LY / 2.0
    r2 = dx * dx + dy * dy
    larg = float(np.sqrt(np.sum(w * r2) / tot))
    fuori = None if w0 is None else float(np.sum(w[r2 > (3.0 * w0) ** 2]) / tot)
    return cx, cy, larg, fuori, tot


def fit_a(tt, xx):
    tt, xx = np.array(tt, dtype=float), np.array(xx, dtype=float)
    if len(tt) < MIN_PUNTI:
        return None, None
    X = np.stack([np.ones_like(tt), tt, 0.5 * tt * tt], axis=1)
    coef, *_ = np.linalg.lstsq(X, xx, rcond=None)
    res = xx - X @ coef
    var = float(res @ res) / (len(tt) - 3)
    cov = var * np.linalg.inv(X.T @ X)
    return float(coef[2]), float(np.sqrt(max(cov[2, 2], 0.0)))


def corri(forma, nome, st, mot, par, n, x, y, ticks, cs, x0, w0=None, ferma=True):
    """### `ticks` tick del passo intero a `cs` dato; ### **il baricentro in `x` relativo a `x0`, la larghezza** *(e si ferma se `|dx| >= Lx/32`)*."""
    import _modi_pi_e_solitoni as MP
    import _screening_forme_s3 as SF
    import _stabilita_lineare as SL
    mot.cs = cs
    tt, xx, ll = [], [], []
    with SF.forma(forma), MP.conv(nome):
        for t in range(ticks + 1):
            if t:
                SL.passo(st, mot, par, False, (), 0.0)
            cx, _cy, larg, _f, _tot = osserva(st, n, x, y, w0)
            dx = (cx - x0 + LX / 2.0) % LX - LX / 2.0
            if ferma and abs(dx) >= LX / 32.0:
                break
            tt.append(t)
            xx.append(float(dx))
            ll.append(larg)
    return tt, xx, ll


def main(argv):
    del argv
    import _forza_da_cs as F
    import _gravita_collettiva as GC
    import _modi_pi_e_solitoni as MP
    import _presidio
    import _universalita_massa as UM
    import composizione as CM
    _presidio.avvia(__file__)
    print("=" * 100)
    print("LA PARTE C.3: LA DINAMICA DEI SOLITONI LARGHI IN UN GRADIENTE DI cs (eps 0, ramo a curvatura -, le due convenzioni)")
    print("=" * 100)
    blobs = {r: UM.blob(r) for r in ("soliton_simulator.py", "csv/_forza_da_cs.py", "csv/_stabilita_lineare.py", "csv/_gravita_collettiva.py", "csv/_zero_simmetrico.py",
                                     "csv/_modi_pi_e_solitoni.py", "csv/_solitoni_in_gradiente.py", "doc/referti_l2/modi_pi_e_solitoni.jsonl")}
    print("  il passo: %d pezzi, impronta %s (intatto); il legame acceso (salta = ()); i blob nel repo: %s"
          % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: LX %d; LY %d; T_MIS %d; T0 = max(%d, %d * 2 pi/|mu|); ETA %s; LARGHEZZA_TOLL %g; SPECCHIO_TOLL %g; MIN_PUNTI %d; LAM0 %g"
          % (LX, LY, T_MIS, T0_MIN, PERIODI_T0, ETA, LARGHEZZA_TOLL, SPECCHIO_TOLL, MIN_PUNTI, LAM0))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs})
    warnings.simplefilter("ignore")
    pp = punti()
    print("  i punti (da 9a6955f3): %s" % pp)
    tab, tenute, specchi = [], [], []
    for forma, s, N in pp:
        lista, BB, _ = F.rami(s, 0.0)
        g = [x_ for x_ in GC.gruppi(lista) if x_["segno"] < 0][0]
        c = GC.c_di(g)
        q = MP.largo(forma, c, s, N)
        q2, rg, ug = GC.profilo(forma, c, s, N, LAM0, q["dr"], int(round(q["R"] / q["dr"])), q["larghezza"])
        Q = F.spazio_del_ramo(BB, g)[0]
        e = Q[:, 0]
        mu = q2["mu"]
        T0 = int(max(T0_MIN, np.ceil(PERIODI_T0 * 2.0 * np.pi / abs(mu))))
        print("### %s s %g N %g: larghezza %.3f archi, mu %+.5f, x_centro %.3g; v %.5f; T0 %d tick" % (forma, s, N, q2["larghezza"], mu, q2["x_centro"], g["v"], T0))
        if s >= 0.9:
            print("  ### s >= 0.9: il principio di equivalenza qui e' gia' violato d'ordine 1 (05055fc6): si legge SOLO IL VERSO")
        for nome in CONV:
            inc, mot, st, par = scena(s)
            n = inc.n
            x, y = coordinate(n)
            lam = float(np.mean(mot.densita_vuoto(st)))
            dx = (x - LX / 4.0 + LX / 2.0) % LX - LX / 2.0
            dy = (y - LY / 2.0 + LY / 2.0) % LY - LY / 2.0
            rho = np.interp(np.sqrt(dx * dx + dy * dy), rg, ug * ug, right=0.0)
            cel = np.sqrt(rho)[:, None] * e[None, :]
            cel *= np.sqrt(N / np.sum(np.abs(cel) ** 2))
            st["psi_h"][...] = cel.reshape(st["psi_h"].shape)
            w_in = osserva(st, n, x, y)[2]
            # ---- l'assestamento
            corri(forma, nome, st, mot, par, n, x, y, T0, np.full(n, s), LX / 4.0, ferma=False)
            cx, cy, w_a, fuori, tot = osserva(st, n, x, y, w_in)
            assest = {k: v.copy() for k, v in st.items()}
            # ---- la tenuta
            st_t = {k: v.copy() for k, v in assest.items()}
            tt, xx, ll = corri(forma, nome, st_t, mot, par, n, x, y, T_MIS, np.full(n, s), cx, ferma=False)
            a0, s0_ = fit_a(tt, xx)
            dev = max(abs(l_ - ll[0]) / ll[0] for l_ in ll)
            tiene = dev <= LARGHEZZA_TOLL and a0 is not None and (abs(a0) <= 2.0 * s0_ or abs(a0) < 1e-12)
            esce = next((t for t, l_ in zip(tt, ll) if abs(l_ - ll[0]) / ll[0] > LARGHEZZA_TOLL), None)
            rec = {"tipo": "tenuta", "forma": forma, "s": s, "N": N, "convenzione": nome, "Lambda0": lam, "larghezza_iniziale": w_in, "larghezza_assestata": w_a,
                   "norma_emessa": fuori, "norma": tot, "T0": T0, "scarto_larghezza": dev, "esce_al_tick": esce, "a": a0, "sigma_a": s0_, "tiene": tiene}
            tenute.append(rec)
            scrivi(rec)
            print("  %-4s: Lambda0 %.3f | larghezza iniziale %.3f, dopo T0 %.3f; la norma emessa (oltre 3 w0) %.4f | la tenuta: larghezza entro %.3f%s, a %s (+- %s) -> %s"
                  % (nome, lam, w_in, w_a, fuori, dev, "" if esce is None else " (esce al tick %d)" % esce, f_(a0, "%+.2e"), f_(s0_, "%.1e"),
                     "TIENE" if tiene else "### NON TIENE"))
            sys.stdout.flush()
            if not tiene:
                continue
            aa = {}
            for eta in ETA:
                cs = s * (1.0 + eta * np.cos(2.0 * np.pi * x / LX))
                tt, xx, ll = corri(forma, nome, {k: v.copy() for k, v in assest.items()}, mot, par, n, x, y, T_MIS, cs, cx)
                a, sa = fit_a(tt, xx)
                dsdx = -s * eta * 2.0 * np.pi / LX
                a_RG = -g["v"] ** 2 * dsdx / s
                E_ramo = (np.pi * s if nome == "simm" else 0.0) / s + g["omega0"] / s
                rec = {"tipo": "forza", "forma": forma, "s": s, "N": N, "convenzione": nome, "eta": eta, "a": a, "sigma_a": sa, "punti": len(tt), "a_RG": a_RG,
                       "mis_su_RG": None if a is None else a / a_RG, "E_ramo": E_ramo, "E_legame": mu / s,
                       "domina": "legame" if abs(mu / s) > abs(E_ramo) else "ramo"}
                aa[eta] = a
                tab.append(rec)
                scrivi(rec)
                print("    eta %+.0e: %d punti, a %s (+- %s) | a/a_RG %s -> %s | E_ramo %+.4f, E_legame %+.4f: domina il %s"
                      % (eta, len(tt), f_(a, "%+.3e"), f_(sa, "%.1e"), f_(rec["mis_su_RG"], "%+.3f"),
                         "--" if a is None else ("verso cs BASSO" if rec["mis_su_RG"] > 0 else "verso cs ALTO"), E_ramo, mu / s, rec["domina"]))
                sys.stdout.flush()
            for e_ in (1e-3, 1e-2):
                p_, m_ = aa.get(e_), aa.get(-e_)
                if p_ is not None and m_ is not None:
                    # ### ⭐ **LA PARTE ANTISIMMETRICA in `eta` e' la forza, quella SIMMETRICA la deriva propria del solitone** *(annotazione `2`, prima della corsa)*
                    anti, simm_ = 0.5 * (p_ - m_), 0.5 * (p_ + m_)
                    a_RG = -g["v"] ** 2 * (-s * e_ * 2.0 * np.pi / LX) / s
                    scrivi({"tipo": "forza_antisimmetrica", "forma": forma, "s": s, "N": N, "convenzione": nome, "eta": e_, "a_anti": anti, "a_simm": simm_,
                            "anti_su_RG": anti / a_RG})
                    print("    eta %g: la parte antisimmetrica a %+.3e -> a/a_RG %+.3f (%s); la deriva propria (simmetrica) %+.3e"
                          % (e_, anti, anti / a_RG, "verso cs BASSO" if anti / a_RG > 0 else "verso cs ALTO", simm_))
                if p_ is not None and m_ is not None and p_ != 0:
                    specchi.append({"forma": forma, "s": s, "N": N, "convenzione": nome, "eta": e_, "ok": np.sign(p_) == -np.sign(m_) and abs(abs(m_) - abs(p_)) / abs(p_) < SPECCHIO_TOLL,
                                    "scarto": abs(abs(m_) - abs(p_)) / abs(p_)})
    print("### I CONTROLLI")
    esito("DEVE PASSARE: a cs uniforme, |a| sotto il rumore del fit (la tenuta, %d stati)" % len(tenute), len(tenute) > 0 and all(r["tiene"] for r in tenute),
          "; ".join("%s s %g N %g %s: %s" % (r["forma"], r["s"], r["N"], r["convenzione"], "tiene" if r["tiene"] else "NON TIENE") for r in tenute))
    esito("DEVE PASSARE: lo specchio, a cambia segno e |a| uguale entro il 5%% (%d coppie)" % len(specchi), len(specchi) > 0 and all(r["ok"] for r in specchi),
          "; ".join("%s s %g N %g %s eta %g: %.3f" % (r["forma"], r["s"], r["N"], r["convenzione"], r["eta"], r["scarto"]) for r in specchi))
    pos = [r for r in tab if r["forma"] in ("S3", "S4") and r["convenzione"] == "simm" and r["mis_su_RG"] is not None and r["eta"] > 0]
    esito("PUO' FALLIRE: almeno un solitone S3 o S4 con lo zero simmetrico e a_mis/a_RG > 0", any(r["mis_su_RG"] > 0 for r in pos),
          "; ".join("%s N %g eta %g: %+.3f" % (r["forma"], r["N"], r["eta"], r["mis_su_RG"]) for r in pos))
    print("=" * 100)
    print("LA PARTE C.3: %d su %d controlli   %s  (il verdetto di fisica e' il verso e a_mis/a_RG)" % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
