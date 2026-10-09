# -*- coding: utf-8 -*-
"""PUNTO `15(d)(e)` — **I CONFRONTI COL CAMPO UNICO, e i DATI col loro formato.**

> ### ⛔ **`15(d)`:** *«un `A`/`B` dichiara **il campo UNICO** in cui i bracci
> differiscono, e un controllo verifica che le due configurazioni differiscano **SOLO
> li'** (la lezione di `Z20`). Altrimenti **il confronto non parte**»*.
> ### ⛔ **`15(e)`:** *«ogni file porta **la versione del formato**; la scrittura e'
> **ATOMICA**; i pesanti **restano locali con impronta, percorso e comando**; **un reperto
> non si modifica**»*.

### ⭐ **LA LEZIONE DI `Z20`, detta come la ricordo:** due bracci di un confronto
### **differivano in piu' di un posto**, e il risultato ### **non diceva quale
differenza lo avesse prodotto.** ### ⛔ **Un confronto con due variabili non e' un
confronto: e' due misure sovrapposte.**

### ⚠ **E IL CONTROLLO NON AVVERTE: IL CONFRONTO NON PARTE.** Avvertire vorrebbe
dire ### **lasciar girare una misura che non si sapra' leggere** — e una corsa
lunga ### **non si rifa' per una diagnosi.**
"""
import hashlib
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
for _p in (os.path.join(RADICE, "primo_ordine"),
           os.path.join(RADICE, "primo_ordine", "config")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

NL = chr(10)
PRESIDIO = "P-AB"

CONF = os.path.join(RADICE, "primo_ordine", "config")


def _sha(b):
    return hashlib.sha1(b).hexdigest()[:16]


# =====================================================================================
#   `15(d)` -- IL CONFRONTO `A`/`B`
# =====================================================================================

def differenze(a, b):
    """### I campi in cui due configurazioni ### **differiscono.**"""
    return sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))


def valida_confronto(a, b, campo):
    """### Gli errori di un `A`/`B`, o `[]`. ### **Il confronto non parte, se ce ne sono.**

    ### ⛔ **UN SOLO campo, e DEVE essere quello dichiarato.** Non <<almeno
    quello>>, non <<quello e poco altro>>: ### **ESATTAMENTE quello** -- altrimenti
    ### **il risultato non dice quale differenza lo ha prodotto.**
    """
    err = []
    import schema_config as CFG
    for nome, c in (("A", a), ("B", b)):
        e = CFG.valida(c)
        if e:
            err.append("`P-AB` il braccio `%s` NON passa lo schema: %s" % (nome, e[0]))
    if err:
        return err
    d = differenze(a, b)
    if campo not in set(a) | set(b):
        err.append("`P-AB`: il campo dichiarato `%s` NON E- un campo della "
                   "configurazione" % campo)
    if d == [campo]:
        return err
    if not d:
        err.append("`P-AB`: i due bracci sono IDENTICI. ### Un confronto fra due cose "
                   "uguali non misura niente, e il campo `%s` dichiarato non differisce"
                   % campo)
        return err
    if campo not in d:
        err.append("`P-AB`: il campo dichiarato `%s` NON DIFFERISCE, e differiscono %s. "
                   "### Il confronto misurerebbe una cosa diversa da quella dichiarata"
                   % (campo, d))
    extra = [x for x in d if x != campo]
    if extra:
        err.append("`P-AB`: i bracci differiscono ANCHE in %s, oltre al campo dichiarato "
                   "`%s`. ### E- la lezione di `Z20`: un confronto con DUE variabili non "
                   "e- un confronto, e- DUE MISURE SOVRAPPOSTE -- e il risultato non dice "
                   "quale differenza lo ha prodotto. ### IL CONFRONTO NON PARTE"
                   % (extra, campo))
    return err


def confronto(file_a, file_b, campo):
    """### Fa partire un `A`/`B` ### **solo se e- un confronto.**"""
    import schema_config as CFG
    a = CFG.carica(file_a)
    b = CFG.carica(file_b)
    err = valida_confronto(a, b, campo)
    assert not err, ("### IL CONFRONTO NON PARTE:" + NL
                     + NL.join("  - " + e for e in err))
    return a, b, {"campo": campo, "A": CFG.impronta(a), "B": CFG.impronta(b)}


# =====================================================================================
#   `15(e)` -- I DATI: versione, scrittura atomica, reperti immutabili
# =====================================================================================

def dati_con_timbro():
    """### I dati di `db_era2/`, ### **ciascuno col suo timbro accanto.**"""
    d = os.path.join(RADICE, "db_era2")
    if not os.path.isdir(d):
        return []
    fuori = []
    for f in sorted(os.listdir(d)):
        if f.endswith(".timbro.json") or f.endswith(".parziale"):
            continue
        fuori.append((f, os.path.exists(os.path.join(d, f + ".timbro.json"))))
    return fuori


