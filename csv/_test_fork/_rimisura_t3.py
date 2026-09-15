# -*- coding: utf-8 -*-
"""RI-MISURA T3 dopo la patch della cache `_cs_nodo_prev` — QUATTRO bracci, non due.

La domanda del mandato: la cache riparata recupera la "meta' mancante" di T3?
  atteso dalla FASE 1: -1.03 (naive) / -0.69 (onesta);  misurato prima: -0.43.

Due bracci (ON/OFF col file patchato) non bastano a rispondere: direbbero dove SIAMO, non quanto
la patch ha SPOSTATO. Servono i quattro incroci {file PRE-patch, file POST-patch} x {OFF, ON}, e
il numero che decide e' la DIFFERENZA ON(post) - ON(pre), con la sua barra d'errore.

PREDIZIONE SCRITTA PRIMA (doc/FIX_cache_cs.md par.5, committata in 43e9a47): la differenza sara'
sotto il proprio SE (~0.01), perche' `cs` riparato varia dello 0.023% soltanto e il difetto
congelava SOLO il fattore `cs`, non `d`.

Nessuna pendenza senza barra d'errore: si stampano b, SE, r^2, IC95, n (par.9).
"""
import contextlib, importlib.util, io, os, sys
import numpy as np

RAD = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(RAD); sys.path.insert(0, RAD)
BASE = ["--batch", "--nmasse", "3", "--sep", "8", "--passi", "1", "--ogni", "100000",
        "--db-ogni", "100000", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
        "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--cs-dinamico",
        "--fork-su2", "--fork-su2-mem", "--csv", os.path.join(os.environ.get("TMP", "."), "_t3.csv")]
VECCHIO = os.path.join("csv", "_seal_fork", "_old_sim_pre_fixcache.py")
SEED, PASSI = 1, 300


def carica(percorso, nome, extra=()):
    spec = importlib.util.spec_from_file_location(nome, percorso)
    M = importlib.util.module_from_spec(spec); sys.modules[nome] = M
    sys.argv = ["soliton_simulator.py"] + BASE + list(extra)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(M)
        a = M._cli(); M._applica_regime(a); M._applica_flag(a)
    return M


def passo(M, net):
    M.scuoti_vuoto(net); net.step(); net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()


def evolvi(M, seed, n):
    net = M.Rete(seed); net.semina(80)
    for _ in range(6):
        passo(M, net)
    Nc = M.massa_critica_collasso()
    for k in range(3):
        ang = 2 * np.pi * k / 3
        net.nuova_massa(int(Nc * 0.6), raggio=0.8,
                        centro=(8.0 * np.cos(ang), 8.0 * np.sin(ang), 0.0), fase=0.0)
    for _ in range(n):
        passo(M, net)
    return net


def pend_se(x, y):
    ok = np.isfinite(x) & np.isfinite(y) & (x > 0) & (y > 0)
    lx, ly = np.log(x[ok]), np.log(y[ok])
    b = float(np.polyfit(lx, ly, 1)[0]); r = float(np.corrcoef(lx, ly)[0, 1]); n = int(ok.sum())
    se = abs(b / r) * np.sqrt((1 - r * r) / (n - 2))
    return b, se, r * r, n


def braccio(M, eti):
    net = evolvi(M, SEED, PASSI)
    n = net.n
    rs = getattr(net, "rho_spin", None)
    rho = np.asarray(rs)[:n] if (rs is not None and len(rs) >= n) else np.abs(np.asarray(net.psi[:n])) ** 2
    inz = np.maximum(rho, 1e-6)
    om = np.linalg.norm(np.asarray(net.omega_s[:n], float), axis=1)
    th = np.degrees(om * M.DT)
    v = rho > 1.0000001e-6
    b, se, r2, nn = pend_se(inz[v], th[v])
    fb = getattr(net, "_cs_fallback", None); ch = getattr(net, "_cs_chiamate", None)
    print("  %-22s pendenza %+.4f +- %.4f   r^2 %.3f   n %5d   IC95 [%+.4f, %+.4f]"
          % (eti, b, se, r2, nn, b - 1.96 * se, b + 1.96 * se))
    print("  %-22s theta mediana %10.4g gradi/passo = %8.2f giri   N nodi %d   fallback %s/%s"
          % ("", float(np.median(th)), float(np.median(th)) / 360.0, n,
             fb if fb is not None else "n/d", ch if ch is not None else "n/d"))
    return dict(b=b, se=se, r2=r2, n=nn, th=float(np.median(th)), N=n)


def main():
    print("=" * 108)
    print("RI-MISURA T3 - pendenza di theta contro l'inerzia, 4 bracci, %d passi, seme %d" % (PASSI, SEED))
    print("=" * 108)
    ris = {}
    for tag, perc, extra in (("PRE  OFF", VECCHIO, []),
                             ("PRE  ON ", VECCHIO, ["--tau-luce"]),
                             ("POST OFF", "soliton_simulator.py", []),
                             ("POST ON ", "soliton_simulator.py", ["--tau-luce"])):
        M = carica(perc, "m_" + tag.replace(" ", "_"), extra)
        ris[tag.strip()] = braccio(M, tag)
        print()

    print("=" * 108)
    print("IL NUMERO CHE DECIDE - quanto la PATCH ha spostato il braccio ON")
    print("=" * 108)
    a, b = ris["PRE  ON"], ris["POST ON"]
    d = b["b"] - a["b"]
    sed = float(np.hypot(a["se"], b["se"]))
    print("  ON(pre)  %+.4f +- %.4f        ON(post) %+.4f +- %.4f" % (a["b"], a["se"], b["b"], b["se"]))
    print("  DIFFERENZA = %+.4f +- %.4f    z = %.2f" % (d, sed, abs(d) / max(sed, 1e-12)))
    print("  PREDIZIONE (scritta prima, commit 43e9a47): |differenza| SOTTO il proprio SE -> %s"
          % ("CONFERMATA" if abs(d) <= sed else "SMENTITA"))
    print()
    print("  effetto ON-OFF, prima: %+.4f      dopo: %+.4f"
          % (ris["PRE  ON"]["b"] - ris["PRE  OFF"]["b"], ris["POST ON"]["b"] - ris["POST OFF"]["b"]))
    print("  attesa FASE 1: -1.03 (naive) / -0.69 (onesta)")
    manca = (-0.69) - b["b"]
    print("  meta' mancante rispetto alla stima ONESTA: %+.4f   (frazione recuperata dalla patch: %.1f %%)"
          % (manca, 100.0 * d / ((-0.69) - a["b"]) if abs((-0.69) - a["b"]) > 1e-12 else float("nan")))
    print("=" * 108)
    return 0


if __name__ == "__main__":
    sys.exit(main())
