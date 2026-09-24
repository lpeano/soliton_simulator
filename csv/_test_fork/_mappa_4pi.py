# -*- coding: utf-8 -*-
"""LA MAPPA DEL `4pi` -- dove vive la doppia copertura, e quale delle quattro e'.

Punto (2) del prompt unico di Luca, 2026-09-24. **SOLA LETTURA. AST. Tabella generata.**

RIUSA `_censimento_fasi.py` (`Z118`): non si ricomincia da zero. Quello trova i PUNTI
(`W2`/`W4`/`OSS`/`A2P`) e le classi `T`/`L`/`E` *(cosa si leviga)*; questo aggiunge la domanda
NUOVA -- **di CHI e' il `4pi` in quel punto** -- e lo **stato EFFETTIVO nei run**.

LE QUATTRO CLASSI, e le REGOLE con cui si assegnano (fissate PRIMA di girare):
  `VERA`       la doppia copertura **dello SPINORE**: un oggetto di spin 1/2 torna in se'
               dopo `4pi`, e questo e' FISICA. Regola: nell'espressione compare una
               grandezza spinoriale (`psi_spinor`, `_spinor_lift`, `s_k`, `spinor`) oppure
               un MEZZO ANGOLO (`/2` su `chi`, `theta`, `tw`), o il sito e' fra quelli che
               Luca nomina come veri (`_phc`).
  `DICHIARATA` il **dominio `[0, 4pi)` di `phi`**: e' una CONVENZIONE del codice, non una
               proprieta' misurata. Regola: avvolgimento `% (4 pi)` (o `_w4`/`_wphi`)
               applicato a `phi`, `phi0`, `fm`, `anti`.
  `EREDITATA`  cio' che prende la sua SCALA da `phi`: `dph`, `twp`, `tw`, `_w4`/`_w8`, le
               soglie (`PHI_CRIT + twist_max`, `TW_TETTO`, l'inversione), `twist_dip`,
               l'antifase, il ritmo. Regola: la riga legge una di queste grandezze e NON e'
               `VERA`.
  `INVERSA`    **il finto pilota il vero**: una grandezza `EREDITATA` (tipicamente `tw`)
               SCRIVE una grandezza spinoriale o di Bloch. Regola: un assegnamento il cui
               BERSAGLIO e' spinoriale/Bloch e il cui VALORE legge `tw`/`twp`/`dph`.
               **E' la classe che l'architettura a un solo ponte deve abolire.**

⚠ L'ORDINE DI PRECEDENZA CONTA, e si dichiara: `INVERSA` > `VERA` > `DICHIARATA` >
  `EREDITATA`. Un sito che e' sia spinoriale sia letto da `tw` e' **`INVERSA`**, perche' la
  domanda di Luca e' *dove il finto comanda il vero*, e quella vince su tutto.

⚠ CIO' CHE QUESTA MAPPA NON FA: **non decide**. Dice di CHI e' il `4pi` e se quel punto
  GIRA. La proposta e' il punto (5), ed e' una scheda a parte.

ASCII PURO.
"""
import ast
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

import _censimento_fasi as Z118          # SI RIUSA: non si ricomincia da zero

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SORGENTE = os.path.join(RADICE, "soliton_simulator.py")
# lo stato EFFETTIVO: il referto di configurazione GENERATO da un run vero
CFG = os.path.join(_QUI, "_g4_corto", "CONFIGURAZIONE.json")
OUT = os.path.join(_QUI, "_diag_D", "MAPPA_4PI.md")

# ---------------------------------------------------------------- i vocabolari, dichiarati
SPINORIALI = ("psi_spinor", "_spinor_lift", "spinor", "s_k", "psi_spin")
BLOCH = ("_nb", "nb", "omega_s", "omega_new")
EREDITA = ("dph", "twp", "tw", "twist_dip", "twist_max", "TW_TETTO", "PHI_CRIT",
           "soglia0", "tau_soglia", "fm", "anti", "signed", "phivel")
DA_PHI = ("phi", "phi0", "fm", "anti")
# i siti che Luca nomina come VERI: si dichiarano, perche' non sono derivabili da un nome
VERI_DICHIARATI = {3186: "_phc: la fase dell'orologio proprio, dove il 4pi e' dello spinore"}


def _nomi(nodo):
    """Tutti i nomi (Name/Attribute) che compaiono in un sottoalbero."""
    out = set()
    for n in ast.walk(nodo):
        if isinstance(n, ast.Name):
            out.add(n.id)
        elif isinstance(n, ast.Attribute):
            out.add(n.attr)
    return out


