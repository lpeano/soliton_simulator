# -*- coding: utf-8 -*-
r"""**IL GENERATORE PESATO `G`, `Omega`, E LA FASE CHE NE VIENE** — *la strada `(d)`*.

> ### ⭐⭐ **Decisione di Luca del `2026-10-18`, `00:07`:** l'energia che il passo deve
> conservare e'
>
> ```
> G = somma_k cs_k * H_k(nodo)  +  somma_a w_a * H_a(arco)
> ```
>
> con `w_a` ### **il peso d'arco che il passo GIA' usa** *(la media armonica `B-3`)*.
> ### **Con `cs` uniforme `G = c H_tot`**, e la decisione `QC` resta vera in quel caso.

## ⛔⛔ PERCHE' NASCE UN TERMINE NUOVO

`G` dipende da `phi` ### **in DUE modi**: dentro gli `H`, e dentro i pesi *(attraverso
`Lambda_k = somma_{h in k} |phi_h|^2`)*. ### **Il secondo non era implementato**, e il
gradiente che ne viene e'

```
(dG/dphi*_h)_peso = Omega_k * phi_h          (h nel nodo k)
Omega_k = cs'(Lambda_k) * [ H_k(nodo) + somma_{a in k} (dw_a/dcs_k) * H_a(arco) ]
cs'(Lambda) = Lambda_c / (Lambda + Lambda_c)^2
```

### ✅ **Cioe' UNA FASE, uguale per tutte le estremita' dello stesso nodo**, e
### **`psi` non si tocca.** ### **Nessuna costante nuova:** `cs'` e' la derivata della
forma gia' scelta, e `dw_a/dcs_k` la derivata del peso che il passo gia' usa.

## ⛔ IL TEMPO E' `dtau`, NON `dtau_nodo`

I pezzi di oggi applicano `exp(-i H_k dtau_nodo)` con `dtau_nodo = dtau cs_k`, che e'
### **`exp(-i (cs_k H_k) dtau)`**: ### **il parametro di flusso della composizione e' il
TICK**, e il generatore e' `cs_k H_k`. ### **Questo pezzo e' un altro addendo dello STESSO
generatore**, quindi si integra per ### **`dtau * frazione`.**
### ⚠ **Con `dtau_nodo` sarebbe `cs_k Omega_k`, cioe' UN'ALTRA legge** — e il collaudo del
tempo proprio ### **non lo vedrebbe**, perche' anche quella dipende da `dtau`.

## ⛔⛔ E IL FLUSSO NON E' ESATTO — *errore `n.10` del guardiano, misurato*

### ✅ **La fase e' PURA** *(nessun modulo cambia, quindi `M` e `V` restano al bit)*.
### ⛔ **Ma `Omega` SI MUOVE durante il pezzo**, e si sa esattamente per dove:

| il termine | lo muove una fase uniforme nel nodo? | misurato |
|---|---|---|
| `H(nodo)` *(i due Grover, la moneta, `N`)* | ### **NO** | `1.4e-14` su scala `5.8e+01` |
| `H(arco)` *(i due spostamenti)* | ### **SI'** | `1.5e+01` su scala `4.8e+01` |

### ⭐ **E il <<NO>> e' ESATTO, non numerico:** nel nodo la fase e' ### **la stessa per
tutte le estremita'**, quindi `|phi_h|` non cambia *(e con lui `Lambda` e `N`)* e
### **`|somma_h phi_h|^2` nemmeno** — la fase ### **esce dalla somma.** ### ⛔ **Sull'arco
no:** i due capi stanno in ### **nodi DIVERSI**, quindi la fase ### **RELATIVA** cambia.
### ✅ **Quindi il pezzo si integra col PUNTO MEDIO IMPLICITO**, a punto fisso: e'
### **del secondo ordine e REVERSIBILE**, cioe' ### **non rompe il palindromo.**

## ⚠ E QUESTO MODULO E' L'UNICA FONTE DEI TERMINI DI `H`

`_misura_mb2.pezzi_di_h` ### **lo LEGGE** invece di ricopiarlo, e `_misura_mb2.h_tot`
resta ### **una seconda fonte DICHIARATA** che si confronta ### **a ogni corsa.**
"""
import numpy as np

import flussi_parziali as FP

