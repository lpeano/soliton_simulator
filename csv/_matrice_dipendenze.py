# -*- coding: utf-8 -*-
r"""**LA MATRICE LETTURA/SCRITTURA DEI `14` PEZZI, DAL CODICE** — *il passo `C` della memoria.*

> ### ⛔ **PERCHE' ESISTE** *(`2026-10-19`)*: il mandato della memoria chiede ### **la
> matrice delle dipendenze fra i `14` pezzi**, e la correzione del guardiano *(errore
> `n.11`)* dice che ### **NON si prende dalla tabella**: `ambito` e' una lista unica, non
> distingue lettura da scrittura, e ### **non dichiara che ogni pezzo legge `cs`
> attraverso il proprio tempo proprio** -- un ### **falso zero** proprio sulla dipendenza
> che conta. ### **Si ricava dal CODICE.**

## ⭐ DUE LETTURE, E DEVONO CONCORDARE

### **STATICA (AST, con la CHIUSURA DELLE CHIAMATE):** da ogni operatore del motore si
seguono le chiamate *(`self.x`, `mot.x`, `FP.x`, `EP.x`, `MV.x`, `SAT.x`, e le funzioni
dello stesso modulo)* dentro i moduli del percorso del tick, e si raccolgono gli attributi
del motore che si leggono *(`cs`, `lambda_c`, `dtau`, `geo.U`, ...)* e le chiavi dello
stato. ### ⚠ **E' una SOVRA-approssimazione:** segue anche i rami spenti.
### **DINAMICA (sul passo che gira):** ogni pezzo ### **nella sua posizione del palindromo**
*(lo stato e' quello che gli arriva davvero)*, con `cs` al centro come lo fissa il tick, e
si misura:
- **scrive `psi_h` / `phi_h`**: i byte cambiano;
- **muove `rho` / `Lambda`**: la norma per nodo cambia oltre la ### **banda delle norme**
  *(`_collauda_cs_l1.ULP_NORME` ulp sulla scala)*: una fase o un unitario dentro il nodo
  ### **scrivono `phi_h` senza muovere `Lambda`**;
- **legge `cs`**: l'uscita cambia se `mot.cs` si dimezza ### **sui nodi PARI**;
- **legge la materia** *(per l'uscita sul vuoto)*: `phi_h` in uscita cambia se `psi_h` in
  entrata si dimezza sulle estremita' dei nodi pari;
- **legge il vuoto** *(per l'uscita sulla materia)*: `psi_h` in uscita cambia se `phi_h` in
  entrata si dimezza sulle estremita' dei nodi pari *(con `mot.cs` FERMO: e' la lettura
  DIRETTA di `Lambda`)*.
### ⚠ **Il fattore `0.5` non e' una manopola:** la domanda e' ### **<<l'uscita dipende da
questo ingresso?>>**, e qualunque cambio non nullo risponde -- il confronto e' ### **sui
byte.**
### ⛔⛔ **MA LA PERTURBAZIONE NON PUO' ESSERE UNIFORME** *(trovato dalla prova a vuoto,
`2026-10-19`, col caso `M5`)*: il peso d'arco `2 cs_b^2/(cs_a + cs_b)^2` di
`energia_pesata.d_peso_arco` e' ### **OMOGENEO DI GRADO ZERO** in `cs`, e un `0.5`
uniforme *(esatto in binario)* lo lascia ### **identico al bit** -- quindi la sonda
uniforme ### **non vedeva che `CAMM-FASE-VUOTO` legge `cs`.** ### **Una sonda uniforme e'
cieca alle dipendenze dai RAPPORTI**: si dimezza ### **solo sui nodi pari.**

## ⛔ L'AUTO-DIPENDENZA, IN UNA COLONNA SUA *(annotazione del guardiano, `557f3e66`)*

### **Un pezzo e' AUTO-DIPENDENTE se, nella stessa applicazione, MUOVE `Lambda` e LEGGE
`cs`** *(una funzione di `Lambda`)*. ### **Da solo rende incrociate le dipendenze**, e la
variante sfalsata alla leapfrog diventerebbe implicita.

## ⛔ I CASI, FISSATI NEL TASK HISTORY PRIMA DEI NUMERI

| | il caso | deve |
|---|---|---|
| `M1` | `CAMM-SPOSTAMENTO` legge `cs` *(statico E dinamico)* | ### **RIUSCIRE**, se no lo strumento e' cieco |
| `M1-cieco` | lo STESSO statico **senza** la chiusura delle chiamate | ### **NON trovarlo**: e' cio' che fa la chiusura |
| `M3` | `CAMM-GROVER` **non** scrive `phi_h` | ### **il contrario FALLISCE** |
| `M4` | `CAMM-GROVER-VUOTO` scrive `phi_h` ma **non** muove `Lambda` | ### **il contrario FALLISCE** |
| `M5` | statico e dinamico **concordano** su <<legge `cs`>> | se no, ### **si dice pezzo per pezzo** |

## ⭐ LA CONFIGURAZIONE

La scena e lo stato di `C5` *(`csv/_costo_punti_fissi.scena`)*, taglia `16`, `Lambda_c`
### **`D2.SPAZZATA[3] = 8.0`** *(rapporto `1`, quello del giro corto del passo `B`)*.

Gira con:  python csv/_matrice_dipendenze.py
"""
import ast
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
RADICE = os.path.dirname(_QUI)

