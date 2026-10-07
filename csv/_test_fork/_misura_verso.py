# -*- coding: utf-8 -*-
"""`M1`, `M2`, `M3` — LA MISURA DEL VERSO, in **SOLA LETTURA**.

*(Mandato di Luca del 2026-10-06. Criteri fissati PRIMA della corsa; il mandato dice
«questa misura NON sceglie un'opzione», e lo strumento non scrive raccomandazioni.)*

### ⛔ **CHE COSA SIGNIFICA <<SOLA LETTURA>> QUI, e perche' NON basta prometterlo**

`chiralita_core_locale(..., geom=True)` ### **SCRIVE `_chi_geom_nodi`**, che e'
### **la cache che `TORS_4PI` LEGGE al passo dopo** *(verificato: il blocco della torsione
usa `getattr(self, '_chi_geom_nodi')` se la sua lunghezza e' `n`)*. Chiamarla e lasciarla
scritta ### **cambierebbe la dinamica della corsa che sto misurando.**

**E non e' l'unica scrittura.** Il censimento AST dice:

| la funzione | scrive |
|---|---|
| `chiralita_core_locale(geom=True)` | `_g_ccl_tot`, `_g_ccl_geom`, `_chi_geom_nodi` |
| `lambda_nodi` *(che la precedente CHIAMA)* | ### ⛔ **`_calcolo_schermatura`, `_g_scherm_init`, `_g_scherm_ricorsione`** |
| `_pesi` *(serve a `M2`)* | ### **quindici** contatori `_g_rampa_*` e `_g_kernel_alpha_*` |
| `_mat` *(dentro `calcola_psi`)* | ### ⛔ **muta `_S.data` IN PLACE** |
| `_base_cicli_topologici` *(serve a `M3-C`)* | `_cicli_topologici` |

> ### ⛔ **AVEVO SCRITTO CHE `lambda_nodi` ERA DI SOLA LETTURA, ED ERA FALSO.** L'ho
> trovato col censimento AST, non a occhio. ### **E' la ragione per cui questo strumento NON
> elenca a mano gli attributi da salvare:** un elenco a mano ### **dimentica le scritture
> TRANSITIVE**, e quella l'avevo gia' dimenticata.

> ### ✔ **IL PRESIDIO E' GENERICO:** `sola_lettura(net)` ### **copia TUTTO `net.__dict__`**
> *(63 attributi, `46.8 MB`, `0.02 s`)*, lascia girare, ### **MISURA quali attributi sono
> cambiati** *(e il numero finisce nel json: e' un FATTO, non un'assunzione)*, ripristina
> ### **tutto, comprese le chiavi NUOVE che vanno TOLTE**, e poi ### **RIVERIFICA.**
> ### **Se il ripristino non e' esatto, lo strumento SI FERMA.**

### LE TRE MISURE, coi criteri del mandato

* **`M1`** — `(a)` i nodi con `rho0/rho_c > 1`; `(b)` il ### **MASSIMO** del rapporto;
  `(c)` gli elementi di `_chi_geom_nodi` diversi da `perc_geom`.
  ### **CRITERIO: `(a) = 0` e `(c) = 0` a TUTTI i passi significa `--chi-core` INERTE per il
  dipolo.** ### **E `(b)` si riporta SEMPRE**, anche con `(a) = 0`: un massimo a `0.98` e uno
  a `0.001` danno lo stesso `(a)` e dicono due cose opposte.
  ### ⛔ **I diagnostici `_chi_core_*` NON si leggono:** il ramo `geom=True` non li scrive.
* **`M2`** — `c_k` col ### **DENOMINATORE SATURATO**, che e' la correzione verificata sul
  codice: `satura` cambia il modulo, quindi un numeratore saturo su un denominatore
  ### **nudo** renderebbe `c = 1` ### **irraggiungibile.**
* **`M3`** — quante volte per passo cambiano il segno di `A`, l'olonomia di `C`, il segno di
  `tw` per `D`, e ### **`perc_geom` come RIFERIMENTO DI OGGI.**

### ⚠ **DUE LETTURE DI `A`, E SI RIPORTANO ENTRAMBE**

`A` e' *«`sign(Σ tw)` sugli archi del nodo»*, e ### **`tw` e' orientata `i -> j`**
*(verificato: `dph = _wphi(phi[i] - phi[j])`, e il commento della riga dice <<1-forma di
fase, orientata i->j>>)*. Quindi:

| | |
|---|---|
| `A_grezza` | `Σ tw` col ### **segno MEMORIZZATO**. ### ⛔ **Dipende dalla NUMERAZIONE**: misurato, ### **`471564` archi su `471564` hanno `i < j`** |
| `A_divergenza` | `Σ` col segno ### **relativo al nodo** *(`+` coda, `−` testa)*: e' il ### **FLUSSO USCENTE**, ben definito — ### **e non e' una circolazione** |

### ⚠ **I CONFRONTI FRA PASSI, e la trappola che ho gia' pagato**

`CHI-TORS-ZERO-FALSO` e' nata da uno zero che voleva dire *«non misurato»*. Qui:

* **i NODI si confrontano per INDICE**, perche' nascono ### **in coda** — e lo strumento
  ### **VERIFICA che `n` non scenda mai**: se scendesse, il confronto per indice sarebbe
  invalido e ### **la corsa si fermerebbe**;
* **gli ARCHI si confrontano per CHIAVE `(i,j)`, NON per indice**, perche' alla mitosi
  `i = concat([i[keep], a, m])` ### **rimescola gli indici**;
* **un valore non confrontabile e' `None`**, ### **mai `0`.**
"""
import contextlib
import copy
import hashlib
import io
import json
import os
import sys
import time

import numpy as np
import scipy.sparse as _sp
from scipy.stats import rankdata as _rankdata

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
sys.path.insert(0, _QUI)
import _presidio   # noqa: E402

_presidio.avvia(__file__)

import _passo                                    # noqa: E402
import _cli_flag                                 # noqa: E402
import _mitosi_soglia_grad as _MSG               # noqa: E402
import _mitosi_zero_dove as _MZD                 # noqa: E402

blob, piattaforma, carica = _MSG.blob, _MSG.piattaforma, _MSG.carica
stampa, riga, n4, q = _MSG.stampa, _MSG.riga, _MSG.n4, _MSG.q

NL = chr(10)
FUORI = os.path.join(RADICE, "csv", "_test_fork", "_misura_verso")
SIM = os.path.join(RADICE, "soliton_simulator.py")
# ### IL BLOB ATTESO: la misura vale per QUESTO simulatore e per nessun altro.
BLOB_ATTESO = "b8c21049"
# ### ⭐ **`A1`, 2026-10-07: LA FINESTRA GIUSTA.** La misura del 2026-10-06 girava su
#   `230` passi, e ### **le nascite cominciano al `216`**: era il regime in cui il difetto
#   da curare ### **NON AGISCE**. ### **Ora `1000` passi, con CINQUE passi pesanti oltre il
#   `216`.**
PASSI = 1000
PASSI_MISURA = (1, 150, 230, 300, 400, 500, 700, 1000)
# ### I PASSI PESANTI: i passi della misura ### **E I LORO PREDECESSORI**, perche' la
#   stabilita' e' una DIFFERENZA fra due passi, e il passo `0` e' lo stato PRIMA del primo
#   passo. ### **Senza il predecessore, `M3-C` non avrebbe un <<fra due passi>>.**
PASSI_PESANTI = tuple(sorted(set(PASSI_MISURA) | set(k - 1 for k in PASSI_MISURA)))
PASSI_SALVA = 10
# ### LA BASE DELLE CHIAVI D'ARCO: fissa, e MOLTO sopra `n` (misurato `12802`), cosi' una
#   chiave resta confrontabile ### **anche mentre la rete cresce.**
BASE_CHIAVE = 1 << 21
# ### I SECCHI DI GRADO, DICHIARATI PRIMA: il grado massimo misurato e' `94`.
SECCHI_GRADO = ((0, 20), (21, 40), (41, 60), (61, 80), (81, 10 ** 9))
P4 = 4.0 * np.pi
P2PI = 2.0 * np.pi
EPS_NORMALE = 1e-12
# ### LA FINESTRA PER <<toccato da un salto del dipolo>>, dal mandato.
FINESTRA_SALTO = 50
# ### LE ORIGINI DI UN ARCO, e sono QUATTRO. `seminato` e' tutto cio' che esiste al passo
#   `0`; le altre tre si registrano con INVOLUCRI DI SOLA LETTURA sulle regole di nascita.
ORIGINI = ("seminato", "allaccia", "divisione", "schwinger")
# ### I SECCHI DI ETA', in unita' di `tau_tw`: dichiarati PRIMA. Il taglio `> 2` e' quello
#   del mandato; gli altri servono a far VEDERE la dipendenza dall'eta' invece di
#   affidarsi a un taglio solo.
SECCHI_ETA = ((0.0, 0.5), (0.5, 1.0), (1.0, 2.0), (2.0, 5.0), (5.0, 1e18))


# ====================================================================== il presidio
def _firma(v):
    """La firma di un attributo, per MISURARE se e' cambiato. **Niente float a occhio.**"""
    if isinstance(v, np.ndarray):
        return ("nd", tuple(v.shape), str(v.dtype),
                hashlib.sha1(np.ascontiguousarray(v).tobytes()).hexdigest())
    if _sp.issparse(v):
        return ("sp", tuple(v.shape), _firma(v.data), _firma(v.indices), _firma(v.indptr))
    if hasattr(v, "bit_generator"):
        # ### IL GENERATORE: la sua firma e' lo STATO, non l'identita' dell'oggetto.
        return ("rng", hashlib.sha1(repr(v.bit_generator.state).encode()).hexdigest())
    if isinstance(v, (int, float, bool, complex, str, type(None))):
        return ("scal", repr(v))
    # ### ⛔ **UN `set` NON HA ORDINE, e `repr` ne espone UNO:** `copy.deepcopy` ricostruisce
    #   l'insieme inserendo gli elementi in ordine di iterazione, e il `repr` che ne esce
    #   ### **puo' essere diverso a parita' di CONTENUTO.** ### **Con una firma basata su
    #   `repr`, il presidio accusava una scrittura che NON C'ERA** -- e l'ha fatto davvero,
    #   su `_g_registro_apparse`, al primo giro. ### **Quindi gli insiemi si firmano
    #   ORDINATI**, e i dizionari per CHIAVE ordinata.
    if isinstance(v, (set, frozenset)):
        return ("set", len(v),
                hashlib.sha1(repr(sorted(repr(x) for x in v)).encode("utf-8", "replace")
                             ).hexdigest())
    if isinstance(v, dict):
        return ("dict", len(v),
                hashlib.sha1(repr(sorted((repr(k2), _firma(v2)) for k2, v2 in v.items()))
                             .encode("utf-8", "replace")).hexdigest())
    if isinstance(v, (list, tuple)):
        return (type(v).__name__, len(v),
                hashlib.sha1(repr([_firma(x) for x in v]).encode("utf-8", "replace")
                             ).hexdigest())
    return ("altro", type(v).__name__,
            hashlib.sha1(repr(v).encode("utf-8", "replace")).hexdigest())


