# -*- coding: utf-8 -*-
"""IL COLLAUDO DELLA CATENA — **lo schedulatore, i due candidati, IL CONO, e i SEI casi
che DEVONO fallire.**

### ⛔ **PERCHE- STA IN UN FILE SUO E NON DENTRO `passo.py`:** il cono si misura
### **sulla norma**, la norma e- ### **un osservatore**, e `P-E4` vieta a `passo.py` di
importare `osservatori/` *(`A17`: la fisica non dipende da chi la guarda)*.
### ⭐ **Il presidio mi ha costretto alla forma giusta**, invece di lasciarmi
scegliere.

### ⚠ **E NESSUN NUMERO DI QUESTO COLLAUDO E- RICOPIATO ALTROVE A MANO**
*(`L-NUMERI`)*: il referto della tappa `6` li prende ### **dall-uscita di questo
comando.**
"""
import importlib.util
import io
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(RADICE, "csv"))
sys.path.insert(0, os.path.join(_QUI, "leggi"))

import hamiltoniana as HAM                                   # noqa: E402
import passo as PA                                           # noqa: E402
import schema as SCH                                         # noqa: E402
import stato as ST                                           # noqa: E402

NL = chr(10)
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-64s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))


def _modulo(p, nome):
    spec = importlib.util.spec_from_file_location(nome, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def catena(n=9):
    """### Una CATENA di `n` nodi: ### **le distanze sono senza ambiguita-.**"""
    ii = np.arange(n - 1, dtype=int)
    jj = np.arange(1, n, dtype=int)
    return ii, jj


def stato_seme(n, seme):
    st = ST.nuovo(n)
    rng = np.random.default_rng(seme)
    for k in st:
        st[k][...] = (rng.normal(size=st[k].shape) + 1j * rng.normal(size=st[k].shape))
    return st


def byte(st):
    return tuple((k, st[k].tobytes()) for k in sorted(st))


def distanze(ii, jj, n, da):
    """Le distanze in ARCHI da `da`, per BFS. `-1` = non raggiungibile."""
    vic = [[] for _ in range(n)]
    for a, b in zip(ii, jj):
        vic[int(a)].append(int(b))
        vic[int(b)].append(int(a))
    d = [-1] * n
    d[da] = 0
    coda = [da]
    while coda:
        x = coda.pop(0)
        for y in vic[x]:
            if d[y] < 0:
                d[y] = d[x] + 1
                coda.append(y)
    return d


# =====================================================================================
#   (A) LO SCHEDULATORE -- I TRE LIVELLI
# =====================================================================================

def livelli(T):
    print()
    print("  (A) LO SCHEDULATORE -- I TRE LIVELLI, e quali permutazioni sono byte-identiche")
    n = 9
    ii, jj = catena(n)
    st = stato_seme(n, 11)

    # --- livello 1: i TERMINI di H
    perm = list(reversed(T))
    e1, e2 = HAM.energia(st, ii, jj, T), HAM.energia(st, ii, jj, perm)
    esito("`1` i TERMINI di `H`: permutati, `H` e- IDENTICA AL BIT", e1 == e2,
          "`math.fsum`: la somma ad arrotondamento esatto NON dipende dall-ordine")
    g1 = HAM.gradiente(st, ii, jj, T)
    g2 = HAM.gradiente(st, ii, jj, perm)
    esito("`1` i TERMINI di `H`: permutati, il GRADIENTE e- IDENTICO AL BIT",
          byte(g1) == byte(g2), "perche- `gradiente()` IMPONE l-ordine canonico per ID")
    r1 = HAM.gradiente_grezzo(st, ii, jj, T)
    r2 = HAM.gradiente_grezzo(st, ii, jj, perm)
    esito("### e la somma GREZZA permutata NON lo e-: l-ordine PORTA CARICO",
          byte(r1) != byte(r2),
          "### altrimenti il braccio di sopra sarebbe un FALSO-UNO")

    # --- livello 2: gli ARCHI dentro uno strato
    ss = PA.strati(ii, jj)
    esito("`2` gli STRATI sono DISGIUNTI (nessun nodo in comune dentro uno strato)",
          all(len(set(list(ii[s]) + list(jj[s]))) == 2 * len(s) for s in ss),
          "%d strati su %d archi" % (len(ss), len(ii)))
    archi = [m for m in T if m.TIPO == "termine_arco"]
    s0 = ss[0]
    a, _sc, _us = PA.mezzo_implicito(st, ii[s0], jj[s0], 0.01, archi)
    rng = np.random.default_rng(5)
    p = rng.permutation(len(s0))
    b, _sc, _us = PA.mezzo_implicito(st, ii[s0][p], jj[s0][p], 0.01, archi)
    esito("`2` gli ARCHI dentro UNO strato: permutati, il sotto-passo e- BYTE-IDENTICO",
          byte(a) == byte(b),
          "sono DISGIUNTI: ogni nodo riceve UN SOLO contributo, non c-e- somma da riordinare")

    # --- livello 3: FRA STRATI
    comp = PA.composizione_locale(len(ss))
    esito("`3` la composizione LOCALE e- valida (simmetrica, senza doppioni, pesi a 1)",
          PA.valida_composizione(comp, len(ss)) == [],
          "%d operazioni" % len(comp))
    if len(ss) >= 2:
        u, _ = PA.passo_locale(st, ii, jj, 0.01, T, gli_strati=ss)
        v, _ = PA.passo_locale(st, ii, jj, 0.01, T, gli_strati=tuple(reversed(ss)))
        esito("`3` FRA STRATI: scambiarli NON e- byte-identico -- ### NON COMMUTANO",
              byte(u) != byte(v),
              "### due operatori che non commutano danno un RISULTATO diverso, non un "
              "arrotondamento diverso")
    return ii, jj, ss


# =====================================================================================
#   (B) LA COMPOSIZIONE -- i casi che DEVONO essere rifiutati
# =====================================================================================

def composizioni():
    print()
    print("  (B) LA COMPOSIZIONE -- rifiutata se ASIMMETRICA o con un DOPPIONE")
    esito("NON deve scattare: la composizione GLOBALE",
          PA.valida_composizione(PA.COMPOSIZIONE_GLOBALE, 1) == [])
    esito("### DEVE scattare: una composizione ASIMMETRICA",
          any("NON E- SIMMETRICA" in e for e in PA.valida_composizione(
              (("nodi", 0.5), ("arco:0", 1.0)), 1)),
          "l-errore di ordine PARI non si annulla: l-energia deriva SECOLARMENTE")
    esito("### DEVE scattare: i NOMI palindromi e i PESI no -- simmetria FINTA",
          any("PESI non sono simmetrici" in e for e in PA.valida_composizione(
              (("nodi", 0.25), ("arco:0", 1.0), ("nodi", 0.75)), 1)))
    esito("### DEVE scattare: un DOPPIONE consecutivo",
          any("DOPPIONE" in e for e in PA.valida_composizione(
              (("nodi", 0.25), ("nodi", 0.5), ("nodi", 0.25)), 1)),
          "due volte di fila e- un passo piu- lungo scritto male")
    esito("### DEVE scattare: i pesi che NON sommano a 1",
          any("sommano a" in e for e in PA.valida_composizione(
              (("nodi", 0.25), ("arco:0", 1.0), ("nodi", 0.25)), 1)),
          "si integrerebbe un tempo DIVERSO da dt, e il codice non lo direbbe")
    esito("### DEVE scattare: un-operazione FUORI VOCABOLARIO",
          any("non e- nel vocabolario" in e for e in PA.valida_composizione(
              (("inventata", 1.0),), 1)))
    esito("### DEVE scattare: la composizione VUOTA",
          any("VUOTA" in e for e in PA.valida_composizione((), 1)))


# =====================================================================================
#   (C) IL CONO -- deterministico, per PASSO e per STRATO
# =====================================================================================

def cono(T, n=9, dt=0.01):
    print()
    print("  (C) IL CONO -- perturbo UN nodo, e misuro FIN DOVE arriva")
    ii, jj = catena(n)
    ss = PA.strati(ii, jj)
    d = distanze(ii, jj, n, 0)
    comp = PA.composizione_locale(len(ss))
    n_arco = len([1 for nome, _ in comp if nome.startswith(PA.PREFISSO_ARCO)])

    def raggio(fun, passi, **kw):
        """La distanza MASSIMA a cui lo stato differisce, e se oltre e- ESATTAMENTE zero."""
        a = stato_seme(n, 11)
        b = {k: v.copy() for k, v in a.items()}
        b["psi"][0, 0] += 1e-3
        for _ in range(passi):
            a = fun(a, ii, jj, dt, T, **kw)[0]
            b = fun(b, ii, jj, dt, T, **kw)[0]
        diff = np.abs(a["psi"] - b["psi"]).max(axis=1)
        per_d = {}
        for k in range(n):
            per_d.setdefault(d[k], 0.0)
            per_d[d[k]] = max(per_d[d[k]], float(diff[k]))
        tocchi = [k for k in sorted(per_d) if per_d[k] != 0.0]
        esatti = [k for k in sorted(per_d) if per_d[k] == 0.0]
        return max(tocchi) if tocchi else -1, per_d, esatti

    # --- UN SOLO STRATO: il cono di UN sotto-passo
    archi = [m for m in T if m.TIPO == "termine_arco"]
    a = stato_seme(n, 11)
    b = {k: v.copy() for k, v in a.items()}
    b["psi"][0, 0] += 1e-3
    s0 = ss[0]
    a1 = PA.mezzo_implicito(a, ii[s0], jj[s0], dt, archi)[0]
    b1 = PA.mezzo_implicito(b, ii[s0], jj[s0], dt, archi)[0]
    df = np.abs(a1["psi"] - b1["psi"]).max(axis=1)
    rag = max([k for k in range(n) if df[k] != 0.0] or [-1])
    esito("`per STRATO`: un sotto-passo d-arco arriva a ESATTAMENTE `1` arco",
          max(d[k] for k in range(n) if df[k] != 0.0) == 1,
          "e oltre e- ### **ESATTAMENTE ZERO** (`%d` nodi a `0.0`)"
          % int((df == 0.0).sum()))

    # --- IL LOCALE, per PASSO
    r1, per1, es1 = raggio(PA.passo_locale, 1, gli_strati=ss)
    esito("`per PASSO`, LOCALE: il raggio e- `%d` archi, e oltre e- ESATTAMENTE ZERO" % r1,
          r1 == n_arco and len(es1) > 0,
          "`%d` operazioni d-arco nella composizione -> `%d` archi: COINCIDE"
          % (n_arco, n_arco))
    print("      LOCALE, |delta| per distanza: %s"
          % "  ".join("d=%d:%.3e" % (k, per1[k]) for k in sorted(per1)))

    # --- IL GLOBALE, per PASSO
    r2, per2, es2 = raggio(PA.passo_globale, 1)
    esito("`per PASSO`, GLOBALE: il cono NON e- esatto -- arriva a `%d` archi su `%d`"
          % (r2, max(d)), r2 > n_arco,
          "### il punto fisso ITERA SUL GRAFO INTERO: e- cio- che <<implicito e globale>> SIGNIFICA")
    print("      GLOBALE, |delta| per distanza: %s"
          % "  ".join("d=%d:%.3e" % (k, per2[k]) for k in sorted(per2)))
    # ### ⛔ **QUI AVEVO SCRITTO UN BRACCIO CHE AFFERMAVA IL FALSO:**
    # ### <<il GLOBALE a distanza massima NON e- zero>>. ### **La misura lo ha
    # ### smentito:** oltre un certo raggio e- ### **ESATTAMENTE ZERO.**
    # ### ⭐ **E LA RAGIONE E- PEGGIORE DI QUELLA CHE CREDEVO:** il raggio
    # ### ### **DIPENDE DALLA TOLLERANZA DEL PUNTO FISSO** -- quindi il globale ha
    # ### un orizzonte che ### **ASSOMIGLIA a una causalita- e non lo e-**, perche-
    # ### e- fissato da ### **una manopola del risolutore.**
    # ### ⚠ **Un cono INFINITO si vedrebbe. Questo si nasconde.**
    raggi = {}
    for tl in (1e-4, 1e-8, 1e-14):
        aa = stato_seme(n, 11)
        bb = {k: v.copy() for k, v in aa.items()}
        bb["psi"][0, 0] += 1e-3
        a2, info = PA.passo_globale(aa, ii, jj, dt, T, toll=tl)
        b2, _ = PA.passo_globale(bb, ii, jj, dt, T, toll=tl)
        df2 = np.abs(a2["psi"] - b2["psi"]).max(axis=1)
        tocchi = [d[k] for k in range(n) if df2[k] != 0.0]
        raggi[tl] = (max(tocchi), info["iterazioni"])
    print("      GLOBALE, il RAGGIO contro la TOLLERANZA: %s"
          % "  ".join("toll=%g: %d archi (%d iterazioni)" % (t_, r, it)
                      for t_, (r, it) in sorted(raggi.items())))
    esito("### il cono del GLOBALE CAMBIA con la TOLLERANZA: NON e- una causalita-",
          len({r for r, _ in raggi.values()}) > 1,
          "### un orizzonte fissato da una MANOPOLA del risolutore "
          "ASSOMIGLIA a una causalita- e non lo e-")
    esito("### e oltre quel raggio e- ESATTAMENTE zero, non piccolo",
          per2[max(per2)] == 0.0,
          "### e- UNDERFLOW relativo allo stato, non una legge: "
          "### IO AVEVO SCRITTO IL CONTRARIO, e la misura mi ha corretto")
    return {"n": n, "dt": dt, "strati": len(ss), "op_arco": n_arco,
            "raggio_strato": 1, "raggio_locale": r1, "raggio_globale": r2,
            "per_d_locale": per1, "per_d_globale": per2, "d_max": max(d)}


# =====================================================================================
#   (D) NORMA ED ENERGIA -- la deriva, MISURATA
# =====================================================================================

def deriva(T, n=9, dt=0.01, passi=200):
    print()
    print("  (D) NORMA ED ENERGIA -- la deriva su `%d` passi, dt=%g" % (passi, dt))
    OSS = _modulo(os.path.join(_QUI, "osservatori", "prova_norma.py"), "_oss_norma")
    ii, jj = catena(n)
    ss = PA.strati(ii, jj)
    fuori = {}
    for nome, fun, kw in (("GLOBALE", PA.passo_globale, {}),
                          ("LOCALE", PA.passo_locale, {"gli_strati": ss})):
        st = stato_seme(n, 11)
        n0, e0 = OSS.misura(st), HAM.energia(st, ii, jj, T)
        for _ in range(passi):
            st = fun(st, ii, jj, dt, T, **kw)[0]
        n1, e1 = OSS.misura(st), HAM.energia(st, ii, jj, T)
        dn = abs(n1 - n0) / abs(n0)
        de = abs(e1 - e0) / max(abs(e0), 1e-300)
        fuori[nome] = {"norma0": n0, "norma1": n1, "deriva_norma": dn,
                       "energia0": e0, "energia1": e1, "deriva_energia": de}
        print("      %-8s norma %.15f -> %.15f   relativa %.3e" % (nome, n0, n1, dn))
        print("      %-8s energia %+.12f -> %+.12f   relativa %.3e" % ("", e0, e1, de))
        esito("`%s`: la norma si conserva entro `1e-10` relativo" % nome, dn < 1e-10,
              "### MISURATA, non asserita: `%.3e`" % dn)
    esito("### e la norma NON e- conservata AL BIT da nessuno dei due",
          fuori["GLOBALE"]["deriva_norma"] != 0.0
          or fuori["LOCALE"]["deriva_norma"] != 0.0,
          "il punto medio conserva gli invarianti quadratici in aritmetica ESATTA, "
          "non in virgola mobile -- e lo dico invece di promettere il bit")
    return fuori


# =====================================================================================
#   (E) `A8b` -- NESSUNA CACHE NASCOSTA
# =====================================================================================

def cache(T, n=9):
    print()
    print("  (E) `A8b` -- NESSUNA CACHE NASCOSTA FRA I PASSI")
    ii, jj = catena(n)
    moduli = [HAM, PA, ST] + list(T)
    st = stato_seme(n, 11)

    def tre_passi():
        s = st
        for _ in range(3):
            s = PA.passo_locale(s, ii, jj, 0.01, T)[0]
        return s
    guai, _ = PA.senza_cache(moduli, tre_passi)
    esito("nessun modulo di fisica si RICORDA niente fra i passi", guai == [],
          "`%d` moduli guardati: %s" % (len(moduli),
                                        ", ".join(sorted(m.__name__ for m in moduli))))

    # ### e il presidio DEVE scattare se qualcuno se lo ricorda.
    def sporca():
        HAM._cache_finta = 42
        return None
    g2, _ = PA.senza_cache(moduli, sporca)
    if hasattr(HAM, "_cache_finta"):
        del HAM._cache_finta
    esito("### DEVE scattare: un modulo che si RICORDA un valore",
          any("E- NATO durante il passo" in e for e in g2),
          "`A8b`: cio- che una legge ricorda va in `stato.py`, con la sua voce")


# =====================================================================================
#   (F) I SEI CASI CHE DEVONO FALLIRE -- in UN SOLO POSTO
# -------------------------------------------------------------------------------------
#   ### ⛔ **Il mandato li elenca per nome, e qui si ESEGUONO**: ciascuno si costruisce,
#   ### si passa al presidio che lo riguarda, e si verifica che scatti
#   ### ### **PER LA CHIAVE GIUSTA** -- non che scatti qualcosa.
#   ### ⚠ **Vivono anche nei collaudi dei loro strumenti**: qui stanno INSIEME, perche-
#   ### il mandato chiede ### **la catena**, e una catena si guarda intera.
# =====================================================================================

def sei_casi():
    import _genera as GEN
    import _presidi_era2 as PRE
    print()
    print("  (F) I SEI CASI CHE DEVONO FALLIRE -- la catena, in un solo posto")
    leggi, varia = PRE._tabella()
    vocab = {v["nome"]: v["tipo"] for v in varia}
    # ### un vocabolario con una variabile D-ARCO, per il caso `1`.
    voc_arco = dict(vocab, d="reale_arco")
    base = [x for x in leggi if x["tipo"] == "termine_nodo"][0]

    # --- `1` un TERMINE DI NODO CHE LEGGE UN VICINO
    l1 = dict(base, id="PROVA-VICINO", ambito=["psi", "d"])
    esito("`1` un `termine_nodo` che legge un VICINO (variabile d-ARCO nell-ambito)",
          any("NON VEDE I VICINI" in e or "e- di ARCO" in e or "arco" in e.lower()
              for e in SCH.valida_legge(l1, voc_arco)),
          "lo SCHEMA lo rifiuta PRIMA di generare, e i simboli dei vicini "
          "NON ESISTONO nell-ambiente")

    # --- `2` un'ESPRESSIONE CON `pos`
    l2 = dict(base, id="PROVA-POS", espressione="pos_x*psi_0c*psi_0")
    esito("`2` un-espressione che nomina `pos`",
          any("VIETATO" in e for e in GEN.controlla(l2, vocab)[0]),
          "`A17`: una posizione non entra nella fisica, e la decisione `9` e- APERTA")

    # --- `3` un FILE GENERATO RITOCCATO A MANO
    gen_finto = {base["id"]: ("termini/x.py", {"IMPRONTA": "ritoccato"})}
    esito("`3` un file generato RITOCCATO A MANO (impronta diversa dalla tabella)",
          any("TOCCATO A MANO" in e for e in PRE.pe2(leggi, gen_finto, varia)),
          "`P-E2`: si RIGENERA, non si corregge il file")

    # --- `4` una LEGGE SENZA VOCE o SENZA SCHEDA
    oss = [x for x in leggi if x["tipo"] == "osservatore"]
    l4a = dict(oss[0], id="PROVA-SENZA-VOCE", voce="")
    esito("`4a` un OSSERVATORE senza `voce`",
          any("voce" in e for e in SCH.valida_legge(l4a, vocab)),
          "un osservatore DICHIARA l-ID della voce MISURA che calcola")
    l4b = dict(base, id="PROVA-SENZA-SCHEDA", scheda="")
    esito("`4b` una LEGGE senza `scheda`",
          any("scheda" in e for e in SCH.valida_legge(l4b, vocab)),
          "una legge senza scheda NON SI GENERA")
    l4c = dict(oss[0], id="PROVA-VOCE-FINTA", voce="VOCE-CHE-NON-ESISTE")
    reg_l, reg_v = PRE._registri()
    esito("`4c` un OSSERVATORE con una `voce` che NON E- NELL-INDICE",
          any("NON E- NELL-INDICE" in e
              for e in PRE.pe7(reg_l, reg_v, leggi + [l4c], varia)),
          "### `P-E7`: un campo che nessuno risolve e- prosa con la forma di un dato")

    # --- `5` un OSSERVATORE CHE SCRIVE LO STATO
    p5 = os.path.join(_QUI, "osservatori", "_prova_scrive.py")
    try:
        io.open(p5, "w", encoding="utf-8", newline=NL).write(NL.join([
            "# -*- coding: utf-8 -*-",
            "LEGGE = 'PROVA-SCRIVE'",
            "TIPO = 'osservatore'",
            "",
            "",
            "def misura(st):",
            "    st['psi'][0, 0] += 1.0",
            "    return 0.0",
        ]) + NL)
        esito("`5` un OSSERVATORE CHE SCRIVE lo stato",
              any("ha SCRITTO" in e for e in PRE.pe5(verboso=False)),
              "`P-E5` lo misura AL BYTE: non si fida della regola scritta")
    finally:
        if os.path.exists(p5):
            os.remove(p5)

    # --- `6` un TERMINE CHE IMPORTA UN OSSERVATORE
    p6 = os.path.join(_QUI, "termini", "_prova_import.py")
    try:
        io.open(p6, "w", encoding="utf-8", newline=NL).write(
            "# -*- coding: utf-8 -*-" + NL + "import osservatori" + NL)
        esito("`6` un TERMINE che importa `osservatori`",
              any("NON E- FISICA" in e for e in PRE.pe4()),
              "`A17`: la fisica non puo- dipendere da chi la guarda")
    finally:
        if os.path.exists(p6):
            os.remove(p6)

    esito("NON deve scattare: tolti i finti, i presidi TACCIONO di nuovo",
          PRE.pe5(verboso=False) == [] and PRE.pe4() == [],
          "### i bracci di sopra scattavano per LORO, non per un residuo")


# =====================================================================================
#   IL GIRO
# =====================================================================================

def main():
    import _presidio
    _presidio.avvia(__file__)
    T = HAM.carica_termini()
    print("=" * 100)
    print("IL COLLAUDO DELLA CATENA -- lo schedulatore, i due candidati, IL CONO, i SEI casi")
    print("=" * 100)
    print("  i termini caricati: %s" % ", ".join(m.LEGGE for m in T))
    livelli(T)
    composizioni()
    c = cono(T)
    d = deriva(T)
    cache(T)
    sei_casi()
    print()
    print("=" * 100)
    print("IL COLLAUDO DELLA CATENA: %d su %d   %s"
          % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    print()
    print("  LA TAVOLA DEI DUE CANDIDATI -- ### SENZA SCEGLIERE (la scelta e- di Luca, nodo `INT`)")
    print("  %-10s %-14s %-18s %-18s %s" % ("", "cono (archi)", "deriva norma",
                                            "deriva energia", "costo (iterazioni/passo)"))
    for nome in ("GLOBALE", "LOCALE"):
        r = c["raggio_globale"] if nome == "GLOBALE" else c["raggio_locale"]
        print("  %-10s %-14s %-18.3e %-18.3e %s"
              % (nome, "%d su %d%s" % (r, c["d_max"],
                                       "  (ESATTO, dichiarato)" if nome == "LOCALE"
                                       else "  (NON dichiarato: artefatto)"),
                 d[nome]["deriva_norma"], d[nome]["deriva_energia"],
                 "dipende dalla TOLLERANZA" if nome == "GLOBALE"
                 else "x %d sotto-passi" % len(PA.composizione_locale(c["strati"]))))
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main())
