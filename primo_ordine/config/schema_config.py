# -*- coding: utf-8 -*-
"""PUNTO `15(a)(c)` — **LA CONFIGURAZIONE: UNA SOLA FONTE, e NESSUN INTERRUTTORE.**

### ⚠ **E IL FILE SI CHIAMA `schema_config.py` E NON `schema.py`, per una ragione
### PRATICA che vale la pena scrivere:** `primo_ordine/leggi/schema.py` esiste gia-, e
### su un `sys.path` piatto ### **due file con lo stesso nome sono LO STESSO MODULO** --
### il secondo `import schema` ### **torna il primo.** ### **E- successo**, e il
### collaudo e- caduto con `module schema has no attribute valida_legge`.

> ### ⛔ **LA RIGA DI COMANDO SCEGLIE SOLO IL FILE.** Nessun'altra via: nessun flag
> che cambi un parametro, nessuna variabile d'ambiente, nessun default nel codice.

### ⭐ **E IL PUNTO `15(c)` E' LA LEZIONE DELL'ERA `1` DETTA NEL MODO PIU' SECCO.**
L'era `1` ha ### **`140` costanti di modulo** che accendono e spengono pezzi di fisica, e
`CONFIG-1` ha misurato che ### **`28` leggi su `31` giravano SPENTE** in sei misure.
### ⛔ **La cura non e' un presidio sui flag: e' TOGLIERE I FLAG** — una legge
e' ### **in tabella e attiva PER ID**, oppure ### **non c'e'.**

| il campo | che cos'e' | e perche' e' OBBLIGATORIO |
|---|---|---|
| `versione` | la versione del ### **formato** | un file senza versione ### **non si sa leggere domani** *(punto `15(e)`)* |
| `scena` | come nasce il grafo | ### **la scena e' un dato**, non un argomento |
| `nodi` | quanti nodi | — |
| `seme` | il seme del `Generator` | ### **esplicito, sempre**: niente RNG globale |
| `dt` | il passo di tempo | — |
| `passi` | quanti passi | — |
| `integratore` | `globale` oppure `locale` | ### **la scelta e' di Luca** *(nodo `INT`)*, e il file la ### **DICHIARA** |
| `iterazioni` e `toll` | i parametri del ### **risolutore** | ### ⚠ **il cono del GLOBALE dipende da `toll`**, misurato: quindi ### **non e' innocuo e sta nel file** |
| `leggi_attive` | ### **gli ID delle leggi** che girano | ### ⛔ **E' IL `15(c)`:** una legge e' qui ### **per ID**, o ### **non gira** |
| `osservatori` | gli ID degli osservatori | — |

### ⛔ **E UN CAMPO IN PIU' E' UN ERRORE, non una comodita':** il vocabolario e'
### **CHIUSO**, perche' un campo che nessuno legge e' ### **una manopola che qualcuno
leggera'.**
"""
import io
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(os.path.dirname(_QUI))

NL = chr(10)
VERSIONE = 1

# ### ⛔ **IL VOCABOLARIO CHIUSO DEI CAMPI.** Tutti ### **obbligatori**: il punto
# ### `15(b)` dice che ### **un parametro non presente e- un ERRORE**, quindi
# ### ### **non esiste un campo facoltativo.**
# ### ✅ **`confronto` E- ENTRATO IL `2026-10-10`, per la decisione di Luca sul
# ### nodo `INT`:** l-integratore e- ### **il LOCALE a strati**, e il GLOBALE resta nel
# ### codice ### **SOLO come termine di confronto dei collaudi.**
# ### ⛔ **Quindi una configurazione che chiede `globale` DEVE dichiarare
# ### `confronto: true`**, e senza quella dichiarazione ### **viene RIFIUTATA**: cosi-
# ### ### **nessuna corsa di FISICA puo- girare col globale per distrazione.**
# ### ⭐ **E- un CAMPO e non un giudizio** (par. 9): la differenza fra una corsa di
# ### fisica e un confronto ### **la dice il file**, non chi legge.
CAMPI = ("versione", "scena", "nodi", "seme", "dt", "passi", "integratore",
         "iterazioni", "toll", "leggi_attive", "osservatori", "confronto")

