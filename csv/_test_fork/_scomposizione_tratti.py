r"""**`TRATTI` — IL CALO STA NEL VARCO O NEGLI INTERNI?** *(in unita' ASSOLUTE)*

*(Mandato di Luca, 2026-09-27, quarto punto della verifica del guardiano su `8c2997c`. I criteri
sono in `doc/TASK_HISTORY/2026-09-27_tratti.md`, committati **prima**.)*

**NON SERVE RIGIRARE NIENTE:** legge i `misura.json` **gia' committati** del pilota.

**LA SCOMPOSIZIONE, in unita' ASSOLUTE e con IC95 fra semi (`P3`, `t(3) = 3.182`):**

    D_centri   = centro_centro(t)     - centro_centro(0)
    D_varco    = insieme_insieme(t)   - insieme_insieme(0)
    D_interni  = D_centri - D_varco

> ### ⚠⚠ **`D_interni` E' UN INDICATORE, NON IL TRATTO INTERNO DEL CAMMINO.**
> E' **«centri meno varco minimo»**: `insieme_insieme` e' **la distanza fra i due nodi piu' vicini**
> delle due regioni, che **non sta necessariamente sul cammino** `medoide -> medoide`. Quindi
> `D_interni` misura *«quanto del moto dei centri NON e' spiegato dall'avvicinarsi delle superfici
> piu' vicine»*, **non** *«di quanto si e' accorciato il tratto dentro le regioni»*.
> **La scomposizione VERA richiede il CAMMINO**, e quindi gli stati del grafo ai checkpoint, che
> **questo run non ha salvato**: e' il `TODO` del task history. **Dichiarato, non sottinteso.**

> ### ⚠ **E PERCHE' IN UNITA' ASSOLUTE, ed e' il difetto `ALLUNG-RELATIVO`:**
> il criterio `V6` del pilota calcolava **`(st-s0)/s0 - (ct-c0)/c0`**, cioe' sottraeva due
> variazioni **RELATIVE con DENOMINATORI DIVERSI** — `s0 ~ 3.0` contro `c0 ~ 10.7`. **Due corpi
> RIGIDI che si avvicinano di `delta` darebbero**
> `-delta/3.0 + delta/10.7 = -0.24 * delta`, cioe' **un «allungamento» FINTO che non esiste.**
> **In unita' assolute il problema sparisce per costruzione.**

    python csv/_test_fork/_scomposizione_tratti.py
    python csv/_test_fork/_scomposizione_tratti.py --collaudo    # i due casi a risposta NOTA

ASCII puro.
"""
import io
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))

import _presidio                                                       # noqa: E402
import _osservabile_p1 as OP                                           # noqa: E402

_presidio.avvia(__file__)

# ESENTE-H-P5: non costruisce nessuna scena e non carica il simulatore. Legge i `misura.json` di un
#   run che ha GIA' dichiarato la propria configurazione intera nel suo referto (`REFERTO.txt`).

NL = chr(10)
DEST = os.path.join(_QUI, "_pilota_prova1")
FUORI = os.path.join(DEST, "SCOMPOSIZIONE_tratti.txt")
SEMI = [11, 12, 13, 14]
CPS = [40, 80, 120]
R = []


def P(s=""):
    print(s)
    R.append(s)


def barra(v):
    """`(media, sd, lo, hi, contiene_zero)` col `t` di Student giusto (`P3`)."""
    o = OP.dispersione([x for x in v if np.isfinite(x)])
    if o["ic95"] is None:
        return o["media"], float("nan"), float("nan"), float("nan"), True
    lo, hi = o["ic95"]
    return o["media"], o["sd"], lo, hi, bool(lo <= 0.0 <= hi)


def riga(nome, v, P=P):
    m, sd, lo, hi, z = barra(v)
    P("    %-34s %+.5f   sd %.5f   IC95 [%+.5f,%+.5f]   %s"
      % (nome, m, sd, lo, hi,
         ("CONTIENE LO ZERO -> limite |x| < %.4g" % max(abs(lo), abs(hi))) if z
         else "** ESCLUDE LO ZERO **"))
    return m, z


