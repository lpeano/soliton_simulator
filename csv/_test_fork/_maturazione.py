# -*- coding: utf-8 -*-
"""L'ALIASING SPARISCE DA SOLO? — misura della MATURAZIONE (`ramp`) e del suo effetto su `theta`.

LA DOMANDA (doc/PREDIZIONE_maturazione.md, scritta PRIMA)
---------------------------------------------------------
Il `1e-7` dell'inerzia e' ETA', non normalizzazione: `ramp = min(1, eta/TAU_A)` con TAU_A = 50 e
`eta += dt_n (~0.01)` per passo, quindi peso pieno solo dopo ~5000 passi. Se e' cosi', l'aliasing
(`theta` ~ 112 giri/passo) potrebbe sparire DA SOLO, e non ci sarebbe niente da riparare.

LE TRE GRANDEZZE
----------------
  ramp     quanto e' maturo il sistema
  inerzia  |Psi|^2 (o rho_spin): cresce come ~ramp^4?  E quando molla il pavimento 1e-6?
  theta    |omega_s| * dt_n in GRADI/PASSO: LA GRANDEZZA CHE DECIDE. Scende sotto ~30?

IL PRESIDIO ANTI-ILLUSIONE (dichiarato prima di misurare)
----------------------------------------------------------
La MEDIANA puo' scendere mentre una CODA di nodi giovani resta aliasata: i figli della mitosi
nascono con `eta = 0` (riga 3119), quindi esiste SEMPRE una popolazione giovane. Percio' si riporta
anche la FRAZIONE di nodi con `theta > 30 gradi/passo`, e si stratifica per eta' (giovani/maturi).
Se la mediana scende ma la frazione resta alta, e' l'esito (C) MASCHERATO.

PUREZZA (sigillo PRIMA dell'uso, par.2.3)
------------------------------------------
Legge SOLO array di stato: `psi`, `rho_spin`, `omega_s`, `eta`, `n`. NON chiama `calcola_psi()`,
`ritmo()`, `_pesi()`, `_lam_archi()`, `lambda_nodi()`, che mutano cache di continuita' lette dalla
dinamica. Non consuma `net.rng`. `--sigillo` lo DIMOSTRA invece di assumerlo.

USO
---
python csv/_test_fork/_maturazione.py --sigillo
python csv/_test_fork/_maturazione.py --passi 2000
"""
import sys as _sys_enc  # PRESIDIO ENCODING (CLAUDE.md): lo stdout di Windows e' cp1252 e
# uccide qualunque print con un carattere non-ASCII. E' successo SETTE volte, l'ultima allo
# script che stava CONTANDO le occorrenze. Il `# -*- coding: utf-8 -*-` NON basta: riguarda il
# SORGENTE, non lo STDOUT. Questa riga lo risolve alla radice.
try:
    _sys_enc.stdout.reconfigure(encoding="utf-8")
    _sys_enc.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import argparse
import contextlib
import io
import os
import sys

import numpy as np

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SOGLIA_ALIAS = 30.0        # gradi/passo: sotto, il settore e' integrabile
CHI_NULL_MEDIA, CHI_NULL_STD = 90.000, 39.171


def prepara(mostra_flag=True):
    os.chdir(RADICE); sys.path.insert(0, RADICE)
    sys.argv = ["soliton_simulator.py", "--batch", "--nmasse", "3", "--sep", "8",
                "--passi", "1", "--ogni", "100000", "--db-ogni", "100000",
                "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto", "--chi-core",
                "--calore-scal", "--deparam-orologio", "--verlet", "--cs-dinamico",
                "--fork-su2", "--fork-su2-mem",
                "--csv", os.path.join(os.environ.get("TMP", "."), "_matur.csv")]
    import soliton_simulator as S
    a = S._cli(); S._applica_regime(a)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        S._applica_flag(a)
    if mostra_flag:
        print("=" * 100)
        print("CONFERMA DEI FLAG **IN-RUN** (lezione del falso O3c: non fidarsi della riga di comando)")
        print("=" * 100)
        for riga in buf.getvalue().splitlines():
            if riga.strip().startswith("["):
                print("  " + riga.strip())
        print("  GAMMA_TURBO = %.4g   (1.0 = NESSUN turbo)        STEP2_OROLOGIO = %s   (deve essere False)"
              % (S.GAMMA_TURBO, S.STEP2_OROLOGIO))
        print("  FORK_SU2 = %s   FORK_SU2_MEM = %s   CS_DINAMICO = %s" % (S.FORK_SU2, S.FORK_SU2_MEM, S.CS_DINAMICO))
        print("  TAU_A = %.4g   DT = %.4g   -> maturazione piena a %.0f passi"
              % (S.TAU_A, S.DT, S.TAU_A / S.DT))
        print()
    return S