def _impronta(net):
    return {k: _firma(v) for k, v in net.__dict__.items()}


@contextlib.contextmanager
def sola_lettura(net, etichetta):
    """### **COPIA TUTTO, misura cio' che cambia, RIPRISTINA TUTTO, e RIVERIFICA.**

    L'oggetto restituito e' un `dict` che a uscita contiene `toccati`: ### **gli attributi
    che la chiamata ha scritto davvero.** ### **E' una MISURA, non una dichiarazione.**
    """
    prima = _impronta(net)
    salvo = {k: copy.deepcopy(v) for k, v in net.__dict__.items()}
    esito = {"etichetta": etichetta}
    try:
        yield esito
    finally:
        dopo = _impronta(net)
        toccati = sorted(set(prima) ^ set(dopo))
        toccati += sorted(k for k in set(prima) & set(dopo) if prima[k] != dopo[k])
        esito["toccati"] = sorted(set(toccati))
        # --- il RIPRISTINO: anche le chiavi NUOVE vanno TOLTE.
        for k in list(net.__dict__):
            if k not in salvo:
                del net.__dict__[k]
        for k, v in salvo.items():
            net.__dict__[k] = v
        fin = _impronta(net)
        residuo = [k for k in fin if prima.get(k) != fin[k]]
        residuo += [k for k in prima if k not in net.__dict__]
        if residuo:
            # ### ⛔ **UN ERRORE CHE NON PORTA LA PROVA COSTRINGE A INDOVINARE:** per ogni
            #   chiave si dice se era PRESENTE prima, e le due firme. ### **Cosi' si
            #   distingue una scrittura non ripristinata da una FIRMA INSTABILE**, che
            #   sono due guasti diversi con due cure diverse.
            det = [{"chiave": k, "era_presente_prima": k in prima,
                    "firma_prima": str(prima.get(k))[:200],
                    "firma_dopo_il_ripristino": str(fin.get(k))[:200],
                    "firma_durante": str(dopo.get(k))[:200]}
                   for k in sorted(set(residuo))]
            raise SystemExit(
                "[FERMO] il ripristino di `%s` NON e' esatto.%s%s%s### La corsa si ferma: "
                "una misura che altera lo stato che misura non vale niente."
                % (etichetta, NL, json.dumps(det, indent=1, default=str), NL))
        esito["ripristino_esatto"] = True


# ====================================================================== gli aiuti
def chiavi_archi(net):
    """La chiave di un arco, ### **CANONICA `(min, max)`.**

    ### ⛔ **LA PRIMA VERSIONE USAVA `i * BASE + j`, e poggiava su una premessa che la
    corsa del 2026-10-06 ha SMENTITO al passo `229`:** *<<tutti gli archi hanno `i < j`>>*
    era misurato ai passi `0`, `1` e `2`, cioe' ### **prima della prima nascita** *(il
    passo `216`)*. ### **Ogni nascita produce ESATTAMENTE un arco con `i > j`**: alla
    mitosi nascono `a-m` e `m-b` col nodo nuovo `m` di indice ### **piu' alto**, quindi
    `m-b` ha `i > j` ### **sempre** *(e lo Schwinger fa lo stesso con `k-bb`)*.

    ### ✔ **Con la chiave canonica non c'e' piu' niente da assumere:** un arco e'
    identificato dalla ### **coppia NON ORDINATA**, comunque sia stato memorizzato.
    """
    ii = np.asarray(net.i, np.int64)
    jj = np.asarray(net.j, np.int64)
    return np.minimum(ii, jj) * BASE_CHIAVE + np.maximum(ii, jj)


def tw_canonico(net):
    """`tw` riportata all'orientamento ### **canonico `min -> max`.**

    `tw` e' una ### **1-forma orientata `i -> j`**, quindi il suo SEGNO dipende da come
    l'arco e' memorizzato. ### **Confrontare `sign(tw)` fra due passi per coppia di nodi
    SENZA questa riduzione conterebbe un cambio di segno dove e' cambiata solo la
    SCRITTURA dell'arco.**
    """
    ii = np.asarray(net.i, np.int64)
    jj = np.asarray(net.j, np.int64)
    return np.asarray(net.tw, float) * np.where(ii <= jj, 1.0, -1.0)


def allinea(ch_a, va, ch_b, vb):
    """I valori di due passi, ### **allineati per CHIAVE** e non per indice.

    Restituisce `(va_comuni, vb_comuni, n_comuni)`. ### **Le chiavi assenti da una delle due
    parti NON entrano**, e il loro numero si riporta.
    """
    ch_a = np.asarray(ch_a); ch_b = np.asarray(ch_b)
    # ### ⛔ **L'ARRAY VUOTO E' UN CASO, NON UN INCIDENTE:** `searchsorted` su un array
    #   vuoto da' `0`, e indicizzarlo esplode. ### **Zero confrontabili e' la risposta
    #   giusta**, e il collaudo ci passa.
    if ch_a.size == 0 or ch_b.size == 0:
        return np.zeros(0), np.zeros(0), 0
    o_a = np.argsort(ch_a, kind="stable")
    sa, vsa = ch_a[o_a], np.asarray(va)[o_a]
    pos = np.searchsorted(sa, ch_b)
    pos = np.minimum(pos, max(len(sa) - 1, 0))
    ok = (len(sa) > 0) & (sa[pos] == ch_b)
    return vsa[pos[ok]], np.asarray(vb)[ok], int(np.sum(ok))


def dipoli_opzioni(net, delta):
    """### **IL DIPOLO CHE CIASCUNA OPZIONE PRODURREBBE**, per ARCO.

    ### ⛔ **E' IL METRO GIUSTO, e il motivo e' nell'annotazione `(c)` di
    `doc/GEOM_SENZA_VERSO.md`:** contare ### **quanti segni cambiano** mette sulla stessa
    riga grandezze che non lo sono — per `D` e `MEM` il dipolo e' ### **continuo** *(un
    valore che passa per zero non inietta niente)*, per `A` e `perc_geom` ogni cambio e' un
    ### **salto di `pi`**, e `perc_geom` cambia ### **per NODO** dove ogni nodo tocca
    ### **~74 archi**. ### **`Somma |Delta dipolo|` e' l'unica grandezza che le mette tutte
    nella STESSA unita'.**

    ### LE QUATTRO FORME, e ognuna e' DICHIARATA
      `perc_geom`  `pi*0.5*(chi_i - chi_j)` con `chi = _chi_geom_nodi` — ### **la legge di
                   OGGI**, letta dove il dipolo la legge *(e `M1` ha misurato che
                   `_chi_geom_nodi == perc_geom` in questa scena)*;
      `A`          `pi*0.5*(s_i - s_j)` con `s = sign(Somma tw sugli archi del nodo)`, la
                   somma col segno ### **MEMORIZZATO** — ### **l'opzione `A` come scritta**;
      `D`          `pi*tanh(tw/PHI_CRIT)` — ### **per ARCO, continua**, la forma proposta
                   nell'annotazione delle tre obiezioni *(`sup|f'| = 1/2`, zero numeri
                   nuovi)*;
      `MEM`        `pi*tanh(delta/PHI_CRIT)` con `delta = twp - tw` — ### **la STESSA forma
                   di `D` con la MEMORIA al posto dell'istante.**

    ### ⚠ **NESSUNA DI QUESTE E' UNA LEGGE: sono LETTURE.** Il simulatore non le vede.
    """
    n = int(net.n)
    ii = np.asarray(net.i, int); jj = np.asarray(net.j, int)
    tw = np.asarray(net.tw, float)
    m = (ii < n) & (jj < n)
    out = {}
    # --- `perc_geom`: la legge di OGGI, letta dove il dipolo la legge
    chi = getattr(net, "_chi_geom_nodi", None)
    if chi is None or len(np.asarray(chi)) < n:
        chi = np.asarray(net.perc_geom, float)[:n]
    chi = np.asarray(chi, float)[:n]
    d = np.zeros(len(ii))
    d[m] = np.pi * 0.5 * (chi[ii[m]] - chi[jj[m]])
    out["perc_geom"] = d
    # --- `A`: il segno della somma GREZZA sugli archi del nodo
    s = np.zeros(n)
    np.add.at(s, ii[m], tw[m]); np.add.at(s, jj[m], tw[m])
    s = np.sign(s)
    d = np.zeros(len(ii))
    d[m] = np.pi * 0.5 * (s[ii[m]] - s[jj[m]])
    out["A"] = d
    # --- `D` e `MEM`: per ARCO, continue
    out["D"] = np.pi * np.tanh(tw / P2PI)
    out["MEM"] = np.pi * np.tanh(np.asarray(delta, float) / P2PI)
    return out


def secchio_eta(e):
    """L'indice del secchio di eta', coi limiti DICHIARATI in `SECCHI_ETA`."""
    e = np.asarray(e, float)
    fuori = np.full(e.shape, -1, int)
    for k, (lo, hi) in enumerate(SECCHI_ETA):
        fuori = np.where((e >= lo) & (e < hi) & (fuori < 0), k, fuori)
    return fuori


def auc(a, b):
    """`AUC` di `a` contro `b` *(Mann-Whitney)*. ### **`0.5` = nessuna separazione.**"""
    a = np.asarray(a, float); b = np.asarray(b, float)
    na, nb = a.size, b.size
    if na == 0 or nb == 0:
        return None
    r = _rankdata(np.concatenate([a, b]))
    return float((np.sum(r[:na]) - na * (na + 1) / 2.0) / (na * nb))


def per_classe(val, cl, nomi=_MZD.CLASSI):
    """Mediana, media, massimo e numerosita' per classe. ### **`None` se la classe e' vuota.**"""
    val = np.asarray(val, float)
    fuori = {}
    for k, nome in enumerate(nomi):
        m = (cl == k)
        if not np.any(m):
            fuori[nome] = None
            continue
        v = val[m]
        fuori[nome] = {"n": int(v.size), "mediana": float(np.median(v)),
                       "media": float(np.mean(v)), "max": float(np.max(v)),
                       "min": float(np.min(v))}
    return fuori


