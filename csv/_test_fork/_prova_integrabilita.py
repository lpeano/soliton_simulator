# -*- coding: utf-8 -*-
"""IL TEST DI INTEGRABILITA' -- **il criterio del <<NO>>**, sullo snapshot della scena.

### ⛔ **IL PUNTO, e non e' mio: il metodo <<scrivo `E` e verifico `F = -dE/dx`>> DIMOSTRA IL
### SI' MA NON IL NO.** Non trovare `E` non prova che `E` non esista.

Questo banco fa **due** test, nell'ordine:

**`(A)` IL TEST STRUTTURALE** -- *e viene PRIMA, perche' senza di lui il `(B)` mente.*
Una legge che scrive `x` ma **NON legge `x`** ha `dF/dx = 0`, che e' **simmetrica**: il `(B)`
la promuoverebbe a traducibile. ### **E' un FALSO-ZERO.** Il `(A)` lo prende: una forza il cui
spazio d'ingresso **non e'** lo spazio d'uscita **non e' il gradiente di nessuna `E(x)`**.

**`(B)` IL TEST DI INTEGRABILITA' NUMERICO** -- *per le leggi che passano il `(A)`.*
`J_ij = dF_i/dx_j` per differenze finite centrali su un campione di nodi **e dei loro vicini**,
e `||J - J^T|| / ||J||` contro il **PAVIMENTO CALCOLATO** -- non contro una costante.

| | |
|---|---|
| **controllo positivo** | la **coppia SCALARE**, gradiente noto: deve risultare **simmetrica** |
| ### ⛔ **caso che DEVE fallire `(A)`** | la **coppia del DRIVER**: legge lo **spinore**, scrive su `phi` |
| ### ⛔ **caso che DEVE fallire `(B)`** | una legge **sintetica NON conservativa** -- la stessa coppia con un **prefattore di nodo**: `F_i = c_i * somma_j A_ij sin(phi_j - phi_i)`. ### **Serve a provare che il banco DISCRIMINA**, non solo che approva |

Gira con:  python csv/_test_fork/_prova_integrabilita.py
"""
import contextlib
import io
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(os.path.dirname(_QUI))
sys.path.insert(0, os.path.join(RADICE, "csv"))
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)
import _cli_flag                                             # noqa: E402
import _passo                                                # noqa: E402
import _mitosi_soglia_grad as _MSG                           # noqa: E402

SIM = os.path.join(RADICE, "soliton_simulator.py")
BLOB_ATTESO = "b8c21049"
FUORI = os.path.join(_QUI, "_prova_integrabilita")
NL = chr(10)
P = []

N_CAMPIONE = 3           # ### i nodi di base; si prendono ANCHE I LORO VICINI
TETTO_CAMPIONE = 40      # ### ⚠ IL TETTO: su questo grafo (12802 nodi, 471564 archi) 12 nodi
#                        # ### di base portano 11049 vicini, cioe' una jacobiana 11049^2 e
#                        # ### 22098 valutazioni per ogni h. ### **La restrizione e' LECITA:
#                        # ### una J simmetrica ha TUTTE le sottomatrici principali
#                        # ### simmetriche**, quindi un <<asimmetrica>> sul campione e' un no
#                        # ### sul tutto, e un <<simmetrica>> e' un si' SUL CAMPIONE.
PASSI_PRIMA = 3          # ### lo snapshot: pochi passi, come il mandato chiede
SEME_CAMPIONE = 11


def stampa(s=""):
    P.append(s)
    print(s, flush=True)


def riga(c="-", n=104):
    stampa(c * n)


