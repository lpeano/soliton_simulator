# -*- coding: utf-8 -*-
"""**SIGILLO DI `OSSERVABILE-P1`** -- i criteri del task history
(`doc/TASK_HISTORY/2026-09-27_osservabile-p1.md`, committato **prima** dello strumento).

| # | criterio | come si verifica |
|--:|---|---|
| **K1** | grafo **SINTETICO** a distanza NOTA | catena a pesi dati, reticolo Manhattan, due componenti staccate, medoide di una catena: **errore `< 1e-12`** *(e' il `--collaudo` dello strumento, richiamato qui)* |
| **K2** | **il caso che DEVE fallire** | vedi il blocco qui sotto: **il criterio dettato NON E' SODDISFACIBILE A PASSO 0**, e al suo posto c'e' una coppia **piu' forte** |
| **K3** | **invarianza** | stessa rete, **due chiamate**: uguaglianza **ESATTA**, non «entro epsilon» |
| **K4** | **punti di CONTROLLO nel vuoto** | esistono, sono oltre `r_regione` da ogni massa, e stanno **entro il 10 %** dichiarato |
| **K5** | **dispersione fra semi**, `>= 4` | **quattro processi, uno per braccio** (`STANDARD 1`), IC95 con `t(3) = 3.182` |

> ### ❌ **`K2` COME E' STATO DETTATO NON PUO' PASSARE, E IL PERCHE' E' STRUTTURALE.**
> Il criterio era: *«la stessa misura con pesi da `pos` da' un numero DIVERSO sulla scena `(ii)`,
> cosi' si vede che lo strumento usa `d`»*. **MISURATO: `L_d / L_pos = 1.000000` esatto su tutte
> e tre le coppie.** Non e' un difetto dello strumento: **a passo 0 `d` E' la distanza euclidea**,
> perche' `_allaccia` crea l'arco con `d = dd` e `dd` e' la distanza che il KD-tree ha misurato su
> `pos` *(`soliton_simulator.py`, `self.d = np.concatenate([self.d, dd])`)*. **Le due grandezze
> coincidono per COSTRUZIONE**, e un criterio che chiede che differiscano e' della famiglia di
> `Q6` *(«>= 100 volte» una dispersione che vale ZERO)*.
>
> **AL SUO POSTO, UNA COPPIA CHE PROVA LA STESSA COSA MEGLIO -- e nei due versi:**
> **`K2a`** si cambia **solo `d`** *(un arco del cammino minimo x10)* → la distanza **DEVE**
> cambiare; **`K2b`** si cambia **solo `pos`** *(un nodo spostato di `10 LAM`)* → la distanza
> **NON DEVE** cambiare, e **per niente**: uguaglianza esatta.
> **E' piu' forte del criterio dettato**, perche' isola la dipendenza invece di dedurla da due
> numeri diversi. **Il valore `L_d/L_pos = 1.000000` resta stampato: e' la PROVA del perche'.**

**Nessun run lungo:** la scena si costruisce e si misura, **zero passi di dinamica**.

    python csv/_seal_fork/_sigillo_osservabile_p1.py            # tutto
    python csv/_seal_fork/_sigillo_osservabile_p1.py --corto    # senza K5 (i quattro processi)

ASCII puro.
"""
import io
import json
import os
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))

import _presidio                                                       # noqa: E402
import _cli_flag                                                       # noqa: E402
import _osservabile_p1 as OP                                           # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
DEST = os.path.join(_QUI, "_sig_osservabile_p1")
REFERTO = os.path.join(DEST, "REFERTO.txt")
STRUM = "csv/_osservabile_p1.py"
SEMI = [11, 12, 13, 14]
R = []


def P(s=""):
    print(s)
    R.append(s)


