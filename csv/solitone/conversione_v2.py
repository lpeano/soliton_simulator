# -*- coding: utf-8 -*-
r"""**LA CONVERSIONE DELLE COSTANTI DELL'ENERGIA DAL NUCLEO VECCHIO A v2** *(l'unificazione, U4; Luca `2026-11-12`; il task history `doc/TASK_HISTORY/2026-11-12_unificazione.md`, sez. `1.6`)*. [[PIANO-2D-3D]] [[H-NUCLEO-CONGELATO]]

**v2** *(lo zero simmetrico nel nucleo, `energia_pesata.termini_di_h`)* **sposta l'ENERGIA di uno stato, non la dinamica** *(il braccio `0`, `4/4` al bit)*. **Per termine**
*(`doc/referti_l2/mb_costante.txt`; U3, `67ba77a7`: `E0` nuovo meno vecchio `= pi (M + V)` con scarto `0`)*: `cin` e `leg` **uguali**; `cost` **`+ pi M`**; `vuo` **`+ pi V`**;
`tot` **`+ pi (M + V)`**; `e_K` *(per unita' di norma)* **`+ pi`**.
### **I jsonl e i referti vecchi NON si riscrivono: la conversione si fa nel CONTROLLO.** **La tolleranza:** `TOLL = 1e-14` relativa *(Luca, U0 confermato: l'ultimo bit della
conversione, dichiarato: `-4.7122750003546425 + pi` differisce dal misurato di `4.4e-16`)*. **Le chiavi della dinamica restano AL BIT.**
"""
import math

TOLL = 1e-14                 # ### Luca (U0 confermato, 2026-11-12): le costanti convertite entro 1e-14 relativo
EPS = 2.0 ** -52
TOLL_ACC = 64                # ### l'ACCUMULATORE (E_ass): 64 eps |E| sqrt(2 N), la soglia gia' fissata in (mb-a), sez. 4 del task history del laterale (mb_costante.py); non un numero nuovo


def vicino(a, b):
    return a == b or abs(a - b) <= TOLL * max(abs(a), abs(b))


def e_K(registrato, misurato):
    """### `"uguale"` *(lo stesso nucleo, al bit)*, `"convertito"` *(registrato col vecchio: `misurato = registrato + pi` entro `TOLL`)*, o `None` *(ne' l'uno ne' l'altro)*."""
    if misurato == registrato:
        return "uguale"
    if vicino(misurato, registrato + math.pi):
        return "convertito"
    return None


def conti(E):
    """### un dizionario di conti per regione *(`{regione: {M, V, cin, cost, leg, tot, vuo}}`)* **convertito a v2.**"""
    out = {}
    for reg, c in E.items():
        d = dict(c)
        d["cost"] = c["cost"] + math.pi * c["M"]
        d["vuo"] = c["vuo"] + math.pi * c["V"]
        d["tot"] = c["tot"] + math.pi * (c["M"] + c["V"])
        out[reg] = d
    return out


def scala(c):
    """### **la scala della tolleranza del TOTALE** *(Luca `2026-11-12` `14:55`)*: `max(|tot|, pi (M + V))`, il pavimento dell'arrotondamento della costante aggiunta."""
    return max(abs(c["tot"]), math.pi * (c["M"] + c["V"]))


def uguale_totale(a, b):
    """### **i conti del TOTALE** *(il toro intero)*: `M` e `V` al bit; `cin`, `cost`, `leg`, `tot`, `vuo` del vecchio CONVERTITI entro `TOLL max(|tot|, pi (M + V))`. `(ok, scarto / scala)`."""
    cv = conti({"t": b})["t"]
    ok = set(a) == set(cv) and a["M"] == cv["M"] and a["V"] == cv["V"]
    sc = scala(a)
    peggio = 0.0
    for k in ("cin", "cost", "leg", "tot", "vuo"):
        d = abs(a[k] - cv[k])
        ok = ok and d <= TOLL * sc
        peggio = max(peggio, d / sc)
    return ok, peggio


def conti_like(d):
    return isinstance(d, dict) and {"M", "V", "cin", "tot"} <= set(d)


