# -*- coding: utf-8 -*-
"""L'INERZIA DEGLI OSSERVATORI **ATTRAVERSO LE NASCITE**, senza una corsa in piu'.

*(Mandato di Luca del 2026-10-07. ### **Rilievo del guardiano, che riconosce il proprio
errore:** la byte-inerzia di `d01cc2a` girava su ### **`50` passi**, cioe' ### **PRIMA della
prima nascita (`216`)** — quindi gli involucri sulle funzioni di nascita
### **non sono mai stati esercitati mentre lavorano.**)*

### ✔ **E IL CONTROLLO E' GRATIS: la corsa di riferimento ESISTE GIA'**

`csv/_test_fork/_mitosi_zero_dove/amp0.json` e' il braccio ### **`_AMP = 0`** su
### **`1000` passi**, e il simulatore di oggi ### **riproduce quella corsa**:

| | |
|---|---|
| `amp0.json` | blob ### **`cf2a1ac8`** con `_AMP = 0`, cioe' la modulazione del `0.3` ### **annullata** |
| `S1` del sigillo ### **`6d7107b`** | ha verificato che ### **`30e18cdd`** *(il `0.3` USCITO)* riproduce `amp0.json` ### **AL BIT su `230` passi** |
| il sigillo ### **`35044cc`** | ha verificato che ### **`b8c21049`** differisce da `30e18cdd` ### **solo per DUE STRINGHE**, col codice compilato ### **IDENTICO** |

> ### ➜ **QUINDI `amp0.json` E' UN RIFERIMENTO VALIDO PER `b8c21049`**, e il confronto
> ### **non costa una corsa.**

### ⛔ **IL CRITERIO, FISSATO DA LUCA PRIMA DI GUARDARE**

> ### **Zero differenze su tutti i `1000` passi = gli osservatori, involucri di nascita
> compresi, NON cambiano la dinamica.**
> ### **Una differenza = il primo passo diverso e il campo vanno nel referto, e i numeri di
> `A1` DOPO quel passo NON VALGONO finche' non si trova la causa.**

### ⚠ **E UNA TRAPPOLA DI CONVENZIONE, che si prova invece di assumerla**

Nel `json` di riferimento ### **`n` viene da `chiudi` (POST-passo)** mentre
### **`archi` viene dal gancio della torsione (META' passo)**: al passo `216` si leggono
### **`n = 12804` e `archi = 471564`**, cioe' ### **due nodi nati e nessun arco nuovo** —
e un arco di divisione compare ### **al passo dopo.**

> ### ⛔ **QUINDI UN DISALLINEAMENTO DI UN PASSO SU `archi` SAREBBE UNA CONVENZIONE, NON UNA
> DIFFERENZA DI DINAMICA.** ### ✔ **Si provano ENTRAMBI gli allineamenti e si DICHIARA
> quale combacia** — ### **chiamare <<differenza>> una convenzione sarebbe un falso
> allarme, e chiamare <<convenzione>> una differenza sarebbe un insabbiamento.**

### ⚠ **E I CAMPI CHE LO STRUMENTO DI `A1` NON REGISTRA, DICHIARATI**

| campo del riferimento | lo strumento di `A1` lo registra? |
|---|---|
| `n` | ### ✔ **SI'** |
| `archi` | ### ✔ **SI'** |
| `nati_tot`, `schwinger_tot` | ### ⛔ **NO** — e ### **non si aggiunge ORA**: il `par.5` vieta di toccare un file del percorso in uso, e la corsa e' in volo |
| `q_tw` *(i quantili di `\|tw\|`)* | ### ⛔ **NO**: `A1` registra ### **la FRAZIONE sopra `2π`**, che non si ricava dai quantili. ### ✔ **Si fa un CONTROLLO DI COERENZA a forbice**, dichiarato come tale |

> ### ⚠ **`n` E `archi` A OGNI PASSO NON SONO POCO:** ### **`n` e' il conto delle nascite
> integrato** e ### **`archi` risente sia della mitosi** *(`-1 +2`)* ### **sia dello
> Schwinger** *(`+2`)*. ### **Uno spostamento di UNA nascita di UN passo si vedrebbe in
> entrambi.**
"""
import io
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
sys.path.insert(0, os.path.join(RADICE, "csv", "_test_fork"))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

