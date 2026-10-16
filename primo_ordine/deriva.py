# -*- coding: utf-8 -*-
r"""LA DERIVA DI `E` SUL TICK INTERO — **rimisurata, perche' il numero vecchio era ORFANO.**

> ### ⛔ **PERCHE' QUESTO FILE ESISTE.** Nel task history del `2026-10-12` avevo scritto che
> a tempo totale fisso l'ultimo dimezzamento di `dtau` da' **rapporto `4.20`**, *«la firma
> dell'esponente `2`»*. ### **NESSUNO SCRIPT COMMITTATO PRODUCEVA QUEL NUMERO**, e il
> mandato del `2026-10-13` lo ha poi citato come *«tua misura»* costruendoci sopra una
> richiesta. ### ⚠ **Un numero senza provenienza che viene letto come una misura orienta
> il lavoro**, ed e' cio' che `L-NUMERI` vieta.

## ⛔ E LA PREVISIONE SCRITTA PRIMA DEI NUMERI DICE CHE QUELLA CONCLUSIONE E' FALSA

Il pezzo lineare **non e'** il flusso di un'hamiltoniana per un tempo `dtau`. In
`primo_ordine/composizione.py`, che e' **generata dalla tabella**, ### **quattro pezzi su
sette non dipendono da `dtau`:** il Grover e' **un'involuzione** `(2/d)J - I`, lo
spostamento e' **una permutazione con trasporto**, e le due camminate del vuoto sono le
stesse cose sul vuoto. ### **Solo la moneta di spin e il flusso di saturazione scalano.**

### ⛔ **Quindi a `dtau -> 0` il tick NON tende all'identita':** e' **un cammino quantistico
a tempo discreto**, non un integratore. ### **E allora <<`E` conservata a `O(dtau^2)`>> non
puo' voler dire <<per tick>>.**

## ✅ CIO' CHE SI SA DI ESATTO, e che questo file separa invece di mescolare

| | il termine | che cosa gli fa il tick |
|---|---|---|
| `1` | `Re<psi\|W psi>` | ### ✅ **conservato ESATTAMENTE dal pezzo lineare:** `Re<W psi\|W (W psi)> = Re<psi\|W psi>` per **qualunque** `W` unitario -- **un'identita'** |
| `2` | `somma_k Lambda_k G(h_k/Lambda_k)` | ### ⛔ **cambia**, perche' il pezzo lineare cambia `h_k` e la camminata del vuoto cambia `Lambda_k` |

### ⭐ **E' per questo che si misurano SEPARATI:** *«`E` deriva»* senza dire **in quale dei
due termini** ### **non dice dove cercare.**

Gira con:  python primo_ordine/deriva.py --scrivi
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)

import composizione as CM                                     # noqa: E402
import energia as EN                                          # noqa: E402
import deriva_referto as RF                                   # noqa: E402
import saturazione as SAT                                     # noqa: E402

# ### ⛔ **LA LEGGE -> L'OPERATORE, e NON e' una mia scelta:** la lista delle leggi e il
# ### loro ordine stanno in `composizione.py`, che e' ### **GENERATA dalla tabella**; qui
# ### c'e' solo ### **il nome con cui il motore registra ciascuna.**
# ### ⚠ **E un `id` che non e' in questa mappa FERMA**, invece di essere saltato in
# ### silenzio: ### **un pezzo del tick che non gira e' un tick diverso.**
OPERATORE = {
    # ### ⭐⭐ **IL FLUSSO CHE GIRA dal `2026-10-15`** *(decisione di Luca)*:
    # ### `CAMM-MATERIA-VUOTO` ### **sostituisce** `CAMM-SATURAZIONE` nell-ordine di
    # ### composizione. ### ⚠ **La riga della saturazione RESTA**, perche- la legge
    # ### resta in tabella e il suo operatore esiste: ### **una riga tolta da qui
    # ### farebbe ALZARE il tick se qualcuno la rimettesse nell-ordine**, invece di
    # ### girare.
    "CAMM-MATERIA-VUOTO": ("CAMM-MATERIA-VUOTO", False),
    "CAMM-SATURAZIONE": ("CAMM-SATURAZIONE", False),
    "CAMM-MONETA-SPIN": ("moneta_spin", True),
    "CAMM-GROVER": ("grover", False),
    "CAMM-SPOSTAMENTO": ("spostamento_trasporto", False),
    "CAMM-GROVER-VUOTO": ("grover_scalare", False),
    "CAMM-SPOSTAMENTO-VUOTO": ("spostamento_scalare", False),
}
def tick(st, mot, par):
    """### UN tick, ### **nell'ordine della tabella e non in uno mio.**"""
    mot.apri_tick()
    for idl, frazione, _tipo in CM.ORDINE:
        nome, vuole_par = OPERATORE.get(idl, (None, None))
        assert nome, (
            "la legge `%s` e' nell'ordine di composizione e NON e' in `OPERATORE`:"
            " ### **un pezzo del tick che non gira e' un tick diverso**, e saltarlo in"
            " silenzio sarebbe misurare un'altra cosa" % idl)
        mot.operatori[nome](st, par if vuole_par else {}, frazione)
    mot.chiudi_tick()


def due_termini(st, mot, par):
    r"""### `(primo, vuoto)`: ### **i due termini di `E`, SEPARATI.**

    ### ⛔ **Separati e non sommati, perche' sommati non dicono dove cercare:** uno e'
    conservato **per identita'**, l'altro no — e ### **<<`E` deriva>> senza dire quale dei
    due e' una misura che non si puo' usare.**
    """
    eh = EN.densita_estremita(st, mot, par,
                              mot._b("dv_h", (st["psi_h"].shape[0],), float))
    primo = float(np.sum(eh))
    ek = EN.densita_nodo(st, mot, mot._b("dv_k", (mot.inc.n,), float))
    return primo, float(np.sum(ek))


