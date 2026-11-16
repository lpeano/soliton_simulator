# -*- coding: utf-8 -*-
r"""**D1, D3, D4, D5 DEL MOTORE NUMBA INTERO** *(il primo passo e il secondo; la carta `doc/TASK_HISTORY/2026-11-15_motore_numba.md`, sez. `4` e `14`)*.

    E:\python\py3132\python.exe csv/solitone/prova_numba_motore.py tempi > doc/referti_l2/motore_numba_tempi.txt     (NUMBA_CACHE_DIR su E:, PYTHONNOUSERSITE=1, TMP su E:)
    ... d3 --fma si|no|esplicita > motore_numba_d3.txt ;  ... d4 --fma si|no|esplicita > motore_numba_d4.txt ;  ... d1 > motore_numba_d1.txt
    ... tempi_fma > motore_numba_tempi_fma.txt   (Luca 2026-11-16 13:58, V5: (a) e (c) i due passi col modo esplicita, a 2 e a 6 fili, alternati due volte; poi (a) di nuovo)

**La scena:** **il mattone di `L 162`** *(`L162_MGU_03000`, `t 63000`; `A`, `E` dal file, `U` dal campo)* **nella scena di S162, il bordo da `R_A 60`; il tick di `mattone.Campi`** *(`MGU`: G+U col lapse; `MU`: senza lapse)*.
**Ogni corsa riparte dal FILE** *(lo stato, `A`, `E`, `e`, `U`)*.
- **D1** *(switch SPENTO)*: **`1000` tick `MGU` e `1000` `MU` senza aver importato `motore_numba`; poi importato e SPENTO, gli stessi: AL BIT ogni `100` tick, ogni chiave; `numba` NON in `sys.modules`.**
- **D3** *(switch ACCESO, i due passi, `6` fili)*: **`1000` tick `MGU` contro spento: la differenza relativa per chiave ogni `100`** *(la soglia `1e-10` alla fine)*; **il picco, il respiro, il centro entro `1e-8`.**
- **D4** *(la riproducibilita')*: **`200` tick `MGU` acceso a `1` filo, a `6`, e di nuovo a `6`: AL BIT fra loro.**
- **TEMPI** *(D5; Luca `23:36`, punto 2)*: **`60` tick `MGU` per ognuno, la mediana degli ultimi `50`** *(`10` di riscaldamento)*: **(a) il motore di oggi; (b) il primo passo a `1`, `2`, `6` fili; (c) i due passi con e senza `fma`, a `1`, `2`, `6`** *(l'accensione, cioe' la compilazione, a parte)*;
  **poi `10` tick con un orologio attorno a ogni funzione sostituita** *(il tempo INCLUSIVO; il peso nel tick di (a), il profilo fine)*; **i giri del punto fisso; il costo di una copia dello stato; il carico della macchina.**
"""
import json
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone as MT  # noqa: E402

FILI_MOLTI = 6
SOLO_FMA = [False]  # ### tempi_fma (C2)
FMA = [None]       # ### d3, d4: --fma si|no|esplicita dalla riga di comando (H1, Luca 23:36; esplicita: Luca 2026-11-16 08:57): il MODO di accendi_secondo_passo
GIRI = []


def leggi_cottura():
    with open(os.path.join(MT.DIR_REF, "cottura_L162_MGU.json"), encoding="utf-8") as fh:
        return json.load(fh)


def riparti(Z, caso, ct, rho_c):
    """### lo stato, `A`, `E`, `e`, `U` DAL FILE; un `Campi` nuovo."""
    import _u1_prototipo as U1
    with np.load(ct["file"]) as d:
        Z["metti"]({k: d[k].copy() for k in Z["chiavi"]})
        A, E = d["campo_A"].copy(), d["campo_E"].copy()
    C = MT.Campi(Z, caso, rho_c, MT.PB.E_DECISO)
    C.campo.A[...] = A
    C.campo.E[...] = E
    C.campo.e = MT.PB.E_DECISO
    C.e_prec = MT.PB.E_DECISO
    U1.scrivi_U(Z["mot"], C.campo)
    return C


def fotografia(Z, C):
    f = {k: Z["st"][k].copy() for k in Z["chiavi"]}
    f["campo_A"], f["campo_E"], f["U"] = C.campo.A.copy(), C.campo.E.copy(), Z["mot"].geo.U.copy()
    return f


