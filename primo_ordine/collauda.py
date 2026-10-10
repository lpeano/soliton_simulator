# -*- coding: utf-8 -*-
"""PUNTO `6` DELLA TERZA PARTE — **UN SOLO COMANDO, E I TEMPI.**

> ### ⛔ **Il mandato, alla lettera:** *«**I TEMPI:** budget dichiarato per il
> `pre-commit`, suite completa in CI; **un solo comando**, `primo_ordine/collauda.py`,
> esegue tutti i collaudi e **stampa i tempi**. Oltre il budget → segnale»*.

### ⭐ **E <<OLTRE IL BUDGET → SEGNALE>> E' LA PARTE CHE CONTA, non il budget.** Un budget
che ### **FERMA** sarebbe un presidio sul tempo di una macchina — e il tempo di una
macchina ### **non è una proprietà del repo**: cambia col PC, col carico, col disco.
### ⛔ **Fermare su quello vorrebbe dire rifiutare un commit perché il computer era
occupato.** ### ✅ **Un SEGNALE invece dice una cosa vera: <<questo `pre-commit` sta
diventando una ragione per dare `--no-verify`>>** — ed è il difetto che `A9` descrive,
### **arrivato dal lato del tempo.**

### 📌 **IL BUDGET E' DICHIARATO E NON SCELTO:** `120` secondi, ### **che è il valore che
questo repo ha già misurato come soglia** — i collaudi lenti *(la catena, il referto
dell'infrastruttura)* ### **lo superano, e per quello vivono SOLO nella CI.** ### **Non
l'ho tarato io: era già la riga di divisione fra `VELOCI` e `LENTI`.**

### ⚠ **E I TEMPI NON SONO UN NUMERO DEL REPO: sono una MISURA DI QUESTA MACCHINA.** Il
referto li stampa ### **con la piattaforma accanto**, perché ### **un tempo senza la
macchina che l'ha prodotto non si può confrontare con niente.**
"""
import io
import os
import subprocess
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, os.path.join(RADICE, "csv"))

NL = chr(10)
PRESIDIO = "P-TEMPI"

# ### ⛔ **IL BUDGET, in secondi.** ### **Non e- scelto: e- la riga di divisione fra
# ### `VELOCI` e `LENTI` che `csv/_replay_registri.py` ha gia-** -- e quella nasce da una
# ### misura, non da un gusto.
BUDGET = 120.0

# ### ⚠ **I COLLAUDI, DICHIARATI UNO A UNO.** ### **Non si scoprono con un `glob`:**
# ### un `glob` prenderebbe ### **anche un file nuovo che nessuno ha ancora guardato**, e
# ### ### **un collaudo che nessuno ha deciso di far girare non e- una garanzia.**
#   `(nome, comando, dove)`  --  `dove`: `pre-commit` oppure `solo-CI`
COLLAUDI = (
    # ------------------------------------------------------------------ `primo_ordine/`
    ("il grafo valido", "primo_ordine/_collauda_grafo.py", "pre-commit"),
    ("il determinismo", "primo_ordine/_collauda_determinismo.py", "pre-commit"),
    ("le simmetrie e le conservazioni", "primo_ordine/_collauda_simmetrie.py",
     "pre-commit"),
    ("lo schema della tabella", "primo_ordine/leggi/schema.py", "pre-commit"),
    ("il generatore", "primo_ordine/_collauda_genera.py", "pre-commit"),
    ("lo schema della configurazione", "primo_ordine/config/schema_config.py",
     "pre-commit"),
    ("`@rif` byte-inerte", "primo_ordine/_rif.py", "pre-commit"),
    ("il modello di sigillo", "primo_ordine/sigilli/_modello.py", "pre-commit"),
    # ### ⭐ **E LA CATENA STA NEL `pre-commit`, PERCHE- L-HO MISURATA: `2.55` s.**
    # ### ⛔ **Era classificata LENTA** -- <<oltre i `120` secondi>> -- e
    # ### ### **quel numero era di un-altra cosa**: i lenti veri sono ### **i generatori
    # ### di referto** *(`45.99` e `28.33` s)*.
    # ### ⚠ **Questo e- il punto in cui un comando che STAMPA I TEMPI ha pagato: la
    # ### classificazione era asserita, non misurata.**
    ("la catena", "primo_ordine/_collauda_passo.py", "pre-commit"),
    # ### ⚠ **I LENTI VERI, e stanno SOLO in CI**: non perche- superino il budget da
    # ### soli, ma perche- ### **lo superano SOMMATI a tutto il resto.**
    ("il referto della seconda parte (LENTO)", "csv/_referto_seconda_parte.py",
     "solo-CI"),
    ("il referto dell-infrastruttura (LENTO)", "csv/_referto_infrastruttura_era2.py",
     "solo-CI"),
    # ------------------------------------------------------------------ `csv/`
    ("la barriera dei hook", "csv/_barriera.py --collaudo", "pre-commit"),
    ("`P-ALB` l-albero delle scelte", "csv/_albero_era2.py --collaudo", "pre-commit"),
    ("`P-ID` un id che nasce", "csv/_id_nuovo.py --collaudo", "pre-commit"),
    ("`P-T2` il replay dei registri", "csv/_replay_registri.py --collaudo", "pre-commit"),
    ("l-arbitro fra le due vie", "csv/_registri_indice.py --collaudo", "pre-commit"),
    ("i presidi dell-indice", "csv/_presidio_indice.py --collaudo", "pre-commit"),
)


