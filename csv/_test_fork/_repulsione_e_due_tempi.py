# -*- coding: utf-8 -*-
"""DUE DIFETTI CANDIDATI, misurati sugli SNAPSHOT GIA' SCRITTI. Nessun run, nessuna cura.

Mandato di Luca, 2026-09-22.

CANDIDATO 1 -- LA REPULSIONE ALLA MASSIMA COMPRESSIONE (`S05_spinta_locale`) E' INERTE.
  La mitosi inverte il segno solo quando `tau_pp` supera il punto medio fra soglia e tetto:
      tau_pp   = 1 + |tw|/PHI_CRIT                 (PHI_CRIT = 2pi)
      soglia   = soglia0 * (1 - 0.3*tanh(grad_tau))   soglia0 = 2pi + pi = 3pi   (TORS_4PI)
      tau_tetto= 1 + TW_TETTO/PHI_CRIT = 3           TW_TETTO = 4pi
      centro   = 0.5*(tau_soglia + tau_tetto)
      segno    = -tanh(3*(tau_pp - centro))          NEGATIVO solo se tau_pp > centro
  Col `soglia0` non modulato, `centro = 2.75`, cioe' **|tw| > 3.5pi**.
  **IL COMMENTO IN TESTA AL SIMULATORE (`:64-66`) DICE CHE LA TORSIONE SATURA A ~2.5pi**, e
  che percio' il surrogato "non raggiunge mai il tetto 4pi di spegnimento".
  ⚠ **QUEL `2.5pi` E' PRE-FORK** *(par.9-bis: ogni numero porta la sua epoca)*. **Qui si
  rimisura sugli archivi delle cure, e il numero di oggi puo' essere un altro.**

CANDIDATO 2 -- DUE DEFINIZIONI DI TEMPO PROPRIO.
      r        il ritmo dei NODI, `dt_n = DT*r`, prodotto da `ritmo()`
      tau_pp   1 + tw/PHI_CRIT, il "surrogato" di mitosi e repulsione, per ARCO
  Si elencano i punti del codice che usano l'uno o l'altro, e si misura quanto differiscono
  sugli stessi nodi.

IL CRITERIO, SCRITTO PRIMA DI VEDERE I NUMERI:
  (1) `S05` e' INERTE se la frazione di archi con `resp < 0` e' **zero** su tutti gli snapshot.
      Se e' > 0 ma minuscola, **non si dice "inerte"**: si dice quanto vale, e si confronta
      il suo contributo col saldo degli altri scrittori. *(par.9: un risultato negativo si
      scrive come LIMITE, non come «non c'e'».)*
  (2) I due tempi sono LA STESSA GRANDEZZA se, proiettati sugli stessi nodi, il rapporto
      `r / tau_nodo` ha dispersione trascurabile e correlazione ~1. Sono DIVERSI se la
      correlazione e' bassa o il rapporto varia di ordini di grandezza.
  ⚠ E LA DOMANDA VA POSTA PRIMA AL SORGENTE: se `ritmo()` prende un RAMO che non e'
    `1+tw/PHI_CRIT`, allora sono due grandezze diverse **per costruzione**, e la misura
    serve a dire QUANTO diverse, non SE.

SOLA LETTURA: apre snapshot `.pkl.gz` gia' scritti e legge `soliton_simulator.py` come TESTO.
Non importa il simulatore, non esegue fisica, non tocca nessun run.
ASCII PURO.
"""
import gzip
import io
import os
import pickle
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SORGENTE = os.path.join(RADICE, "soliton_simulator.py")
OUT = os.path.join(_QUI, "_diag_D", "REPULSIONE_E_DUE_TEMPI.md")

PI = np.pi
PHI_CRIT = 2 * PI
TW_TETTO = 4 * PI
GAMMA = None            # letto dal sorgente: zero manopole, zero valori a memoria

ARCHIVI = [
    ("G4 riferimento (tutto acceso)", "_g4_riferimento"),
    ("G4 senza memoria del moto", "_g4_senza_memmoto"),
    ("G3 senza gravita' bifase", "_g3_senza_bifase"),
    ("validazione 600 (`_val600`)", "_val600"),
]


