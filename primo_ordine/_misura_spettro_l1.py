# -*- coding: utf-8 -*-
r"""**LO SPETTRO DEL PASSO LINEARE PALINDROMO — una MISURA, nessuna decisione.**

> **Punto 3 del mandato di Luca del 2026-10-15** *(12:44)*: *«Su un toro piccolo, col passo
> palindromo, a `theta = pi`, `0.5 pi`, `0.25 pi` (`dtau` uniforme): le fasi proprie `eps`
> del passo lineare sono appaiate `eps <-> -eps`? ci sono degeneranze doppie (alla Kramers,
> perche' `C^2 = -1` su `psi`)? `C W C^-1 = W^-1` vale al bit o all'ulp?»*
>
> ### ⛔ **NESSUNA CONCLUSIONE DI FISICA: la decide Luca.** Qui ci sono **solo numeri**.

## ⭐ CHE COS'E' `W` QUI, E CHE COSA NON E'

### **`W` e' la PARTE LINEARE del passo**: *moneta di spin, Grover, spostamento* — e
### ⛔ **SENZA LA SATURAZIONE**, che e' il solo pezzo non lineare *(dipende da `h` e da
`Lambda`, cioe' **dallo stato**)*.
### 📌 **E si costruisce APPLICANDO il passo ai vettori di base**, non scrivendo una
matrice a mano: ### **cosi' `W` e' per costruzione l'operatore che il motore applica
davvero**, e non la mia idea di che cosa applichi.

### ⛔ **E `bande.py` RESTA CONGELATO:** questo e' uno script **nuovo di `L1`**, e **non
importa** `bande.py`, `segno.py` ne' le loro misure.

## ⭐⭐ UNA DERIVAZIONE SCRITTA PRIMA DI MISURARE — **e dice che cosa aspettarsi**

### Se `C W C^-1 = W^-1` e `W v = e^{i eps} v`, allora *(e `C` e' **antiunitaria**, quindi
coniuga gli scalari)*:

```
W^-1 (C v) = C W C^-1 C v = C (W v) = C (e^{i eps} v) = e^{-i eps} (C v)
      ==>   W (C v) = e^{+i eps} (C v)
```

### ⭐ **Quindi `C v` e' autovettore con LO STESSO autovalore**, e siccome `C^2 = -1` su
`psi` ### **`C v` e' indipendente da `v`**: ### ✅ **ogni autovalore e' ALMENO DOPPIO.**
### **E' la degenerazione di Kramers, e qui e' una CONSEGUENZA, non un'ipotesi.**

### ⚠⚠ **E LA STESSA DERIVAZIONE DICE CHE `eps <-> -eps` NON SEGUE.** Un'antiunitaria da'
**la degenerazione**; un appaiamento `eps <-> -eps` vorrebbe un'**antisimmetria UNITARIA**
*(del tipo `X W X^-1 = W^-1` con `X` lineare)*, che ### **nessuno ha mostrato esistere.**
### 📌 **Quindi la risposta attesa e': degeneranze DOPPIE SI', appaiamento `eps <-> -eps`
NON NECESSARIAMENTE.** ### ⛔ **E lo scrivo PRIMA per non poter chiamare <<previsto>> cio'
che la misura dira'.**

## ⛔ IL CASO CHE DEVE FALLIRE

### **L'ordine NON palindromo** *(quello di prima del `2026-10-15`)*: la' `C W C^-1 = W^-1`
### **deve ROMPERSI**, perche' `C W C^-1` e' il prodotto degli `Op^-1` **nello stesso
ordine** mentre `W^-1` lo e' **in ordine rovescio.**
### ⚠ **Senza questo braccio il verdetto sarebbe un FALSO-UNO:** una `C` che passa non
proverebbe che e' **il palindromo** a farla passare.

Gira con:  python primo_ordine/_misura_spettro_l1.py
"""
import os
import sys

import numpy as np
import tick as TK

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