# ### ⛔ **`OMEGA_H` E' `pi` E NON E' UNA SCELTA:** `flussi_parziali.espi` applica
# ### ### **`e^{i pi s}`**, quindi il generatore dei pezzi di nodo e d'arco porta
# ### ### **`pi`** davanti. ### **Si legge dal codice che gira, non si tara.**
OMEGA_H = float(np.pi)
# ### ⛔ **IL TETTO DEI GIRI DEL PUNTO MEDIO, e NON e' una manopola:** e' ### **il numero
# ### oltre il quale si DICHIARA che non converge**, come `GIRI_MAX` di `tick.py`.
# ### ⚠ **Misurato il `2026-10-18`: il massimo osservato e' scritto nel referto.**
GIRI_MAX_OMEGA = 120
EPS_OMEGA = 8.0 * float(np.finfo(float).eps)


def _per_nodo(mot, v, fuori):
    """### La somma di una grandezza di ESTREMITA' ### **sul suo nodo.**"""
    fuori.fill(0.0)
    np.add.at(fuori, mot.inc.nodo, v)
    return fuori


def termini_di_h(mot, st, par):
    """### `(per_nodo, per_arco)`: ### **i termini di `H`, NON sommati e NON pesati.**

    ### ⛔⛔ **LA DIVISIONE IN DUE GRUPPI NON E' UNA SCELTA: E' LA MAPPA PEZZO -> PESO**,
    letta da `flussi_parziali`. ### **NODO:** i due Grover *(via `z_nodo`)*, la moneta
    *(via `dtau_nodo`)*, l'accoppiamento `N` *(via `dtau_nodo`)*. ### **ARCO:** i due
    spostamenti *(via `z_arco`, la media ARMONICA di `B-3`)*.
    ### ⚠ **E la moneta porta `eps`, che NON e' una costante nuova:** e' il parametro
    ### **di `CAMM-MONETA-SPIN`**, e arriva dal `par` del tick.
    """
    inc = mot.inc
    psi, phi = st["psi_h"], st["phi_h"]
    m = inc.m
    U = mot.geo.U
    # ------------------------------------------------- i termini di NODO
    nrm_psi = _per_nodo(mot, np.abs(psi[:, 0]) ** 2 + np.abs(psi[:, 1]) ** 2,
                        mot._b("ep_nrm_psi", (inc.n,), float))
    nrm_phi = _per_nodo(mot, np.abs(phi) ** 2, mot._b("ep_nrm_phi", (inc.n,), float))
    S_psi = np.zeros((inc.n, 2), dtype=complex)
    np.add.at(S_psi, inc.nodo, psi)
    S_phi = np.zeros(inc.n, dtype=complex)
    np.add.at(S_phi, inc.nodo, phi)
    d = inc.grado.astype(float)
    pu_psi = (np.abs(S_psi[:, 0]) ** 2 + np.abs(S_psi[:, 1]) ** 2) / d
    pu_phi = np.abs(S_phi) ** 2 / d
    per_nodo = -OMEGA_H * ((nrm_psi - pu_psi) + (nrm_phi - pu_phi))
    # ### la MONETA: `elicita` e' ### **GIA' SOMMATA PER NODO**, e il peso che legge e'
    # ### `dtau_nodo`, cioe' il peso del NODO.
    h = mot.elicita(st)
    assert h.shape == (inc.n,), (
        "`elicita` ha forma %r invece di `(n,)`: se tornasse per ESTREMITA' andrebbe"
        " raccolta sui nodi, e questo termine starebbe pesato SBAGLIATO" % (h.shape,))
    eps = par.get("eps")
    assert eps is not None, (
        "`Omega` vuole `eps` dal `par` del tick: senza, il termine della moneta"
        " sparirebbe da `H` IN SILENZIO -- e `Omega` sarebbe quello di un'altra energia")
    per_nodo = per_nodo + float(eps) * h
    # ### l'ACCOPPIAMENTO `N`, per nodo: ### **la forma che gira**, non una sua copia
    rho, lam = nrm_psi, nrm_phi
    N = np.zeros(inc.n, dtype=float)
    vivi = rho > 0.0
    if np.any(vivi):
        N[vivi] = rho[vivi] * np.log(rho[vivi] / (rho[vivi] + lam[vivi]))
    per_nodo = per_nodo + N
    # ------------------------------------------------- i termini di ARCO
    v = psi.reshape(m, 2, 2)
    p0, p1 = v[:, 0, :], v[:, 1, :]
    incro = np.einsum("ai,aji,aj->a", np.conj(p0), np.conj(U), p1)
    nrm_a = (np.abs(p0) ** 2).sum(axis=1) + (np.abs(p1) ** 2).sum(axis=1)
    arco_psi = (nrm_a - 2.0 * np.real(incro)) / 2.0
    w = phi.reshape(m, 2)
    f0, f1 = w[:, 0], w[:, 1]
    arco_phi = (np.abs(f0) ** 2 + np.abs(f1) ** 2
                - 2.0 * np.real(np.conj(f0) * f1)) / 2.0
    per_arco = -OMEGA_H * (arco_psi + arco_phi)
    return per_nodo, per_arco


