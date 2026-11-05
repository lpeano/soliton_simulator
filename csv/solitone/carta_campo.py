# -*- coding: utf-8 -*-
r"""**FIN DOVE ARRIVA IL CAMPO: I PROFILI E LE MAPPE LEGGERE DA `TM1000`** *(Luca, `2026-11-03` `18:26`; il task history `doc/TASK_HISTORY/2026-11-03_campo_TM1000.md`)*
    python csv/solitone/carta_campo.py > doc/referti_l2/campo_TM1000.txt
    python csv/solitone/carta_campo.py --corsa TM3 > doc/referti_l2/campo_TM3.txt     # (Luca 19:34) TM3 + TM3C, F3; gli indici mappe_indice_TM3.txt, mappe_indice_TM3C.txt
    python csv/solitone/carta_campo.py --corsa TB3 > doc/referti_l2/campo_TB3.txt     # (Luca 2026-11-04 sera) TB3, F3 col bordo; l'indice mappe_indice_TB3.txt
    python csv/solitone/carta_campo.py --corsa TBS > doc/referti_l2/campo_TBS.txt     # (Luca 2026-11-05 19:24) TBS, F3 col bordo, la partenza simmetrizzata; l'indice mappe_indice_TBS.txt
### **Nessuna corsa: `E:` solo in lettura** *(le mappe di `TM1000`, al bit di `TP1000`, `0 .. 16000`, `F0`)*. ### **Scrive nel repo:** `doc/referti_l2/campo_TM1000/profili.npz` *(`float32`:
i profili ad anelli di `rho`, `Lambda`, `|Lambda - Lambda(t 0)|` e `Lambda - Lambda(t 0)` di ogni istantanea, quelli di `t 0`, i centri, la portata)* e `mappe_leggere.npz` *(una ogni
`OGNI_LEGGERA` istantanee: `rho` e `Lambda - Lambda(t 0)` per nodo in `float16`)*.
### **I DEVE:** `F0` lo `sha1` di ogni file = l'indice *(`doc/referti_l2/mappe_indice.txt`)*; `F0-F` *(deve fallire)* lo `sha1` del primo file contro la riga del secondo; `F1` le somme di
`rho` e `Lambda` = `M` e `V` del campione di `TP1000` allo stesso `t` entro `TOLL`; `F1-F` *(deve fallire)* il nodo piu' denso raddoppiato; `F2` `Lambda(t 0)` uniforme entro `TOLL`
*(la simmetria attesa, dichiarata)*; `F3` `rho(t 0)` della mappa = la densita' della partenza ricalcolata *(`V.partenza`)* entro `TOLL` *(per `rho(t 0)` nessuna simmetria esatta:
`3.67e-2` contro `R180`, `impulso_partenza.txt`)*. ### **La portata** *(`campo.portata`)*: `rho` contro `SOGLIE_RHO` della media dell'anello `0`; `|Lambda - Lambda(t 0)|` contro
`SOGLIA_L` della media di `Lambda(t 0)`; la tabella a blocchi di `BLOCCO`.
"""
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

PARTI = {"TM1000": (("TM1000", "TP1000"),),                      # ### la corsa: (le corse con le mappe, la gemella al bit coi campioni nel repo)
         "TM3": (("TM3", "TF3"), ("TM3C", "TF3C")),              # ### Luca 19:34: TF3 + TF3C con le mappe (due corse: lo sha_fine al bit pezzo per pezzo)
         "TB3": (("TB3", "TB3"),),                               # ### Luca 2026-11-04 sera: TB3 ha le mappe e i campioni (nel repo) nella stessa corsa, nessuna gemella
         "TBS": (("TBS", "TBS"),)}                               # ### Luca 2026-11-05 19:24: come TB3 (le mappe e i campioni nella stessa corsa)
INDICI = {"TM1000": ("mappe_indice.txt",), "TM3": ("mappe_indice_TM3.txt", "mappe_indice_TM3C.txt"), "TB3": ("mappe_indice_TB3.txt",), "TBS": ("mappe_indice_TBS.txt",)}   # ### corsa_accensione.py --indice <nome>
SOGLIE_RHO = (1e-3, 1e-4, 1e-5)   # ### Luca 18:26
SOGLIA_L = 1e-3                # ### Luca 18:26
TOLL = 1e-6                    # ### Luca 18:26 (come K2 di TM1000: float32)
BLOCCO = 500.0                 # ### Luca 18:26: la tabella a blocchi di 500 unita'
OGNI_LEGGERA = 10              # ### Luca 18:26: una ogni 10 istantanee ...
TETTO_MB = 10.0                # ### ... se supera 10 MB, una ogni 20
DIR_REF = os.path.join(solitone.RADICE, "doc", "referti_l2")

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


