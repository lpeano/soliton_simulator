# -*- coding: utf-8 -*-
"""IL COLLAUDO DEL GENERATORE — **nei DUE VERSI, e col ramo END-TO-END.**

### ⛔ **STA IN UN MODULO SUO, e me lo ha detto `P-MOD` rifiutando il commit:**
`_genera.py` era arrivato a ### **`738` righe**, oltre il tetto di `700`, e il presidio
dice *<<oltre ### **SI DIVIDE, NON SI ALLUNGA**>>*. ### ⭐ **Alzare il tetto sarebbe
stato esattamente la manopola che `A1` vieta** — e un generatore e il suo collaudo
### **sono due responsabilita-**, che la mappa vuole ### **in UNA riga** ciascuna.
### **E- la stessa lezione di `grafo.py`, che ho imparato due punti prima.**

### ⭐ **E IL BRACCIO CHE CONTA E- IL RAMO END-TO-END DELLE DIMENSIONI.** Avevo messo
il controllo dimensionale dentro `valida_legge` leggendo le dimensioni ### **da
`variabili`** — ma il generatore gli passa `{nome: tipo}`, che ### **non le porta.**
### ⛔ **Il controllo SALTAVA IN SILENZIO, e i collaudi di unita- PASSAVANO TUTTI**
*(`34` su `34`)*, perche- provavano ### **la funzione** e non ### **il generatore.**
### **L-ho visto solo rompendo la tabella a posta e guardando il codice d-uscita: era
`0`.**
"""
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(_QUI, "leggi"))
sys.path.insert(0, os.path.join(RADICE, "csv"))

import _genera as GEN                                        # noqa: E402

GENERA = os.path.join(_QUI, "_genera.py")

# ### ⛔ **I NOMI SI PRENDONO DAL GENERATORE, non si riscrivono:** un secondo elenco
# ### ### **divergerebbe** -- ed e- lo stesso motivo per cui la tabella e- l-unica fonte.
_NOMI = [n for n in dir(GEN) if not n.startswith("__")]
for _n in _NOMI:
    globals().setdefault(_n, getattr(GEN, _n))