NORME = ("locale", "globale")


def scena(nn, seme, dtau, lunghezza=0, norma="locale", vuoto_modulo=1.0,
          su2=False):
    """### L'anello di `nn` nodi, ### **e `lunghezza` sceglie la LUNGHEZZA D'ONDA.**

    ### ⚠ **`lunghezza = 0` vuol dire CASUALE** *(il caso piu' ruvido)*; un intero `L`
    mette una **modulazione di periodo `L` nodi** sullo spinore, cioe' ### **uno stato
    LISCIO su quella scala.** ### ⛔ **E serve per la misura per lunghezza d'onda**, dove
    uno stato casuale ### **non ha UNA lunghezza d'onda.**

    ## ⛔ `norma` NON E' UN DETTAGLIO: DECIDE SE LA SATURAZIONE E' ACCESA

    ### ⚠ **`globale`** *(`||psi|| = 1` su tutto il grafo)* **fa `h_k/Lambda_k ~ 1/(2m)`**,
    e `G(x) = x - arctan x` va come `x^3/3`: su un anello di `16` nodi il termine del vuoto
    vale ### **`~1e-5`**, cioe' ### **la saturazione e' PRATICAMENTE SPENTA.**
    ### ⛔ **Misurare la sua sorgente la' sarebbe un FALSO-ZERO**, ed e' il motivo per cui
    il collaudo della saturazione **guarda `max |h|`** invece di fidarsi.

    ### ✅ **`locale`** *(ampiezza di ordine `1` PER ESTREMITA', nessuna normalizzazione
    globale)* **tiene `h_k/Lambda_k` di ordine `1`**, e ### **e' anche l'unico modo di
    confrontare taglie diverse A STATO LOCALE UGUALE** -- che e' cio' che chiede la misura
    dell'estensivita'.

    ### ⭐ **E LE DUE SI MISURANO ENTRAMBE**, perche' *«la deriva e' `1e-5`»* senza dire
    **in quale regime** ### **non e' una misura.**
    """
    assert norma in NORME, (
        "`norma` vale `locale` o `globale`, e NON ha un valore di comodo: decide se la"
        " saturazione e' accesa, cioe' ### **se la misura ha materia** (%r)" % (norma,))
    import incidenza as IN
    import motore as MO
    import stato as ST
    ii = np.arange(nn, dtype=IN.INDICE)
    jj = (ii + 1) % nn
    inc = IN.Incidenza(ii, jj, nn, capacita=nn)
    r = np.random.default_rng(seme)
    nv = r.normal(size=(2 * inc.m, 3))
    nv /= np.linalg.norm(nv, axis=1).reshape(-1, 1)
    U = np.zeros((inc.m, 2, 2), dtype=complex)
    for a in range(inc.m):
        X = r.normal(size=(2, 2)) + 1j * r.normal(size=(2, 2))
        Qm, _ = np.linalg.qr(X)
        if su2:
            # ### ⭐ **`det U = 1`, e NON e- un abbellimento: e- CIO- CHE SERVE ALLA
            # ### `C`.** La `C` antilineare chiede `sigma_y U* sigma_y^-1 = U`, che vale
            # ### ### **se e solo se `U` sta in `SU(2)`.** ### ⛔ **Misurato: con `U(2)`
            # ### generico `|CW - WC| = 4.33` su scala `2.76`; con `SU(2)` fa `8.0e-16`.**
            # ### ⚠ **OFF di default**, perche- la misura della deriva e- ### **gia-
            # ### committata con `U(2)`** e un default che cambia ### **cambierebbe un
            # ### numero senza che nessuno l-abbia chiesto.**
            Qm = Qm / np.sqrt(np.linalg.det(Qm))
        U[a] = Qm
    st = ST.nuovo(nn, inc.m)
    if lunghezza <= 0:
        st["psi_h"][...] = (r.normal(size=st["psi_h"].shape)
                            + 1j * r.normal(size=st["psi_h"].shape))
    else:
        # ### un'onda piana sui NODI: ### **liscia su scala `lunghezza`**
        k = 2.0 * np.pi / float(lunghezza)
        fase = np.exp(1j * k * inc.nodo.astype(float))
        st["psi_h"][:, 0] = fase
        st["psi_h"][:, 1] = 0.5 * fase
    if norma == "globale":
        st["psi_h"] /= np.linalg.norm(st["psi_h"])
    # ### ⭐ **`vuoto_modulo` E- LA MANOPOLA DEL REGIME, e non una costante nuova:**
    # ### `Lambda_k = somma |phi_h|^2` sulle estremita- del nodo, quindi `x = h/Lambda`
    # ### scala come ### **`1 / vuoto_modulo^2`.** ### ⚠ **Un vuoto PIU- DEBOLE porta
    # ### `x` verso `1`, cioe- ### ACCENDE la saturazione** -- ed e- l-unico modo di
    # ### misurarla ### **dove lavora.**
    st["phi_h"][...] = (float(vuoto_modulo)
                        * np.exp(1j * r.random(st["phi_h"].shape) * 2.0 * np.pi))
    mot = MO.Motore(inc, MO.Geometria(nv, U), st, np.full(nn, dtau), "numpy")
    return inc, mot, st, {"eps": 0.5}