def gira(cmd):
    """### `(secondi, codice)`. ### **Il tempo lo misura `perf_counter`**, non `time`."""
    pezzi = cmd.split()
    t0 = time.perf_counter()
    r = subprocess.run([sys.executable] + pezzi, cwd=RADICE, capture_output=True)
    return time.perf_counter() - t0, r.returncode


def macchina():
    """La macchina, ### **perche- un tempo senza la macchina non si confronta.**"""
    import platform
    return "%s %s, python %s" % (platform.system(), platform.machine(),
                                 sys.version.split()[0])


def main(argv):
    solo_veloci = "--solo-veloci" in argv
    scelti = [x for x in COLLAUDI if not solo_veloci or x[2] == "pre-commit"]
    print("=" * 100)
    print("TUTTI I COLLAUDI, CON I TEMPI   (punto 6)")
    print("=" * 100)
    print("  la macchina: %s" % macchina())
    print("  il budget del `pre-commit`: %.0f s   ### e oltre il budget e- un SEGNALE, "
          "non un rifiuto" % BUDGET)
    print()
    print("  %-38s %-10s %9s  %s" % ("il collaudo", "dove", "secondi", "esito"))
    print("  " + "-" * 94)
    tot = {"pre-commit": 0.0, "solo-CI": 0.0}
    rotti = []
    for nome, cmd, dove in scelti:
        s, rc = gira(cmd)
        tot[dove] += s
        if rc != 0:
            rotti.append((nome, cmd, rc))
        print("  %-38s %-10s %9.2f  %s"
              % (nome, dove, s, "ok" if rc == 0 else "### FALLISCE (codice %d)" % rc))
    print("  " + "-" * 94)
    print("  %-38s %-10s %9.2f" % ("IL TOTALE del `pre-commit`", "", tot["pre-commit"]))
    if not solo_veloci:
        print("  %-38s %-10s %9.2f" % ("piu- i LENTI, solo in CI", "", tot["solo-CI"]))
        print("  %-38s %-10s %9.2f" % ("IN TUTTO", "", sum(tot.values())))
    print()
    # ------------------------------------------------------------------ il VERDETTO
    if rotti:
        print("  ### %d COLLAUDI FALLISCONO:" % len(rotti))
        for nome, cmd, rc in rotti:
            print("     %-38s `%s` -> codice %d" % (nome, cmd, rc))
    else:
        print("  ### TUTTI I COLLAUDI PASSANO: %d su %d" % (len(scelti), len(scelti)))
    if tot["pre-commit"] > BUDGET:
        print()
        print("  ### ⚠ SEGNALE: il `pre-commit` costa %.1f s, oltre il budget di "
              "%.0f s." % (tot["pre-commit"], BUDGET))
        print("  ### Non e- un rifiuto, ed e- una scelta: il tempo di una macchina NON E-")
        print("  ### una proprieta- del repo, e fermare su quello vorrebbe dire rifiutare")
        print("  ### un commit perche- il computer era occupato.")
        print("  ### MA UN `pre-commit` COSI- E- UNA RAGIONE PER DARE `--no-verify`, ed e-")
        print("  ### il difetto di `A9` arrivato dal lato del tempo: un presidio che si")
        print("  ### spegne perche- costa troppo NON E- UN PRESIDIO.")
    else:
        print("  ### il `pre-commit` sta nel budget: %.1f s su %.0f s (%.0f%%)"
              % (tot["pre-commit"], BUDGET, 100.0 * tot["pre-commit"] / BUDGET))
    print("=" * 100)
    # ### ⛔ **IL CODICE D-USCITA GUARDA I COLLAUDI, NON I TEMPI:** il budget
    # ### ### **segnala** e ### **non rifiuta**, ed e- scritto sopra.
    return 1 if rotti else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