def corsa(Z, caso, ct, rho_c, n, ogni, tempi=None):
    """### `n` tick dal file; `{k: fotografia}` ogni `ogni`; i tempi per tick in `tempi`."""
    C = riparti(Z, caso, ct, rho_c)
    t0 = int(ct["t"])
    foto = {}
    for k in range(1, n + 1):
        t = time.perf_counter()
        C.tick(k, t0 + k, 1.0, MT.PB.E_DECISO)
        if tempi is not None:
            tempi.append(time.perf_counter() - t)
        if k % ogni == 0:
            foto[k] = fotografia(Z, C)
    return foto


def rel(a, b):
    den = float(np.max(np.abs(b))) or 1.0
    return float(np.max(np.abs(a - b))) / den


def confronta_al_bit(nome, fa, fb):
    """### per ogni tick e ogni chiave: al bit o no; il numero di chiavi diverse."""
    diverse = 0
    for k in sorted(fa):
        dd = [c for c in fa[k] if not np.array_equal(fa[k][c], fb[k][c])]
        diverse += len(dd)
        print("  %s, k %5d: %d chiavi su %d al bit%s" % (nome, k, len(fa[k]) - len(dd), len(fa[k]), ("; diverse: %s (la differenza relativa massima %.3e)" % (dd, max(rel(fa[k][c], fb[k][c]) for c in dd))) if dd else ""))
        sys.stdout.flush()
    return diverse == 0


def con_giri():
    """### i giri del punto fisso di ogni tick, in memoria *(come `giri_lapse.py`)*: nessun file cambiato."""
    from solitone import tick_lapse as TL
    orig = TL.cs_al_centro

    def contato(*a, **k):
        cs, g = orig(*a, **k)
        GIRI.append(g)
        return cs, g
    TL.cs_al_centro = contato


def d1(Z, ct, rho_c):
    ok = True
    for caso in ("MGU", "MU"):
        assert "motore_numba" not in sys.modules
        a = corsa(Z, caso, ct, rho_c, 1000, 100)
        import motore_numba as MN
        assert MN.MOTORE != "numba"
        b = corsa(Z, caso, ct, rho_c, 1000, 100)
        print("### D1, %s: numba in sys.modules: %s; motore_numba.stato(): %s" % (caso, "numba" in sys.modules, MN.stato()))
        ok = confronta_al_bit("D1 %s, mai importato contro importato e spento" % caso, b, a) and ok and "numba" not in sys.modules
        del sys.modules["motore_numba"]
    return ok


def d3(Z, ct, rho_c):
    import motore_numba as MN
    a = corsa(Z, "MGU", ct, rho_c, 1000, 100)
    MN.accendi_numba(FILI_MOLTI)
    MN.accendi_secondo_passo(FMA[0])
    b = corsa(Z, "MGU", ct, rho_c, 1000, 100)
    print("### D3: motore_numba.stato(): %s" % MN.stato())
    MN.spegni()
    peggio_fine = 0.0
    for k in sorted(a):
        r = {c: rel(b[k][c], a[k][c]) for c in a[k]}
        print("  D3, k %5d: %s" % (k, ", ".join("%s %.2e" % (c, r[c]) for c in sorted(r))))
        if k == max(a):
            peggio_fine = max(v for c, v in r.items() if c != "h_int")
    # ### il picco, il respiro, il centro: dallo stato finale delle due corse
    picchi = []
    for f in (a[max(a)], b[max(b)]):
        Z["metti"]({k: f[k] for k in Z["chiavi"]})
        rho = MT.rho_di(Z)
        picchi.append((float(rho.max()), MT.respiro(rho), MT.centro_di(Z, rho)))
    (pa, sa, ca), (pb, sb, cb) = picchi
    oss = max(abs(pb - pa) / abs(pa), abs(sb - sa) / abs(sa), MT.distanza(Z["L"], ca, cb))
    print("### D3 a k %d: il picco %.12e contro %.12e; il respiro %.12e contro %.12e; il centro %s contro %s; il peggio relativo (la distanza dei centri in nodi) %.3e"
          % (max(a), pb, pa, sb, sa, cb, ca, oss))
    print("  DEVE: la differenza relativa per chiave alla fine sotto 1e-10 (h_int esclusa): %.3e  %s" % (peggio_fine, "PASSA" if peggio_fine < 1e-10 else "### FALLISCE"))
    print("  DEVE: il picco, il respiro, il centro entro 1e-8: %.3e  %s" % (oss, "PASSA" if oss < 1e-8 else "### FALLISCE"))
    # ### la FMA esplicita (C2): AL BIT ATTESO, quindi per quel modo il bit e' un DEVE; per gli altri si stampa e basta
    bit = confronta_al_bit("D3 al bit, numba (%s) contro numpy" % FMA[0], b, a)
    return peggio_fine < 1e-10 and oss < 1e-8 and (bit or FMA[0] != "esplicita")


