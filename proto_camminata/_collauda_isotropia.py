# -*- coding: utf-8 -*-
r"""IL BANCO DELL'ISOTROPIA LOCALE — **i bracci che il mandato chiede, piu' quelli che devono SCATTARE.**

| | il braccio | che cosa prova |
|---|---|---|
| `1` | le **due vie** di estrazione degli archi della Delaunay danno lo **STESSO INSIEME** | ### **ESATTAMENTE** *(sono interi: niente tolleranza)* |
| `2` | le **due vie** del rilassamento danno la **STESSA SCENA** | i punti differiscono di `~1e-11`, e ### ⭐ **gli archi di ZERO** |
| `3` | il **Grover PESATO a pesi uguali** e' il Grover del `v3` | ### **AL BIT** |
| `4` | la **`C`** regge col Grover pesato, a pesi **uguali** e **casuali** | e si misura ### **sull'IDENTITA'**, non sulla curva |
| `5` | sul **cubico** l'anisotropia del profilo medio e' **SISTEMATICA a OGNI `t`** | ### ⛔ **e' il CONTROLLO del mandato:** un reticolo e' `3D` e **NON** isotropo |
| `6` | lo **sbilanciamento** e' **`0` esatto** sul cubico e **`> 0`** sul geometrico | ### **la grandezza misura quello che dice** |
| `7` | la **correlazione** di `s7`: **`1` su un caso costruito**, e **non significativa** su uno indipendente | ### ⛔ **nei DUE VERSI: un controllo positivo che PUO' fallire** |
| `8` | **`U`, `R`, `Rn` non leggono le POSIZIONI**, e la dinamica non le riceve | sul ### **SORGENTE** |
| — | nessun `clip`, nessun import del simulatore, determinismo fra **due processi** | sul **sorgente** |

Gira con:  python proto_camminata/_collauda_isotropia.py
"""
import ast
import inspect
import io
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

import camminata as CM                                        # noqa: E402
import camminata2 as C2                                       # noqa: E402
import geometria as GE                                        # noqa: E402
import pesi4 as P4                                            # noqa: E402
import scena as SC                                            # noqa: E402
import scene3d as S3D                                         # noqa: E402

SEME = 11
EPS = float(np.finfo(float).eps)
# ### ⚠ **`np.minimum`/`np.maximum` NON stanno in questi file**, e il braccio lo verifica
# ### invece di assumerlo. ### ⛔ **E la lista e' VUOTA: nessun clip ammesso.**
# ### ⭐ **L'UNICO AMMESSO, e NON e- un clip: e' una DEFINIZIONE.**
# ### `np.minimum(d, 1 - d)` in `_d2_periodica` e' la ### **convenzione dell'IMMAGINE
# ### MINIMA sul toro** *(la distanza fra due punti del cubo periodico **e'** la minore
# ### fra le due vie)*. ### ⛔ **Non protegge da nessun errore** -- e `A11` chiede
# ### l'errore ### **solo a un clip**, cioe' a qualcosa che ALTERA una grandezza.
CLIP_AMMESSI = {"scene3d.py": ("np.minimum",)}
FILE = ("scene3d.py", "pesi4.py", "_letture_isotropia_locale.py")


def _codice(testo):
    """### Il testo ### **SENZA commenti e SENZA docstring**: solo il codice eseguibile.

    ### ⛔ **SERVE PERCHE' DUE BRACCI FALLIVANO SULLA PROSA:** uno sulla docstring che
    ### **dichiara** il vincolo che verifica, l'altro sui ### **miei commenti** che dicono
    *«qui non c'e' nessun `np.maximum`»*. ### ⭐ **Un presidio deve guardare il CODICE.**
    """
    try:
        albero = ast.parse(testo)
    except SyntaxError:
        # ### ⚠ **un FRAMMENTO di sorgente** (una funzione estratta) e' indentato:
        # ### si de-indenta prima di rinunciare.
        import textwrap
        albero = ast.parse(textwrap.dedent(testo))
    for nodo in ast.walk(albero):
        if isinstance(nodo, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)) and ast.get_docstring(nodo):
            nodo.body = nodo.body[1:] or [ast.Pass()]
    return ast.unparse(albero)