def collaudo():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-66s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    VOC = {"psi": "complesso_c2_nodo", "w": "reale_arco"}

    def lg(**kw):
        d = {"id": "PROVA-X", "tipo": "termine_nodo",
             "espressione": "psi_0c*psi_0 + psi_1c*psi_1",
             "ambito": ["psi"], "parametri": {}, "assiomi": [], "prova": True,
             "scheda": "s"}
        d.update(kw)
        return d

    print("=" * 100)
    print("IL COLLAUDO DEL GENERATORE -- e i casi che DEVONO fallire")
    print("=" * 100)
    g, e = controlla(lg(), VOC)
    esito("il caso SANO: i simboli sono dentro l-ambiente", g == [] and e is not None)
    # ### ⛔ **UN TERMINE DI NODO CHE LEGGE UN VICINO.**
    g, _e = controlla(lg(espressione="psi_i_0c*psi_j_0"), VOC)
    esito("### DEVE rifiutare: un `termine_nodo` che nomina `psi_i`/`psi_j` (il VICINO)",
          any("NON VEDE I VICINI" in x for x in g),
          "i simboli dei vicini NON ESISTONO nell-ambiente di un termine di nodo")
    # ### ⚠ **E QUESTO BRACCIO L-HO CORRETTO, perche- la mia espressione era SBAGLIATA:**
    # ### usavo `psi_i_0c*psi_j_0`, che e- ### **NON HERMITIANA** -- e fino a che il
    # ### controllo di realta- non c-era ### **passava.** ### **Il braccio provava
    # ### l-ambito con un-espressione che un`H` non puo- avere.**
    esito("NON deve rifiutare: un `termine_arco` che legge i due capi, CON il `c.c.`",
          controlla(lg(tipo="termine_arco",
                       espressione="psi_i_0c*psi_j_0 + psi_j_0c*psi_i_0"),
                    VOC)[0] == [],
          "un termine d-arco PUO- leggere i due capi: e- il suo mestiere")
    # ### ⛔ **`pos` NELL-ESPRESSIONE.**
    g, _e = controlla(lg(espressione="psi_0c*psi_0 + pos_x"), VOC)
    esito("### DEVE rifiutare: un-espressione che nomina `pos_x` (`A17`)",
          any("VIETATO" in x for x in g))
    # ### ⛔ **I RAMI: un limite e- una LEGGE** *(punto `2`)*.
    for _e_ramo, _nome in (("Max(psi_0c*psi_0, 0)", "Max"),
                           ("Abs(psi_0)*psi_0c", "Abs"),
                           ("Piecewise((psi_0c*psi_0, True))", "Piecewise"),
                           ("sign(psi_0c*psi_0)", "sign"),
                           ("floor(psi_0c*psi_0)", "floor")):
        g, _x = controlla(lg(espressione=_e_ramo), VOC)
        esito("### DEVE rifiutare: un RAMO nell-espressione (`%s`)" % _nome,
              any("A11" in x for x in g),
              "un limite e- una LEGGE, non una toppa; e non si TARA: si DERIVA")
    # ### ✅ **E NON deve rifiutare le DUE leggi VERE**, altrimenti il braccio
    # ### ### **sarebbe vero per costruzione**: una lista di nomi vietati che
    # ### ### **rifiuta tutto** non distingue niente.
    _leggi_vere, _varia_vere = carica()
    _voc_vero = {v["nome"]: v["tipo"] for v in _varia_vere}
    for _lg in _leggi_vere:
        esito("NON deve rifiutare: la legge vera `%s`" % _lg["id"],
              controlla(_lg, _voc_vero)[0] == [],
              "### se rifiutasse, la lista dei rami sarebbe TROPPO LARGA")
    # ### ⚠ **E i confini di parola: `max_nodi` CONTIENE `Max`?** No, e si prova.
    g, _x = controlla(lg(espressione="psi_0c*psi_0"), VOC)
    esito("### i CONFINI DI PAROLA: `Abs` NON si trova dentro `Absurdo`",
          SCH.rami_vietati("Absurdo*psi_0") == []
          and SCH.rami_vietati("Abs(psi_0)") == ["Abs"],
          "### in questo repo i confini di parola sono stati dimenticati QUATTRO volte")
    # ### ⛔ **UN SIMBOLO FUORI DALL-AMBITO.**
    g, _e = controlla(lg(espressione="psi_0c*psi_0 + w"), VOC)
    esito("### DEVE rifiutare: un simbolo FUORI dall-ambito (`w` non e- dichiarato)",
          any("FUORI DALL-AMBITO" in x for x in g))
    # ### ⭐ **LA DERIVATA: Wirtinger, e si verifica a MANO su un caso noto.**
    import sympy
    _g, e = controlla(lg(), VOC)
    d = derivata(e, ["psi_0c", "psi_1c"])
    esito("la derivata di `psi_0c*psi_0 + psi_1c*psi_1` rispetto a `psi_0c` e- `psi_0`",
          d["psi_0c"] == sympy.Symbol("psi_0"),
          "Wirtinger: `psi` e `psi*` sono simboli INDIPENDENTI")
    _g, e2 = controlla(lg(espressione="(psi_0c*psi_0 + psi_1c*psi_1)**2"), VOC)
    d2 = derivata(e2, ["psi_0c"])
    atteso = 2 * sympy.Symbol("psi_0") * (sympy.Symbol("psi_0c") * sympy.Symbol("psi_0")
                                          + sympy.Symbol("psi_1c") * sympy.Symbol("psi_1"))
    esito("e la derivata del QUADRATO e- `2*psi_0*(psi_0c*psi_0 + psi_1c*psi_1)`",
          sympy.simplify(d2["psi_0c"] - atteso) == 0)
    # ### ⛔ **LA REALTA- DELL-ESPRESSIONE, e il difetto lo ha trovato il guardiano:** il
    # ### modulo faceva `np.real(np.sum(_e))` e ### **scartava in SILENZIO la parte
    # ### immaginaria** *(`A8`)*. ### **Il controllo va SULLA TABELLA, simbolicamente.**
    VA = {"psi": "complesso_c2_nodo"}
    _g, e_h = controlla(lg(tipo="termine_arco",
                           espressione="-K*(psi_i_0c*psi_j_0 + psi_i_1c*psi_j_1 "
                                       "+ psi_j_0c*psi_i_0 + psi_j_1c*psi_i_1)",
                           parametri={"K": {"valore": 1.0, "origine": "prova"}}), VA)
    esito("NON deve rifiutare: `PROVA-HOPPING` -- il bilineare CON il `c.c.` E- reale",
          _g == [] and e_h is not None,
          "`expr - conj(expr)` si riduce a zero")
    _g2, _e2 = controlla(lg(espressione="(g/2)*(psi_0c*psi_0 + psi_1c*psi_1)**2",
                            parametri={"g": {"valore": 0.5,
                                             "origine": "prova"}}), VA)
    esito("NON deve rifiutare: `PROVA-LOCALE` -- `(g/2)(psi^dag psi)^2` E- reale",
          _g2 == [])
    # ### ⛔ **IL CASO CHE IL GUARDIANO NOMINA: il bilineare SENZA il `c.c.`**
    _g3, _e3 = controlla(lg(tipo="termine_arco", espressione="-K*psi_i_0c*psi_j_0",
                            parametri={"K": {"valore": 1.0,
                                             "origine": "prova"}}), VA)
    esito("### DEVE rifiutare: `-K*psi_i_0c*psi_j_0` SENZA il `c.c.` (non hermitiano)",
          any("NON E- REALE" in x for x in _g3),
          "un `H` non hermitiano NON conserva la norma, e `np.real()` lo scarterebbe "
          "IN SILENZIO")
    # ### ⚠ **E un termine con un `i` davanti NON e- reale**, nemmeno col `c.c.`:
    # ### ### **il braccio lo prova**, perche- <<col c.c.>> non basta da solo.
    _g4, _e4 = controlla(lg(espressione="I*(psi_0c*psi_0 + psi_1c*psi_1)"), VA)
    esito("### DEVE rifiutare: `I*(psi^dag psi)` -- immaginario PURO",
          any("NON E- REALE" in x for x in _g4),
          "<<col c.c.>> non basta: conta che `expr - conj(expr)` sia ZERO")
    # ### ⛔ **L-IMPRONTA non dipende dall-ORDINE delle chiavi.**
    a = dict(lg())
    b = {k: a[k] for k in reversed(list(a))}
    esito("l-impronta NON dipende dall-ordine delle chiavi",
          impronta(a) == impronta(b),
          "riordinare lo yaml NON deve rifiutare ogni file")
    c = dict(a, espressione=a["espressione"] + " + 0")
    esito("### e CAMBIA se l-espressione cambia", impronta(a) != impronta(c))
    print("=" * 100)
    # ===================================================================================
    #   ### ⭐ **IL RAMO END-TO-END DELLE DIMENSIONI** *(punto `2`)*
    # ===================================================================================
    # ### ⛔ **ESISTE PERCHE- UN MIO ERRORE L-HA RESO NECESSARIO**, ed e- scritto nel
    # ### docstring: il controllo dimensionale ### **saltava in silenzio** e i collaudi
    # ### di unita- ### **passavano tutti.** ### **Provare la funzione non prova il
    # ### generatore: fra le due c-e- LA FORMA in cui le dimensioni gli arrivano.**
    import hashlib
    import subprocess
    TAB = os.path.join(_QUI, "leggi", "leggi.yaml")
    b0 = io.open(TAB, "rb").read()
    sha0 = hashlib.sha1(b0).hexdigest()
    print()
    print("  (f) IL RAMO END-TO-END: il GENERATORE rifiuta una dimensione incoerente?")
    try:
        testo = b0.decode("utf-8")
        # ### ⛔ **LA RIGA SI TROVA, NON SI CONTA:** un numero di riga
        # ### ### **shifta** al primo commento in piu- -- e- il par. `2`.
        pezzi = testo.split("      K:" + NL)
        assert len(pezzi) == 2, "### `K:` non compare una volta sola nella tabella"
        testa, coda = pezzi
        assert coda.count("dimensione: E^1") >= 1, "### `K` non ha una dimensione `E^1`"
        io.open(TAB, "w", encoding="utf-8", newline="").write(
            testa + "      K:" + NL
            + coda.replace("dimensione: E^1", "dimensione: E^2", 1))
        r = subprocess.run([sys.executable, GENERA], cwd=RADICE, capture_output=True,
                           text=True, encoding="utf-8", errors="replace")
        fuori = (r.stdout or "") + (r.stderr or "")
        esito("### DEVE scattare: il GENERATORE rifiuta `K` di dimensione `E^2`",
              r.returncode != 0 and "NON E- UN TERMINE DI `H`" in fuori,
              "codice %d: ### e- il braccio che vede un controllo SALTATO IN SILENZIO -- "
              "i 34 collaudi dello schema passavano mentre il generatore accettava"
              % r.returncode)
    finally:
        io.open(TAB, "wb").write(b0)
        subprocess.run([sys.executable, GENERA], cwd=RADICE, capture_output=True)
    esito("### e la tabella e- tornata IDENTICA AL BYTE",
          hashlib.sha1(io.open(TAB, "rb").read()).hexdigest() == sha0,
          "`%s`: ### un collaudo che lascia danno non e- un collaudo" % sha0[:8])
    print()
    print("IL COLLAUDO DEL GENERATORE: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1]
             else "### QUALCUNO FALLISCE"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1



if __name__ == "__main__":
    import _presidio
    _presidio.avvia(__file__)
    sys.exit(collaudo())