# ==========================================================================
#   IL PAVIMENTO, CALCOLATO -- mai una costante (A3c)
# ==========================================================================
def pavimento(J, h, scala_F):
    """### Il pavimento numerico della simmetria di `J`.

    Due sorgenti, **sommate**, e nessuna delle due e' una costante scelta:
      * il **troncamento** della differenza centrale: `O(h^2)` sulla terza derivata, che si
        stima con la scala di `F` stessa;
      * l'**arrotondamento**: `eps * scala_F / h`, che e' l'errore di `F` diviso per `h`.
    """
    eps = float(np.finfo(float).eps)
    arrotondamento = eps * scala_F / h
    troncamento = (h ** 2) * scala_F
    return float(arrotondamento + troncamento)


def jacobiana(F, x, idx, h):
    """### `J[a, b] = dF_{idx[a]} / dx_{idx[b]}` per differenze CENTRALI."""
    m = len(idx)
    J = np.zeros((m, m))
    for b in range(m):
        xp = x.copy(); xp[idx[b]] += h
        xm = x.copy(); xm[idx[b]] -= h
        J[:, b] = (np.asarray(F(xp))[idx] - np.asarray(F(xm))[idx]) / (2.0 * h)
    return J


def asimmetria(J):
    nj = float(np.linalg.norm(J))
    if nj <= 0:
        return 0.0, 0.0
    return float(np.linalg.norm(J - J.T) / nj), nj


# ==========================================================================
#   LA SCENA, E LE LEGGI ISOLATE
# ==========================================================================
def campione(net, quanti=N_CAMPIONE, seme=SEME_CAMPIONE):
    """### Un campione di nodi **E DEI LORO VICINI**: senza i vicini la jacobiana e'
    diagonale per costruzione, e il test non proverebbe niente."""
    rng = np.random.default_rng(seme)
    gradi = np.zeros(net.n, dtype=int)
    np.add.at(gradi, net.i, 1)
    np.add.at(gradi, net.j, 1)
    vivi = np.flatnonzero(gradi > 0)
    base = rng.choice(vivi, size=min(quanti, len(vivi)), replace=False)
    dentro = set(int(k) for k in base)
    for a, b in zip(net.i, net.j):
        if int(a) in dentro or int(b) in dentro:
            dentro.add(int(a)); dentro.add(int(b))
            if len(dentro) >= TETTO_CAMPIONE:
                break
    # ### i nodi di base restano DENTRO, sempre: sono quelli di cui i vicini ci sono
    dentro |= set(int(k) for k in base)
    return np.array(sorted(dentro), dtype=int)