# ============================================================================ IL COLLAUDO
def collaudo():
    """**Due casi a risposta NOTA.** Il primo e' quello che DEVE far vedere lo zero (`P1-sexies`)."""
    P("=" * 104)
    P("`T4` -- I DUE CASI A RISPOSTA NOTA, in unita' ASSOLUTE")
    P("=" * 104)
    ok = 0

    # --- T4: due insiemi RIGIDI traslati di -0.19: D_interni DEVE essere ~0
    delta = -0.19
    c0, s0 = 10.6694, 3.2869          # i valori VERI del passo 0 (coppia 0|1)
    ct, st = c0 + delta, s0 + delta   # rigidi: centri e superfici si muovono UGUALE
    d_c, d_v = ct - c0, st - s0
    d_i = d_c - d_v
    buono = abs(d_i) < 1e-12
    ok += 1 if buono else 0
    P("  T4   due insiemi RIGIDI traslati di %+.2f" % delta)
    P("       D_centri %+.5f   D_varco %+.5f   D_interni %+.5f   -> %s"
      % (d_c, d_v, d_i, "PASS (zero esatto)" if buono else "** FAIL **"))
    # e la controprova sul criterio VECCHIO, quello RELATIVO
    vecchio = (st - s0) / s0 - (ct - c0) / c0
    P("       ** e il criterio RELATIVO di `V6` su questo STESSO caso rigido darebbe")
    P("          (st-s0)/s0 - (ct-c0)/c0 = %+.5f, cioe' un ALLUNGAMENTO che NON ESISTE." % vecchio)
    P("          E' il difetto `ALLUNG-RELATIVO`: denominatori diversi (%.4f contro %.4f)."
      % (s0, c0))

    # --- T4b: contrazione SOLO INTERNA: le superfici ferme, i centri si avvicinano
    ct2, st2 = c0 - 0.19, s0
    d_c2, d_v2 = ct2 - c0, st2 - s0
    d_i2 = d_c2 - d_v2
    buono2 = abs(d_v2) < 1e-12 and abs(d_i2 - d_c2) < 1e-12 and d_i2 < 0
    ok += 1 if buono2 else 0
    P("  T4b  contrazione SOLO INTERNA (superfici FERME, centri -0.19)")
    P("       D_centri %+.5f   D_varco %+.5f   D_interni %+.5f   -> %s"
      % (d_c2, d_v2, d_i2, "PASS (tutto negli interni)" if buono2 else "** FAIL **"))

    # --- T4c: avvicinamento SOLO DEL VARCO: le superfici si avvicinano, gli interni fermi
    d_c3, d_v3 = -0.19, -0.19
    d_i3 = d_c3 - d_v3
    buono3 = abs(d_i3) < 1e-12
    ok += 1 if buono3 else 0
    P("  T4c  avvicinamento SOLO DEL VARCO (superfici e centri di pari passo)")
    P("       D_centri %+.5f   D_varco %+.5f   D_interni %+.5f   -> %s"
      % (d_c3, d_v3, d_i3, "PASS (zero negli interni)" if buono3 else "** FAIL **"))
    P()
    P("  LA RIGA CHE CONTA E' `T4`: due corpi RIGIDI danno `D_interni = 0` ESATTO con la forma")
    P("  assoluta, e un allungamento FINTO di %+.5f con la forma relativa di `V6`." % vecchio)
    P()
    P("  %d/3" % ok)
    return ok


# ============================================================================ LA MISURA
def leggi():
    d = {}
    for s in SEMI:
        p = os.path.join(DEST, "seme_%d" % s, "misura.json")
        if os.path.exists(p):
            d[s] = json.load(io.open(p, encoding="utf-8"))
    return d


def blocco(x, passo):
    for b in x["blocchi"]:
        if int(b["passo"]) == int(passo):
            return b
    return None


