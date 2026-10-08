# -*- coding: utf-8 -*-
"""LA BYTE-INERZIA DELL'OSSERVATORE `TermoH3`: `220` passi CON e SENZA, stato IDENTICO AL BIT.

### ⛔ **PERCHE' SERVE, ed e' il wrapper PIU' INVASIVO finora:** `TermoH3` avvolge
### **`step` STESSO** *(un metodo, quindi l'assegnazione su `net` crea un attributo
d'istanza)* e ### **`scuoti_vuoto`** *(una funzione di MODULO)*. Il presidio `sola_lettura`
guarda ### **`net`**, non il modulo e non i metodi sostituiti: ### **questo sigillo e' l'unico
controllo che dice, al bit, su TUTTO lo stato, se quegli involucri cambiano la dinamica.**

### ⛔ **E LA FINESTRA E' `220` PASSI, NON `50`:** sulla scena del driver col seme `11` la
### **prima nascita e' al passo `216`**, e una finestra piu' corta girerebbe
### **PRIMA che gli involucri lavorino attraverso una nascita** *(`FINESTRA-PRE-NASCITA`)*.

### ✔ **PIU' DUE CONTROLLI POSITIVI CHE POSSONO FALLIRE:** il braccio osservato deve
### **aver misurato qualcosa** *(passi registrati e un bilancio non vuoto)* e gli involucri
devono essere ### **RIMOSSI**. Senza di essi *<<zero differenze>>* potrebbe voler dire
*<<l'osservatore non ha fatto niente>>*, cioe' un ### **`FALSO-UNO`.**
"""
import contextlib
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
for _p in (os.path.join(RADICE, "csv"), os.path.join(RADICE, "csv", "_test_fork"), _QUI):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import _presidio                                   # noqa: E402
_presidio.avvia(__file__)

import _passo                                      # noqa: E402
import _mitosi_soglia_grad as _MSG                 # noqa: E402
import _misura_verso as MV                         # noqa: E402
import _termo_h3 as TH                             # noqa: E402

stampa, riga, blob = _MSG.stampa, _MSG.riga, _MSG.blob
NL = chr(10)
PASSI = 220
FUORI = os.path.join(_QUI, "_inerzia_termo")
SIM = os.path.join(RADICE, "soliton_simulator.py")
BLOB_ATTESO = "b8c21049"
# ### ⛔ **L'ESCLUSIONE NON E' PIU' VUOTA, dal 2026-10-08, e la RAGIONE E' SCRITTA.**
#   `_calcpsi_origini` e' un dizionario DIAGNOSTICO scritto dentro `calcola_psi`
#   *(`:6295`-`:6297`)*, con chiavi costruite come
#       `"%s:%d" % (chiamante.co_name, chiamante.f_lineno)`
#   cioe' ### **IL NOME E LA RIGA DEL CHIAMANTE**. L'osservatore di `D2-TER` avvolge
#   `calcola_psi` per misurare se `K_SYNC = 0` e' un solo interruttore, e
#   ### **l'involucro DIVENTA il chiamante**: le chiavi cambiano ### **per
#   costruzione**, non per un effetto sulla fisica.
#   ### ⚠ **E NON BASTA AGGREGARE PER FUNZIONE**, che e' la pratica abituale per
#   questa voce: con l'involucro cambia ### **anche il nome** della funzione
#   *(`_inv_psi` invece di `step`)*, quindi l'aggregazione non riconcilia niente.
#   ### ✔ **E NESSUNA LEGGE LO LEGGE:** nel simulatore compare SOLO a `:6295` e
#   `:6297`, ### **entrambe SCRITTURE**. Censito, non supposto.
#   ### ⛔ **MA ESCLUDERE SENZA METTERE NIENTE AL POSTO SAREBBE TOGLIERE IL
#   CONTROLLO**, quindi al suo posto c'e' il controllo positivo `(3)` qui sotto: la
#   ### **SOMMA** dei valori deve coincidere fra i due bracci e con
#   `_calcpsi_w_none`. ### **Le CHIAVI cambiano; i NUMERI no.**
ESCLUSI = ("_calcpsi_origini",)