def main():
    os.makedirs(FUORI, exist_ok=True)
    b = _MSG.blob(SIM)
    riga("=")
    stampa("IL TEST DI INTEGRABILITA' -- il criterio del <<NO>>")
    riga("=")
    stampa("  simulatore %s   atteso %s" % (b[:8], BLOB_ATTESO))
    if not b.startswith(BLOB_ATTESO):
        raise SystemExit("[FERMO] il blob del simulatore NON e' quello atteso.")
    with contextlib.redirect_stdout(io.StringIO()):
        S, net, _a = _MSG.carica("integr", SIM)
    _cli_flag.dichiara_configurazione(S, stampa)
    stampa("  scena: n = %d, archi = %d, DT = %r" % (net.n, len(net.i), S.DT))
    # ### ⛔ **`net.step()` NON E' UN PASSO, e il presidio `H-P3` me l'ha preso:** senza
    # ### `passo_pieno` non girano `scuoti_vuoto`, `rilassa_disegno` ne' la memoria
    # ### hebbiana, cioe' lo snapshot NON sarebbe sulla traiettoria del driver.
    with contextlib.redirect_stdout(io.StringIO()):
        for _ in range(PASSI_PRIMA):
            _passo.passo_pieno(S, net)
    stampa("  snapshot dopo %d passi PIENI (`_passo.passo_pieno`, non `net.step()`)"
           % PASSI_PRIMA)

    idx = campione(net)
    stampa("  campione: %d nodi di base -> %d col loro vicinato"
           % (N_CAMPIONE, len(idx)))

    # ------------------------------------------------ gli ingredienti, DAL CODICE
    n = net.n
    w = net.peso() if hasattr(net, "peso") else None
    A = None
    for nome in ("_kernel_A", "_A_corrente"):
        if hasattr(net, nome):
            A = getattr(net, nome)
    if A is None:
        # ### `A = w * cos(phi0_i - phi0_j)` -- la forma del simulatore (`:7566` di questo
        # ### blob). Si RICOSTRUISCE qui perche' lo `step` non la espone, e si DICHIARA.
        wv = net.w if hasattr(net, "w") else np.ones(len(net.i))
        A = wv * np.cos(net.phi0[net.i] - net.phi0[net.j])
    A = np.asarray(A, dtype=float)
    stampa("  A: %d archi, |A| medio %.6g  (A = w*cos(phi0_i - phi0_j), ricostruita e "
           "DICHIARATA)" % (len(A), float(np.mean(np.abs(A)))))

    KC = float(S.K_C)
    ii, jj = net.i, net.j

    def coppia_scalare(phi):
        """### IL CONTROLLO POSITIVO: `K_C * Im(conj(z) (mat(A) @ z))` con `z = e^{i phi}`,
        cioe' il ramo scalare del simulatore, scritto nei soli archi."""
        s = KC * A * np.sin(phi[jj] - phi[ii])
        f = np.zeros(n)
        np.add.at(f, ii, s)
        np.add.at(f, jj, -s)
        return f

    rng = np.random.default_rng(7)
    c_nodo = 1.0 + 0.5 * rng.random(n)

    def coppia_asimmetrica(phi):
        """### ⛔ IL CASO CHE DEVE FALLIRE `(B)`: la stessa coppia con un PREFATTORE DI
        NODO. ### **Non e' una legge del simulatore: e' un controllo che DEVE risultare
        asimmetrico**, e serve a provare che il banco discrimina."""
        s = KC * A * np.sin(phi[jj] - phi[ii])
        f = np.zeros(n)
        np.add.at(f, ii, c_nodo[ii] * s)
        np.add.at(f, jj, -c_nodo[jj] * s)
        return f

    def coppia_driver(phi):
        """### ⛔ IL CASO CHE DEVE FALLIRE `(A)`: la coppia del driver.

        Si chiama ### **la funzione VERA del simulatore**, con `phi` messa nello stato.
        """
        # ### ⚠ **`_bloch_ritardato` SCRIVE `self._nb_ret`: la funzione HA MEMORIA.**
        # ### Senza salvare e rimettere `_nb_ret` due chiamate con la STESSA `phi` danno
        # ### numeri diversi, e il test strutturale leggerebbe quella deriva come
        # ### <<la legge dipende da phi>>: un FALSO-UNO. ### **Preso dal banco stesso.**
        vecchia = net.phi.copy()
        ret = getattr(net, "_nb_ret", None)
        ret = None if ret is None else np.array(ret, copy=True)
        try:
            net.phi[:n] = phi
            z = np.exp(1j * net.phi[:n])
            return np.asarray(net._coppia_interferenza(A, z), dtype=float)
        finally:
            net.phi[:] = vecchia
            if ret is not None:
                net._nb_ret[...] = ret

    def sincronizzazione(phi):
        """### La sincronizzazione: `forza * sin(media - phi)` con
        `media = angle(wI @ e^{i phi})`. ### **Legge `phi` e scrive su `phi`**, quindi passa
        il `(A)` e il `(B)` la puo' misurare."""
        vecchia = net.phi.copy()
        try:
            net.phi[:n] = phi
            wv = net.w if hasattr(net, "w") else np.ones(len(ii))
            wI = net._mat(wv)
            zc = wI @ np.exp(1j * phi)
            media = np.angle(zc)
            psi_s = np.abs(net.calcola_psi(wv))[:n] ** 2
            cmv = (net.pos[:n] * psi_s[:, None]).sum(0) / max(psi_s.sum(), 1e-9)
            r_cm = np.linalg.norm(net.pos[:n] - cmv, axis=1) + S.LAM * 0.5
            pozzo = psi_s.sum() / r_cm
            uno = np.maximum(wI @ np.ones(n), 1e-9)
            prof = pozzo / np.maximum(wI @ pozzo / uno, 1e-9)
            return (2.0 / np.pi) * prof * np.sin(media - phi)
        finally:
            net.phi[:] = vecchia

    LEGGI = [
        ("coppia SCALARE", coppia_scalare, "phi", "CONTROLLO POSITIVO: deve essere SIMMETRICA"),
        ("coppia del DRIVER", coppia_driver, "phi",
         "CASO CHE DEVE FALLIRE: legge lo SPINORE, scrive su phi"),
        ("sincronizzazione", sincronizzazione, "phi", "da classificare"),
        ("coppia ASIMMETRICA (sintetica)", coppia_asimmetrica, "phi",
         "CASO CHE DEVE FALLIRE (B): prova che il banco DISCRIMINA"),
    ]

    phi0 = np.array(net.phi[:n], dtype=float)
    esiti = []
    riga("=")
    stampa("(A) IL TEST STRUTTURALE -- la legge LEGGE la variabile che SCRIVE?")
    riga("=")
    for nome, F, var, nota in LEGGI:
        # ### IL CONTROLLO DI RIPETIBILITA', E VIENE PRIMA DI TUTTO: si chiama `F` DUE VOLTE
        # ### con la STESSA `phi`. ### ⛔ **Se i due valori differiscono, la funzione HA
        # ### MEMORIA e nessuna derivata ha senso** -- la deriva si leggerebbe come
        # ### sensibilita'. ### **E' il difetto che `_bloch_ritardato` ha fatto emergere.**
        f0 = np.asarray(F(phi0), dtype=float)
        fbis = np.asarray(F(phi0), dtype=float)
        scala = float(np.max(np.abs(f0))) or 1.0
        deriva = float(np.max(np.abs(fbis - f0))) / scala
        if deriva > 1e-14:
            stampa("  %-32s  ### RIPETIBILITA' ROTTA: due chiamate con la STESSA phi "
                   "differiscono di %.3e -- la funzione HA MEMORIA, e nessuna derivata ha "
                   "senso" % (nome, deriva))
            esiti.append({"legge": nome, "variabile": var, "nota": nota,
                          "ripetibile": False, "deriva": deriva, "A_passa": None})
            continue
        pp = phi0.copy()
        pp[idx] += 1e-3
        df = float(np.max(np.abs(np.asarray(F(pp), dtype=float) - f0))) / scala
        legge_se_stessa = df > 1e-10
        stampa("  %-32s  dF/F perturbando %s: %.3e   ->  %s"
               % (nome, var, df, "LEGGE x" if legge_se_stessa else "### NON LEGGE x"))
        esiti.append({"legge": nome, "variabile": var, "nota": nota,
                      "ripetibile": True, "deriva": deriva,
                      "A_sensibilita": df, "A_passa": bool(legge_se_stessa)})

    riga("=")
    stampa("(B) IL TEST DI INTEGRABILITA' -- ||J - J^T|| / ||J|| contro il PAVIMENTO CALCOLATO")
    riga("=")
    per_nome = {e["legge"]: e for e in esiti}
    for nome, F, var, nota in LEGGI:
        e = per_nome[nome]
        if not e.get("ripetibile", True):
            stampa("  %-32s  ### NON SI MISURA: la ripetibilita' e' rotta (memoria)." % nome)
            e.update({"B_fatto": False, "asimmetria": None, "pavimento": None,
                      "verdetto": "NON MISURABILE: la funzione ha MEMORIA"})
            continue
        if not e["A_passa"]:
            stampa("  %-32s  ### NON SI MISURA: ha gia' fallito il (A). Misurarla darebbe "
                   "J = 0, che e' SIMMETRICA -- un FALSO-ZERO." % nome)
            e.update({"B_fatto": False, "asimmetria": None, "pavimento": None,
                      "verdetto": "NON TRADUCIBILE in quelle variabili (test A)"})
            continue
        f0 = np.asarray(F(phi0), dtype=float)
        scala = float(np.max(np.abs(f0))) or 1.0
        fila = []
        for h in (1e-4, 1e-5, 1e-6):
            J = jacobiana(F, phi0, idx, h)
            a, nj = asimmetria(J)
            pav = pavimento(J, h, scala)
            fila.append({"h": h, "asimmetria": a, "norma_J": nj, "pavimento": pav})
            stampa("  %-32s  h %.0e   asimmetria %.6e   pavimento %.6e   %s"
                   % (nome, h, a, pav, "SIMMETRICA" if a <= pav else "### ASIMMETRICA"))
        # ### il verdetto si prende sul `h` col pavimento PIU' BASSO fra quelli provati
        b_ = min(fila, key=lambda r: r["pavimento"])
        simm = b_["asimmetria"] <= b_["pavimento"]
        e.update({"B_fatto": True, "fila": fila, "asimmetria": b_["asimmetria"],
                  "pavimento": b_["pavimento"],
                  "verdetto": "una E ESISTE (localmente, in quelle variabili)" if simm
                  else "NON ESISTE una E in quelle variabili -- un <<no>> DIMOSTRATO"})
        stampa("      ### -> %s" % e["verdetto"])

    # ------------------------------------------------ i due controlli del banco
    riga("=")
    stampa("I CONTROLLI DEL BANCO")
    riga("=")
    pos = per_nome["coppia SCALARE"]
    neg_a = per_nome["coppia del DRIVER"]
    neg_b = [e for e in esiti if "ASIMMETRICA" in e["legge"]][0]
    ok1 = pos.get("B_fatto") and pos["asimmetria"] <= pos["pavimento"]
    # ### il caso che DEVE fallire passa se la coppia del driver NON risulta traducibile:
    # ### per il (A), per la ripetibilita' o per il (B). ### **Quale dei tre, si DICE.**
    ok2 = (not neg_a.get("ripetibile", True)) or (not neg_a.get("A_passa")) or (
        neg_a.get("B_fatto") and neg_a["asimmetria"] > neg_a["pavimento"])
    ok3 = neg_b["B_fatto"] and neg_b["asimmetria"] > neg_b["pavimento"]
    stampa("  controllo POSITIVO (coppia scalare simmetrica):            %s"
           % ("PASSA" if ok1 else "### FALLISCE"))
    stampa("  caso che DEVE fallire   (coppia del driver NON traducibile): %s   -- per: %s"
           % ("PASSA" if ok2 else "### FALLISCE", neg_a.get("verdetto", "?")))
    stampa("  caso che DEVE fallire (B) (coppia sintetica asimmetrica):   %s"
           % ("PASSA" if ok3 else "### FALLISCE"))
    tutti = ok1 and ok2 and ok3
    stampa()
    stampa("  ### IL BANCO: %s" % ("SANO -- i verdetti si possono leggere" if tutti
                                   else "### ROTTO -- i verdetti NON si leggono"))

    io.open(os.path.join(FUORI, "integrabilita.json"), "w", encoding="utf-8").write(
        json.dumps({"blob": b, "n": int(n), "archi": int(len(ii)),
                    "passi_snapshot": PASSI_PRIMA, "campione": int(len(idx)),
                    "controlli": {"positivo": bool(ok1), "deve_fallire_A": bool(ok2),
                                  "deve_fallire_B": bool(ok3), "banco_sano": bool(tutti)},
                    "esiti": esiti}, ensure_ascii=False, default=str))
    io.open(os.path.join(FUORI, "integrabilita.txt"), "w", encoding="utf-8").write(
        NL.join(P) + NL)
    stampa()
    stampa("scritto %s" % os.path.join(FUORI, "integrabilita.json"))
    return 0 if tutti else 1


if __name__ == "__main__":
    sys.exit(main())