def _ha(nomi, vocab):
    return any(v in nomi for v in vocab)


def _mezzo_angolo(nodo):
    """Un MEZZO ANGOLO: una divisione per 2 (o un `*0.5`) su un angolo."""
    for n in ast.walk(nodo):
        if isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Div, ast.Mult)):
            nm = _nomi(n)
            if not _ha(nm, ("chi", "theta", "tw", "chi_torsione", "_chi_mat")):
                continue
            for lato in (n.left, n.right):
                if isinstance(lato, ast.Constant) and lato.value in (2, 2.0, 0.5):
                    return True
    return False


def classifica(nodo_riga, righe_testo, riga):
    """LA CLASSE, con la regola che l'ha deciso. Precedenza: INVERSA > VERA > DICHIARATA > ERED."""
    nomi = _nomi(nodo_riga) if nodo_riga is not None else set()
    testo = righe_testo[riga - 1] if 0 < riga <= len(righe_testo) else ""

    # INVERSA: un assegnamento il cui BERSAGLIO e' spinoriale/Bloch e il cui VALORE legge tw
    if isinstance(nodo_riga, (ast.Assign, ast.AugAssign)):
        bers = (nodo_riga.targets if isinstance(nodo_riga, ast.Assign)
                else [nodo_riga.target])
        nb = set()
        for b in bers:
            nb |= _nomi(b)
        nv = _nomi(nodo_riga.value) if nodo_riga.value is not None else set()
        if _ha(nb, SPINORIALI + BLOCH) and _ha(nv, ("tw", "twp", "dph")):
            return "INVERSA", "bersaglio spinoriale/Bloch, valore che legge `tw`/`twp`/`dph`"

    if riga in VERI_DICHIARATI:
        return "VERA", "sito dichiarato da Luca: %s" % VERI_DICHIARATI[riga]
    if _ha(nomi, SPINORIALI):
        return "VERA", "l'espressione contiene una grandezza SPINORIALE"
    if _mezzo_angolo(nodo_riga) if nodo_riga is not None else False:
        return "VERA", "MEZZO ANGOLO (`/2` su un angolo): e' la firma dello spin 1/2"

    # DICHIARATA: l'avvolgimento del dominio di `phi`
    if ("4 * np.pi" in testo or "4*np.pi" in testo or "_w4(" in testo
            or "_wphi(" in testo or "_dphi()" in testo):
        if _ha(nomi, DA_PHI):
            return "DICHIARATA", "avvolgimento del DOMINIO di `phi` (convenzione, non misura)"

    if _ha(nomi, EREDITA) or _ha(nomi, DA_PHI):
        return "EREDITATA", "legge una grandezza che prende la sua scala da `phi`"
    return "?", "nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara"


def nodo_di_riga(albero):
    """{riga: il nodo di istruzione che comincia li'}."""
    out = {}
    for n in ast.walk(albero):
        if isinstance(n, ast.stmt) and hasattr(n, "lineno"):
            out.setdefault(n.lineno, n)
    return out


def effettivo():
    """Lo stato EFFETTIVO dei flag in un run vero, dal referto di configurazione GENERATO."""
    if not os.path.exists(CFG):
        return {}, "NESSUN REFERTO: `%s` non esiste" % os.path.relpath(CFG, RADICE)
    d = json.loads(io.open(CFG, encoding="utf-8").read())
    return d.get("effettivo_dal_modulo", {}), (
        "dal referto di configurazione del run `_g4_corto`, commit %s"
        % (d.get("git", {}).get("head", "?")[:8]))


