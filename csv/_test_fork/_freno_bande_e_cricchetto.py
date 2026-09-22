# -*- coding: utf-8 -*-
"""LE DUE MISURE SUL FRENO. Punto 5 del mandato dei sospesi. NESSUNA CURA.

(a) LE BANDE -- distribuzione di `d0/LAM` sugli snapshot gia' scritti, e quanta parte del freno
    viene da ciascuna banda.
(b) IL CRICCHETTO -- `_smorza` applicato DA SOLO a rumore simmetrico sintetico, LONTANO dal
    confine. **Se il freno e' un cricchetto, la somma DEVE derivare verso l'ALTO.**

IL CRITERIO, SCRITTO PRIMA DI VEDERE I NUMERI:

  (b1) Con rumore a media ESATTAMENTE nulla e `x0 >> LAM`, la somma dopo `P` passi deve
       **CRESCERE**. La deriva attesa per passo, derivata e non tarata:
           deriva = E[-dx | dx<0] * P(dx<0) * LAM/x
       perche' ogni discesa perde la frazione `LAM/x` e ogni salita passa intatta.
       **PASSA se la deriva misurata sta entro il `10 %` di quella attesa.**
  (b2) **IL CASO CHE DEVE FALLIRE: con `LAM = 0` la deriva dev'essere ESATTAMENTE ZERO.**
       Se il test mostra deriva anche a `LAM = 0`, la deriva non viene dal freno ma dal banco
       di prova, e **tutto il resto non si legge**.
  (b3) **SECONDO CASO CHE DEVE FALLIRE: un freno SIMMETRICO** *(stessa frazione applicata a
       salite E discese)* **deve dare deriva ZERO** sullo stesso rumore. E' il controllo che
       isola l'ASIMMETRIA come causa, invece dell'attenuazione.

  (a1) La banda che contribuisce di piu' NON e' necessariamente la piu' popolata: conta
       `popolazione * frazione annullata`. **Si riportano entrambe.**

⚠ CIO' CHE QUESTA MISURA NON PUO' DARE, e lo dico PRIMA: gli snapshot contengono `d0` ma **NON
  `dx`**, la variazione dentro il passo. **La quota esatta del freno per banda richiede `dx` e
  non e' ricavabile da uno snapshot.** Si riporta:
    * la popolazione per banda -- **ESATTA**;
    * la frazione annullata `LAM/d0` per banda -- **ESATTA**;
    * la quota del freno **SOTTO L'IPOTESI DICHIARATA** che le discese siano distribuite in modo
      uniforme fra le bande. **E' una STIMA, ed e' etichettata come tale.**

SOLA LETTURA sugli snapshot. Il cricchetto e' interamente SINTETICO.
ASCII PURO.
"""
import gzip
import io
import os
import pickle
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SORGENTE = os.path.join(RADICE, "soliton_simulator.py")
OUT = os.path.join(_QUI, "_diag_D", "FRENO_BANDE_E_CRICCHETTO.md")
ARCHIVI = [("G4 riferimento", "_g4_riferimento"), ("G4 senza memoria del moto", "_g4_senza_memmoto")]
BANDE = [(1.0, 1.1), (1.1, 1.5), (1.5, 2.0), (2.0, 3.0), (3.0, np.inf)]


def costante(nome):
    t = io.open(SORGENTE, encoding="utf-8").read()
    m = re.search(r"^%s\s*=\s*([^\s#]+)" % re.escape(nome), t, re.M)
    return eval(m.group(1), {"np": np, "__builtins__": {}}) if m else None


def smorza(prima, dx, lam):
    """LA STESSA FORMA del simulatore (`:3526`), copiata dal codice."""
    prima = np.asarray(prima, float); dx = np.asarray(dx, float)
    scende = dx < 0.0
    pos = prima > 0.0
    base = np.where(pos, prima, 1.0)
    fatt = np.where(pos, np.maximum(0.0, 1.0 - lam / base), 0.0)
    return np.where(scende, dx * fatt, dx)