if __name__ == "__main__":
    corto = "--corto" in sys.argv[1:]
    if not os.path.isdir(DEST):
        os.makedirs(DEST)
    P("=" * 104)
    P("SIGILLO DI `OSSERVABILE-P1`%s" % ("   (GIRO CORTO: senza K5)" if corto else ""))
    P("=" * 104)
    esiti = []

    # ------------------------------------------------------------------ K1
    q = subprocess.run([sys.executable, STRUM, "--collaudo"], cwd=RADICE,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    ok1 = (q.returncode == 0) and ("FALLITO" not in (q.stdout or ""))
    P("")
    P("  K1  GRAFI SINTETICI A DISTANZA NOTA  (il `--collaudo` dello strumento)")
    for r in (q.stdout or "").split(NL):
        if "atteso" in r or "COLLAUDO `K1`" in r:
            P("      %s" % r.strip())
    esiti.append(("K1  grafo sintetico, errore < 1e-12", ok1))

    # ------------------------------------------------------------------ la scena, UNA VOLTA
    S, coorti, rr, argv = OP.da_scena()
    P("")
    P("  la scena: n %d   archi %d   sep %.6f   r_regione %.6f"
      % (S.net.n, len(S.net.d), S._NMASSE_VIDEO["sep"], rr))
    o = OP.misura(S.net, coorti)
    nomi = sorted(o["coppie"])

    # ------------------------------------------------------------------ K2: la coppia sostitutiva
    op = OP.misura(S.net, coorti, pesi_da_pos=True)
    rapporti = {}
    for k in nomi:
        lp = op["coppie"][k]["centro_centro"]
        rapporti[k] = (o["coppie"][k]["centro_centro"] / lp) if lp else float("nan")
    P("")
    P("  K2  IL CASO CHE DEVE FALLIRE -- e il criterio DETTATO non e' soddisfacibile a passo 0")
    for k in nomi:
        P("      %-22s L_d %12.6f   L_pos %12.6f   L_d/L_pos %.9f"
          % (k, o["coppie"][k]["centro_centro"], op["coppie"][k]["centro_centro"], rapporti[k]))
    coincidono = all(abs(rapporti[k] - 1.0) < 1e-12 for k in nomi)
    P("      -> `d` e la distanza da `pos` COINCIDONO a passo 0: %s" % coincidono)
    P("         e' STRUTTURALE: `_allaccia` crea l'arco con `d = dd`, e `dd` e' la distanza")
    P("         che il KD-tree ha misurato su `pos`. Il criterio dettato chiede che differiscano,")
    P("         e a passo 0 NON POSSONO: e' la famiglia di `Q6`. Sostituito dalla coppia K2a/K2b.")

    # K2a: si cambia SOLO `d` -> la distanza DEVE cambiare
    d_orig = np.asarray(S.net.d, float).copy()
    pos_orig = np.asarray(S.net.pos, float).copy()
    ka = nomi[0]
    ca, cb = o["centri"][ka.split("|")[0]], o["centri"][ka.split("|")[1]]
    g, _u, _s = OP.grafo(S.net.i, S.net.j, S.net.d, S.net.n)
    from scipy.sparse.csgraph import dijkstra as _dij
    dist, pred = _dij(g, directed=False, indices=ca, return_predecessors=True)
    cammino, x = [], cb
    while x != ca and x >= 0:
        cammino.append(x)
        x = pred[x]
    cammino.append(ca)
    # l'arco fra i primi due nodi del cammino: si trova per indice, non per posizione
    a1, a2 = cammino[0], cammino[1]
    ii = np.asarray(S.net.i, int)
    jj = np.asarray(S.net.j, int)
    sel = np.where(((ii == a1) & (jj == a2)) | ((ii == a2) & (jj == a1)))[0]
    S.net.d = d_orig.copy()
    S.net.d[sel] = d_orig[sel] * 10.0
    o_d = OP.misura(S.net, coorti)
    S.net.d = d_orig.copy()
    cambiata = o_d["coppie"][ka]["centro_centro"] != o["coppie"][ka]["centro_centro"]
    P("")
    P("      K2a  cambio SOLO `d` (arco %s del cammino minimo, x10, %d arco/i):"
      % (str(tuple(sorted((int(a1), int(a2))))), len(sel)))
    P("           prima %12.6f   dopo %12.6f   CAMBIATA %s"
      % (o["coppie"][ka]["centro_centro"], o_d["coppie"][ka]["centro_centro"], cambiata))
    # K2b: si cambia SOLO `pos` -> la distanza NON deve cambiare, per niente
    S.net.pos = pos_orig.copy()
    S.net.pos[ca] = pos_orig[ca] + 10.0 * float(S.LAM)
    o_p = OP.misura(S.net, coorti)
    S.net.pos = pos_orig.copy()
    identica = all(o_p["coppie"][k]["centro_centro"] == o["coppie"][k]["centro_centro"]
                   for k in nomi)
    P("      K2b  cambio SOLO `pos` (nodo %d spostato di 10 LAM = %.6f):"
      % (ca, 10.0 * float(S.LAM)))
    for k in nomi:
        P("           %-22s prima %12.6f   dopo %12.6f"
          % (k, o["coppie"][k]["centro_centro"], o_p["coppie"][k]["centro_centro"]))
    P("           IDENTICHE (uguaglianza esatta) %s" % identica)
    esiti.append(("K2a cambio `d` -> la distanza CAMBIA", bool(cambiata)))
    esiti.append(("K2b cambio `pos` -> la distanza NON cambia", bool(identica)))

    # ------------------------------------------------------------------ K3
    o2 = OP.misura(S.net, coorti)
    ident3 = all(o2["coppie"][k]["centro_centro"] == o["coppie"][k]["centro_centro"]
                 for k in nomi) and o2["centri"] == o["centri"]
    P("")
    P("  K3  INVARIANZA -- stessa rete, due chiamate")
    P("      centri uguali %s   distanze uguali (ESATTE) %s"
      % (o2["centri"] == o["centri"], ident3))
    esiti.append(("K3  due chiamate -> stesso numero, esatto", bool(ident3)))

    # ------------------------------------------------------------------ K4
    c = OP.controlli(o, coorti, rr)
    dentro = [v["entro_toll"] for v in (c.get("coppie") or {}).values()]
    P("")
    P("  K4  PUNTI DI CONTROLLO NEL VUOTO  (tolleranza %d %%, dichiarata PRIMA)"
      % int(100 * OP.TOLL_CONTROLLO))
    P("      candidati oltre r_regione (%.6f) dalle masse .... %d"
      % (c.get("metro_lontananza", float("nan")), c.get("candidati_lontani", 0)))
    for k, v in sorted((c.get("coppie") or {}).items()):
        P("      %-22s controllo %12.6f   bersaglio %12.6f   scarto %6.3f %%   entro %s"
          % (k, v["distanza"], v["bersaglio"], 100.0 * v["scarto_relativo"],
             "SI" if v["entro_toll"] else "NO"))
    ok4 = bool(dentro) and all(dentro)
    esiti.append(("K4  controlli nel vuoto entro il 10 %", ok4))

    # ------------------------------------------------------------------ K5
    if corto:
        P("")
        P("  K5  SALTATO nel giro corto (quattro processi dello strumento).")
    else:
        P("")
        P("  K5  DISPERSIONE FRA SEMI -- quattro processi, uno per braccio (`STANDARD 1`)")
        val = {}
        for s in SEMI:
            jf = os.path.join(DEST, "seme_%d.json" % s)
            qq = subprocess.run([sys.executable, STRUM, "--scena", "--semi", str(s),
                                 "--json", os.path.relpath(jf, RADICE)],
                                cwd=RADICE, capture_output=True, text=True,
                                encoding="utf-8", errors="replace")
            if qq.returncode or not os.path.exists(jf):
                P("      seme %-4d uscita %d  ** %s" % (s, qq.returncode,
                                                        (qq.stderr or "").strip()[-140:]))
                continue
            dd = json.load(io.open(jf, encoding="utf-8"))
            per = dd["semi"][str(s)]
            P("      seme %-4d n %-6d sep %.4f   %s" % (s, per["n"], dd["sep"], "   ".join(
                "%s=%.6f" % (k.replace("massa_", "m"), v["centro_centro"])
                for k, v in sorted(per["coppie"].items()))))
            for k, v in per["coppie"].items():
                val.setdefault(k, []).append(float(v["centro_centro"]))
        ok5 = bool(val) and all(len(v) >= 4 for v in val.values())
        for k in sorted(val):
            d = OP.dispersione(val[k])
            P("      %-22s media %12.6f   sd %10.6f   t(%d) %.3f   IC95 [%.6f, %.6f]"
              % (k, d["media"], d["sd"], d["gdl"], d["t"] or 0,
                 (d["ic95"] or (float("nan"),) * 2)[0], (d["ic95"] or (float("nan"),) * 2)[1]))
            if d.get("nota"):
                P("          nota: %s" % d["nota"])
        P("      semi con tutte le coppie: %s   (ne servono >= 4, `P3`)"
          % (min(len(v) for v in val.values()) if val else 0))
        esiti.append(("K5  >= 4 semi, con la barra fra semi", ok5))

    # ------------------------------------------------------------------ la configurazione, INTERA
    P("")
    _cli_flag.dichiara_configurazione(S, P)

    P("")
    P("=" * 104)
    for nome, ok in esiti:
        P("  %-46s %s" % (nome, "PASS" if ok else "** FAIL **"))
    buoni = len([1 for _n, ok in esiti if ok])
    P("SIGILLO: %d/%d" % (buoni, len(esiti)))
    P("=" * 104)
    P()
    P("COSA QUESTO SIGILLO *NON* DICE:")
    P("  - **non fa la `PROVA 1`**: certifica la GRANDEZZA, non che le masse si avvicinino.")
    P("    Tutti i numeri sono al PASSO 0, cioe' la condizione iniziale.")
    P("  - **`K2` non e' il criterio dettato**: quello non e' soddisfacibile a passo 0, perche'")
    P("    `d` E' la distanza euclidea per costruzione. La coppia `K2a`/`K2b` prova la stessa")
    P("    cosa in modo piu' forte, e il rapporto `L_d/L_pos = 1.000000` resta stampato come")
    P("    PROVA del perche'.")
    P("  - **`K4` dice che i punti di controllo ESISTONO al passo 0**, non che restino validi")
    P("    mentre il sistema evolve: quello si rimisura a ogni istante in cui si legge la prova.")
    io.open(REFERTO, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print(NL + "scritto %s" % os.path.relpath(REFERTO, RADICE).replace(chr(92), "/"))
    sys.exit(0 if buoni == len(esiti) else 1)