def scena(S, seed):
    net = S.Rete(seed); net.semina(80)
    for _ in range(6):
        passo(S, net)
    Nc = S.massa_critica_collasso()
    for k in range(3):
        ang = 2 * np.pi * k / 3
        net.nuova_massa(int(Nc * 0.6), raggio=0.8,
                        centro=(8.0 * np.cos(ang), 8.0 * np.sin(ang), 0.0), fase=0.0)
    return net


def passo(S, net):
    S.scuoti_vuoto(net); net.step(); net.mitosi()
    net.rilassa_disegno(); net.memoria_hebbiana_moto()


def leggi(S, net):
    """PURE-READ: solo array di stato, nessuna chiamata che muti cache."""
    n = net.n
    eta = np.asarray(net.eta[:n], float)
    ramp = np.minimum(1.0, eta / S.TAU_A)
    rs = getattr(net, "rho_spin", None)
    rho = np.asarray(rs)[:n] if (rs is not None and len(rs) >= n) else np.abs(np.asarray(net.psi[:n])) ** 2
    inerzia = np.maximum(rho, 1e-6)
    om = np.linalg.norm(np.asarray(net.omega_s[:n], float), axis=1)
    theta = np.degrees(om * S.DT)          # dt_n userebbe ritmo(), che MUTA: si usa il tic nominale
    # tau della memoria (riga 1913), ricostruito dagli stessi array: TAU_A * max(dens/dens_rif, 0.05)
    dens = np.abs(np.asarray(net.psi[:n])) ** 2
    rif = max(float(np.median(dens[dens > 1e-6])), 1e-6) if np.any(dens > 1e-6) else 1.0
    tau = S.TAU_A * np.maximum(dens / rif, 0.05)
    return ramp, rho, inerzia, theta, tau


def trasversale(ramp, inerzia, theta):
    """IL TEST CHE NON CONTIENE IL TEMPO (doc/CRITERIO_omega_rho.md par.4.1).

    Regressione di log(theta) su log(inerzia) ATTRAVERSO I NODI, a tempo FISSATO. Il ritardo e' una
    spiegazione temporale: a un solo istante non puo' essere invocato.
      pendenza -1.3 .. -0.3  -> omega DIPENDE da inerzia: la lettura regge
      pendenza -0.2 .. +0.2  -> omega NON dipende da inerzia PER NESSUNA VIA: lettura sbagliata
    Si escludono i nodi col pavimento attivo (inerzia == 1e-6 esatto): li' l'inerzia NON varia, quindi
    non portano informazione sulla dipendenza e diluirebbero la pendenza verso zero per costruzione.
    """
    vivi = (inerzia > 1.0000001e-6) & (theta > 0)
    out = {"n_usati": int(vivi.sum()), "n_pavimento": int((~vivi).sum())}
    if vivi.sum() < 50:
        out["pendenza"] = float("nan"); return out
    x = np.log(inerzia[vivi]); y = np.log(theta[vivi])
    out["pendenza"] = float(np.polyfit(x, y, 1)[0])
    out["leva"] = float(inerzia[vivi].max() / inerzia[vivi].min())
    # correlazione, per sapere se la pendenza e' sostenuta o rumore
    out["r"] = float(np.corrcoef(x, y)[0, 1])
    # controllo a decili di inerzia: la mediana di theta cala col decile?
    q = np.percentile(inerzia[vivi], [10, 50, 90])
    out["th_basso"] = float(np.median(theta[vivi][inerzia[vivi] <= q[0]]))
    out["th_medio"] = float(np.median(theta[vivi][(inerzia[vivi] > q[0]) & (inerzia[vivi] < q[2])]))
    out["th_alto"] = float(np.median(theta[vivi][inerzia[vivi] >= q[2]]))
    return out