OK = [0, 0]
# ### ⛔ **LA CONFIGURAZIONE INTERA, DICHIARATA E STAMPATA**
LATI = (3, 3)
SEME = 7
DTAU = (1.0, 0.5, 0.25)
EPS = 0.5
VUOTO_MODULO = 2.0
SY = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
# ### ⛔⛔ **LA SOGLIA DELL-APPAIAMENTO E- ALL-ULP, NON <<ENTRO LA SPAZIATURA>>**
# ### *(correzione del guardiano, 2026-10-15)*. ### **E il motivo e- una cosa che ne io ne
# ### lui avevamo visto: con un accoppiamento OTTIMO anche uno spettro CASUALE, senza
# ### nessun appaiamento, da- distanze DELL-ORDINE DELLA SPAZIATURA** -- perche- l-ottimo
# ### trova sempre un partner vicino quando i livelli sono fitti.
# ### ✅ **Quindi <<appaiato>> vuol dire `~1e-15`**, e un numero come `0.082` su una
# ### spaziatura di `0.088` vuol dire ### **<<NON DISTINGUIBILE DAL CASO>>**, non
# ### <<appaiato>>. ### 📌 **E la spaziatura serve ancora, ma a UN-ALTRA COSA: dire quanto
# ### e- grande una distanza CASUALE.**
APPAIATO = 1e-10
# ### ⚠ **I TIRI DEL CONTROLLO: `20`, e non `1`.** ### **Un tiro e- un campione,
# ### non una scala**, e cio- che risponde alla domanda <<il caso potrebbe dare
# ### un numero cosi- piccolo?>> e- ### **il MINIMO su molti tiri.**
TIRI = 20
# ### ⛔ **L-ORDINE DI PRIMA, per il CASO CHE DEVE FALLIRE.** ### **Non e- una seconda
# ### tabella:** e- un dato storico, e serve solo a questo braccio.
ORDINE_VECCHIO = (("CAMM-SATURAZIONE", 0.5), ("CAMM-MONETA-SPIN", 1),
                  ("CAMM-GROVER", 1), ("CAMM-SPOSTAMENTO", 1),
                  ("CAMM-GROVER-VUOTO", 1), ("CAMM-SPOSTAMENTO-VUOTO", 1),
                  ("CAMM-SATURAZIONE", 0.5))


def accoppia(a, b):
    """### `max` distanza dell-accoppiamento **OTTIMO** fra due multinsiemi complessi.

    ### ⛔⛔ **PRIMA QUESTA FUNZIONE ERA GOLOSA, E IL SUO NUMERO DICEVA IL CONTRARIO DEL
    VERO.** Un goloso prende per ogni elemento il piu- vicino ancora libero, quindi
    ### **gli ultimi rimasti vengono accoppiati PER FORZA, anche lontanissimi**: cio- che
    ne usciva ### **non era la distanza fra i due multinsiemi**, era **il peggior residuo
    di una scelta miope.**
    ### ⚠ **Misurato sulla stessa scena a `dtau = 1`: goloso `1.99`, OTTIMO `0.082`, con
    una spaziatura dei livelli di `0.088`** -- cioe- il goloso diceva <<lontanissimo>> dove
    l-ottimo dice <<appaiato entro la spaziatura>>.

    ### ✅ **Un accoppiamento fra multinsiemi E- UN PROBLEMA DI OTTIMIZZAZIONE**, e si
    risolve: `scipy.optimize.linear_sum_assignment` sulla matrice delle distanze.
    ### 📌 **E si resta SUL PIANO COMPLESSO, non sugli angoli:** sugli angoli una coppia
    vicina a `+-pi` si spezza, perche- la- `-(-pi) = +pi` e- **lo stesso autovalore** ma
    due angoli lontani `2pi`.
    """
    # ### ⚠ **E DICO CHE COSA MINIMIZZA, perche- non e- il massimo:**
    # ### `linear_sum_assignment` minimizza ### **la SOMMA** dei costi, e qui si riporta
    # ### ### **il MASSIMO di QUELL-accoppiamento.** ### **Non e- garantito che sia il
    # ### minimo possibile fra i massimi** *(quello sarebbe un problema <<bottleneck>>)*:
    # ### e- una grandezza ben definita e standard, e ### **va letta per quella che e-.**
    from scipy.optimize import linear_sum_assignment
    a = np.asarray(a).reshape(-1)
    b = np.asarray(b).reshape(-1)
    assert a.shape == b.shape, (a.shape, b.shape)
    costo = np.abs(a.reshape(-1, 1) - b.reshape(1, -1))
    ri, ci = linear_sum_assignment(costo)
    return float(np.max(costo[ri, ci]))