def satura(st, mot):
    """### `max_k |h_k / Lambda_k|`: ### **la prova che la saturazione e' ACCESA.**

    ### ⛔ **Senza questo numero ogni misura su `N` e' un FALSO-ZERO sospetto:** a
    `h/Lambda ~ 0` si ha `G ~ x^3/3 ~ 0`, e ### **una sorgente nulla non direbbe che `N`
    non ha sorgente, direbbe che `N` non c'era.**
    """
    h = mot.elicita(st)
    lam = mot.densita_vuoto(st)
    buoni = lam > 0.0
    return float(np.max(np.abs(h[buoni] / lam[buoni]))) if np.any(buoni) else 0.0


def corri(nn, dtau, ticks, seme=7, lunghezza=0, ogni=1, norma="locale",
          vuoto_modulo=1.0, su2=False):
    """### Fa girare `ticks` tick e rende ### **le tre serie: `E`, primo, vuoto.**"""
    inc, mot, st, par = scena(nn, seme, dtau, lunghezza, norma, vuoto_modulo, su2)
    sat = satura(st, mot)
    e1, e2 = due_termini(st, mot, par)
    serie = [(0, e1 + e2, e1, e2)]
    for t in range(1, ticks + 1):
        tick(st, mot, par)
        if (t % ogni) == 0 or t == ticks:
            e1, e2 = due_termini(st, mot, par)
            serie.append((t, e1 + e2, e1, e2))
    return np.asarray(serie, dtype=float), inc, mot, st, par, sat


def m0(nn=16, tempo=2.0, dimezzamenti=5, dtau0=0.2, seme=7, norma="locale"):
    """### `D-ENERGIA:M0` — **la deriva a TEMPO TOTALE FISSO, su `n` dimezzamenti.**

    ### ⛔ **A tempo totale fisso, non a tick fissi:** dimezzando `dtau` i tick
    **raddoppiano**, ed e' ### **esattamente il confronto che il numero orfano
    dichiarava.**
    """
    righe = []
    sat = 0.0
    scale = (0.0, 0.0)
    for i in range(dimezzamenti):
        dt = dtau0 / (2 ** i)
        ticks = int(round(tempo / dt))
        serie, _i, _m, _s, _p, sat = corri(nn, dt, ticks, seme=seme,
                                           ogni=max(1, ticks), norma=norma)
        d = serie[-1] - serie[0]
        scale = (abs(serie[0, 2]), abs(serie[0, 3]))
        righe.append((dt, ticks, abs(d[1]), abs(d[2]), abs(d[3])))
    # ### ⚠ **E LE SCALE TORNANO INSIEME AI SALTI:** ### **`1e-5` senza la scala non e'
    # ### una misura**, e qui la scala del vuoto e- ### **proprio cio- che il regime
    # ### cambia.**
    return righe, sat, scale


def rapporti(righe, col):
    """### I rapporti fra dimezzamenti consecutivi. ### **`4` = esponente `2`.**"""
    fuori = []
    for a, b in zip(righe[:-1], righe[1:]):
        fuori.append(a[col] / b[col] if b[col] > 0 else float("inf"))
    return fuori


def escursioni(serie):
    """### `(somma, primo, vuoto)`: ### **`max - min` lungo la corsa**, non `fine - inizio`.

    ### ⛔ **E la differenza conta:** `fine - inizio` di un'oscillazione puo' fare **zero**
    anche quando l'escursione e' grande. ### **L'escursione e' cio' che la verifica esterna
    ha misurato sul banco**, e si misura la stessa cosa per poter confrontare.
    """
    return tuple(float(serie[:, c].max() - serie[:, c].min()) for c in (1, 2, 3))


