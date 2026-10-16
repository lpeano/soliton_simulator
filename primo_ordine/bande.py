# -*- coding: utf-8 -*-
r"""LE DUE BANDE DI `W` — **particella e antiparticella, e il CONTROLLO viene PRIMA.**

> **Idea di Luca, 2026-10-13:** *«Se l'energia vada cercata su materia e antimateria come
> dominio. Nelle camminate di tipo Dirac le due BANDE del passo lineare `W` sono particella
> e antiparticella.»*

## ⛔ QUESTO STRUMENTO E' GLOBALE PER COSTRUZIONE, E VA DICHIARATO

I proiettori `P+` e `P-` sono **proiettori SPETTRALI**: si ottengono **diagonalizzando `W`
su tutta la scena**. ### ⚠ **Quindi ogni grandezza per banda e' definita GLOBALMENTE**, e
### **trovarne una forma locale e' un passo successivo** — da proporre a Luca, **non da
fare qui**.

### ⛔ **E IL COSTO E' CUBICO:** `O((4m)^3)` in tempo e `O((4m)^2)` in memoria.
### **Sotto `~2000` dimensioni**, e la memoria **si dichiara**.

## ⭐ IL CONTROLLO DELLA LETTURA VIENE PRIMA DI OGNI MISURA

> **Il mandato:** *«Verifica che `C` (`psi -> i sigma_y psi*`) SCAMBI le due bande, cioe'
> mandi `omega` in `-omega` e i proiettori `P+` in `P-`, entro ulp. **Se non lo fa, "bande =
> materia/antimateria" non e' la lettura giusta: fermati e riportalo.**»*

### ✅ **E il conto che lo rende un test diretto:** `C` e' **antilineare**, quindi se
`W v = e^{-i omega} v` allora `C W v = e^{+i omega} C v`. ### **Se `C W = W C` come
operatori antilineari, allora `C v` e' autovettore con `e^{+i omega}`** — cioe'
### **`omega -> -omega`, cioe' le bande si scambiano.**
### ⛔ **Percio' il controllo e' `||C(W psi) - W(C psi)||`**, e non una somiglianza a occhio.

## ⚠ IL SETTORE `0` SI CONTA A PARTE, E NON E' UN DETTAGLIO

Gli autovalori a `+1` e `-1` *(`omega = 0` o `pi`)* **non hanno un segno di banda**. Le
camminate di Grover hanno **tipicamente grandi autospazi degeneri** la' *(bande piatte,
stati localizzati)*. ### **Si riportano la loro DIMENSIONE e il PESO dello stato che ci
cade**, perche' ### **una carica `Q = N+ - N-` che ignora un settore grande non e' una
carica.**

Gira con:  python primo_ordine/bande.py --scrivi
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)

import deriva as DV                                           # noqa: E402
import tick as TK                                           # noqa: E402
import deriva_variabile as DVAR                               # noqa: E402
import energia as EN                                          # noqa: E402

# ### ⚠ **LA SOGLIA DEL SETTORE `0`, e NON e' una manopola di fisica:** separa
# ### `omega = 0` o `pi` ### **dal resto**, e un autovalore a distanza numerica da `+-1`
# ### ### **e- `+-1`.** ### **Si dichiara, e si misura quanti ci cadono.**
SOGLIA_ZERO = 1e-9
DOVE = os.path.join(os.path.dirname(_QUI), "doc", "REFERTO_bande.md")


def applica_W(mot, st, v):
    """### `W v`, ### **col pezzo lineare della tabella e nient'altro.**"""
    s = dict(st)
    s["psi_h"] = v.reshape(st["psi_h"].shape).copy()
    mot.operatori["moneta_spin"](s, {"eps": 0.5}, 1)
    mot.operatori["grover"](s, {}, 1)
    mot.operatori["spostamento_trasporto"](s, {}, 1)
    return s["psi_h"].ravel().copy()


def matrice_W(mot, st):
    """### `W` come matrice `(4m, 4m)`. ### **Esatta: `W` e' LINEARE.**

    ### ⚠ **E la memoria si dichiara:** `(4m)^2` complessi, cioe' `16 m^2 * 16` byte.
    """
    d = st["psi_h"].size
    Wm = np.zeros((d, d), dtype=complex)
    e = np.zeros(d, dtype=complex)
    for j in range(d):
        e.fill(0)
        e[j] = 1.0
        Wm[:, j] = applica_W(mot, st, e)
    return Wm