def accoppia_collo(a, b):
    """### L-ottimo **A COLLO DI BOTTIGLIA**: ### **il MINIMO dei MASSIMI.**

    ### ⭐⭐ **E- QUESTA la grandezza che risponde alla domanda <<lo spettro e- appaiato
    entro `d`?>>**, perche- e- ### **il piu- piccolo `d` per cui esiste una biiezione
    che sta tutta entro `d`.** ### ⚠ **`linear_sum_assignment` minimizza la SOMMA**, e il
    massimo di quell-accoppiamento ### **puo- essere piu- grande del minimo possibile.**
    ### 📌 **E la differenza si vede nei numeri: a `dtau = 0.5` la somma-ottima da-
    `2.000` e il collo di bottiglia da- un altro valore** -- e il guardiano aveva riportato
    `1.40`, che e- la- in mezzo. ### **Quindi si stampano TUTTE E TRE**, e chi legge sa
    quale sta guardando.

    ### **Come:** ricerca binaria sulle distanze presenti, e a ogni soglia si chiede se
    esiste ### **un abbinamento COMPLETO** nel grafo bipartito delle coppie ammesse.
    """
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import maximum_bipartite_matching
    a = np.asarray(a).reshape(-1)
    b = np.asarray(b).reshape(-1)
    n = a.shape[0]
    assert b.shape[0] == n, (a.shape, b.shape)
    d = np.abs(a.reshape(-1, 1) - b.reshape(1, -1))
    cand = np.unique(d)

    def basta(soglia):
        m = csr_matrix(d <= soglia)
        acc = maximum_bipartite_matching(m, perm_type="column")
        return int(np.sum(acc >= 0)) == n

    lo, hi = 0, len(cand) - 1
    if not basta(cand[hi]):
        return float(cand[hi])
    while lo < hi:
        mid = (lo + hi) // 2
        if basta(cand[mid]):
            hi = mid
        else:
            lo = mid + 1
    return float(cand[lo])


def spettro_casuale(lam, seme):
    """### Uno spettro **CASUALE** con lo **STESSO numero** e lo **STESSO intervallo**.

    ### ⛔⛔ **E- IL CONTROLLO DI SCALA, e senza di lui il numero dell-appaiamento NON SI
    PUO- LEGGERE:** dice ### **quanto vale una distanza DOVUTA AL CASO** su uno spettro
    fitto come questo.
    ### ⚠ **L-intervallo si copia da quello vero** *(non tutto il cerchio)*, perche-
    altrimenti ### **la spaziatura del controllo sarebbe un-altra** e il confronto non
    starebbe in piedi.
    """
    a = np.angle(lam)
    r = np.random.default_rng(seme)
    fasi = r.uniform(float(np.min(a)), float(np.max(a)), len(lam))
    return np.exp(1j * fasi)


def _goloso(a, b):
    """### L-accoppiamento GOLOSO, ### **tenuto SOLO per far vedere che sbaglia.**

    ### ⛔ **NON si usa per misurare niente:** e- qui perche- ### **un difetto che non si
    puo- piu- riprodurre non si puo- piu- spiegare** -- e questo ha fatto scrivere nella
    `RIPRESA` un numero che diceva il contrario del vero.
    """
    b = list(np.asarray(b).reshape(-1))
    peggio = 0.0
    for x in np.asarray(a).reshape(-1):
        k = min(range(len(b)), key=lambda j: abs(b[j] - x))
        peggio = max(peggio, abs(b[k] - x))
        b.pop(k)
    return float(peggio)


def hausdorff(a, b):
    """### La distanza di **Hausdorff** fra i due insiemi, ### **nei DUE versi.**

    ### ⭐ **Dice una cosa DIVERSA dall-accoppiamento, e per questo ci vogliono entrambe:**
    Hausdorff guarda <<ogni elemento ha QUALCUNO vicino?>> e ### **ignora le
    molteplicita-**; l-accoppiamento guarda <<esiste una BIIEZIONE vicina?>> e le conta.
    ### ⚠ **Hausdorff e- sempre `<=` dell-accoppiamento ottimo**, quindi un Hausdorff
    piccolo con un accoppiamento grande vuol dire ### **molteplicita- che non tornano.**
    """
    a = np.asarray(a).reshape(-1)
    b = np.asarray(b).reshape(-1)
    d = np.abs(a.reshape(-1, 1) - b.reshape(1, -1))
    return float(max(np.max(np.min(d, axis=1)), np.max(np.min(d, axis=0))))


def spaziatura(lam):
    """### La **spaziatura media dei livelli**: ### **il metro con cui si legge il resto.**

    ### ⛔ **Senza di lei una distanza fra spettri NON SI PUO- LEGGERE:** `0.082` e-
    <<appaiato>> o <<no>> ### **solo rispetto a qualcosa**, e quel qualcosa e- **quanto
    distano fra loro i livelli vicini.**
    ### 📌 **Si misura come CORDA fra autovalori consecutivi** *(ordinati per angolo)*,
    cosi- e- ### **nella stessa unita-** dell-accoppiamento e di Hausdorff -- e per
    separazioni piccole la corda e- l-arco, quindi il numero coincide con la spaziatura
    ANGOLARE.
    """
    lam = np.asarray(lam).reshape(-1)
    ord_ = lam[np.argsort(np.angle(lam))]
    if len(ord_) < 2:
        return float("nan")
    return float(np.mean(np.abs(np.diff(ord_))))


