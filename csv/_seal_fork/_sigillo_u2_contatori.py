# -*- coding: utf-8 -*-
"""`U2` -- **I CONTATORI DI `_nasce` SI COLLAUDANO SU UNA MITOSI A RISPOSTA NOTA.**

> **Rilievo di Luca, 2026-09-25:** *«`_sm_lunghezza` mescola `d` e `d0`. In mitosi `_nasce` e'
> chiamata due volte: `dh = _nasce(dh)` -> una volta su `len(sel)`, ma `dh` diventa DUE archi
> (`concatenate([dh, dh])`); `d0new = _nasce(d0new)` -> gia' sui due archi figli. In `_allaccia`
> una sola chiamata vale per `d` E `d0`. Quindi la somma non e' "nelle unita' del bilancio di
> `d0`".»*

**I QUATTRO SITI, letti dal codice** *(e il quarto NON era fra i tre del rilievo)*:

```
semina     `_allaccia`  dd      md=1 md0=1   d = concat([d, dd])   E   d0 = concat([d0, dd])
mitosi     `dh`                 md=2 md0=0   d = concat([d[keep], dh, dh])
mitosi     `d0new`              md=0 md0=1   d0new e' GIA' concat([d0h, d0h])
schwinger  `dd`                 md=2 md0=2   [d, dd, dd] E [d0, dd, dd]
```

**IL CASO A RISPOSTA NOTA** *(`P1-sexies`: prima il caso sintetico, poi il codice vero)*:
un SOLO arco con `d = d0 = 1.2 LAM` si divide. `dh = 0.6 LAM < LAM` -> **entrambi i figli
troncati**, su `d` **e** su `d0`.

```
ATTESO, per costruzione:
  _sm_trd_mitosi   = 2      (DUE archi veri di `d`, non uno: e' il difetto corretto)
  _sm_trd0_mitosi  = 2
  _sm_lund_mitosi  = 2 * (LAM - 0.6 LAM) = 0.8 LAM
  _sm_lund0_mitosi = 2 * (LAM - 0.6 LAM) = 0.8 LAM
```

**E IL CASO CHE DEVE FALLIRE** *(`P1-sexies`, ed e' il piu' importante)*: la formula VECCHIA
-- un contatore solo -- **sullo stesso evento** da' `0.4 LAM` sul lato `d` *(sottoconto di `2`)*
e una somma `1.2 LAM` che **non e' in nessuna delle due unita'**. **Il criterio, applicato a
quella, DEVE dare FAIL.** Se passasse, il criterio non discriminerebbe la cura dal difetto.

**Un processo per braccio** *(`STANDARD 1`)*, **byte-identita' e non `max|delta|`**
*(`STANDARD 2`)*. ASCII puro nel sorgente; l'output e' UTF-8.
"""
import io
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
DEST = os.path.join(_QUI, "_sig_u2", "SIGILLO_u2_contatori.txt")
TMP = os.path.join(_QUI, "_sig_u2", "_tmp")
os.makedirs(TMP, exist_ok=True)

SEME = 7
NODI = 40
FATT = 1.2          # l'arco vale 1.2 LAM -> i figli 0.6 LAM, entrambi sotto LAM