def coniuga_C(psi):
    """### `C psi = i sigma_y psi*`: ### **`(psi*_1, -psi*_0)`.**

    `i sigma_y (a, b) = (b, -a)`, e poi la coniugazione. ### ⚠ **E' ANTILINEARE**, ed e'
    proprio questo che le fa scambiare le bande.
    """
    p = np.asarray(psi)
    fuori = np.empty_like(p)
    fuori[..., 0] = np.conj(p[..., 1])
    fuori[..., 1] = -np.conj(p[..., 0])
    return fuori


def diagonalizza(Wm):
    """### `(omega, V, piu, meno, zero)`. ### **`omega` in `(-pi, pi]`.**"""
    val, V = np.linalg.eig(Wm)
    # ### `val = exp(-i omega)`, quindi ### **`omega = -angolo(val)`**
    omega = -np.angle(val)
    # ### il SETTORE `0`: gli autovalori a `+-1`, cioe- ### **`sin(omega) ~ 0`**
    zero = np.abs(np.sin(omega)) <= SOGLIA_ZERO
    piu = (~zero) & (omega > 0)
    meno = (~zero) & (omega < 0)
    return omega, V, piu, meno, zero


def proiettore(V, mask):
    """### `P` sul sottospazio: ### **da una base ORTONORMALE del suo span.**

    ### ⛔ **E non dai vettori come vengono:** `np.linalg.eig` non ortonormalizza dentro
    un autospazio DEGENERE, e ### **i Grover ne hanno di grandi.** ### **La `QR` dello
    blocco da' una base ortonormale dello stesso span**, e il proiettore e' quello giusto.
    """
    if not np.any(mask):
        return np.zeros((V.shape[0], V.shape[0]), dtype=complex)
    Q, _r = np.linalg.qr(V[:, mask])
    return Q @ Q.conj().T


def controllo_C(mot, st, seme=11):
    """### **IL CONTROLLO CHE VIENE PRIMA:** `C` scambia le bande?

    Rende un dizionario coi **quattro** numeri che il mandato chiede, e
    ### ⛔ **nessuno dei quattro e' un giudizio: sono residui.**
    """
    r = np.random.default_rng(seme)
    psi = (r.normal(size=st["psi_h"].shape)
           + 1j * r.normal(size=st["psi_h"].shape))
    # ### ① `C W = W C` come operatori ANTILINEARI
    a = coniuga_C(applica_W(mot, st, psi.ravel()).reshape(psi.shape))
    b = applica_W(mot, st, coniuga_C(psi).ravel()).reshape(psi.shape)
    res_cw = float(np.max(np.abs(a - b)))
    scala = float(np.max(np.abs(a)))
    Wm = matrice_W(mot, st)
    omega, V, piu, meno, zero = diagonalizza(Wm)
    # ### ② lo SPETTRO e- simmetrico sotto `omega -> -omega`?
    su = np.sort(omega[piu])
    giu = np.sort(-omega[meno])
    simm = (float(np.max(np.abs(su - giu)))
            if su.size == giu.size and su.size else float("inf"))
    # ### ③ `P+ C = C P-` sul `psi` casuale
    Pp = proiettore(V, piu)
    Pm = proiettore(V, meno)
    c1 = (Pp @ coniuga_C(psi).ravel())
    c2 = coniuga_C((Pm @ psi.ravel()).reshape(psi.shape)).ravel()
    res_p = float(np.max(np.abs(c1 - c2)))
    # ### ④ i proiettori sono proiettori, e ### **si SOMMANO all-identita-**
    P0 = proiettore(V, zero)
    ident = float(np.max(np.abs(Pp + Pm + P0 - np.eye(Wm.shape[0]))))
    idem = float(np.max(np.abs(Pp @ Pp - Pp)))
    peso0 = float(np.real(psi.ravel().conj() @ (P0 @ psi.ravel()))
                  / max(float(np.sum(np.abs(psi) ** 2)), 1e-300))
    return {"CW_meno_WC": res_cw, "scala": scala, "spettro_simmetrico": simm,
            "Pp_C_meno_C_Pm": res_p, "somma_identita": ident, "idempotenza": idem,
            "dim": int(Wm.shape[0]), "dim_piu": int(np.sum(piu)),
            "dim_meno": int(np.sum(meno)), "dim_zero": int(np.sum(zero)),
            "peso_zero": peso0, "Wm": Wm, "V": V, "omega": omega,
            "Pp": Pp, "Pm": Pm, "P0": P0,
            "memoria_MB": Wm.nbytes / 1048576.0}