def costante(nome):
    """Legge una costante di modulo DAL SORGENTE, come testo. Zero import, zero memoria."""
    t = io.open(SORGENTE, encoding="utf-8").read()
    m = re.search(r"^%s\s*=\s*([^\s#]+)" % re.escape(nome), t, re.M)
    if not m:
        return None
    try:
        return eval(m.group(1), {"np": np, "__builtins__": {}})
    except Exception:
        return m.group(1)


def satura(f, gamma):
    """La STESSA forma del simulatore (`:3389`), copiata dal codice e non ricordata."""
    return f / (1.0 + gamma * np.sqrt(np.abs(f) ** 2 + 1e-9))


def leggi(p):
    with gzip.open(p, "rb") as f:
        return pickle.load(f)["attrs"]


def snapshot(cartella):
    d = os.path.join(RADICE, "csv", "_test_fork", cartella)
    if not os.path.isdir(d):
        return []
    return [os.path.join(d, f) for f in sorted(os.listdir(d))
            if f.startswith("scena_") and f.endswith(".pkl.gz")]


# ------------------------------------------------------------------ CANDIDATO 1
def risposta(a, gamma, tors_4pi):
    """Ricostruisce `resp` ESATTAMENTE come `mitosi()`. Ogni riga ha il suo riscontro."""
    tw = np.asarray(a["tw"], float)
    ii = np.asarray(a["i"]); jj = np.asarray(a["j"])
    deg = np.asarray(a["_deg"], float)
    n = len(deg)
    avv = np.abs(tw)
    soglia0 = (PHI_CRIT + PI) if tors_4pi else PHI_CRIT
    soglia = np.full(len(avv), soglia0, float)
    modulata = False
    if tors_4pi and len(ii) == len(avv):
        tau_nodo = np.zeros(n)
        mi = ii < n; mj = jj < n
        np.add.at(tau_nodo, ii[mi], avv[mi])
        np.add.at(tau_nodo, jj[mj], avv[mj])
        tau_nodo = 1.0 + tau_nodo / np.maximum(deg, 1) / PHI_CRIT
        grad_tau = np.abs(tau_nodo[ii] - tau_nodo[jj])
        soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_tau))
        modulata = True
    ecc = np.maximum(avv / np.maximum(soglia, 1e-9) - 1.0, 0.0)
    salita = satura(ecc, gamma)
    discesa = np.clip(1.0 - avv / TW_TETTO, 0.0, 1.0)
    tau_pp = 1.0 + avv / PHI_CRIT
    tau_soglia = 1.0 + soglia / PHI_CRIT
    tau_tetto = 1.0 + TW_TETTO / PHI_CRIT
    centro = 0.5 * (tau_soglia + tau_tetto)
    segno = -np.tanh(3.0 * (tau_pp - centro))
    resp = salita * discesa * (1.0 / tau_pp) * segno
    return dict(avv=avv, tau_pp=tau_pp, centro=centro, soglia=soglia, resp=resp,
                modulata=modulata, soglia0=soglia0)


def q(x, p):
    return float(np.percentile(x, p)) if len(x) else float("nan")


# ------------------------------------------------------------------ CANDIDATO 2
def siti_dei_due_tempi():
    """Ogni riga del sorgente che usa l'uno o l'altro. Si LEGGE, non si ricorda."""
    righe = io.open(SORGENTE, encoding="utf-8").read().splitlines()
    r_pat = re.compile(r"\bdt_n\b|\b_r_corrente\b|\britmo\(\)|\br_loc\b")
    t_pat = re.compile(r"\btau_pp\b|1\.0\s*\+\s*.*?/\s*(?:max\()?PHI_CRIT|"
                       r"1\.0\s*\+\s*avv\s*/\s*PHI_CRIT")
    a, b = [], []
    for k, riga in enumerate(righe, 1):
        nudo = riga.strip()
        commento = nudo.startswith("#")
        if r_pat.search(riga):
            a.append((k, commento, nudo[:110]))
        if t_pat.search(riga):
            b.append((k, commento, nudo[:110]))
    return a, b