def _impronta(net):
    return {k: MV._firma(v) for k, v in net.__dict__.items() if k not in ESCLUSI}


def _gira(nome, con_osservatore):
    """Una corsa da `PASSI` passi. ### **La scena e il seme sono gli stessi.**"""
    with contextlib.redirect_stdout(io.StringIO()):
        S, N, _a = _MSG.carica(nome, SIM)
        o = None
        if con_osservatore:
            # ### **IL BRACCIO `base`: gli involucri sono di SOLA LETTURA**, nessun
            #   intervento. E' quello che gira in `D1`.
            o = TH.TermoH3("base")
            o.prepara(S, N)
            o.osserva(S, N, 0, True)
        for k in range(1, PASSI + 1):
            _passo.passo_pieno(S, N)
            if o is not None:
                o.osserva(S, N, k, k in TH.PASSI_MISURA)
        if o is not None:
            o.ripristina()
    return _impronta(N), o, N


def main(argv):
    riga("=")
    stampa("LA BYTE-INERZIA DELL'OSSERVATORE `TermoH3`: %d passi CON e SENZA" % PASSI)
    riga("=")
    b = blob(SIM)
    stampa("  simulatore %s   atteso %s" % (b[:8], BLOB_ATTESO))
    if not b.startswith(BLOB_ATTESO):
        raise SystemExit("[FERMO] il blob del simulatore NON e' quello atteso.")
    stampa("  strumento %s (termo_h3)   %s (misura_verso)"
           % (blob(TH.__file__)[:8], blob(MV.__file__)[:8]))
    stampa("  ### LA FINESTRA E' %d PASSI, cioe' OLTRE la prima nascita (216)." % PASSI)
    stampa()
    stampa("  --- il braccio NUDO")
    f1, _o1, N1 = _gira("termo_nudo", False)
    stampa("      n = %d, archi = %d, attributi = %d" % (N1.n, len(N1.i), len(f1)))
    stampa("  --- il braccio CON L'OSSERVATORE")
    f2, o2, N2 = _gira("termo_oss", True)
    stampa("      n = %d, archi = %d, attributi = %d" % (N2.n, len(N2.i), len(f2)))
    solo1 = sorted(set(f1) - set(f2))
    solo2 = sorted(set(f2) - set(f1))
    diversi = sorted(k for k in set(f1) & set(f2) if f1[k] != f2[k])
    stampa()
    riga("-")
    stampa("  attributi solo nel NUDO: %d  %r" % (len(solo1), solo1))
    stampa("  attributi solo CON l'osservatore: %d  %r" % (len(solo2), solo2))
    stampa("  attributi DIVERSI: %d  %r" % (len(diversi), diversi[:8]))
    ok = not (solo1 or solo2 or diversi)
    stampa()
    riga("=")
    if ok:
        stampa("  ### ✔ LA BYTE-INERZIA PASSA: lo stato e' IDENTICO AL BIT su %d "
               "attributi." % len(f1))
        stampa("  ### L'osservatore `TermoH3` NON cambia la dinamica, involucri su `step` e "
               "su `scuoti_vuoto` compresi.")
    else:
        stampa("  ### ⛔ LA BYTE-INERZIA FALLISCE. LE CORSE NON PARTONO.")
        stampa("  ### Le differenze sono NOMINATE qui sopra.")
    riga("=")
    # ### ✔ **I DUE CONTROLLI POSITIVI, e POSSONO fallire.**
    _np_ = len(o2.passi) if o2 is not None else 0
    _bil = 0
    if o2 is not None:
        _bil = sum(1 for r in o2.passi if r.get("per_classe"))
    _tolti = (o2._inv is None) if o2 is not None else False
    stampa("  controllo: passi registrati %d   passi col BILANCIO %d   involucri rimossi %s"
           % (_np_, _bil, "SI" if _tolti else "NO"))
    # ### ⭐ **IL TERZO CONTROLLO POSITIVO, che RIMPIAZZA l'attributo escluso.**
    #   `_calcpsi_origini` e' escluso perche' le sue CHIAVI sono righe del chiamante.
    #   ### **Ma i suoi NUMERI devono coincidere**: la somma dei conteggi e' il numero
    #   di chiamate con `w is None`, che e' ### **una grandezza della dinamica**, non
    #   della contabilita'. ### ⛔ **E PUO' FALLIRE:** se l'involucro aggiungesse o
    #   togliesse una chiamata, questa somma cambierebbe.
    _o1d = getattr(N1, "_calcpsi_origini", None) or {}
    _o2d = getattr(N2, "_calcpsi_origini", None) or {}
    _s1 = sum(_o1d.values())
    _s2 = sum(_o2d.values())
    _w1 = int(getattr(N1, "_calcpsi_w_none", 0) or 0)
    _w2 = int(getattr(N2, "_calcpsi_w_none", 0) or 0)
    _c1 = int(getattr(N1, "_calcpsi_chiamate", 0) or 0)
    _c2 = int(getattr(N2, "_calcpsi_chiamate", 0) or 0)
    stampa("  controllo dell'ATTRIBUTO ESCLUSO -- le CHIAVI cambiano, i NUMERI no:")
    stampa("     somma dei conteggi di `_calcpsi_origini`:  nudo %d   osservato %d"
           % (_s1, _s2))
    stampa("     `_calcpsi_w_none`:                         nudo %d   osservato %d"
           % (_w1, _w2))
    stampa("     chiavi (che POSSONO differire):            nudo %d   osservato %d  %r"
           % (len(_o1d), len(_o2d), sorted(_o2d)[:4]))
    stampa("     `_calcpsi_chiamate` TOTALI:                nudo %d   osservato %d"
           % (_c1, _c2))
    _ok_num = (_s1 == _s2 == _w1 == _w2) and (_c1 == _c2)
    if not _ok_num:
        stampa("  ### ⛔ I NUMERI DELL'ATTRIBUTO ESCLUSO NON COINCIDONO: l'involucro ha "
               "cambiato QUANTE volte `calcola_psi` viene chiamata, e quello NON e' "
               "contabilita'.")
        ok = False
    else:
        stampa("  ### ✔ I NUMERI COINCIDONO: l'involucro cambia le CHIAVI e non i "
               "CONTEGGI, quindi l'esclusione copre contabilita' e non fisica.")
    if _np_ == 0 or _bil == 0 or not _tolti:
        stampa("  ### ⛔ IL BRACCIO OSSERVATO NON HA MISURATO, o gli involucri sono "
               "rimasti: il confronto sarebbe un FALSO-UNO.")
        ok = False
    d = {"blob_sim": b, "blob_termo_h3": blob(TH.__file__), "blob_misura_verso": blob(MV.__file__),
         "passi": PASSI, "esclusi": list(ESCLUSI), "attributi": len(f1),
         "solo_nudo": solo1, "solo_osservatore": solo2, "diversi": diversi,
         "passi_registrati": _np_, "passi_col_bilancio": _bil,
         "involucri_rimossi": bool(_tolti),
         # ### ⭐ **il controllo dell'attributo ESCLUSO**, nel json e non solo a schermo
         "escluso_calcpsi_origini": {
             "somma_conteggi": {"nudo": int(_s1), "osservato": int(_s2)},
             "calcpsi_w_none": {"nudo": _w1, "osservato": _w2},
             "calcpsi_chiamate": {"nudo": _c1, "osservato": _c2},
             "chiavi": {"nudo": len(_o1d), "osservato": len(_o2d)},
             "numeri_coincidono": bool(_ok_num)},
         "a_valle": {"nudo": [int(N1.n), int(len(N1.i))],
                     "oss": [int(N2.n), int(len(N2.i))]},
         "esito": "PASSA" if ok else "FALLISCE"}
    os.makedirs(FUORI, exist_ok=True)
    io.open(os.path.join(FUORI, "inerzia.json"), "w", encoding="utf-8").write(
        json.dumps(d, indent=1, ensure_ascii=False))
    io.open(os.path.join(FUORI, "inerzia.txt"), "w", encoding="utf-8").write(
        NL.join(_MSG.P) + NL)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
