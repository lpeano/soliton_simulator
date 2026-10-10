# -*- coding: utf-8 -*-
"""BLOCCO `1` — **UN ID CREATO DA OGGI NON PUO' COLLIDERE, e ha almeno `4` caratteri.**

> ### ⛔ **La decisione di Luca:** *«gli `11` OMONIMI restano **omonimi dichiarati**,
> non si sceglie un significato … **Piu' un PRESIDIO NUOVO, ERRORE:** un ID creato da
> oggi **non puo' coincidere** con un ID, un alias o un omonimo esistente, e **deve avere
> almeno `4` caratteri.** Collaudo nei due versi»*.

### ⭐ **PERCHE' I TRE INSIEME, e non solo <<non coincide con un ID>>:**

| | che cosa impedisce | e il difetto che lo ha insegnato |
|---|---|---|
| **un `id` esistente** | due voci con lo stesso nome | ### **e' la collisione che l'indice esiste per curare** — ed e' successo: `A3` era ### **tre cose** |
| **un `alias`** | un nome nuovo che ### **un vecchio nome gia' risolve** | un alias e' ### **una promessa di risoluzione**: se un ID nuovo lo prende, ### **la promessa si rompe** |
| **un `omonimo`** | un nome nuovo uguale a uno dei ### **significati dichiarati** di un omonimo | gli `11` omonimi ### **restano omonimi**, e il loro metadato ### **RESTA**: un ID nuovo che ne prende un significato ### **ne cancella la dichiarazione** |
| **meno di `4` caratteri** | `D1`, `E2`, `T1`… | ### **i nomi corti sono quelli che hanno collisionato**: `11` omonimi su `11` hanno un nome di `2` o `3` caratteri |

### ⚠ **E <<DA OGGI>> E' LA PAROLA CHE CONTA:** gli ID corti ### **esistenti restano**
*(sono `953` ID conservati, e `10` alias hanno meno di `4` caratteri)*.
### ⛔ **Il presidio guarda CHI NASCE**, non chi c'e' — perche' rinominare gli
esistenti ### **perderebbe degli ID**, e ### **un ID non si perde.**
"""
import io
import json
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)

NL = chr(10)
PRESIDIO = "P-ID"

MIN_CARATTERI = 4

# ### ⛔ **L-ID dentro un significato di omonimo si cita fra backtick**, e cosi- si
# ### ### **riconosce senza leggere la prosa** *(il principio del mandato precedente)*.
_BT = re.compile(r"`([A-Z][A-Za-z0-9:_-]{1,})`")


def _jsonl(p):
    if not os.path.exists(p):
        return []
    return [json.loads(r) for r in io.open(p, encoding="utf-8").read().split(NL)
            if r.strip()]


def presi(voci=None, etich=None):
    """### `(id, alias, omonimi)`: ### **tutti i nomi GIA- PRESI.**"""
    D = os.path.join(RADICE, "doc", "indice")
    voci = _jsonl(os.path.join(D, "voci.jsonl")) if voci is None else voci
    etich = _jsonl(os.path.join(D, "etichette_rimosse.jsonl")) if etich is None else etich
    ids = {v["id"] for v in voci} | {e["id"] for e in etich}
    al = set()
    om = set()
    for v in voci:
        al |= set(v.get("alias") or [])
        for s in ((v.get("meta") or {}).get("omonimo") or []):
            om |= set(_BT.findall(str(s)))
    return ids, al, om