def gruppi_di(lam, toll):
    """### Le molteplicita', raggruppando ### **per AUTOVALORE** e non per angolo."""
    n = len(lam)
    usato = np.zeros(n, dtype=bool)
    fuori = []
    for i in range(n):
        if usato[i]:
            continue
        vv = [j for j in range(n) if not usato[j] and abs(lam[j] - lam[i]) <= toll]
        for j in vv:
            usato[j] = True
        fuori.append(len(vv))
    return fuori


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-58s %s   %s" % (che[:58], "PASSA" if passa else "### FALLISCE", nota))


def scena(dtau):
    """### Il **TORO** `LATI`, ### **grado `2 d` e NON `2`.**

    ### ⛔ **Il toro, e non l'anello:** un anello ha grado `2`, e li' il Grover e' quasi
    una permutazione — ### **una proprieta' dello spettro misurata a grado `2` non dice
    niente del grado `4`.** ### ✅ **E non ha bordi**, che e' cio' che <<toro>> compra.
    ### 📌 **Il costruttore e' `corrente.toro`, usato IN SOLA LETTURA.**
    """
    import corrente as CO
    import incidenza as IN
    import motore as MO
    import stato as ST
    ii, jj, nn = CO.toro(LATI)
    inc = IN.Incidenza(np.asarray(ii, dtype=IN.INDICE),
                       np.asarray(jj, dtype=IN.INDICE), nn, capacita=len(ii))
    r = np.random.default_rng(SEME)
    nv = r.normal(size=(2 * inc.m, 3))
    nv /= np.linalg.norm(nv, axis=1).reshape(-1, 1)
    U = np.zeros((inc.m, 2, 2), dtype=complex)
    for a in range(inc.m):
        X = r.normal(size=(2, 2)) + 1j * r.normal(size=(2, 2))
        Qm, _ = np.linalg.qr(X)
        # ### ⛔ **`SU(2)`, e NON e- un abbellimento:** la `C` antilineare chiede
        # ### `sigma_y U^* sigma_y^-1 = U`, che vale ### **se e solo se `det U = 1`.**
        U[a] = Qm / np.sqrt(np.linalg.det(Qm))
    st = ST.nuovo(nn, inc.m)
    st["psi_h"][...] = (r.normal(size=st["psi_h"].shape)
                        + 1j * r.normal(size=st["psi_h"].shape))
    st["phi_h"][...] = (float(VUOTO_MODULO)
                        * np.exp(1j * r.random(st["phi_h"].shape) * 2.0 * np.pi))
    mot = MO.Motore(inc, MO.Geometria(nv, U), st, np.full(nn, dtau), "numpy")
    return inc, mot, st


def ordine_lineare(ordine):
    """### L'ordine dato **senza la saturazione**: ### **e' la PARTE LINEARE.**"""
    return [(idl, fr) for idl, fr in ordine if idl != "CAMM-SATURAZIONE"]


def ordine_tabella():
    """### L'ordine della **TABELLA**, letto da `composizione.py`."""
    import composizione as CM
    return [(idl, fr) for idl, fr, _t in CM.ORDINE]


def passo(mot, st, ordine):
    """### Applica `ordine` **una volta**, ### **in posto.**"""
    import deriva as DV
    mot.apri_tick()
    for idl, fr in ordine:
        nome, vuole_par = TK.OPERATORE[idl]
        mot.operatori[nome](st, {"eps": EPS} if vuole_par else {}, fr)
    mot.chiudi_tick()


def matrice(mot, st, ordine):
    """### `W` **sulla parte `psi`**, costruita applicando il passo ai vettori di base.

    ### ⚠ **`phi` si azzera**, e si puo': i pezzi del vuoto ### **non toccano `psi`**,
    e la saturazione — l'unico pezzo che li lega — ### **non e' in `ordine`.**
    """
    forma = st["psi_h"].shape
    d = forma[0] * forma[1]
    W = np.zeros((d, d), dtype=complex)
    for k in range(d):
        st["psi_h"].fill(0)
        st["phi_h"].fill(0)
        st["psi_h"].reshape(-1)[k] = 1.0
        passo(mot, st, ordine)
        W[:, k] = st["psi_h"].reshape(-1)
    return W