def smorza_simmetrico(prima, dx, lam):
    """IL CONTROLLO di `b3`: la STESSA attenuazione, ma su ENTRAMBI i versi."""
    prima = np.asarray(prima, float); dx = np.asarray(dx, float)
    pos = prima > 0.0
    base = np.where(pos, prima, 1.0)
    fatt = np.where(pos, np.maximum(0.0, 1.0 - lam / base), 0.0)
    return dx * fatt


def cricchetto(W, lam_vero):
    """(b) IL TEST DEL CRICCHETTO, interamente SINTETICO."""
    W("## (b) IL TEST DEL CRICCHETTO — **`_smorza` da solo, su rumore SIMMETRICO**\n\n")
    W("> **Nessun simulatore, nessuno snapshot.** Rumore a media **esattamente** nulla "
      "*(antitetico: ogni `+a` ha il suo `-a`)*, **lontano dal confine**.\n\n")
    rng = np.random.default_rng(20260922)
    N, P = 200000, 400
    amp = 0.02
    esiti = []
    W("| caso | `x0/LAM` | `LAM` | deriva MISURATA per passo | deriva ATTESA | scarto | esito |\n")
    W("|---|--:|--:|--:|--:|--:|---|\n")
    prove = [("b1 il freno VERO, `x0 = 10*LAM`", 10.0, lam_vero, smorza, True),
             ("b1 il freno VERO, `x0 = 100*LAM`", 100.0, lam_vero, smorza, True),
             ("**b2 IL CASO CHE DEVE FALLIRE: `LAM = 0`**", 10.0, 0.0, smorza, False),
             ("**b3 IL CASO CHE DEVE FALLIRE: freno SIMMETRICO**", 10.0, lam_vero,
              smorza_simmetrico, False)]
    for eti, mult, lam, fn, deve_derivare in prove:
        x0 = mult * lam_vero
        x = np.full(N, x0)
        meta = N // 2
        for _k in range(P):
            a = rng.normal(0.0, amp * x0, meta)
            dx = np.concatenate([a, -a])          # media ESATTAMENTE zero, per costruzione
            rng.shuffle(dx)
            x = x + fn(x, dx, lam)
        mis = (float(np.mean(x)) - x0) / P
        # l'attesa, DERIVATA: ogni discesa perde la frazione LAM/x, le salite passano intatte
        sig = amp * x0
        att = (sig / np.sqrt(2 * np.pi)) * (lam / x0) if fn is smorza else 0.0
        sc = abs(mis - att) / max(abs(att), 1e-300) if att else abs(mis)
        if deve_derivare:
            ok = (mis > 0) and (sc <= 0.10)
            txt = "PASS" if ok else "*** FAIL ***"
        else:
            ok = abs(mis) <= max(1e-12, 0.01 * abs(sig) / np.sqrt(N * P))
            txt = ("PASS: nessuna deriva, come DEVE essere" if ok
                   else "*** FAIL: deriva SENZA il freno asimmetrico ***")
        esiti.append(ok)
        W("| %s | %.0f | %.4f | **%+.6e** | %+.6e | %.1f %% | %s |\n"
          % (eti, mult, lam, mis, att, 100 * sc, txt))
    W("\n> **`b1` — l'attesa e' DERIVATA, non tarata:** per rumore gaussiano simmetrico\n")
    W("> `E[-dx | dx<0]*P(dx<0) = sigma/sqrt(2 pi)`, e ogni discesa perde la frazione `LAM/x`.\n")
    W("> **deriva per passo = `sigma/sqrt(2 pi) * LAM/x`.**\n")
    W("> **`b2` e `b3` sono i casi che DEVONO dare zero**, e sono il motivo per cui `b1` si puo'\n")
    W("> leggere: senza di loro una deriva potrebbe venire dal banco di prova o dalla semplice\n")
    W("> attenuazione, invece che dall'ASIMMETRIA.\n\n")
    return all(esiti)


