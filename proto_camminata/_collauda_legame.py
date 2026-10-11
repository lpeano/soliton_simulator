r"""IL BANCO DEL LEGAME — **i cinque bracci che la seconda versione del mandato chiede.**

| | il braccio | che cosa prova |
|---|---|---|
| `1` | **regressione** con le candidate spente | ### **AL BIT** |
| `2` | `-N` e `-D` **rispettano `C`** e **invertono esattamente** | e la `C` si misura ### **sull'IDENTITA'**, non sulla curva |
| `3` | l'iterazione di `M2` **si ferma** se non converge | e la **fase globale** e' la ragione per cui un `FERMO` sarebbe falso senza fissarla |
| `4` | `M0` **riproduce lo spettro noto** del `v2` nel caso di controllo | ### ⭐ **compreso il `64.9` della lettura `M`**, che era un ARTEFATTO: lo ritrova **nella colonna <<con tutto>>** e non in quella che decide |
| `5` | la **regola sul raggio** e' applicata, e ### ⛔ **un caso costruito apposta la fa SCATTARE** | nei **due versi**: concentrato ⟹ decidibile, diffuso ⟹ **NON DECIDIBILE PER TAGLIA** |
| — | nessun `clip`, nessun import del simulatore, determinismo fra **due processi** | sul **sorgente** |

Gira con:  python proto_camminata/_collauda_legame.py
"""
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

import autostati2 as A2                                        # noqa: E402
import buchi0 as B0                                            # noqa: E402
import camminata as CM                                         # noqa: E402
import camminata2 as C2                                        # noqa: E402
import camminata3 as C3                                        # noqa: E402
import geometria as GE                                         # noqa: E402
import scena as SC                                             # noqa: E402
import segni1 as S1                                            # noqa: E402
import vuoto3 as V3                                            # noqa: E402
import _letture_legame as LL                                   # noqa: E402
import _spettro as SP                                          # noqa: E402

EPS = float(np.finfo(float).eps)
SEME = 11
CLIP = ("np.clip", ".clip(", "np.maximum", "np.minimum", "np.fmax", "np.fmin")
# ### ⚠ **`np.minimum`/`np.maximum` NON stanno in questi file**, e il braccio lo verifica
# ### invece di assumerlo.
CLIP_AMMESSI = {}
FILE = ("buchi0.py", "segni1.py", "autostati2.py", "_letture_legame.py")