# ---------------------------------------------------------------- IL COLLAUDO (`P1-sexies`)
def collaudo(W):
    W("COLLAUDO DELLE REGOLE DI CLASSIFICAZIONE su casi a RISPOSTA NOTA (`P1-sexies`)\n")
    W("-" * 100 + "\n")
    e = []

    def cls(src, riga=1):
        a = ast.parse(src)
        nodi = nodo_di_riga(a)
        return classifica(nodi.get(riga), src.split("\n"), riga)

    casi = [
        ("self.omega_s = self.omega_s + tw / (4 * np.pi)", "INVERSA",
         "il finto (`tw`) scrive il vero (`omega_s`)"),
        ("x = np.angle(self._psi_spinor[:, 0])", "VERA",
         "grandezza SPINORIALE"),
        ("u = np.exp(1j * chi / 2)", "VERA",
         "MEZZO ANGOLO su un angolo"),
        ("self.phi = (self.phi + d) % (4 * np.pi)", "DICHIARATA",
         "il dominio di `phi`"),
        ("self.tw += self._w8(dph - self.twp)", "EREDITATA",
         "legge `dph`/`twp`, che prendono la scala da `phi`"),
    ]
    for src, atteso, perche in casi:
        c, regola = cls(src)
        ok = (c == atteso)
        W("K%d %-58s -> %-11s (atteso %-11s) %s\n"
          % (len(e) + 1, perche, c, atteso, "OK" if ok else "*** NO ***"))
        e.append(ok)

    # IL CASO CHE DEVE FALLIRE: senza la precedenza, un sito INVERSA passerebbe per VERA
    src = "self.omega_s = self.omega_s + tw / (4 * np.pi)"
    a = ast.parse(src)
    nomi = _nomi(a.body[0])
    finto_vera = _ha(nomi, BLOCH)      # la regola SBAGLIATA: "contiene omega_s -> VERA"
    ok = finto_vera and cls(src)[0] == "INVERSA"
    W("K%d IL CASO CHE DEVE FALLIRE: la regola senza precedenza direbbe VERA (contiene "
      "`omega_s`) -> %s\n"
      % (len(e) + 1, "OK: la precedenza INVERSA>VERA lo salva" if ok else "*** NO ***"))
    e.append(ok)

    # SECONDO CASO CHE DEVE FALLIRE: un sito senza nessuna di queste grandezze non si
    # classifica a forza -- deve uscire `?`
    c, _ = cls("y = np.sin(alpha) * 3")
    ok = (c == "?")
    W("K%d SECONDO CASO CHE DEVE FALLIRE: una riga estranea -> `%s` (atteso `?`, non una "
      "classe a forza) -> %s\n" % (len(e) + 1, c, "OK" if ok else "*** classifica a forza ***"))
    e.append(ok)

    ok = all(e)
    W("-" * 100 + "\n  -> %s\n\n" % ("le regole PASSANO" if ok else "*** NON PASSANO ***"))
    return ok


# ---------------------------------------------------------------- IL GRAFO
GRAFO = [
    ("SPINORE `psi_spinor`", "`phi`",
     "`_phc` / `phivel` / `omega_clk`: l'orologio proprio nasce dalla fase dello spinore",
     "VERA -> DICHIARATA"),
    ("`phi`", "`dph`", "`dph = _wphi(phi[i] - phi[j])` (`:4675`)", "DICHIARATA -> EREDITATA"),
    ("`dph`", "`twp`, `tw`", "`tw += _w8(dph + twist_dip - twp)` (`:4698-4699`)", "EREDITATA"),
    ("`tw`", "MITOSI", "`avv = |tw|`, soglia `PHI_CRIT + twist_max`, campana fino a `TW_TETTO`",
     "EREDITATA"),
    ("`tw`", "SCHWINGER", "`eccesso_torsione` -> `prob_coppia`, e l'antifase `fm + dphi/2`",
     "EREDITATA"),
    ("`tw`", "REPULSIONE / `d0`", "il termine di massima compressione (`S05`)", "EREDITATA"),
    ("`tw`", "TEMPI", "`ritmo()` ramo `TEMPO_SEGNO` (`r = 1 + mean|tw|/PHI_CRIT`) e `tau_pp`",
     "EREDITATA"),
    ("`phi`", "TEMPI", "`ritmo()` ramo VIVO: `signed` da `np.angle(psi_spin)`, gauge, bottleneck",
     "DICHIARATA -> EREDITATA"),
    ("`tw`", "SPINORE", "`TW_SPINORE`: `_otw` sommato a `omega_new` (`:2149-2154`)",
     "*** INVERSA ***"),
]


