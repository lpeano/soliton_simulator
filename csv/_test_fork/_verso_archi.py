# -*- coding: utf-8 -*-
"""**`M2`: IL VERSO DELL'ARCO ENTRA NELLA FISICA? La prova dello specchio su `(i, j)`.**

**Mandato del guardiano del 2026-10-01.** Vale per **due** voci insieme —
### **`DIVISIONE-AUTOCONSISTENTE`** e ### **`GEOM-SENZA-VERSO`** — e si misura **una volta sola**.

### IL SOSPETTO, e nasce da una lettura del codice
Nel ramo che gira, il calcio della mitosi da' al genitore `a` ### **`+chi_a`** e al genitore `b`
### **`−chi_b`**. Scambiando le etichette ### **si inverte il verso del calcio del nodo che era
`b`.** Ma *«`a`»* e *«`b`»* vengono ### **SOLO dall'ordine di memorizzazione dell'arco `(i, j)`**:
se l'arco non ha un **verso fisico dichiarato**, ### **e' un'orientazione ARBITRARIA che entra
nella FISICA.**

### LA PROVA
1. si costruisce la scena di riferimento **due volte, identiche**;
2. su una si **invertono `(i, j) -> (j, i)` per TUTTI gli archi**, e ### **`tw` cambia segno** —
   perche' se `tw` e' un avvolgimento **orientato**, invertire il verso dell'arco **deve**
   invertirne il segno. ### **Questa e' la parte che il mandato chiama <<coerentemente>>**, ed e'
   anche ### **un'IPOTESI CHE LA MISURA PUO' SMENTIRE**: se `tw` non fosse orientato, la
   trasformazione giusta sarebbe un'altra, e il referto lo dice;
3. si fa ### **UN PASSO PIENO** su entrambe;
4. si confrontano le grandezze ### **PER NODO** *(invarianti per rinumerazione degli archi)* e
   le grandezze **per arco** ### **riportate al verso originale**.

### ⚠ **PERCHE' SI GUARDANO I NODI, e non gli archi**
Invertire `(i, j)` ### **NON rinumera gli archi** *(l'arco `k` resta il `k`-esimo)*, quindi un
confronto per arco e' legittimo — ### **ma solo se si sa come ogni grandezza d'arco si
trasforma**: `d`, `d0`, `vd`, `peq` sono ### **simmetriche** *(una lunghezza non ha verso)*, `tw`
e `twp` ### **devono cambiare segno.** ### **Le grandezze PER NODO non si trasformano affatto**, e
sono quindi il confronto ### **che non dipende da nessuna mia convenzione.**
### ➜ **Il verdetto si legge SUI NODI.** Gli archi si riportano e si mostrano, come controllo.

### ⚠ **I NOMI DELLE MISURE: la forma corta `M0`…`M6` e' LOCALE A QUESTO FILE**
Nell'indice ### **`M1`, `M2`, `M3`, `M4` ESISTONO GIA'**, e `M2` e' *«LA MITOSI — ① il figlio
nasce nel PUNTO MEDIO»*, cioe' ### **lo stesso argomento**: la forma nuda ### **risolverebbe al
difetto sbagliato.** ### **Fuori da qui si scrive `DIVISIONE-AUTOCONSISTENTE:M0` … `:M6`.**

COMANDO:  python csv/_test_fork/_verso_archi.py [--passi=1]
USCITA:   `csv/_test_fork/_verso_archi/_verso_archi.json` + stdout.
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

FUORI = os.path.join(RADICE, "csv", "_test_fork", "_verso_archi")
SIM = os.path.join(RADICE, "soliton_simulator.py")

# le grandezze PER NODO: il verdetto si legge QUI. Non si trasformano invertendo `(i, j)`.
PER_NODO = ("phi", "phi0", "phi_s", "phivel", "psi", "psi_spin", "eta", "pos", "perc_tw",
            "perc_chi", "perc_geom", "mem_mot", "omega_s", "rho_spin", "_nb", "_psi_spinor")
# le grandezze PER ARCO, con la loro trasformazione DICHIARATA sotto `(i,j) -> (j,i)`.
PER_ARCO_SIMMETRICHE = ("d", "d0", "vd", "peq", "_rep")
PER_ARCO_ANTISIMMETRICHE = ("tw", "twp")


def blob(percorso):
    return hashlib.sha1(io.open(percorso, "rb").read()).hexdigest()


def carica(nome):
    """La scena **GRANDE** di riferimento, lo stesso caricamento del sigillo."""
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                              dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome=nome)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    return S, S.net


def specchia(net):
    """**Inverte `(i, j) -> (j, i)` per TUTTI gli archi, e cambia segno a `tw` e `twp`.**

    ### ⚠ **E NON TOCCA NIENT'ALTRO, di proposito:** se il sistema fosse indifferente al verso,
    ### **questa sola trasformazione dovrebbe bastare** — e se non basta, la misura dice **quanto**
    non basta.
    """
    i = np.asarray(net.i).copy()
    j = np.asarray(net.j).copy()
    net.i, net.j = j, i
    for nome in PER_ARCO_ANTISIMMETRICHE:
        v = getattr(net, nome, None)
        if v is not None and len(np.asarray(v)):
            setattr(net, nome, -np.asarray(v).copy())
    return {"archi_invertiti": int(len(i)),
            "antisimmetriche_cambiate_di_segno": list(PER_ARCO_ANTISIMMETRICHE)}


def confronta(a, b, nomi, segno=1.0):
    """Le differenze fra due reti su un elenco di grandezze. `segno = -1` per le antisimmetriche.

    ### ⛔ **DUE DIFETTI MIEI, curati il 2026-10-01, e li ha trovati IL CONTROLLO ZERO di questo
    stesso strumento** *(che percio' ha fatto il suo lavoro: ha RIFIUTATO la misura)*.

    | | |
    |---|---|
    | ### **<<assente in UNO dei due>>** | la condizione era `x is None or y is None`, che e' vera anche quando ### **mancano a ENTRAMBI** — e cache pigre come `psi_spin`, `rho_spin`, `_nb` ### **non esistono prima del primo passo**, in nessuna delle due reti. ### **Assente in entrambi non e' una differenza: e' uno STATO COERENTE** |
    | ### **i NON FINITI** | `eta` contiene `inf` *(misurati 12802)*, e ### **`inf − inf` da' `NaN`**, che non e' mai `== 0`: la grandezza risultava **DIVERSA** senza che un solo elemento differisse. ### **E' la stessa trappola di `nan_to_num` dopo la sottrazione**, gia' incontrata in questa sessione |

    ### ➜ **La cura: si confrontano gli ELEMENTI, non la distanza.** `x == y` tratta `inf == inf`
    come uguale e `+inf` contro `−inf` come diverso *(che e' giusto)*, e ### **`NaN` contro `NaN` si
    dichiara UGUALE** — perche' qui la domanda e' *«e' lo stesso stato?»*, non *«quanto distano?»*.
    La **distanza** si calcola **solo sugli elementi finiti**, e i non finiti ### **si CONTANO e si
    riportano** invece di inquinare il massimo.
    """
    fuori = []
    for nome in nomi:
        x = getattr(a, nome, None)
        y = getattr(b, nome, None)
        if x is None and y is None:
            # ### assente in ENTRAMBI: non e' una differenza, e' uno stato coerente.
            fuori.append({"grandezza": nome, "esito": "ASSENTE IN ENTRAMBI",
                          "elementi_diversi": 0})
            continue
        if x is None or y is None:
            fuori.append({"grandezza": nome, "esito": "ASSENTE IN UNO SOLO",
                          "dove": ("a" if x is None else "b")})
            continue
        x = np.asarray(x)
        y = np.asarray(y) * segno
        if x.shape != y.shape:
            fuori.append({"grandezza": nome, "esito": "FORMA DIVERSA",
                          "forma_a": list(x.shape), "forma_b": list(y.shape)})
            continue
        with np.errstate(invalid="ignore", over="ignore"):
            if np.iscomplexobj(x) or np.iscomplexobj(y):
                xx = x.astype(complex)
                yy = y.astype(complex)
            else:
                xx = x.astype(float)
                yy = y.astype(float)
            # ### UGUAGLIANZA ELEMENTO PER ELEMENTO, con `NaN` contro `NaN` dichiarato UGUALE.
            uguali = (xx == yy) | (np.isnan(xx) & np.isnan(yy))
            diversi = ~uguali
            quante = int(np.count_nonzero(diversi))
            # la DISTANZA si misura SOLO dove entrambi sono finiti: altrove non ha senso.
            finiti = np.isfinite(xx) & np.isfinite(yy)
            d = np.abs(xx - yy)
            dfin = d[finiti & diversi]
            dm = float(np.max(dfin)) if dfin.size else 0.0
            base = np.abs(xx[np.isfinite(xx)])
            scala = max(float(np.max(base)) if base.size else 0.0, 1e-30)
            non_finiti = int(np.count_nonzero(~finiti))
            diversi_non_finiti = int(np.count_nonzero(diversi & ~finiti))
        fuori.append({"grandezza": nome, "esito": ("IDENTICA" if quante == 0 else "DIVERSA"),
                      "scostamento_max_sui_finiti": dm,
                      "scostamento_relativo": dm / scala,
                      "elementi_diversi": quante, "elementi": int(d.size),
                      "elementi_non_finiti": non_finiti,
                      "elementi_diversi_non_finiti": diversi_non_finiti})
    return fuori


def principale():
    passi = 1
    for a in sys.argv[1:]:
        if a.startswith("--passi="):
            passi = int(a.split("=", 1)[1])
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    P = []

    def stampa(*x):
        r = " ".join(str(y) for y in x)
        P.append(r)
        print(r)

    stampa("=" * 104)
    stampa("M2 -- IL VERSO DELL'ARCO ENTRA NELLA FISICA? La prova dello specchio su `(i, j)`")
    stampa("=" * 104)
    stampa("simulatore ..... %s" % blob(SIM)[:8])
    stampa("questo strumento %s" % blob(os.path.abspath(__file__))[:8])
    stampa("passi .......... %d" % passi)
    stampa("")

    SA, A = carica("verso_base")
    SB, B = carica("verso_specchio")
    _cli_flag.dichiara_configurazione(SA, stampa)
    stampa("")

    # --- le due scene partono IDENTICHE, e si VERIFICA invece di crederlo
    pari = confronta(A, B, PER_NODO)
    # ### <<ASSENTE IN ENTRAMBI>> E' COERENTE e non fa fallire il controllo zero: le cache
    #   pigre (`psi_spin`, `rho_spin`, `_nb`) NON ESISTONO prima del primo passo, in nessuna
    #   delle due reti. ### Cio' che fa fallire e' <<assente in UNO SOLO>> o <<DIVERSA>>.
    diverse_subito = [x for x in pari
                      if x.get("esito") not in ("IDENTICA", "ASSENTE IN ENTRAMBI")]
    stampa("CONTROLLO ZERO: le due scene partono identiche?")
    stampa("  grandezze per nodo confrontate: %d   DIVERSE: %d"
           % (len(pari), len(diverse_subito)))
    if diverse_subito:
        for x in diverse_subito:
            stampa("      ### %s: %s" % (x["grandezza"], x.get("esito")))
        stampa("  ### LA MISURA NON SI PUO' FARE: le due scene non partono uguali.")
        return 1
    stampa("  -> IDENTICHE. La misura e' lecita.")

    info = specchia(B)
    stampa("")
    stampa("SPECCHIO applicato a B: %d archi invertiti, segno cambiato a %s"
           % (info["archi_invertiti"], ", ".join(info["antisimmetriche_cambiate_di_segno"])))

    # ⚠ lo specchio e' una SCRITTURA FUORI DAL PASSO: il controllo del registro del commit 1
    #   verifica le FORME, e le forme non cambiano. Si dichiara comunque che la scrittura c'e'.
    stampa("  (scrittura FUORI dal passo: le forme non cambiano, quindi il controllo del")
    stampa("   registro non ha nulla da dire -- e lo si dichiara invece di tacerlo.)")

    for k in range(passi):
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(SA, A)
            _passo.passo_pieno(SB, B)

    stampa("")
    stampa("=" * 104)
    stampa("IL VERDETTO SI LEGGE SUI NODI (invarianti per la trasformazione)")
    stampa("=" * 104)
    nodi = confronta(A, B, PER_NODO)
    nd = [x for x in nodi if x.get("esito") == "DIVERSA"]
    stampa("  %-16s %-19s %14s %14s %12s" % ("grandezza", "esito", "scost.max fin.", "relativo",
                                             "elem. div."))
    for x in nodi:
        stampa("  %-16s %-19s %14.4e %14.4e %12s"
               % (x["grandezza"], x.get("esito", "?"), x.get("scostamento_max_sui_finiti", 0.0),
                  x.get("scostamento_relativo", 0.0), x.get("elementi_diversi", "-")))
    stampa("")
    stampa("  ### GRANDEZZE PER NODO DIVERSE: %d su %d" % (len(nd), len(nodi)))
    if nd:
        stampa("  ### ➜ IL VERSO DELL'ARCO ENTRA NELLA FISICA. La simulazione cambia, e non per")
        stampa("        una rinumerazione: le grandezze per NODO non si trasformano affatto.")
    else:
        stampa("  ### ➜ IL VERSO DELL'ARCO NON ENTRA NELLA FISICA, su questa trasformazione e")
        stampa("        su questo numero di passi. (NON prova che non entri MAI: prova che")
        stampa("         questa inversione, con tw antisimmetrica, non si vede sui nodi.)")

    stampa("")
    stampa("=" * 104)
    stampa("CONTROLLO sugli ARCHI, con la trasformazione DICHIARATA per ciascuna")
    stampa("=" * 104)
    sim = confronta(A, B, PER_ARCO_SIMMETRICHE, segno=1.0)
    anti = confronta(A, B, PER_ARCO_ANTISIMMETRICHE, segno=-1.0)
    for et, gruppo in (("SIMMETRICHE (nessun segno)", sim),
                       ("ANTISIMMETRICHE (riportate con -1)", anti)):
        stampa("  %s:" % et)
        for x in gruppo:
            stampa("      %-8s %-19s scost.max(fin) %12.4e  relativo %12.4e  elem.div %s"
                   % (x["grandezza"], x.get("esito", "?"), x.get("scostamento_max_sui_finiti", 0.0),
                      x.get("scostamento_relativo", 0.0), x.get("elementi_diversi", "-")))

    # --- e il primo sospetto, nominato: il calcio della mitosi
    stampa("")
    stampa("=" * 104)
    stampa("DOVE: il primo sospetto e' il CALCIO DELLA MITOSI, e si dice se ha agito")
    stampa("=" * 104)
    for et, nt in (("BASE", A), ("SPECCHIO", B)):
        stampa("  %-9s nati mitosi %s   nati Schwinger %s   n = %d"
               % (et, getattr(nt, "_g_nati_mitosi", 0), getattr(nt, "_g_nati_schwinger", 0),
                  int(nt.n)))
    stampa("  ⚠ Se in questi passi NON ci sono nascite, il calcio della mitosi NON HA AGITO:")
    stampa("    allora una differenza sui nodi viene da ALTRO, e il referto non puo' attribuirla")
    stampa("    al calcio. ### Il primo sospetto non e' l'unico, e questa riga lo tiene onesto.")

    fuori = {"blob_sim_sha1_byte": blob(SIM), "blob_strumento": blob(os.path.abspath(__file__)),
             "passi": passi, "specchio": info,
             "controllo_zero_diverse": diverse_subito,
             "per_nodo": nodi, "per_nodo_diverse": [x["grandezza"] for x in nd],
             "per_arco_simmetriche": sim, "per_arco_antisimmetriche": anti,
             "nascite": {"base": {c: int(getattr(A, c, 0)) for c in
                                  ("_g_nati_mitosi", "_g_nati_schwinger")},
                         "specchio": {c: int(getattr(B, c, 0)) for c in
                                      ("_g_nati_mitosi", "_g_nati_schwinger")}},
             "verdetto_il_verso_entra_nella_fisica": bool(nd)}
    json.dump(fuori, io.open(os.path.join(FUORI, "_verso_archi.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8").write(chr(10).join(P))
    stampa("")
    stampa("scritto: %s" % os.path.join(FUORI, "_verso_archi.json"))
    return 0


if __name__ == "__main__":
    sys.exit(principale())
