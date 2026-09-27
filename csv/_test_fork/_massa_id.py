r"""**`MASSA-ID`** — le masse per **LIGNAGGIO**, e il **MEDOIDE PESATO**.

*(Criteri `Y1`-`Y5` committati **prima**, in `0dc51a8`:
`doc/TASK_HISTORY/2026-09-27_massa-id.md`.)*

> ## 🛑 **MI FERMO SU `Y1`/`Y2`, E DICO PERCHE': SERVE MODIFICARE IL SIMULATORE.**
> Il mandato dice *«se un criterio richiede di modificare il simulatore, FERMATI e dillo»*.
> **Lo richiede, e i blocchi sono DUE, indipendenti, verificati dal disco:**
>
> ### ① la scena **NON registra** le tre regioni nel tracking — `soliton_simulator.py:7398`
> ```
> # ⚠ `conc_nodi` NON viene toccato, di proposito: le regioni NON sono masse SEMINATE, e
> #   marcarle come tali direbbe che il lignaggio viene da una semina che non c'e' stata.
> ```
> **Quindi nessun `mass_id` esiste**, e `indici_massa_vivi()` non restituirebbe niente.
> Registrarle *(col `origine="regione coerente"` che la preoccupazione del commento richiede)*
> significa **modificare `_semina_masse_coerenti`**, cioe' **il simulatore**.
>
> ### ② gli stati salvati **NON portano il lignaggio**
> Campi nello `.npz`: **`i, j, d, phi, pos, n, passo, seme, blob`**. **`conc_nodi` non c'e'.**
> Quindi, **anche se la registrazione ci fosse**, `MASSA-ID` **non sarebbe calcolabile OFFLINE da
> questi stati**: servirebbe estendere il salvataggio in `_pilota_prova1_braccio.py`, che **e' nel
> percorso del run IN CORSO** (`par.5`).
>
> **CONSEGUENZA OPERATIVA, detta chiaramente: `MASSA-ID` non entra in questo run.** Il run attuale
> **non potra'** darlo, nemmeno a posteriori. **Serve una decisione di Luca**, e le strade sono due:
> *(a)* registrare nel simulatore **e** salvare `conc_nodi`, **e rifare il run**; *(b)* tenere il
> run com'e' e rimandare `MASSA-ID` al prossimo.

**CHE COSA QUESTO FILE CONSEGNA LO STESSO, ed e' la novita' metodologica della voce:**
il **MEDOIDE PESATO** *(«dove sono piu' densi»)* col suo **collaudo su caso NOTO**, pronto a
ricevere i pesi `cos(phi - phi_massa)` appena il lignaggio esistera'.
**E quando il lignaggio manca, lo strumento SI FERMA con la ragione esatta** invece di ricadere in
silenzio sulle coorti del passo 0 — che sono **l'insieme congelato** che `MASSA-ID` esiste per
superare.

    python csv/_test_fork/_massa_id.py --collaudo      # il medoide pesato, su caso NOTO
    python csv/_test_fork/_massa_id.py --stato <f.npz> # si ferma, e dice quale dei due blocchi

ASCII puro.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))

import _presidio                                                       # noqa: E402
import _osservabile_p1 as OP                                           # noqa: E402

_presidio.avvia(__file__)

# ESENTE-H-P5: non costruisce nessuna scena e non carica il simulatore. Il `--collaudo` gira su un
#   grafo SINTETICO a risposta nota; su uno stato vero legge un `.npz` e, oggi, SI FERMA.

NL = chr(10)


# ============================================================================ IL MEDOIDE PESATO
def medoide_pesato(g, idx, pesi):
    """**IL CENTRO di `MASSA-ID`: `argmin_k sum_m w_m * d(k, m)`**, sul **sottografo indotto**.

    **I PESI NEGATIVI SI TAGLIANO A ZERO, E LA SCELTA E' DICHIARATA** *(task history par.2.3)*:
    `w = cos(phi - phi_massa)` sta in `[-1, +1]`, e il codice del simulatore dice che **`-1` e'
    antifase, «proietta CONTRO»** — quindi quel nodo **non fa parte di «dove la massa e' densa»**.
    **Non e' una toppa (`A11`): e' il significato.**

    **`Y5`: i negativi si CONTANO.** Se fossero la maggioranza, questa lettura andrebbe rifatta.

    **Se la somma dei pesi e' ZERO il medoide pesato NON E' DEFINITO:** si **ricade su quello NON
    pesato** e **si CONTA** (`A8`), invece di dividere per zero o di scegliere in silenzio.

    Restituisce `(nodo, diagnostica)`.
    """
    idx = np.asarray(sorted(set(int(x) for x in idx)), int)
    w = np.asarray(pesi, float)
    if len(w) != len(idx):
        raise SystemExit("[massa-id] pesi e indici di lunghezza diversa (%d contro %d): mi fermo."
                         % (len(w), len(idx)))
    dia = {"n": int(len(idx)), "negativi": int(np.sum(w < 0.0)),
           "frazione_negativi": float(np.mean(w < 0.0)) if len(w) else float("nan"),
           "ripiego_non_pesato": 0}
    if len(idx) == 0:
        return -1, dia
    wc = np.maximum(w, 0.0)                       # il taglio DICHIARATO
    if len(idx) == 1:
        return int(idx[0]), dia
    sub = g[idx, :][:, idx]
    d = OP.distanze(sub, np.arange(len(idx)))
    fin = np.isfinite(d)
    if wc.sum() <= 0.0:
        dia["ripiego_non_pesato"] = 1
        somma = np.where(fin, d, 0.0).sum(axis=1)
    else:
        somma = np.where(fin, d, 0.0) @ wc
    somma[fin.sum(axis=1) < fin.sum(axis=1).max()] = np.inf   # chi raggiunge meno nodi perde
    k = int(np.argmin(somma))                     # PAREGGI: l'indice MINORE, come `OP.medoide`
    dia["pari"] = int(np.sum(somma == somma[k]))
    return int(idx[k]), dia


# ============================================================================ IL LIGNAGGIO
def lignaggio_da_stato(percorso):
    """**Oggi SI FERMA, e dice QUALE dei due blocchi** — non ricade sulle coorti del passo 0."""
    z = np.load(percorso, allow_pickle=False)
    if "conc_nodi" in z.files:
        return z["conc_nodi"]
    raise SystemExit(
        "[massa-id] MI FERMO: lo stato %s NON porta il lignaggio." % os.path.basename(percorso)
        + NL + "  campi presenti: %s" % ", ".join(z.files)
        + NL + "  E ci sono DUE blocchi, indipendenti:"
        + NL + "   (1) la scena NON registra le regioni nel tracking (soliton_simulator.py:7398,"
        + NL + "       <<`conc_nodi` NON viene toccato, di proposito>>): serve modificare IL"
        + NL + "       SIMULATORE, e il mandato dice di FERMARSI e dirlo."
        + NL + "   (2) il salvataggio degli stati non include `conc_nodi`: servirebbe modificare"
        + NL + "       _pilota_prova1_braccio.py, che e' nel percorso del RUN IN CORSO (par.5)."
        + NL + "  NON ricado sulle coorti del passo 0: sono l'insieme CONGELATO che `MASSA-ID`"
        + NL + "  esiste per superare, e usarle in silenzio darebbe un numero che sembra nuovo"
        + NL + "  ed e' quello vecchio.")


# ============================================================================ IL COLLAUDO
def collaudo():
    """**Caso NOTO: un CAMMINO di 21 nodi**, e il peso decide dove sta il centro.

    | caso | risposta NOTA | e come puo' FALLIRE |
    |---|---|---|
    | pesi UNIFORMI | **lo stesso medoide di `OP.medoide`** | se differisse, il pesato non ridurrebbe al non pesato |
    | peso tutto a SINISTRA | **il medoide si sposta a sinistra** | se NON si spostasse, **i pesi non sono usati** |
    | pesi con META' NEGATIVI | **come se quella meta' non ci fosse** | se cambiasse, il taglio a zero non e' applicato |
    | somma dei pesi ZERO | **ripiego NON pesato, CONTATO** | se non ripiegasse, dividerebbe per zero in silenzio |

    **La riga che conta e' la SECONDA**: e' quella che **fallisce** se i pesi vengono ignorati —
    ed e' proprio l'errore che `T4` non sapeva prendere.
    """
    P = print
    n = 21
    i = np.arange(n - 1)
    j = np.arange(1, n)
    g, _u, _s = OP.grafo(i, j, np.ones(n - 1), n)
    idx = np.arange(n)
    ok, tot = 0, 0

    def esito(nome, buono, testo):
        nonlocal ok, tot
        tot += 1
        ok += 1 if buono else 0
        P("  %-44s %s" % (nome, "PASS" if buono else "** FAIL **"))
        P("      %s" % testo)

    P("=" * 104)
    P("`Y`-MEDOIDE PESATO -- il collaudo su CASO NOTO (cammino di %d nodi)" % n)
    P("=" * 104)
    base, _p, _r = OP.medoide(g, idx)
    m_u, d_u = medoide_pesato(g, idx, np.ones(n))
    esito("uniformi -> lo stesso di `OP.medoide`", m_u == base,
          "medoide non pesato %d   pesato con pesi uniformi %d" % (base, m_u))

    w = np.zeros(n)
    w[:5] = 1.0                                   # tutto il peso sui primi cinque nodi
    m_s, d_s = medoide_pesato(g, idx, w)
    esito("peso a SINISTRA -> il centro si SPOSTA", m_s < base,
          "medoide %d -> %d   (se i pesi fossero IGNORATI resterebbe %d: e' la riga che"
          " fallisce)" % (base, m_s, base))

    w2 = np.ones(n)
    w2[10:] = -1.0                                # meta' negativi
    m_n, d_n = medoide_pesato(g, idx, w2)
    w3 = np.zeros(n)
    w3[:10] = 1.0
    m_t, _d = medoide_pesato(g, idx, w3)
    esito("negativi TAGLIATI a zero, e CONTATI", m_n == m_t and d_n["negativi"] == 11,
          "col taglio %d, con quei nodi assenti %d   negativi contati %d (%.1f %%)"
          % (m_n, m_t, d_n["negativi"], 100 * d_n["frazione_negativi"]))

    m_z, d_z = medoide_pesato(g, idx, np.full(n, -1.0))
    esito("somma ZERO -> ripiego NON pesato, CONTATO",
          d_z["ripiego_non_pesato"] == 1 and m_z == base,
          "ripiego %d volta, medoide %d = quello non pesato %d"
          % (d_z["ripiego_non_pesato"], m_z, base))
    P()
    P("  %d/%d" % (ok, tot))
    P()
    P("  ⚠ E QUESTO NON E' `MASSA-ID`: e' il suo CENTRO. `Y1`/`Y2` richiedono di registrare le")
    P("  regioni nel simulatore, e il mandato dice di FERMARSI e dirlo. Vedi il docstring.")
    return ok, tot


if __name__ == "__main__":
    A = sys.argv[1:]
    if "--collaudo" in A:
        k, t = collaudo()
        raise SystemExit(0 if k == t else 1)
    if "--stato" in A:
        lignaggio_da_stato(A[A.index("--stato") + 1])
    print(__doc__)