def main():
    W = sys.stdout.write
    if not collaudo(W):
        return 1
    testo = io.open(SORGENTE, encoding="utf-8").read()
    righe = testo.split("\n")
    albero = ast.parse(testo)
    nodi = nodo_di_riga(albero)
    punti = Z118.censisci(testo)
    eff, fonte_eff = effettivo()

    try:
        os.makedirs(os.path.dirname(OUT))
    except OSError:
        pass
    f = io.open(OUT, "w", encoding="utf-8", newline="\n")
    Wf = f.write
    Wf("# LA MAPPA DEL `4pi` -- **di chi e' la doppia copertura, punto per punto**\n\n")
    Wf("> **GENERATA** da `csv/_test_fork/_mappa_4pi.py`, che **riusa `_censimento_fasi.py`**\n")
    Wf("> (`Z118`). **Sola lettura, AST.** Stato effettivo dei flag: %s.\n\n" % fonte_eff)
    Wf("## LE QUATTRO CLASSI\n\n")
    Wf("| classe | che cos'e' | che se ne fa l'architettura a un solo ponte |\n|:--:|---|---|\n")
    Wf("| **`VERA`** | la doppia copertura **dello SPINORE**: un oggetto di spin 1/2 torna in "
       "se' dopo `4pi`. **E' fisica.** | **RESTA**, ed e' l'unico posto dove il `4pi` vive |\n")
    Wf("| **`DICHIARATA`** | il **dominio `[0, 4pi)` di `phi`**: una **convenzione del codice**, "
       "non una proprieta' misurata | **CADE**: `phi` diventa una lettura dello spinore, su "
       "`2pi` |\n")
    Wf("| **`EREDITATA`** | cio' che prende la sua **scala** da `phi` | **si RIDERIVA** dal "
       "trasporto degli spinori, non dalle differenze di `phi` |\n")
    Wf("| **`INVERSA`** | **il finto pilota il vero**: una grandezza ereditata SCRIVE una "
       "grandezza spinoriale | **si ABOLISCE**: e' il verso sbagliato del ponte |\n\n")
    Wf("**Precedenza dichiarata:** `INVERSA` > `VERA` > `DICHIARATA` > `EREDITATA`. Un sito "
       "che e' sia spinoriale sia scritto da `tw` e' **`INVERSA`**, perche' la domanda e' "
       "*dove il finto comanda il vero*.\n\n")

    conta = {}
    Wf("## I PUNTI\n\n")
    Wf("| riga | funzione | tipo | **di chi** | regola che l'ha deciso | flag | **EFFETTIVO "
       "nei run** |\n|--:|---|:--:|:--:|---|---|:--:|\n")
    for p in punti:
        c, regola = classifica(nodi.get(p["riga"]), righe, p["riga"])
        conta[c] = conta.get(c, 0) + 1
        fl = p.get("flag") or "-"
        val = "-"
        for nome in eff:
            if nome and nome in fl:
                val = str(eff[nome])
                break
        Wf("| `:%d` | `%s` | `%s` | **`%s`** | %s | %s | **%s** |\n"
           % (p["riga"], p["fn"], p["tipo"], c, regola, fl, val))
    Wf("\n**Conteggio per classe:** %s\n\n"
       % " . ".join("**%s** %d" % (k, v) for k, v in sorted(conta.items())))
    if conta.get("?"):
        Wf("> **!! `%d` punti NON CLASSIFICATI**, e restano `?`: nessuna regola ha attaccato. "
           "**Non li forzo in una classe**, perche' una classe assegnata a forza e' peggio di "
           "una cella vuota.\n\n" % conta["?"])

    Wf("## IL GRAFO DELLE DIPENDENZE\n\n")
    Wf("```\n")
    Wf("  SPINORE (4pi VERO)\n")
    Wf("      |  _phc / phivel / omega_clk\n")
    Wf("      v\n")
    Wf("    phi  (4pi DICHIARATO -- la convenzione)\n")
    Wf("      |  dph = _wphi(phi[i] - phi[j])   :4675\n")
    Wf("      v\n")
    Wf("  twp, tw  (EREDITATO)                  :4698-4699\n")
    Wf("      |                |            |              |\n")
    Wf("      v                v            v              v\n")
    Wf("   MITOSI          SCHWINGER    REPULSIONE       TEMPI\n")
    Wf("   soglia,         antifase,    max compress.    ritmo, tau_pp\n")
    Wf("   campana         prob_coppia  (S05)            d/cs\n")
    Wf("\n")
    Wf("  E IL VERSO SBAGLIATO, che l'architettura deve abolire:\n")
    Wf("    tw  ---- TW_SPINORE ---->  omega_s  (lo SPINORE)     *** INVERSA ***\n")
    Wf("```\n\n")
    Wf("| da | a | come | classe |\n|---|---|---|:--:|\n")
    for da, a, come, cl in GRAFO:
        Wf("| %s | %s | %s | `%s` |\n" % (da, a, come, cl))
    Wf("\n")
    Wf("> **⚠ COSA QUESTA MAPPA NON FA: non decide.** Dice **di chi** e' il `4pi` in ogni "
       "punto e **se quel punto gira**. La proposta e' una **scheda a parte**.\n")
    f.close()
    W("mappa scritta -> %s\n" % os.path.relpath(OUT, RADICE))
    W("conteggio per classe: %s\n"
      % " . ".join("%s %d" % (k, v) for k, v in sorted(conta.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
