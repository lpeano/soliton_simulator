# -*- coding: utf-8 -*-
"""**`G1`-`G4`: LA CARICA, L'ANTIMATERIA, E SE IL SEGNO E' UNA CONVENZIONE.**

**Mandato del guardiano del 2026-10-01**, per verificare e registrare le sue misure, e per dare la
**linea di base** dei criteri del par. `(E)` di `doc/PIANO_divisione_e_calore.md`.

### LA VISIONE DI LUCA che queste misure mettono alla prova
*(registrata in `doc/REGISTRO_FISICA.md` con la data di oggi)*
| | |
|---|---|
| **(a)** | la nascita di un nodo ha ### **TRE esiti**: **spazio**, **materia**, oppure **materia e antimateria**; ### **`peq` e' il riferimento che li separa** |
| **(b)** | ### **si conserva ESATTAMENTE solo la CARICA** *(materia contro antimateria)* |
| **(c)** | ### **l'energia GLOBALE non si conserva** *(uno spaziotempo che si espande non la conserva)*; resta il ### **bilancio LOCALE**: ogni variazione ha una **causa dichiarata** |

| | che cosa misura |
|---|---|
| **`G1`** | ### **LA CARICA**: la serie di `sum(perc_chi)`, e ### **se il segno dipende da una CONVENZIONE** — il rappresentante canonico |
| **`G2`** | ### **`D35`**: con `phi` su `4π`, `anti = phi + 2π` e il campo legge `exp(i·phi)`: ### **l'antinodo e' IDENTICO al genitore?** |
| **`G3`** | ### **`COPPIA_DENSITA`**: `peq` entra nella decisione di creare coppie? *(il legame previsto da (a))* |
| **`G4`** | ### **quanti nodi crea lo Schwinger**, e come cambia la carica totale a ogni evento |
| **`E-base`** | la ### **LINEA DI BASE** dei criteri del par. `(E)`: `K_fase` ed `E_cin` su un run **lungo**, col volume |

### ⚠ **PERCHE' `G1` E' LA PIU' IMPORTANTE, e perche' e' una domanda di CONVENZIONE**
`perc_chi` viene **riscritta a ogni passo** dal segno di
`real(sum(conj(_bloch_a_spinore(_nb)) * _psi_spinor))`. ### **Il rappresentante canonico e' una
SCELTA DI GAUGE**: moltiplicarlo per `−1` *(un giro di `2π` nella doppia copertura, che e' lo
STESSO stato fisico)* ### **ribalta TUTTE le cariche.** ### ➜ **Se la carica e' definita da una
scelta di gauge, non e' una carica: e' una convenzione** — ed e' ### **la stessa famiglia del
verso degli archi** (`MEM-HEBB-VERSO`).
### **Lo strumento lo MISURA invece di dedurlo**, e misura anche ### **quanto e' FRAGILE**: quanti
nodi hanno `real(_ov)` vicino a zero, dove un epsilon ribalta il segno.

### ⚠ I NOMI: `G1`...`G4` sono LOCALI A QUESTO FILE
Fuori si scrive ### **`DIVISIONE-AUTOCONSISTENTE:G1`** ... `:G4`, per la stessa ragione per cui le
misure `M` hanno un namespace: ### **nell'indice ci sono id che collidono con le forme nude.**

COMANDO:  python csv/_test_fork/_carica_e_coppie.py [--seme=11] [--passi=72]
USCITA:   `csv/_test_fork/_carica_e_coppie/_carica_e_coppie_s<seme>_p<passi>.json` + stdout.
"""
import contextlib
import hashlib
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)
import numpy as np  # noqa: E402
import _cli_flag  # noqa: E402
import _passo  # noqa: E402

FUORI = os.path.join(RADICE, "csv", "_test_fork", "_carica_e_coppie")
SIM = os.path.join(RADICE, "soliton_simulator.py")


def blob(percorso):
    return hashlib.sha1(io.open(percorso, "rb").read()).hexdigest()


def carica(nome, seme):
    """La scena **GRANDE** di riferimento, lo stesso caricamento del sigillo del controllo unico."""
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=%d" % seme],
                                              dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome=nome)
        S._applica_regime(a)      # il TERZO passo del percorso del CLI
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    return S, S.net