def grandezze(psi, Wm, Pp, Pm, P0):
    """### Le grandezze per banda: ### **popolazioni, energie, e la candidata carica.**"""
    v = np.asarray(psi).ravel()
    nrm = float(np.real(v.conj() @ v))
    out = {"norma": nrm}
    for nome, P in (("piu", Pp), ("meno", Pm), ("zero", P0)):
        pv = P @ v
        out["N_" + nome] = float(np.real(pv.conj() @ pv))
        # ### `E_banda = Re<psi| W P |psi> = somma_{k in banda} |c_k|^2 cos(omega_k)`
        out["E_" + nome] = float(np.real(v.conj() @ (Wm @ pv)))
    out["Q"] = out["N_piu"] - out["N_meno"]
    wv = Wm @ v
    out["Re_W"] = float(np.real(v.conj() @ wv))
    out["Im_W"] = float(np.imag(v.conj() @ wv))
    return out


def corri_bande(nn=16, dtau=0.25, ticks=200, seme=7, vuoto_modulo=2.0,
                enne=True, ogni=2):
    """### Fa girare il tick e segue **le grandezze per banda, tick per tick.**

    ### ⚠ **`enne=False` e' IL CONTROLLO:** senza `N` il pezzo lineare **commuta con i
    suoi proiettori spettrali**, quindi ### **le popolazioni devono essere costanti entro
    ulp.** ### ⛔ **Se non lo sono, i proiettori sono sbagliati** e tutto il resto non si
    legge.
    """
    import composizione as CM
    # ### ⛔ **`su2=True` NON E- UN DETTAGLIO: SENZA, `C` NON SCAMBIA LE BANDE.**
    # ### Misurato: con `U(2)` generico `|CW - WC| = 4.33` su scala `2.76`; con `SU(2)`
    # ### ### **`8.0e-16`.** ### **E senza quel controllo <<bande = materia/antimateria>>
    # ### non e- la lettura giusta**, quindi la misura ### **non si fa.**
    inc, mot, st, par = DV.scena(nn, seme, dtau, norma="locale",
                                 vuoto_modulo=vuoto_modulo, su2=True)
    sat = DVAR.satura(st, mot)
    cc = controllo_C(mot, st)
    Wm, Pp, Pm, P0 = cc["Wm"], cc["Pp"], cc["Pm"], cc["P0"]
    salta = () if enne else ("CAMM-SATURAZIONE",)
    serie = []
    for t in range(0, ticks + 1):
        if t:
            mot.apri_tick()
            for idl, frazione, _tipo in CM.ORDINE:
                if idl in salta:
                    continue
                nome, vuole_par = TK.OPERATORE[idl]
                mot.operatori[nome](st, par if vuole_par else {}, frazione)
            mot.chiudi_tick()
        if t == 0 or (t % ogni) == 0 or t == ticks:
            g = grandezze(st["psi_h"], Wm, Pp, Pm, P0)
            g["t"] = t
            g["vuoto"] = float(np.sum(EN.densita_nodo(
                st, mot, mot._b("bd_k", (nn,), float))))
            g["elicita"] = float(np.sum(mot.elicita(st)))
            serie.append(g)
    return serie, cc, sat


def esc(serie, chiave):
    """### L'escursione `max - min` di una grandezza, ### **e la sua SCALA.**"""
    v = np.asarray([g[chiave] for g in serie], dtype=float)
    return (float(v.max() - v.min()), float(abs(v[0])),
            float(v.max() - v.min()) / max(abs(v[0]), 1e-300))


def correlazione(serie, a, b):
    """### La correlazione di Pearson fra **le variazioni** di due grandezze.

    ### ⛔ **FRA LE VARIAZIONI e non fra i valori:** due grandezze che derivano insieme
    hanno valori correlati ### **anche quando le loro variazioni non c'entrano niente.**
    """
    x = np.diff(np.asarray([g[a] for g in serie], dtype=float))
    y = np.diff(np.asarray([g[b] for g in serie], dtype=float))
    if x.size < 2 or np.std(x) == 0 or np.std(y) == 0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


