# -*- coding: utf-8 -*-
r"""**`ambito` CONTRO LA MATRICE DAL CODICE, CONTATO** — *il passo `D` della memoria.*

> ### ⛔ **PERCHE' ESISTE** *(`2026-10-19`)*: la correzione del guardiano *(errore
> `n.11`)* chiede di registrare ### **come OSSERVAZIONE, senza toccare `leggi.yaml`**, che
> ### **`ambito` non dichiara le letture di `cs`** -- e il task history *(passo `D`)* vuole
> ### **quante dipendenze la tabella NON dichiara, contate.**

## ⭐ CHE COSA CONFRONTA

Per ogni legge dell'ordine di composizione: le dipendenze ### **misurate** dalla matrice
del passo `C` *(`csv/_matrice_dipendenze.dinamica`, unite sulle posizioni)* contro
### **`ambito`** in `primo_ordine/leggi/leggi.yaml` *(letto con `_genera.carica`)*:
- `W psi_h` / `W phi_h`: la legge **scrive** quel campo;
- `R psi_h` *(legge la materia)* / `R phi_h` *(legge il vuoto)*;
- `R cs`: la legge **legge `cs`**.
### ⚠ **`ambito` e' UNA lista** *(«le variabili che PUO' leggere»)*: non distingue
lettura da scrittura, quindi una dipendenza conta come dichiarata ### **se la sua variabile
e' nella lista**, in lettura o in scrittura.
### ⛔ **E `cs` NON E' nel vocabolario delle variabili** *(`psi`, `psi_h`, `phi_h`,
`Lambda`, `rho`, `h_int`)*: ### **nessun `ambito` puo' dichiararlo.** Si contano DUE
modi: ### **STRETTO** *(`cs` dichiarato solo se compare `cs`)* e ### **LARGO** *(basta
`Lambda`, perche' `cs` e' una funzione di `Lambda`)*.

## ⛔ I CASI

- ### **DEVE RIUSCIRE:** `CAMM-SPOSTAMENTO` *(`ambito: [psi_h]`)* ha `R cs` ### **NON
  dichiarato** nei due modi -- e' l'esempio della correzione `n.11`, il falso zero.
- ### **DEVE FALLIRE** *(cioe' NON risultare non dichiarato)*: `W psi_h` di
  `CAMM-MATERIA-VUOTO`, che ha `psi_h` in `ambito`. ### **Un confronto che segnasse tutto
  come mancante sarebbe un falso uno.**

Gira con:  python csv/_ambito_contro_matrice.py
"""
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "primo_ordine"))

import _matrice_dipendenze as MD                               # noqa: E402


def dipendenze(righe):
    """### `{legge: set di (verso, variabile)}`, ### **unite sulle posizioni.**"""
    fuori = {}
    for d in righe:
        s = fuori.setdefault(d["id"], set())
        if d["scrive_psi"]:
            s.add(("W", "psi_h"))
        if d["scrive_phi"]:
            s.add(("W", "phi_h"))
        if d["legge_materia"]:
            s.add(("R", "psi_h"))
        if d["legge_vuoto"]:
            s.add(("R", "phi_h"))
        if d["legge_cs"]:
            s.add(("R", "cs"))
    return fuori


def dichiarata(dip, ambito, largo):
    verso, var = dip
    if var == "cs":
        return "cs" in ambito or (largo and "Lambda" in ambito)
    return var in ambito


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import _genera as G
    leggi, varia, _o = G.carica()
    vocab = [v["nome"] for v in varia]
    ambiti = {l["id"]: list(l.get("ambito") or []) for l in leggi}
    righe, lc, rapp = MD.dinamica()
    dip = dipendenze(righe)
    print("=" * 100)
    print("`ambito` CONTRO LA MATRICE DAL CODICE, CONTATO -- il passo `D` della memoria")
    print("=" * 100)
    print("  la matrice: csv/_matrice_dipendenze.dinamica (taglia %d, Lambda_c = %.2f,"
          " rapporto %.3f)" % (MD.TAGLIA, lc, rapp))
    print("  la tabella: primo_ordine/leggi/leggi.yaml (via _genera.carica)")
    print("  il vocabolario delle variabili: %s   -- `cs` %s"
          % (vocab, "C'E'" if "cs" in vocab else "NON C'E'"))
    print("-" * 100)
    print("  %-24s %-34s %-24s %s" % ("legge", "ambito", "misurate", "NON dichiarate"
                                      " (stretto | largo)"))
    tot, ns, nl = 0, 0, 0
    mancanti = {}
    for idl in sorted(dip):
        amb = ambiti[idl]
        mis = sorted(dip[idl])
        st = [x for x in mis if not dichiarata(x, amb, False)]
        lg = [x for x in mis if not dichiarata(x, amb, True)]
        mancanti[idl] = (st, lg)
        tot += len(mis)
        ns += len(st)
        nl += len(lg)
        print("  %-24s %-34s %-24s %s | %s"
              % (idl, ",".join(amb), " ".join("%s %s" % x for x in mis),
                 " ".join("%s %s" % x for x in st) or "-",
                 " ".join("%s %s" % x for x in lg) or "-"))
    print("-" * 100)
    print("### CONTATE: %d dipendenze misurate; NON dichiarate in `ambito`: %d (stretto),"
          " %d (largo)" % (tot, ns, nl))
    rcs = sum(1 for idl in dip if ("R", "cs") in dip[idl])
    print("### e le letture di `cs`: %d leggi su %d la leggono; in `ambito` c'e' `cs` in %d,"
          " c'e' `Lambda` in %d" % (rcs, len(dip), sum(1 for i in dip if "cs" in ambiti[i]),
                                    sum(1 for i in dip if ("R", "cs") in dip[i]
                                        and "Lambda" in ambiti[i])))
    print("-" * 100)
    ok1 = (("R", "cs") in mancanti["CAMM-SPOSTAMENTO"][0]
           and ("R", "cs") in mancanti["CAMM-SPOSTAMENTO"][1])
    ok2 = ("W", "psi_h") in dip["CAMM-MATERIA-VUOTO"] and \
        ("W", "psi_h") not in mancanti["CAMM-MATERIA-VUOTO"][0]
    print("  DEVE RIUSCIRE: R cs di CAMM-SPOSTAMENTO NON dichiarato (stretto e largo)  %s"
          % ("PASSA" if ok1 else "### FALLISCE"))
    print("  DEVE FALLIRE:  W psi_h di CAMM-MATERIA-VUOTO risulta non dichiarato      %s"
          % ("PASSA (non risulta)" if ok2 else "### FALLISCE"))
    print("-" * 100)
    print("### ⛔ OSSERVAZIONE, NON UNA DECISIONE: `leggi.yaml` NON si tocca. Se vada aggiunto")
    print("###   un campo alla tabella (cambierebbe l'impronta) e' una decisione di Luca.")
    print("=" * 100)
    return 0 if ok1 and ok2 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