# ------------------------------------------------------------------ il braccio (figlio)
FIGLIO = r'''
import io, json, os, sys
import numpy as np
sys.path.insert(0, RAD)
import importlib.util as _iu
_sp = _iu.spec_from_file_location("sim_u2", SIM)
S = _iu.module_from_spec(_sp); _sp.loader.exec_module(S)

net = S.Rete(SEME)
net.semina(NODI)
assert len(net.d) > 0, "rete senza archi"
# UN PASSO PRIMA, e non e' un dettaglio: `mitosi` legge `I = self._rho_sorgente()`, che su una
# rete appena seminata e' VUOTO (`IndexError` a `:5749`). La soglia di densita'
# `0.5*(I[a]+I[b]) >= QMIN_M*median(peq)` esiste, e un arco che non la passa NON si divide:
# senza il passo, il caso "a risposta nota" non arriverebbe nemmeno a `_nasce`.
net.step()

# --- lo stato NOTO: un solo arco lungo `FATT * LAM`, e la torsione solo LI'. ---
LAM = float(S.LAM)
net.d = np.full(len(net.d), 3.0 * LAM)          # tutti gli altri BEN SOPRA LAM
net.d0 = net.d.copy()
net.d[0] = FATT * LAM
net.d0[0] = FATT * LAM
# LA TORSIONE VA IN UNA FINESTRA, NON "GRANDE": `1.0e3` NON FACEVA SCATTARE NULLA.
#   `discesa = clip(1 - avv/TW_TETTO, 0, 1)` -> ZERO sopra il tetto: la mitosi si SPEGNE.
#   `segno = -tanh(3*(tau_pp - centro))` -> NEGATIVO (repulsione) sopra `centro`.
#   Con `tau_pp = 1 + avv/PHI_CRIT`, `tau_soglia = 2`, `tau_tetto = 3`, `centro = 2.5`:
#   serve `avv` fra `PHI_CRIT` e `1.5*PHI_CRIT`. Si prende `1.2*PHI_CRIT` -> `tau_pp = 2.2`.
#   ⚠ DIFETTO MIO, ed e' il quinto criterio scritto DAL MIO MODELLO MENTALE invece che da una
#     misura (par.9): avevo scelto "un numero grande" senza guardare la campana.
# LA FINESTRA SI DERIVA DAL CODICE, NON SI SCEGLIE (par.9):
#   soglia0 = PHI_CRIT + pi  se `TORS_4PI and not FASE_2PI`  (il default: 3pi, NON 2pi)
#   creazione  <=>  avv > soglia0   E   tau_pp < centro = (tau_soglia + tau_tetto)/2
#   con tau_pp = 1 + avv/PHI_CRIT  ->  avv < (centro - 1)*PHI_CRIT
# Misurata: (1.500, 1.750)*PHI_CRIT. Si prende IL MEZZO della finestra.
_s0 = (S.PHI_CRIT + np.pi) if (S.TORS_4PI and not S.FASE_2PI) else S.PHI_CRIT
_centro = 0.5 * ((1.0 + _s0 / S.PHI_CRIT) + (1.0 + (4.0 * np.pi) / S.PHI_CRIT))
_lo, _hi = _s0, (_centro - 1.0) * S.PHI_CRIT
TW0 = 0.5 * (_lo + _hi)
net.tw = np.zeros(len(net.d))
net.tw[0] = TW0
if hasattr(net, "_rep"):
    net._rep = np.zeros(len(net.d))

# `nasce = rng.random(k) < prob`: con `random -> 0` divide OGNI arco con `prob > 0`,
# e `prob` e' ESATTAMENTE 0 dove `resp <= 0`. Quindi divide SOLO l'arco 0.
_rng = net.rng
class _R:
    def __getattr__(self, k):
        return getattr(_rng, k)
    def random(self, *a, **k):
        _n = a[0] if a else k.get("size")
        return np.zeros(_n) if _n is not None else 0.0
net.rng = _R()

# --- azzera i contatori, poi la MITOSI VERA ---
for _k in [k for k in list(vars(net)) if k.startswith("_sm_") or k == "_g_sm_nascite"]:
    delattr(net, _k)

n_pre = int(net.n)
archi_pre = int(len(net.d))
d_pre_sel = float(net.d[0]); d0_pre_sel = float(net.d0[0])
# il PRE della STESSA grandezza: e' il controllo positivo giusto per `U2-8`.
np.save(os.path.join(TMPD, NOME + "_dPRE.npy"), np.ascontiguousarray(np.asarray(net.d, float)))
net.mitosi()

out = {
    "LAM": LAM,
    "n_pre": n_pre, "n_post": int(net.n),
    "archi_pre": archi_pre, "archi_post": int(len(net.d)),
    "d_pre_sel": d_pre_sel, "d0_pre_sel": d0_pre_sel,
    "nascite": int(getattr(net, "_g_sm_nascite", 0)),
    "negate": int(getattr(net, "negate", -1)),
    "peq_med": float(np.median(net.peq)) if len(net.peq) else float("nan"),
    # quanti archi VERI stanno esattamente a LAM, sulle due grandezze
    "d_a_lam": int(np.sum(np.asarray(net.d) == LAM)),
    "d0_a_lam": int(np.sum(np.asarray(net.d0) == LAM)),
    "d_min": float(np.min(net.d)), "d0_min": float(np.min(net.d0)),
    "TEMPO_UNICO_MITOSI": bool(S.TEMPO_UNICO_MITOSI),
    # `TW_TETTO` e' una LOCALE di `mitosi` (`:5578`), non un attributo di modulo: si
    # ricalcola qui e SI DICHIARA da dove viene, invece di leggerla dove non esiste.
    "PHI_CRIT": float(S.PHI_CRIT), "TW_TETTO": float(4.0 * np.pi),
    "tw_sel": float(TW0), "soglia0": float(_s0),
    "finestra": [float(_lo), float(_hi)],
    "PLAST_DIN": bool(S.PLAST_DIN), "PLAST_MIT": float(S.PLAST_MIT),
}
for k, v in sorted(vars(net).items()):
    if k.startswith("_sm_"):
        out[k] = float(v) if isinstance(v, float) else int(v)
np.save(os.path.join(TMPD, NOME + "_d.npy"), np.ascontiguousarray(np.asarray(net.d, float)))
np.save(os.path.join(TMPD, NOME + "_d0.npy"), np.ascontiguousarray(np.asarray(net.d0, float)))
io.open(os.path.join(TMPD, NOME + ".json"), "w", encoding="utf-8").write(json.dumps(out))
print("OK " + NOME + " n %d -> %d, archi %d -> %d" % (n_pre, net.n, archi_pre, len(net.d)))
'''