import numpy as np                                             # noqa: E402

import _costo_punti_fissi as CPF                               # noqa: E402

TAGLIA = 16
IRAPPORTO = 3                # D2.SPAZZATA[3] = 8.0: rapporto 1
NOMI_MOTORE = ("self", "mot", "motore")
INTERESSANTI = ("cs", "lambda_c", "dtau", "geo.U", "geo.n", "regola_punto_medio")


# =====================================================================================
#   LA LETTURA STATICA
# =====================================================================================
class Indice(object):
    """### Le funzioni dei moduli del percorso del tick, ### **e i loro alias.**"""

    def __init__(self, moduli):
        self.f = {}          # (modulo, nome) -> FunctionDef
        self.alias = {}      # modulo -> {alias: modulo}
        for mod in moduli:
            src = io.open(os.path.join(RADICE, "primo_ordine", mod + ".py"),
                          encoding="utf-8").read()
            arb = ast.parse(src)
            al = {}
            for n in ast.walk(arb):
                if isinstance(n, ast.Import):
                    for a in n.names:
                        if a.name in moduli:
                            al[a.asname or a.name] = a.name
            self.alias[mod] = al
            for n in arb.body:
                if isinstance(n, ast.FunctionDef):
                    self.f[(mod, n.name)] = n
                elif isinstance(n, ast.ClassDef):
                    for m in n.body:
                        if isinstance(m, ast.FunctionDef):
                            self.f[(mod, "%s.%s" % (n.name, m.name))] = m

    def chiamate(self, mod, fn):
        """### Le funzioni chiamate da `fn`, ### **risolte nei moduli del percorso.**"""
        fuori = []
        for n in ast.walk(fn):
            if not isinstance(n, ast.Call):
                continue
            f = n.func
            dove = None
            if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
                if f.value.id in self.alias[mod]:
                    dove = (self.alias[mod][f.value.id], f.attr)
                elif f.value.id in NOMI_MOTORE:
                    dove = ("motore", "Motore." + f.attr)
            elif isinstance(f, ast.Name):
                dove = (mod, f.id)
            if dove is not None and dove in self.f:
                fuori.append(dove)
        return fuori


def _attributi_del_motore(fn):
    """### Gli attributi letti dal motore in `fn`: `cs`, `geo.U`, ..."""
    fuori = set()
    for n in ast.walk(fn):
        if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) \
                and n.value.id in NOMI_MOTORE:
            fuori.add(n.attr)
        elif isinstance(n, ast.Attribute) and isinstance(n.value, ast.Attribute) \
                and isinstance(n.value.value, ast.Name) and n.value.value.id in NOMI_MOTORE:
            fuori.add("%s.%s" % (n.value.attr, n.attr))
    return fuori