CAMPI = ("pos", "phi", "phi0", "phivel", "eta", "d", "d0", "vd", "peq", "tw", "twp",
         "i", "j", "perc_chi", "perc_tw", "_nb", "_nb_ret", "_psi_spinor", "omega_s", "psi")


def sigillo(S, seed, passi):
    def corri(osserva):
        net = scena(S, seed)
        for _ in range(passi):
            passo(S, net)
            if osserva:
                leggi(S, net)
        return net
    a = corri(False); b = corri(True)
    print("=" * 100)
    print("SIGILLO — il diagnostico e' PURE-READ?  (%d passi, seme %d)" % (passi, seed))
    print("=" * 100)
    print("PRESIDIO: uno zero con N DIVERSO e' MANCANZA DI CONFRONTO, non identita'.")
    print("  n senza osservatore = %d   n con osservatore = %d   ->  %s"
          % (a.n, b.n, "CONFRONTABILI" if a.n == b.n else "NON CONFRONTABILI: sigillo NULLO"))
    if a.n != b.n:
        return False
    ok = True
    for c in CAMPI:
        va, vb = getattr(a, c, None), getattr(b, c, None)
        if va is None or vb is None:
            print("  %-14s assente -> SALTATO" % c); continue
        va, vb = np.asarray(va), np.asarray(vb)
        if va.shape != vb.shape:
            print("  %-14s SHAPE %s vs %s -> FAIL" % (c, va.shape, vb.shape)); ok = False; continue
        d = float(np.max(np.abs(va.astype(complex) - vb.astype(complex)))) if va.size else 0.0
        if d != 0.0:
            ok = False
        print("  %-14s shape %-14s max|A-B| = %.3e   %s" % (c, str(va.shape), d, "PASS" if d == 0 else "FAIL"))
    rng_ok = (a.rng.bit_generator.state == b.rng.bit_generator.state)
    print("  %-14s %s   %s" % ("stato RNG", "identico" if rng_ok else "DIVERSO", "PASS" if rng_ok else "FAIL"))
    ok = ok and rng_ok
    print("\nSIGILLO: %s" % ("PASS — il diagnostico non tocca nulla" if ok else "FAIL — NON USARLO"))
    return ok