def pesi(mot):
    """### `(w_nodo, w_arco)`: ### **i pesi che IL PASSO usa**, come rapporto.

    ### ⛔⛔ **PERCHE' UN RAPPORTO E NON UNA FORMULA:** la media armonica di `B-3` vive
    in `flussi_parziali.s_arco`, e ### **riscriverla qui sarebbe una SECONDA FONTE della
    legge** *(`STRUMENTO-LEGGE-DALLA-TABELLA`)*. ### **Il rapporto chiama due volte la
    stessa funzione** — una con `cs` acceso e una spento — e ### **misura il peso invece
    di dedurlo.**
    """
    salvo = mot.cs
    sn_con = FP.s_nodo(mot).copy()
    sa_con = FP.s_arco(mot).copy()
    mot.cs = None
    sn_senza = FP.s_nodo(mot).copy()
    sa_senza = FP.s_arco(mot).copy()
    mot.cs = salvo
    return sn_con / sn_senza, sa_con / sa_senza


def d_peso_arco(mot):
    """### `dw_a/dcs_k` ### **PER ESTREMITA'**, cioe' `2 cs_altro^2 / (cs_i + cs_j)^2`.

    ### ⭐ **E' la derivata della MEDIA ARMONICA `w = 2 cs_i cs_j/(cs_i + cs_j)`**, e
    ### **non e' una formula nuova: e' la derivata di quella che il passo usa.**
    ### ✅ **VERIFICATA contro la differenza finita di `FP.s_arco`** *(`1.3e-07` con
    `h = 1e-7`)*, e l'omogeneita' di grado `1` *(`cs_i w_i + cs_j w_j = w`)* regge
    ### **al bit** *(`2.2e-16`)*.
    ### ⭐ **E PER ESTREMITA' il CAPPIO si risolve da se':** se i due capi stanno nello
    stesso nodo, le due derivate ### **si sommano** e danno `1` — ### **senza un ramo
    apposta.**
    """
    cs = mot.cs
    assert cs is not None, (
        "`d_peso_arco` senza la forma `cs`: a forma spenta il peso d'arco NON dipende da"
        " `cs`, e questa derivata non esiste -- chi la chiede ha sbagliato ramo")
    due = np.take(cs, mot.inc.nodo).reshape(-1, 2)
    a, b = due[:, 0], due[:, 1]
    s2 = (a + b) ** 2
    fuori = mot._b("ep_dw", (mot.inc.m, 2), float)
    fuori[:, 0] = 2.0 * b * b / s2
    fuori[:, 1] = 2.0 * a * a / s2
    return fuori.reshape(-1)


def cs_primo(lam, lambda_c, fuori):
    """### `cs'(Lambda) = Lambda_c/(Lambda + Lambda_c)^2`, ### **la derivata della forma.**

    ### ⛔ **ALZA se `lambda_c <= 0`**, per lo stesso motivo di `FP.cs`: ### **la forma
    spenta si ottiene NON ACCENDENDOLA**, non passando zero.
    """
    lc = float(lambda_c)
    assert lc > 0.0, (
        "`cs_primo` con `lambda_c` = %r: la forma SPENTA non e' `lambda_c = 0`, e'"
        " `mot.cs is None` -- un valore nullo qui sarebbe una forma che non esiste" % (lc,))
    np.add(lam, lc, out=fuori)
    np.multiply(fuori, fuori, out=fuori)
    np.divide(lc, fuori, out=fuori)
    return fuori