def d4(Z, ct, rho_c):
    import motore_numba as MN
    out = {}
    for nome, fili in (("1 filo", 1), ("%d fili" % FILI_MOLTI, FILI_MOLTI), ("%d fili, di nuovo" % FILI_MOLTI, FILI_MOLTI)):
        MN.accendi_numba(fili)
        MN.accendi_secondo_passo(FMA[0])
        out[nome] = corsa(Z, "MGU", ct, rho_c, 200, 50)
        MN.spegni()
    n = list(out)
    ok = confronta_al_bit("D4, %s contro %s" % (n[1], n[2]), out[n[1]], out[n[2]])
    ok = confronta_al_bit("D4, %s contro %s" % (n[0], n[1]), out[n[0]], out[n[1]]) and ok
    return ok


OROLOGI = (("flussi_parziali", None, "_grover_mezzo"), ("flussi_parziali", None, "_hop_psi_mezzo"), ("motore", "Motore", "_ruota_attorno_a_n"),
            ("motore", "Motore", "_somma_per_nodo"), ("motore", "Motore", "elicita"), ("motore", "Motore", "densita_materia"),
            ("motore", "Motore", "densita_vuoto"), ("energia_pesata", None, "_per_nodo"), ("energia_pesata", None, "termini_di_h"))
N_CALDO, N_MISURA, N_OROLOGI = 10, 50, 10


def metti_orologi(conto):
    """### un orologio attorno a ogni funzione di `OROLOGI` *(quella che c'e' ORA: la numba se acceso)*; `(bersaglio, nome, prima)` per toglierli.
    ### **Il tempo e' INCLUSIVO:** una funzione chiamata da un'altra conta in tutte e due."""
    tolti = []
    for modulo, classe, nome in OROLOGI:
        m = sys.modules[modulo]
        b = getattr(m, classe) if classe else m
        prima = getattr(b, nome)

        def orologio(*a, _f=prima, _n=nome, **k):
            t = time.perf_counter()
            try:
                return _f(*a, **k)
            finally:
                conto[_n] = conto.get(_n, 0.0) + time.perf_counter() - t
        setattr(b, nome, orologio)
        tolti.append((b, nome, prima))
    return tolti


def togli_orologi(tolti):
    for b, nome, prima in reversed(tolti):
        setattr(b, nome, prima)


def carico():
    import subprocess
    try:
        r = subprocess.run(["tasklist", "/FO", "CSV", "/NH", "/FI", "IMAGENAME eq python.exe"], capture_output=True, text=True, timeout=60).stdout
        return "%d processi python.exe vivi (questo compreso)" % sum(1 for x in r.splitlines() if x.startswith('"python.exe"'))
    except Exception as x:                                                  # ### scritto, mai taciuto
        return "il conto dei processi non riuscito: %r" % x