def main():
    lam = float(costante("LAM"))
    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    W = o.write
    W("# IL FRENO: **le BANDE di `d0/LAM`** e **il TEST DEL CRICCHETTO**\n\n")
    W("> Punto 5 del mandato dei sospesi. Generato da "
      "`csv/_test_fork/_freno_bande_e_cricchetto.py`.\n")
    W("> **`LAM = %s`, letto dal sorgente.** Le bande sugli snapshot gia' scritti; il cricchetto "
      "e' **interamente sintetico**.\n\n" % lam)

    ok_b = cricchetto(W, lam)

    W("\n## (a) LE BANDE DI `d0/LAM` — **dove il freno morde**\n\n")
    W("> La **frazione annullata** di una discesa e' `LAM/d0`: a `d0 = 1.1*LAM` il freno "
      "annulla il **`90.9 %`** di ogni discesa, a `d0 = 3*LAM` il **`33.3 %`**.\n>\n")
    W("> **⚠ LA QUOTA DEL FRENO E' UNA STIMA, e lo dico prima di scriverla:** gli snapshot "
      "hanno `d0` ma **NON `dx`**. La quota vale **sotto l'ipotesi DICHIARATA** che le discese "
      "siano distribuite in modo uniforme fra le bande. **Popolazione e frazione annullata sono "
      "invece ESATTE.**\n\n")
    for eti, cart in ARCHIVI:
        d = os.path.join(RADICE, "csv", "_test_fork", cart)
        if not os.path.isdir(d):
            continue
        files = sorted(f for f in os.listdir(d) if f.startswith("scena_") and f.endswith(".pkl.gz"))
        if not files:
            continue
        W("### %s\n\n" % eti)
        W("| passo | banda `d0/LAM` | archi | quota archi | frazione annullata `LAM/d0` "
          "(mediana) | **quota STIMATA del freno** |\n")
        W("|--:|---|--:|--:|--:|--:|\n")
        for f in files:
            passo = int(f.split("_")[1].split(".")[0])
            with gzip.open(os.path.join(d, f), "rb") as fh:
                a = pickle.load(fh)["attrs"]
            d0 = np.asarray(a["d0"], float)
            r = d0 / lam
            peso = []
            for lo, hi in BANDE:
                m = (r >= lo) & (r < hi)
                peso.append(float(np.sum(lam / np.maximum(d0[m], 1e-12))) if m.any() else 0.0)
            tot = sum(peso) or 1.0
            for (lo, hi), pw in zip(BANDE, peso):
                m = (r >= lo) & (r < hi)
                nb = int(np.sum(m))
                eti_b = ("`[%.1f, %.1f)`" % (lo, hi)) if np.isfinite(hi) else ("`>= %.1f`" % lo)
                W("| %d | %s | %d | %.2f %% | %s | **%.2f %%** |\n"
                  % (passo, eti_b, nb, 100.0 * nb / len(r),
                     ("%.4f" % float(np.median(lam / np.maximum(d0[m], 1e-12)))) if nb else "—",
                     100.0 * pw / tot))
        W("\n")

    W("\n## GLI ESITI, contro i criteri scritti PRIMA\n\n")
    W("- **(b) il cricchetto: %s.**\n"
      % ("**CONFERMATO** — il freno crea deriva su rumore a media nulla, e i due casi che "
         "devono dare zero la danno" if ok_b else "**i criteri NON tornano: si dichiara e non si "
         "conclude**"))
    W("- **(a) le bande:** popolazione e frazione annullata sono **esatte**; la quota del freno e' "
      "una **stima sotto ipotesi dichiarata**.\n")
    W("\n**LIMITI:** le bande vengono da UN seme, UNA scena, archivi delle cure. Il cricchetto e' "
      "**sintetico e non dipende da nessun run**: e' una proprieta' della FORMULA, e vale per "
      "qualunque seme.\n")
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0 if ok_b else 1


if __name__ == "__main__":
    sys.exit(main())