def uguale_regione(a, b):
    """### **i conti di una REGIONE o di un SETTORE:** solo `M` e `V` al bit *(Luca `14:55`: le energie per regione dipendono dalla scelta dello zero -- lo zero di v2 sposta energia
    fra archi e nodi, e al confine di una regione non si compensa)*."""
    return isinstance(a, dict) and set(a) == set(b) and a["M"] == b["M"] and a["V"] == b["V"]


def uguale_ricorsivo(a, b):
    """### al bit, tranne i dizionari di conti *(regioni, settori)*: per loro `uguale_regione`."""
    if conti_like(b):
        return uguale_regione(a, b)
    if isinstance(b, dict):
        return isinstance(a, dict) and set(a) == set(b) and all(uguale_ricorsivo(a[k], b[k]) for k in b)
    if isinstance(b, list):
        return isinstance(a, list) and len(a) == len(b) and all(uguale_ricorsivo(x, y) for x, y in zip(a, b))
    return a == b


def uguali_campioni(nuovi, vecchi, M_ass0, V_ass0, n_tick):
    """### **I campioni di un pezzo rifatto con v2 contro quelli registrati col vecchio** *(Luca `14:55`)*: **`E["totale"]` convertito** *(`uguale_totale`)*; **le altre regioni e i settori
    di `per` solo `M` e `V` al bit**; **il campione del bordo:** `E` convertito, `E_ass` da accumulatore; **ogni altra chiave AL BIT.** `(ok, il peggio scarto/scala del totale, le chiavi diverse)`."""
    if len(nuovi) != len(vecchi):
        return False, float("inf"), ["il numero dei campioni"]
    ok, peggio, div = True, 0.0, []
    for a, b in zip(nuovi, vecchi):
        if set(a) != set(b):
            ok = False
            div.append("le chiavi")
            continue
        for k in a:
            if k == "E":
                o = set(a[k]) == set(b[k])
                for reg in b[k]:
                    if reg == "totale":
                        o2, p = uguale_totale(a[k][reg], b[k][reg])
                        peggio = max(peggio, p)
                    else:
                        o2 = uguale_regione(a[k].get(reg), b[k][reg])
                    o = o and o2
            elif k == "bordo" and isinstance(b[k], dict):
                o, _p = uguale_bordo(a[k], b[k], M_ass0, V_ass0, n_tick, campione=True)
            else:
                o = uguale_ricorsivo(a[k], b[k])
            if not o:
                ok = False
                div.append(k)
    return ok, peggio, sorted(set(div))


def uguale_bordo(a, b, M_ass0, V_ass0, n_tick, campione=False, scala_E=None):
    """### il bordo *(del pezzo o del campione)*: al bit, tranne `E_ass` *(e `E` nel campione)* convertiti. **`E_ass` e' un ACCUMULATORE** *(la somma di `n_tick` differenze
    di energie grandi)*: **la sua soglia e' `TOLL_ACC eps |E| sqrt(2 n_tick)`**, `|E|` l'energia del campione *(o `scala_E` per il bordo del pezzo)*."""
    if set(a) != set(b):
        return False, float("inf")
    ok, peggio = True, 0.0
    for k in a:
        if k == "E_ass":
            v = b[k] + math.pi * ((b["M_ass"] - M_ass0) + (b["V_ass"] - V_ass0))
            sc = abs(a["E"]) if campione else abs(scala_E)
            tol = TOLL_ACC * EPS * sc * math.sqrt(2.0 * n_tick)
            ok = ok and abs(a[k] - v) <= tol
            peggio = max(peggio, abs(a[k] - v) / max(sc, 1e-300))
            continue
        elif k == "E" and campione:
            v = b[k] + math.pi * (b["M"] + b["V"])
            sc = max(abs(a[k]), math.pi * (a["M"] + a["V"]))   # ### Luca 14:55: la scala del totale
            ok = ok and abs(a[k] - v) <= TOLL * sc
            peggio = max(peggio, abs(a[k] - v) / sc)
            continue
        else:
            ok = ok and a[k] == b[k]
            continue
        ok = ok and vicino(a[k], v)
        peggio = max(peggio, abs(a[k] - v) / max(abs(a[k]), abs(v), 1e-300))
    return ok, peggio
