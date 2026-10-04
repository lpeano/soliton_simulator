# -*- coding: utf-8 -*-
"""LA PATCH DEL COMMIT `6b`: `MITOSI_2LAM` diventa LEGGE, in forma GENERALE.

### **LA LEGGE:** un arco si divide **solo se** `FRAZ_NASCITA * d >= LAM` **E**
`(1 - FRAZ_NASCITA) * d >= LAM`, ### **sempre, senza condizione sul flag.**

### ⛔ **PERCHE' UNA PATCH E NON UN EDIT A MANO:** il par.7 vuole che il codice di una
misura sia recuperabile ### **per costruzione**, e il braccio `0` del sigillo lo verifica
rifacendo il blob di oggi dal *prima* ### **piu' questa patch**. ### **Un edit a mano non si
ri-applica; una patch si.**

### **LE OPZIONI, e ciascuna serve A UN BRACCIO PRECISO del sigillo**

| opzione | che cosa fa | per quale braccio |
|---|---|---|
| *(nessuna)* | la cura, come va nel sorgente | `0`, `A`, `B` |
| `--t=N` | cambia `FRAZ_NASCITA` | `C` |
| `--cancello-vecchio` | lascia il cancello `d >= 2*LAM` | `C-bis (i)` |
| `--solo-destra` | il cancello guarda **solo** `(1-t)*d >= LAM` | `C-bis (ii)` |
| `--solo-sinistra` | il cancello guarda **solo** `t*d >= LAM` | `C-bis (iii)` |

### ⚠ **`(ii)` E `(iii)` SONO DUE CASI E NON UNO:** un cancello a **una sola meta'** sbaglia
### **solo sul lato che non guarda**. Con `t = 0.4` il troncone corto e' quello di `t`, quindi
il controllo sul solo `(1-t)` lo ### **manca**; con `t = 0.6` il corto si ### **scambia**.
### **Due copie provano che la congiunzione serve DA ENTRAMBI I LATI; una sola proverebbe
meta' della legge.**

**COMANDO:** `python csv/_seal_fork/_legge_2lam_patch.py --file=<copia> [opzioni]`
"""
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_QUI, ".."))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
Q = chr(34)
FILE = None
T = None
CANCELLO_VECCHIO = False
SOLO_DESTRA = False
SOLO_SINISTRA = False
for _a in sys.argv[1:]:
    if _a.startswith("--file="):
        FILE = _a.split("=", 1)[1]
    elif _a.startswith("--t="):
        T = float(_a.split("=", 1)[1])
    elif _a == "--cancello-vecchio":
        CANCELLO_VECCHIO = True
    elif _a == "--solo-destra":
        SOLO_DESTRA = True
    elif _a == "--solo-sinistra":
        SOLO_SINISTRA = True
if not FILE:
    raise SystemExit("serve --file=<copia del simulatore>")

t = io.open(FILE, encoding="utf-8").read()
fatte = []


def sost(ancora, nuovo, etichetta):
    """### OGNI SOSTITUZIONE SI ASSERISCE PER SE' (`P1-quater`): l'ancora si CONTA, e se
    non e' unica si FALLISCE. Un `assert` globale sarebbe soddisfatto dalle ALTRE."""
    global t
    n = t.count(ancora)
    if n != 1:
        raise SystemExit("** %s: ancora trovata %d volte, non 1 **" % (etichetta, n))
    t = t.replace(ancora, nuovo)
    fatte.append(etichetta)


def righe(*x):
    return NL.join(x)


# ===================== 1. IL CANCELLO, incondizionato e in forma GENERALE
_ANCORA_CANCELLO = righe(
    "        self._g_m2l_tot = getattr(self, " + Q + "_g_m2l_tot" + Q + ", 0) + int(np.size(c))",
    "        if MITOSI_2LAM and len(c):",
    "            _dc = np.asarray(self.d, float)[c]",
    "            _conforme = _dc >= 2.0 * LAM",
    "            self._g_m2l_negati = getattr(self, " + Q + "_g_m2l_negati" + Q
    + ", 0) + int(np.sum(~_conforme))",
    "            self._g_m2l_dmin = min(getattr(self, " + Q + "_g_m2l_dmin" + Q
    + ", float(" + Q + "inf" + Q + ")),",
    "                                   float(_dc.min()) if _dc.size else float("
    + Q + "inf" + Q + "))",
    "            ok = ok & _conforme")

if CANCELLO_VECCHIO:
    _COND = "_dc >= 2.0 * LAM"
    _NOTA = "CASO (i): il cancello VECCHIO `d >= 2*LAM`, che IGNORA la frazione"
elif SOLO_DESTRA:
    _COND = "(1.0 - FRAZ_NASCITA) * _dc >= LAM"
    _NOTA = "CASO (ii): SOLO la meta' `(1-t)`, che non guarda il troncone di `t`"
elif SOLO_SINISTRA:
    _COND = "FRAZ_NASCITA * _dc >= LAM"
    _NOTA = "CASO (iii): SOLO la meta' `t`, che non guarda il troncone di `(1-t)`"