SCENE = ("catena", "anello")
INTEGRATORI = ("globale", "locale")

_ID = re.compile(r"^[A-Z][A-Z0-9-]{3,}$")


def _err(f, che):
    f.append(che)


def valida(d, leggi_in_tabella=None, osservatori_in_tabella=None):
    """### Gli errori di una configurazione, o `[]`. ### **Pura: non legge il disco.**"""
    f = []
    if not isinstance(d, dict):
        return ["la configurazione non e- una mappa"]
    manca = sorted(set(CAMPI) - set(d))
    if manca:
        _err(f, "mancano i campi %s. ### Il punto `15(b)`: un parametro NON PRESENTE e- "
                "un ERRORE, non un default" % manca)
    extra = sorted(set(d) - set(CAMPI))
    if extra:
        _err(f, "campi NON previsti %s: il vocabolario e- CHIUSO. ### Un campo che "
                "nessuno legge e- una manopola che qualcuno leggera-" % extra)
    if d.get("versione") != VERSIONE:
        _err(f, "`versione` %r: questo schema legge la `%d`. ### Un file senza la sua "
                "versione non si sa leggere domani" % (d.get("versione"), VERSIONE))
    if d.get("scena") not in SCENE:
        _err(f, "`scena` %r fuori vocabolario: %s" % (d.get("scena"), list(SCENE)))
    # ### ⛔ **IL GLOBALE SOLO COME CONFRONTO** -- decisione di Luca, 2026-10-10,
    # ### nodo `INT`. ### **La ragione e- MISURATA, non di gusto:** il cono del LOCALE e-
    # ### ### **esatto**, quello del GLOBALE ### **dipende dalla tolleranza** -- cioe-
    # ### ### **non e- una causalita-** -- e sulla reversibilita- ### **i due sono
    # ### UGUALI** *(b99bb4c: entrambi tornano a `4e-16`)*. ### ✅ **Quindi il
    # ### discrimine non e- la precisione: e- la CAUSALITA-.**
    if d.get("integratore") == "globale" and not d.get("confronto"):
        _err(f, "`integratore: globale` SENZA `confronto: true`. ### Decisione di Luca "
                "del 2026-10-10 (nodo `INT`): l-integratore e- il LOCALE a strati, e il "
                "GLOBALE resta SOLO come termine di confronto dei collaudi -- il suo "
                "cono DIPENDE DALLA TOLLERANZA, cioe- NON E- UNA CAUSALITA-. ### Una "
                "corsa di FISICA non lo puo- scegliere, e un confronto lo DICHIARA")
    if d.get("confronto") is not None and not isinstance(d.get("confronto"), bool):
        _err(f, "`confronto` deve essere un booleano: e- un CAMPO, non una frase")
    if d.get("integratore") not in INTEGRATORI:
        _err(f, "`integratore` %r fuori vocabolario: %s. ### La scelta e- di Luca (nodo "
                "`INT`), e il file la DICHIARA" % (d.get("integratore"),
                                                   list(INTEGRATORI)))
    for k, minimo in (("nodi", 2), ("passi", 1), ("iterazioni", 1)):
        v = d.get(k)
        if not isinstance(v, int) or isinstance(v, bool) or v < minimo:
            _err(f, "`%s` %r: serve un intero >= %d" % (k, v, minimo))
    if not isinstance(d.get("seme"), int) or isinstance(d.get("seme"), bool):
        _err(f, "`seme` %r: serve un intero. ### ESPLICITO, sempre: niente RNG globale"
             % d.get("seme"))
    for k in ("dt", "toll"):
        v = d.get(k)
        if not isinstance(v, (int, float)) or isinstance(v, bool) or not v > 0:
            _err(f, "`%s` %r: serve un numero > 0" % (k, v))
    for k in ("leggi_attive", "osservatori"):
        v = d.get(k)
        if not isinstance(v, list):
            _err(f, "`%s` deve essere una lista di ID (anche vuota, e allora lo dice)" % k)
            continue
        for x in v:
            if not isinstance(x, str) or not _ID.match(x):
                _err(f, "`%s` contiene %r, che non ha la forma di un ID" % (k, x))
        if len(set(v)) != len(v):
            _err(f, "`%s` ha un ID DOPPIO: %s" % (k, sorted({x for x in v
                                                             if v.count(x) > 1})))
    # ------------------------------------------------------------------ `15(c)`
    # ### ⛔ **UNA LEGGE E- ATTIVA PER ID, E L-ID DEVE ESISTERE IN TABELLA.**
    # ### Senza questo, `leggi_attive` sarebbe ### **una lista di stringhe** -- cioe-
    # ### un flag con un altro nome.
    if leggi_in_tabella is not None and isinstance(d.get("leggi_attive"), list):
        for x in d["leggi_attive"]:
            if x not in leggi_in_tabella:
                _err(f, "`leggi_attive` nomina `%s`, che NON E- IN `leggi.yaml`. "
                        "### Una legge e- in tabella e attiva per ID, oppure NON C-E-"
                        % x)
    if osservatori_in_tabella is not None and isinstance(d.get("osservatori"), list):
        for x in d["osservatori"]:
            if x not in osservatori_in_tabella:
                _err(f, "`osservatori` nomina `%s`, che NON E- un osservatore di "
                        "`leggi.yaml`" % x)
    return f