import _mitosi_soglia_grad as _MSG               # noqa: E402

stampa, riga, blob = _MSG.stampa, _MSG.riga, _MSG.blob
NL = chr(10)
FUORI = os.path.join(_QUI, "_inerzia_nascite")
RIF = os.path.join(RADICE, "csv", "_test_fork", "_mitosi_zero_dove", "amp0.json")
OSS = os.path.join(RADICE, "csv", "_test_fork", "_misura_verso", "verso.json")
P2PI = 2.0 * np.pi
# ### I CAMPI CHE SI CONFRONTANO, e quelli che si DICHIARANO non registrati.
CONFRONTA = ("n", "archi")
NON_REGISTRATI = ("nati_tot", "schwinger_tot", "q_tw")


def forbice_quantili(q):
    """La FORBICE sulla frazione sopra `2pi`, dai QUANTILI. ### **E si collauda.**

    ### ⛔ **LA PRIMA VERSIONE ERA SBAGLIATA IN DUE MODI MIEI:** dividevo i percentili
    per ### **`1000`** invece che per `100`, e avevo ### **`lo` e `hi` SCAMBIATI.**
    ### **Trovato rileggendo lo strumento prima di usarlo**, non dai numeri.
    ### ⚠ **Una forbice sbagliata non alza niente: avrebbe DICHIARATO un disaccordo
    inesistente, o taciuto uno vero.** ### ✔ **Percio' ora e' una FUNZIONE con un
    collaudo**, invece di sei righe dentro un ciclo.

    ### LA DERIVAZIONE, scritta: le chiavi sono `q000`..`q100`, cioe' PERCENTILI.
      se `q_p > 2pi` allora ### **piu' di `1 - p/100`** degli archi sta sopra `2pi`;
      se `q_p <= 2pi` allora ### **al piu' `1 - p/100`** ci sta.
    ### ➜ `lo = 1 - min{p : q_p > 2pi}/100`  e  `hi = 1 - max{p : q_p <= 2pi}/100`.
    """
    pp = [(int(kk[1:]), float(v)) for kk, v in q.items() if kk.startswith("q")]
    if not pp:
        return None
    sotto = [p for p, v in pp if v <= P2PI]
    sopra = [p for p, v in pp if v > P2PI]
    hi = (1.0 - max(sotto) / 100.0) if sotto else 1.0
    lo = (1.0 - min(sopra) / 100.0) if sopra else 0.0
    return lo, hi