def statica(ind, metodo, chiusura):
    """### `{attributo: catena}` letti dal metodo, ### **con o senza la chiusura.**

    La catena e' ### **la prima strada trovata** *(in ampiezza)* dal metodo alla funzione
    che legge.
    """
    radice = ("motore", "Motore." + metodo)
    visti, coda = {radice: [radice[1]]}, [radice]
    letti = {}
    chi = {}
    while coda:
        x = coda.pop(0)
        for a in _attributi_del_motore(ind.f[x]):
            letti.setdefault(a, visti[x])
            chi.setdefault(a, set()).add(x[1])
        if not chiusura:
            continue
        for y in ind.chiamate(x[0], ind.f[x]):
            if y not in visti:
                visti[y] = visti[x] + [y[1]]
                coda.append(y)
    letti["__chi__"] = chi
    return letti, set(visti)


# =====================================================================================
#   LA LETTURA DINAMICA
# =====================================================================================
def _norme(mot, st):
    return mot.densita_materia(st).copy(), mot.densita_vuoto(st).copy()


def _applica(mot, par, idl, st):
    import tick as TK
    nome, vp = TK.OPERATORE[idl]
    mot.apri_tick()
    mot.operatori[nome](st, par if vp else {}, 0.5)
    mot.chiudi_tick()
    return st