def misura(S, seed, passi, ogni_fitto, fino, ogni_rado):
    net = scena(S, seed)
    print("scena: n=%d archi=%d  (seme %d)  soglia di aliasing = %.0f gradi/passo"
          % (net.n, len(net.i), seed, SOGLIA_ALIAS))
    print()
    print(" passo      n    ramp_med |  rho_med   %sotto |  theta_med   theta_p95 | %>soglia |  tau/DT med  tau/DT p50nodo | giovani  maturi")
    print(" " + "-" * 118)
    storia = []
    for t in range(1, passi + 1):
        passo(S, net)
        ogni = ogni_fitto if t <= fino else ogni_rado
        if t % ogni and t != 1:
            continue
        ramp, rho, inerzia, theta, tau = leggi(S, net)
        giovani = ramp < 0.1
        maturi = ramp > 0.5
        th_g = float(np.median(theta[giovani])) if giovani.any() else float("nan")
        th_m = float(np.median(theta[maturi])) if maturi.any() else float("nan")
        riga = dict(passo=t, n=net.n, ramp_med=float(np.median(ramp)),
                    ramp_p95=float(np.percentile(ramp, 95)),
                    rho_med=float(np.median(rho)), sotto=float(np.mean(rho < 1e-6)),
                    th_med=float(np.median(theta)), th_p95=float(np.percentile(theta, 95)),
                    fr_alias=float(np.mean(theta > SOGLIA_ALIAS)),
                    th_g=th_g, th_m=th_m, fr_giov=float(np.mean(giovani)))
        storia.append(riga)
        riga["tau_dt"] = float(np.median(tau)) / S.DT
        riga["tau_frac_pav"] = float(np.mean(tau <= S.TAU_A * 0.05 * 1.0000001))
        print(" %5d  %6d  %8.4f | %9.3g %6.1f%% | %10.4g  %10.4g | %7.1f%% | %11.4g  %13.1f%% | %8.4g %8.4g"
              % (t, net.n, riga["ramp_med"], riga["rho_med"], 100 * riga["sotto"],
                 riga["th_med"], riga["th_p95"], 100 * riga["fr_alias"],
                 riga["tau_dt"], 100 * riga["tau_frac_pav"], th_g, th_m))
    return net, storia


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--passi", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--ogni-fitto", type=int, default=25)
    ap.add_argument("--fino", type=int, default=600)
    ap.add_argument("--ogni-rado", type=int, default=100)
    ap.add_argument("--sigillo", action="store_true")
    ap.add_argument("--passi-sigillo", type=int, default=25)
    o = ap.parse_args()
    S = prepara()
    if o.sigillo:
        sys.exit(0 if sigillo(S, o.seed, o.passi_sigillo) else 1)
    net, storia = misura(S, o.seed, o.passi, o.ogni_fitto, o.fino, o.ogni_rado)
    ramp, rho, inerzia, theta, tau = leggi(S, net)
    tr = trasversale(ramp, inerzia, theta)
    print()
    print("=" * 100)
    print("TEST TRASVERSALE — a UN SOLO ISTANTE, fra i nodi (doc/CRITERIO_omega_rho.md par.4.1)")
    print("=" * 100)
    print("  nodi usati %d   (esclusi %d col pavimento attivo: li' l'inerzia non varia)"
          % (tr["n_usati"], tr["n_pavimento"]))
    if tr["n_usati"] >= 50:
        print("  leva sull'inerzia: x%.4g      correlazione r = %+.3f" % (tr["leva"], tr["r"]))
        print("  theta mediano per decile di inerzia:  basso %.4g | medio %.4g | ALTO %.4g"
              % (tr["th_basso"], tr["th_medio"], tr["th_alto"]))
        print()
        print("  >>> PENDENZA TRASVERSALE  d(log theta)/d(log inerzia) = %+.3f" % tr["pendenza"])
        p = tr["pendenza"]
        if -1.3 <= p <= -0.3:
            print("  >>> -1.3..-0.3 : omega DIPENDE da inerzia. La lettura regge, il problema e' temporale.")
        elif -0.2 <= p <= 0.2:
            print("  >>> -0.2..+0.2 : omega NON DIPENDE da inerzia PER NESSUNA VIA.")
            print("  >>> La lettura omega = coppia/inerzia e' SBAGLIATA ALLA RADICE. Nessun ritardo la salva.")
        else:
            print("  >>> fuori da entrambe le bande dichiarate: riportare senza concludere.")
    print()
    print("=" * 100)
    print("LETTURA (regola scritta PRIMA, doc/PREDIZIONE_maturazione.md)")
    print("=" * 100)
    if not storia:
        print("nessun campione."); return
    p, u = storia[0], storia[-1]
    print("  theta mediano: %.4g -> %.4g gradi/passo   (fattore %.3g)"
          % (p["th_med"], u["th_med"], u["th_med"] / max(p["th_med"], 1e-30)))
    print("  frazione aliasata (theta > %.0f): %.1f%% -> %.1f%%"
          % (SOGLIA_ALIAS, 100 * p["fr_alias"], 100 * u["fr_alias"]))
    print("  ramp mediano: %.4f -> %.4f      rho mediano: %.3g -> %.3g   (pavimento 1e-6)"
          % (p["ramp_med"], u["ramp_med"], p["rho_med"], u["rho_med"]))
    print()
    if u["th_med"] < SOGLIA_ALIAS and u["fr_alias"] < 0.05:
        print("  -> theta SOTTO soglia e coda rientrata: serve la SECONDA misura (chi nella zona matura).")
    elif u["th_med"] < SOGLIA_ALIAS:
        print("  -> mediana sotto soglia MA CODA ANCORA ALIASATA (%.1f%%): e' l'esito (C) MASCHERATO."
              % (100 * u["fr_alias"]))
    else:
        print("  -> theta NON e' sceso sotto soglia: esito (C), aliasing STRUTTURALE.")


if __name__ == "__main__":
    main()