def c_su_psi(v, forma):
    """### `C psi = i sigma_y psi^*` ### **per estremita'.**"""
    p = np.conj(v.reshape(forma))
    return np.einsum("ij,aj->ai", 1.0j * SY, p).reshape(-1)


def c_su_U(U):
    """### `C U = sigma_y U^* sigma_y^-1` — ### **la correzione di Luca del 2026-10-13.**"""
    return np.einsum("ij,ajk,kl->ail", SY, np.conj(U), SY)


def valida_la_misura():
    """### ⛔ **DUE CASI CHE VALIDANO LA MISURA, non la fisica.**

    ### ⚠ **Servono perche- la versione di prima di `accoppia` era ROTTA e nessuno se ne
    accorgeva:** il numero usciva, era plausibile, e ### **diceva il contrario del vero.**
    ### ✅ **Un caso che DEVE passare e uno che DEVE fallire lo avrebbero preso.**
    """
    print("-" * 96)
    print("### LA VALIDAZIONE DELLA MISURA (non della fisica):")
    r = np.random.default_rng(3)
    eps = r.uniform(0.05, 3.0, 36)
    # ### il caso che DEVE PASSARE: uno spettro ### **appaiato PER COSTRUZIONE**
    app = np.concatenate([np.exp(1j * eps), np.exp(-1j * eps)])
    d1 = accoppia(app, np.conj(app))
    h1 = hausdorff(app, np.conj(app))
    s1 = spaziatura(app)
    esito("### DEVE PASSARE: uno spettro appaiato PER COSTRUZIONE da- ~0",
          d1 <= 1024 * float(np.finfo(float).eps),
          "ottimo %.3e  Hausdorff %.3e  spaziatura %.3e" % (d1, h1, s1))
    # ### il caso che DEVE FALLIRE: ### **le stesse fasi TRASLATE**, cosi- l-insieme
    # ### ### **non e- piu- chiuso per coniugazione**
    delta = 0.3
    rot = app * np.exp(1j * delta)
    d2 = accoppia(rot, np.conj(rot))
    s2 = spaziatura(rot)
    esito("### DEVE FALLIRE: le stesse fasi TRASLATE di %.1f NON sono appaiate" % delta,
          d2 > 10.0 * s2,
          "ottimo %.3e contro una spaziatura di %.3e, cioe- %.0f volte"
          % (d2, s2, d2 / s2))
    # ### ⚠⚠ **E UN BRACCIO CHE AVEVO SCRITTO MALE, e lo dico invece di toglierlo in
    # ### silenzio:** avevo messo qui il confronto col goloso, aspettandomi che sbagliasse.
    # ### ### **NON sbaglia su un insieme ESATTAMENTE appaiato** -- la- ogni elemento ha
    # ### il suo partner a distanza zero, e ### **anche il goloso lo trova** *(misurato:
    # ### goloso `0.000e+00` come l-ottimo)*.
    # ### ✅ **Il goloso sbaglia dove l-appaiamento e- APPROSSIMATO, cioe- SULLO SPETTRO
    # ### VERO**, ed e- la- che il confronto sta adesso *(in `prove`)*.
    # ### ⭐ **E la lezione e- la stessa di prima, applicata a me due volte: un caso di
    # ### prova COSTRUITO TROPPO FACILE non prova niente.**
    return d1, d2


