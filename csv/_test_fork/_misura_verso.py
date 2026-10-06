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
PASSI = 230
PASSI_MISURA = (1, 50, 150, 230)
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
EPS_NORMALE = 1e-12


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
    ii = np.asarray(net.i, np.int64)
    jj = np.asarray(net.j, np.int64)
    return ii * BASE_CHIAVE + jj


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

    # ---------------------------------------------------------------- la scena
    def prepara(self, S, net):
        # ### LA CLASSE VIENE DAL CODICE CHE HA PRODOTTO `27c10bd`, non da una copia:
        #   `_MZD.Misura` si usa SOLO per `prepara` e `_u`. ### **Non viene mai agganciata
        #   come `_MIS`, quindi NESSUN gancio di quello strumento gira qui.**
        self.g = _MZD.Misura(S.DT, 0.0)
        self.geo = self.g.prepara(S, net)
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
        return {"n": n, "chiavi": chiavi_archi(net),
                "sg_grezza": np.sign(grezza), "sg_divg": np.sign(divg),
                "sg_tw": np.sign(tw),
                "perc_geom": np.asarray(net.perc_geom, float)[:n].copy()}

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

    # ---------------------------------------------------------------- il giro
    def osserva(self, S, net, k, pesante):
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
        riga_p = {"passo": k, "n": n, "archi": int(len(net.i))}
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
        return {"geometria": self.geo, "passi": self.passi,
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
    prova("chiavi: ### la chiave e' `i*BASE + j`, e BASE e' sopra `n`",
          c1[0] == 0 * BASE_CHIAVE + 1 and BASE_CHIAVE > 100000)
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