def carica(percorso, leggi=None, osservatori=None):
    """### Legge, VALIDA e torna la configurazione. ### **Se non passa, SOLLEVA.**"""
    import yaml
    d = yaml.safe_load(io.open(percorso, encoding="utf-8").read()) or {}
    err = valida(d, leggi, osservatori)
    assert not err, ("### LA CONFIGURAZIONE `%s` NON PASSA LO SCHEMA:" % percorso
                     + NL + NL.join("  - " + e for e in err))
    return d


def impronta(d):
    """### L-### **IMPRONTA** della configurazione *(punti `5` e `6`)*."""
    import hashlib
    import json
    return hashlib.sha1(json.dumps(d, sort_keys=True, ensure_ascii=False)
                        .encode("utf-8")).hexdigest()[:16]


# =====================================================================================
#   IL COLLAUDO -- nei due versi, su mappe costruite IN MEMORIA
# =====================================================================================

def collaudo():
    sys.path.insert(0, os.path.join(RADICE, "csv"))
    import _presidio
    _presidio.avvia(__file__)
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-64s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    BUONA = {"versione": 1, "scena": "catena", "nodi": 9, "seme": 11, "dt": 0.01,
             "passi": 200, "integratore": "locale", "iterazioni": 64, "toll": 1e-14,
             "leggi_attive": ["PROVA-HOPPING", "PROVA-LOCALE"],
             "osservatori": ["PROVA-NORMA"], "confronto": False}
    LG = {"PROVA-HOPPING", "PROVA-LOCALE"}
    OS_ = {"PROVA-NORMA"}
    print("=" * 100)
    print("IL COLLAUDO DELLO SCHEMA DELLA CONFIGURAZIONE -- nei DUE VERSI")
    print("=" * 100)
    esito("NON deve scattare: una configurazione BUONA",
          valida(BUONA, LG, OS_) == [], "%d campi" % len(CAMPI))
    for k in CAMPI:
        d = {x: v for x, v in BUONA.items() if x != k}
        esito("### DEVE scattare: MANCA il campo `%s`" % k,
              any("mancano i campi" in e for e in valida(d, LG, OS_)),
              "### un parametro NON PRESENTE e- un ERRORE (`15(b)`)" if k == "dt" else "")
    esito("### DEVE scattare: un campo IN PIU-",
          any("vocabolario e- CHIUSO" in e
              for e in valida(dict(BUONA, inventato=1), LG, OS_)),
          "### un campo che nessuno legge e- una manopola che qualcuno leggera-")
    esito("### DEVE scattare: la `versione` sbagliata",
          any("versione" in e for e in valida(dict(BUONA, versione=99), LG, OS_)))
    esito("### DEVE scattare: una `scena` fuori vocabolario",
          any("scena" in e for e in valida(dict(BUONA, scena="spirale"), LG, OS_)))
    # ### ⛔ **IL GLOBALE SOLO COME CONFRONTO -- decisione di Luca del 2026-10-10.**
    esito("### DEVE scattare: `integratore: globale` SENZA `confronto: true`",
          any("SOLO come termine di confronto" in e
              for e in valida(dict(BUONA, integratore="globale"), LG, OS_)),
          "### il suo cono DIPENDE DALLA TOLLERANZA: non e- una causalita-")
    esito("NON deve scattare: `globale` CON `confronto: true` dichiarato",
          valida(dict(BUONA, integratore="globale", confronto=True), LG, OS_) == [],
          "### un confronto e- legittimo, e si DICHIARA")
    esito("### DEVE scattare: `confronto` che non e- un booleano",
          any("deve essere un booleano" in e
              for e in valida(dict(BUONA, confronto="si"), LG, OS_)),
          "### e- un CAMPO, non una frase")
    esito("### DEVE scattare: un `integratore` fuori vocabolario",
          any("integratore" in e for e in valida(dict(BUONA, integratore="rk4"), LG, OS_)),
          "### la scelta e- di Luca, e il file la DICHIARA")
    esito("### DEVE scattare: un `seme` che non e- un intero",
          any("seme" in e for e in valida(dict(BUONA, seme="undici"), LG, OS_)),
          "ESPLICITO, sempre: niente RNG globale")
    esito("### DEVE scattare: un `dt` <= 0",
          any("dt" in e for e in valida(dict(BUONA, dt=0.0), LG, OS_)))
    esito("### DEVE scattare: una legge attiva CHE NON E- IN TABELLA",
          any("NON C-E-" in e
              for e in valida(dict(BUONA, leggi_attive=["LEGGE-INVENTATA"]), LG, OS_)),
          "### `15(c)`: una legge e- in tabella e attiva per ID, oppure NON C-E-")
    esito("### DEVE scattare: un ID DOPPIO in `leggi_attive`",
          any("DOPPIO" in e
              for e in valida(dict(BUONA,
                                   leggi_attive=["PROVA-LOCALE", "PROVA-LOCALE"]),
                              LG, OS_)))
    esito("### DEVE scattare: un `leggi_attive` che non e- una lista",
          any("lista di ID" in e
              for e in valida(dict(BUONA, leggi_attive="PROVA-LOCALE"), LG, OS_)),
          "### una stringa che SEMBRA un ID e- il flag con un altro nome")
    esito("NON deve scattare: `leggi_attive` VUOTA, che e- una scelta DICHIARATA",
          valida(dict(BUONA, leggi_attive=[]), LG, OS_) == [],
          "### zero leggi e- un caso LEGITTIMO (il vuoto), e lo dice")
    # ### l-IMPRONTA: due mappe uguali danno la stessa, due diverse NO.
    esito("l-IMPRONTA e- STABILE sull-ordine delle chiavi",
          impronta(BUONA) == impronta(dict(reversed(list(BUONA.items())))),
          "`sort_keys=True`: ### l-ordine in cui si scrive un yaml NON e- un dato")
    esito("### e CAMBIA se cambia un valore",
          impronta(BUONA) != impronta(dict(BUONA, seme=12)),
          "### altrimenti il timbro del punto `5` non direbbe niente")
    print("=" * 100)
    print("IL COLLAUDO DELLA CONFIGURAZIONE: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(collaudo())