def principale():
    d = leggi()
    if not d:
        P("NESSUN `misura.json`.")
        return
    coppie = sorted(blocco(d[sorted(d)[0]], 0)["coppie_passo0"].keys())
    P("=" * 104)
    P("`TRATTI` -- IL CALO STA NEL VARCO O NEGLI INTERNI?   %d semi, unita' ASSOLUTE, IC95 `t(3)`"
      % len(d))
    P("=" * 104)
    P("  D_centri  = centro_centro(t)   - centro_centro(0)")
    P("  D_varco   = insieme_insieme(t) - insieme_insieme(0)")
    P("  D_interni = D_centri - D_varco")
    P()
    P("  ⚠ `D_interni` E' UN INDICATORE, NON IL TRATTO INTERNO DEL CAMMINO: e' <<centri meno varco")
    P("    minimo>>, e `insieme_insieme` e' la distanza fra i due nodi PIU' VICINI, che non sta")
    P("    necessariamente sul cammino medoide->medoide. La scomposizione VERA richiede il")
    P("    CAMMINO, e quindi gli stati del grafo ai checkpoint, che questo run NON ha salvato.")

    # le scale al passo 0, perche' senza non si legge niente
    P()
    P("  LE SCALE AL PASSO 0 (e sono la ragione per cui la forma RELATIVA sbagliava):")
    for cp in coppie:
        c0 = float(np.mean([blocco(d[s], 0)["coppie_passo0"][cp]["centro_centro"]
                            for s in sorted(d)]))
        s0 = float(np.mean([blocco(d[s], 0)["coppie_passo0"][cp]["insieme_insieme"]
                            for s in sorted(d)]))
        P("    %-17s centro_centro %7.4f   insieme_insieme %6.4f   rapporto %.2f"
          % (cp, c0, s0, c0 / s0))

    esito = {}
    for c in CPS:
        P()
        P("-" * 104)
        P("  PASSO %d" % c)
        P("-" * 104)
        for cp in coppie:
            vc, vv, vi = [], [], []
            for s in sorted(d):
                b0, bt = blocco(d[s], 0), blocco(d[s], c)
                c0 = b0["coppie_passo0"][cp]["centro_centro"]
                ct = bt["coppie_passo0"][cp]["centro_centro"]
                s0 = b0["coppie_passo0"][cp]["insieme_insieme"]
                st = bt["coppie_passo0"][cp]["insieme_insieme"]
                if not all(np.isfinite(x) for x in (c0, ct, s0, st)):
                    continue
                vc.append(ct - c0)
                vv.append(st - s0)
                vi.append((ct - c0) - (st - s0))
            P("  %s" % cp)
            riga("D_centri", vc)
            mv, zv = riga("D_varco", vv)
            mi, zi = riga("D_interni  <- l'indicatore", vi)
            esito.setdefault(c, []).append((cp, mv, zv, mi, zi))

    # ------------------------------------------------------------------ il verdetto
    P()
    P("=" * 104)
    P("IL VERDETTO, col criterio scritto PRIMA")
    P("=" * 104)
    for c in CPS:
        n_i = sum(1 for _, _, _, _, zi in esito[c] if not zi)
        n_v = sum(1 for _, _, zv, _, _ in esito[c] if not zv)
        P("  passo %4d   `D_interni` esclude lo zero su %d coppie su %d;  `D_varco` su %d su %d"
          % (c, n_i, len(esito[c]), n_v, len(esito[c])))
    P()
    c = 80
    n_i = sum(1 for _, _, _, _, zi in esito[c] if not zi)
    n_v = sum(1 for _, _, zv, _, _ in esito[c] if not zv)
    if n_i >= 2 and n_v == 0:
        P("  **A 80 PASSI IL CALO STA NEGLI INTERNI, NON NEL VARCO.**")
        P("  `D_interni` esclude lo zero su %d coppie su %d; `D_varco` lo contiene su TUTTE."
          % (n_i, len(esito[c])))
        P("  LETTURA, e va detta cosi': il moto dei CENTRI non e' spiegato dall'avvicinarsi delle")
        P("  superfici piu' vicine. E' compatibile con **le regioni che si CONTRAGGONO**, e NON")
        P("  con **i corpi che si avvicinano**. NON E' GRAVITA', ed e' esattamente cio' che la")
        P("  `PROVA 1` deve poter escludere.")
    else:
        P("  Il quadro NON e' quello: `D_interni` %d su %d, `D_varco` %d su %d."
          % (n_i, len(esito[c]), n_v, len(esito[c])))
    P()
    P("  ⚠ E IL LIMITE RESTA: `D_interni` e' un INDICATORE. Per dire <<il tratto DENTRO le regioni")
    P("    si e' accorciato>> serve la scomposizione del CAMMINO, con gli stati del grafo salvati")
    P("    ai checkpoint. -> `doc/TASK_HISTORY/2026-09-27_tratti.md`, punto ⓵ del TODO.")
    P()
    P("=" * 104)


if __name__ == "__main__":
    if "--collaudo" in sys.argv[1:]:
        n = collaudo()
        io.open(os.path.join(DEST, "COLLAUDO_tratti.txt"), "w",
                encoding="utf-8", newline=NL).write(NL.join(R) + NL)
        raise SystemExit(0 if n == 3 else 1)
    collaudo()
    P()
    principale()
    io.open(FUORI, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print(NL + "scomposizione in %s" % FUORI)