# ====================================================================== l'osservatore
class Verso(object):
    """### **LEGGE SOLTANTO.** Ogni chiamata che scrive passa da `sola_lettura`."""

    nome = "verso"

    def __init__(self):
        self.geo = None
        self.g = None               # l'oggetto che porta la classe MATERIA/BORDO/VUOTO
        self.passi = []             # una riga per passo: `A` e `D`, che costano poco
        self.misure = {}            # una voce per passo di `PASSI_MISURA`
        self.pesanti = {}           # lo stato grezzo ai passi pesanti, per le differenze
        self.toccati = {}           # che cosa ha scritto ogni chiamata guardata
        self.n_prec = None
        self.avvisi = []
        self._prec = None
        self._acc = None            # l'accumulatore PARALLELO di `M5(b)`
        self.origine = {}           # chiave d'arco -> origine, dagli INVOLUCRI
        self._involucri = None

    # ---------------------------------------------------------------- la scena
    def prepara(self, S, net):
        # ### LA CLASSE VIENE DAL CODICE CHE HA PRODOTTO `27c10bd`, non da una copia:
        #   `_MZD.Misura` si usa SOLO per `prepara` e `_u`. ### **Non viene mai agganciata
        #   come `_MIS`, quindi NESSUN gancio di quello strumento gira qui.**
        self.g = _MZD.Misura(S.DT, 0.0)
        self.geo = self.g.prepara(S, net)
        # ### ⭐ **GLI INVOLUCRI DELL'ORIGINE si agganciano QUI**, prima del primo passo,
        #   cosi' ogni arco che nasce porta la sua provenienza. ### **Toccano il MODULO e
        #   `net._allaccia`, non lo STATO**, e si ripristinano a corsa chiusa.
        self.geo["archi_seminati"] = self.involucri(S, net)
        return self.geo

    def classe_nodi(self, net):
        idx = np.arange(net.n)
        u, _c = self.g._u(net, idx)
        return _MZD.classe(u, self.g.u_bordo), u

    # ---------------------------------------------------------------- M1
    def m1(self, S, net):
        """`(a)` i nodi sopra soglia, `(b)` il MASSIMO del rapporto, `(c)` i diversi."""
        n = int(net.n)
        fuori = {"n": n}
        # ### ⛔ **IL RAMO `calcola_psi` NON DEVE MAI SCATTARE**, e non si assume: si
        #   VERIFICA. Se `psi` mancasse, `chiralita_core_locale` la RICALCOLEREBBE, e
        #   `M1` misurerebbe uno stato che il passo non ha prodotto.
        ok_psi = hasattr(net, "psi") and len(np.asarray(net.psi)) >= n
        fuori["psi_presente"] = bool(ok_psi)
        if not ok_psi or n == 0 or not len(net.i):
            fuori["stato"] = "NON MISURATO: psi assente o rete vuota"
            return fuori
        fuori["stato"] = "MISURATO"
        I2 = np.abs(np.asarray(net.psi)[:n]) ** 2
        # --- `rho_c`: **la STESSA via della funzione**, e il ramo di riserva pure.
        with sola_lettura(net, "massa_critica_adattiva") as g:
            try:
                mc = float(S.massa_critica_adattiva(net)); via = "adattiva"
            except Exception:
                mc = float(S.massa_critica_collasso()); via = "collasso"
        self.toccati["massa_critica_adattiva"] = g["toccati"]
        rho_c = mc / ((4.0 / 3.0) * np.pi * S.LAM_BASE ** 3)
        # --- `rho0[k] = max(I2 su {k} unito ai vicini)`: la STESSA definizione, VETTORIALE.
        #   ### **Lo stesso filtro della funzione:** solo gli archi con `a < n` e `b < n`.
        ii = np.asarray(net.i, int); jj = np.asarray(net.j, int)
        m = (ii < n) & (jj < n)
        rho0 = I2.copy()
        np.maximum.at(rho0, ii[m], I2[jj[m]])
        np.maximum.at(rho0, jj[m], I2[ii[m]])
        rapporto = rho0 / max(rho_c, 1e-12)
        sopra = rapporto > 1.0
        fuori.update({"via_rho_c": via, "massa_critica": mc, "rho_c": rho_c,
                      "a_nodi_sopra_1": int(np.sum(sopra)),
                      "b_rapporto_max": float(np.max(rapporto)),
                      "rapporto_mediano": float(np.median(rapporto)),
                      "I2_max": float(np.max(I2))})
        # --- `(c)`: la funzione VERA, chiamata DENTRO il presidio.
        with sola_lettura(net, "chiralita_core_locale") as g:
            chi_g = np.asarray(net.chiralita_core_locale(net.perc_geom, geom=True), float).copy()
        self.toccati["chiralita_core_locale"] = g["toccati"]
        pg = np.asarray(net.perc_geom, float)[:n]
        div = chi_g[:n] != pg
        fuori["c_diversi_da_perc_geom"] = int(np.sum(div))
        fuori["c_scarto_max"] = float(np.max(np.abs(chi_g[:n] - pg))) if n else 0.0
        # ### ✔ **UN CONTROLLO CHE PUO' FALLIRE, e lega i due conti INDIPENDENTI:** la
        #   funzione modifica `chi_core[k]` ### **solo dove `r > 0`**, cioe' solo dove
        #   `rapporto > 1`. ### **Quindi `(c)` NON PUO' superare `(a)`.** Se lo facesse, il
        #   mio ricalcolo di `rho0` non sarebbe quello della funzione, e la misura sarebbe
        #   da buttare. ### **E' un controllo sul MIO codice, non sul simulatore.**
        fuori["c_dentro_a"] = bool(np.all(~div | sopra))
        if not fuori["c_dentro_a"]:
            self.avvisi.append(
                "M1: `(c)` esce da `(a)`: il ricalcolo di rho0 NON coincide con la funzione.")
        return fuori

    # ---------------------------------------------------------------- M2
    def m2(self, S, net, cl):
        """`c_k` col denominatore ### **SATURATO**, e il grado come secondo asse."""
        n = int(net.n)
        fuori = {"n": n}
        if n == 0 or not len(net.i):
            fuori["stato"] = "NON MISURATO: rete vuota"
            return fuori
        with sola_lettura(net, "_pesi") as g:
            w = np.asarray(net._pesi(), float).copy()
            # ### IL NUMERATORE E IL DENOMINATORE DALLO ### **STESSO** `w`: `net.psi` e'
            #   stato calcolato DENTRO il passo, con un `w` di uno stato PRECEDENTE alla
            #   fine del passo. ### **Mischiarli sarebbe un numeratore e un denominatore
            #   di due istanti diversi**, e il rapporto non vorrebbe dire niente.
            F = np.asarray(net._mat(w) @ (S.SCALA_AMP * np.exp(1j * np.asarray(net.phi)))).copy()
        self.toccati["_pesi"] = g["toccati"]
        num = np.abs(np.asarray(net.satura(F), complex))[:n]
        ii = np.asarray(net.i, int); jj = np.asarray(net.j, int)
        m = (ii < n) & (jj < n)
        somma_w = np.zeros(n)
        np.add.at(somma_w, ii[m], np.abs(w[m]))
        np.add.at(somma_w, jj[m], np.abs(w[m]))
        den = np.asarray(net.satura(S.SCALA_AMP * somma_w), float)
        # ### ⛔ **IL DENOMINATORE SATURO E' LA CORREZIONE, e il motivo e' algebrico:**
        #   `|satura(F)| = |F| / (1 + GAMMA*sqrt(|F|^2+1e-9))` e' ### **monotona nel
        #   MODULO**, quindi `|satura(F)| <= satura(amp * Somma|W|)`: ### **con il
        #   denominatore SATURO `c_k` sta in `[0, 1]` e `c = 1` E' RAGGIUNGIBILE**; con il
        #   denominatore NUDO non lo sarebbe mai.
        c = num / np.maximum(den, 1e-300)
        grado = np.zeros(n)
        np.add.at(grado, ii[m], 1.0)
        np.add.at(grado, jj[m], 1.0)
        fuori.update({
            "stato": "MISURATO",
            "c_fuori_0_1": int(np.sum((c < -1e-12) | (c > 1.0 + 1e-9))),
            "c_tutti": {"mediana": float(np.median(c)), "media": float(np.mean(c)),
                        "min": float(np.min(c)), "max": float(np.max(c))},
            "c_per_classe": per_classe(c, cl),
            "den_per_classe": per_classe(den, cl),
            "num_per_classe": per_classe(num, cl),
            "psi_vs_num_scarto_max": float(np.max(np.abs(
                np.abs(np.asarray(net.psi)[:n]) - num))),
            "auc_materia_vuoto": auc(c[cl == 0], c[cl == 2]),
            "auc_den_materia_vuoto": auc(den[cl == 0], den[cl == 2]),
            "grado": {"medio": float(np.mean(grado)), "max": float(np.max(grado))},
        })
        secchi = {}
        for lo, hi in SECCHI_GRADO:
            mm = (grado >= lo) & (grado <= hi)
            et = "%d-%d" % (lo, hi) if hi < 10 ** 9 else "%d+" % lo
            secchi[et] = (None if not np.any(mm) else
                          {"n": int(np.sum(mm)), "c_mediana": float(np.median(c[mm])),
                           "den_mediana": float(np.median(den[mm]))})
        fuori["c_per_grado"] = secchi
        # ### ⛔ **`c_k` FUORI DA `[0,1]` E' UN GUASTO, non un dato:** l'algebra sopra lo
        #   esclude, quindi se capita e' il MIO conto a essere sbagliato.
        if fuori["c_fuori_0_1"]:
            self.avvisi.append("M2: %d valori di c_k fuori da [0,1]: l'algebra lo esclude."
                               % fuori["c_fuori_0_1"])
        return fuori

    # ---------------------------------------------------------------- M3
    def _a_e_d(self, net):
        """Le grandezze di `A` e di `D`: ### **costano poco, quindi si prendono a OGNI passo.**"""
        n = int(net.n)
        tw = np.asarray(net.tw, float)
        ii = np.asarray(net.i, int); jj = np.asarray(net.j, int)
        m = (ii < n) & (jj < n)
        grezza = np.zeros(n); divg = np.zeros(n)
        np.add.at(grezza, ii[m], tw[m]); np.add.at(grezza, jj[m], tw[m])
        np.add.at(divg, ii[m], tw[m]); np.add.at(divg, jj[m], -tw[m])
        # ### `A` GREZZA usa i segni ### **MEMORIZZATI**, ed e' il punto: e' la lettura
        #   che ### **dipende da come l'arco e' scritto.** `A` DIVERGENZA e `D`, invece,
        #   devono essere ### **indipendenti dalla scrittura**, e `D` lo diventa
        #   riducendo `tw` al verso canonico.
        # ### ⭐ **`A1`: `delta = twp - tw` E' LA MEMORIA GIA' DENTRO `tw`** -- l'algebra
        #   sta nel §`4b` di `doc/MEMORIE_MANCANTI.md`: e' una ### **media mobile
        #   esponenziale di `dph_prec`** con ritmo `dt_e/tau_tw`.
        #   ### ⚠ **E IL SEGNO SI RIDUCE AL VERSO CANONICO**, come per `D`: `twp` e `tw`
        #   sono ### **entrambi orientati `i -> j`**, quindi la loro differenza lo e'.
        _or = np.where(ii <= jj, 1.0, -1.0)
        delta = (np.asarray(net.twp, float) - tw)
        dip = dipoli_opzioni(net, delta)
        # ### `dt_e` E `tau_tw` SI LEGGONO DA `net`, NON SI RICALCOLANO: `_dt_e_ultimo` e'
        #   scritto dallo `step` *(riga `7536`)* e `_tau_tw_locale` e' una funzione pura
        #   del modulo. ### **Nessuna copia patchata del simulatore.**
        dte = np.asarray(getattr(net, "_dt_e_ultimo", 0.0), float) * np.ones(len(ii))
        return {"n": n, "chiavi": chiavi_archi(net),
                "sg_grezza": np.sign(grezza), "sg_divg": np.sign(divg),
                "sg_tw": np.sign(tw_canonico(net)),
                "sg_mem": np.sign(delta * _or),
                "archi_i_maggiore_j": int(np.sum(ii > jj)),
                "perc_geom": np.asarray(net.perc_geom, float)[:n].copy(),
                "delta": delta, "tw": tw.copy(), "dip": dip,
                "twp_dip": np.asarray(net.twp_dip, float).copy(),
                "dt_e": dte,
                "fraz_tw_oltre_2pi": (float(np.mean(np.abs(tw) > P2PI))
                                      if len(tw) else None)}

    def m3_cicli(self, net):
        """`C`: l'olonomia di FASE sulla base, per ### **DUE vie indipendenti.**

        ### ⛔ **IL `verso` MEMORIZZATO NON SI PUO' USARE COSI' COM'E', e l'ho MISURATO.**
        Il cammino di un ciclo fondamentale e' `u -> lca -> v -> u`, e la ### **chiusura si
        percorre `v -> u`** mentre il suo `verso` e' registrato ### **`+1`**, cioe'
        ### **opposto**. Gli scarti dal multiplo di `4pi`, sulle quattro convenzioni:

        | la convenzione | scarto max |
        |---|--:|
        | come MEMORIZZATO | ### ⛔ **`6.17`** |
        | ### **solo la CHIUSURA ribaltata** | ### ✔ **`7.1e-15`** |
        | tutti ribaltati | ### ⛔ **`6.17`** |
        | tutti tranne la chiusura | ### ✔ **`7.1e-15`** |

        > ### ⛔ **QUINDI CHI IMPLEMENTASSE `B` o `C` LEGGENDO `verso` INGENUAMENTE
        > OTTERREBBE UN'OLONOMIA SPAZZATURA** *(scarto mediano `3.06`, cioe' nemmeno un
        > multiplo di `2pi`)*. ### **E' un rischio CONCRETO e NUOVO per quelle due opzioni**,
        > e non e' un difetto di fisica: il `verso` ### **non lo legge nessuna legge**, solo
        > la diagnostica.

        **La via PRIMARIA e' `_vertici_ciclo`**, l'helper del simulatore, che ricostruisce la
        sequenza dei NODI e quindi ### **chiude il ciclo per costruzione**; la via degli
        ARCHI, con la convenzione misurata, resta come ### **controllo indipendente**, e il
        loro disaccordo si riporta. ### **Due vie che concordano valgono piu' di una.**
        """
        with sola_lettura(net, "_base_cicli_topologici") as g:
            with contextlib.redirect_stdout(io.StringIO()):
                cicli = [list(c) for c in net._base_cicli_topologici()]
                vert = [net._vertici_ciclo(c) for c in cicli]
        self.toccati["_base_cicli_topologici"] = g["toccati"]
        n = int(net.n)
        ii = np.asarray(net.i, int); jj = np.asarray(net.j, int)
        phi = np.asarray(net.phi, float)
        dph = np.asarray(net._wphi(phi[ii] - phi[jj]), float)
        ch = chiavi_archi(net)
        olon, olon_e, firme, lung, senza = [], [], [], [], 0
        for c, sq in zip(cicli, vert):
            e = np.asarray([int(x[0]) for x in c], int)
            s = np.asarray([int(x[1]) for x in c], float)
            if e.size == 0 or e.max() >= dph.size:
                senza += 1
                continue
            if sq is None or len(sq) < 3:
                # ### ⚠ **UN CICLO SENZA SEQUENZA NON E' UN CICLO CON OLONOMIA ZERO:**
                #   si CONTA a parte, e non entra nella frazione.
                senza += 1
                continue
            sq = np.asarray(sq, int)
            olon.append(float(np.sum(np.asarray(
                net._wphi(phi[sq] - phi[np.roll(sq, -1)]), float))))
            s2 = s.copy(); s2[0] = -s2[0]        # ### la convenzione MISURATA
            olon_e.append(float(np.sum(s2 * dph[e])))
            firme.append(frozenset(int(x) for x in ch[e]))
            lung.append(int(e.size))
        olon = np.asarray(olon, float); olon_e = np.asarray(olon_e, float)
        # ### ✔ **IL CONTROLLO CHE PUO' FALLIRE, e al primo giro HA FALLITO** *(scarto
        #   `6.17` invece di `~0`)*: l'olonomia ### **deve** essere un multiplo intero di
        #   `4pi`, perche' su un ciclo chiuso la somma di `(phi_i - phi_j)` telescopia a
        #   `0` ESATTO e `_wphi` avvolge sul periodo `4pi`. ### **Se lo scarto fosse
        #   grande, l'algebra dell'obiezione `(b)` sarebbe SBAGLIATA** -- quindi questo
        #   numero e' la PROVA di quell'obiezione, non un dettaglio.
        k = np.round(olon / P4) if olon.size else np.zeros(0)
        scarto = np.abs(olon - k * P4) if olon.size else np.zeros(0)
        return {"n_cicli": int(olon.size), "cicli_senza_sequenza": int(senza),
                "lunghezza": ({"min": int(min(lung)), "max": int(max(lung)),
                               "media": float(np.mean(lung))} if lung else None),
                "olonomia_non_nulla": int(np.sum(np.abs(k) > 0)) if olon.size else 0,
                "frazione_non_nulla": (float(np.mean(np.abs(k) > 0))
                                       if olon.size else None),
                "k_max": float(np.max(np.abs(k))) if olon.size else None,
                "scarto_dal_multiplo_max": float(np.max(scarto)) if olon.size else None,
                # ### ⛔ **LE DUE VIE CONCORDANO SUL MODULO E NON SEMPRE SUL SEGNO**, e
                #   la differenza misurata al primo giro era `50.265 = 16pi`, cioe'
                #   ### **un multiplo di `4pi` compatibile con un VERSO DI PERCORRENZA
                #   OPPOSTO.** ### **Non e' un difetto dei miei conti: e' la stessa
                #   arbitrarieta' di orientamento che rende arbitrario il SEGNO
                #   dell'opzione `C`** -- due routine DEL SIMULATORE scelgono due versi
                #   diversi sullo STESSO ciclo. ### **Quindi si riportano separati:** il
                #   modulo come controllo *(deve coincidere)*, il segno come MISURA.
                "due_vie_modulo_disaccordo_max": (
                    float(np.max(np.abs(np.abs(olon) - np.abs(olon_e))))
                    if olon.size else None),
                "due_vie_segno_discorde": (
                    int(np.sum((np.sign(olon) != np.sign(olon_e))
                               & (np.abs(olon) > 1e-9)))
                    if olon.size else None),
                "_firme": firme}

    # ---------------------------------------------------------------- l'ORIGINE
    def involucri(self, S, net):
        """Registra l'ORIGINE di ogni arco con ### **INVOLUCRI DI SOLA LETTURA.**

        Le regole di nascita vivono in ### **`REGOLE_NASCITA[(evento, grandezza)]`**, un
        dizionario di MODULO *(74 voci)*. L'involucro ### **chiama l'originale** e poi
        ### **osserva quali chiavi d'arco sono comparse**: ### **non cambia niente.**

        ### ⚠ **E TOCCA IL MODULO, non `net`**, quindi il presidio di `net` non lo
        copre: ### **si ripristina a corsa chiusa** *(`ripristina_involucri`)*, e
        ### **la BYTE-INERZIA e' il controllo che dice se ha cambiato la dinamica.**
        """
        self._involucri = []
        for ev, gr in ((("divisione", "i"), "divisione"), (("schwinger", "i"), "schwinger")):
            voce = S.REGOLE_NASCITA.get(ev)
            if voce is None:
                raise SystemExit("[FERMO] regola di nascita `%s` assente." % (ev,))
            orig = voce["regola"]
            etich = gr

            def _invol(_net, _c, _orig=orig, _et=etich):
                _prima = set(chiavi_archi(_net).tolist())
                _r = _orig(_net, _c)
                for _k in set(chiavi_archi(_net).tolist()) - _prima:
                    self.origine[int(_k)] = _et
                return _r

            voce["regola"] = _invol
            self._involucri.append((voce, orig))
        # ### E `_allaccia` E' UN METODO DI `net`: si avvolge sull'ISTANZA.
        _oa = net._allaccia

        def _inv_all(*a, **kw):
            _prima = set(chiavi_archi(net).tolist())
            _r = _oa(*a, **kw)
            for _k in set(chiavi_archi(net).tolist()) - _prima:
                self.origine[int(_k)] = "allaccia"
            return _r

        # ### ⛔ **`_allaccia` E' UN METODO DI CLASSE, e assegnarlo su `net` CREA UN
        #   ATTRIBUTO D'ISTANZA che prima non c'era.** ### **Quindi il ripristino non e'
        #   una riassegnazione: e' una CANCELLAZIONE** -- e si registra ### **se la chiave
        #   c'era**, invece di indovinarlo. ### ⚠ **E' LA STESSA REGOLA CHE `sola_lettura`
        #   APPLICA GIA' ALLE CHIAVI NUOVE**, e che qui non avevo applicato: ### **la
        #   BYTE-INERZIA l'ha presa, con `240` attributi identici e UNO in piu'.**
        _cera = "_allaccia" in net.__dict__
        net._allaccia = _inv_all
        self._involucri.append((None, (net, _oa, _cera)))
        # ### TUTTO CIO' CHE ESISTE AL PASSO `0` E' `seminato`, per definizione.
        for _k in chiavi_archi(net).tolist():
            self.origine[int(_k)] = "seminato"
        return len(self.origine)

    def ripristina_involucri(self, net):
        """### **A corsa chiusa gli involucri si TOLGONO**, e si verifica che siano tolti."""
        if not self._involucri:
            return 0
        n = 0
        for voce, orig in self._involucri:
            if voce is None:
                _net, _oa, _cera = orig
                if _cera:
                    _net._allaccia = _oa
                else:
                    # ### **LA CHIAVE NON C'ERA: si CANCELLA**, e il metodo di classe
                    #   torna visibile da se'.
                    net_d = _net.__dict__
                    if "_allaccia" in net_d:
                        del net_d["_allaccia"]
                n += 1
            else:
                voce["regola"] = orig
                n += 1
        self._involucri = None
        return n

    # ---------------------------------------------------------------- M5(b): l'accumulo
    def _accumula(self, S, net, cur, pr):
        """L'accumulatore PARALLELO del dipolo, e l'ETA' dell'arco. ### **Per CHIAVE.**

        ### ⛔ **PER CHIAVE E NON PER INDICE**, perche' alla mitosi gli indici si
        rimescolano: un accumulatore per indice ### **mescolerebbe la storia di due archi
        diversi.** ### **Un arco nuovo parte da `0`, e la sua eta' da `0`.**
        """
        ch = cur["chiavi"]
        with sola_lettura(net, "_tau_tw_locale") as g:
            tau = np.asarray(S._tau_tw_locale(net), float) * np.ones(len(ch))
        self.toccati.setdefault("_tau_tw_locale", g["toccati"])
        cur["tau_tw"] = tau
        if pr is None:
            self._acc = {"chiavi": ch.copy(), "tw_dip": np.zeros(len(ch)),
                         "nato": np.zeros(len(ch)), "salto": np.full(len(ch), -1.0e18)}
            cur["tw_dip"] = self._acc["tw_dip"].copy()
            cur["eta"] = np.zeros(len(ch))
            cur["salto_recente"] = np.zeros(len(ch), bool)
            return
        A = self._acc
        # --- i valori VECCHI, allineati sulle chiavi di ADESSO; gli archi nuovi -> `0`
        vecchi = {}
        for nome, zero in (("tw_dip", 0.0), ("nato", float(self.passo)),
                           ("salto", -1.0e18)):
            o = np.argsort(A["chiavi"], kind="stable")
            sa = A["chiavi"][o]
            pos = np.searchsorted(sa, ch)
            pos = np.minimum(pos, max(sa.size - 1, 0))
            ok = (sa.size > 0) & (sa[pos] == ch)
            v = np.full(len(ch), zero)
            v[ok] = A[nome][o][pos[ok]]
            vecchi[nome] = v
        # --- `Delta dipolo` VERO: `twp_dip` di adesso contro quello di prima
        dprec, dora, _n = allinea(pr["chiavi"], pr["twp_dip"], ch, cur["twp_dip"])
        ddip = np.zeros(len(ch))
        o = np.argsort(pr["chiavi"], kind="stable")
        sa = pr["chiavi"][o]
        pos = np.searchsorted(sa, ch)
        pos = np.minimum(pos, max(sa.size - 1, 0))
        ok = (sa.size > 0) & (sa[pos] == ch)
        ddip[ok] = (np.nan_to_num(cur["twp_dip"][ok])
                    - np.nan_to_num(np.asarray(pr["twp_dip"])[o][pos[ok]]))
        nuovo = ~ok
        # ### UN ARCO NUOVO NON HA UN `Delta`: la sua spinta e' ZERO al primo passo, ed e'
        #   la STESSA regola del `NaN` del simulatore.
        ddip[nuovo] = 0.0
        td = vecchi["tw_dip"] + ddip - cur["dt_e"] * vecchi["tw_dip"] / np.maximum(tau, 1e-12)
        td[nuovo] = 0.0
        salto = np.where(np.abs(ddip) > 1e-9, float(self.passo), vecchi["salto"])
        self._acc = {"chiavi": ch.copy(), "tw_dip": td, "nato": vecchi["nato"],
                     "salto": salto}
        cur["tw_dip"] = td.copy()
        # ### L'ETA' IN UNITA' DI `tau_tw`: `(passo - nato) * dt_e / tau_tw`.
        cur["eta"] = ((float(self.passo) - vecchi["nato"]) * cur["dt_e"]
                      / np.maximum(tau, 1e-12))
        # ### ⛔ **L'ETA' IN PASSI, e serve a UNA COSA SOLA: escludere IL PRIMO PASSO di un
        #   arco.** Al suo primo passo `twp` e `twp_dip` ### **non sono ancora stati
        #   scritti dalla dinamica** *(`twp` nasce a `0`, `twp_dip` a `NaN`)*, quindi una
        #   differenza fra il primo e il secondo passo ### **non misura la dinamica: misura
        #   l'inizializzazione.** ### **E' la STESSA ragione per cui il simulatore mette
        #   `NaN` in `twp_dip` e da' spinta ZERO al primo passo.**
        cur["eta_passi"] = float(self.passo) - vecchi["nato"]
        _maturo = cur["eta_passi"] >= 2.0
        cur["maturo"] = _maturo
        # ### E IL SALTO SI REGISTRA SOLO SUGLI ARCHI MATURI: senza questo, al passo `1`
        #   risultavano `235491` archi <<toccati da un salto>>, e ### **era il `NaN`
        #   iniziale letto come un salto.**
        salto = np.where(_maturo, salto, -1.0e18)
        self._acc["salto"] = salto
        cur["salto_recente"] = _maturo & ((float(self.passo) - salto) <= FINESTRA_SALTO)

    # ---------------------------------------------------------------- M5
    def m5(self, S, net, cur, cl):
        """`M5` — LE MEMORIE. ### **Tutto in SOLA LETTURA, da `net` e dall'accumulatore.**"""
        n = int(net.n)
        ii = np.asarray(net.i, int); jj = np.asarray(net.j, int)
        m = (ii < n) & (jj < n)
        ph0 = np.asarray(net.phi0, float)[:n]
        tw = cur["tw"]
        with sola_lettura(net, "_wphi") as g:
            dph = np.asarray(net._wphi(np.asarray(net.phi, float)[ii]
                                       - np.asarray(net.phi, float)[jj]), float)
        self.toccati.setdefault("_wphi", g["toccati"])
        c0 = np.full(len(ii), np.nan)
        c0[m] = np.cos(ph0[ii[m]] - ph0[jj[m]])
        cd = np.cos(dph - tw)
        # --- la classe dell'arco: quella del nodo `i` (DICHIARATO)
        cla = np.full(len(ii), -1, int)
        cla[m] = cl[ii[m]]
        ori = np.array([self.origine.get(int(k), "?") for k in cur["chiavi"]], dtype=object)
        eta = cur["eta"]
        se = secchio_eta(eta)
        buoni = m & ~np.isnan(c0)

        def _coppia(sel):
            """Spearman fra `c0` e `c_delta` su un sottoinsieme. ### **`None` se poco.**"""
            s = sel & buoni
            q = int(np.sum(s))
            if q < 3:
                return None, q
            a = _rankdata(c0[s]); b = _rankdata(cd[s])
            if np.std(a) < 1e-12 or np.std(b) < 1e-12:
                return None, q
            return float(np.corrcoef(a, b)[0, 1]), q

        fuori = {"n_archi": int(len(ii)), "n_confrontabili": int(np.sum(buoni))}
        # --- (a) per CLASSE
        pc = {}
        for q_, nome in enumerate(_MZD.CLASSI):
            s = buoni & (cla == q_)
            r, q = _coppia(s)
            pc[nome] = {"spearman": r, "n": q,
                        "q_diff": ([float(x) for x in
                                    np.percentile(cd[s] - c0[s], [5, 25, 50, 75, 95])]
                                   if q else None),
                        "segno_discorde": (float(np.mean(np.sign(cd[s]) != np.sign(c0[s])))
                                           if q else None)}
        fuori["a_per_classe"] = pc
        # --- (a) per ORIGINE
        po = {}
        for nome in ORIGINI:
            s = buoni & (ori == nome)
            r, q = _coppia(s)
            po[nome] = {"spearman": r, "n": q}
        po["?"] = {"n": int(np.sum(ori == "?"))}
        fuori["a_per_origine"] = po
        # --- (a) per ETA', e IL CRITERIO: VUOTO con eta' > 2 tau_tw
        pe = {}
        for k2, (lo, hi) in enumerate(SECCHI_ETA):
            s = buoni & (se == k2)
            r, q = _coppia(s)
            pe["%.1f-%s" % (lo, "inf" if hi > 1e17 else "%.1f" % hi)] = {
                "spearman": r, "n": q}
        fuori["a_per_eta"] = pe
        s_cr = buoni & (cla == 2) & (eta > 2.0)
        r_cr, q_cr = _coppia(s_cr)
        fuori["a_criterio"] = {"spearman": r_cr, "n": q_cr,
                               "classe": "VUOTO", "eta_oltre": 2.0}
        # --- (b) la parte del dipolo dentro `tw`
        td = cur.get("tw_dip")
        if td is None:
            fuori["b"] = None
        else:
            den = np.maximum(np.abs(tw), 1e-12)
            rap = np.abs(td) / den
            sr = cur.get("salto_recente", np.zeros(len(ii), bool))
            fuori["b"] = {
                "mediana": float(np.median(rap[m])) if int(np.sum(m)) else None,
                "q": ([float(x) for x in np.percentile(rap[m], [5, 25, 50, 75, 95])]
                      if int(np.sum(m)) else None),
                "mediana_con_salto_recente": (float(np.median(rap[m & sr]))
                                              if int(np.sum(m & sr)) else None),
                "n_con_salto_recente": int(np.sum(m & sr)),
                "per_classe": per_classe(np.where(m, rap, np.nan), cla)}
        # --- (c) il disordine CONGELATO
        neg = np.full(len(ii), np.nan)
        neg[m] = (c0[m] < 0).astype(float)
        fuori["c"] = {"quota_c0_negativo": per_classe(neg, cla),
                      "quota_totale": (float(np.mean(c0[m] < 0))
                                       if int(np.sum(m)) else None)}
        # --- (d) IL BILANCIO DELLA TORSIONE
        pot = tw ** 2 * cur["dt_e"] / np.maximum(cur["tau_tw"], 1e-12)
        pn = np.zeros(n)
        np.add.at(pn, ii[m], 0.5 * pot[m])
        np.add.at(pn, jj[m], 0.5 * pot[m])
        fuori["d"] = {"potenza_totale": float(np.sum(pot[m])),
                      "per_classe_arco": per_classe(np.where(m, pot, np.nan), cla),
                      "per_nodo_per_classe": per_classe(pn, cl)}
        mm = fuori["d"]["per_nodo_per_classe"].get("MATERIA")
        vv = fuori["d"]["per_nodo_per_classe"].get("VUOTO")
        # ### ⛔ **CON IL DENOMINATORE A ZERO IL CRITERIO NON E' FALSO: E' NON
        #   DECIDIBILE.** Al passo `1` `tw = 0` su tutti gli archi, quindi entrambe le
        #   mediane sono `0` e `0 < 0.25*0` dava ### **`False`** -- cioe' *<<la
        #   dissipazione NON sta nel vuoto>>* letto da ### **un'assenza di dissipazione.**
        #   ### **E' la famiglia di `CHI-TORS-ZERO-FALSO`.**
        if not (mm and vv) or mm["mediana"] is None or vv["mediana"] is None:
            fuori["d"]["criterio_materia_sotto_un_quarto"] = None
        elif vv["mediana"] <= 0.0:
            fuori["d"]["criterio_materia_sotto_un_quarto"] = None
            fuori["d"]["criterio_nota"] = ("NON DECIDIBILE: la potenza nel VUOTO e' zero, "
                                           "quindi non c'e' niente da confrontare")
        else:
            fuori["d"]["criterio_materia_sotto_un_quarto"] = bool(
                mm["mediana"] < 0.25 * vv["mediana"])
        return fuori

    # ---------------------------------------------------------------- il giro
    def osserva(self, S, net, k, pesante):
        self.passo = k
        n = int(net.n)
        # ### ⛔ **IL CONTROLLO CHE RENDE VALIDO IL CONFRONTO PER INDICE:** se `n` scendesse,
        #   i nodi NON nascerebbero solo in coda e confrontare `perc_geom[k]` fra due passi
        #   sarebbe un errore muto. ### **Si ferma, non si avvisa.**
        if self.n_prec is not None and n < self.n_prec:
            raise SystemExit("[FERMO] `n` e' SCESO da %d a %d al passo %d: il confronto dei "
                             "nodi per indice non e' piu' valido." % (self.n_prec, n, k))
        self.n_prec = n
        cur = self._a_e_d(net)
        pr = self._prec
        # ### ⛔ **L'ACCUMULO VA PRIMA DELLA RIGA, e il giro corto me l'ha mostrato:** la
        #   riga usa `cur["maturo"]`, che e' ### **l'accumulatore a scriverlo.** Con
        #   l'ordine invertito la spinta risultava ### **`None` a OGNI passo**, cioe' la
        #   misura centrale del lavoro ### **non si misurava.**
        self._accumula(S, net, cur, pr)
        riga_p = {"passo": k, "n": n, "archi": int(len(net.i)),
                  # ### IL FATTO CHE MI ERA SFUGGITO ora si MISURA a OGNI passo, invece
                  #   di essere assunto una volta e creduto per sempre.
                  "archi_i_maggiore_j": cur["archi_i_maggiore_j"]}
        if pr is None:
            riga_p.update({"nodi_confrontabili": None, "cambi_A_grezza": None,
                           "cambi_A_divg": None, "cambi_perc_geom": None,
                           "archi_confrontabili": None, "cambi_D_segno_tw": None})
        else:
            nc = min(pr["n"], n)
            riga_p["nodi_confrontabili"] = nc
            riga_p["nodi_nuovi"] = n - pr["n"]
            riga_p["cambi_A_grezza"] = int(np.sum(
                cur["sg_grezza"][:nc] != pr["sg_grezza"][:nc]))
            riga_p["cambi_A_divg"] = int(np.sum(cur["sg_divg"][:nc] != pr["sg_divg"][:nc]))
            riga_p["cambi_perc_geom"] = int(np.sum(
                cur["perc_geom"][:nc] != pr["perc_geom"][:nc]))
            riga_p["A_grezza_zero"] = int(np.sum(cur["sg_grezza"] == 0))
            riga_p["A_divg_zero"] = int(np.sum(cur["sg_divg"] == 0))
            a, b, nco = allinea(pr["chiavi"], pr["sg_tw"], cur["chiavi"], cur["sg_tw"])
            riga_p["archi_confrontabili"] = nco
            riga_p["archi_nuovi"] = int(len(cur["chiavi"]) - nco)
            riga_p["cambi_D_segno_tw"] = int(np.sum(a != b)) if nco else None
            am, bm, _n = allinea(pr["chiavi"], pr["sg_mem"], cur["chiavi"], cur["sg_mem"])
            riga_p["cambi_MEM_segno_delta"] = int(np.sum(am != bm)) if nco else None
            # ### ⭐ **LA SPINTA INIETTATA, IL METRO GIUSTO:** per ciascuna opzione,
            #   `Somma |Delta dipolo|` fra due passi, ### **allineata per CHIAVE** e con
            #   gli archi non confrontabili ### **CONTATI e ESCLUSI** *(mai zero al loro
            #   posto: e' la lezione di `CHI-TORS-ZERO-FALSO`)*.
            # ### ⛔ **SI ESCLUDONO GLI ARCHI AL LORO PRIMO PASSO, PER TUTTE E QUATTRO LE
            #   OPZIONI.** Per `perc_geom`, `A` e `D` non cambia niente *(la loro spinta
            #   li' e' gia' `~0`)*; per ### **`MEM` cambia tutto**: al passo `1`
            #   iniettava `597235` ### **perche' `delta` parte da `dph`**, e quello e'
            #   ### **l'avvio, non la dinamica.** ### ✔ **La regola e' UNIFORME e
            #   DICHIARATA**, non un'eccezione per l'opzione scomoda.
            sp, spn = {}, {}
            _mat = cur.get("maturo")
            for et in ("perc_geom", "A", "D", "MEM"):
                x, y, nn = allinea(pr["chiavi"], pr["dip"][et],
                                   cur["chiavi"], cur["dip"][et])
                if not nn:
                    sp[et], spn[et] = None, 0
                    continue
                if _mat is None:
                    sp[et], spn[et] = None, 0
                    continue
                _xm, _ym, _nm = allinea(pr["chiavi"], pr["dip"][et],
                                        cur["chiavi"][_mat], cur["dip"][et][_mat])
                sp[et] = float(np.sum(np.abs(_ym - _xm))) if _nm else None
                spn[et] = _nm
            riga_p["spinta_iniettata"] = sp
            riga_p["spinta_n_maturi"] = spn
            riga_p["spinta_n_confrontabili"] = nco
        riga_p["fraz_tw_oltre_2pi"] = cur["fraz_tw_oltre_2pi"]
        # ### L'ACCUMULATORE PARALLELO di `M5(b)`: `tw_dip' = tw_dip + Delta dipolo
        #   - dt_e*tw_dip/tau_tw`, e ### **parte da `0` ALLA NASCITA dell'arco.**
        #   ### ⚠ **E' PARALLELO: non tocca `net`.** Serve a dire ### **quanta parte di
        #   `tw` viene dal DIPOLO** invece che dalla fase.
        self.passi.append(riga_p)
        self._prec = cur
        if not pesante:
            return
        cl, u = self.classe_nodi(net)
        dati = {"passo": k, "n": n, "archi": int(len(net.i)),
                "classi": {nome: int(np.sum(cl == q_)) for q_, nome in enumerate(_MZD.CLASSI)},
                "M3_C": self.m3_cicli(net)}
        if k in PASSI_MISURA:
            dati["M1"] = self.m1(S, net)
            dati["M2"] = self.m2(S, net, cl)
            dati["M5"] = self.m5(S, net, cur, cl)
        self.pesanti[k] = dati

    def chiudi(self):
        """Le differenze fra i passi pesanti ### **e il loro PREDECESSORE.**"""
        for k in PASSI_MISURA:
            d = self.pesanti.get(k)
            p = self.pesanti.get(k - 1)
            if d is None:
                continue
            m = dict(d)
            fc = m.pop("M3_C")
            fp = (p or {}).get("M3_C")
            cam = None
            if fp is not None:
                a = set(fc["_firme"]); b = set(fp["_firme"])
                cam = {"cicli_oggi": len(a), "cicli_prima": len(b),
                       "spariti": len(b - a), "nuovi": len(a - b),
                       "frazione_cambiata": (float(len(a - b)) / max(len(a), 1))}
            fc = {x: y for x, y in fc.items() if x != "_firme"}
            m["M3_C"] = fc
            m["M3_C_cambio_base"] = cam
            m["passo_precedente"] = (k - 1) if p is not None else None
            self.misure[k] = m

    def esito(self):
        self.chiudi()
        # ### GLI AGGREGATI SU TUTTA LA CORSA: la spinta iniettata TOTALE per opzione, e
        #   i passi su cui e' stata confrontabile. ### **Un totale senza il suo
        #   denominatore non e' un totale.**
        # ### ⚠ **IL TOTALE DA SOLO NON BASTA, e il giro corto lo mostra:** al passo `2`
        #   le spinte sono ### **da `278186` a `739817`**, e nei passi quieti
        #   ### **da `0` a `2030`**. ### **Un totale dominato da UN transitorio dice del
        #   transitorio, non del regime.** ### ✔ **Quindi si riporta anche la MEDIANA per
        #   passo**, che un singolo transitorio non sposta.
        tot, nn, med = {}, {}, {}
        for et in ("perc_geom", "A", "D", "MEM"):
            v = [r["spinta_iniettata"][et] for r in self.passi
                 if r.get("spinta_iniettata") and r["spinta_iniettata"].get(et) is not None]
            tot[et] = float(sum(v)) if v else None
            nn[et] = len(v)
            med[et] = float(np.median(v)) if v else None
        return {"geometria": self.geo, "passi": self.passi,
                "spinta_totale": tot, "spinta_passi": nn, "spinta_mediana": med,
                "origini_registrate": {k: sum(1 for x in self.origine.values() if x == k)
                                       for k in ORIGINI},
                "misure": {str(k): v for k, v in sorted(self.misure.items())},
                "passi_misura": list(PASSI_MISURA),
                "passi_pesanti": list(PASSI_PESANTI),
                "secchi_grado": [list(x) for x in SECCHI_GRADO],
                "scritture_misurate": self.toccati, "avvisi": self.avvisi}


