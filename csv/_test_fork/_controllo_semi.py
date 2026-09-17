# -*- coding: utf-8 -*-
"""CONTROLLO SUI SEMI — il `z = 3.16` della ri-misura T3 e' reale o dispersione di run?

LA DOMANDA. La ri-misura T3 (csv/_test_fork/_rimisura_t3.txt, seme 1) dice che la cura della cache
ha spostato la pendenza ON da -0.4265 +- 0.0091 a -0.4710 +- 0.0107, `Delta = -0.0445 +- 0.0141`.
Ma quelle `SE` sono l'errore di campionamento della retta **DENTRO un singolo run**, e i due bracci
sono **due traiettorie diverse di un sistema caotico** (N = 3999 contro 4100).

**Il valore sotto ipotesi nulla qui NON e' zero** (par.9): e' la dispersione della pendenza fra run
che differiscono per una perturbazione irrilevante. Finche' non la si misura, `z = 3.16` non decide
niente — e questo vale in ENTRAMBE le direzioni: indebolirebbe allo stesso modo una conferma.

IL DISEGNO. Tre semi x due bracci (file PRE-patch ON, file POST-patch ON). Da qui:
  * **il segnale**: `Delta(seme) = ON_post - ON_pre`, tre volte. Se si ripete, e' sistematico.
  * **il nullo**: la dispersione di `ON_pre` fra i tre semi, e quella di `ON_post`. E' la barra
    d'errore GIUSTA, quella che il singolo run non puo' dare.
  * **il test onesto**: `media(Delta)` contro `SE della media` calcolato dai tre `Delta`, non dalle
    `SE` interne.

NB: par.2.7 chiede almeno due semi per qualunque fatto pubblicabile. Il seme 1 c'e' gia' ma va
rifatto qui, perche' i tre `Delta` devono venire dallo stesso identico codice di misura.
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
import contextlib, importlib.util, io, os, sys
import numpy as np

RAD = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(RAD); sys.path.insert(0, RAD)
BASE = ["--batch", "--nmasse", "3", "--sep", "8", "--passi", "1", "--ogni", "100000",
        "--db-ogni", "100000", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
        "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--cs-dinamico",
        "--fork-su2", "--fork-su2-mem", "--tau-luce",
        "--csv", os.path.join(os.environ.get("TMP", "."), "_ctl.csv")]
VECCHIO = os.path.join("csv", "_seal_fork", "_old_sim_pre_fixcache.py")
SEMI = (1, 2, 3)
PASSI = 300


def carica(percorso, nome):
    spec = importlib.util.spec_from_file_location(nome, percorso)
    M = importlib.util.module_from_spec(spec); sys.modules[nome] = M
    sys.argv = ["soliton_simulator.py"] + BASE
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(M)
        a = M._cli(); M._applica_regime(a); M._applica_flag(a)
    return M


def passo(M, net):
    M.scuoti_vuoto(net); net.step(); net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()


def pendenza(M, seed):
    net = M.Rete(seed); net.semina(80)
    for _ in range(6):
        passo(M, net)
    Nc = M.massa_critica_collasso()
    for k in range(3):
        ang = 2 * np.pi * k / 3
        net.nuova_massa(int(Nc * 0.6), raggio=0.8,
                        centro=(8.0 * np.cos(ang), 8.0 * np.sin(ang), 0.0), fase=0.0)
    for _ in range(PASSI):
        passo(M, net)
    n = net.n
    rs = getattr(net, "rho_spin", None)
    rho = np.asarray(rs)[:n] if (rs is not None and len(rs) >= n) else np.abs(np.asarray(net.psi[:n])) ** 2
    inz = np.maximum(rho, 1e-6)
    om = np.linalg.norm(np.asarray(net.omega_s[:n], float), axis=1)
    th = np.degrees(om * M.DT)
    v = rho > 1.0000001e-6
    x, y = inz[v], th[v]
    ok = np.isfinite(x) & np.isfinite(y) & (x > 0) & (y > 0)
    lx, ly = np.log(x[ok]), np.log(y[ok])
    b = float(np.polyfit(lx, ly, 1)[0]); r = float(np.corrcoef(lx, ly)[0, 1]); nn = int(ok.sum())
    se = abs(b / r) * np.sqrt((1 - r * r) / (nn - 2))
    return b, se, nn, net.n, float(np.median(th))


def main():
    print("=" * 100)
    print("CONTROLLO SUI SEMI - %d semi x 2 bracci (ON pre-patch, ON post-patch), %d passi"
          % (len(SEMI), PASSI))
    print("=" * 100)
    M_pre = carica(VECCHIO, "ctl_pre")
    M_post = carica("soliton_simulator.py", "ctl_post")
    pre, post = {}, {}
    for s in SEMI:
        bp, sep, np_, Np, thp = pendenza(M_pre, s)
        bo, seo, no_, No, tho = pendenza(M_post, s)
        pre[s] = bp; post[s] = bo
        print("  seme %d   ON pre  %+.4f +- %.4f (n %d, N %d, %6.2f giri)"
              % (s, bp, sep, np_, Np, thp / 360.0))
        print("           ON post %+.4f +- %.4f (n %d, N %d, %6.2f giri)    Delta = %+.4f"
              % (bo, seo, no_, No, tho / 360.0, bo - bp))
    print()
    print("=" * 100)
    print("IL NULLO - dispersione della pendenza FRA SEMI, a codice invariato")
    print("=" * 100)
    vp = np.array([pre[s] for s in SEMI]); vo = np.array([post[s] for s in SEMI])
    sp = float(np.std(vp, ddof=1)); so = float(np.std(vo, ddof=1))
    print("  ON pre  : %s   media %+.4f   dev.std FRA SEMI %.4f"
          % ("  ".join("%+.4f" % v for v in vp), float(vp.mean()), sp))
    print("  ON post : %s   media %+.4f   dev.std FRA SEMI %.4f"
          % ("  ".join("%+.4f" % v for v in vo), float(vo.mean()), so))
    print("  CONFRONTO: la SE INTERNA a un run vale ~0.010. La dispersione FRA SEMI vale %.4f / %.4f."
          % (sp, so))
    print("             -> la barra giusta e' %s grande di quella usata nel z = 3.16"
          % ("PIU'" if max(sp, so) > 0.010 else "PIU' PICCOLA o pari"))
    print()
    print("=" * 100)
    print("IL TEST ONESTO - media dei Delta contro la SE della media, dai Delta stessi")
    print("=" * 100)
    d = vo - vp
    md = float(d.mean()); sd = float(np.std(d, ddof=1)); sem = sd / np.sqrt(len(d))
    print("  Delta per seme: %s" % ("  ".join("%+.4f" % v for v in d)))
    print("  media %+.4f   dev.std %.4f   SE della media %.4f   t = %.2f  (gdl %d)"
          % (md, sd, sem, md / sem if sem > 0 else float("nan"), len(d) - 1))
    conc = all(x < 0 for x in d)
    print("  segno concorde su tutti i semi: %s" % ("SI" if conc else "NO"))
    print()
    if conc and abs(md) > 2.0 * sem:
        print("  LETTURA: lo spostamento e' SISTEMATICO. Il z = 3.16 del seme 1 non era")
        print("           dispersione di run, e il 16.9%% recuperato resta il numero da riportare.")
    elif conc:
        print("  LETTURA: segno concorde ma NON separato dal rumore fra semi. Lo spostamento e'")
        print("           plausibile e NON dimostrato: si riporta come tale, senza il z = 3.16.")
    else:
        print("  LETTURA: il segno NON e' concorde. Il z = 3.16 del seme 1 era DISPERSIONE DI RUN,")
        print("           e la frazione '16.9%% recuperato' NON e' un numero che si puo' riportare.")
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main())