def prove(dtau):
    """### Le tre domande, ### **a un `dtau` dato.**"""
    eps_m = float(np.finfo(float).eps)
    inc, mot, st = scena(dtau)
    forma = st["psi_h"].shape
    ordine = ordine_lineare(ordine_tabella())
    W = matrice(mot, st, ordine)
    d = W.shape[0]
    print("-" * 96)
    print("  dtau = %.4f -> theta = %.4f pi   |   W e' %dx%d, %d pezzi lineari"
          % (dtau, dtau, d, d, len(ordine)))
    # ------------------------------------------------- (0) W e' UNITARIA?
    sb = float(np.max(np.abs(np.conj(W.T).dot(W) - np.eye(d))))
    esito("(0) `W` e' UNITARIA (senza questo, le fasi non sono fasi)",
          sb <= 1024 * eps_m, "scarto %.3e, cioe' %.0f ulp" % (sb, sb / eps_m))
    # ------------------------------------------------- le fasi proprie
    autov = np.linalg.eigvals(W)
    e = np.sort(np.angle(autov))
    toll = 1e-8
    # ------------------------------------------------- (1) eps <-> -eps?
    # ### ⭐ **`eps -> -eps` e- `lambda -> coniugato(lambda)`**, e si misurano ### **TRE
    # ### numeri, non uno**: l-accoppiamento OTTIMO, Hausdorff, e ### **la spaziatura dei
    # ### livelli**, che e- il metro.
    dist = accoppia(autov, np.conj(autov))
    collo = accoppia_collo(autov, np.conj(autov))
    haus = hausdorff(autov, np.conj(autov))
    spa = spaziatura(autov)
    print("    le fasi: min %.6f  max %.6f  (su pi: %.4f .. %.4f)"
          % (e[0], e[-1], e[0] / np.pi, e[-1] / np.pi))
    print("    ### (1) APPAIAMENTO: somma-ottima %.6e   COLLO DI BOTTIGLIA %.6e"
          "   Hausdorff %.6e" % (dist, collo, haus))
    print("    ###     e IL METRO: spaziatura media dei livelli %.6e  ->  collo su"
          " spaziatura = %.2f" % (spa, collo / spa if spa > 0 else float("nan")))
    # ### ⛔ **IL CONTROLLO DI SCALA: uno spettro CASUALE, stesso numero e stesso
    # ### intervallo.** ### **Se il casuale da- lo stesso ordine di grandezza, allora il
    # ### numero vero NON DICE <<appaiato>>: dice <<non distinguibile dal caso>>.**
    # ### ⚠ **E IL CONTROLLO SI FA CON PIU- TIRI, non con uno:** ### **un tiro casuale
    # ### e- UN CAMPIONE, non una scala.** ### **Cio- che serve e- il MINIMO su molti
    # ### tiri**, perche- la domanda e- <<il caso POTREBBE dare un numero cosi- piccolo?>>.
    tiri = [accoppia_collo(c, np.conj(c))
            for c in (spettro_casuale(autov, 101 + t) for t in range(TIRI))]
    c_collo = float(np.median(tiri))
    c_min = float(np.min(tiri))
    c_spa = spaziatura(spettro_casuale(autov, 101))
    print("    ###     e IL CONTROLLO DI SCALA (%d spettri CASUALI, stesso intervallo):"
          " collo mediano %.6e, MINIMO %.6e, spaziatura %.6e"
          % (TIRI, c_collo, c_min, c_spa))
    esito("(1) APPAIATO ALL'ULP (<= %.0e)? e non <<entro la spaziatura>>" % APPAIATO,
          collo <= APPAIATO,
          "collo %.3e: %s   (e il CASO su %d tiri: mediana %.3e, MINIMO %.3e)"
          % (collo, "APPAIATO" if collo <= APPAIATO else "NON appaiato", TIRI,
             c_collo, c_min))
    # ### ⛔⛔ **E QUI IL CONFRONTO COL GOLOSO, SULLO SPETTRO VERO: e- la prova che la
    # ### cura serviva.** ### **Su un insieme esattamente appaiato il goloso non sbaglia;
    # ### dove l-appaiamento e- APPROSSIMATO, sbaglia di un fattore 20.**
    gol = _goloso(autov, np.conj(autov))
    print("    ###     e il GOLOSO di prima: %.6e  ->  diverso dal collo di %.3e,"
          " cioe' %.1f spaziature" % (gol, abs(gol - collo),
                                      abs(gol - collo) / spa if spa > 0 else
                                      float("nan")))
    # ------------------------------------------------- (2) degeneranze doppie?
    gruppi = gruppi_di(autov, toll)
    molt = {}
    for g in gruppi:
        molt[g] = molt.get(g, 0) + 1
    esito("(2) ogni autovalore e' ALMENO DOPPIO (Kramers, `C^2 = -1`)",
          min(gruppi) >= 2,
          "molteplicita': %s su %d gruppi (tolleranza %.0e)"
          % (molt, len(gruppi), toll))
    # ------------------------------------------------- (3) C W C^-1 = W^-1?
    scarto = _prova_c(mot, st, forma, ordine)
    sc = 1.0
    esito("(3) `C W C^-1 = W^-1` (inversione del tempo del PASSO INTERO)",
          scarto <= 1024 * eps_m * sc,
          "scarto %.3e, cioe' %.0f ulp" % (scarto, scarto / eps_m))
    # ------------------------------------------------- il caso che DEVE fallire
    vecchio = ordine_lineare(ORDINE_VECCHIO)
    inc2, mot2, st2 = scena(dtau)
    rotto = _prova_c(mot2, st2, forma, vecchio)
    esito("### DEVE ROMPERSI: lo stesso con l'ordine NON palindromo",
          rotto > 1024 * eps_m,
          "scarto %.3e: ### senza questo il braccio (3) sarebbe un FALSO-UNO" % rotto)
    # ============================================= LA DIAGNOSI: CHI ROMPE LA (3)?
    # ### ⛔ **Il braccio `(3)` FALLISCE anche col palindromo**, e la derivazione dice
    # ### ### **chi**: ### la MONETA DI SPIN. ### ⭐ **Il conto, in due righe:**
    # ### `C exp(-i a sigma.n) C^-1 = (i sigma_y) exp(+i a (sigma.n)^*) (i sigma_y)^-1`,
    # ### e siccome `sigma_y (sigma.n)^* sigma_y^-1 = -(sigma.n)` *(con `n` reale)*, il
    # ### risultato e- ### **`exp(-i a sigma.n)`, cioe- LA STESSA COSA** -- ### **non la
    # ### sua inversa.** ### ⚠ **E la moneta NON c-era nel test dei quattro pezzi del
    # ### 2026-10-15**: ### **non l-avevo mai misurata.**
    print("    ### LA DIAGNOSI DEL BRACCIO (3): chi non si rovescia?")
    inc3, mot3, st3 = scena(dtau)
    m_inv = _prova_c(mot3, st3, forma, [("CAMM-MONETA-SPIN", 0.5)])
    inc4, mot4, st4 = scena(dtau)
    m_ug = _prova_c_uguale(mot4, st4, forma, [("CAMM-MONETA-SPIN", 0.5)])
    esito("(4) la MONETA sotto `C` resta SE STESSA, non la sua inversa",
          m_ug <= 1024 * eps_m and m_inv > 1024 * eps_m,
          "`C M C^-1 = M` da' %.3e, `= M^-1` da' %.3e" % (m_ug, m_inv))
    senza = [x for x in ordine if x[0] != "CAMM-MONETA-SPIN"]
    inc5, mot5, st5 = scena(dtau)
    s_senza = _prova_c(mot5, st5, forma, senza)
    esito("(5) e SENZA la moneta `C W C^-1 = W^-1` TORNA ESATTA",
          s_senza <= 1024 * eps_m,
          "scarto %.3e su %d pezzi, cioe' %.0f ulp"
          % (s_senza, len(senza), s_senza / eps_m))
    W2 = matrice(mot5, st5, senza)
    l2 = np.linalg.eigvals(W2)
    g2 = gruppi_di(l2, toll)
    esito("(6) e SENZA la moneta la degenerazione di Kramers C'E'",
          min(g2) >= 2, "molteplicita' minima %d su %d gruppi" % (min(g2), len(g2)))
    # ### ⚠ **anche qui il COLLO DI BOTTIGLIA**, non la somma-ottima: altrimenti i due
    # ### numeri della tabella ### **non sarebbero confrontabili fra loro.**
    d2 = accoppia_collo(l2, np.conj(l2))
    s2 = spaziatura(l2)
    esito("(7) e SENZA la moneta: APPAIATO ALL'ULP?", d2 <= APPAIATO,
          "collo %.3e   Hausdorff %.3e   spaziatura %.3e   -> %s"
          % (d2, hausdorff(l2, np.conj(l2)), s2,
             "APPAIATO" if d2 <= APPAIATO else "NON appaiato"))
    return (dist, collo, spa, min(gruppi), scarto, rotto, m_ug, s_senza, min(g2),
            d2, s2, gol)