def tempi(Z, ct, rho_c):
    import flussi_parziali  # noqa: F401
    import energia_pesata  # noqa: F401
    import motore  # noqa: F401
    import motore_numba as MN
    con_giri()
    print("### IL CARICO, all'inizio: %s" % carico())
    t = time.perf_counter()
    for _r in range(10):
        _c = {k: v.copy() for k, v in Z["st"].items() if isinstance(v, np.ndarray)}
    print("### una copia dello stato (tutte le chiavi) %.4f s" % ((time.perf_counter() - t) / 10))
    conf = [("(a) il motore di oggi", 0, None)]
    for f in (1, 2, FILI_MOLTI):
        conf.append(("(b) il primo passo, %d fili" % f, f, "primo"))
    if SOLO_FMA[0]:
        # ### V5 (Luca 2026-11-16 13:58): (a), poi (c) i due passi col modo esplicita a 2 e a 6 fili, ALTERNATI due volte (un carico che cambia si vede)
        conf = [("(a) il motore di oggi", 0, None)]
        for _g in (1, 2):
            for f in (2, FILI_MOLTI):
                conf.append(("(c) i due passi, esplicita, %d fili, giro %d" % (f, _g), f, "esplicita"))
        conf.append(("(a) il motore di oggi, di nuovo", 0, None))
    else:
        for modo in ("contract", "semplice"):
            for f in (1, 2, FILI_MOLTI):
                conf.append(("(c) i due passi, %s, %d fili" % (modo, f), f, modo))
    righe = []
    for nome, fili, passo in conf:
        comp = 0.0
        if fili:
            t = time.perf_counter()
            MN.accendi_numba(fili)
            if passo is not None and passo != "primo":
                MN.accendi_secondo_passo(passo)
            comp = time.perf_counter() - t
        del GIRI[:]
        tt = []
        corsa(Z, "MGU", ct, rho_c, N_CALDO + N_MISURA, N_CALDO + N_MISURA, tt)
        giri = list(GIRI)
        conto = {}
        tolti = metti_orologi(conto)
        to = []
        corsa(Z, "MGU", ct, rho_c, N_OROLOGI, N_OROLOGI, to)
        togli_orologi(tolti)
        if fili:
            MN.spegni()
        med = float(np.median(tt[N_CALDO:]))
        righe.append((nome, med, {k: v / N_OROLOGI for k, v in conto.items()}, sum(to) / N_OROLOGI))
        print("  %-36s la mediana per tick (i tick %d-%d) %.3f s (min %.3f, max %.3f); il riscaldamento %s; l'accensione %.2f s; i giri del punto fisso %s"
              % (nome, N_CALDO + 1, N_CALDO + N_MISURA, med, min(tt[N_CALDO:]), max(tt[N_CALDO:]), ["%.2f" % x for x in tt[:3]], comp, sorted(set(giri))))
        print("      con gli orologi (%d tick a parte, %.3f s per tick): %s" % (N_OROLOGI, righe[-1][3], ", ".join("%s %.3f" % (k, v) for k, v in sorted(righe[-1][2].items()))))
        sys.stdout.flush()
    print("-" * 130)
    a_med, a_f, a_tick = righe[0][1], righe[0][2], righe[0][3]
    if SOLO_FMA[0]:
        print("### (a) all'inizio %.3f s, alla fine %.3f s: la deriva del carico %.1f%%" % (righe[0][1], righe[-1][1], 100.0 * (righe[-1][1] - righe[0][1]) / righe[0][1]))
    print("### IL PESO NEL TICK DI (a)  (il tempo inclusivo per tick / il tick con gli orologi %.3f s):" % a_tick)
    for k in sorted(a_f, key=lambda x: -a_f[x]):
        print("    %-22s %.3f s  %5.1f%%" % (k, a_f[k], 100.0 * a_f[k] / a_tick))
    print("### IL GUADAGNO CONTRO (a)  (la mediana di (a) %.3f s / la mediana):" % a_med)
    for nome, med, f, _t in righe[1:]:
        print("    %-36s %.2fx    %s" % (nome, a_med / med, ", ".join("%s %.1fx" % (k, a_f[k] / f[k]) for k in sorted(f) if f[k] > 0)))
    b1 = [med for nome, med, _f, _t in righe if nome.startswith("(b)")]
    c1 = [med for nome, med, _f, _t in righe if nome.startswith("(c)")]
    if SOLO_FMA[0]:
        print("### IL CARICO, alla fine: %s" % carico())
        return True
    print("### LE ATTESE W4 (scritte prima, non riviste): il primo passo al piu' 1.16x -> il migliore %.2fx; i due passi 1.5-2.5x -> da %.2fx a %.2fx"
          % (a_med / min(b1), a_med / max(c1), a_med / min(c1)))
    print("### IL CARICO, alla fine: %s" % carico())
    return True


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    parte = argv[0]
    assert parte in ("d1", "d3", "d4", "tempi", "tempi_fma")
    if parte in ("d3", "d4"):
        assert len(argv) == 3 and argv[1] == "--fma" and argv[2] in ("si", "no", "esplicita"), "d3, d4: --fma si|no|esplicita"
        FMA[0] = {"no": "semplice", "si": "contract", "esplicita": "esplicita"}[argv[2]]
    SOLO_FMA[0] = parte == "tempi_fma"
    if parte == "tempi_fma":
        parte = "tempi"
    ct = leggi_cottura()
    rho_c = MT.rho_c_assoluto()
    print("=" * 130)
    print("%s DEL MOTORE NUMBA INTERO: %s (t %s); sys.executable %s" % (parte.upper(), ct["file"], ct["t"], sys.executable))
    print("=" * 130)
    t = time.time()
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        ok = {"d1": d1, "d3": d3, "d4": d4, "tempi": tempi}[parte](Z, ct, rho_c)
        Z["metti"]()
    print("=" * 130)
    print("ESITO %s: %s (%.0f s)" % (parte.upper(), "PASSA" if ok else "### FALLISCE", time.time() - t))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