else:
    _COND = None
    _NOTA = None

if _COND is None:
    _RIGHE_COND = righe(
        "            # ### I DUE TRONCONI, ENTRAMBI: il figlio nasce a `FRAZ_NASCITA * d` da",
        "            #   `a` e a `(1 - FRAZ_NASCITA) * d` da `b`, quindi ### **servono DUE",
        "            #   disuguaglianze e non una.** A `t = 0.5` coincidono, e la congiunzione",
        "            #   si riduce a `0.5*d >= LAM` -- che e' `d >= 2*LAM` ### **al bit**,",
        "            #   perche' moltiplicare per `0.5` e per `2.0` e' ### **esatto in",
        "            #   IEEE-754** (potenze di due: la mantissa non cambia). ### **Per questo",
        "            #   il braccio `A` del sigillo e' IDENTICO AL BYTE con il flag acceso.**",
        "            _sx = FRAZ_NASCITA * _dc >= LAM",
        "            _dx = (1.0 - FRAZ_NASCITA) * _dc >= LAM",
        "            _conforme = _sx & _dx")
else:
    _RIGHE_COND = righe(
        "            # ### " + _NOTA,
        "            _conforme = " + _COND)

sost(_ANCORA_CANCELLO, righe(
    "        self._g_m2l_tot = getattr(self, " + Q + "_g_m2l_tot" + Q + ", 0) + int(np.size(c))",
    "        # ### IL CANCELLO E' INCONDIZIONATO DAL COMMIT `6b`: `A13` ALLA NASCITA E' LEGGE.",
    "        #   ### **Non c'e' piu' un `if MITOSI_2LAM`**: il comportamento <<senza il flag>>",
    "        #   e' ### **uscito dal sorgente** e sta in `csv/_archivio/_rami_off_cura2.py`,",
    "        #   e il flag resta ### **INERTE come `PAV_COM`** (decisione 3 di Luca: si",
    "        #   conserva tutto), dichiarato fra i `[flag-inerti]`.",
    "        #   ### ⛔ **E IL CONTO DELLE LEGGI VA IN DIMINUZIONE** (`9-ter`): prima c'erano",
    "        #   ### **DUE comportamenti** (col flag e senza), ora ce n'e' ### **UNO**.",
    "        #   ### ✅ **E TOGLIE UNA VIOLAZIONE DI `A14`:** senza il cancello gli archi",
    "        #   sotto `LAM` nascono comunque e ### **`_nasce` li ALZA** -- cioe' modifica una",
    "        #   lunghezza DOPO averla creata, che e' una ### **proiezione** e viola `A14`",
    "        #   ### **per costruzione, qualunque sia il valore.** ### **Un cancello non",
    "        #   modifica lo stato: RIFIUTA un evento.** Non e' un taglio, e' un",
    "        #   ### **NON-ACCADIMENTO**.",
    "        #   ### ⚠ **E NON LA TOGLIE DOVE NON GUARDA:** lo Schwinger continua a produrre",
    "        #   archi sotto `LAM` -- e' `SCHW-SOTTO-LAM`, registrata e NON curata qui.",
    "        if len(c):",
    "            _dc = np.asarray(self.d, float)[c]",
    _RIGHE_COND,
    "            # ### I RIFIUTI SEPARATI PER CANCELLO, e serve: `negate` li MESCOLA, quindi",
    "            #   un rifiuto per densita' e uno per `LAM` erano ### **indistinguibili**.",
    "            #   ### **Tre contatori, e la somma dei tre e' il totale dei rifiutati.**",
    "            _no_dens = ~ok",
    "            _no_lam = ~_conforme",
    "            self._g_m2l_rif_solo_dens = getattr(self, " + Q
    + "_g_m2l_rif_solo_dens" + Q + ", 0) + int(np.sum(_no_dens & ~_no_lam))",
    "            self._g_m2l_rif_solo_lam = getattr(self, " + Q
    + "_g_m2l_rif_solo_lam" + Q + ", 0) + int(np.sum(~_no_dens & _no_lam))",
    "            self._g_m2l_rif_entrambi = getattr(self, " + Q
    + "_g_m2l_rif_entrambi" + Q + ", 0) + int(np.sum(_no_dens & _no_lam))",
    "            # ### `|tw|` DEGLI ARCHI RIFIUTATI PER `LAM`: una DIAGNOSTICA per il `6c`,",
    "            #   non una legge. ### Si tiene la LISTA e non la somma, perche' il mandato",
    "            #   chiede la ### **MEDIANA** -- e una mediana non si ricostruisce da una",
    "            #   somma. ### ⚠ Cresce, ma i rifiuti sono pochi (2 per scena nella misura",
    "            #   del guardiano), e ### **non entra in nessun calcolo di fisica.**",
    "            if np.any(_no_lam):",
    "                _tws = np.abs(np.asarray(self.tw, float)[c][_no_lam])",
    "                self._g_m2l_tw_rif = (getattr(self, " + Q + "_g_m2l_tw_rif" + Q
    + ", []) + [float(x) for x in _tws])",
    "            self._g_m2l_negati = getattr(self, " + Q + "_g_m2l_negati" + Q
    + ", 0) + int(np.sum(~_conforme))",
    "            self._g_m2l_dmin = min(getattr(self, " + Q + "_g_m2l_dmin" + Q
    + ", float(" + Q + "inf" + Q + ")),",
    "                                   float(_dc.min()) if _dc.size else float("
    + Q + "inf" + Q + "))",
    "            ok = ok & _conforme"),
    "IL CANCELLO incondizionato, in forma generale, coi tre contatori separati")