def omega(mot, st, par):
    """### `Omega_k`: ### **il coefficiente della fase sul vuoto.**

    ### ⛔ **Legge `mot.lambda_c`**, che e' ### **il numero FISSO** della forma: con la
    forma spenta *(`None`)* ### **questo pezzo non esiste.**
    """
    per_nodo, per_arco = termini_di_h(mot, st, par)
    dw = d_peso_arco(mot)
    # ### ⛔ **IL CONTRIBUTO D'ARCO SI RACCOGLIE SUL NODO DEL CAPO**, perche'
    # ### `dw_a/dcs_k` e' ### **la derivata rispetto al capo `k`**: ogni estremita' porta
    # ### il suo pezzo al SUO nodo.
    arco_sul_nodo = _per_nodo(mot, dw * np.repeat(per_arco, 2),
                              mot._b("ep_arco_nodo", (mot.inc.n,), float))
    lam = mot.densita_vuoto(st)
    csp = cs_primo(lam, mot.lambda_c, mot._b("ep_csp", (mot.inc.n,), float))
    fuori = mot._b("ep_omega", (mot.inc.n,), float)
    np.add(per_nodo, arco_sul_nodo, out=fuori)
    np.multiply(fuori, csp, out=fuori)
    return fuori


def pesi_dello_stato(mot, st):
    """### `(w_nodo, w_arco)` ### **che la `Lambda` DI ADESSO darebbe.**

    ### ⛔⛔ **I PESI SONO DUE COSE DIVERSE, E CONFONDERLE E' COSTATO UN
    RISULTATO** *(errore `n.12` del guardiano, `2026-10-18`)*:

    | | quali pesi | chi li usa | perche' |
    |---|---|---|---|
    | ### **DEL PASSO** *(`pesi(mot)`)* | quelli in `mot.cs` | ### **i pezzi del passo** | sono quelli con cui il passo ha girato: ### **cambiarli vorrebbe dire cambiare la DINAMICA** |
    | ### **DELLO STATO** *(questa)* | `cs(Lambda di adesso)` | ### **le OSSERVABILI** | misurano ### **lo stato in cui mi trovo**: usare gli altri vorrebbe dire ### **leggere due istanti diversi** |

    ### ⚠ **E dopo `tick_con_cs`, `mot.cs` e' il `cs` del CENTRO di quel tick** --
    quindi un'osservabile che lo usasse ### **confronterebbe `G(t)` con `G(0)` calcolate
    con pesi di istanti diversi**, e la differenza e' ### **`O(dtau)`.**
    ### ✅ **E `mot.cs` NON SI TOCCA:** si mette il `cs` dello stato
    ### **per il tempo di una lettura**, e il `finally` ### **lo rimette** -- se restasse
    dentro, ### **il passo dopo girerebbe con un altro peso.**
    """
    salvo = mot.cs
    mot.cs = FP.cs(mot.densita_vuoto(st), mot.lambda_c,
                   mot._b("ep_cs_stato", (mot.inc.n,), float)).copy()
    try:
        return pesi(mot)
    finally:
        mot.cs = salvo


def g_dello_stato(mot, st, par):
    """### ⭐⭐ **`G` LETTA SULLO STATO: l'osservabile GIUSTA.**

    ### ⛔ **E' quella che `C1` deve usare**, e la differenza con `g_pesata` non e'
    un dettaglio: ### **con `g_pesata` la pendenza di `G` dava `1.002`** *(un artefatto)*,
    ### **con questa da' `~2.09`** -- e ### **il passo e' lo stesso.**
    ### ✅ **A forma SPENTA le due COINCIDONO**, perche' i pesi sono `1` da entrambe
    le parti: ### **la correzione si vede solo dove la forma gira.**
    """
    per_nodo, per_arco = termini_di_h(mot, st, par)
    if mot.cs is None or mot.lambda_c is None:
        # ### ✅ **A forma spenta i pesi sono `1`**, e `G` e' `H_tot` *(a meno
        # ### dell'ordine della somma)*: ### **nessun peso da calcolare.**
        return float(np.sum(per_nodo)) + float(np.sum(per_arco))
    w_nodo, w_arco = pesi_dello_stato(mot, st)
    return float(np.sum(w_nodo * per_nodo)) + float(np.sum(w_arco * per_arco))