def controlla():
    err = []
    # ------------------------------------------------------------------ `15(e)`
    d = os.path.join(RADICE, "db_era2")
    for f, ha in dati_con_timbro():
        if not ha:
            err.append("`P-AB` `db_era2/%s`: NON HA IL TIMBRO accanto. ### Un dato senza "
                       "timbro non si sa da dove viene, e ### non si puo- riprendere" % f)
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f.endswith(".parziale"):
                err.append("`P-AB` `db_era2/%s`: E- UN FILE A META-. ### La scrittura e- "
                           "ATOMICA (temporaneo + rinomina): un `.parziale` che resta "
                           "vuol dire che ### il processo e- morto in mezzo -- e il PC si "
                           "riavvia da solo fra `00:00` e `02:00`" % f)
            if f.endswith(".timbro.json"):
                t = json.load(io.open(os.path.join(d, f), encoding="utf-8"))
                if "versione_dati" not in t:
                    err.append("`P-AB` `db_era2/%s`: il timbro NON PORTA "
                               "`versione_dati`. ### Un file senza la versione del "
                               "formato NON SI SA LEGGERE DOMANI" % f)
                for k in ("impronta_tabella", "impronta_generati", "impronta_config"):
                    if not t.get(k):
                        err.append("`P-AB` `db_era2/%s`: il timbro non porta `%s`"
                                   % (f, k))
    # ------------------------------------------------------------------ le configurazioni
    n = 0
    for f in sorted(os.listdir(CONF)):
        if not f.endswith(".yaml"):
            continue
        n += 1
        import schema_config as CFG
        try:
            CFG.carica(os.path.join(CONF, f))
        except AssertionError as e:
            err.append("`P-AB` `config/%s`: NON passa lo schema: %s"
                       % (f, str(e).split(NL)[1].strip() if NL in str(e) else str(e)))
    if n == 0:
        err.append("`P-AB`: NESSUNA configurazione in `primo_ordine/config/`")
    return err


# =====================================================================================
#   IL COLLAUDO -- NEI DUE VERSI
# =====================================================================================

def collaudo():
    import schema_config as CFG
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-64s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL COLLAUDO DI `P-AB` -- nei DUE VERSI")
    print("=" * 100)
    esito("sul disco: `P-AB` TACE", controlla() == [],
          "%d dati con timbro, %d configurazioni"
          % (len(dati_con_timbro()),
             len([1 for f in os.listdir(CONF) if f.endswith(".yaml")])))
    a = CFG.carica(os.path.join(CONF, "prova.yaml"))
    # ------------------------------------------------------------------ `15(d)`
    b = dict(a, seme=99)
    esito("`15(d)` un `A`/`B` con UN SOLO campo diverso PARTE",
          valida_confronto(a, b, "seme") == [],
          "### e- un confronto: il risultato dice QUALE differenza lo ha prodotto")
    esito("### il braccio sopra HA MATERIA (i bracci DIFFERISCONO)",
          differenze(a, b) == ["seme"], "`seme`: 11 contro 99")
    b2 = dict(a, seme=99, dt=0.02)
    esito("### DEVE scattare: i bracci differiscono in DUE campi",
          any("DUE MISURE SOVRAPPOSTE" in e for e in valida_confronto(a, b2, "seme")),
          "### la lezione di `Z20`, e ### IL CONFRONTO NON PARTE")
    esito("### DEVE scattare: il campo DICHIARATO non differisce",
          any("NON DIFFERISCE" in e for e in valida_confronto(a, dict(a, dt=0.02),
                                                              "seme")),
          "### il confronto misurerebbe una cosa DIVERSA da quella dichiarata")
    esito("### DEVE scattare: i due bracci sono IDENTICI",
          any("IDENTICI" in e for e in valida_confronto(a, dict(a), "seme")),
          "### un confronto fra due cose uguali non misura niente")
    esito("### DEVE scattare: un campo dichiarato che NON ESISTE",
          any("NON E- un campo" in e
              for e in valida_confronto(a, dict(a, seme=99), "inventato")))
    esito("### DEVE scattare: un braccio che NON passa lo schema",
          any("NON passa lo schema" in e
              for e in valida_confronto(a, dict(a, seme="undici"), "seme")),
          "### un braccio mal formato non e- un braccio")
    # ------------------------------------------------------------------ `15(e)`
    d = os.path.join(RADICE, "db_era2")
    n_dati = len(dati_con_timbro())
    esito("`15(e)` ogni dato ha IL TIMBRO accanto", all(h for _f, h in dati_con_timbro()),
          "%d dati: ### un dato senza timbro non si sa da dove viene" % n_dati)
    esito("### e il braccio sopra HA MATERIA (c-e- almeno un dato)", n_dati >= 1,
          "%d: se fosse 0 il braccio sarebbe un FALSO-UNO" % n_dati)
    if os.path.isdir(d):
        pz = os.path.join(d, "_finto.npz.parziale")
        try:
            io.open(pz, "wb").write(b"x")
            esito("### DEVE scattare: un file `.parziale` che resta",
                  any("FILE A META-" in e for e in controlla()),
                  "### la scrittura e- ATOMICA: un `.parziale` vuol dire processo morto "
                  "in mezzo")
        finally:
            if os.path.exists(pz):
                os.remove(pz)
        tp = [f for f in os.listdir(d) if f.endswith(".timbro.json")]
        if tp:
            p = os.path.join(d, tp[0])
            salva = io.open(p, "rb").read()
            try:
                t = json.load(io.open(p, encoding="utf-8"))
                del t["versione_dati"]
                io.open(p, "w", encoding="utf-8", newline=NL).write(
                    json.dumps(t, ensure_ascii=False) + NL)
                esito("### DEVE scattare: un timbro SENZA `versione_dati`",
                      any("versione_dati" in e for e in controlla()),
                      "### un file senza la versione del formato NON SI SA LEGGERE "
                      "DOMANI")
            finally:
                io.open(p, "wb").write(salva)
    esito("NON deve scattare: rimesso tutto a posto, `P-AB` TACE", controlla() == [],
          "### i bracci di sopra scattavano per i loro casi finti")
    print("=" * 100)
    print("IL COLLAUDO DI `P-AB`: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--collaudo" in argv:
        return collaudo()
    err = controlla()
    print("  `P-AB`: %d dati con timbro, %d configurazioni"
          % (len(dati_con_timbro()),
             len([1 for f in os.listdir(CONF) if f.endswith(".yaml")])))
    for e in err[:14]:
        print("  ### %s" % e)
    print("  ### %d errori" % len(err))
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