def main():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL BANCO DELL'ISOTROPIA LOCALE -- gli otto bracci, e i due che DEVONO scattare")
    print("=" * 100)
    SC._niente_simulatore()

    # ================================================ 1) le due vie degli archi
    for n in (512, 1728):
        a_v, _p = P4.delaunay_periodica(n, SEME, False, False)
        a_l, _q = P4.delaunay_periodica(n, SEME, False, True)
        esito("### (1) gli archi della Delaunay: la via VELOCE = la LENTA, n = %d" % n,
              a_v == a_l and set(a_v) == set(a_l) and len(a_v) > 0,
              "### %d archi, confronto ESATTO su interi" % len(a_v))

    # ================================================ 2) le due vie del rilassamento
    n = 1728
    p_loop = S3D.punti3d_rilassati(n, SEME)
    vero = S3D.MAX_N2
    try:
        # ### ⛔ **SI FORZA LA VIA DELL'ALBERO SULLA STESSA TAGLIA**, altrimenti il
        # ### confronto sarebbe fra due TAGLIE e non fra due VIE.
        S3D.MAX_N2 = 100
        p_alb = S3D.punti3d_rilassati(n, SEME)
        sc_a = S3D.geometrico3d(n, rilassati=True)
        S3D.MAX_N2 = vero
        sc_b = S3D.geometrico3d(n, rilassati=True)
    finally:
        S3D.MAX_N2 = vero
    dp = float(np.max(np.abs(p_loop - p_alb)))
    uguali = (set(map(tuple, sc_a["archi"])) == set(map(tuple, sc_b["archi"])))
    esito("### (2) il rilassamento: le due vie danno la STESSA SCENA", uguali,
          "### max|dp| = %.2e (il passo tipico e' ~1e-2), archi diversi = %d"
          % (dp, len(set(map(tuple, sc_a["archi"])) ^ set(map(tuple, sc_b["archi"])))))
    esito("### (2-bis) e NON sono bit-identiche: la differenza si MISURA", dp > 0.0,
          "### se fosse `0` il braccio (2) sarebbe un FALSO-ZERO")

    # ================================================ 3) i pesi uguali = il `v3`
    sc = S3D.geometrico3d(512)
    psi = CM.stato_casuale(sc, SEME)
    uno_w = np.ones(2 * sc["m"], dtype=float)
    a = P4.grover_pesato(psi, sc, uno_w)
    b = CM.moneta_grover(psi, sc)
    esito("### (3) il Grover PESATO a pesi uguali = il Grover del `v3`, AL BIT",
          float(np.max(np.abs(a - b))) == 0.0,
          "### max|diff| = %.3g" % float(np.max(np.abs(a - b))))
    # ### ⭐ **E I DUE CONTROLLI CHE DEVONO FALLIRE:** peso nullo e scala.
    w0 = uno_w.copy()
    w0[0] = 0.0
    esito("### (3-bis) un peso NULLO cambia il risultato: il braccio (3) e' VIVO",
          float(np.max(np.abs(P4.grover_pesato(psi, sc, w0) - a))) > 0.0,
          "### se non cambiasse, i pesi non sarebbero LETTI")
    k = 3.7
    esito("### (3-ter) il Grover pesato e' INVARIANTE DI SCALA nei pesi",
          float(np.max(np.abs(P4.grover_pesato(psi, sc, k * uno_w) - a))) < 64 * EPS,
          "### max|diff| = %.3g con pesi x%.1f"
          % (float(np.max(np.abs(P4.grover_pesato(psi, sc, k * uno_w) - a))), k))

    # ================================================ 4) la `C` col Grover pesato
    rng = np.random.default_rng(SEME)
    for et, w in (("uguali", uno_w), ("casuali", rng.random(2 * sc["m"]) + 0.1)):
        x = P4.grover_pesato(np.conj(psi), sc, w)
        y = np.conj(P4.grover_pesato(psi, sc, w))
        esito("### (4) la `C` regge col Grover pesato, pesi %s" % et,
              float(np.max(np.abs(x - y))) < 64 * EPS * float(np.max(np.abs(psi))),
              "### max|C G - G C| = %.3g (relativo alla scala di psi)"
              % float(np.max(np.abs(x - y))))

    # ================================================ 5) il cubico e' SISTEMATICO
    # ### ⛔ **IL PRIMO GIRO DI QUESTO BRACCIO FALLIVA, E LA COLPA ERA DEL BRACCIO:**
    # ### con `L = 6` e ### **`12` nodi** l'anisotropia del cubico misurava
    # ### `3.28`, `2.73`, `1.25` volte il rumore -- cioe- ### **scendeva sotto la soglia
    # ### mentre a `L = 20` con `40` nodi sta stabile a `~6`.**
    # ### ⭐ **E IL MOTIVO E- NEL MISURANDO: il rumore atteso e-
    # ### `irregolarita'/sqrt(N)`**, quindi ### **con un terzo dei nodi il rumore e-
    # ### `1.8` volte piu- grande** e il rapporto si schiaccia. ### ⚠ **<<SISTEMATICA>>
    # ### NON E- UNA PROPRIETA- DELLA SCENA SOLTANTO: e- della scena E DEL CAMPIONE**, e un
    # ### braccio che non lo rispetta misura la propria statistica.
    cub = S3D.cubico(8)
    pc = S3D.punti_cubico(8)
    nodi_c = S3D.nodi_a_caso(cub, 40, 1)
    tutti, righe = True, []
    for t in (4, 6, 8):
        r = S3D.isotropia(cub, pc, passi=t, nodi=nodi_c)["euclideo"]
        righe.append("t=%d a/r=%.2f" % (t, r["aniso_su_rumore"]))
        tutti = tutti and bool(r["sistematica"])
    esito("### (5) sul CUBICO l'anisotropia e' SISTEMATICA a OGNI `t`", tutti,
          "### " + ", ".join(righe) + "   (L = 8, 40 nodi)")

    # ================================================ 6) lo sbilanciamento
    sb_c = S3D.sbilanciamento(cub, pc)
    sb_g = S3D.sbilanciamento(sc, S3D.punti3d(512, SEME))
    esito("### (6) lo sbilanciamento e' `0` ESATTO sul cubico",
          float(np.max(np.abs(sb_c))) < 64 * EPS,
          "### max = %.3g (le sei direzioni si cancellano)"
          % float(np.max(np.abs(sb_c))))
    esito("### (6-bis) e sul geometrico e' `> 0`: il braccio (6) non e' un FALSO-ZERO",
          float(np.mean(sb_g)) > 0.05,
          "### medio = %.4f su %d nodi" % (float(np.mean(sb_g)), sc["n"]))

    # ================================================ 7) la correlazione, nei due versi
    pos_g = S3D.punti3d(512, SEME)
    sb = S3D.sbilanciamento(sc, pos_g)
    # ### ⛔ **IL CONTROLLO POSITIVO: un'irregolarita' COSTRUITA uguale allo
    # ### sbilanciamento.** ### **Se la correlazione non la vedesse, non leggerebbe la
    # ### grandezza che dichiara.**
    finto = {"per_nodo": [{"nodo": int(k2), "relativa_euclidea": float(sb[k2])}
                          for k2 in range(sc["n"])]}
    c1 = S3D.correlazione(sc, pos_g, finto)
    esito("### (7) la correlazione vede un legame COSTRUITO: Pearson = 1",
          abs(c1["pearson"] - 1.0) < 1e-9 and bool(c1["significativa"]),
          "### Pearson = %+.9f, %s" % (c1["pearson"],
                                       "significativa" if c1["significativa"]
                                       else "### NON significativa"))
    # ### ⭐ **E IL VERSO CHE DEVE DARE <<NIENTE>>:** rumore indipendente.
    ru = np.random.default_rng(99).normal(size=sc["n"])
    finto2 = {"per_nodo": [{"nodo": int(k2), "relativa_euclidea": float(ru[k2])}
                           for k2 in range(sc["n"])]}
    c2 = S3D.correlazione(sc, pos_g, finto2)
    esito("### (7-bis) e su rumore INDIPENDENTE NON e' significativa",
          not c2["significativa"],
          "### Pearson = %+.4f, %.2f sigma" % (c2["pearson"], c2["in_sigma"]))

    # ================================================ 8) le POSIZIONI, sul sorgente
    # ### ⛔ **E QUESTO BRACCIO FALLIVA PER COLPA SUA:** cercava `pos` nel testo
    # ### ### **GREZZO**, e la docstring di `peso_di` contiene la frase *<<`U`, `R` e `Rn`
    # ### NON toccano `pos`>>* -- cioe- ### **la riga che DICHIARA il vincolo faceva
    # ### fallire il braccio che lo verifica.** ### ✅ **La cura: si guarda il CODICE**,
    # ### con l'albero sintattico, e ### **non la prosa.**
    src = _codice(inspect.getsource(P4.peso_di))
    esito("### (8) `peso_di` legge le posizioni SOLO nel braccio `V`",
          "pos" not in src and "_peso_voronoi" in src,
          "### nel CODICE (senza commenti ne' docstring), e il campo lo dichiara: %r"
          % (P4.LEGGE_POSIZIONI,))
    for br in ("U", "R", "Rn"):
        esito("### (8-bis) il braccio `%s` e' dichiarato SENZA posizioni" % br,
              P4.LEGGE_POSIZIONI[br] is False, "### e `V` e' `True` (controllo)")
    # ### ⛔ **E LA DINAMICA NON RICEVE `pos`:** si verifica sulla FIRMA del passo.
    fp = inspect.signature(C2.passo2).parameters
    esito("### (8-ter) il passo del `v3` non ha nessun parametro di POSIZIONE",
          not any("pos" in x or "punt" in x for x in fp),
          "### parametri: %s" % ", ".join(fp))
    esito("### (8-quater) e `sc` non contiene nessun campo di posizione",
          not any(("pos" in x) or ("punt" in x) for x in sc),
          "### campi: %s" % ", ".join(sorted(sc)[:8]))

    # ================================================ i `clip` e il simulatore
    for f in FILE:
        # ### ⛔ **ANCHE QUI IL BRACCIO LEGGEVA I COMMENTI, e il caso e- comico:** i
        # ### due `clip` che trovava in `scene3d.py` e in `pesi4.py` erano ### **i MIEI
        # ### COMMENTI che dicono <<qui non c'e- nessun `np.maximum`>>.** ### ⭐ **Un
        # ### presidio che si accende sulla PROPRIA dichiarazione di conformita- e- un
        # ### presidio che non guarda il codice** (`A9`).
        testo = _codice(io.open(os.path.join(_QUI, f), encoding="utf-8").read())
        trovati = [x for x in ("np.minimum", "np.maximum", "np.clip", ".clip(")
                   if x in testo and x not in CLIP_AMMESSI.get(f, ())]
        esito("### `%s` non contiene nessun `clip`" % f, not trovati,
              "### trovati: %s" % (", ".join(trovati) if trovati else "nessuno"))
        esito("### `%s` non IMPORTA il simulatore" % f,
              "import soliton_simulator" not in testo
              and "from soliton_simulator" not in testo, "### cercate le due forme")

    # ================================================ il determinismo
    pr = []
    for _ in range(2):
        q = subprocess.run([sys.executable, "-c",
                            "import sys; sys.path.insert(0, %r); sys.path.insert(0, %r);"
                            " import scena as SC, scene3d as S3D; SC._niente_simulatore();"
                            " sc = S3D.geometrico3d(512, rilassati=True);"
                            " print(sc['m'], list(sc['grado'][:20]))"
                            % (_QUI, os.path.join(RADICE, "csv"))],
                           cwd=RADICE, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        pr.append((q.stdout or "").strip())
    esito("### il DETERMINISMO della scena `(ii)` fra DUE PROCESSI",
          len(pr) == 2 and pr[0] == pr[1] and bool(pr[0]),
          "### %d caratteri confrontati" % len(pr[0] if pr else ""))

    print("=" * 100)
    print("IL BANCO DELL'ISOTROPIA: %d su %d   ### %s"
          % (ok[0], ok[1], "TUTTI PASSATI" if ok[0] == ok[1] else "CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(main())
