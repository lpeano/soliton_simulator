# -*- coding: utf-8 -*-
r"""IL REFERTO DELLA DERIVA — **scritto da chi ha misurato, e non ricopiato.**

### ⛔ **PERCHE' STA IN UN FILE SUO:** `primo_ordine/deriva.py` ha passato il tetto di
`700` righe, e la regola e' ### **oltre SI DIVIDE, NON SI ALLUNGA.** ### ⚠ **E la riga di
taglio non e' casuale:** la- dentro c'e' ### **la MISURA**, qui c'e' ### **COME SI
RACCONTA** -- due responsabilita' diverse, e il presidio lo ha fatto notare prima di me.

### ⚠ **E `CONFIG` sta QUI**, perche' e' cio' che il referto ### **deve dichiarare per
intero** *(la regola di `H-P5`)*: il difetto che quel presidio cura e' ### **dichiarare i
parametri che ho toccato io e tacere i trenta che stavano a default.**
"""
import os

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))


DOVE = os.path.join(os.path.dirname(_QUI), "doc", "REFERTO_deriva_energia.md")
CONFIG = (("seme", 7),
          ("eps della moneta di spin", 0.5),
          ("sommatoria", "numpy"),
          ("psi iniziale", "gaussiano complesso dal seme, NORMALIZZATO a 1"),
          ("phi iniziale", "modulo 1, fasi uniformi dal seme"),
          ("versori n per estremita'", "gaussiani dal seme, normalizzati a 1"),
          ("U per arco", "U(2) casuale via QR, COMPAGNA = coniugata trasposta"),
          ("il tick", "l'ORDINE INTERO di composizione.py, 7 applicazioni"),
          ("il flusso N", "ACCESO, in due mezzi (Strang)"))


def scrivi_referto(dati):
    """### Il referto, ### **scritto dallo script che ha misurato** *(`L-NUMERI`).**

    ### ⚠ **E dichiara `CONFIG` per intero**, che e' la regola di **`H-P5`**.
    """
    import io
    import platform
    nl = chr(10)
    r = []
    r.append("# LA DERIVA DI `E` SUL TICK INTERO — **il `4.20` non si riproduce, e il"
             " perche' e' STRUTTURALE**")
    r.append("")
    r.append("> ### ⛔ **IL NUMERO VECCHIO ERA ORFANO** *(`L-NUMERI-DERIVA-ORFANA`)*:"
             " nessuno script lo")
    r.append("> produceva. ### **Questo referto lo sostituisce con numeri che escono da un"
             " comando.**")
    r.append("")
    r.append("Lo rigira:  `python primo_ordine/deriva.py --scrivi`")
    r.append("")
    r.append("## 1. LA CONFIGURAZIONE INTERA")
    r.append("")
    r.append("| la voce | il valore |")
    r.append("|---|---|")
    for k, v in CONFIG:
        r.append("| %s | `%s` |" % (k, v))
    r.append("| piattaforma | `%s`, python `%s`, numpy `%s` |" %
             (platform.system(), platform.python_version(), np.__version__))
    r.append("")
    for blocco in dati:
        r.extend(blocco)
        r.append("")
    dati_b = (nl.join(r) + nl).encode("utf-8")
    io.open(DOVE, "wb").write(dati_b)
    return DOVE


def blocco_su2(sx2):
    """### Il blocco del referto per la scansione in `SU(2)`.

    ### ⛔ **Sta QUI e non nella misura:** `primo_ordine/deriva.py` ha ripassato il
    tetto di `700` righe quando questo blocco e' nato, e la regola e' ### **oltre SI
    DIVIDE.** ### ⚠ **E la riga di taglio e' la stessa di sempre: la- la MISURA, qui
    COME SI RACCONTA.**
    """
    b = ["## 8. **LA STESSA SCANSIONE, MA CON `U` IN `SU(2)`**", "",
         "### ⛔ **PERCHE' SI RIFA':** la misura delle bande"
         " *(`doc/REFERTO_bande.md`)* ha trovato",
         "che la `C` chiede **`det U = 1`**, e la scansione qui sopra e' fatta con `U(2)`",
         "generico. ### ⚠ **Non credevo che la conclusione cambiasse** -- la causa e'"
         " il termine",
         "del vuoto, che dipende da `h_k` -- ### **ma non l'avevo misurato.**", "",
         "| `|phi|` | `x` max | esc. **primo** | esc. **vuoto** | esc. **SOMMA** |"
         " esc./scala naturale: **SOMMA** |",
         "|--:|--:|--:|--:|--:|--:|"]
    for r2 in sx2:
        print("      |phi|=%-6.2f x_max=%-10.4g  esc: lin %-10.3e vuoto %-10.3e"
              " SOMMA %-10.3e   esc/scala SOMMA %.2e"
              % (r2["modulo"], r2["x_max"], r2["esc_primo"], r2["esc_vuoto"],
                 r2["esc_somma"], r2["relnat_somma"]))
        b.append("| `%.2f` | `%.4g` | `%.3e` | `%.3e` | **`%.3e`** | **`%.2e`** |" %
                 (r2["modulo"], r2["x_max"], r2["esc_primo"], r2["esc_vuoto"],
                  r2["esc_somma"], r2["relnat_somma"]))
    v2 = min(sx2, key=lambda z: abs(np.log10(max(z["x_max"], 1e-300))))
    pg2 = max(v2["esc_primo"], v2["esc_vuoto"])
    f2 = v2["esc_somma"] >= pg2
    print("      STOP in SU(2): x piu' vicino a 1 = %.4g; esc. SOMMA = %.3e contro %.3e"
          "  ->  %s" % (v2["x_max"], v2["esc_somma"], pg2,
                        "FERMA (come con U(2))" if f2 else "NON ferma"))
    b.append("")
    b.append("### %s **LA CONDIZIONE DI STOP, in `SU(2)`**, sul punto con `x` piu' vicino"
             " a `1` *(`x = %.4g`)*: escursione della **SOMMA** `%.3e` contro `%.3e` del"
             " maggiore dei termini — ### **%s**" %
             ("⛔" if f2 else "✅", v2["x_max"], v2["esc_somma"], pg2,
              "SCATTA ANCHE QUI" if f2 else "non scatta"))
    return b
