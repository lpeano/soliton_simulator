# -*- coding: utf-8 -*-
"""PUNTI `5`, `6` e `10` — **IL TIMBRO, SALVA-E-RIPRENDI, e IL CONTO DELLE LEGGI.**

> ### ⛔ **`5`** *«ogni uscita porta **l'impronta della tabella e dei generati**, la
> composizione, il seme, e le versioni»* — piu' ### **l'impronta della
> configurazione** *(punto `15`)*.
> ### ⛔ **`6`** *«salva e riprendi: tutto lo stato + l'impronta; la ripresa
> **RIFIUTA se la tabella e' cambiata**»*.
> ### ⛔ **`10`** *«ogni referto stampa **il numero delle leggi**, e un commit che lo
> aumenta deve dichiararlo»*.

### ⭐ **PERCHE' I TRE STANNO IN UN FILE SOLO:** sono ### **la stessa cosa guardata
da tre lati** — ### **l'impronta di cio' che ha girato.** Il timbro la
### **stampa**, il salvataggio la ### **scrive accanto ai dati**, la ripresa la
### **confronta e RIFIUTA.** Tenerli separati vorrebbe dire ### **calcolare l'impronta in
tre posti**, e tre posti ### **divergono.**

### ⛔ **E LA RIPRESA RIFIUTA, non avverte** *(`RIPRESA-ARGV`)*: riprendere con una
tabella diversa ### **continua una corsa che non e' quella** — e il risultato
### **sembra la stessa misura.**

### ⚠ **LA SCRITTURA E' ATOMICA** *(punto `15(e)`)*: temporaneo + rinomina, perche'
### **il PC si riavvia da solo fra `00:00` e `02:00`** e ### **un file a meta' e' peggio
di nessun file.**
"""
import hashlib
import io
import json
import os
import platform
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
for _p in (_QUI, os.path.join(_QUI, "config"), os.path.join(_QUI, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

NL = chr(10)

# ### ⛔ **LA VERSIONE DEL FORMATO DEI DATI** *(punto `15(e)`)*: un file senza la sua
# ### versione ### **non si sa leggere domani.**
VERSIONE_DATI = 1


def _sha(b):
    return hashlib.sha1(b).hexdigest()[:16]


def _sha_file(p):
    return _sha(io.open(p, "rb").read())


def impronta_generati():
    """### L-impronta ### **dei file GENERATI**, in ordine canonico.

    ### ⛔ **Dei GENERATI e non del generatore:** se il generatore cambiasse senza
    cambiare cio- che genera, ### **l-uscita e- la stessa** -- e il timbro deve dire
    ### **che cosa ha girato**, non chi l-ha scritto.
    """
    pezzi = []
    for rel in sorted(["stato.py"]
                      + ["termini/" + f for f in sorted(os.listdir(
                          os.path.join(_QUI, "termini")))
                         if f.endswith(".py") and f != "__init__.py"]
                      + ["osservatori/" + f for f in sorted(os.listdir(
                          os.path.join(_QUI, "osservatori")))
                         if f.endswith(".py") and f != "__init__.py"]):
        pezzi.append("%s=%s" % (rel, _sha_file(os.path.join(_QUI, rel))))
    return _sha((";".join(pezzi)).encode("utf-8")), tuple(pezzi)


def conto_leggi():
    """### `10`: ### **IL NUMERO DELLE LEGGI**, per tipo, ### **dalla TABELLA.**

    ### ⭐ **Dalla tabella e non dai file:** la tabella e- ### **l-unica fonte**, e
    contare i file direbbe ### **quante ne sono state generate**, non ### **quante ce ne
    sono.**
    """
    import yaml
    d = yaml.safe_load(io.open(os.path.join(_QUI, "leggi", "leggi.yaml"),
                               encoding="utf-8").read()) or {}
    per = {}
    for lg in (d.get("leggi") or []):
        per[lg["tipo"]] = per.get(lg["tipo"], 0) + 1
    prova = sum(1 for lg in (d.get("leggi") or []) if lg.get("prova"))
    return {"per_tipo": per, "totale": sum(per.values()), "di_prova": prova,
            "variabili": len(d.get("variabili") or [])}


def timbro(config, impronta_config):
    """### `5`: ### **TUTTO cio- che distingue questa corsa da un-altra.**"""
    gen, pezzi = impronta_generati()
    import determinismo as _DET
    import numpy
    tab = os.path.join(_QUI, "leggi", "leggi.yaml")
    return {
        "versione_dati": VERSIONE_DATI,
        "impronta_tabella": _sha_file(tab),
        "impronta_generati": gen,
        "generati": pezzi,
        "impronta_config": impronta_config,
        "config": dict(config),
        "conto_leggi": conto_leggi(),
        # ### ⚠ **E LE VERSIONI**, perche- ### **i conteggi assoluti dipendono
        # ### dalla piattaforma** -- e- scritto nelle trappole di questo repo.
        "versioni": {"python": sys.version.split()[0], "numpy": numpy.__version__,
                     "piattaforma": platform.platform(),
                     "macchina": platform.machine()},
        # ### ✅ **IL DETERMINISMO, TIMBRATO** *(punto `1` della terza parte)*: le
        # ### cinque variabili dei thread, ### **se sono state fissate IN TEMPO**
        # ### *(prima dell-`import numpy`: dopo non servono a niente)*, le versioni
        # ### ### **confrontate col blocco**, e il conto degli RNG globali.
        # ### ⚠ **E le DIFFERENZE dal blocco stanno QUI e non fanno fermare**, perche-
        # ### ### **una corsa con versioni diverse dal blocco non e- confrontabile AL BIT
        # ### con una che coincide** -- e quello e- il contenuto vero.
        "determinismo": _DET.per_il_timbro(),
    }


def righe_timbro(t):
    """### Il timbro ### **in righe**, per stamparlo in testa a un-uscita."""
    c = t["conto_leggi"]
    L = ["# TIMBRO (versione dati %d)" % t["versione_dati"],
         "#   tabella    %s" % t["impronta_tabella"],
         "#   generati   %s   (%d file)" % (t["impronta_generati"], len(t["generati"])),
         "#   config     %s" % t["impronta_config"],
         "#   LEGGI      %d in tutto, %d DI PROVA, %s   |   %d variabili"
         % (c["totale"], c["di_prova"],
            ", ".join("%s=%d" % kv for kv in sorted(c["per_tipo"].items())),
            c["variabili"]),
         "#   scena      %s, %d nodi, seme %s, dt %s, %d passi, integratore %s"
         % (t["config"]["scena"], t["config"]["nodi"], t["config"]["seme"],
            t["config"]["dt"], t["config"]["passi"], t["config"]["integratore"]),
         "#   attive     %s" % ", ".join(t["config"]["leggi_attive"]),
         "#   versioni   python %s, numpy %s, %s"
         % (t["versioni"]["python"], t["versioni"]["numpy"],
            t["versioni"]["macchina"])]
    return L


# =====================================================================================
#   `6` -- SALVA E RIPRENDI, e la ripresa RIFIUTA
# =====================================================================================

def scrivi_atomico(percorso, byte):
    """### Temporaneo + rinomina: ### **il riavvio notturno non lascia file a meta-.**"""
    tmp = percorso + ".parziale"
    with io.open(tmp, "wb") as f:
        f.write(byte)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, percorso)


def salva(percorso, st, passo, config, impronta_config):
    """### `6`: ### **tutto lo stato + il TIMBRO**, in `npz` + un `json` accanto."""
    import numpy as np
    t = timbro(config, impronta_config)
    t["passo"] = passo
    # ### ⛔ **LO STATO IN `npz`** *(non tracciato: e- un dato pesante)*, e
    # ### ### **il timbro in un `json` accanto** -- che invece si puo- committare.
    import io as _io
    buf = _io.BytesIO()
    np.savez(buf, **{k: v for k, v in st.items()})
    scrivi_atomico(percorso, buf.getvalue())
    scrivi_atomico(percorso + ".timbro.json",
                   (json.dumps(t, sort_keys=True, ensure_ascii=False, indent=1)
                    + NL).encode("utf-8"))
    return t


def riprendi(percorso, config, impronta_config):
    """### `6`: ### **RIFIUTA se la tabella, i generati o la configurazione sono cambiati.**

    ### ⛔ **RIFIUTA e non avverte** *(`RIPRESA-ARGV`)*: riprendere con una tabella
    diversa ### **continua una corsa che non e- quella**, e il risultato
    ### **sembra la stessa misura.**
    """
    import numpy as np
    tp = percorso + ".timbro.json"
    assert os.path.exists(tp), ("### NON C-E- IL TIMBRO accanto a `%s`: uno stato senza "
                               "timbro NON SI PUO- RIPRENDERE, perche- non si sa che "
                               "codice lo ha prodotto" % percorso)
    vecchio = json.load(io.open(tp, encoding="utf-8"))
    nuovo = timbro(config, impronta_config)
    guai = []
    for k in ("versione_dati", "impronta_tabella", "impronta_generati",
              "impronta_config"):
        if vecchio.get(k) != nuovo.get(k):
            guai.append("`%s`: salvato `%s`, ora `%s`"
                        % (k, vecchio.get(k), nuovo.get(k)))
    assert not guai, ("### LA RIPRESA RIFIUTA, e non avverte:" + NL
                      + NL.join("  - " + g for g in guai) + NL
                      + "### Riprendere con una tabella diversa CONTINUA UNA CORSA CHE "
                        "NON E- QUELLA, e il risultato SEMBRA la stessa misura.")
    d = np.load(percorso)
    return {k: d[k] for k in d.files}, vecchio.get("passo", 0)