def carica_foto(net):
    """`G1`: la carica, come la rete la porta ADESSO."""
    n = int(net.n)
    pc = np.asarray(getattr(net, "perc_chi", []))[:n]
    if pc.size == 0:
        return {"n": n, "somma": None}
    return {"n": n, "somma": int(np.sum(pc)), "piu": int(np.count_nonzero(pc > 0)),
            "meno": int(np.count_nonzero(pc < 0)), "zero": int(np.count_nonzero(pc == 0))}


def g1_convenzione(S, net):
    """### **`G1`: IL SEGNO DELLA CARICA DIPENDE DA UNA SCELTA DI GAUGE?**

    Si ricalcola `perc_chi` ### **con la legge del simulatore** *(non con una mia copia)* e poi
    ### **con il rappresentante canonico moltiplicato per `−1`** — che e' lo **stesso stato
    fisico**, un giro di `2π` nella doppia copertura.
    ### ➜ **Se tutte le cariche si ribaltano, il segno e' una CONVENZIONE.**
    E si misura anche ### **la FRAGILITA'**: quanti nodi hanno `real(_ov)` cosi' vicino a zero che
    un epsilon li ribalta.
    """
    n = int(net.n)
    nb = getattr(net, "_nb", None)
    ps = getattr(net, "_psi_spinor", None)
    if nb is None or ps is None or len(nb) < n or len(ps) < n:
        return {"non_misurabile": "`_nb` o `_psi_spinor` assenti o corti"}
    canon = net._bloch_a_spinore(np.asarray(nb)[:n])
    ov = np.sum(np.conj(canon) * np.asarray(ps)[:n], axis=1)
    r = np.real(ov)
    segno = np.where(r >= 0.0, 1, -1)
    # ### IL GAUGE: `-canon` e' lo STESSO stato fisico (giro di 2 pi nella doppia copertura).
    ov_g = np.sum(np.conj(-canon) * np.asarray(ps)[:n], axis=1)
    segno_g = np.where(np.real(ov_g) >= 0.0, 1, -1)
    ribaltati = int(np.count_nonzero(segno != segno_g))
    ar = np.abs(r)
    scala = float(np.median(ar)) if ar.size else 0.0
    return {"n": n, "somma_segno": int(np.sum(segno)),
            "ribaltati_dal_gauge": ribaltati,
            "frazione_ribaltata": (ribaltati / n if n else None),
            "real_ov_mediano_assoluto": scala,
            "nodi_entro_1e-12": int(np.count_nonzero(ar < 1e-12)),
            "nodi_entro_1e-6_della_mediana": int(np.count_nonzero(ar < 1e-6 * max(scala, 1e-30))),
            "coerente_con_perc_chi": int(np.count_nonzero(
                segno == np.asarray(net.perc_chi)[:n]))}


def g2_antifase(S, net, nati):
    """### **`G2` (`D35`): per il campo, l'antinodo e' IDENTICO al genitore?**

    Il campo e' `Mw @ exp(1j*phi)`. Con `phi` su `_dphi()` e `anti = phi + _dphi()/2`, il
    contributo dell'antinodo e' `exp(i*anti)`. ### **Si misura la distanza fra i due numeri
    complessi**, su **tutti** i nodi: se e' zero a precisione di macchina, ### **l'antifase non e'
    un'antifase.**
    """
    P = float(net._dphi())
    ph = np.asarray(net.phi)[:int(net.n)].astype(float)
    a = np.exp(1j * ph)
    b = np.exp(1j * ((ph + P / 2.0) % P))
    d = np.abs(a - b)
    return {"dphi": P, "FASE_2PI": bool(getattr(S, "FASE_2PI", False)),
            "scostamento_max": float(np.max(d)) if d.size else 0.0,
            "scostamento_mediano": float(np.median(d)) if d.size else 0.0,
            "nodi": int(ph.size),
            "nati_schwinger": int(nati),
            "identico_a_precisione_di_macchina": bool(d.size and float(np.max(d)) < 1e-9)}


