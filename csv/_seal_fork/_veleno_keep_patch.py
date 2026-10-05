# -*- coding: utf-8 -*-
r"""LA PATCH DELLA CURA DI `VELENO-ARCHI-KEEP`, via (i).

*(Decisione di Luca del 2026-10-05. Task history:
`doc/TASK_HISTORY/2026-10-05_veleno-archi-keep-cura.md`.)*

### CHE COSA FA: su una COPIA del simulatore, inserisce
`_riallinea_derivate_arco` e la sua chiamata **immediatamente prima** del veleno.
### **Il veleno resta dov e: la cura sta PRIMA di lui.**

### A CHE SERVE, ed e il braccio 0 del sigillo: applicata al blob **0f060670**
deve riprodurre **e2940b3c** AL BYTE. ### **Cosi il punto di partenza non e
asserito: e verificabile.**

### LE DUE SOSTITUZIONI SI ASSERISCONO PER SE, e FALLISCONO se l ancora non e
### unica (`P1-quater`).

USO:
    python csv/_seal_fork/_veleno_keep_patch.py --file=<copia>

# ESENTE-H-P3: non importa il simulatore e non lo fa girare. Scrive un file.
"""
import hashlib
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
# ### IL BLOB ATTESO DOPO LA PATCH, cioe il braccio 0 scritto come NUMERO.
BLOB_PRIMA = "0f060670"
BLOB_DOPO = "e2940b3c"

# ### I DUE BLOCCHI, estratti dal sorgente curato e NON ritrascritti a mano.
ANCORA_FUN = 'def _avvelena_derivate(net):'
BLOCCO_FUN = 'def _riallinea_derivate_arco(net, evento, c):\n    """### `keep` SI APPLICA ANCHE ALLE DERIVATE D ARCO, e non solo alle colonne.\n\n    *(`VELENO-ARCHI-KEEP`, cura del 2026-10-05. **VIA (i), DECISIONE DI LUCA**: la\n    nascita applica `keep` a TUTTE le derivate d arco PRIMA del veleno. La via (ii)\n    -- far ricalcolare `dt_e` a chi lo legge -- e\' SCARTATA: curava **un lettore\n    solo**, lasciava `_sin2_vir` col difetto, e aggiungeva **una seconda scrittura**\n    della legge di `dt_e`.)*\n\n    ### IL DIFETTO CHE CURA, MISURATO (passo (1), `doc/REFERTO_veleno_archi_keep_2026-10-05.md`)\n    La nascita ricostruisce le colonne d arco con `concat(x[keep], ...)`: **toglie**\n    archi e ne **aggiunge** in coda. `_avvelena_derivate` allungava **solo in coda**\n    con `NaN`, e ### **non applicava `keep`**. Quindi dal primo arco tolto in poi\n    ### **ogni arco leggeva il valore di UN ALTRO arco** -- un valore **FINITO**, che\n    il veleno non segnala.\n\n    ### IL CONTO, e il numero misurato\n    Con `s` archi divisi: tolti `s`, aggiunti `2s`, quindi il veleno appendeva\n    `(m+s) - m = s` celle su `2s` archi nuovi -- ### **copertura `0.5000`, misurata\n    `min = max` su 166 confronti.** Negli eventi **Schwinger**, che non hanno `keep`,\n    la copertura era ### **`1.0000`** -- e l unica differenza fra i due casi era `keep`.\n    ### ➜ Dopo questa cura `len(v) = sum(keep) = m - s`, quindi il veleno appende\n    `(m+s) - (m-s) = 2s` celle: ### **copertura `1.0000` in ENTRAMBI i casi.**\n    ### **La cura non aggiunge un comportamento: estende al caso che gli sfuggiva\n    quello che il veleno faceva GIA\' nell altro.**\n\n    ### PERCHE\' QUI E NON DENTRO IL VELENO\n    Il veleno sta **dopo le regole** perche\' deve conoscere le lunghezze NUOVE, e il\n    suo commento lo dichiara. ### **Il riallineamento invece vuole la lunghezza\n    VECCHIA**, che e\' `len(keep)`: sono due istanti diversi, e metterli nella stessa\n    funzione vorrebbe dire darle due bersagli. ### **Restano due funzioni, in fila.**\n\n    ### NESSUN FLAG, ED E\' LA STESSA SCELTA DEL VELENO\n    *<<Il veleno agisce sempre>>*: un flag renderebbe un **presidio** un **opzione**,\n    ed e\' il difetto che `E4-LAM` ha curato. ### **Questa e\' la riparazione di un\n    difetto, non un esperimento: agisce sempre.**\n\n    ### E SE LA LUNGHEZZA NON TORNA, NON SI INDOVINA\n    Una derivata d arco **deve** avere la lunghezza degli archi di **PRIMA** della\n    nascita, cioe\' `len(keep)`. ### **Se non l ha, si ferma il run con\n    `_ferma_registro`** -- le stesse eccezioni delle guardie esistenti.\n    ### **Allungare o troncare qui sarebbe IL RIPIEGO che quel controllo esiste per\n    impedire** (`RIPIEGHI-ZERO`, `A9`).\n    """\n    keep = None if c is None else c.get("keep")\n    if keep is None:\n        # ### L EVENTO NON TOGLIE ARCHI (e\' lo Schwinger: `concat(net.i, aa, k)`).\n        #   Niente da riallineare, e il veleno gia\' copriva tutto: misurato `1.0000`.\n        net._g_keep_senza = getattr(net, "_g_keep_senza", 0) + 1\n        return\n    keep = np.asarray(keep)\n    if keep.dtype != bool:\n        keep = keep.astype(bool)\n    tenuti = np.flatnonzero(keep)\n    for nome, dove, classe, _motivo in REGISTRO_DERIVATE:\n        if dove != "arco" or classe != "avvelena":\n            continue\n        v = getattr(net, nome, None)\n        if v is None:\n            # ### non esiste ANCORA: per lei il difetto non c e\' ancora, e si conta.\n            net._g_keep_assenti = getattr(net, "_g_keep_assenti", 0) + 1\n            continue\n        v = np.asarray(v)\n        if v.ndim != 1 or v.dtype.kind != "f":\n            # ### LE STESSE DUE GUARDIE DEL VELENO, e per la stessa ragione: non si\n            #   riallinea cio\' che il veleno non sa avvelenare. Se una diventasse\n            #   multiasse o intera, questo contatore salirebbe invece di far passare\n            #   la cosa in silenzio (`A8`).\n            net._g_keep_salti = getattr(net, "_g_keep_salti", 0) + 1\n            continue\n        if len(v) != len(keep):\n            # ### NON SI INDOVINA: `_ferma_registro`, come le guardie esistenti.\n            _ferma_registro(CacheCorta if len(v) < len(keep) else CacheLunga,\n                             "CORTA" if len(v) < len(keep) else "LUNGA",\n                             # ### `_scrivi_forma` ITERA l argomento: gli si passa la\n                             #   FORMA, non l array -- altrimenti il messaggio\n                             #   stamperebbe i VALORI. Una guardia che stampa\n                             #   spazzatura e una guardia a meta.\n                             nome, (len(keep),), v.shape,\n                             "_riallinea_derivate_arco, evento `%s`" % evento)\n        setattr(net, nome, v[tenuti])\n        net._g_keep_riallineate = getattr(net, "_g_keep_riallineate", 0) + 1\n        net._g_keep_celle_tolte = (getattr(net, "_g_keep_celle_tolte", 0)\n                                   + int(len(v) - len(tenuti)))\n\n\n'
ANCORA_CALL = '    _avvelena_derivate(net)\n'
BLOCCO_CALL = '    # ### [VELENO-ARCHI-KEEP, cura del 2026-10-05, VIA (i), DECISIONE DI LUCA]\n    #   `keep` SI APPLICA ANCHE ALLE DERIVATE D ARCO, e PRIMA del veleno.\n    #   ### PERCHE PRIMA: il veleno allunga fino alla lunghezza NUOVA; il\n    #   riallineamento vuole quella VECCHIA (`len(keep)`). Sono due istanti, e\n    #   l ordine fra loro E la cura: riallinea, POI avvelena il resto.\n    #   ### IL DIFETTO MISURATO (passo (1)): senza questo, dal primo arco tolto\n    #   in poi ogni arco leggeva il valore di UN ALTRO arco -- un valore FINITO,\n    #   che il veleno non segnala -- e la copertura del veleno era `0.5000` nelle\n    #   divisioni contro `1.0000` negli Schwinger, con `keep` come UNICA\n    #   differenza. Misurato `min = max` su 166 confronti.\n    _riallinea_derivate_arco(net, evento, c)\n    _avvelena_derivate(net)\n'