# ====================================================================== il motore
def corsa(nome, passi, osservatori, scrivi, battito=True):
    """Il giro condiviso. ### **Nessuna copia patchata: gira il simulatore VERO.**"""
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    pf = piattaforma()
    b = blob(SIM)[:8]
    stampa("  simulatore %s   atteso %s" % (b, BLOB_ATTESO))
    if b != BLOB_ATTESO:
        stampa("  ### IL BLOB DEL SIMULATORE NON E' QUELLO ATTESO. MI FERMO.")
        scrivi({"esito": 1, "stato": "BLOB SBAGLIATO", "blob_trovato": b,
                "blob_atteso": BLOB_ATTESO, "piattaforma": pf})
        return 1
    stampa("  ### il blob COINCIDE: la misura vale per questo simulatore.")
    S, N, _a = carica(nome, SIM)
    in_conf = _cli_flag.dichiara_configurazione(S, stampa)
    stampa("  scena: n = %d, archi = %d, DT = %r" % (N.n, len(N.i), S.DT))
    for o in osservatori:
        g = o.prepara(S, N)
        stampa("  %-10s geometria: %s" % (o.nome, g))
    stampa()
    riga("=")
    stampa("LA CORSA: %d passi, UN braccio, SOLA LETTURA" % passi)
    riga("=")
    t0 = time.time()
    pesanti = set(k for k in PASSI_PESANTI if k <= passi) | {0}

    def _ist(stato, k, err=None):
        d = {"piattaforma": pf, "passi": passi, "passi_girati": k, "stato": stato,
             "blob_sim": blob(SIM), "blob_atteso": BLOB_ATTESO,
             "blob_strumento": blob(__file__),
             "in_configurazione_del_driver": bool(in_conf),
             "secondi": round(time.time() - t0, 1),
             "a_valle": {"n": int(N.n), "archi": int(len(N.i))}}
        for o in osservatori:
            d[o.nome] = o.esito()
        if err is not None:
            d["errore"] = err
        scrivi(d)
        return d

    # ### IL PASSO `0`: lo stato PRIMA del primo passo, e serve come predecessore del `1`.
    for o in osservatori:
        o.osserva(S, N, 0, True)
    for k in range(1, passi + 1):
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                _passo.passo_pieno(S, N)
            pes = k in pesanti
            t1 = time.time()
            for o in osservatori:
                o.osserva(S, N, k, pes)
            if battito:
                print("  passo %4d/%d  n %5d  archi %7d  %s%s"
                      % (k, passi, N.n, len(N.i), "PESANTE " if pes else "",
                         ("%.1fs" % (time.time() - t1)) if pes else ""), flush=True)
            if k % PASSI_SALVA == 0:
                _ist("IN CORSO", k)
        except SystemExit:
            raise
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            stampa("### LA CORSA E' CADUTA AL PASSO %d: %r" % (k, e))
            stampa(tb)
            try:
                _ist("CADUTA al passo %d" % k, k,
                     err={"passo": k, "errore": repr(e), "traccia": tb})
            except Exception as e2:
                stampa("### ⛔ E IL SALVATAGGIO E' CADUTO ANCHE LUI: %r" % (e2,))
                stampa(traceback.format_exc())
            return 1
    # ### ⛔ **GLI INVOLUCRI SI TOLGONO A CORSA CHIUSA, e si VERIFICA che siano tolti:**
    #   lasciarli attaccati farebbe sbagliare la corsa DOPO, e un ripristino che non si
    #   controlla e' una promessa.
    for o in osservatori:
        if hasattr(o, "ripristina_involucri"):
            q = o.ripristina_involucri(N)
            stampa("  involucri rimossi da %s: %d" % (o.nome, q))
            if o._involucri is not None:
                stampa("  ### ⛔ GLI INVOLUCRI NON SONO STATI TOLTI. Lo dico.")
                return 1
    _ist("DATI SALVATI", passi)
    stampa("  ### I DATI SONO SALVATI.")
    return 0