def principale():
    seme, passi = 11, 72
    for a in sys.argv[1:]:
        if a.startswith("--seme="):
            seme = int(a.split("=", 1)[1])
        elif a.startswith("--passi="):
            passi = int(a.split("=", 1)[1])
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    P = []

    def stampa(*x):
        r = " ".join(str(y) for y in x)
        P.append(r)
        print(r)

    stampa("=" * 104)
    stampa("G1-G4 -- LA CARICA, L'ANTIMATERIA, E SE IL SEGNO E' UNA CONVENZIONE")
    stampa("=" * 104)
    stampa("simulatore ..... %s" % blob(SIM)[:8])
    stampa("questo strumento %s" % blob(os.path.abspath(__file__))[:8])
    stampa("seme %d   passi %d" % (seme, passi))
    stampa("")

    S, net = carica("carica_s%d" % seme, seme)
    _cli_flag.dichiara_configurazione(S, stampa)
    stampa("")

    # ---------------------------------------------------------------- G3, subito
    stampa("=" * 104)
    stampa("G3 -- `peq` ENTRA NELLA DECISIONE DI CREARE COPPIE?")
    stampa("=" * 104)
    g3 = {"COPPIA_DENSITA": bool(getattr(S, "COPPIA_DENSITA", False)),
          "ANTIFASE_ADD": bool(getattr(S, "ANTIFASE_ADD", False)),
          "COPPIA_MIT": float(getattr(S, "COPPIA_MIT", float("nan")))}
    stampa("  COPPIA_DENSITA = %s   (ESPLORATIVO: lega la coppia all'anomalia di densita')"
           % g3["COPPIA_DENSITA"])
    stampa("  ANTIFASE_ADD   = %s      COPPIA_MIT = %s" % (g3["ANTIFASE_ADD"], g3["COPPIA_MIT"]))
    if not g3["COPPIA_DENSITA"]:
        stampa("  ### -> NEL SISTEMA DI RIFERIMENTO `peq` NON ENTRA nella decisione di creare")
        stampa("      coppie: IL LEGAME PREVISTO DALLA VISIONE (a) E' SPENTO.")

    # ------------------------------------------------- la SPIA: carica per VOCE
    serie = []
    eventi = []
    stato = {"passo": 0, "prec": None}
    vero = S._ferma_se_registro_incoerente

    def spia(nt, dove, voce=None, comp=None):
        f = carica_foto(nt)
        prec = stato["prec"]
        if prec is not None and f.get("somma") is not None and prec.get("somma") is not None:
            if f["somma"] != prec["somma"] or f["n"] != prec["n"]:
                eventi.append({"passo": stato["passo"], "voce": voce,
                               "n_prima": prec["n"], "n_dopo": f["n"],
                               "somma_prima": prec["somma"], "somma_dopo": f["somma"],
                               "d_n": f["n"] - prec["n"],
                               "d_somma": f["somma"] - prec["somma"]})
        stato["prec"] = f
        return vero(nt, dove, voce=voce, comp=comp)

    S._ferma_se_registro_incoerente = spia

    stampa("")
    stampa("=" * 104)
    stampa("IL RUN: %d passi, con la SPIA sui confini di voce" % passi)
    stampa("=" * 104)
    f0 = carica_foto(net)
    serie.append({"passo": 0, "carica": f0,
                  "K_fase": float(0.5 * np.sum(np.asarray(net.phivel)[:int(net.n)] ** 2)),
                  "E_cin": float(np.mean(np.asarray(net.phivel)[:int(net.n)] ** 2)),
                  "m": int(len(net.i)),
                  "somma_d": float(np.sum(np.asarray(net.d)))})
    stampa("  passo 0: n %d   sum(perc_chi) %s   (+%s / -%s)"
           % (f0["n"], f0.get("somma"), f0.get("piu"), f0.get("meno")))
    for k in range(1, passi + 1):
        stato["passo"] = k
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(S, net)
        pv = np.asarray(net.phivel)[:int(net.n)].astype(float)
        serie.append({"passo": k, "carica": carica_foto(net),
                      "K_fase": float(0.5 * np.sum(pv ** 2)),
                      "E_cin": float(np.mean(pv ** 2)),
                      "m": int(len(net.i)),
                      "somma_d": float(np.sum(np.asarray(net.d)))})
    S._ferma_se_registro_incoerente = vero

    # ---------------------------------------------------------------- G1
    stampa("")
    stampa("=" * 104)
    stampa("G1 -- LA CARICA: la serie, e se il segno e' una CONVENZIONE")
    stampa("=" * 104)
    stampa("  %6s %8s %10s %8s %8s" % ("passo", "n", "sum(chi)", "+1", "-1"))
    # ⚠ le righe NON si duplicano quando la serie e' corta: con <= 6 voci si stampa TUTTA.
    #   (La prima stesura concatenava `serie[:3]` e `serie[-3:]` sempre, e su 3 voci le ripeteva.)
    _righe = (serie if len(serie) <= 6
              else serie[:3] + [{"passo": "..."}] + serie[-3:])
    for r in _righe:
        if r.get("passo") == "...":
            stampa("  %6s" % "...")
            continue
        c = r["carica"]
        stampa("  %6s %8d %10s %8s %8s" % (r["passo"], c["n"], c.get("somma"),
                                           c.get("piu"), c.get("meno")))
    g1 = g1_convenzione(S, net)
    stampa("")
    if "non_misurabile" in g1:
        stampa("  ### G1 (convenzione) NON MISURABILE: %s" % g1["non_misurabile"])
    else:
        stampa("  ### IL SEGNO DIPENDE DAL RAPPRESENTANTE CANONICO? (gauge: canon -> -canon,")
        stampa("      che e' LO STESSO STATO FISICO, un giro di 2 pi nella doppia copertura)")
        stampa("      cariche RIBALTATE dal gauge: %d su %d   (frazione %.6f)"
               % (g1["ribaltati_dal_gauge"], g1["n"], g1["frazione_ribaltata"]))
        stampa("      la legge del simulatore e il mio ricalcolo concordano su %d nodi su %d"
               % (g1["coerente_con_perc_chi"], g1["n"]))
        stampa("      FRAGILITA': |real(_ov)| mediano %.6e; nodi sotto 1e-12: %d; nodi sotto"
               % (g1["real_ov_mediano_assoluto"], g1["nodi_entro_1e-12"]))
        stampa("      1e-6 della mediana: %d" % g1["nodi_entro_1e-6_della_mediana"])
        if g1["ribaltati_dal_gauge"] == g1["n"]:
            stampa("  ### -> TUTTE. Il segno della carica E' UNA SCELTA DI GAUGE, non una")
            stampa("      proprieta' fisica del nodo: la stessa famiglia del verso degli archi.")
        elif g1["ribaltati_dal_gauge"] == 0:
            stampa("  ### -> NESSUNA: il segno NON dipende da quella scelta.")
        else:
            stampa("  ### -> PARZIALE (%d su %d): da capire, perche' un gauge globale dovrebbe"
                   % (g1["ribaltati_dal_gauge"], g1["n"]))
            stampa("      agire su tutti o su nessuno.")

    # ---------------------------------------------------------------- G4
    stampa("")
    stampa("=" * 104)
    stampa("G4 -- QUANTI NODI CREA UN EVENTO, E COME CAMBIA LA CARICA TOTALE")
    stampa("=" * 104)
    nasc = [e for e in eventi if e["d_n"] != 0]
    stampa("  eventi con `n` cambiato: %d" % len(nasc))
    stampa("  %6s %-22s %6s %10s" % ("passo", "voce", "d_n", "d_sum(chi)"))
    for e in nasc:
        stampa("  %6d %-22s %+6d %+10d" % (e["passo"], str(e["voce"]), e["d_n"], e["d_somma"]))
    if nasc:
        neutri = [e for e in nasc if e["d_somma"] == 0]
        stampa("")
        stampa("  ### eventi che NON cambiano la carica totale: %d su %d"
               % (len(neutri), len(nasc)))
        if len(neutri) < len(nasc):
            stampa("  ### -> LA CARICA NON SI CONSERVA ALLE NASCITE. Il commento dello Schwinger")
            stampa("      dice <<la coppia e' NEUTRA e N(+1)-N(-1) NON cambia>>, ma lo Schwinger")
            stampa("      crea UN SOLO nodo (l'antinodo) accanto a un genitore CHE C'ERA GIA':")
            stampa("      la somma cambia di -perc_chi[genitore], cioe' di +-1.")
        else:
            stampa("  ### -> la carica si conserva a ogni evento misurato.")
    # ⚠ e la riscrittura per passo: la carica di nascita DURA UN SOLO PASSO
    stampa("")
    stampa("  ⚠ E LE REGOLE DI NASCITA DELLA CARICA DURANO UN SOLO PASSO: `perc_chi` viene")
    stampa("    RISCRITTA a ogni passo dal segno dell'overlap con il rappresentante canonico.")
    stampa("    Quindi <<l'antinodo nasce con chiralita' opposta>> e' vero per UN passo.")

    # ---------------------------------------------------------------- G2
    stampa("")
    stampa("=" * 104)
    stampa("G2 (D35) -- PER IL CAMPO, L'ANTINODO E' IDENTICO AL GENITORE?")
    stampa("=" * 104)
    _ns = int(getattr(net, "_g_nati_schwinger", 0))
    g2 = g2_antifase(S, net, _ns)
    stampa("  FASE_2PI = %s   _dphi() = %.6f   (2 pi = %.6f)"
           % (g2["FASE_2PI"], g2["dphi"], 2 * np.pi))
    stampa("  nati dallo Schwinger in questo run: %d" % g2["nati_schwinger"])
    stampa("  |exp(i*phi) - exp(i*(phi + dphi/2))| su %d nodi: max %.3e, mediano %.3e"
           % (g2["nodi"], g2["scostamento_max"], g2["scostamento_mediano"]))
    if g2["identico_a_precisione_di_macchina"]:
        stampa("  ### -> IDENTICO A PRECISIONE DI MACCHINA: con `phi` su 4 pi il `+2 pi` NON E'")
        stampa("      UN'ANTIFASE, e per il campo l'antiparticella E' LA PARTICELLA. E' `D35`, e")
        stampa("      il commento del codice lo diceva gia': qui e' MISURATO.")
    else:
        stampa("  ### -> NON identico: l'antifase ha un effetto sul campo.")

    # ---------------------------------------------------------------- E-base
    stampa("")
    stampa("=" * 104)
    stampa("E-base -- LA LINEA DI BASE DEI CRITERI DEL PAR. (E)")
    stampa("=" * 104)
    kf = [r["K_fase"] for r in serie]
    ec = [r["E_cin"] for r in serie]
    nn = [r["carica"]["n"] for r in serie]
    mm = [r["m"] for r in serie]
    sd = [r["somma_d"] for r in serie]
    cresce = sum(1 for i in range(1, len(kf)) if kf[i] > kf[i - 1])
    base = {"K_fase_iniziale": kf[0], "K_fase_finale": kf[-1],
            "K_fase_rapporto": (kf[-1] / kf[0]) if kf[0] else None,
            "E_cin_iniziale": ec[0], "E_cin_finale": ec[-1],
            "E_cin_rapporto": (ec[-1] / ec[0]) if ec[0] else None,
            "passi_in_cui_K_cresce": cresce, "passi": len(kf) - 1,
            "n_iniziale": nn[0], "n_finale": nn[-1],
            "m_iniziale": mm[0], "m_finale": mm[-1],
            "somma_d_iniziale": sd[0], "somma_d_finale": sd[-1],
            "somma_d_rapporto": (sd[-1] / sd[0]) if sd[0] else None}
    stampa("  K_fase  da %.6e a %.6e   (x %.3f)"
           % (base["K_fase_iniziale"], base["K_fase_finale"], base["K_fase_rapporto"] or 0.0))
    stampa("  E_cin   da %.6e a %.6e   (x %.3f)"
           % (base["E_cin_iniziale"], base["E_cin_finale"], base["E_cin_rapporto"] or 0.0))
    stampa("  K_fase cresce in %d passi su %d" % (cresce, base["passi"]))
    stampa("  VOLUME: n da %d a %d, archi da %d a %d, sum(d) da %.6e a %.6e (x %.4f)"
           % (base["n_iniziale"], base["n_finale"], base["m_iniziale"], base["m_finale"],
              base["somma_d_iniziale"], base["somma_d_finale"], base["somma_d_rapporto"] or 0.0))
    stampa("  ### -> QUESTA E' LA LINEA DI BASE: il criterio <<non esplode>> del par. (E) va")
    stampa("      scritto in modo che IL SISTEMA DI OGGI LO PASSI, oppure la crescita di `E_cin`")
    stampa("      a volume quasi fermo E' GIA' UN DIFETTO, e va registrata come tale.")

    fuori = {"blob_sim_sha1_byte": blob(SIM), "blob_strumento": blob(os.path.abspath(__file__)),
             "seme": seme, "passi": passi, "G1": g1, "G2": g2, "G3": g3,
             "G4_eventi": nasc, "E_base": base, "serie": serie}
    nome = "_carica_e_coppie_s%d_p%d" % (seme, passi)
    json.dump(fuori, io.open(os.path.join(FUORI, nome + ".json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    io.open(os.path.join(FUORI, nome + ".txt"), "w", encoding="utf-8").write(chr(10).join(P))
    stampa("")
    stampa("scritto: %s" % os.path.join(FUORI, nome + ".json"))
    return 0


if __name__ == "__main__":
    sys.exit(principale())