def main():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL BANCO DEL LEGAME -- i cinque bracci, e i due che DEVONO scattare")
    print("=" * 100)
    SC._niente_simulatore()

    sc = SC.irregolare(120)
    reg = SC.regolare(120)
    geo_i = GE.scena_identita(sc)
    geo_c = GE.scena_curva(sc, SEME)
    n_est = 2 * sc["m"]
    dim = 4 * sc["m"]
    tol = n_est * EPS
    uno = np.ones(sc["n"], dtype=float)
    st = C3.stato3(sc, SEME)
    K = 16

    # ============================================================ 1) la regressione
    a = st["psi"].copy()
    b = dict(st)
    for _ in range(K):
        a = C2.passo2(a, sc, geo_c, uno, 1.0, 0.5)
        b = C3.passo3(b, sc, geo_c, uno, 1.0, 0.5, S1.flusso_di("lineare"))
    esito("### (1) con le candidate SPENTE il passo e- il `v2` lineare, AL BIT",
          float(np.max(np.abs(b["psi"] - a))) == 0.0,
          "### max|psi - psi_v2| = %.3g su %d tick"
          % (float(np.max(np.abs(b["psi"] - a))), K))

    # ============================================================ 2) `C` e l-inverso
    n0 = CM.norma(st["psi"])
    f0 = V3.norma_vuoto(st["phi"])
    cc, ii, nn = {}, {}, {}
    for et in S1.VARIANTI:
        fl = S1.flusso_di(et)
        e1 = C3.coniuga3(C3.passo3(st, sc, geo_i, uno, 1.0, 0.5, fl))
        e2 = C3.passo3(C3.coniuga3(st), sc, geo_i, uno, 1.0, 0.5, fl)
        cc[et] = max(float(np.max(np.abs(e1["psi"] - e2["psi"]))),
                     float(np.max(np.abs(e1["phi"] - e2["phi"]))))
        z = dict(st)
        for _ in range(K):
            z = C3.passo3(z, sc, geo_i, uno, 1.0, 0.5, fl)
        nn[et] = max(abs(CM.norma(z["psi"]) - n0) / n0,
                     abs(V3.norma_vuoto(z["phi"]) - f0) / f0)
        w = dict(z)
        for _ in range(K):
            w = C3.passo3_inverso(w, sc, geo_i, uno, 1.0, 0.5, fl)
        ii[et] = max(float(np.max(np.abs(w["psi"] - st["psi"]))),
                     float(np.max(np.abs(w["phi"] - st["phi"])))) \
            / max(math.sqrt(f0), 1.0)
    esito("### (2) `-N` e `-D` rispettano la `C`, AL BIT, come `+N` e `+D`",
          max(cc.values()) == 0.0,
          "### " + ", ".join("%s %.3g" % (k, v) for k, v in cc.items()))
    esito("### (2) `-N` e `-D` INVERTONO esattamente, e le norme si conservano",
          max(ii.values()) <= tol and max(nn.values()) <= tol,
          "### inverso max %.3g, norme max %.3g (relativi), soglia %.3g"
          % (max(ii.values()), max(nn.values()), tol))
    # ### ⛔ **E IL GEMELLO CHE DEVE SCATTARE: sulla CURVA la `C` si rompe PER TUTTE**,
    # ### ### **`lineare` compresa** -- quindi un `0.149` sulla curva ### **non dice niente
    # ### sul SEGNO**, ed e- il falso-positivo che ho preso al primo giro.
    cur = {}
    for et in S1.VARIANTI:
        fl = S1.flusso_di(et)
        e1 = C3.coniuga3(C3.passo3(st, sc, geo_c, uno, 1.0, 0.5, fl))
        e2 = C3.passo3(C3.coniuga3(st), sc, geo_c, uno, 1.0, 0.5, fl)
        cur[et] = max(float(np.max(np.abs(e1["psi"] - e2["psi"]))),
                      float(np.max(np.abs(e1["phi"] - e2["phi"]))))
    # ### \u26a0 **E LA SOGLIA E- RELATIVA, perche- al primo giro la mia era ASSOLUTA e
    # ### troppo stretta** *(`1e-9`)*: cinque dinamiche diverse ### **non danno la stessa
    # ### rottura al bit**, e pretenderlo era un braccio rosso ### **per una soglia mia.**
    # ### \u2b50 **Il numero che conta e- lo SCARTO RELATIVO:** se tutte rompono dello
    # ### ### **stesso `0.1494` a meno di uno su diecimila**, la rottura e-
    # ### ### **della fase `U(1)` e non del segno.**
    base = cur["lineare"]
    rel = max(abs(v - base) / base for v in cur.values())
    esito("### DEVE SCATTARE: sulla CURVA la `C` si rompe per TUTTE, lineare compreso",
          min(cur.values()) > 1e-3 and rel < 1e-4,
          "### tutte a **%.6f**, scarto relativo massimo **%.2g** su %d varianti: ### "
          "**e- la fase `U(1)`, non il segno**" % (base, rel, len(cur)))
    # ### \u2b50 **E UN BRACCIO CHE IL NUMERO MI HA REGALATO:** `+N` e `-N` deviano dal
    # ### lineare ### **della STESSA quantita- e col SEGNO OPPOSTO** -- che e- esattamente
    # ### cio- che *«il segno rovescia il flusso»* predice. ### **Se non fosse cosi-, `-N`
    # ### non sarebbe il flusso di `-N`.**
    # ### ⚠ **E LA SOGLIA E- RELATIVA ALLA DEVIAZIONE, non assoluta:** la somma delle
    # ### due deviazioni e- il ### **residuo di SECONDO ordine**, e pretenderlo sotto un
    # ### numero fisso ### **non ha una scala.** ### ⛔ **E- la TERZA volta che faccio
    # ### questo errore in questa sessione** *(la soglia delle norme del `v4`, la `C` della
    # ### quota, e questa)*: sempre ### **una tolleranza assoluta su una grandezza la cui
    # ### scala non e- `1`.**
    dn = (cur["+N"] - base, cur["-N"] - base)
    dd = (cur["+D"] - base, cur["-D"] - base)
    rn = abs(sum(dn)) / max(abs(dn[0]), 1e-300)
    rd = abs(sum(dd)) / max(abs(dd[0]), 1e-300)
    esito("### `+N` e `-N` deviano dal lineare in modo ANTISIMMETRICO: il segno rovescia il "
          "flusso",
          max(rn, rd) <= 1e-4 and min(abs(dn[0]), abs(dd[0])) > 0.0,
          "### `+N` %+.3g contro `-N` %+.3g (residuo relativo **%.1g**) | `+D` %+.3g contro "
          "`-D` %+.3g (**%.1g**)" % (dn[0], dn[1], rn, dd[0], dd[1], rd))

    # ============================================================ 3) il FERMO di `M2`
    spaz = 2.0 * math.pi / dim
    fermato = False
    try:
        A2.cerca(sc, geo_i, "+N", 0.5, [0.0, math.pi], spaz, max_giri=3)
    except A2.NonConverge:
        fermato = True
    esito("### (3) l-iterazione di `M2` si FERMA se non converge",
          fermato, "### `NonConverge` alzata entro il budget dichiarato")
    # ### ⛔ **E LA FASE GLOBALE E- LA RAGIONE PER CUI UN `FERMO` SAREBBE FALSO SENZA
    # ### FISSARLA:** lo stesso vettore con una fase diversa da- uno scarto ### **`O(1)`**.
    v = st["psi"] / math.sqrt(CM.norma(st["psi"]))
    ruotato = v * np.exp(1j * 1.234)
    esito("### DEVE SCATTARE: senza fissare la fase lo STESSO vettore sembra diverso",
          float(np.max(np.abs(ruotato - v))) > 1e-3
          and float(np.max(np.abs(A2._fissa_fase(ruotato, v) - v))) <= tol,
          "### senza %.4f, con `_fissa_fase` %.3g: ### **percio- un `FERMO` non e- un "
          "artefatto della fase**"
          % (float(np.max(np.abs(ruotato - v))),
             float(np.max(np.abs(A2._fissa_fase(ruotato, v) - v)))))

    # ============================================================ 4) lo spettro noto
    for nome, s in (("irregolare", sc), ("regolare", reg)):
        g = GE.scena_identita(s)
        a0 = B0.analizza(s, g, 0.0)
        M = C2.matrice_passo(s, g, np.ones(s["n"]), 1.0, 0.0)
        lam = np.linalg.eigvals(M)
        noti = (SP.conta_autovalori(lam, 1.0, SP.TOLLERANZE[1]),
                SP.conta_autovalori(lam, -1.0, SP.TOLLERANZE[1]))
        esito("### (4) `M0` riproduce la molteplicita- nota di `+-1` sul %s" % nome,
              (a0["piu_uno"], a0["meno_uno"]) == noti,
              "### `M0` %d/%d, `_spettro` %d/%d  (a `eps = 0`)"
              % (a0["piu_uno"], a0["meno_uno"], noti[0], noti[1]))
    # ### ⭐ **E IL CONTROLLO CHE VALE PIU- DI TUTTI: il `64.9` DELLA LETTURA `M` DEL `v2`
    # ### SI RITROVA, ma ### **nella colonna <<con tutto>>** -- e NON in quella che decide.
    a0 = B0.analizza(sc, geo_i, 0.0)
    ct = a0["con_tutto"]["piu_grande_in_spaziature"]
    sz = a0["senza_spigole"]["piu_grande_in_spaziature_usati"]
    esito("### (4) il `64.9` della lettura `M` del `v2` si RITROVA, e sta nella colonna "
          "sbagliata",
          abs(ct - 64.9) < 0.5 and abs(sz - ct) > 1.0,
          "### <<con tutto>> **%.2f sp** *(il numero storico)* contro <<senza spigole>> "
          "**%.2f sp_u**: ### **la differenza E- la trappola**" % (ct, sz))

    # ============================================================ 5) la regola sul raggio
    diam, esatto = LL.diametro(sc)
    # ### concentrato: UN NODO SOLO ⟹ raggio iniziale `0` ⟹ ### **DECIDIBILE**
    p_conc = CM.stato_zero(sc)
    p_conc[int(np.argmax(sc["nodo"] == 0)), 0] = 1.0
    r_conc = LL.raggio(sc, {"psi": p_conc}, 0)
    # ### diffuso: TUTTE le estremita- uguali ⟹ raggio grande
    p_dif = np.ones((n_est, 2), dtype=complex)
    r_dif = LL.raggio(sc, {"psi": p_dif}, 0)
    # ### \u26d4 **IL CASO CHE MI HA CORRETTO IL GUARDIANO: parte CONCENTRATO e finisce
    # ### DIFFUSO.** ### **Prima dava <<NON DECIDIBILE PER TAGLIA>>, perche- guardavo il
    # ### raggio FINALE** -- e ### **<<si disperde>> e- il risultato piu- chiaro
    # ### possibile**, non un-assenza di risultato.
    d_disp = LL.decidibile(sc, diam, r_conc, 4, r_dif)
    esito("### (5) DEVE: un caso che SI DISPERDE resta DECIDIBILE",
          d_disp["decidibile"] and d_disp["raggio_finale"] > diam / 3.0,
          "### raggio iniziale **%.0f** (soglia %.2f) e finale **%.0f** (oltre la soglia): "
          "**%s** \u2014 ### **il finale e- una MISURA, non una condizione**"
          % (r_conc, diam / 3.0, r_dif, d_disp["verdetto"]))
    # ### \u26d4 **E IL CASO PER CUI LA REGOLA ESISTE: uno STAZIONARIO troppo grande.**
    d_grande = LL.decidibile(sc, diam, r_dif, 4, r_dif)
    esito("### (5) DEVE: uno stato INIZIALE troppo grande e- NON DECIDIBILE PER TAGLIA",
          not d_grande["decidibile"] and not d_grande["raggio_ok"],
          "### raggio iniziale **%.0f** oltre la soglia %.2f: **%s** \u2014 ### **e- il "
          "caso per cui la regola esiste** (uno stato LEGATO ma GRANDE)"
          % (r_dif, diam / 3.0, d_grande["verdetto"]))
    # ### e il TEMPO: un `t_oss` oltre `T_max` ⟹ ### **NON DECIDIBILE**, anche se concentrato
    d_tempo = LL.decidibile(sc, diam, r_conc, LL.t_max(diam) + 1)
    esito("### (5) e la condizione di TEMPO scatta da sola, col raggio a posto",
          not d_tempo["decidibile"] and d_tempo["raggio_ok"],
          "### `t_oss` %d > `t_max` %d: **%s** (diametro %s)"
          % (LL.t_max(diam) + 1, LL.t_max(diam), d_tempo["verdetto"],
             ("%d" % diam) if esatto else (">=%d" % diam)))
    # ### ⛔ **E IL DIAMETRO DELL-IRREGOLARE CRESCE COME `log n`:** e- il fatto che rende
    # ### la regola ### **quasi sempre negativa** la-, e si misura invece di crederlo.
    d120, _e = LL.diametro(SC.irregolare(120))
    d500, _e = LL.diametro(SC.irregolare(500))
    esito("### il diametro dell-irregolare cresce come `log n`, non come `n`",
          d500 < 2 * d120,
          "### `n=120` diametro **%d**, `n=500` diametro **%d**: ### **crescere la taglia "
          "NON allarga la soglia** (%.2f -> %.2f)" % (d120, d500, d120 / 3.0, d500 / 3.0))

    # ============================================================ il sorgente
    for f in FILE:
        testo = open(os.path.join(_QUI, f), encoding="utf-8").read()
        trovati = [c for c in CLIP if c in testo and c not in CLIP_AMMESSI.get(f, ())]
        esito("### nessun `clip` in `%s`" % f, not trovati,
              "### %d forme cercate" % len(CLIP))
        esito("### `%s` non IMPORTA il simulatore" % f,
              "import soliton_simulator" not in testo
              and "from soliton_simulator" not in testo, "### cercate le due forme")

    # ============================================================ il determinismo
    for f in ("buchi0.py", "segni1.py"):
        imp = []
        for _ in range(2):
            pr = subprocess.run([sys.executable, os.path.join(_QUI, f)],
                                cwd=RADICE, capture_output=True, text=True,
                                encoding="utf-8", errors="replace")
            imp.append((pr.stdout or "").strip())
        esito("### il DETERMINISMO di `%s` fra DUE PROCESSI" % f,
              len(imp) == 2 and imp[0] == imp[1] and bool(imp[0]),
              "### %d caratteri confrontati" % len(imp[0] if imp else ""))

    print("=" * 100)
    print("IL BANCO DEL LEGAME: %d su %d   ### %s"
          % (ok[0], ok[1], "TUTTI PASSATI" if ok[0] == ok[1] else "CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(main())