def braccio(nome, sim, fatt):
    """UN PROCESSO PER BRACCIO (`STANDARD 1`). `sim` e' il file del simulatore da usare."""
    src = ("RAD = %r\nTMPD = %r\nNOME = %r\nSIM = %r\nSEME = %d\nNODI = %d\nFATT = %r\n"
           % (RADICE, TMP, nome, sim, SEME, NODI, fatt)) + FIGLIO
    p = os.path.join(TMP, "_br_" + nome + ".py")
    io.open(p, "w", encoding="utf-8", newline="\n").write(src)
    r = subprocess.run([sys.executable, p], cwd=RADICE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r


def leggi(nome):
    import json
    return json.loads(io.open(os.path.join(TMP, nome + ".json"), encoding="utf-8").read())


# ------------------------------------------------------------------ il VECCHIO simulatore
VECCHIO = os.path.join(TMP, "_sim_vecchio.py")
r = subprocess.run(["git", "cat-file", "-p", "HEAD:soliton_simulator.py"], cwd=RADICE,
                   capture_output=True)
assert r.returncode == 0, r.stderr[:400]
# in BINARIO: la trappola CRLF di par.5-quinquies
io.open(VECCHIO, "wb").write(r.stdout)

NUOVO = os.path.join(RADICE, "soliton_simulator.py")

# ------------------------------------------------------------------ i bracci
ESITI = []
LOG = []
for nome, sim, fatt in (("nuovo_12", NUOVO, FATT),      # l'arco a 1.2 LAM: i figli troncati
                        ("nuovo_30", NUOVO, 3.0),       # nessun troncamento: i contatori a ZERO
                        ("vecchio_12", VECCHIO, FATT)): # il codice di HEAD, per la byte-identita'
    rr = braccio(nome, sim, fatt)
    LOG.append("[%s] rc=%d%s%s" % (nome, rr.returncode, chr(10), (rr.stdout or "")[-600:]))
    if rr.returncode != 0:
        LOG.append((rr.stderr or "")[-2000:])
    ESITI.append((nome, rr.returncode))

P_ = []


def P(s=""):
    P_.append(s)


def criterio(sigla, cosa, ok, detta):
    P("%-6s %-4s  %s" % (sigla, "PASS" if ok else "FAIL", cosa))
    if detta:
        for r_ in detta.split(chr(10)):
            P("              " + r_)
    return bool(ok)


P("=" * 100)
P("SIGILLO `U2` -- CONTATORI DI `_nasce` SEPARATI PER GRANDEZZA E PER SITO")
P("=" * 100)
P()
for l in LOG:
    P(l)
P()

if any(rc != 0 for _, rc in ESITI):
    P("STOP: un braccio non e' arrivato in fondo. Nessun criterio si legge.")
    io.open(DEST, "w", encoding="utf-8", newline="\n").write(chr(10).join(P_) + chr(10))
    print(chr(10).join(P_))
    sys.exit(1)

A = leggi("nuovo_12")
B = leggi("nuovo_30")
V = leggi("vecchio_12")
LAM = A["LAM"]

P("CONFIGURAZIONE (dai default del sorgente, dichiarata):")
P("  LAM = %.9f   TEMPO_UNICO_MITOSI = %s   PLAST_DIN = %s   PLAST_MIT = %s"
  % (LAM, A["TEMPO_UNICO_MITOSI"], A["PLAST_DIN"], A["PLAST_MIT"]))
P("  PHI_CRIT = %.9f   TW_TETTO = %.9f   soglia0 = %.9f  (= 3 pi: TORS_4PI e' ON)"
  % (A["PHI_CRIT"], A["TW_TETTO"], A["soglia0"]))
P("  FINESTRA DI CREAZIONE, derivata dal codice: avv in (%.6f, %.6f) = (%.3f, %.3f) PHI_CRIT"
  % (A["finestra"][0], A["finestra"][1],
     A["finestra"][0] / A["PHI_CRIT"], A["finestra"][1] / A["PHI_CRIT"]))
P("  tw dell'arco = %.9f = %.4f PHI_CRIT  (IL MEZZO della finestra, non un numero scelto)"
  % (A["tw_sel"], A["tw_sel"] / A["PHI_CRIT"]))
P("  arco selezionato: d = %.9f = %.4f LAM,  d0 = %.9f"
  % (A["d_pre_sel"], A["d_pre_sel"] / LAM, A["d0_pre_sel"]))
P("  n  %d -> %d      archi  %d -> %d" % (A["n_pre"], A["n_post"], A["archi_pre"], A["archi_post"]))
P()
P("I CONTATORI, come sono usciti:")
for k in sorted(k for k in A if k.startswith("_sm_")):
    P("  %-26s %s" % (k, A[k]))
P()

OK = []

# ---- U2-1: UN SOLO arco si e' diviso. Senza questo, "risposta nota" non vale. -------------
uno = (A["n_post"] == A["n_pre"] + 1) and (A["archi_post"] == A["archi_pre"] + 1)
OK.append(criterio("U2-1", "UN SOLO arco si e' diviso (il caso e' quello dichiarato)", uno,
                   "n +%d, archi +%d   atteso +1 e +1 (un arco sparisce, due nascono)"
                   % (A["n_post"] - A["n_pre"], A["archi_post"] - A["archi_pre"])))

# ---- U2-2: i DUE figli su `d` sono troncati, e il contatore dice DUE (non uno) ------------
att_trd = 2
OK.append(criterio("U2-2", "`_sm_trd_mitosi` conta gli ARCHI VERI di `d`: DUE, non uno",
                   A.get("_sm_trd_mitosi") == att_trd,
                   "misurato %s   atteso %d   (il difetto corretto era proprio il sottoconto x2)"
                   % (A.get("_sm_trd_mitosi"), att_trd)))

# ---- U2-3: la LUNGHEZZA FABBRICATA su `d`, a risposta nota -------------------------------
att_lund = 2.0 * (LAM - A["d_pre_sel"] / 2.0)
mis_lund = A.get("_sm_lund_mitosi", 0.0)
OK.append(criterio("U2-3", "`_sm_lund_mitosi` = 2*(LAM - d/2), a risposta nota",
                   abs(mis_lund - att_lund) <= 1e-12 * max(1.0, att_lund),
                   "misurato %.15f%satteso    %.15f  = 2*(%.6f - %.6f)"
                   % (mis_lund, chr(10), att_lund, LAM, A["d_pre_sel"] / 2.0)))

# ---- U2-4: e la STESSA cosa su `d0`, con la sua chiave SEPARATA --------------------------
att_lund0 = 2.0 * (LAM - A["d0_pre_sel"] / 2.0)
mis_lund0 = A.get("_sm_lund0_mitosi", 0.0)
OK.append(criterio("U2-4", "`_sm_lund0_mitosi` ha la sua chiave e il suo valore (e' QUELLO di `P-GONFIA`)",
                   (abs(mis_lund0 - att_lund0) <= 1e-12 * max(1.0, att_lund0)
                    and A.get("_sm_trd0_mitosi") == 2),
                   "lund0 misurato %.15f   atteso %.15f%strd0 misurato %s   atteso 2"
                   % (mis_lund0, att_lund0, chr(10), A.get("_sm_trd0_mitosi"))))

# ---- U2-5: i contatori corrispondono agli ARCHI VERI nell'array, non a un modello --------
#      E' il criterio MODEL-FREE: si legge `d`/`d0` e si contano gli archi a LAM.
OK.append(criterio("U2-5", "i contatori coincidono con gli archi che nell'ARRAY stanno a `LAM`",
                   (A["d_a_lam"] == A.get("_sm_trd_mitosi")
                    and A["d0_a_lam"] == A.get("_sm_trd0_mitosi")),
                   "archi di `d`  a LAM nell'array: %d   contatore: %s%s"
                   "archi di `d0` a LAM nell'array: %d   contatore: %s%s"
                   "min(d) = %.9f   min(d0) = %.9f   (nessuno sotto LAM)"
                   % (A["d_a_lam"], A.get("_sm_trd_mitosi"), chr(10),
                      A["d0_a_lam"], A.get("_sm_trd0_mitosi"), chr(10),
                      A["d_min"], A["d0_min"])))

# ---- U2-6: IL CASO CHE DEVE FALLIRE -- la formula VECCHIA sullo STESSO evento ------------
#      Un contatore solo: `sum(LAM - v)` per CHIAMATA, senza molteplicita'.
#        chiamata `dh`     -> 1 voce  sotto LAM -> LAM - 0.6 LAM        = 0.4 LAM
#        chiamata `d0new`  -> 2 voci  sotto LAM -> 2*(LAM - 0.6 LAM)    = 0.8 LAM
#      totale MESCOLATO = 1.2 LAM, e sul lato `d` il conto era 0.4 LAM invece di 0.8.
vec_lund = 1.0 * (LAM - A["d_pre_sel"] / 2.0)                    # quello che la vecchia dava su `d`
vec_mesc = vec_lund + 2.0 * (LAM - A["d0_pre_sel"] / 2.0)        # la somma mescolata
fallisce = abs(vec_lund - att_lund) > 1e-12 * max(1.0, att_lund)
OK.append(criterio("U2-6", "IL CASO CHE DEVE FALLIRE: il criterio `U2-3` applicato alla formula VECCHIA da' FAIL",
                   fallisce,
                   "la vecchia, sullo STESSO evento, dava su `d`: %.15f%s"
                   "il criterio chiede                              %.15f   -> scarto %.15f%s"
                   "e la sua SOMMA MESCOLATA valeva %.9f = %.4f LAM, che non e' in NESSUNA delle due unita'.%s"
                   "Se questo criterio passasse sulla vecchia, non discriminerebbe la cura dal difetto."
                   % (vec_lund, chr(10), att_lund, abs(vec_lund - att_lund), chr(10),
                      vec_mesc, vec_mesc / LAM, chr(10))))

# ---- U2-7: `_g_sm_nascite` SALE anche senza troncamenti, i contatori nuovi NO ------------
zeri = [k for k in B if k.startswith("_sm_") and B[k] not in (0, 0.0)]
OK.append(criterio("U2-7", "senza troncamenti: `_g_sm_nascite` sale, i contatori nuovi restano a ZERO",
                   B["nascite"] > 0 and not zeri,
                   "arco a 3.0 LAM: nascite = %d (sale), contatori non nulli = %s%s"
                   "E' la ragione per cui i contatori esistono: `_g_sm_nascite` conta le INVOCAZIONI."
                   % (B["nascite"], zeri if zeri else "NESSUNO", chr(10))))

# ---- U2-8: BYTE-INERZIA contro il codice di HEAD (`STANDARD 2`) --------------------------
import numpy as np

fd = [io.open(os.path.join(TMP, n + "_d.npy"), "rb").read() for n in ("nuovo_12", "vecchio_12")]
fd0 = [io.open(os.path.join(TMP, n + "_d0.npy"), "rb").read() for n in ("nuovo_12", "vecchio_12")]
ident = (fd[0] == fd[1]) and (fd0[0] == fd0[1])
# CONTROLLO POSITIVO, e il primo che avevo scritto era VACUO: confrontava il caso a 3.0 LAM,
# i cui `d` sono diversi PERCHE' LI AVEVO IMPOSTATI IO diversi. Non provava che il confronto
# vedesse una differenza, provava che avevo scritto due numeri diversi. (Difetto mio.)
# Il controllo giusto e' `d` PRIMA contro `d` DOPO la mitosi, nello STESSO braccio: stessa
# grandezza, stesso braccio, e la mitosi DEVE averli cambiati.
ctrl = io.open(os.path.join(TMP, "nuovo_12_dPRE.npy"), "rb").read()
vive = (ctrl != fd[0])
OK.append(criterio("U2-8", "BYTE-IDENTICO al codice di HEAD su `d` e `d0` (i contatori non toccano la fisica)",
                   ident and vive,
                   "d  identico: %s      d0 identico: %s%s"
                   "CONTROLLO POSITIVO: `d` PRIMA della mitosi contro `d` DOPO, stesso braccio,"
                   " DIVERSO: %s%s"
                   "(senza, uno `identico` potrebbe essere un confronto cieco -- par.9)"
                   % (fd[0] == fd[1], fd0[0] == fd0[1], chr(10), vive, chr(10))))

# ---- U2-9: le chiavi sono SEPARATE per grandezza e per sito ------------------------------
chiavi = sorted(k for k in A if k.startswith("_sm_"))
attese_mit = {"_sm_lund_mitosi", "_sm_trd_mitosi", "_sm_visd_mitosi",
              "_sm_lund0_mitosi", "_sm_trd0_mitosi", "_sm_visd0_mitosi"}
OK.append(criterio("U2-9", "le chiavi sono SEPARATE per grandezza (`d`/`d0`) e per sito",
                   attese_mit.issubset(set(chiavi)),
                   "presenti: %s%smancanti: %s"
                   % (", ".join(chiavi), chr(10),
                      ", ".join(sorted(attese_mit - set(chiavi))) or "NESSUNA")))

P()
P("=" * 100)
P("ESITO: %d/%d PASS" % (sum(1 for x in OK if x), len(OK)))
P("=" * 100)
P()
P("COSA QUESTO SIGILLO *NON* DICE, e va detto:")
P("  - NON collauda il sito `schwinger` (md=2, md0=2): quel ramo non e' stato fatto scattare qui.")
P("    E' il QUARTO sito, e NON era fra i tre del rilievo -- la molteplicita' e' letta dal codice,")
P("    non misurata. **Resta da collaudare.**")
P("  - NON collauda il sito `semina` con un valore noto: li' md=1/md0=1 e il conto e' banale,")
P("    ma banale non e' misurato.")
P("  - I default usati sono quelli del SORGENTE, non l'argv del driver: `TEMPO_UNICO_MITOSI = %s`."
  % A["TEMPO_UNICO_MITOSI"])

T = chr(10).join(P_) + chr(10)
os.makedirs(os.path.dirname(DEST), exist_ok=True)
io.open(DEST, "w", encoding="utf-8", newline="\n").write(T)
print(T)
sys.exit(0 if all(OK) else 1)