def collaudo():
    """### **I casi della forbice, e UNO DEVE FALLIRE.**"""
    esiti = []

    def prova(et, ok):
        esiti.append(bool(ok))
        stampa("  %s  %s" % ("ok  " if ok else "FALLITO", et))

    _s, _g = P2PI * 0.5, P2PI * 2.0      # sotto e sopra `2pi`
    # ---- tutti SOTTO: la frazione e' ZERO, e la forbice deve essere [0, 0]
    q = {"q%03d" % p: _s for p in (0, 1, 5, 25, 50, 75, 95, 99, 100)}
    f = forbice_quantili(q)
    prova("forbice: ### tutti i quantili SOTTO `2pi` -> `[0, 0]`, cioe' frazione ZERO",
          f == (0.0, 0.0))
    # ---- tutti SOPRA: la frazione e' UNO
    q = {"q%03d" % p: _g for p in (0, 1, 5, 25, 50, 75, 95, 99, 100)}
    f = forbice_quantili(q)
    prova("forbice: ### tutti SOPRA -> `[1, 1]`, cioe' frazione UNO", f == (1.0, 1.0))
    # ---- il caso che conta: `q095 <= 2pi < q099`
    q = {"q%03d" % p: (_g if p >= 99 else _s)
         for p in (0, 1, 5, 25, 50, 75, 95, 99, 100)}
    f = forbice_quantili(q)
    prova("forbice: ### `q095 <= 2pi < q099` -> `[0.01, 0.05]`, e una frazione del `3 %` "
          "ci sta dentro",
          f is not None and abs(f[0] - 0.01) < 1e-12 and abs(f[1] - 0.05) < 1e-12
          and f[0] <= 0.03 <= f[1])
    # ---- ### ⛔ **IL CASO CHE DEVE FALLIRE: la VERSIONE SBAGLIATA, /1000 e scambiata**
    pp = [(int(kk[1:]), float(v)) for kk, v in q.items() if kk.startswith("q")]
    _sopra = [p for p, v in pp if v > P2PI]
    _lo_sb = 1.0 - max(_sopra) / 1000.0
    _hi_sb = 1.0 - min(_sopra) / 1000.0
    _lo_sb, _hi_sb = min(_lo_sb, _hi_sb), max(_lo_sb, _hi_sb)
    prova("forbice: ### DEVE FALLIRE -- la versione VECCHIA da' `[%.3f, %.3f]`, che NON "
          "contiene il `3 %%`: avrebbe dichiarato un disaccordo INESISTENTE"
          % (_lo_sb, _hi_sb),
          not (_lo_sb <= 0.03 <= _hi_sb))
    # ---- un dizionario senza quantili non inventa una forbice
    prova("forbice: ### un dizionario SENZA quantili da' `None`, non `[0, 1]`",
          forbice_quantili({"altro": 1.0}) is None)
    riga("-")
    stampa("  COLLAUDO: %d su %d" % (sum(esiti), len(esiti)))
    return 0 if all(esiti) else 1