def _prova_c_uguale(mot, st, forma, ordine):
    """### `max |C W C psi - psi|`: ### **vale se `C W C^-1 = W`**, non `W^-1`.

    ### ⭐ **La differenza col test di sopra e' SOLO il verso del confronto:** qui si
    applica `C`, il passo, `C`, e **l'INVERSO non si applica** — si confronta col passo
    fatto una volta sola. ### **E il segno di `C^2 = -1` resta.**
    """
    r = np.random.default_rng(SEME + 1)
    v = (r.normal(size=forma) + 1j * r.normal(size=forma))
    # ### il passo UNA volta, su `v`
    st["psi_h"][...] = v
    st["phi_h"].fill(0)
    passo(mot, st, ordine)
    diretto = st["psi_h"].copy()
    # ### e `C`, il passo, `C` -- che e- `C W C^-1` a meno del segno di `C^2`
    st["psi_h"][...] = v
    st["phi_h"].fill(0)
    st["psi_h"][...] = c_su_psi(st["psi_h"].reshape(-1), forma).reshape(forma)
    mot.geo.U[...] = c_su_U(mot.geo.U.copy())
    passo(mot, st, ordine)
    st["psi_h"][...] = c_su_psi(st["psi_h"].reshape(-1), forma).reshape(forma)
    mot.geo.U[...] = c_su_U(mot.geo.U.copy())
    sc = float(np.max(np.abs(diretto)))
    return float(np.max(np.abs(st["psi_h"] + diretto))) / sc


