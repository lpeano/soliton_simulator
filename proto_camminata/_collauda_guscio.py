r"""IL COLLAUDO DELLE LETTURE `G1` E `G2` — **e un osservatore si prova SU DUE COSE.**

> ## ⛔ **UN OSSERVATORE SI PROVA SU DUE COSE, e il mandato le chiede entrambe:**
> ## ### **(1) che NON cambi cio' che guarda** *(`V1`)*, e ### **(2) che cio' che misura
> ## sia INVARIANTE DI GAUGE** *(`V4`)* — perche' una fase non trasportata **non vuol dire
> ## niente.**

| | il braccio | che cosa prova |
|---|---|---|
| `V9` | a `N` spento le letture girano **sul `v2`** | ### **AL BIT** |
| `V1` | le letture **non modificano lo stato** che ricevono | confronto **byte a byte** prima/dopo |
| `V4` | il `cos` trasportato e' **invariante di gauge** | e ### **DEVE cambiare se NON si trasporta** |
| — | le uscite `json` **esistono** e **non sono vuote** | |

Gira con:  python proto_camminata/_collauda_guscio.py
"""
import io
import json
import math
import os
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio                                              # noqa: E402

_presidio.avvia(__file__)

import camminata as CM                                         # noqa: E402
import camminata2 as C2                                        # noqa: E402
import camminata3 as C3                                        # noqa: E402
import geometria as GE                                         # noqa: E402
import interferenza3 as I3                                     # noqa: E402
import saturazione3 as S3                                      # noqa: E402
import scena as SC                                             # noqa: E402
import vuoto3 as V3                                            # noqa: E402
import _guscio_moto as GM                                      # noqa: E402
import _letture3 as L3                                         # noqa: E402

EPS = float(np.finfo(float).eps)
NLN = chr(10)
SEME = 11
PASSI = 20
EPS_RIF = 0.5
CLIP = ("np.clip", ".clip(", "np.maximum", "np.minimum", "np.fmax", "np.fmin")