# ===================== 2. `FRAZ_NASCITA`, per le copie
if T is not None:
    sost("FRAZ_NASCITA = 0.5",
         "FRAZ_NASCITA = %r" % T,
         "`FRAZ_NASCITA` = %r (solo nelle copie)" % T)

# ===================== 3. il default del flag, e il commento NOMINA il flag (`H-P7`)
sost(righe(
    "MITOSI_2LAM = False     # [CURA 5, 2026-09-25] `MITOSI_2LAM`: `A13` ALLA NASCITA. Approvata"),
    righe(
    "MITOSI_2LAM = False     # ⛔⛔ `MITOSI_2LAM` E' INERTE DAL COMMIT `6b` (2026-10-04): il"),
    "il default: `MITOSI_2LAM` dichiarato INERTE, e il commento NOMINA il flag")

# ===================== 4. il flag fra i `[flag-inerti]`, come `PAV_COM`
sost(righe(
    "    if PAV_COM:",
    "        _inerti.append(" + Q + "PAV_COM: il pavimento di d0 e' ARCHIVIATO in " + Q),
    righe(
    "    if MITOSI_2LAM:",
    "        _inerti.append(" + Q + "MITOSI_2LAM: il suo cancello e' diventato LEGGE "
    "INCONDIZIONATA " + Q,
    "              " + Q + "nel commit `6b` (2026-10-04), e il ramo <<senza il flag>> e' " + Q,
    "              " + Q + "ARCHIVIATO in csv/_archivio/_rami_off_cura2.py. Il flag NON FA " + Q,
    "              " + Q + "NIENTE: un arco si divide SOLO se FRAZ_NASCITA*d >= LAM E " + Q,
    "              " + Q + "(1-FRAZ_NASCITA)*d >= LAM, con o senza di lui." + Q + ")",
    "    if PAV_COM:",
    "        _inerti.append(" + Q + "PAV_COM: il pavimento di d0 e' ARCHIVIATO in " + Q),
    "`MITOSI_2LAM` fra i `[flag-inerti]`, col posto dove e' finito il ramo")

# ===================== 5. l'avviso `[cura5]` non ha piu' senso: il flag e' inerte
sost(righe(
    "    if MITOSI_2LAM:",
    "        print(" + Q + "[cura5] MITOSI_2LAM ON: un arco si divide SOLO se `d >= 2 LAM` (`A13` alla " + Q,
    "              " + Q + "nascita). Lo Schwinger NON e' toccato." + Q + ")"),
    righe(
    "    # ### L'AVVISO `[cura5]` E' TOLTO, e il motivo e' che DIREBBE IL FALSO: annunciava",
    "    #   *<<MITOSI_2LAM ON: un arco si divide SOLO se d >= 2 LAM>>* ### **come se fosse il",
    "    #   flag a deciderlo.** Dal `6b` la legge vale ### **sempre**, e il flag e'",
    "    #   ### **inerte**: l'annuncio lo dà ora il blocco `[flag-inerti]`, che e' il posto",
    "    #   dove questo repo dichiara i flag che non fanno niente (come `PAV_COM`)."),
    "l'avviso `[cura5]` tolto: diceva il falso")

# ===================== 6. i DUE commenti che asserivano la legge SOTTO CONDIZIONE
sost("# PIU': con `SEMINA_LAM` e `MITOSI_2LAM` si ha `d >= LAM`. ⚠ MA E'",
     "# PIU': con `SEMINA_LAM` si ha `d >= LAM` alla semina, e dal `6b` ANCHE alla "
     "divisione — ### **senza condizione sul flag**. ⚠ MA E'",
     "il commento :3471: la legge non e' piu' condizionata al flag")

sost("#   NESSUN PAVIMENTO: `d >= LAM` con `SEMINA_LAM`/`MITOSI_2LAM`. E poiche' e'",
     "#   NESSUN PAVIMENTO: `d >= LAM` con `SEMINA_LAM`, e alla divisione ### **SEMPRE dal "
     "commit `6b`** (non piu' <<con `MITOSI_2LAM`>>: il flag e' INERTE). E poiche' e'",
     "il commento :8929: la legge e' incondizionata, il flag e' inerte")

io.open(FILE, "w", encoding="utf-8", newline=NL).write(t)
print("=" * 92)
print("  patch applicata a %s" % FILE)
for f in fatte:
    print("  OK  " + f)