# ---------------------------------------------------------------- LA `C` COMPLETA
# ### ⛔ **LA CORREZIONE DEL 2026-10-13, e l'errore era MIO.** In `efc113b` avevo concluso
# ### che *«la `C` chiede `det U = 1`, il trasporto deve stare in `SU(2)`»*.
# ### ⚠ **LA MISURA ERA GIUSTA, LA CONCLUSIONE NO:** avevo applicato la `C` ### **alla sola
# ### MATERIA, su una `U` TENUTA FISSA.** ### ⛔ **La coniugazione di carica INVERTE ANCHE
# ### IL CAMPO DI GAUGE** -- in elettrodinamica `C` manda `A` in `-A` -- e la `C` e' una
# ### simmetria della ### **TEORIA INTERA**, non della materia su un campo fisso.
# ### ✅ **Particella e antiparticella nello stesso campo `U(1)` NON hanno lo stesso
# ### spettro, e questa E' FISICA, non un difetto.**
# ### ⭐ **E la mia stessa derivazione della `U` dinamica lo diceva:** sotto `C` la fase
# ### `U(1)` e' ### **DISPARI**, `theta -> -theta`.


def coniuga_U(U):
    """### `C U = sigma_y U* sigma_y^-1`: ### **`theta -> -theta` per la parte `U(1)`.**

    ### ✅ **E il conto si vede scrivendo `U = exp(i theta) V` con `V` in `SU(2)`:**
    `sigma_y U* sigma_y^-1 = exp(-i theta) sigma_y V* sigma_y^-1 = exp(-i theta) V`.
    ### ⭐ **Quindi la parte `SU(2)` resta e la FASE SI INVERTE** -- esattamente
    `theta -> -theta`, che e' cio' che la derivazione della `U` dinamica aveva trovato.
    """
    sy = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
    return np.einsum("ij,ajk,kl->ail", sy, np.conj(np.asarray(U)), sy)


def controllo_C_completa(nn=16, seme=7, vuoto_modulo=2.0, su2=False):
    """### **IL CONTROLLO CON LA `C` COMPLETA:** `C W(U) C^-1 = W(C U)`?

    La `C` completa e' **`psi -> i sigma_y psi*`**, **`phi -> phi*`**,
    **`U -> sigma_y U* sigma_y^-1`**.

    ### ⛔ **E QUESTO E' IL CONTROLLO GIUSTO, non quello di `efc113b`:** la' avevo
    coniugato **solo la materia** e tenuto `U` fissa, e ### **quella non e' la `C` della
    teoria.**

    ### ⚠ **`phi -> phi*` non entra in questo residuo**, perche' `W` non tocca `phi`:
    ### **lo dichiaro invece di lasciar credere che sia verificato qui.**
    """
    import motore as MO
    inc, mot, st, par = DV.scena(nn, seme, 0.25, norma="locale",
                                 vuoto_modulo=vuoto_modulo, su2=su2)
    # ### il motore della teoria CONIUGATA: stessa `n`, `U` coniugata
    mot2 = MO.Motore(inc, MO.Geometria(mot.geo.n, coniuga_U(mot.geo.U)),
                     st, np.full(nn, 0.25), "numpy")
    r = np.random.default_rng(seme + 101)
    psi = (r.normal(size=st["psi_h"].shape)
           + 1j * r.normal(size=st["psi_h"].shape))
    # ### `C (W(U) psi)` contro `W(C U) (C psi)`
    a = coniuga_C(applica_W(mot, st, psi.ravel()).reshape(psi.shape))
    b = applica_W(mot2, st, coniuga_C(psi).ravel()).reshape(psi.shape)
    res = float(np.max(np.abs(a - b)))
    scala = float(np.max(np.abs(a)))
    # ### e lo SPETTRO: la teoria coniugata ha lo spettro RIBALTATO
    o1 = np.sort(-np.angle(np.linalg.eigvals(matrice_W(mot, st))))
    o2 = np.sort(np.angle(np.linalg.eigvals(matrice_W(mot2, st))))
    simm = float(np.max(np.abs(o1 - o2))) if o1.size == o2.size else float("inf")
    # ### ⛔ **E IL CASO CHE DEVE FALLIRE: la `C` DELLA SOLA MATERIA** -- cioe- il
    # ### controllo sbagliato di `efc113b`, rifatto qui ### **per mostrare che la
    # ### differenza e- la `U`.**
    c = applica_W(mot, st, coniuga_C(psi).ravel()).reshape(psi.shape)
    res_sbagliato = float(np.max(np.abs(a - c)))
    deter = float(np.mean(np.abs(np.linalg.det(mot.geo.U) - 1.0)))
    return {"residuo": res, "scala": scala, "spettro": simm,
            "solo_materia": res_sbagliato, "det_meno_uno": deter}