def _prova_c(mot, st, forma, ordine):
    """### `max |W C W C psi + psi|`, ### **e il `+` e' `C^2 = -1`.**

    ### ⭐ **La prova non costruisce `C` come matrice:** applica `C`, il passo, `C`, il
    passo, e confronta con ### **`-psi`** — perche' `C^2 = -1` su `psi`, che e' un fatto
    derivato *(`sigma_y^* = -sigma_y`)* e **non una convenzione.**
    ### ⚠ **E `C` tocca ANCHE `U`**, che e' la parte che avevo dimenticato una volta.
    """
    r = np.random.default_rng(SEME + 1)
    v = (r.normal(size=forma) + 1j * r.normal(size=forma))
    st["psi_h"][...] = v
    st["phi_h"].fill(0)
    for _ in range(2):
        st["psi_h"][...] = c_su_psi(st["psi_h"].reshape(-1), forma).reshape(forma)
        mot.geo.U[...] = c_su_U(mot.geo.U.copy())
        passo(mot, st, ordine)
    sc = float(np.max(np.abs(v)))
    return float(np.max(np.abs(st["psi_h"] + v))) / sc


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 96)
    print("LO SPETTRO DEL PASSO LINEARE PALINDROMO -- una MISURA, nessuna decisione")
    print("=" * 96)
    print("  LA CONFIGURAZIONE: toro %s   seme = %d   dtau = %s   eps = %.1f"
          "   vuoto_modulo = %.1f   U in SU(2)"
          % (LATI, SEME, DTAU, EPS, VUOTO_MODULO))
    valida_la_misura()
    tab = []
    for dtau in DTAU:
        tab.append((dtau,) + prove(dtau))
    print("=" * 96)
    print("  LA TABELLA, in una riga per `dtau`. ### ATTENZIONE AL FATTORE 2: con l'ordine")
    print("  palindromo OGNI PEZZO sta a frazione 0.5, quindi un pezzo agisce a")
    print("  `theta = pi*dtau/2`, non a `pi*dtau`.")
    print("  %-7s %-11s %-11s %-11s %-6s %-11s %-11s %s"
          % ("dtau", "collo", "spaziatura", "collo/spaz", "molt.", "C W C-1=W-1",
             "senza mon.", "molt. senza / appaiam. senza"))
    for (dtau, dist, collo, spa, mm, sc, rotto, m_ug, s_senza, mm2, d2, s2,
         gol) in tab:
        print("  %-7.4f %-11.3e %-11.3e %-11.2f %-6d %-11.3e %-11.3e %d / %.3e (sp. %.3e)"
              % (dtau, collo, spa, collo / spa, mm, sc, s_senza, mm2, d2, s2))
    # ### ⛔ **E L-ASSERZIONE SUL GOLOSO STA QUI, non dentro `prove`:** <<il goloso
    # ### sbaglia>> ### **NON e- vero a OGNI `dtau`** -- a `dtau = 0.5` da- lo stesso
    # ### numero. ### ✅ **Cio- che e- vero, e che basta, e- che ALMENO A UN `dtau` il
    # ### goloso da- UN ALTRO VERDETTO**, e quello e- il `dtau` su cui avevo scritto la
    # ### frase sbagliata nella `RIPRESA`.
    # ### ⚠ **gli indici si contano dalla tupla, non a memoria:** la prima volta avevo
    # ### preso `x[11]` *(la spaziatura senza moneta)* per il goloso, ed e- `x[12]`.
    diversi = [(x[0], x[12], x[2], x[3]) for x in tab
               if abs(x[12] - x[2]) > x[3]]
    esito("### ALMENO A UN `dtau` il GOLOSO dava un altro verdetto",
          len(diversi) >= 1,
          "a %s: goloso %.3e contro collo %.3e, su spaziatura %.3e"
          % (diversi[0][0], diversi[0][1], diversi[0][2], diversi[0][3])
          if diversi else "nessuno: allora la cura non era necessaria")
    print("=" * 96)
    print("  %d su %d" % (OK[0], OK[1]))
    print("### ⛔ E NESSUNA CONCLUSIONE DI FISICA: i numeri sono questi, e la lettura")
    print("###   la decide Luca. Cio' che questo file NON dice e' se il modello DEVE")
    print("###   avere la C, la CT, o un'altra simmetria.")
    print("=" * 96)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