def indice(corsa):
    """### **Le righe delle mappe negli indici della corsa:** `{percorso: (byte, sha1)}`, nell'ordine *(le parti nell'ordine di `PARTI`)*."""
    out = {}
    for (p, _g), nf in zip(PARTI[corsa], INDICI[corsa]):
        with open(os.path.join(DIR_REF, nf), encoding="utf-8") as f:
            for riga in f:
                m = re.search(r"(E:\\soliton_simulator\\mappe\\%s\\%s_\d+\.npz)\s+(\d+) byte\s+sha1 ([0-9a-f]{40})" % (p, p), riga)
                if m:
                    out[m.group(1)] = (int(m.group(2)), m.group(3))
    return out


def salva(percorso, **dati):
    os.makedirs(os.path.dirname(percorso), exist_ok=True)
    tmp = percorso + ".tmp.npz"
    np.savez_compressed(tmp, **dati)
    os.replace(tmp, percorso)
    return os.path.getsize(percorso)


def main(argv):
    corsa = argv[argv.index("--corsa") + 1] if "--corsa" in argv else "TM1000"
    parti = PARTI[corsa]
    DIR_OUT = os.path.join(DIR_REF, "campo_%s" % corsa)
    import _energia_del_legame as EL
    import _presidio
    import _vuoto_vivo_B as V
    from solitone import campo as CP
    from solitone import corsa_accensione as CA
    from solitone import mappe as MP
    from solitone import toro as TO
    for m in ("__init__", "toro", "mappe", "campo", "corsa_accensione"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    print("=" * 130)
    print("FIN DOVE ARRIVA IL CAMPO (Luca 2026-11-03 18:26): le mappe di %s (al bit di %s; il vuoto %s) su E:, solo lettura; SOGLIE_RHO %s SOGLIA_L %g TOLL %g BLOCCO %g OGNI_LEGGERA %d TETTO_MB %g"
          % ("+".join(p for p, _g in parti), "+".join(g for _p, g in parti), "F3" if corsa in ("TM3", "TB3", "TBS") else "F0", SOGLIE_RHO, SOGLIA_L, TOLL, BLOCCO, OGNI_LEGGERA, TETTO_MB))
    print("  le definizioni (campo.py, dichiarate nel task history): gli anelli [k, k+1) fino alla meta' del periodo; la media al centro = l'anello 0; la portata: R_contiguo (il primo")
    print("  anello che NON supera la soglia, il bordo interno; nan = mai entro R) e R_ultimo (il bordo esterno dell'ultimo che la supera); Lambda - Lambda(t 0) per nodo")
    print("=" * 130)
    idx = indice(corsa)
    files = list(idx)
    sha_letti = {f: MP.sha1(f) for f in files}
    presenti = sorted(os.path.join(MP.RADICE, p, n) for p, _g in parti for n in os.listdir(os.path.join(MP.RADICE, p)) if n.endswith(".npz"))
    esito("DEVE PASSARE: F0 lo sha1 di ogni file delle mappe = l'indice, e i file su E: sono quelli dell'indice", all(sha_letti[f] == idx[f][1] for f in files) and presenti == sorted(files),
          "%d file nell'indice, %d su E:" % (len(files), len(presenti)))
    esito("DEVE FALLIRE: F0-F lo sha1 del primo file = la riga del secondo", sha_letti[files[0]] != idx[files[1]][1], "")
    camp = [c for _p, g in parti for c in CA.serie(g)[1]]
    MV = {c["t"]: (c["E"]["totale"]["M"], c["E"]["totale"]["V"]) for c in camp}
    with V.scena(s, vuoto, V.EPS) as (_rec, z, phi0, pK):
        L, m1, m2 = z["L"], np.asarray(z["m1"]), np.asarray(z["m2"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        p0, _info = V.partenza(sol, z, phi0, pK, s)
        if corsa in CA.SIMMETRIZZATE:      # ### TBS (Luca 19:24): la partenza della corsa e' la simmetrizzata di TS (corsa_accensione.partenza_ts), non V.partenza
            p0 = CA.partenza_ts(z, phi0, pK, s)["psi"]
        st = dict(salvato)
        st["psi_h"] = p0
        rho_p, _l = EL.densita(z["inc"], st)
        for k, v in salvato.items():
            z["st"][k][...] = v
    R = TO.meta_periodo(L)
    n = CP.quanti(R)
    tt, cen, cen_mappa, PR, PL, PA, PS, por_r, por_l = [], [], [], [], [], [], [], [], []
    legg_t, legg_r, legg_l, legg_c = [], [], [], []
    eM = eV = 0.0
    manca = 0
    L0 = r0 = None
    i_glob = 0
    for f in files:
        with np.load(f) as d:
            assert np.array_equal(d["d1"] + L // 2, m1) and np.array_equal(d["d2"] + L // 2, m2), "l'ordine dei nodi della mappa NON e' quello della scena"
            T, RH, LA, CE = d["t"], d["rho"], d["Lambda"], d["centro"]
        for i in range(len(T)):
            rho = RH[i].astype(np.float64)
            la = LA[i].astype(np.float64)
            t = int(T[i])
            if t in MV:
                eM = max(eM, abs(float(rho.sum()) / MV[t][0] - 1.0))
                eV = max(eV, abs(float(la.sum()) / MV[t][1] - 1.0))
            else:
                manca += 1
            if L0 is None:
                L0, r0 = la.copy(), rho.copy()
                rho_doppio = None
            elif rho_doppio is None:
                rho_doppio = rho.copy()
                rho_doppio[int(np.argmax(rho_doppio))] *= 2.0
                eF = abs(float(rho_doppio.sum()) / MV[t][0] - 1.0)
            c1, c2, x, y = TO.centro(rho, m1, m2, L)
            k, _rr = CP.anelli(m1, m2, c1, c2, L, R)
            dl = la - L0
            pr, pl, pa, ps = CP.profilo(rho, k, n), CP.profilo(la, k, n), CP.profilo(np.abs(dl), k, n), CP.profilo(dl, k, n)
            tt.append(t)
            cen.append((c1, c2, x, y))
            cen_mappa.append(TO.distanza((x, y), CE[i], L))
            PR.append(pr)
            PL.append(pl)
            PA.append(pa)
            PS.append(ps)
            por_r.append([v for sg in SOGLIE_RHO for v in CP.portata(pr, sg * pr[0])])
            por_l.append(list(CP.portata(pa, SOGLIA_L * float(L0.mean()))))
            if i_glob % OGNI_LEGGERA == 0:
                legg_t.append(t)
                legg_r.append(rho.astype(np.float16))
                legg_l.append(dl.astype(np.float16))
                legg_c.append((c1, c2))
            i_glob += 1
    esito("DEVE PASSARE: F1 sum rho = M e sum Lambda = V del campione di %s allo stesso t, entro %g relativo, ogni istantanea" % ("+".join(g for _p, g in parti), TOLL), eM <= TOLL and eV <= TOLL and manca == 0,
          "%d istantanee; il peggiore M %.2e, V %.2e; senza campione %d" % (len(tt), eM, eV, manca))
    esito("DEVE FALLIRE: F1-F la seconda istantanea col nodo piu' denso raddoppiato: sum rho = M entro %g" % TOLL, not eF <= TOLL, "l'errore %.2e" % eF)
    sp = float(L0.std() / L0.mean())
    esito("DEVE PASSARE: F2 Lambda(t 0) uniforme (la simmetria attesa, dichiarata): std / media entro %g" % TOLL, sp <= TOLL, "%.3e (la media %.9f, min %.9f, max %.9f)" % (sp, L0.mean(), L0.min(), L0.max()))
    e3 = float(np.linalg.norm(r0 - rho_p) / np.linalg.norm(rho_p))
    esito("DEVE PASSARE: F3 rho(t 0) della mappa = la densita' della partenza ricalcolata (V.partenza), entro %g relativo" % TOLL, e3 <= TOLL, "%.3e" % e3)
    print("  il centro ricalcolato dalla rho float32 contro quello salvato nella mappa (dal campione): il massimo %.3e nodi (registrato)" % max(cen_mappa))
    # ------------------------------------------------------------------ i file nel repo
    tt = np.array(tt)
    por_r, por_l = np.array(por_r), np.array(por_l)
    b_pro = salva(os.path.join(DIR_OUT, "profili.npz"), t=tt, tempo=(tt * s).astype(np.float32), centro=np.array(cen, dtype=np.float32), rho=np.array(PR, dtype=np.float32),
                  Lambda=np.array(PL, dtype=np.float32), dLambda_abs=np.array(PA, dtype=np.float32), dLambda=np.array(PS, dtype=np.float32), rho_t0=np.array(PR[0], dtype=np.float32),
                  Lambda_t0=np.array(PL[0], dtype=np.float32), anelli_bordo_interno=np.arange(n, dtype=np.float32), R=np.float32(R),
                  portata_rho=por_r.astype(np.float32), soglie_rho=np.array(SOGLIE_RHO), portata_dLambda=por_l.astype(np.float32), soglia_L=np.float64(SOGLIA_L))
    ogni = OGNI_LEGGERA
    while True:
        sel = [j for j in range(len(legg_t)) if (j * OGNI_LEGGERA) % ogni == 0]
        b_leg = salva(os.path.join(DIR_OUT, "mappe_leggere.npz"), t=np.array(legg_t)[sel], tempo=(np.array(legg_t)[sel] * s).astype(np.float32), rho=np.stack([legg_r[j] for j in sel]),
                      dLambda=np.stack([legg_l[j] for j in sel]), centro=np.array([legg_c[j] for j in sel], dtype=np.float32), d1=(m1 - L // 2).astype(np.int16),
                      d2=(m2 - L // 2).astype(np.int16), L=np.int64(L), ogni=np.int64(ogni))
        if b_leg <= TETTO_MB * 1e6 or ogni >= 2 * OGNI_LEGGERA:
            break
        ogni = 2 * OGNI_LEGGERA
    print("  ### profili.npz %d byte; mappe_leggere.npz %d byte (%d mappe, una ogni %d istantanee%s)"
          % (b_pro, b_leg, len(sel), ogni, "" if b_leg <= TETTO_MB * 1e6 else "; ### OLTRE IL TETTO anche a una ogni 20"))
    print("  float16: rho fino a %.4e (il massimo float16 65504); la precisione relativa float16 ~1e-3 (dichiarata)" % max(float(x.max()) for x in legg_r))
    # ------------------------------------------------------------------ la tabella
    print("-" * 130)
    print("### LA PORTATA, a blocchi di %g: la media sulle istantanee del blocco di R_contiguo e il massimo di R_ultimo (nodi); n = quante istantanee non scendono mai (R_contiguo nan)" % BLOCCO)
    print("  %-17s %4s  %-26s %-26s %-26s %-26s" % ("blocco", "ist", "rho 1e-3 contig/ult (n)", "rho 1e-4", "rho 1e-5", "|dLambda| 1e-3 di L(t0)"))
    tempo = tt * s

    def cella(col_c, col_u, m):
        cc = col_c[m]
        ok = np.isfinite(cc)
        return "%6.2f / %5.1f (%d)" % (float(cc[ok].mean()) if ok.any() else float("nan"), float(col_u[m].max()), int((~ok).sum()))

    for a in np.arange(0.0, tempo[-1] + 1e-9, BLOCCO):
        m = (tempo >= a) & (tempo < a + BLOCCO)
        if not m.any():
            continue
        print("  %7.0f .. %7.0f %4d  %-26s %-26s %-26s %-26s" % (a, a + BLOCCO, int(m.sum()), cella(por_r[:, 0], por_r[:, 1], m), cella(por_r[:, 2], por_r[:, 3], m),
                                                         cella(por_r[:, 4], por_r[:, 5], m), cella(por_l[:, 0], por_l[:, 1], m)))
    print("-" * 130)
    print("### I PROFILI DI t 0, %g, %g, %g (rho e |Lambda - Lambda(t 0)| per anello, ogni 5 anelli)" % tuple(tempo[[len(tt) // 3, 2 * len(tt) // 3, len(tt) - 1]]))
    for j in [0, len(tt) // 3, 2 * len(tt) // 3, len(tt) - 1]:
        print("  tempo %8.2f rho %s" % (tempo[j], " ".join("%.2e" % v for v in PR[j][::5])))
        print("  %14s |dL| %s" % ("", " ".join("%.2e" % v for v in PA[j][::5])))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