def controlla_nuovo(idv, voci=None, etich=None):
    """### Gli errori di ### **UN ID che nasce**, o `[]`."""
    err = []
    ids, al, om = presi(voci, etich)
    if len(idv) < MIN_CARATTERI:
        err.append("`P-ID` `%s`: ha %d caratteri, e il minimo e- %d. ### I nomi CORTI "
                   "sono quelli che hanno collisionato: gli 11 omonimi hanno TUTTI un "
                   "nome di 2 o 3 caratteri" % (idv, len(idv), MIN_CARATTERI))
    if idv in ids:
        err.append("`P-ID` `%s`: ESISTE GIA- come ID. ### Due voci con lo stesso nome "
                   "sono la collisione che l-indice esiste per curare -- ed e- "
                   "successo: `A3` era TRE cose" % idv)
    if idv in al:
        err.append("`P-ID` `%s`: e- GIA- UN ALIAS di un-altra voce. ### Un alias e- una "
                   "PROMESSA DI RISOLUZIONE: se un ID nuovo lo prende, la promessa si "
                   "rompe" % idv)
    if idv in om:
        err.append("`P-ID` `%s`: e- GIA- uno dei significati dichiarati di un OMONIMO. "
                   "### Gli omonimi RESTANO omonimi, e il loro metadato RESTA: un ID "
                   "nuovo che ne prende un significato NE CANCELLA LA DICHIARAZIONE"
                   % idv)
    return err


def censimento():
    """### Chi ### **violerebbe** il presidio, fra le voci che ci sono ### **OGGI.**

    ### ⚠ **E- un CENSIMENTO, non un verdetto:** il presidio guarda ### **chi
    nasce**, e questi ### **c-erano prima.** ### **Serve a dire quanto il divieto e-
    nuovo**, non a condannare qualcuno.
    """
    D = os.path.join(RADICE, "doc", "indice")
    voci = _jsonl(os.path.join(D, "voci.jsonl"))
    ids, al, om = presi(voci)
    corti = sorted(x for x in ids if len(x) < MIN_CARATTERI)
    collisi = sorted((ids & al) | (ids & om))
    return {"corti": corti, "collisi": collisi, "id": len(ids), "alias": len(al),
            "omonimi": len(om)}