def scansione(moduli, nn=16, dtau=0.25, ticks=400, seme=7, su2=False):
    """### **LA SCANSIONE IN `x = |h_k|/Lambda_k`**, dal regime vacuo a quello che LAVORA.

    > **Mandato della verifica esterna, 2026-10-13:** *«Un `M0` nel regime `x ~ 1e-3` e'
    > VACUO: non distingue "`E` conservata" da "il termine non c'e'".»*

    ### ⛔ **ED E' LO STESSO DIFETTO CHE AVEVO TROVATO IO un'ora prima**, misurando: col
    `psi` normalizzato su tutto il grafo `x ~ 1/(2m)`, e `G(x) = x - arctan x` va come
    `x^3/3`. ### **Il termine del vuoto valeva `~1e-5`: la saturazione era SPENTA.**

    ### ⭐ **Per ogni punto si stampa:** `x`, **la scala di ciascun termine**, la loro
    **escursione** e quella **della somma**, e le escursioni **RELATIVE alla scala**.
    ### ⚠ **Perche' un'escursione assoluta senza la sua scala non dice se e' grande.**
    """
    righe = []
    for f in moduli:
        serie, _i, mot, st, _p, _s = corri(nn, dtau, ticks, seme=seme,
                                           ogni=max(1, ticks // 100),
                                           vuoto_modulo=f, su2=su2)
        # ### `x` si rimisura SULLO STATO INIZIALE, ricostruito: la corsa l-ha cambiato
        _i2, mot2, st2, _p2 = scena(nn, seme, dtau, 0, "locale", f, su2)
        h = mot2.elicita(st2)
        lam = mot2.densita_vuoto(st2)
        buoni = lam > 0.0
        x_max = float(np.max(np.abs(h[buoni] / lam[buoni]))) if np.any(buoni) else 0.0
        x_med = float(np.mean(np.abs(h[buoni] / lam[buoni]))) if np.any(buoni) else 0.0
        esc = escursioni(serie)
        sc = (abs(float(serie[0, 2])), abs(float(serie[0, 3])))
        # ### ⛔ **LE SCALE NATURALI, e non solo il valore iniziale:** il valore
        # ### iniziale del primo termine puo- capitare ### **vicino a uno zero**, e
        # ### allora un-escursione divisa per lui ### **sembra enorme senza esserlo.**
        # ### ⭐ `|Re<psi|W psi>| <= ||psi||^2` sempre, quindi ### **`||psi||^2` E- la
        # ### scala del primo termine**; e per il vuoto, siccome
        # ### `Lambda G(h/Lambda) -> h - (pi/2) Lambda sign(h)` a grande `x`, la scala e-
        # ### ### **`somma|h| + (pi/2) somma Lambda`.**
        nat1 = float(np.sum(np.abs(st2["psi_h"]) ** 2))
        nat2 = float(np.sum(np.abs(h)) + SAT.PIMEZZI * np.sum(lam))
        righe.append({"modulo": f, "x_max": x_max, "x_medio": x_med,
                      "nat_primo": nat1, "nat_vuoto": nat2,
                      "relnat_primo": esc[1] / max(nat1, 1e-300),
                      "relnat_vuoto": esc[2] / max(nat2, 1e-300),
                      "relnat_somma": esc[0] / max(nat1 + nat2, 1e-300),
                      "scala_primo": sc[0], "scala_vuoto": sc[1],
                      "esc_somma": esc[0], "esc_primo": esc[1], "esc_vuoto": esc[2],
                      "rel_primo": esc[1] / max(sc[0], 1e-300),
                      "rel_vuoto": esc[2] / max(sc[1], 1e-300),
                      "e0": float(serie[0, 1])})
    return righe


def lambda_sotto_vuoto(nn=16, seme=7, uniforme=True):
    """### `max_k |Delta Lambda_k|` sotto la **sola camminata del vuoto.**

    ### ⛔ **PERCHE' QUESTA MISURA ESISTE: la decomposizione di `(c)` dava numeri
    IDENTICI** col vuoto che cammina e senza, a tutte le cifre. ### ⚠ **Un'identita' a
    tutte le cifre non si spiega con <<e' piccolo>>: o la si capisce, o e' un difetto.**

    ### ⭐ **E la si capisce:** su un grafo **`2`-regolare** il Grover scalare e'
    `(2/2)(phi_a + phi_b) - phi_h`, cioe' **uno SCAMBIO**, e lo spostamento e' una
    **permutazione**. ### **Con `|phi|` UNIFORME le due cose permutano moduli tutti
    uguali, quindi `Lambda_k` E' ESATTAMENTE INVARIANTE** — e la camminata del vuoto
    ### **non porta energia di vuoto da nessuna parte.**

    ### ⛔ **Quindi la decomposizione di `(c)` e' VACUA PER QUESTO VUOTO**, e va detto:
    `uniforme=False` e' il **controllo positivo** che lo prova, con `|phi|` **non
    uniforme**.
    """
    import incidenza as IN
    import motore as MO
    import stato as ST
    ii = np.arange(nn, dtype=IN.INDICE)
    jj = (ii + 1) % nn
    inc = IN.Incidenza(ii, jj, nn, capacita=nn)
    r = np.random.default_rng(seme)
    nv = r.normal(size=(2 * inc.m, 3))
    nv /= np.linalg.norm(nv, axis=1).reshape(-1, 1)
    U = np.zeros((inc.m, 2, 2), dtype=complex)
    U[:, 0, 0] = 1.0
    U[:, 1, 1] = 1.0
    st = ST.nuovo(nn, inc.m)
    st["psi_h"][...] = 1.0
    moduli = (np.ones(2 * inc.m) if uniforme
              else (0.5 + r.random(2 * inc.m)))
    st["phi_h"][...] = moduli * np.exp(1j * r.random(2 * inc.m) * 2.0 * np.pi)
    mot = MO.Motore(inc, MO.Geometria(nv, U), st, np.full(nn, 0.2), "numpy")
    prima = mot.densita_vuoto(st).copy()
    mot.apri_tick()
    mot.operatori["grover_scalare"](st, {}, 1)
    mot.operatori["spostamento_scalare"](st, {}, 1)
    mot.chiudi_tick()
    return float(np.max(np.abs(mot.densita_vuoto(st) - prima)))


def secolare(serie):
    """### `(pendenza, ampiezza, rapporto)`: ### **deriva SECOLARE o OSCILLAZIONE?**

    ### ⭐ **Il criterio e' un rapporto e non un occhio:** si adatta una retta a `E(t)` e
    si confronta la **variazione che la retta spiega** con l'**ampiezza dei residui**.
    ### ✅ **`rapporto >> 1` vuol dire SECOLARE** *(la retta spiega quasi tutto)*;
    ### ⛔ **`rapporto << 1` vuol dire OSCILLANTE** *(la retta non spiega niente, e il
    segnale e' tutto nei residui)*.
    """
    t = serie[:, 0]
    e = serie[:, 1] - serie[0, 1]
    pend, quota = np.polyfit(t, e, 1)
    spiegata = abs(pend) * (t[-1] - t[0])
    residui = e - (pend * t + quota)
    amp = float(np.max(residui) - np.min(residui))
    return (float(pend), amp,
            spiegata / amp if amp > 0 else float("inf"))


def sorgente_per_nodo(nn=16, dtau=0.2, seme=7, norma="locale", vuoto_cammina=True,
                      vuoto_modulo=1.0):
    """### `(c)` — **LA SORGENTE PER NODO sul tick INTERO, con `N` acceso.**

    `s_k = Delta E_k - (div J)_k`, dove `J` e' la corrente locale **costruita** per il
    pezzo lineare *(`primo_ordine/corrente.py`)*, valutata sullo stato che **entra** nel
    pezzo lineare, cioe' **dopo il primo mezzo flusso.**

    ### ⛔ **E `N` NON ATTRAVERSA**, perche' il suo generatore dipende solo da grandezze
    di nodo: ### **la sua corrente e' ZERO, e cio' che resta nel bilancio e' la
    SORGENTE.**

    ### ⚠ **E si misura PER NODO, come il mandato chiede**, non solo in totale: una
    sorgente che in totale fa zero ### **puo' essere grande su ogni nodo.**

    ## ⛔ `vuoto_cammina` SEPARA DUE COSE CHE IL RESIDUO MESCOLA

    ### ⚠ **Il mio `J` copre il pezzo lineare DELLO SPINORE, e nient'altro.** Ma la
    **camminata del vuoto** *(`CAMM-GROVER-VUOTO`, `CAMM-SPOSTAMENTO-VUOTO`)* muove `phi`
    fra i nodi, quindi cambia `Lambda_k`: ### **trasferisce energia di vuoto fra nodi, e
    quello e' una CORRENTE CHE MANCA, non una sorgente.**
    ### ⛔ **Chiamare <<sorgente>> un trasferimento che non ho modellato sarebbe
    attribuire al fenomeno un buco del mio strumento**, ed e' lo stesso errore della
    candidata di ieri. ### ✅ **Quindi si misura nei due modi, e la differenza DICE quanto
    e' l'uno e quanto l'altro.**
    """
    import corrente as CO
    inc, mot, st, par = scena(nn, seme, dtau, norma=norma,
                              vuoto_modulo=vuoto_modulo)
    sat = satura(st, mot)
    prima = EN.per_nodo(st, mot, par).copy()
    # ### il PRIMO MEZZO FLUSSO, poi si fotografa lo stato che entra nel pezzo lineare
    mot.apri_tick()
    mot.operatori["CAMM-SATURAZIONE"](st, {}, 0.5)
    mezzo = {k: (v.copy() if hasattr(v, "copy") else v) for k, v in st.items()}
    # ### la corrente del pezzo lineare, costruita SU QUELLO STATO
    Q = CO.forma_quadratica(mezzo, mot, par)
    J, portata, dia = CO.instrada(Q, inc, CO.x_da_psi(mezzo["psi_h"]))
    # ### e il resto del tick, ### **saltando la camminata del vuoto se richiesto**
    salta = () if vuoto_cammina else ("CAMM-GROVER-VUOTO", "CAMM-SPOSTAMENTO-VUOTO")
    for idl, frazione, _tipo in CM.ORDINE[1:]:
        if idl in salta:
            continue
        nome, vuole_par = OPERATORE[idl]
        mot.operatori[nome](st, par if vuole_par else {}, frazione)
    mot.chiudi_tick()
    dopo = EN.per_nodo(st, mot, par).copy()
    s = (dopo - prima) - CO.divergenza(J, inc)
    return s, (dopo - prima), portata, sat


def main(argv):
    sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))
    import _presidio
    _presidio.avvia(__file__)
    blocchi = []
    print("=" * 100)
    print("LA DERIVA DI `E`: RIMISURATA -- il numero vecchio era ORFANO")
    print("=" * 100)

    # ---------------------------------------------------------------- M0, I DUE REGIMI
    b = ["## 2. `D-ENERGIA:M0` \u2014 la deriva a **tempo totale fisso** `T = 2.0`,"
         " nei **DUE REGIMI**", "",
         "### \u26d4 **E IL REGIME NON E\' UN DETTAGLIO:** con `||psi|| = 1` su tutto il"
         " grafo si ha", "`h_k/Lambda_k ~ 1/(2m)`, e `G(x) = x - arctan x` va come"
         " `x^3/3` \u2014 ### **la saturazione e\'", "praticamente SPENTA, e misurare la"
         " sua sorgente la\' sarebbe un FALSO-ZERO.**", ""]
    for norma in NORME:
        print("  D-ENERGIA:M0 (%s)  deriva a T = 2.0, anello di 16 nodi" % norma)
        righe, sat, scale = m0(norma=norma)
        print("      LA SCALA:  primo termine = %.6e   vuoto = %.6e"
              "   max|h/Lambda| = %.4f" % (scale[0], scale[1], sat))
        b.append("### %s **regime `%s`:** `primo = %.4e`, `vuoto = %.4e`,"
                 " ### **`max|h/Lambda| = %.4f`**" %
                 ("\u2705" if sat > 0.1 else "\u26d4", norma, scale[0], scale[1], sat))
        b.append("")
        b.append("| `dtau` | tick | `|Delta E|` | `|Delta` primo`|` |"
                 " `|Delta` vuoto`|` |")
        b.append("|---|--:|--:|--:|--:|")
        for dt, tk, de, d1, d2 in righe:
            print("      dtau=%-8.5f tick=%-5d |dE|=%.6e  |d primo|=%.3e"
                  "  |d vuoto|=%.6e" % (dt, tk, de, d1, d2))
            b.append("| `%.5f` | %d | `%.6e` | `%.3e` | `%.6e` |" % (dt, tk, de, d1, d2))
        rE = rapporti(righe, 2)
        r1 = rapporti(righe, 3)
        r2 = rapporti(righe, 4)
        print("      rapporti su |dE|:    " + "  ".join("%.3f" % x for x in rE))
        print("      rapporti sul vuoto:  " + "  ".join("%.3f" % x for x in r2))
        b.append("")
        b.append("| i rapporti fra dimezzamenti, su | |")
        b.append("|---|---|")
        b.append("| `|Delta E|` | " + "  ".join("`%.3f`" % x for x in rE) + " |")
        b.append("| il **primo** termine | " + "  ".join("`%.3f`" % x for x in r1)
                 + " |")
        b.append("| il termine del **vuoto** | " + "  ".join("`%.3f`" % x for x in r2)
                 + " |")
        b.append("")
        b.append("### \u2b50 **`4` sarebbe l\'esponente `2`; `1` vuol dire CHE NON"
                 " SCENDE.**")
        b.append("")
        if norma == "locale":
            primo_max = max(x[3] for x in righe)
            vuoto_max = max(x[4] for x in righe)
            sc = scale
    blocchi.append(b)

    # ---------------------------------------------------------------- M0-bis / M0-ter
    print("  D-ENERGIA:M0-bis / M0-ter  DOVE sta la deriva (regime locale)")
    print("      max |Delta primo| = %.6e   su un primo termine di %.6e  (relativo %.2e)"
          % (primo_max, sc[0], primo_max / max(sc[0], 1e-300)))
    print("      max |Delta vuoto| = %.6e   su un vuoto di          %.6e  (relativo %.2e)"
          % (vuoto_max, sc[1], vuoto_max / max(sc[1], 1e-300)))
    b = ["## 3. `D-ENERGIA:M0-bis` e `D-ENERGIA:M0-ter` \u2014 **DOVE** sta la deriva",
         "", "*(regime `locale`, quello in cui la saturazione e\' accesa)*", "",
         "| il termine | `max |Delta|` | la sua SCALA | relativo |",
         "|---|--:|--:|--:|",
         "| il **primo**, `Re<psi\\|W psi>` | `%.4e` | `%.4e` | `%.2e` |"
         % (primo_max, sc[0], primo_max / max(sc[0], 1e-300)),
         "| il **vuoto**, `somma_k Lambda_k G(h_k/Lambda_k)` | `%.4e` | `%.4e` |"
         " `%.2e` |" % (vuoto_max, sc[1], vuoto_max / max(sc[1], 1e-300))]
    blocchi.append(b)

    # ---------------------------------------------------------------- M1a
    print("  D-ENERGIA:M1a  il run LUNGO: oscilla o deriva?")
    serie, _i, _m, _s, _p, sat = corri(16, 0.2, 20000, ogni=20)
    pend, amp, rap = secolare(serie)
    estremi = (float(np.min(serie[:, 1] - serie[0, 1])),
               float(np.max(serie[:, 1] - serie[0, 1])))
    print("      20000 tick:  pendenza %.3e per tick, ampiezza residui %.3e,"
          " rapporto %.3f" % (pend, amp, rap))
    print("      E(t) - E(0) sta fra %.6f e %.6f   su E(0) = %.6f"
          % (estremi[0], estremi[1], float(serie[0, 1])))
    b = ["## 4. `D-ENERGIA:M1a` \u2014 il **run lungo**: `20000` tick", "",
         "| la grandezza | il valore |", "|---|--:|",
         "| `E(0)` | `%.6f` |" % float(serie[0, 1]),
         "| `max|h/Lambda|` all\'inizio | `%.4f` |" % sat,
         "| la **pendenza** della retta adattata | `%.3e` per tick |" % pend,
         "| l\'**ampiezza** dei residui | `%.3e` |" % amp,
         "| il **rapporto** *(spiegata dalla retta / ampiezza)* | **`%.3f`** |" % rap,
         "| `E(t) - E(0)` sta fra | `%.6f` e `%.6f` |" % estremi,
         "",
         "### \u2b50 **IL CRITERIO, fissato PRIMA:** `rapporto >> 1` = **SECOLARE**,"
         " `rapporto << 1` = **OSCILLANTE**."]
    blocchi.append(b)

    # ---------------------------------------------------------------- M1b
    print("  D-ENERGIA:M1b  tre taglie, fattore 4 fra gli estremi (regime locale)")
    b = ["## 5. `D-ENERGIA:M1b` \u2014 **tre taglie**, fattore `4` fra gli estremi", "",
         "### \u26a0 **A STATO LOCALE UGUALE** *(regime `locale`)*: con la"
         " normalizzazione globale",
         "le tre taglie ### **non avrebbero lo stesso stato locale**, e il confronto non"
         " direbbe", "niente sull\'estensivita\'.", "",
         "| `n` | `E(0)` | **escursione** di `E` su `200` tick | **per nodo** |",
         "|--:|--:|--:|--:|"]
    for nn in (8, 16, 32):
        s2, _i, _m, _s, _p, _sa = corri(nn, 0.2, 200, ogni=2)
        # ### ⛔ **L-ESCURSIONE, non `fine - inizio`:** con `E` che oscilla di `76` su
        # ### una scala di `6`, ### **`fine - inizio` E- UN CAMPIONE A CASO** di
        # ### un-oscillazione grande -- e tre campioni a caso non dicono niente
        # ### sull-estensivita-.
        d = escursioni(s2)[0]
        print("      n=%-4d E(0) = %-12.4f |dE| = %.6e   per nodo = %.6e"
              % (nn, float(s2[0, 1]), d, d / nn))
        b.append("| %d | `%.4f` | `%.6e` | `%.6e` |" % (nn, float(s2[0, 1]), d, d / nn))
    blocchi.append(b)

    # ---------------------------------------------------------------- M1c
    print("  D-ENERGIA:M1c  per lunghezza d'onda (n = 32, regime locale)")
    b = ["## 6. `D-ENERGIA:M1c` \u2014 per **lunghezza d\'onda**, `n = 32`", "",
         "| lo stato iniziale | `max|h/Lambda|` | **escursione** di `E` su `200` tick |",
         "|---|--:|--:|"]
    for lung, etic in ((0, "CASUALE (il piu\' ruvido)"), (2, "periodo 2 nodi"),
                       (4, "periodo 4 nodi"), (8, "periodo 8 nodi"),
                       (32, "periodo 32 nodi (il piu\' liscio)")):
        s3, _i, _m, _s, _p, sa = corri(32, 0.2, 200, lunghezza=lung, ogni=2)
        d = escursioni(s3)[0]
        print("      %-34s max|h/Lam| = %-8.4f |dE| = %.6e" % (etic, sa, d))
        b.append("| %s | `%.4f` | `%.6e` |" % (etic, sa, d))
    blocchi.append(b)

    # ------------------------------------------------- LA SCANSIONE IN x (mandato)
    print("  LA SCANSIONE IN x = |h_k|/Lambda_k: dal regime VACUO a quello che LAVORA")
    moduli = (16.0, 8.0, 4.0, 2.0, 1.0, 0.5, 0.25)
    sx = scansione(moduli)
    b = ["## 7. **LA SCANSIONE IN `x = |h_k|/Lambda_k`** — dal regime **vacuo** a"
         " quello che **lavora**", "",
         "> **Mandato della verifica esterna, 2026-10-13:** *<<Un `M0` nel regime"
         " `x ~ 1e-3` e'", "> VACUO: non distingue \"`E` conservata\" da \"il termine non"
         " c'e'\".>>*", "",
         "### ⭐ **E' LO STESSO DIFETTO CHE AVEVO TROVATO MISURANDO**, un'ora prima"
         " che il mandato", "arrivasse: col `psi` normalizzato su tutto il grafo"
         " `x ~ 1/(2m)`, e `G(x) = x - arctan x`",
         "va come `x^3/3` — ### **il termine del vuoto valeva `~1e-5`: la saturazione"
         " era SPENTA.**", "",
         "### ⚠ **`x` SI SCANSIONA COL MODULO DEL VUOTO**, e non e' una costante"
         " nuova:",
         "`Lambda_k = somma |phi_h|^2`, quindi `x` scala come `1/|phi|^2`."
         " ### **Un vuoto piu' debole",
         "porta `x` verso `1`, cioe' ACCENDE la saturazione.**", "",
         "| `|phi|` | `x` max | `x` medio | scala **primo** | scala **vuoto** |"
         " esc. **primo** | esc. **vuoto** | esc. **SOMMA** |"
         " esc./scala NATURALE: primo | vuoto | **SOMMA** |",
         "|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|"]
    for r in sx:
        print("      |phi|=%-6.2f x_max=%-10.4g x_med=%-10.4g  scale: lin %-11.4g"
              " vuoto %-11.4g   esc: lin %-10.3e vuoto %-10.3e SOMMA %-10.3e"
              % (r["modulo"], r["x_max"], r["x_medio"], r["scala_primo"],
                 r["scala_vuoto"], r["esc_primo"], r["esc_vuoto"], r["esc_somma"]))
        print("                     scale NATURALI: ||psi||^2 = %-10.4g  vuoto = %-10.4g   esc/scala: lin %.2e  vuoto %.2e  SOMMA %.2e"
              % (r["nat_primo"], r["nat_vuoto"], r["relnat_primo"],
                 r["relnat_vuoto"], r["relnat_somma"]))
        b.append("| `%.2f` | `%.4g` | `%.4g` | `%.4g` | `%.4g` | `%.3e` | `%.3e` |"
                 " **`%.3e`** | `%.2e` | `%.2e` | **`%.2e`** |" %
                 (r["modulo"], r["x_max"], r["x_medio"], r["scala_primo"],
                  r["scala_vuoto"], r["esc_primo"], r["esc_vuoto"], r["esc_somma"],
                  r["relnat_primo"], r["relnat_vuoto"], r["relnat_somma"]))
    # ### ⛔ **LA CONDIZIONE DI STOP DEL MANDATO, verificata da un CRITERIO e non a occhio:**
    # ### *<<se nel regime `x ~ 1` la somma non si conserva (escursione della somma >=
    # ### quella dei termini), FERMATI e porta il risultato a Luca>>*.
    vicino = min(sx, key=lambda r: abs(np.log10(max(r["x_max"], 1e-300))))
    peggio = max(vicino["esc_primo"], vicino["esc_vuoto"])
    ferma = vicino["esc_somma"] >= peggio
    b.append("")
    b.append("### %s **LA CONDIZIONE DI STOP DEL MANDATO**, sul punto con `x` piu' vicino"
             " a `1` *(`x = %.4g`)*:" %
             ("⛔" if ferma else "✅", vicino["x_max"]))
    b.append("")
    b.append("| | il numero |")
    b.append("|---|--:|")
    b.append("| escursione della **SOMMA** | `%.3e` |" % vicino["esc_somma"])
    b.append("| la **maggiore** dei due termini | `%.3e` |" % peggio)
    b.append("| ### %s **il verdetto** | ### **%s** |" %
             ("⛔" if ferma else "✅",
              "LA SOMMA NON SI CONSERVA: VA A LUCA" if ferma
              else "la somma si conserva meglio dei termini"))
    print("      STOP del mandato: x piu' vicino a 1 = %.4g; esc. SOMMA = %.3e contro"
          " la maggiore dei termini %.3e  ->  %s"
          % (vicino["x_max"], vicino["esc_somma"], peggio,
             "FERMA (va a Luca)" if ferma else "non ferma"))
    blocchi.append(b)

    # ------------------------------------- LA STESSA SCANSIONE, MA IN SU(2)
    # ### ⛔ **PERCHE- SI RIFA-: la misura delle BANDE ha trovato che la `C` chiede
    # ### `det U = 1`**, e la scansione qui sopra e- fatta con `U(2)` generico.
    # ### ⚠ **Non credevo che la conclusione cambiasse -- la causa e- il termine del
    # ### vuoto, che dipende da `h_k` -- ma ### NON L-AVEVO MISURATO**, e un numero su cui
    # ### si e- fermato un pezzo ### **non si lascia con un dubbio dichiarato.**
    print("  LA STESSA SCANSIONE IN SU(2), perche' la C chiede det U = 1")
    sx2 = scansione((16.0, 4.0, 2.0, 1.0, 0.5), su2=True)
    b = RF.blocco_su2(sx2)
    blocchi.append(b)

    # ---------------------------------------------------------------- (c)
    print("  (c)  LA SORGENTE PER NODO, con N acceso -- e DECOMPOSTA")
    b = ["## 9. `(c)` \u2014 **LA SORGENTE PER NODO**, con `N` acceso", "",
         "`s_k = Delta E_k - (div J)_k`, con `J` la corrente locale **costruita** per il"
         " pezzo",
         "lineare, valutata sullo stato che **entra** nel pezzo lineare *(dopo il primo"
         " mezzo",
         "flusso)*.", "",
         "### \u26d4 **E SI DECOMPONE, perche\' il residuo MESCOLA DUE COSE:** il mio `J`"
         " copre il",
         "pezzo lineare **dello spinore**, e la **camminata del vuoto** muove `phi` fra i"
         " nodi,",
         "cioe\' ### **trasferisce energia di vuoto senza che io la modelli.**"
         " ### \u26a0 **Quello e\' una",
         "CORRENTE CHE MANCA, non una sorgente** \u2014 e chiamarlo sorgente sarebbe"
         " attribuire al",
         "fenomeno un buco del mio strumento. ### **Lo stesso errore della candidata di"
         " ieri.**", ""]
    # ### ⛔ **E LA DECOMPOSIZIONE SI RIVELA VACUA PER QUESTO VUOTO, e lo si PROVA**
    lu = lambda_sotto_vuoto(uniforme=True)
    lnu = lambda_sotto_vuoto(uniforme=False)
    print("    e PRIMA: la camminata del vuoto cambia Lambda_k?"
          "  |phi| uniforme -> %.3e   |phi| NON uniforme -> %.3e" % (lu, lnu))
    b.append("### ⛔ **MA LA DECOMPOSIZIONE E' VACUA PER QUESTO VUOTO, e si PROVA invece"
             " di dedurlo:**")
    b.append("")
    b.append("| `|phi|` | `max_k |Delta Lambda_k|` sotto la **sola** camminata del"
             " vuoto | |")
    b.append("|---|--:|---|")
    b.append("| **uniforme** *(il vuoto del banco)* | `%.3e` |"
             " ### ⛔ **ESATTAMENTE invariante** |" % lu)
    b.append("| **non uniforme** *(controllo positivo)* | `%.3e` |"
             " ### ✅ **cambia: la misura SA vedere** |" % lnu)
    b.append("")
    b.append("### ⭐ **E IL PERCHE' E' STRUTTURALE:** su un grafo **`2`-regolare** il"
             " Grover scalare e'")
    b.append("`(2/2)(phi_a + phi_b) - phi_h`, cioe' **uno SCAMBIO**, e lo spostamento e'"
             " una")
    b.append("**permutazione**: con `|phi|` uniforme permutano **moduli tutti uguali**,"
             " quindi")
    b.append("### **`Lambda_k` non cambia e la camminata del vuoto NON PORTA ENERGIA DI"
             " VUOTO.**")
    b.append("### ⚠ **Percio' le due righe qui sotto coincidono A TUTTE LE CIFRE**, e non"
             " e' un errore:")
    b.append("### **e' che qui non c'e' niente da decomporre.** ### ⛔ **Su un grafo di"
             " grado `> 2`")
    b.append("la decomposizione tornerebbe a dire qualcosa, e NON l'ho misurata.**")
    b.append("")
    for cammina, etic in ((False, "SENZA la camminata del vuoto (la sorgente VERA di `N`)"),
                          (True, "col tick INTERO (sorgente + corrente del vuoto che manca)")):
        print("    %s" % etic)
        b.append("### %s **%s**" %
                 ("\u2705" if not cammina else "\u26a0", etic))
        b.append("")
        b.append("| `dtau` | `max_k |s_k|` | `somma_k s_k` | `max_k |Delta E_k|` |"
                 " `s/Delta E` | rapporto col precedente |")
        b.append("|---|--:|--:|--:|--:|--:|")
        prec = None
        for dt in (0.2, 0.1, 0.05, 0.025):
            s, dE, portata, sa = sorgente_per_nodo(dtau=dt, vuoto_cammina=cammina)
            mx = float(np.max(np.abs(s)))
            tot = float(np.sum(s))
            mdE = float(np.max(np.abs(dE)))
            rr = ("%.3f" % (prec / mx)) if prec and mx > 0 else "--"
            print("      dtau=%-8.5f max_k|s_k| = %.6e  somma_k s_k = %+.3e"
                  "  max_k|dE_k| = %.3e  s/dE = %.2e  rapp %s"
                  % (dt, mx, tot, mdE, mx / max(mdE, 1e-300), rr))
            b.append("| `%.5f` | `%.6e` | `%+.3e` | `%.3e` | `%.2e` | `%s` |" %
                     (dt, mx, tot, mdE, mx / max(mdE, 1e-300), rr))
            prec = mx
        b.append("")
        b.append("### \u2b50 **`4` sarebbe `O(dtau^2)`; `1` vuol dire `O(1)`, cioe\' CHE"
                 " NON SCENDE.**")
        b.append("")
    blocchi.append(b)

    print("=" * 100)
    if "--scrivi" in argv:
        print("REFERTO: %s" % RF.scrivi_referto(blocchi))
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