def main(argv):
    if "--collaudo" in argv[1:]:
        riga("=")
        stampa("IL COLLAUDO DELLA FORBICE DI _inerzia_nascite.py")
        riga("=")
        return collaudo()
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    riga("=")
    stampa("L'INERZIA DEGLI OSSERVATORI ATTRAVERSO LE NASCITE")
    riga("=")
    for p in (RIF, OSS):
        if not os.path.isfile(p):
            stampa("  ### manca %s. MI FERMO." % p)
            return 1
    R = json.load(io.open(RIF, encoding="utf-8"))
    O = json.load(io.open(OSS, encoding="utf-8"))
    stampa("  riferimento  %s   blob %s   stato %s   passi %s"
           % (os.path.basename(RIF), str(R.get("blob_sim"))[:8], R.get("stato"),
              R.get("passi_girati")))
    stampa("  osservata    %s   blob %s   stato %s   passi %s"
           % (os.path.basename(OSS), str(O.get("blob_sim"))[:8], O.get("stato"),
              O.get("passi_girati")))
    if O.get("stato") != "DATI SALVATI" or O.get("passi_girati") != O.get("passi"):
        stampa("  ### ⛔ LA CORSA OSSERVATA NON E' COMPLETA. MI FERMO, e lo dico.")
        return 1
    rr = {int(x["passo"]): x for x in R.get("passi_dati", [])}
    oo = {int(x["passo"]): x for x in O["verso"]["passi"]}
    comuni = sorted(set(rr) & set(oo))
    stampa("  passi in comune: %d  (riferimento %d, osservata %d)"
           % (len(comuni), len(rr), len(oo)))
    stampa()
    # ### I DUE ALLINEAMENTI, PROVATI: `0` e `-1` sul riferimento.
    esiti = {}
    for campo in CONFRONTA:
        for off in (0, -1):
            dif = []
            for k in comuni:
                k2 = k + off
                if k2 not in rr:
                    continue
                a, b = rr[k2].get(campo), oo[k].get(campo)
                if a is None or b is None:
                    continue
                if int(a) != int(b):
                    dif.append((k, int(a), int(b)))
            esiti[(campo, off)] = dif
            stampa("  %-7s allineamento %+d:  differenze %d%s"
                   % (campo, off, len(dif),
                      ("   primo: passo %d  rif %d  oss %d" % dif[0]) if dif else ""))
    stampa()
    riga("-")
    # ### LA LETTURA: per ogni campo vince l'allineamento con ZERO differenze, e si DICHIARA.
    scelto, ok = {}, True
    for campo in CONFRONTA:
        zeri = [off for off in (0, -1) if not esiti[(campo, off)]]
        if zeri:
            scelto[campo] = {"allineamento": zeri[0], "differenze": 0}
            stampa("  ### ✔ `%s`: ZERO differenze con allineamento %+d su %d passi."
                   % (campo, zeri[0], len(comuni)))
        else:
            d0 = esiti[(campo, 0)]
            scelto[campo] = {"allineamento": None, "differenze": len(d0),
                             "primo": list(d0[0]) if d0 else None}
            ok = False
            stampa("  ### ⛔ `%s`: NESSUN allineamento da zero differenze." % campo)
            stampa("  ###    il primo passo diverso (allineamento 0): passo %d, "
                   "riferimento %d, osservata %d" % d0[0])
    stampa()
    # ### IL CONTROLLO A FORBICE su `q_tw`, dichiarato come forbice e non come uguaglianza.
    forbice = []
    for k in comuni:
        q = rr[k].get("q_tw") or {}
        f = oo[k].get("fraz_tw_oltre_2pi")
        if not q or f is None:
            continue
        _fb = forbice_quantili(q)
        if _fb is None:
            continue
        lo, hi = _fb
        forbice.append((k, f, lo, hi, bool(lo - 1e-9 <= f <= hi + 1e-9)))
    fuori_f = [x for x in forbice if not x[4]]
    stampa("  controllo a FORBICE su `q_tw` contro la frazione sopra 2pi: %d passi, "
           "%d fuori forbice" % (len(forbice), len(fuori_f)))
    stampa("  ### ⚠ E' UNA FORBICE, NON UN'UGUAGLIANZA: dai quantili non si ricava la "
           "frazione esatta.")
    for x in fuori_f[:5]:
        stampa("      passo %d: frazione %.4f, forbice [%.4f, %.4f]" % (x[0], x[1], x[2], x[3]))
    stampa()
    riga("=")
    if ok:
        stampa("  ### ✔ IL CRITERIO DI LUCA E' SODDISFATTO: ZERO differenze su %d passi."
               % len(comuni))
        stampa("  ### Gli osservatori, INVOLUCRI DI NASCITA COMPRESI, non cambiano la "
               "dinamica.")
    else:
        stampa("  ### ⛔ IL CRITERIO NON E' SODDISFATTO.")
        stampa("  ### I numeri di A1 DOPO il primo passo diverso NON VALGONO finche' non "
               "si trova la causa.")
    riga("=")
    stampa("  campi NON registrati dallo strumento di A1, DICHIARATI: %s"
           % ", ".join(NON_REGISTRATI))
    d = {"riferimento": os.path.basename(RIF), "blob_riferimento": R.get("blob_sim"),
         "blob_osservata": O.get("blob_sim"), "passi_comuni": len(comuni),
         "confrontati": list(CONFRONTA), "non_registrati": list(NON_REGISTRATI),
         "esito_per_campo": scelto,
         "differenze": {("%s@%+d" % (c, o)): len(v) for (c, o), v in esiti.items()},
         "forbice_q_tw": {"passi": len(forbice), "fuori": len(fuori_f),
                          "primi_fuori": [list(x[:4]) for x in fuori_f[:5]]},
         "esito": "PASSA" if ok else "FALLISCE"}
    io.open(os.path.join(FUORI, "nascite.json"), "w", encoding="utf-8").write(
        json.dumps(d, indent=1, default=str))
    io.open(os.path.join(FUORI, "nascite.txt"), "w", encoding="utf-8").write(
        NL.join(_MSG.P) + NL)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