def collaudo():
    import _presidio
    _presidio.avvia(__file__)
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-64s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    c = censimento()
    print("=" * 100)
    print("IL COLLAUDO DI `P-ID` -- nei DUE VERSI")
    print("=" * 100)
    print("  il CENSIMENTO: %d ID, %d alias, %d significati di omonimo"
          % (c["id"], c["alias"], c["omonimi"]))
    print("  ### gli ID piu- corti di %d: %d -- %s"
          % (MIN_CARATTERI, len(c["corti"]), ", ".join(c["corti"][:14])
             + (" ..." if len(c["corti"]) > 14 else "")))
    print("  ### gli ID che collidono con un alias o un omonimo: %d -- %s"
          % (len(c["collisi"]), ", ".join(c["collisi"][:14])
             + (" ..." if len(c["collisi"]) > 14 else "")))
    print()
    # ------------------------------------------------------------------ i DUE versi
    esito("NON deve scattare: un ID NUOVO, lungo e libero",
          controlla_nuovo("PROVA-ID-LIBERO-OGGI") == [],
          "### e- il verso che dice che il presidio NON rifiuta tutto")
    esito("### DEVE scattare: un ID che ESISTE GIA-",
          any("ESISTE GIA- come ID" in e for e in controlla_nuovo("A16")),
          "### `A3` era TRE cose: e- la collisione che l-indice cura")
    al = sorted(presi()[1])
    esito("### DEVE scattare: un ID che e- GIA- UN ALIAS",
          any("GIA- UN ALIAS" in e for e in controlla_nuovo(al[0])),
          "`%s`: ### un alias e- una PROMESSA DI RISOLUZIONE" % al[0])
    om = sorted(presi()[2])
    esito("### DEVE scattare: un ID che e- GIA- un significato di OMONIMO",
          any("significati dichiarati" in e for e in controlla_nuovo(om[0])),
          "`%s`: ### gli omonimi RESTANO, e il metadato RESTA" % om[0])
    esito("### DEVE scattare: un ID piu- corto di %d caratteri" % MIN_CARATTERI,
          any("il minimo e-" in e for e in controlla_nuovo("XY")),
          "### i nomi corti sono quelli che hanno collisionato")
    esito("### e il CENSIMENTO ha MATERIA: ci sono ID corti ESISTENTI",
          len(c["corti"]) > 0,
          "%d: ### restano, perche- un ID NON SI PERDE -- il presidio guarda CHI NASCE"
          % len(c["corti"]))
    esito("### e il braccio sopra DICE che <<da oggi>> e- la parola che conta",
          len(c["corti"]) > 10,
          "### se il presidio guardasse anche gli esistenti, rifiuterebbe %d voci VERE"
          % len(c["corti"]))

    # ===================================================================================
    #   ### ⭐ **LA CURA DEL CRITERIO ② DI `da-decidere`, NEI DUE VERSI**
    # ===================================================================================
    # ### ⛔ **Sta QUI e non in `indice.py` per una ragione precisa:** il criterio ②
    # ### e- stato ### **TOLTO**, e ### **`P-ID` E- LA GUARDIA CHE LO SOSTITUISCE.** Un
    # ### collaudo che prova la rimozione ### **deve stare attaccato a cio- che la rende
    # ### sicura**, altrimenti domani qualcuno toglie `P-ID` e ### **nessuno misura che la
    # ### rimozione del criterio era appoggiata a lui.**
    D = os.path.join(RADICE, "doc", "indice")
    voci = _jsonl(os.path.join(D, "voci.jsonl"))
    omon = sorted(v["id"] for v in voci if (v.get("meta") or {}).get("omonimo"))
    elenco = io.open(os.path.join(D, "DA_DECIDERE_LUCA.md"),
                     encoding="utf-8").read() if os.path.exists(
                         os.path.join(D, "DA_DECIDERE_LUCA.md")) else ""
    print()
    print("  la CURA del criterio ②: %d voci hanno ANCORA `meta.omonimo` -- %s"
          % (len(omon), ", ".join(omon)))
    esito("### il collaudo ha MATERIA: ci sono voci con `meta.omonimo`",
          len(omon) >= 11,
          "%d: ### il metadato RESTA, e- un FATTO -- la decisione di Luca lo dice" % len(omon))
    dentro = [i for i in omon if ("`%s`" % i) in elenco]
    esito("NON deve scattare: un omonimo NON e- piu- in `DA_DECIDERE_LUCA.md`",
          dentro == [],
          "### il criterio ② e- TOLTO: <<la domanda si chiude>> E <<il metadato resta>>"
          if not dentro else "### ANCORA DENTRO: %s" % ", ".join(dentro))
    rifiutati = [i for i in omon if controlla_nuovo(i, voci) != []]
    esito("### DEVE scattare: `P-ID` RIFIUTA la rinascita di OGNI omonimo",
          len(rifiutati) == len(omon),
          "%d su %d: ### e- LA GUARDIA CHE SOSTITUISCE IL CRITERIO -- un ID prende un "
          "secondo significato SOLO se qualcuno riusa un ID che esiste"
          % (len(rifiutati), len(omon)))
    sig = sorted(presi(voci)[2])
    esito("### DEVE scattare: `P-ID` rifiuta anche un SIGNIFICATO dichiarato",
          sig != [] and controlla_nuovo(sig[0], voci) != [],
          "`%s` fra %d significati: ### un ID nuovo che ne prende uno NE CANCELLA LA "
          "DICHIARAZIONE" % (sig[0] if sig else "-", len(sig)))
    print("=" * 100)
    print("IL COLLAUDO DI `P-ID`: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--collaudo" in argv:
        return collaudo()
    c = censimento()
    print("  `P-ID`: %d ID, %d alias, %d significati di omonimo; minimo %d caratteri"
          % (c["id"], c["alias"], c["omonimi"], MIN_CARATTERI))
    print("  ### il censimento (chi VIOLEREBBE, e c-era prima): %d ID corti, %d collisi"
          % (len(c["corti"]), len(c["collisi"])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