def dinamica():
    """### Una riga per POSIZIONE del palindromo, ### **sullo stato che le arriva.**"""
    import _collauda_cs_l1 as L1
    import composizione as CM
    import flussi_parziali as FP
    import tick as TK
    eps = float(np.finfo(float).eps)
    lc, _lam, rapp = CPF.lambda_c(TAGLIA, IRAPPORTO)
    _inc, mot, st, par = CPF.scena(TAGLIA)
    FP.accendi_cs(mot, lc, st)
    fp = mot._b("tk_cs", (mot.inc.n,), float)
    TK.cs_al_centro(CPF._copia(st), mot, par, lc, fp, ())
    cs = mot.cs.copy()
    # ### la sonda: `0.5` sui nodi PARI, `1` sui dispari -- per nodo e per estremita'
    pari_n = np.where(np.arange(mot.inc.n) % 2 == 0, 0.5, 1.0)
    pari_e = pari_n[mot.inc.nodo]
    righe = []
    s = CPF._copia(st)
    for k, (idl, _fr, _tp) in enumerate(CM.ORDINE):
        r0, l0 = _norme(mot, s)
        mot.cs = cs.copy()
        base = _applica(mot, par, idl, CPF._copia(s))
        r1, l1 = _norme(mot, base)
        banda_r = L1.ULP_NORME * eps * float(np.max(np.abs(r0)))
        banda_l = L1.ULP_NORME * eps * float(np.max(np.abs(l0)))

        def diverso(a, b):
            return not np.array_equal(a, b)
        # legge cs: mot.cs dimezzato SUI NODI PARI (una sonda uniforme e' cieca ai rapporti)
        mot.cs = cs * pari_n
        pc = _applica(mot, par, idl, CPF._copia(s))
        mot.cs = cs.copy()
        # legge la materia: psi_h dimezzato, si guarda phi_h in uscita
        sm = CPF._copia(s)
        sm["psi_h"] = sm["psi_h"] * pari_e.reshape(-1, 1)
        pm = _applica(mot, par, idl, sm)
        # legge il vuoto: phi_h dimezzato, si guarda psi_h in uscita
        sv = CPF._copia(s)
        sv["phi_h"] = sv["phi_h"] * pari_e
        pv = _applica(mot, par, idl, sv)
        mot.cs = cs.copy()
        d = {
            "pos": k + 1, "id": idl,
            "scrive_psi": diverso(base["psi_h"], s["psi_h"]),
            "scrive_phi": diverso(base["phi_h"], s["phi_h"]),
            "muove_rho": float(np.max(np.abs(r1 - r0))) > banda_r,
            "muove_lam": float(np.max(np.abs(l1 - l0))) > banda_l,
            "d_rho": float(np.max(np.abs(r1 - r0))), "d_lam": float(np.max(np.abs(l1 - l0))),
            "legge_cs": (diverso(pc["psi_h"], base["psi_h"])
                         or diverso(pc["phi_h"], base["phi_h"])),
            "legge_materia": diverso(pm["phi_h"], base["phi_h"]),
            "legge_vuoto": diverso(pv["psi_h"], base["psi_h"]),
        }
        d["auto"] = d["muove_lam"] and d["legge_cs"]
        righe.append(d)
        # lo stato avanza: la posizione dopo riceve cio' che questa ha prodotto
        s = base
    return righe, lc, rapp


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import _censimento_punti_fissi as C
    import _collauda_cs_l1 as L1
    import composizione as CM
    import tick as TK
    moduli = sorted(os.path.basename(p)[:-3] for p in C.chiusura_import(C.RADICI_TICK))
    ind = Indice(moduli)
    print("=" * 100)
    print("LA MATRICE LETTURA/SCRITTURA DEI 14 PEZZI, DAL CODICE -- il passo `C` della memoria")
    print("=" * 100)
    print("  i moduli letti (il percorso del tick): %s" % " ".join(moduli))
    print("  l'ordine: composizione.ORDINE, impronta %s, %d pezzi" % (CM.IMPRONTA,
                                                                    len(CM.ORDINE)))
    # ------------------------------------------------------------------ STATICA
    print("-" * 100)
    print("### LA LETTURA STATICA (AST, chiusura delle chiamate; segue anche i rami spenti)")
    stat = {}
    for idl in sorted(set(x[0] for x in CM.ORDINE)):
        nome, _vp = TK.OPERATORE[idl]
        # il nome del metodo si legge dal REGISTRO del motore, non si indovina
        metodo = _metodo_registrato(ind, nome)
        letti, funzioni = statica(ind, metodo, True)
        stat[idl] = (letti, funzioni)
        print("  %-24s %-24s legge: %s" % (idl, "Motore." + metodo,
                                         ", ".join(a for a in INTERESSANTI if a in letti)))
        if "cs" in letti:
            print("  %-24s %-24s   la prima strada fino a `.cs`: %s"
                  % ("", "", " -> ".join(letti["cs"])))
            print("  %-24s %-24s   TUTTE le funzioni che leggono `.cs`: %s"
                  % ("", "", ", ".join(sorted(letti["__chi__"]["cs"]))))
    # ------------------------------------------------------------------ DINAMICA
    print("-" * 100)
    righe, lc, rapp = dinamica()
    print("### LA LETTURA DINAMICA: taglia %d, Lambda_c = %.2f (rapporto %.3f), cs al CENTRO;"
          " la banda delle norme %d ulp" % (TAGLIA, lc, rapp, L1.ULP_NORME))
    print("  %-3s %-24s %-5s %-5s %-6s %-6s %-6s %-8s %-8s %-6s %s"
          % ("pos", "pezzo", "scr.", "scr.", "muove", "muove", "legge", "legge",
             "legge", "AUTO", "max|d rho| / max|d Lambda|"))
    print("  %-3s %-24s %-5s %-5s %-6s %-6s %-6s %-8s %-8s %-6s"
          % ("", "", "psi", "phi", "rho", "Lambda", "cs", "materia", "vuoto",
             "L<-cs"))

    def sn(x):
        return "si" if x else "-"
    for d in righe:
        print("  %-3d %-24s %-5s %-5s %-6s %-6s %-6s %-8s %-8s %-6s %.1e / %.1e"
              % (d["pos"], d["id"], sn(d["scrive_psi"]), sn(d["scrive_phi"]),
                 sn(d["muove_rho"]), sn(d["muove_lam"]), sn(d["legge_cs"]),
                 sn(d["legge_materia"]), sn(d["legge_vuoto"]),
                 "### SI" if d["auto"] else "-", d["d_rho"], d["d_lam"]))
    sys.stdout.flush()
    # ------------------------------------------------------------------ I CASI
    print("-" * 100)
    print("### I CASI, fissati nel task history PRIMA dei numeri")
    per = {}
    for d in righe:
        per.setdefault(d["id"], []).append(d)
    esiti = []

    def caso(che, ok, nota):
        esiti.append(ok)
        print("  %-62s %s   %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    m1s = "cs" in stat["CAMM-SPOSTAMENTO"][0]
    m1d = all(d["legge_cs"] for d in per["CAMM-SPOSTAMENTO"])
    caso("M1  CAMM-SPOSTAMENTO legge cs (statico E dinamico)", m1s and m1d,
         "statico %s, dinamico %s" % (m1s, m1d))
    cieco, _f = statica(ind, _metodo_registrato(ind, TK.OPERATORE["CAMM-SPOSTAMENTO"][0]),
                        False)
    caso("M1-cieco  senza la chiusura lo statico NON lo trova", "cs" not in cieco,
         "il corpo dell'operatore da solo legge: %s"
         % (sorted(x for x in cieco if x != "__chi__") or "niente"))
    m3 = not any(d["scrive_phi"] for d in per["CAMM-GROVER"])
    caso("M3  CAMM-GROVER non scrive phi_h", m3, "")
    m4 = (all(d["scrive_phi"] for d in per["CAMM-GROVER-VUOTO"])
          and not any(d["muove_lam"] for d in per["CAMM-GROVER-VUOTO"]))
    caso("M4  CAMM-GROVER-VUOTO scrive phi_h e NON muove Lambda", m4,
         "max|d Lambda| = %.1e" % max(d["d_lam"] for d in per["CAMM-GROVER-VUOTO"]))
    discordi = [idl for idl in per
                if ("cs" in stat[idl][0]) != all(d["legge_cs"] for d in per[idl])]
    caso("M5  statico e dinamico concordano su <<legge cs>>", not discordi,
         "discordi: %s" % (discordi or "nessuno"))
    # ------------------------------------------------------------------ LE LETTURE
    print("-" * 100)
    print("### INCROCIATE? -- la definizione del par.2 del task history, e l'annotazione")
    a_ = sorted(set(d["id"] for d in righe if d["muove_lam"] and d["legge_materia"]))
    b_ = sorted(set(d["id"] for d in righe
                    if (d["scrive_psi"] or d["muove_rho"]) and (d["legge_cs"]
                                                               or d["legge_vuoto"])))
    auto = sorted(set(d["id"] for d in righe if d["auto"]))
    print("  (A) muove Lambda E legge la materia:        %s" % (a_ or "nessuno"))
    print("  (B) scrive la materia E legge cs o il vuoto: %s" % (b_ or "nessuno"))
    print("  la definizione del par.2 (A e B nello stesso palindromo): %s"
          % ("INCROCIATE" if a_ and b_ else "NON incrociate"))
    print("  l'AUTO-DIPENDENZA (muove Lambda E legge cs, nello stesso pezzo): %s"
          % (auto or "nessuno"))
    print("  con l'annotazione di 557f3e66 (l'auto-dipendenza basta): %s"
          % ("INCROCIATE" if (a_ and b_) or auto else "NON incrociate"))
    print("-" * 100)
    print("### E PER LE VARIANTI DELLA MEMORIA (lettura, NON una decisione)")
    if auto:
        print("  (a) estrapolazione: resta ESPLICITA -- l'auto-dipendenza non la rende")
        print("      implicita, ma il peso estrapolato e' fisso dentro un pezzo che muove la")
        print("      grandezza da cui dipende: NON simmetrica (come gia' scritto in mappa).")
        print("  (b) peso sfalsato alla leapfrog: ESCLUSA come variante esplicita simmetrica.")
        print("      In %s il passo del pezzo dipende da cio' che il pezzo muove: per essere"
              % ", ".join(auto))
        print("      simmetrica dentro il pezzo servirebbe di nuovo un punto fisso.")
    else:
        print("  nessun pezzo auto-dipendente: l'annotazione non esclude (b).")
    print("  la scelta <<lo stato contiene il passato>> e' UNA e di Luca.")
    print("=" * 100)
    ok = all(esiti)
    print("### I CASI: %d su %d   %s" % (sum(esiti), len(esiti),
                                         "PASSA" if ok else "### FALLISCE"))
    print("=" * 100)
    return 0 if ok else 1


def _metodo_registrato(ind, nome):
    """### Il metodo che il motore REGISTRA per l'operatore `nome`, ### **letto dall'AST
    del dizionario `self.operatori` in `Motore.__init__`.**"""
    init = ind.f[("motore", "Motore.__init__")]
    for n in ast.walk(init):
        if isinstance(n, ast.Assign) and any(
                isinstance(t, ast.Attribute) and t.attr == "operatori" for t in n.targets):
            for k, v in zip(n.value.keys, n.value.values):
                if isinstance(k, ast.Constant) and k.value == nome:
                    return v.attr
    raise AssertionError("l'operatore %r non e' nel registro del motore" % nome)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