def g_pesata(mot, st, par):
    """### `G` ### **coi pesi DEL PASSO** *(`mot.cs`)*.

    ### ⛔⛔ **NON E' L'OSSERVABILE DA USARE DOPO UN TICK** *(errore `n.12` del
    guardiano, `2026-10-18`)*: dopo `tick_con_cs` ### **`mot.cs` e' il `cs` del CENTRO**
    di quel tick, quindi questa funzione ### **legge lo stato di adesso coi pesi di
    allora** -- e la differenza e' ### **`O(dtau)`.**
    ### ✅ **PER UN'OSSERVABILE SI USA `g_dello_stato`.** ### **Questa resta** perche'
    e' ### **`G` come il PASSO la vede**, e serve ### **dove i pesi del passo sono cio'
    che si vuole** *(per esempio per dire quanto le due letture distano)*.
    ### ⚠ **A forma SPENTA le due COINCIDONO**, perche' i pesi sono `1`.
    """
    per_nodo, per_arco = termini_di_h(mot, st, par)
    if mot.cs is None:
        return float(np.sum(per_nodo)) + float(np.sum(per_arco))
    w_nodo, w_arco = pesi(mot)
    return float(np.sum(w_nodo * per_nodo)) + float(np.sum(w_arco * per_arco))


def applica(mot, st, par, frazione):
    """### La fase sul vuoto, ### **col PUNTO MEDIO IMPLICITO a punto fisso.**

    ### ⛔⛔ **PERCHE' IMPLICITO e non esplicito** *(errore `n.10` del guardiano)*:
    `Omega` dipende dalle ### **fasi RELATIVE del vuoto sugli archi**, che
    ### **questa fase MUOVE** — quindi il flusso ### **non e' esatto**, e una valutazione
    all'inizio del pezzo darebbe ### **il primo ordine.**
    ### ✅ **Il punto medio implicito e' del SECONDO ORDINE e REVERSIBILE**, cioe'
    ### **non rompe il palindromo** — ed e' la stessa scelta di `D2` per `cs`.
    ### ⚠ **L'iterazione gira su una COPIA:** lo stato vero ### **non si muove** finche'
    `Omega` non e' deciso.
    ### ⛔ **E se non converge entro `GIRI_MAX_OMEGA` ALZA**, perche' la regola dice
    ### **di relazionare, non di scegliere un altro schema.**
    """
    if mot.cs is None or mot.lambda_c is None:
        # ### ✅ **LA FORMA SPENTA: il pezzo NON ESISTE.** `cs'` non c'e', e il passo
        # ### ### **resta quello di prima AL BIT** -- e' il braccio `0` di questo mandato.
        # ### ⛔⛔ **E I DUE RAMI SONO UNO SOLO, PER UN MOTIVO ESATTO:** se `cs`
        # ### e' messo A MANO come COSTANTE *(le diagnosi a `cs` uniforme di `D3` e di
        # ### `H_w`)*, `cs` ### **NON E' UNA FUNZIONE DI `Lambda`** -- quindi
        # ### ### **`cs'` e' ZERO per definizione**, e il termine ### **non c'e'
        # ### davvero.** ### **Non e' una scappatoia: e' la derivata di una costante.**
        return st
    tau = float(mot.dtau[0]) * float(frazione)
    assert np.all(mot.dtau == mot.dtau[0]), (
        "`CAMM-FASE-VUOTO` con `dtau` NON uniforme fra i nodi: il tempo di questo pezzo"
        " e' IL TICK, e un tick per nodo non e' definito -- la scena va costruita con un"
        " `dtau` solo")
    phi = st["phi_h"]
    salvo = mot._b("ep_phi_salvo", phi.shape, phi.dtype)
    salvo[...] = phi
    prec = omega(mot, st, par).copy()
    giri = 0
    for giri in range(1, GIRI_MAX_OMEGA + 1):
        # ### il punto MEDIO: ### **mezza fase**, poi si rilegge `Omega`
        np.multiply(salvo, np.exp(-1j * (prec * (tau * 0.5))[mot.inc.nodo]), out=phi)
        nuovo = omega(mot, st, par)
        scarto = float(np.max(np.abs(nuovo - prec)))
        scala = float(np.max(np.abs(nuovo)))
        if scarto <= EPS_OMEGA * scala or scala == 0.0:
            prec = nuovo.copy()
            break
        prec = nuovo.copy()
    else:
        phi[...] = salvo
        raise AssertionError(
            "il punto medio di `Omega` NON CONVERGE in %d giri (ultimo scarto %.3e): la"
            " regola dice di RELAZIONARE coi numeri e NON di scegliere un altro schema,"
            " quindi questo ALZA invece di fermarsi a un valore qualunque"
            % (GIRI_MAX_OMEGA, scarto))
    # ### ✅ **E ADESSO LA FASE INTERA, dallo stato VERO**: `prec` e' il punto medio.
    np.multiply(salvo, np.exp(-1j * (prec * tau)[mot.inc.nodo]), out=phi)
    mot.giri_omega = giri
    return st