def applica(testo):
    """Le due sostituzioni, ciascuna asserita UNICA."""
    for a in (ANCORA_FUN, ANCORA_CALL):
        n = testo.count(a)
        if n != 1:
            raise SystemExit("[FERMO] l ancora compare %d volte, non 1: %r"
                             % (n, a[:60]))
    testo = testo.replace(ANCORA_FUN, BLOCCO_FUN + ANCORA_FUN, 1)
    testo = testo.replace(ANCORA_CALL, BLOCCO_CALL, 1)
    return testo


def principale(dest):
    t = io.open(dest, encoding="utf-8").read()
    b = hashlib.sha1(t.encode("utf-8")).hexdigest()[:8]
    print("  file: %s   blob PRIMA: %s" % (os.path.basename(dest), b))
    if b != BLOB_PRIMA:
        print("  ### ATTENZIONE: il blob di partenza non e %s. La patch si applica"
              % BLOB_PRIMA)
        print("      comunque, ma il braccio 0 NON potra valere.")
    t = applica(t)
    io.open(dest, "w", encoding="utf-8", newline=NL).write(t)
    b2 = hashlib.sha1(io.open(dest, "rb").read()).hexdigest()[:8]
    print("  blob DOPO: %s   atteso %s   %s"
          % (b2, BLOB_DOPO, "COINCIDE" if b2 == BLOB_DOPO else "### NON COINCIDE"))
    return 0 if b2 == BLOB_DOPO else 1


if __name__ == "__main__":
    _d = None
    for _a in sys.argv[1:]:
        if _a.startswith("--file="):
            _d = _a.split("=", 1)[1]
    if _d is None:
        raise SystemExit("[FERMO] serve --file=<copia>")
    sys.exit(principale(_d))