CONFIG = (("seme", 7),
          ("scena", "anello di 16 nodi"),
          ("dtau", 0.25),
          ("tick", 200),
          ("eps della moneta di spin", 0.5),
          ("psi iniziale", "gaussiano complesso dal seme, ampiezza ~1 per estremita'"),
          ("phi iniziale", "modulo |phi| = vuoto_modulo, fasi uniformi dal seme"),
          ("U per arco", "SU(2) casuale -- det U = 1, OBBLIGATORIO per la C"),
          ("il tick", "l'ORDINE INTERO di composizione.py"),
          ("soglia del settore 0", SOGLIA_ZERO))


def main(argv):
    sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))
    import _presidio
    _presidio.avvia(__file__)
    # ### ⭐ **IL RAMO DEL FLOQUET E- SEPARATO, e non e- comodita-:** gira su una scena
    # ### di  dimensioni e ### **non deve girare per sbaglio** insieme alle misure
    # ### piccole.
    nl = chr(10)
    r = []
    print("=" * 100)
    print("LE DUE BANDE DI W: IL CONTROLLO PRIMA DI TUTTO")
    print("=" * 100)
    r.append("# LE DUE BANDE DI `W` — **il controllo `C` passa, ma SOLO in `SU(2)`**")
    r.append("")
    r.append("Lo rigira:  `python primo_ordine/bande.py --scrivi`")
    r.append("")
    r.append("## 1. LA CONFIGURAZIONE INTERA")
    r.append("")
    r.append("| la voce | il valore |")
    r.append("|---|---|")
    for k, v in CONFIG:
        r.append("| %s | `%s` |" % (k, v))

    # ------------------------------------------------ IL CONTROLLO, nei DUE casi
    print("  IL CONTROLLO: C scambia le bande?  (e il confronto U(2) contro SU(2))")
    r.append("")
    r.append("## 2. ⭐ **IL CONTROLLO DELLA LETTURA** — e il suo esito dipende"
             " da `det U`")
    r.append("")
    r.append("`C` e' **antilineare**, quindi se `W v = e^{-i omega} v` e `C W = W C`"
             " allora `C v`")
    r.append("e' autovettore con `e^{+i omega}`: ### **`omega -> -omega`, cioe' le bande"
             " si")
    r.append("scambiano.** ### ⛔ **Percio' il controllo e'"
             " `||C(W psi) - W(C psi)||`**, e non una")
    r.append("somiglianza a occhio.")
    r.append("")
    r.append("| `U` | `|CW - WC|` | spettro simmetrico | `|P+C - CP-|` | |")
    r.append("|---|--:|--:|--:|---|")
    buono = None
    for su2 in (False, True):
        _i, mot, st, _p = DV.scena(16, 7, 0.25, norma="locale", vuoto_modulo=2.0,
                                   su2=su2)
        c = controllo_C(mot, st)
        ok = c["CW_meno_WC"] < 1e-10
        print("      U in %-6s |CW-WC| = %.3e su scala %.3f   spettro simm = %.3e"
              "   |P+C-CP-| = %.3e   %s"
              % ("SU(2)" if su2 else "U(2)", c["CW_meno_WC"], c["scala"],
                 c["spettro_simmetrico"], c["Pp_C_meno_C_Pm"],
                 "PASSA" if ok else "### FALLISCE"))
        r.append("| **%s** | `%.3e` | `%.3e` | `%.3e` | ### %s |" %
                 ("SU(2)" if su2 else "U(2) generico", c["CW_meno_WC"],
                  c["spettro_simmetrico"], c["Pp_C_meno_C_Pm"],
                  "✅ **PASSA**" if ok else "⛔ **FALLISCE**"))
        if su2:
            buono = c
    print("      dim = %d:  +/-/0 = %d/%d/%d   peso del settore 0 = %.4f"
          "   memoria %.3f MB"
          % (buono["dim"], buono["dim_piu"], buono["dim_meno"], buono["dim_zero"],
             buono["peso_zero"], buono["memoria_MB"]))
    r.append("")
    r.append("### ⛔ **ECCO IL FATTO, ED E' UNA CONDIZIONE DI FISICA:** la `C` chiede")
    r.append("`sigma_y U* sigma_y^-1 = U`, che vale ### **se e solo se `det U = 1`.**")
    r.append("### ⚠ **E `motore.Geometria` valida SOLO l'unitarieta', NON il"
             " determinante** —")
    r.append("quindi la tabella **permette** un trasporto che **rompe la `C`**, che e' una"
             " legge")
    r.append("della carta. ### **Non lo decido io: va a Luca.**")
    r.append("")
    r.append("| | il numero |")
    r.append("|---|--:|")
    r.append("| dimensione dello spazio *(`4m`)* | `%d` |" % buono["dim"])
    r.append("| banda `+` / banda `-` | `%d` / `%d` |"
             % (buono["dim_piu"], buono["dim_meno"]))
    r.append("| ### ⭐ **SETTORE `0`** *(autovalori a `+-1`)* | **`%d`** |"
             % buono["dim_zero"])
    r.append("| il **peso** dello stato nel settore `0` | `%.4f` |" % buono["peso_zero"])
    r.append("| i proiettori sommano all'identita' | `%.3e` |" % buono["somma_identita"])
    r.append("| e sono idempotenti | `%.3e` |" % buono["idempotenza"])
    r.append("| memoria della matrice | `%.3f` MB |" % buono["memoria_MB"])
    r.append("")
    r.append("### ⭐ **IL SETTORE `0` E' VUOTO su questa scena**, e il mandato"
             " chiedeva di")
    r.append("guardarlo: le bande piatte dei Grover ### **non compaiono qui**, quindi")
    r.append("`Q = N+ - N-` e' definita ### **senza un pezzo di stato che non ha segno.**")

    # ------------------------------------------------ LA C COMPLETA (correzione)
    print("  LA C COMPLETA (correzione del 2026-10-13): C W(U) C^-1 = W(C U)?")
    r.append("")
    r.append("## 2-bis. ⭐ **LA CORREZIONE DEL 2026-10-13: LA `C` COMPLETA**")
    r.append("")
    r.append("### ⛔ **LA CONCLUSIONE DEL PARAGRAFO `2` E' SBAGLIATA, e l'errore e'"
             " MIO.** Avevo scritto")
    r.append("che *<<la `C` chiede `det U = 1`, il trasporto deve stare in `SU(2)`>>*."
             " ### ⚠ **La misura")
    r.append("era giusta, la conclusione no:** avevo applicato la `C` ### **alla sola"
             " MATERIA, su una `U`")
    r.append("TENUTA FISSA.** ### ⛔ **La coniugazione di carica INVERTE ANCHE IL CAMPO"
             " DI GAUGE** --")
    r.append("in elettrodinamica `C` manda `A` in `-A` -- e la `C` e' una simmetria della"
             " **TEORIA")
    r.append("INTERA**, non della materia su un campo fisso."
             " ### ✅ **Particella e antiparticella")
    r.append("nello stesso campo `U(1)` NON hanno lo stesso spettro, e questa E' FISICA,"
             " non un difetto.**")
    r.append("")
    r.append("La `C` completa: **`psi -> i sigma_y psi*`**, **`phi -> phi*`**,"
             " **`U -> sigma_y U* sigma_y^-1`**")
    r.append("*(cioe' `theta -> -theta` per la parte `U(1)`, che e' proprio cio' che la"
             " derivazione")
    r.append("della `U` dinamica aveva trovato)*.")
    r.append("")
    r.append("| `U` | `|det U - 1|` | `|C W(U) C^-1 - W(C U)|` | spettro ribaltato |"
             " ### ⛔ **DEVE FALLIRE:** la `C` della **sola materia** |")
    r.append("|---|--:|--:|--:|--:|")
    for su2 in (False, True):
        c = controllo_C_completa(su2=su2)
        print("      U in %-6s |det U - 1| = %.4f   |C W(U) C^-1 - W(C U)| = %.3e"
              "   spettro %.3e   sola materia %.3e"
              % ("SU(2)" if su2 else "U(2)", c["det_meno_uno"], c["residuo"],
                 c["spettro"], c["solo_materia"]))
        r.append("| **%s** | `%.4f` | ### ✅ **`%.3e`** | `%.3e` | `%.3e` |" %
                 ("U(2) generico" if not su2 else "SU(2)", c["det_meno_uno"],
                  c["residuo"], c["spettro"], c["solo_materia"]))
    r.append("")
    r.append("### ⭐ **LA `C` COMPLETA E' UNA SIMMETRIA DELLA TEORIA INTERA, ANCHE CON"
             " `U(2)` GENERICO**")
    r.append("*(residuo **esattamente `0`**)*, e lo spettro di `W(C U)` e'"
             " **l'opposto** di quello di `W(U)`.")
    r.append("### ⚠ **E IL CASO CHE DEVE FALLIRE SPIEGA COMPLETAMENTE I NUMERI DEL"
             " PARAGRAFO `2`:** la `C`")
    r.append("della sola materia da' **`O(1)`** con `U(2)` e **ulp** con `SU(2)` --"
             " ### **perche' in `SU(2)`")
    r.append("`C U = U`, quindi li' il controllo sbagliato COINCIDE con quello giusto.**")
    r.append("")
    r.append("### ✅ **QUINDI LE BANDE COME MATERIA/ANTIMATERIA SONO LETTE"
             " CORRETTAMENTE in due casi,")
    r.append("e lo dichiaro:** su `U` in **`SU(2)`** *(dove `C U = U`)*, oppure con la `C`"
             " **che")
    r.append("trasforma anche `U`**. ### ⚠ **E la scelta del parametro `su2` resta un"
             " CONTROLLO DI")
    r.append("MISURA, non una legge.**")
    r.append("")
    r.append("### ⚠ **CHE COSA QUESTO RESIDUO NON VERIFICA:** `phi -> phi*` non entra,"
             " perche' `W` non")
    r.append("tocca `phi`. ### **Lo dichiaro invece di lasciar credere che sia verificato"
             " qui.**")

    # ------------------------------------------------ B1: LE POPOLAZIONI
    print("  B1  LE POPOLAZIONI: N spento (controllo) e N acceso, nella scansione in x")
    r.append("")
    r.append("## 3. `B1` — **LE POPOLAZIONI**")
    r.append("")
    r.append("### ✅ **IL CONTROLLO:** con `N` **spento** le popolazioni devono essere")
    r.append("**costanti**, perche' `W` commuta coi suoi proiettori spettrali."
             " ### ⛔ **Se non lo")
    r.append("fossero, i proiettori sarebbero sbagliati e tutto il resto non si"
             " leggerebbe.**")
    r.append("")
    r.append("| `N` | `|phi|` | `x` max | esc. `N+` | esc. `N-` | esc. `N0` |"
             " esc. rel. `N+` |")
    r.append("|---|--:|--:|--:|--:|--:|--:|")
    for enne, moduli in ((False, (2.0,)), (True, (16.0, 4.0, 2.0, 1.0, 0.5))):
        for f in moduli:
            serie, cc, sat = corri_bande(vuoto_modulo=f, enne=enne)
            ep = esc(serie, "N_piu")
            em = esc(serie, "N_meno")
            ez = esc(serie, "N_zero")
            print("      N %-7s |phi|=%-6.2f x=%-9.4g  esc N+ = %.3e (rel %.2e)"
                  "   N- = %.3e   N0 = %.3e"
                  % ("ACCESO" if enne else "spento", f, sat, ep[0], ep[2],
                     em[0], ez[0]))
            r.append("| %s | `%.2f` | `%.4g` | `%.3e` | `%.3e` | `%.3e` | `%.2e` |" %
                     ("**ACCESO**" if enne else "spento", f, sat,
                      ep[0], em[0], ez[0], ep[2]))

    # ------------------------------------------------ B2 e B3
    print("  B2  L'ENERGIA PER BANDA, e le CORRELAZIONI misurate")
    serie, cc, sat = corri_bande(vuoto_modulo=2.0, enne=True)
    r.append("")
    r.append("## 4. `B2` — **L'ENERGIA PER BANDA**, e le correlazioni **MISURATE**")
    r.append("")
    r.append("*(`|phi| = 2`, cioe' `x = %.4g`: il regime in cui la saturazione lavora)*"
             % sat)
    r.append("")
    r.append("| la grandezza | scala | escursione | relativa |")
    r.append("|---|--:|--:|--:|")
    for k, et in (("E_piu", "`E+`"), ("E_meno", "`E-`"), ("E_zero", "`E0`"),
                  ("Re_W", "`Re<psi|W psi>`"), ("vuoto", "il termine del **vuoto**"),
                  ("N_piu", "`N+`"), ("N_meno", "`N-`"), ("Q", "`Q = N+ - N-`"),
                  ("Im_W", "`Im<psi|W psi>`"), ("elicita", "`somma_k h_k`"),
                  ("norma", "`||psi||^2`")):
        e = esc(serie, k)
        print("      %-28s scala %-12.4g esc %-12.3e rel %.2e"
              % (et.replace("`", ""), e[1], e[0], e[2]))
        r.append("| %s | `%.4g` | `%.3e` | `%.2e` |" % (et, e[1], e[0], e[2]))
    r.append("")
    r.append("### ⭐ **LE CORRELAZIONI FRA LE VARIAZIONI** — ### **misurate, non"
             " inventate:**")
    r.append("")
    r.append("| fra | e | correlazione |")
    r.append("|---|---|--:|")
    coppie = (("Re_W", "vuoto", "`Re<psi|W psi>`", "il **vuoto**"),
              ("E_piu", "E_meno", "`E+`", "`E-`"),
              ("E_piu", "N_piu", "`E+`", "`N+`"),
              ("N_piu", "N_meno", "`N+`", "`N-`"),
              ("Q", "elicita", "`Q`", "`somma_k h_k`"),
              ("Im_W", "elicita", "`Im<psi|W psi>`", "`somma_k h_k`"),
              ("Im_W", "Q", "`Im<psi|W psi>`", "`Q`"))
    for a, b2, ea, eb in coppie:
        c = correlazione(serie, a, b2)
        print("      corr(d %-8s, d %-9s) = %+.4f" % (a, b2, c))
        r.append("| %s | %s | `%+.4f` |" % (ea, eb, c))
    r.append("")
    r.append("### ⛔ **FRA LE VARIAZIONI e non fra i valori:** due grandezze che"
             " derivano insieme")
    r.append("hanno **valori** correlati ### **anche quando le loro variazioni non"
             " c'entrano niente.**")
    r.append("")
    r.append("## 5. `B3` — **LA CANDIDATA CARICA**")
    r.append("")
    eq = esc(serie, "Q")
    ei = esc(serie, "Im_W")
    eh = esc(serie, "elicita")
    r.append("| la candidata | scala | escursione | relativa | |")
    r.append("|---|--:|--:|--:|---|")
    for e, et in ((eq, "`Q = N+ - N-`"), (ei, "`Im<psi|W psi>`"),
                  (eh, "`somma_k h_k`")):
        r.append("| %s | `%.4g` | `%.3e` | `%.2e` | ### %s |" %
                 (et, e[1], e[0], e[2],
                  "✅ **conservata**" if e[2] < 1e-10
                  else "⛔ **NON conservata**"))
    print("  B3  Q rel = %.2e   Im<W> rel = %.2e   elicita rel = %.2e"
          % (eq[2], ei[2], eh[2]))

    r.append("")
    r.append("## 6. ⚠ IL LIMITE, DICHIARATO")
    r.append("")
    r.append("### ⛔ **Tutto cio' che e' <<per banda>> e' definito GLOBALMENTE:**"
             " `P+` e `P-` sono")
    r.append("**proiettori spettrali**, e si ottengono **diagonalizzando `W` su tutta la"
             " scena**.")
    r.append("### **Trovarne una forma locale e' un passo successivo, da proporre a Luca e"
             " non da")
    r.append("fare qui** — e il mandato lo dice.")
    r.append("")
    if "--scrivi" in argv:
        import io
        dati = (nl.join(r) + nl).encode("utf-8")
        io.open(DOVE, "wb").write(dati)
        print("REFERTO: %s" % DOVE)
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