def _scrivi(d):
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    io.open(os.path.join(FUORI, "verso.json"), "w", encoding="utf-8").write(
        json.dumps(d, indent=1, default=str))
    io.open(os.path.join(FUORI, "verso.txt"), "w", encoding="utf-8").write(
        NL.join(_MSG.P) + NL)


# ====================================================================== il collaudo
def collaudo():
    esiti = []

    def prova(et, ok):
        esiti.append(bool(ok))
        stampa("  %s  %s" % ("ok  " if ok else "FALLITO", et))

    # ---- il presidio, su un oggetto FINTO: si verifica che FUNZIONI e che SAPPIA FALLIRE
    class Finto(object):
        pass

    f = Finto()
    f.a = np.arange(5.0); f.b = 3; f.lista = [1, 2]
    with sola_lettura(f, "prova") as g:
        f.a[0] = 99.0
        f.nuovo = "c'e'"
        f.b = 7
    prova("presidio: ### ripristina un ARRAY mutato in place", f.a[0] == 0.0)
    prova("presidio: ### TOGLIE una chiave NUOVA", not hasattr(f, "nuovo"))
    prova("presidio: ### ripristina uno scalare", f.b == 3)
    prova("presidio: ### e MISURA che cosa e' stato toccato (a, b, nuovo)",
          set(g["toccati"]) == {"a", "b", "nuovo"})
    prova("presidio: ### dichiara il ripristino esatto", g["ripristino_esatto"] is True)
    with sola_lettura(f, "niente") as g2:
        pass
    prova("presidio: ### una chiamata che non scrive da `toccati` VUOTO", g2["toccati"] == [])

    # ---- il presidio DEVE accorgersi di un ripristino impossibile
    class Ostile(object):
        pass

    o = Ostile()
    o.x = np.arange(3.0)
    # ### ⚠ **LA MIA PRIMA VERSIONE DI QUESTO CASO NON FALLIVA, e aveva ragione il
    #   codice:** mettevo il valore non copiabile ### **DENTRO** il `with`, e un valore
    #   messo DOPO lo scatto ### **si ripristina benissimo** -- basta riassegnare la copia
    #   salvata. ### **Il caso vero e' un valore non copiabile GIA' PRESENTE allo scatto:**
    #   li' il presidio ### **non PUO' proteggere niente, e deve RIFIUTARSI** invece di
    #   fingere di proteggere.
    o.y = _NonCopiabile()
    rotto = False
    try:
        with sola_lettura(o, "ostile"):
            pass
    except Exception:
        rotto = True
    prova("presidio: ### DEVE FALLIRE -- cio' che NON si copia non si GUARDA, e il "
          "presidio si RIFIUTA invece di fingere", rotto)
    del o.y
    # ### ✔ **E LA FIRMA DEVE ESSERE STABILE**, altrimenti il presidio grida al lupo: una
    #   firma che cambia da sola farebbe fallire OGNI chiamata guardata.
    import numpy.random as _nr
    camp = [np.arange(4.0), 3, 2.5, "x", None, [1, 2], {"a": 1}, (1, "x"),
            {"b": np.arange(3.0)}, _sp.csr_matrix(np.eye(3)), _nr.default_rng(11)]
    prova("presidio: ### la firma e' STABILE sui tipi veri di `net` (array, sparse, rng...)",
          all(_firma(v) == _firma(v) for v in camp))
    # ### ⛔ **IL CASO CHE IL MIO COLLAUDO NON AVEVA, e la corsa l'ha trovato al primo
    #   giro:** `_g_registro_apparse` e' un ### **`set`**, e la firma basata su `repr`
    #   ### **cambiava dopo un `deepcopy` a CONTENUTO IDENTICO.** ### **La mia prova di
    #   stabilita' usava un `dict` e mai un `set`: era PIU' DEBOLE del codice che doveva
    #   proteggere.** Ora la firma di un insieme e' ORDINATA, e il caso c'e'.
    _ins = set("abcdefghijklmnopqrstuvwxyz")
    prova("presidio: ### DEVE FALLIRE -- un `set` deepcopy-ato ha la STESSA firma",
          _firma(_ins) == _firma(copy.deepcopy(_ins)))
    prova("presidio: ### e un `set` con un elemento IN MENO ha una firma DIVERSA",
          _firma(_ins) != _firma(_ins - {"a"}))
    _d = {"x": np.arange(3.0), "y": {1, 2}}
    prova("presidio: ### e lo stesso vale per un dict che CONTIENE un set e un array",
          _firma(_d) == _firma(copy.deepcopy(_d))
          and _firma(_d) != _firma({"x": np.arange(3.0) + 1, "y": {1, 2}}))
    prova("presidio: ### e DISTINGUE due array diversi",
          _firma(np.arange(3.0)) != _firma(np.arange(3.0) + 1))

    # ---- le chiavi d'arco e l'allineamento
    class Rete(object):
        pass

    r1 = Rete(); r1.i = np.array([0, 1, 2]); r1.j = np.array([1, 2, 3])
    r2 = Rete(); r2.i = np.array([1, 0, 5]); r2.j = np.array([2, 1, 6])
    c1, c2 = chiavi_archi(r1), chiavi_archi(r2)
    prova("chiavi: ### la chiave e' CANONICA `(min, max)*BASE`, e BASE e' sopra `n`",
          c1[0] == 0 * BASE_CHIAVE + 1 and BASE_CHIAVE > 100000)
    # --- ### ⛔ **IL CASO CHE LA CORSA DEL 2026-10-06 HA RESO NECESSARIO:** un arco
    #   scritto `(1,0)` e uno scritto `(0,1)` sono ### **LO STESSO ARCO**, e la chiave
    #   deve dirlo. ### **Con la chiave `i*BASE + j` non lo diceva.**
    rv = Rete(); rv.i = np.array([1, 2]); rv.j = np.array([0, 1])
    cv = chiavi_archi(rv)
    # ### ⚠ **E L'INDICE SBAGLIATO ERA MIO:** avevo scritto `c1[2]`, che e' la coppia
    #   `(2,3)`, mentre `cv[1]` e' la coppia `(1,2)`, cioe' `c1[1]`.
    #   ### **Il collaudo ha trovato un errore nel COLLAUDO, non nel codice.**
    prova("chiavi: ### un arco scritto al ROVESCIO ha la STESSA chiave",
          cv[0] == c1[0] and cv[1] == c1[1])
    prova("chiavi: ### DEVE FALLIRE -- con la chiave vecchia `i*BASE + j` NON coincideva",
          (1 * BASE_CHIAVE + 0) != c1[0])
    # --- ### e `tw` si riduce al verso canonico, altrimenti `D` conterebbe un cambio di
    #   segno dove e' cambiata solo la SCRITTURA dell'arco.
    rv.tw = np.array([3.0, -5.0])
    tc = tw_canonico(rv)
    prova("tw_canonico: ### l'arco scritto `(1,0)` ribalta il segno di `tw`",
          tc[0] == -3.0 and tc[1] == 5.0)
    rd = Rete(); rd.i = np.array([0, 1]); rd.j = np.array([1, 2])
    rd.tw = np.array([-3.0, 5.0])
    prova("tw_canonico: ### quindi la STESSA forma scritta nei due modi da' lo STESSO segno",
          list(np.sign(tw_canonico(rd))) == list(np.sign(tc)))
    a, b, nco = allinea(c1, np.array([1.0, -1.0, 1.0]), c2, np.array([-1.0, 1.0, 1.0]))
    prova("allinea: ### trova i DUE archi comuni, non tre", nco == 2)
    prova("allinea: ### li allinea per CHIAVE e non per indice -- (1,2) e (0,1)",
          list(a) == [-1.0, 1.0] and list(b) == [-1.0, 1.0])
    # ### ⚠ **LA MIA PRIMA VERSIONE DICEVA <<3>>, e il conto giusto e' `2`:** le serie
    #   sono `[1,-1,1]` e `[-1,1,1]`, e il TERZO elemento COINCIDE. ### **Il collaudo ha
    #   trovato un errore nel COLLAUDO, non nel codice** -- e il numero sbagliato era mio.
    prova("allinea: ### ZERO cambi di segno, e per INDICE ne avrebbe visti DUE (falsi)",
          int(np.sum(a != b)) == 0
          and int(np.sum(np.array([1.0, -1.0, 1.0]) != np.array([-1.0, 1.0, 1.0]))) == 2)
    a0, b0, n0 = allinea(np.zeros(0, np.int64), np.zeros(0), c2, np.array([1.0, 1.0, 1.0]))
    prova("allinea: ### DEVE FALLIRE -- senza archi prima, ZERO confrontabili", n0 == 0)

    # ---- `AUC`
    prova("auc: ### due campioni identici danno 0.5", abs(auc([1, 2, 3], [1, 2, 3]) - 0.5) < 1e-12)
    prova("auc: ### separazione totale da 1.0", auc([10, 11], [1, 2]) == 1.0)
    prova("auc: ### e al contrario 0.0", auc([1, 2], [10, 11]) == 0.0)
    prova("auc: ### un campione vuoto da `None`, non 0.5", auc([], [1, 2]) is None)

    # ---- `per_classe`
    pc = per_classe(np.array([1.0, 2.0, 3.0]), np.array([0, 0, 2]))
    prova("per_classe: ### MATERIA ha 2 nodi e mediana 1.5",
          pc["MATERIA"]["n"] == 2 and pc["MATERIA"]["mediana"] == 1.5)
    prova("per_classe: ### una classe VUOTA da `None`, non zero", pc["BORDO"] is None)

    # ---- `satura` e il denominatore: il MOTIVO della correzione
    import importlib.util as _iu
    sp_ = _iu.spec_from_file_location("sim_coll", SIM)
    mod = _iu.module_from_spec(sp_)
    with contextlib.redirect_stdout(io.StringIO()):
        sp_.loader.exec_module(mod)
    cls = next((getattr(mod, x) for x in dir(mod)
                if isinstance(getattr(mod, x), type) and hasattr(getattr(mod, x), "satura")),
               None)
    if cls is None:
        raise SystemExit("[FERMO] nessuna classe con `satura` nel simulatore.")
    sat = cls.satura
    F = 3.0 + 4.0j
    prova("satura: ### |satura(f)| = satura(|f|) -- vale sul MODULO",
          abs(abs(sat(F)) - abs(sat(abs(F)))) < 1e-12)
    prova("satura: ### e' MONOTONA crescente nel modulo", sat(10.0) > sat(1.0))
    prova("satura: ### quindi col denominatore SATURO c_k <= 1 (qui 5 su 5)",
          abs(sat(abs(F)) / sat(5.0) - 1.0) < 1e-12)
    prova("satura: ### DEVE FALLIRE -- col denominatore NUDO il rapporto NON arriva a 1",
          sat(abs(F)) / 5.0 < 0.9)
    prova("satura: ### il tetto e' 1/GAMMA", abs(sat(1e12) - 1.0 / mod.GAMMA) < 1e-3)

    # ---- l'algebra dell'olonomia: il multiplo di `4pi`
    prova("olonomia: ### `FASE_2PI` e' False, quindi il dominio di phi e' 4pi",
          mod.FASE_2PI is False)
    _ph = np.array([0.3, 2.0, -1.1, 5.0])
    _seq = [(0, 1), (1, 2), (2, 3), (3, 0)]
    _s = sum(cls._wphi(_ph[x] - _ph[y]) for x, y in _seq)
    prova("olonomia: ### su un ciclo chiuso la somma e' un multiplo di 4pi (scarto ~0)",
          abs(_s - round(_s / P4) * P4) < 1e-9)

    # ---- `A` e la convenzione di `tw`: l'errore del guardiano, in forma di controllo
    tw = np.array([1.0, 1.0]); ii = np.array([0, 1]); jj = np.array([1, 2])
    gz = np.zeros(3); dv = np.zeros(3)
    np.add.at(gz, ii, tw); np.add.at(gz, jj, tw)
    np.add.at(dv, ii, tw); np.add.at(dv, jj, -tw)
    prova("A: ### la GREZZA somma entranti e uscenti col MEDESIMO segno (nodo 1 -> 2.0)",
          gz[1] == 2.0)
    prova("A: ### la DIVERGENZA li oppone, e sul nodo di mezzo si ANNULLA (nodo 1 -> 0.0)",
          dv[1] == 0.0)
    prova("A: ### sono DUE grandezze diverse, e il mandato ne nomina una sola",
          gz[1] != dv[1])

    # ================================================================ A1: le estensioni
    class R2(object):
        pass

    # ---- `dipoli_opzioni`: le QUATTRO forme, su una rete minima
    rr = R2()
    rr.n = 3
    rr.i = np.array([0, 1]); rr.j = np.array([1, 2])
    rr.tw = np.array([P2PI, 0.0])          # il primo arco a `2pi`, il secondo a zero
    rr.twp = np.array([0.0, 0.0])
    rr.perc_geom = np.array([1.0, -1.0, 1.0])
    rr._chi_geom_nodi = np.array([1.0, -1.0, 1.0])
    dd = dipoli_opzioni(rr, rr.twp - rr.tw)
    prova("dipoli: ### `perc_geom` da' `pi*0.5*(chi_i - chi_j)`, cioe' `pi` sul primo arco",
          abs(dd["perc_geom"][0] - np.pi) < 1e-12)
    prova("dipoli: ### `D` e' `pi*tanh(tw/2pi)`: `pi*tanh(1)` sul primo, ZERO sul secondo",
          abs(dd["D"][0] - np.pi * np.tanh(1.0)) < 1e-12 and dd["D"][1] == 0.0)
    prova("dipoli: ### `D` DEVE FALLIRE a dare `pi` esatto -- `tanh(1) = 0.7616`, non `1`",
          abs(dd["D"][0] - np.pi) > 0.5)
    prova("dipoli: ### `MEM` usa `delta = twp - tw`, quindi col `twp` a zero e' `-D`",
          abs(dd["MEM"][0] + dd["D"][0]) < 1e-12)
    # `A`: la somma GREZZA sul nodo 1 e' `tw[0] + tw[1] = 2pi > 0`, sul nodo 0 e' `2pi > 0`
    prova("dipoli: ### `A` e' il SEGNO della somma grezza: nodi 0 e 1 entrambi `+1` -> ZERO",
          abs(dd["A"][0]) < 1e-12)
    prova("dipoli: ### e sul secondo arco il nodo 2 ha somma ZERO -> `sign = 0` -> `pi*0.5`",
          abs(dd["MEM"][1]) < 1e-12 and abs(dd["A"][1] - np.pi * 0.5) < 1e-12)

    # ---- `secchio_eta`: i limiti DICHIARATI
    se = secchio_eta(np.array([0.0, 0.4, 0.5, 1.5, 3.0, 100.0, -1.0]))
    prova("eta: ### i secchi sono quelli dichiarati, e `0` cade nel primo",
          list(se[:6]) == [0, 0, 1, 2, 3, 4])
    prova("eta: ### DEVE FALLIRE -- un'eta' NEGATIVA non sta in nessun secchio (`-1`)",
          se[6] == -1)

    # ---- ⛔ IL CASO CHE DEVE FALLIRE: un arco al suo PRIMO passo NON contribuisce
    #      alla spinta. ### **E' il difetto che il giro corto ha trovato**: `MEM`
    #      iniettava `597235` al passo `1` perche' `delta` parte da `dph`.
    ch_a = np.array([10, 20], np.int64)
    d_a = np.array([0.0, 0.0])
    ch_b = np.array([10, 20, 30], np.int64)     # `30` e' NUOVO
    d_b = np.array([0.1, 0.2, 999.0])           # e porterebbe una spinta ENORME
    mat = np.array([True, True, False])         # ...ma NON e' maturo
    x, y, nn = allinea(ch_a, d_a, ch_b[mat], d_b[mat])
    prova("primo passo: ### l'arco NUOVO non entra, e la spinta e' `0.1 + 0.2 = 0.3`",
          nn == 2 and abs(float(np.sum(np.abs(y - x))) - 0.3) < 1e-12)
    x2, y2, n2 = allinea(ch_a, d_a, ch_b, d_b)
    prova("primo passo: ### DEVE FALLIRE -- senza il filtro la spinta sarebbe la stessa, "
          "perche' l'allineamento per chiave lo esclude GIA'",
          n2 == 2 and abs(float(np.sum(np.abs(y2 - x2))) - 0.3) < 1e-12)
    # ### ⚠ **E IL CASO VERO E' UN ALTRO, e il collaudo me l'ha chiarito:** un arco che
    #   ESISTEVA ma era al suo PRIMO passo di dinamica ### **E' nelle chiavi di prima**,
    #   quindi l'allineamento NON lo esclude: lo esclude ### **solo il filtro `maturo`.**
    ch_c = np.array([10, 20], np.int64)
    d_c = np.array([0.0, 0.0])
    d_d = np.array([0.1, 999.0])                 # il secondo e' al suo primo passo
    mat2 = np.array([True, False])
    x3, y3, n3 = allinea(ch_c, d_c, ch_c[mat2], d_d[mat2])
    prova("primo passo: ### ECCO il caso vero -- l'arco IMMATURO c'era GIA', e solo il "
          "filtro `maturo` lo tiene fuori: `0.1` invece di `999.1`",
          n3 == 1 and abs(float(np.sum(np.abs(y3 - x3))) - 0.1) < 1e-12)
    x4, y4, n4 = allinea(ch_c, d_c, ch_c, d_d)
    prova("primo passo: ### DEVE FALLIRE -- senza il filtro sarebbe `999.1`",
          abs(float(np.sum(np.abs(y4 - x4))) - 999.1) < 1e-9)

    riga("-")
    stampa("  COLLAUDO: %d su %d" % (sum(esiti), len(esiti)))
    return 0 if all(esiti) else 1


class _NonCopiabile(object):
    def __deepcopy__(self, memo):
        raise RuntimeError("non si copia")

    def __repr__(self):
        return "<non copiabile %d>" % id(self)


# ====================================================================== main
def main(argv):
    if "--collaudo" in argv[1:]:
        riga("=")
        stampa("IL COLLAUDO DI _misura_verso.py")
        riga("=")
        return collaudo()
    passi = PASSI
    for a in argv[1:]:
        if a.startswith("--passi="):
            passi = int(a.split("=", 1)[1])
    riga("=")
    stampa("M1, M2, M3 -- LA MISURA DEL VERSO: %d passi, UN braccio, SOLA LETTURA" % passi)
    riga("=")
    e = corsa("msg_verso", passi, [Verso()], _scrivi)
    io.open(os.path.join(FUORI, "verso.txt"), "w", encoding="utf-8").write(
        NL.join(_MSG.P) + NL)
    return e


if __name__ == "__main__":
    sys.exit(main(sys.argv))