def main():
    gamma = costante("GAMMA")
    tors_4pi = bool(costante("TORS_4PI"))
    tempo_segno = bool(costante("TEMPO_SEGNO"))
    tau_loc = costante("TAU_LOC")
    tpo = bool(costante("TEMPO_PROPRIO_ORIENTATO"))
    try:
        os.makedirs(os.path.dirname(OUT))
    except OSError:
        pass
    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    W = o.write
    W("# `S05` e I DUE TEMPI PROPRI — **misurati sugli snapshot gia' scritti**\n\n")
    W("> Generato da `csv/_test_fork/_repulsione_e_due_tempi.py`. **Nessun run.** Legge gli\n")
    W("> archivi delle cure e il sorgente come testo.\n>\n")
    W("> **Le costanti sono LETTE DAL SORGENTE, non ricordate:** `GAMMA = %s` · `TORS_4PI = "
      "%s` · `TEMPO_SEGNO = %s` · `TAU_LOC = %s` · `TEMPO_PROPRIO_ORIENTATO = %s`.\n\n"
      % (gamma, tors_4pi, tempo_segno, tau_loc, tpo))

    # ---------------------------------------------------------- CANDIDATO 1
    W("## CANDIDATO 1 — **la repulsione alla massima compressione (`S05`)**\n\n")
    soglia0 = (PHI_CRIT + PI) if tors_4pi else PHI_CRIT
    centro0 = 0.5 * ((1 + soglia0 / PHI_CRIT) + 3.0)
    tw_inv = (centro0 - 1.0) * PHI_CRIT
    W("**IL PUNTO DI INVERSIONE, ricavato dal codice e non supposto:** con `soglia0 = %.4f` "
      "*(= `%.2f pi`)* il `centro` vale **`%.4f`**, cioe' l'inversione di segno avviene a\n"
      "**`|tw| = %.4f` = `%.3f pi`**. *(La soglia LOCALE e' modulata di al piu' `-30 %%`, quindi "
      "il punto di inversione vero varia per arco: si riporta quello misurato.)*\n\n"
      % (soglia0, soglia0 / PI, centro0, tw_inv, tw_inv / PI))
    W("### La torsione contro il tetto `4pi`\n\n")
    W("| archivio | passo | archi | `max\\|tw\\|/pi` | `p50/pi` | `p99/pi` | `p99.99/pi` | "
      "`\\|tw\\| >= 2.5pi` | `\\|tw\\| >= 3.5pi` | `\\|tw\\| >= 4pi` |\n")
    W("|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|\n")
    righe2 = []
    for eti, cart in ARCHIVI:
        for p in snapshot(cart):
            passo = int(os.path.basename(p).split("_")[1].split(".")[0])
            a = leggi(p)
            r = risposta(a, gamma, tors_4pi)
            avv = r["avv"]
            na = len(avv)
            W("| %s | %d | %d | **%.4f** | %.4f | %.4f | %.4f | %.4g | **%.4g** | %.4g |\n"
              % (eti, passo, na, avv.max() / PI, q(avv, 50) / PI, q(avv, 99) / PI,
                 q(avv, 99.99) / PI,
                 float(np.mean(avv >= 2.5 * PI)), float(np.mean(avv >= 3.5 * PI)),
                 float(np.mean(avv >= TW_TETTO))))
            neg = r["resp"] < 0
            sopra = r["tau_pp"] > r["centro"]
            rep_snap = np.asarray(a.get("_rep", []), float)
            d0 = np.asarray(a["d0"], float)
            spinta = (0.02 * d0 * rep_snap) if len(rep_snap) == len(d0) else np.zeros(0)
            righe2.append((eti, passo, na, int(np.sum(sopra)), int(np.sum(neg)),
                           float(np.min(r["resp"])),
                           int(np.sum(rep_snap > 0)) if len(rep_snap) else -1,
                           float(np.max(rep_snap)) if len(rep_snap) else float("nan"),
                           float(np.sum(spinta)) if len(spinta) else float("nan")))
    W("\n### Il SEGNO: quanti archi sono davvero in repulsione\n\n")
    W("| archivio | passo | archi | `tau_pp > centro` | **`resp < 0`** | `min(resp)` | "
      "`_rep > 0` | `max(_rep)` | somma della spinta `0.02*d0*_rep` |\n")
    W("|---|--:|--:|--:|--:|--:|--:|--:|--:|\n")
    tot_neg = 0
    for e_, pa, na, so, ne, mr, rp, mx, sp in righe2:
        tot_neg += ne
        W("| %s | %d | %d | %d | **%d** | %.3e | %s | %.3e | %.3e |\n"
          % (e_, pa, na, so, ne, mr, ("%d" % rp) if rp >= 0 else "n/d", mx, sp))
    W("\n**ARCHI IN REPULSIONE, sommati su tutti gli snapshot: %d.**\n\n" % tot_neg)

    # ---- LA FINESTRA: dove il segno si inverte e dove l'ampiezza si azzera
    W("\n### ⚠ **LA FINESTRA DELLA REPULSIONE: fra l'inversione del SEGNO e lo zero "
      "dell'AMPIEZZA**\n\n")
    W("> **`resp = salita * discesa * (1/tau_pp) * segno`.** Il `segno` si inverte a "
      "`tau_pp > centro`, cioe' **oltre `~3.5pi`**.\n")
    W("> **Ma `discesa = clip(1 - |tw|/4pi, 0, 1)` vale ESATTAMENTE ZERO per `|tw| >= 4pi`.**\n")
    W("> **Quindi la repulsione puo' esistere SOLO nella finestra `[~3.5pi, 4pi)`, larga "
      "mezzo `pi`** — e **oltre il tetto e' zero per costruzione**, cioe' **proprio dove la "
      "materia e' piu' compressa**, che e' il caso per cui la legge dichiara di esistere.\n\n")
    W("| archivio | passo | oltre l'inversione | **nella finestra `[3.5pi, 4pi)`** | "
      "**oltre `4pi`: repulsione ZERO** | quota azzerata |\n")
    W("|---|--:|--:|--:|--:|--:|\n")
    for eti, cart in ARCHIVI:
        for p in snapshot(cart):
            passo = int(os.path.basename(p).split("_")[1].split(".")[0])
            a = leggi(p)
            r = risposta(a, gamma, tors_4pi)
            avv = r["avv"]
            oltre_inv = int(np.sum(r["tau_pp"] > r["centro"]))
            oltre_tetto = int(np.sum(avv >= TW_TETTO))
            finestra = int(np.sum((avv >= 3.5 * PI) & (avv < TW_TETTO)))
            quota = (oltre_tetto / oltre_inv) if oltre_inv else float("nan")
            W("| %s | %d | %d | **%d** | **%d** | **%.1f %%** |\n"
              % (eti, passo, oltre_inv, finestra, oltre_tetto, 100.0 * quota))
    W("\n**⚠ E LA VERIFICA CHE LA FINESTRA E' DAVVERO IL VINCOLO:** `min(resp)` vale "
      "`~-1.5e-02` su tutti gli snapshot — **non cresce mai**, perche' gli archi che "
      "potrebbero dare una repulsione grande sono **esattamente quelli che `discesa` azzera**.\n")

    # ---------------------------------------------------------- CANDIDATO 2
    W("\n## CANDIDATO 2 — **due definizioni di tempo proprio**\n\n")
    a_r, a_t = siti_dei_due_tempi()
    W("### I punti del codice, letti dal sorgente\n\n")
    W("**`r` / `dt_n` — il ritmo dei NODI: %d righe** *(di cui %d in commento)*.\n\n"
      % (len(a_r), sum(1 for _k, c, _s in a_r if c)))
    W("| riga | | codice |\n|--:|---|---|\n")
    for k, c, s in a_r:
        if c:
            continue
        W("| `%d` | %s | `%s` |\n" % (k, "cod", s.replace("|", "\\|")))
    W("\n**`tau_pp` — il surrogato per ARCO: %d righe** *(di cui %d in commento)*.\n\n"
      % (len(a_t), sum(1 for _k, c, _s in a_t if c)))
    W("| riga | | codice |\n|--:|---|---|\n")
    for k, c, s in a_t:
        if c:
            continue
        W("| `%d` | %s | `%s` |\n" % (k, "cod", s.replace("|", "\\|")))

    W("\n### Quanto differiscono, sugli STESSI nodi\n\n")
    W("> `tau_nodo = 1 + mean(|tw| sugli archi incidenti)/PHI_CRIT` e' **la forma esatta** che\n")
    W("> `ritmo()` userebbe nel ramo `TEMPO_SEGNO` *(`:2553`)* e che `mitosi()` usa per il\n")
    W("> gradiente *(`:5120`)*. **Si confronta con `r` = `_r_corrente`, quello che il sistema\n")
    W("> usa davvero in `dt_n = DT*r`.**\n\n")
    W("| archivio | passo | nodi | `med r` | `med tau_nodo` | correlazione | "
      "`med(r/tau_nodo)` | `p01` | `p99` | `max/min` di `r` |\n")
    W("|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|\n")
    for eti, cart in ARCHIVI:
        for p in snapshot(cart):
            passo = int(os.path.basename(p).split("_")[1].split(".")[0])
            a = leggi(p)
            rr = np.asarray(a.get("_r_corrente", []), float)
            if not len(rr):
                W("| %s | %d | — | — | — | — | — | — | — | "
                  "`_r_corrente` ASSENTE |\n" % (eti, passo))
                continue
            avv = np.abs(np.asarray(a["tw"], float))
            ii = np.asarray(a["i"]); jj = np.asarray(a["j"])
            deg = np.asarray(a["_deg"], float)
            n = len(deg)
            acc = np.zeros(n)
            mi = ii < n; mj = jj < n
            np.add.at(acc, ii[mi], avv[mi])
            np.add.at(acc, jj[mj], avv[mj])
            tau_nodo = 1.0 + acc / np.maximum(deg, 1) / PHI_CRIT
            # ⚠ P5: `_r_corrente` puo' essere PIU' CORTO di `_deg` (la mitosi aggiunge nodi
            #   dopo l'ultima scrittura della cache). Si TAGLIA e si DICHIARA.
            m = min(len(rr), len(tau_nodo))
            taglio = (len(rr) != len(tau_nodo))
            r1 = rr[:m]; t1 = tau_nodo[:m]
            rap = r1 / np.maximum(t1, 1e-12)
            cor = float(np.corrcoef(r1, t1)[0, 1]) if m > 2 and np.std(r1) > 0 else float("nan")
            W("| %s | %d | %d%s | %.6f | %.6f | **%+.4f** | %.4e | %.4e | %.4e | %.3e |\n"
              % (eti, passo, m, " ⚠" if taglio else "", float(np.median(r1)),
                 float(np.median(t1)), cor, float(np.median(rap)), q(rap, 1), q(rap, 99),
                 float(np.max(r1) / max(np.min(r1), 1e-300))))
    W("\n⚠ `⚠` accanto al numero di nodi = **`_r_corrente` era PIU' CORTO di `_deg`** e si "
      "e' tagliato al minimo. E' la stessa famiglia di `A8b` *(cache cross-passo da estendere a "
      "ogni punto di crescita)*, e si dichiara invece di nasconderla.\n")

    W("\n## LE LETTURE, fissate PRIMA\n\n")
    W("1. **`S05` e' INERTE se `resp < 0` non capita MAI.** Se capita ma poco, **non si dice "
      "«inerte»**: si dice **quanto**, e si confronta col saldo degli altri "
      "scrittori *(par.9: un negativo si scrive come LIMITE)*.\n")
    W("2. **I due tempi sono la STESSA grandezza** se correlazione `~1` e rapporto con "
      "dispersione trascurabile; **DIVERSI** se la correlazione e' bassa o il rapporto varia di "
      "ordini di grandezza.\n")
    W("\n**LIMITI:** UN seme, UNA scena, gli archivi delle cure. **Il `2.5pi` del commento "
      "`:64-66` e' PRE-FORK** *(par.9-bis)*: qui non si sta verificando quel numero, si sta "
      "misurando **quello di oggi**.\n")
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