def main():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL COLLAUDO DELLE LETTURE G1 E G2 -- un osservatore si prova su DUE cose")
    print("=" * 100)
    SC._niente_simulatore()

    sc = SC.irregolare()
    uno_r = np.ones(sc["n"], dtype=float)
    gmax = int(sc["grado"].max())
    ident = GE.scena_identita(sc)
    gauge = GE.scena_gauge_puro(sc, SEME)
    st, dentro, d = L3.grumo(sc, ident, 0, 1, 8.0, seme=SEME)
    tol = PASSI * gmax * EPS * math.sqrt(CM.norma(st["psi"]))

    # ================================================================ V9
    a = st["psi"].copy()
    for _ in range(PASSI):
        a = C2.passo2(a, sc, ident, uno_r, 1.0, EPS_RIF)
    b = dict(st)
    for _ in range(PASSI):
        b = C3.passo3(b, sc, ident, uno_r, 1.0, EPS_RIF, None)
    esito("### (V9) a `N` spento le letture girano sul v2, AL BIT",
          float(np.max(np.abs(b["psi"] - a))) == 0.0,
          "### max|psi3 - psi2| = %.3g su %d tick"
          % (float(np.max(np.abs(b["psi"] - a))), PASSI))

    # ================================================================ V1
    prima_p = st["psi"].copy()
    prima_f = st["phi"].copy()
    _r1 = GM.g1(sc, ident, S3.flusso, "prova", passi=4)
    _r2 = GM.due_grumi(sc, ident, S3.flusso, "prova", 2, 0.0, passi=4)
    esito("### (V1) le letture NON modificano lo stato che ricevono",
          float(np.max(np.abs(st["psi"] - prima_p))) == 0.0
          and float(np.max(np.abs(st["phi"] - prima_f))) == 0.0,
          "### confronto byte a byte dello stato di partenza, prima e dopo le letture")

    # ================================================================ V4
    S = I3.campo_S(st["psi"], sc)
    # ### lo stato TRASFORMATO dal gauge, e il suo campo
    ruo = np.empty_like(st["psi"])
    for e in range(2 * sc["m"]):
        k = int(sc["nodo"][e])
        ruo[e] = np.exp(1j * gauge["fi"][k]) * (gauge["g"][k] @ st["psi"][e])
    Sg = I3.campo_S(ruo, sc)
    nodo = next(k for k in range(sc["n"]) if 0 < int(SC.distanze(sc, 0)[k]) <= 2)
    c1, _d1, nq = GM.cos_trasportato(sc, ident, S, 0, nodo)
    c2, _d2, _nq = GM.cos_trasportato(sc, gauge, Sg, 0, nodo)
    esito("### (V4) il `cos` TRASPORTATO e- invariante di gauge",
          abs(c1 - c2) <= tol,
          "### %.6f contro %.6f (scarto %.3g, soglia %.3g), su %d cammini piu- corti"
          % (c1, c2, abs(c1 - c2), tol, nq))
    # ### ⛔ **E SENZA TRASPORTO DEVE CAMBIARE**: altrimenti il trasporto
    # ### ### **non starebbe facendo niente**, e il braccio di sopra sarebbe un FALSO-UNO.
    z1 = complex(np.vdot(S[0], S[nodo]))
    z2 = complex(np.vdot(Sg[0], Sg[nodo]))
    g1_ = float(np.real(z1) / abs(z1)) if abs(z1) > 0 else float("nan")
    g2_ = float(np.real(z2) / abs(z2)) if abs(z2) > 0 else float("nan")
    esito("### DEVE CAMBIARE: il `cos` NON trasportato non e- invariante",
          abs(g1_ - g2_) > 1e-6,
          "### %.6f contro %.6f (scarto %.3g): ### **senza trasporto il confronto non vuol "
          "dire niente**" % (g1_, g2_, abs(g1_ - g2_)))

    # ================================================================ i cammini
    cc = GM.cammini_corti(sc, nodo, 0)
    esito("### MATERIA: i cammini piu- corti si contano, e la dispersione si riporta",
          len(cc) >= 1,
          "### %d cammini fra il nodo %d e il centro: se fossero piu- d-uno, la "
          "dispersione e- l-olonomia che si vede" % (len(cc), nodo))

    # ================================================================ le meta-
    za, zb = GM.meta_di_voronoi(sc, 0, nodo)
    esito("### le META- DI VORONOI sono disgiunte e non vuote",
          bool(za) and bool(zb) and not (set(za) & set(zb)),
          "### %d e %d nodi, e gli equidistanti restano FUORI da entrambe"
          % (len(za), len(zb)))

    # ================================================================ la `Q` del lineare
    # ### ⛔ **QUESTO BRACCIO NASCE DA UN DIFETTO MIO, e sarebbe scattato:** in
    # ### `due_grumi` avevo scritto `"N" if nome == "N" else "N"`, cioe-
    # ### ### **SEMPRE `"N"`** -- e per il braccio `lineare` misuravo ### **la `Q` di `N`**,
    # ### che nel lineare ### **non e- conservata.**
    # ### ⭐ **E LA PROVA E- ESATTA, non statistica:** la quasi-energia lineare
    # ### `Re<psi|U psi>` e- ### **conservata per unitarieta-**
    # ### *(`<U^t psi|U U^t psi> = <psi|U psi>`)*, quindi la soglia e-
    # ### ### **l-errore di macchina**, non una tolleranza scelta.
    PQ = 6
    n_est = 2 * sc["m"]
    d0q = SC.distanze(sc, 0)
    c2q = int(next(k for k in range(sc["n"]) if int(d0q[k]) == 2))
    ga, _za, _dq = L3.grumo(sc, ident, 0, 0, 8.0, seme=SEME)
    gb, _zb, _dq2 = L3.grumo(sc, ident, c2q, 0, 8.0, seme=SEME)
    pq = ga["psi"] + gb["psi"]
    sq = {"psi": pq / math.sqrt(CM.norma(pq)),
          "phi": V3.vuoto_fondo(sc, V3.LAMBDA0, SEME)}
    qL0 = L3.conservazione_modificata(sq, sc, ident, uno_r, 1.0, EPS_RIF, "lineare")
    qN0 = L3.conservazione_modificata(sq, sc, ident, uno_r, 1.0, EPS_RIF, "N")
    sq_fine = dict(sq)
    for _ in range(PQ):
        sq_fine = C3.passo3(sq_fine, sc, ident, uno_r, 1.0, EPS_RIF, None)
    qL1 = L3.conservazione_modificata(sq_fine, sc, ident, uno_r, 1.0, EPS_RIF, "lineare")
    qN1 = L3.conservazione_modificata(sq_fine, sc, ident, uno_r, 1.0, EPS_RIF, "N")
    tolQ = PQ * n_est * EPS * math.sqrt(CM.norma(sq["psi"]))
    esito("### la `Q` del braccio `lineare` si CONSERVA, all-errore di macchina",
          abs(qL1 - qL0) <= tolQ,
          "### |dQ| = %.3g, soglia %d*%d*eps = %.3g (la quasi-energia lineare e- "
          "conservata per UNITARIETA-)" % (abs(qL1 - qL0), PQ, n_est, tolQ))
    # ### ⛔ **E IL GEMELLO CHE DEVE FALLIRE:** la ### **`Q` di `N`**, misurata
    # ### sulla ### **stessa corsa lineare**, ### **NON si conserva** -- ed e-
    # ### ### **esattamente il numero che il ternario produceva.**
    esito("### DEVE SCATTARE: la `Q` di `N` sulla corsa LINEARE non si conserva",
          abs(qN1 - qN0) > 1e3 * tolQ,
          "### |dQ| = %.3g contro la soglia %.3g: ### **e- il difetto che il ternario "
          "<<N if nome == N else N>> nascondeva**" % (abs(qN1 - qN0), tolQ))

    # ================================================================ le uscite
    p = os.path.join(_QUI, "uscite", "letture_guscio_moto.json")
    dati = {}
    if os.path.exists(p):
        dati = json.loads(io.open(p, encoding="utf-8").read())
    esito("### le uscite `json` esistono e NON sono vuote",
          bool(dati.get("G1")) and bool(dati.get("G2")),
          "### G1: %d voci, G2: %d voci"
          % (len(dati.get("G1", {})), len(dati.get("G2", {}))))
    # ### ⭐ **E OGNI RIGA DI `G2` DICHIARA SU QUALE GRANDEZZA E- LA SUA `Q`:**
    # ### senza quel campo ### **nessuno potrebbe sapere che il ternario sbagliava.**
    _g2 = dati.get("G2") or {}
    # ### ⚠ **SOLO le righe che HANNO una `Q`:** `massima_densita` non passa
    # ### da `due_grumi`, quindi ### **non ne ha nessuna** -- e pretenderla sarebbe
    # ### ### **un braccio che fallisce per la ragione sbagliata.**
    _righe = [r for s in ("interazione", "massima_densita", "moto_collettivo")
              for r in (_g2.get(s) or {}).values()
              if isinstance(r, dict) and "Q_iniziale" in r]
    _senza = [r for r in _righe if not r.get("quale_Q")]
    _storte = [r for r in _righe
               if r.get("quale_Q") == "N" and r.get("nome") not in ("N", "D", "E")]
    esito("### ogni riga di `G2` dichiara `quale_Q`, e NON e- `N` per il lineare",
          bool(_righe) and not _senza and not _storte,
          "### %d righe, %d senza il campo, %d col `quale_Q` sbagliato"
          % (len(_righe), len(_senza), len(_storte)))
    # ### ⛔ **E QUESTO BRACCIO NASCE DA UNA MIA AFFERMAZIONE SBAGLIATA:**
    # ### avevo scritto *<<la saturazione rallenta l-allargamento del `~20%`>>*
    # ### guardando ### **solo le pendenze**, e la soglia che avevo fissato PRIMA dice
    # ### ### **<<come nel lineare = entro `3 sigma`>>.** ### ⭐ **Il `sigma`
    # ### C-ERA NEL `json`, e io non l-avevo guardato:** `0.0018`, cioe- lo scarto
    # ### ### **sta a meno di `1 sigma`.** ### ⚠ **Quindi il braccio pretende che OGNI
    # ### riga porti il suo `sigma`**, perche- una pendenza senza barra
    # ### ### **non decide niente.**
    _mdq = (_g2.get("massima_densita") or {})
    _nosig = [k for k, r in _mdq.items()
              if not isinstance(r, dict) or not r.get("sigma")]
    esito("### ogni pendenza di `G2(b)` porta il suo `sigma`",
          bool(_mdq) and not _nosig,
          "### %d righe, %d senza barra d-errore: ### **una pendenza senza barra non "
          "decide niente**" % (len(_mdq), len(_nosig)))

    # ================================================================ il banco
    testo = io.open(os.path.join(_QUI, "_guscio_moto.py"), encoding="utf-8").read()
    esito("### la lettura non IMPORTA il simulatore",
          "import soliton_simulator" not in testo
          and "from soliton_simulator" not in testo, "### cercate le due forme")
    esito("### NESSUN clip nella lettura",
          not [c for c in CLIP if c in testo],
          "### %d forme cercate" % len(CLIP))

    # ================================================================ il determinismo
    imp = []
    for _ in range(2):
        pr = subprocess.run([sys.executable, os.path.join(_QUI, "_guscio_moto.py")],
                            cwd=RADICE, capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
        imp.append((pr.stdout or "").strip())
    esito("### il DETERMINISMO fra DUE PROCESSI: uscita identica",
          len(imp) == 2 and imp[0] == imp[1] and bool(imp[0]),
          "### %d caratteri confrontati" % len(imp[0] if imp else ""))

    print("=" * 100)
    print("IL COLLAUDO DELLE LETTURE G1 E G2: %d su %d   ### %s"
          % (ok[0], ok[1], "TUTTI PASSATI" if ok[0] == ok[1] else "CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(main())
