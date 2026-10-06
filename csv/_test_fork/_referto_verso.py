# -*- coding: utf-8 -*-
"""GENERA `doc/REFERTO_verso_e_plaquette_2026-10-06.md` dai due json di `M1`-`M4`.

### ⛔ **NESSUN NUMERO E' RICOPIATO A MANO** *(`L-NUMERI`)*: tutto esce dai json, comprese
le soglie e i criteri, che i due strumenti salvano insieme ai dati.

### ⛔ **E NESSUNA RACCOMANDAZIONE NUOVA, perche' il mandato lo vieta:** *«questa misura NON
sceglie un'opzione. Riporta i numeri e l'unica affermazione permessa e' descrittiva.»*
### **Le raccomandazioni restano quelle di `doc/GEOM_SENZA_VERSO.md`**, e questo referto
### **non ne aggiunge e non ne ritira nessuna.**

### ⚠ **E SI RIFIUTA DI SCRIVERE SE UNA CORSA NON E' COMPLETA**, dicendo ### **quale.**
"""
import io
import json
import os
import sys

from scipy.stats import norm as _norm

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
sys.path.insert(0, _QUI)
import _presidio   # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
J_V = os.path.join(RADICE, "csv", "_test_fork", "_misura_verso", "verso.json")
J_P = os.path.join(RADICE, "csv", "_test_fork", "_misura_plaquette", "plaquette.json")
FUORI = os.path.join(RADICE, "doc", "REFERTO_verso_e_plaquette_2026-10-06.md")
CLASSI = ("MATERIA", "BORDO", "VUOTO")


def n4(x, c=4):
    """### **`n/d` NON E' `0`**: un valore che non c'e' si dice, non si inventa."""
    if x is None:
        return "n/d"
    if isinstance(x, bool):
        return "SI" if x else "NO"
    if isinstance(x, float):
        if x != x:
            return "n/d"
        if x and (abs(x) < 1e-3 or abs(x) >= 1e6):
            return "%.2e" % x
        return ("%." + str(c) + "f") % x
    return str(x)


def pct(x):
    return "n/d" if x is None else "%.2f %%" % (100.0 * x)


def tab_classi(d, campo, c=4):
    """Una riga per classe, da un dizionario `per_classe`. ### **I `None` passano.**"""
    r = []
    for k in CLASSI:
        v = (d or {}).get(k)
        r.append("n/d" if not v else n4(v.get(campo), c))
    return r


def main(argv):
    mancano = [p for p in (J_V, J_P) if not os.path.isfile(p)]
    if mancano:
        print("[FERMO] manca %s" % ", ".join(mancano))
        return 1
    V = json.load(io.open(J_V, encoding="utf-8"))
    P = json.load(io.open(J_P, encoding="utf-8"))
    # ### ⛔ **IL GUARDIANO DEL REFERTO:** una corsa incompleta non si racconta come
    #   completa. ### **E si dice QUALE delle due**, perche' i due json nascono dalla
    #   STESSA corsa e un disallineamento sarebbe esso stesso un fatto.
    guai = []
    for et, D in (("verso", V), ("plaquette", P)):
        if D.get("stato") != "DATI SALVATI":
            guai.append("%s: stato = %r" % (et, D.get("stato")))
        if D.get("passi_girati") != D.get("passi"):
            guai.append("%s: passi girati %s su %s"
                        % (et, D.get("passi_girati"), D.get("passi")))
    if V.get("blob_sim", "")[:8] != V.get("blob_atteso"):
        guai.append("il blob del simulatore non e' quello atteso")
    if guai:
        print("[FERMO] la corsa non e' completa: %s" % "; ".join(guai))
        return 1
    vv, pp = V["verso"], P["plaquette"]
    passi_m = [int(x) for x in vv["passi_misura"]]
    righe = {int(r["passo"]): r for r in vv["passi"]}
    o = []
    A = o.append

    # ------------------------------------------------------------------ la testa
    A("# REFERTO — `M1`-`M4`: **IL VERSO E LE PLAQUETTE**, in sola lettura *(2026-10-06)*")
    A("")
    A("*(Mandato di Luca del 2026-10-06 e sua integrazione. ### **Criteri e previsioni "
      "fissati PRIMA della corsa** in `doc/TASK_HISTORY/2026-10-06_misura-verso-e-"
      "plaquette.md`, committato **prima** in `76b18ef`.)*")
    A("")
    A("> ### ⛔ **QUESTO REFERTO NON SCEGLIE NIENTE, e lo dice il mandato:** *«questa "
      "misura NON sceglie un'opzione. Riporta i numeri e l'unica affermazione permessa e' "
      "DESCRITTIVA.»* ### **Le raccomandazioni restano quelle di "
      "`doc/GEOM_SENZA_VERSO.md`: questo referto non ne aggiunge e non ne ritira "
      "nessuna.**")
    A("")
    A("## LA CORSA")
    A("")
    A("| | |")
    A("|---|---|")
    A("| simulatore | `%s` *(atteso `%s`: ### **coincide**)* |"
      % (V["blob_sim"][:8], V["blob_atteso"]))
    A("| strumenti | `%s` *(`M1`-`M3`)* · `%s` *(`M4`)* |"
      % (V["blob_strumento"][:8], P["blob_strumento"][:8]))
    A("| passi | ### **%s**, un braccio, ### **SOLA LETTURA** |" % V["passi_girati"])
    A("| passi della misura | %s |" % ", ".join("`%d`" % k for k in passi_m))
    A("| passi ### **PESANTI** | %s — ### **i quattro della misura E I LORO "
      "PREDECESSORI**, perche' la stabilita' e' una differenza fra due passi |"
      % ", ".join("`%d`" % k for k in vv["passi_pesanti"]))
    A("| in configurazione del driver | ### **%s** |"
      % n4(V["in_configurazione_del_driver"]))
    A("| a valle | `n = %s`, archi `%s` |"
      % (V["a_valle"]["n"], V["a_valle"]["archi"]))
    A("| durata | `%s s` |" % n4(V["secondi"], 1))
    A("| piattaforma | %s · numpy %s |"
      % (V["piattaforma"].get("python", "?"), V["piattaforma"].get("numpy", "?")))
    A("")
    g = vv["geometria"]
    A("**LA GEOMETRIA, letta DALLA SCENA** *(nessun numero nuovo)*: `r_regione = %s`, "
      "`R_CONN = %s`, quindi `u_bordo = 1 + R_CONN/r_regione = %s`; `sep = %s`, coorti "
      "`%s`."
      % (n4(g["r_regione"], 6), n4(g["R_CONN"], 6), n4(g["u_bordo"]), n4(g["sep"], 4),
         g["n_coorti"]))
    A("")
    A("> ### \U0001f4cc **`M4` E' GIRATO SULLA STESSA CORSA DI `M1`-`M3`, e lo dichiaro:** "
      "il mandato lo consente *«se lo strumento non e' ancora stato committato»*, e "
      "### **non lo era** quando l'integrazione e' arrivata. ### **Un file separato, un "
      "json separato, UNA corsa sola** *(il json lo registra: "
      "`gira_sulla_stessa_corsa_di_M1_M3 = %s`)*."
      % n4(pp.get("gira_sulla_stessa_corsa_di_M1_M3")))
    A("")
    A("> ### ⚠ **E IL PASSO `1` ERA GIA' VISTO:** il collaudo su `2` passi *(che il "
      "mandato chiede)* ha prodotto quei numeri ### **prima** della corsa. ### **Per il "
      "passo `1` le mie previsioni non erano previsioni**, e nel task history sono marcate "
      "come tali. ### **Le previsioni vere riguardano i passi `50`, `150` e `230`.**")
    A("")

    # ------------------------------------------------------------------ SOLA LETTURA
    A("---")
    A("")
    A("## ✔ **CHE COSA HA SCRITTO OGNI CHIAMATA GUARDATA — MISURATO, non dichiarato**")
    A("")
    A("Il presidio `sola_lettura` copia **tutto** `net.__dict__`, ### **misura quali "
      "attributi la chiamata ha scritto**, ripristina tutto e ### **riverifica.** "
      "### **Questi non sono gli attributi che io CREDO che vengano scritti: sono quelli "
      "che il presidio ha VISTO cambiare.**")
    A("")
    A("| la chiamata | quanti | quali |")
    A("|---|--:|---|")
    for k, x in sorted(vv["scritture_misurate"].items()):
        A("| `%s` | ### **%d** | %s |"
          % (k, len(x), ", ".join("`%s`" % y for y in x) or "### **nessuno**"))
    A("")
    A("> ### ⛔ **E AVEVO SCRITTO CHE `lambda_nodi` ERA DI SOLA LETTURA, ED ERA "
      "FALSO.** Un elenco a mano avrebbe perso le scritture ### **TRANSITIVE** — e "
      "`_chi_geom_nodi` e' ### **la cache che `TORS_4PI` legge al passo dopo**, quindi "
      "lasciarla scritta avrebbe cambiato la dinamica della corsa che sto misurando.")
    A("")

    # ------------------------------------------------------------------ M1
    A("---")
    A("")
    A("## `M1` — **`--chi-core` AGISCE SUL DIPOLO?**")
    A("")
    A("**IL CRITERIO, fissato prima:** ### **`(a) = 0` E `(c) = 0` a TUTTI E QUATTRO i "
      "passi significa `--chi-core` INERTE per il dipolo.** Altrimenti si riporta dove e "
      "quanto agisce. ### **E `(b)` si riporta SEMPRE:** un massimo a `0.98` e uno a "
      "`0.001` danno lo stesso `(a) = 0` e ### **dicono due cose opposte.**")
    A("")
    A("| passo | `(a)` nodi con `rho0/rho_c > 1` | `(b)` ### **il MASSIMO del rapporto** | "
      "`(c)` diversi da `perc_geom` | `rho_c` | `max |psi|^2` | mediana del rapporto |")
    A("|--:|--:|--:|--:|--:|--:|--:|")
    tutti_a0, tutti_c0, visti = True, True, 0
    bmax = []
    for k in passi_m:
        m = (vv["misure"].get(str(k)) or {}).get("M1")
        if not m or m.get("stato") != "MISURATO":
            A("| `%d` | n/d | n/d | n/d | n/d | n/d | n/d |" % k)
            tutti_a0 = tutti_c0 = False
            continue
        visti += 1
        a_ = m["a_nodi_sopra_1"]; c_ = m["c_diversi_da_perc_geom"]
        tutti_a0 &= (a_ == 0); tutti_c0 &= (c_ == 0)
        bmax.append(m["b_rapporto_max"])
        A("| `%d` | %s**%d** | ### **%s** | %s**%d** | %s | %s | %s |"
          % (k, "### " if a_ else "", a_, n4(m["b_rapporto_max"], 6),
             "### " if c_ else "", c_, n4(m["rho_c"], 3), n4(m["I2_max"], 4),
             n4(m["rapporto_mediano"], 6)))
    A("")
    if visti == 0:
        A("> ### ⛔ **NESSUN PASSO MISURATO: il criterio NON si applica**, e un "
          "<<inerte>> qui sarebbe ### **un'assenza letta come un esito.**")
    elif visti < len(passi_m):
        A("> ### ⚠ **SOLO `%d` PASSI SU `%d` SONO MISURATI**, quindi il criterio "
          "*«a TUTTI i passi»* ### **non e' verificabile su questa corsa.**"
          % (visti, len(passi_m)))
    elif tutti_a0 and tutti_c0:
        A("> ### ✔ **IL CRITERIO E' SODDISFATTO: `(a) = 0` e `(c) = 0` a tutti e "
          "`%d` i passi**, quindi ### **`--chi-core` e' INERTE per il dipolo in questa "
          "scena.**" % visti)
        A(">")
        A("> ### ⚠ **E `(b)` DICE QUANTO MARGINE C'E', che e' la ragione per cui il "
          "mandato lo pretende anche con `(a) = 0`:** il massimo del rapporto arriva a "
          "### **`%s`**, cioe' ### **`%s` volte sotto la soglia.** ### **Non e' <<appena "
          "sotto>>: e' lontano.**"
          % (n4(max(bmax), 6), n4(1.0 / max(max(bmax), 1e-30), 1)))
    else:
        A("> ### ⛔ **IL CRITERIO NON E' SODDISFATTO: `--chi-core` NON e' inerte.** "
          "### **Tre opzioni su quattro cambiano lettore**, e il massimo del rapporto "
          "arriva a ### **`%s`**." % n4(max(bmax) if bmax else None, 6))
    A("")
    ok_c = all(((vv["misure"].get(str(k)) or {}).get("M1") or {}).get("c_dentro_a", True)
               for k in passi_m)
    A("**IL CONTROLLO CHE LEGA I DUE CONTI INDIPENDENTI:** `(a)` e `(b)` li ### **ricalcolo "
      "io** *(vettorialmente, con la stessa definizione)*, `(c)` viene dalla "
      "### **funzione vera** chiamata dentro il presidio. La funzione modifica "
      "`chi_core[k]` ### **solo dove `r > 0`**, cioe' solo dove `rapporto > 1`, quindi "
      "### **`(c)` NON PUO' superare `(a)`.** ### **Esito:** %s."
      % ("✔ **regge a tutti i passi**" if ok_c else
         "⛔ **NON regge: il mio ricalcolo di `rho0` non e' quello della funzione**"))
    A("")

    # ------------------------------------------------------------------ M2
    A("---")
    A("")
    A("## `M2` — **`c_k`, LA COERENZA DEL CAMPO AL NODO, col denominatore SATURO**")
    A("")
    A("**LA FORMA, e la correzione verificata sul codice:** "
      "`c_k = |satura(F_k)| / satura(amp * Somma_j |W_kj|)`. ### **Il denominatore e' "
      "SATURO**, e il motivo e' algebrico: `|satura(f)|` e' ### **monotona nel modulo**, "
      "quindi con questa forma ### **`c_k` sta in `[0,1]` e `c = 1` E' RAGGIUNGIBILE** — "
      "col denominatore ### **nudo** non lo sarebbe mai.")
    A("")
    A("| passo | `c_k` mediana | MATERIA | BORDO | VUOTO | ### **`AUC` MAT/VUOTO** | "
      "fuori da `[0,1]` |")
    A("|--:|--:|--:|--:|--:|--:|--:|")
    for k in passi_m:
        m = (vv["misure"].get(str(k)) or {}).get("M2")
        if not m or m.get("stato") != "MISURATO":
            A("| `%d` | n/d | n/d | n/d | n/d | n/d | n/d |" % k)
            continue
        t = tab_classi(m["c_per_classe"], "mediana")
        A("| `%d` | %s | %s | %s | %s | ### **%s** | %s%s |"
          % (k, n4(m["c_tutti"]["mediana"]), t[0], t[1], t[2],
             n4(m["auc_materia_vuoto"]),
             "### " if m["c_fuori_0_1"] else "", m["c_fuori_0_1"]))
    A("")
    A("> ### **`AUC = 0.5` VUOL DIRE NESSUNA SEPARAZIONE.** Qui l'`AUC` e' la probabilita' "
      "che un nodo di MATERIA preso a caso abbia `c_k` ### **piu' alto** di un nodo di "
      "VUOTO preso a caso.")
    A("")
    A("**E IL SECONDO ASSE CHIESTO DAL MANDATO, il NUMERO DI VICINI** *(secchi dichiarati "
      "prima: %s)*:" % ", ".join("`%s`" % ("%d-%d" % (a, b) if b < 10 ** 9 else "%d+" % a)
                                 for a, b in vv["secchi_grado"]))
    A("")
    sec = [("%d-%d" % (a, b) if b < 10 ** 9 else "%d+" % a) for a, b in vv["secchi_grado"]]
    A("| passo | " + " | ".join("`%s`" % s for s in sec) + " | grado medio |")
    A("|--:|" + "--:|" * (len(sec) + 1))
    for k in passi_m:
        m = (vv["misure"].get(str(k)) or {}).get("M2")
        if not m or m.get("stato") != "MISURATO":
            A("| `%d` |" % k + " n/d |" * (len(sec) + 1))
            continue
        c = []
        for s in sec:
            x = (m["c_per_grado"] or {}).get(s)
            c.append("n/d" if not x else "%s *(n=%d)*" % (n4(x["c_mediana"]), x["n"]))
        A("| `%d` | %s | %s |" % (k, " | ".join(c), n4(m["grado"]["medio"], 2)))
    A("")
    sc = [((vv["misure"].get(str(k)) or {}).get("M2") or {}).get("psi_vs_num_scarto_max")
          for k in passi_m]
    sc = [x for x in sc if x is not None]
    A("> ### ⚠ **UNA DICHIARAZIONE, invece di un silenzio:** numeratore e denominatore "
      "vengono dallo ### **STESSO `w`**, ricalcolato dopo il passo, mentre `net.psi` e' "
      "stato calcolato ### **DENTRO** il passo. ### **Sono due istanti diversi**, e lo "
      "scarto massimo fra `|net.psi|` e il mio numeratore vale ### **`%s`** — si riporta "
      "invece di essere taciuto." % (n4(max(sc), 4) if sc else "n/d"))
    A("")

    # ------------------------------------------------------------------ M3
    A("---")
    A("")
    A("## `M3` — **QUANTO OSCILLA OGNI CANDIDATO AL <<VERSO>>**")
    A("")
    A("> ### ⛔ **E' LA LETTURA CHE CONTA, perche' col dipolo che entra COME "
      "VARIAZIONE un verso GIUSTO ma che OSCILLA inietterebbe `±π` esattamente come "
      "adesso.** ### **Il riferimento e' `perc_geom`: il verso di OGGI.**")
    A("")
    A("### `A` — **DUE letture, e il mandato ne nomina una sola**")
    A("")
    fcv = [(k, (righe.get(k) or {}).get("archi_i_maggiore_j")) for k in passi_m]
    A("`tw` e' orientata `i -> j` *(verificato dal codice)*. Quindi:")
    A("")
    A("> ### \u26d4 **E QUI AVEVO SCRITTO UNA PREMESSA FALSA: <<tutti gli archi hanno "
      "`i < j`>>.** Era misurata ai passi `0`, `1` e `2`, cioe' ### **prima della prima "
      "nascita**, e la corsa precedente si e' ### **FERMATA al passo `229`** su `9` archi "
      "fuori convenzione. ### **Ogni nascita ne produce ESATTAMENTE uno**: alla mitosi "
      "nascono `a-m` e `m-b` col nodo nuovo `m` di indice ### **piu' alto**, quindi `m-b` "
      "ha `i > j` ### **sempre.** ### \u2714 **Adesso il conto NON si assume: si MISURA a "
      "ogni passo** -- %s -- e la chiave d'arco e' ### **canonica `(min, max)`**, col "
      "segno della circolazione ### **letto dall'arco** invece che dedotto."
      % ", ".join("`%d`: %s" % (k, n4(x)) for k, x in fcv))
    A("")
    A("| | |")
    A("|---|---|")
    A("| `A` ### **GREZZA** | `Σ tw` col segno ### **MEMORIZZATO** — ### ⛔ "
      "**dipende dalla NUMERAZIONE** |")
    A("| `A` ### **DIVERGENZA** | col segno ### **relativo al nodo**: il ### **flusso "
      "uscente**, ben definito — ### **e non e' una circolazione** |")
    A("")
    A("| passo | nodi | `A` grezza: cambi | frazione | `A` divergenza: cambi | frazione | "
      "### **`perc_geom`: cambi** | ### **frazione** | `A` grezza `= 0` |")
    A("|--:|--:|--:|--:|--:|--:|--:|--:|--:|")
    for k in passi_m:
        r = righe.get(k)
        if not r:
            A("| `%d` |" % k + " n/d |" * 8)
            continue
        nc = r.get("nodi_confrontabili")
        def fr(x):
            return "n/d" if (x is None or not nc) else pct(float(x) / nc)
        A("| `%d` | %s | %s | %s | %s | %s | ### **%s** | ### **%s** | %s |"
          % (k, n4(nc), n4(r.get("cambi_A_grezza")), fr(r.get("cambi_A_grezza")),
             n4(r.get("cambi_A_divg")), fr(r.get("cambi_A_divg")),
             n4(r.get("cambi_perc_geom")), fr(r.get("cambi_perc_geom")),
             n4(r.get("A_grezza_zero"))))
    A("")
    A("### `D` — **il segno di `tw` SULL'ARCO**, confrontato ### **per CHIAVE `(i,j)`**")
    A("")
    A("> ### ⚠ **PER CHIAVE E NON PER INDICE**, perche' alla mitosi "
      "`i = concat([i[keep], a, m])` ### **rimescola gli indici**: un confronto per indice "
      "conterebbe cambi che non ci sono. ### **E gli archi non confrontabili si CONTANO.**")
    A("")
    A("| passo | archi | ### **con `i > j`** | confrontabili | nuovi | "
      "cambi di `sign(tw)` | frazione |")
    A("|--:|--:|--:|--:|--:|--:|--:|")
    for k in passi_m:
        r = righe.get(k)
        if not r:
            A("| `%d` |" % k + " n/d |" * 6)
            continue
        nc = r.get("archi_confrontabili")
        cd = r.get("cambi_D_segno_tw")
        A("| `%d` | %s | ### **%s** | %s | %s | %s | %s |"
          % (k, n4(r.get("archi")), n4(r.get("archi_i_maggiore_j")), n4(nc),
             n4(r.get("archi_nuovi")), n4(cd),
             "n/d" if (cd is None or not nc) else pct(float(cd) / nc)))
    A("")
    A("> ### \u2714 **E IL SEGNO SI CONFRONTA RIDOTTO AL VERSO CANONICO `min -> max`:** "
      "`tw` e' una ### **1-forma orientata**, quindi confrontare `sign(tw)` fra due passi "
      "senza quella riduzione ### **conterebbe un cambio di segno dove e' cambiata solo "
      "la SCRITTURA dell'arco.**")
    A("")
    # --- l'aggregato su tutta la corsa: A e D si prendono a OGNI passo
    agg = [r for r in vv["passi"] if r.get("nodi_confrontabili")]
    if agg:
        fa = [float(r["cambi_A_grezza"]) / r["nodi_confrontabili"] for r in agg
              if r.get("cambi_A_grezza") is not None]
        fg = [float(r["cambi_perc_geom"]) / r["nodi_confrontabili"] for r in agg
              if r.get("cambi_perc_geom") is not None]
        fd = [float(r["cambi_D_segno_tw"]) / r["archi_confrontabili"] for r in agg
              if r.get("cambi_D_segno_tw") is not None and r.get("archi_confrontabili")]
        A("**E `A` E `D` SI PRENDONO A OGNI PASSO, non solo ai quattro** *(costano poco)*, "
          "quindi si puo' dare ### **la media su tutta la corsa**:")
        A("")
        A("| | passi | frazione media per passo |")
        A("|---|--:|--:|")
        A("| `A` grezza | %d | ### **%s** |" % (len(fa), pct(sum(fa) / max(len(fa), 1))))
        A("| `D` segno di `tw` | %d | ### **%s** |"
          % (len(fd), pct(sum(fd) / max(len(fd), 1))))
        A("| ### **`perc_geom`** *(il riferimento di oggi)* | %d | ### **%s** |"
          % (len(fg), pct(sum(fg) / max(len(fg), 1))))
        A("")
    A("### `C` — **l'OLONOMIA DI FASE sulla base dei cicli**")
    A("")
    A("> ### ⛔ **LA CONVENZIONE DEL `verso` L'HO MISURATA, NON DEDOTTA:** il cammino "
      "e' `u -> lca -> v -> u` e ### **la chiusura si percorre `v -> u` mentre il suo "
      "`verso` e' registrato `+1`**, cioe' opposto. ### **La via primaria e' "
      "`_vertici_ciclo`**, che chiude il ciclo per costruzione; quella sugli archi resta "
      "come ### **controllo indipendente.**")
    A("")
    A("| passo | cicli | ### **olonomia non nulla** | frazione | `|k|` max | "
      "scarto dal multiplo di `4π` | ### **le due vie: modulo** | ### **segno discorde** | "
      "base cambiata |")
    A("|--:|--:|--:|--:|--:|--:|--:|--:|--:|")
    for k in passi_m:
        m = (vv["misure"].get(str(k)) or {})
        c = m.get("M3_C")
        cb = m.get("M3_C_cambio_base")
        if not c:
            A("| `%d` |" % k + " n/d |" * 8)
            continue
        A("| `%d` | %s | ### **%s** | %s | %s | %s | %s | ### **%s** | %s |"
          % (k, n4(c["n_cicli"]), n4(c["olonomia_non_nulla"]),
             pct(c["frazione_non_nulla"]), n4(c["k_max"], 0),
             n4(c["scarto_dal_multiplo_max"]),
             n4(c.get("due_vie_modulo_disaccordo_max")),
             n4(c.get("due_vie_segno_discorde")),
             "n/d" if not cb else "%s su %s (%s)"
             % (cb["nuovi"], cb["cicli_oggi"], pct(cb["frazione_cambiata"]))))
    A("")
    sm = [((vv["misure"].get(str(k)) or {}).get("M3_C") or {}).get(
        "scarto_dal_multiplo_max") for k in passi_m]
    sm = [x for x in sm if x is not None]
    A("> ### ✔ **L'ALGEBRA DELL'OBIEZIONE `(b)` E' CONFERMATA DAL NUMERO, non "
      "assunta:** su un ciclo chiuso la somma di `(phi_i - phi_j)` telescopia a `0` esatto "
      "e `_wphi` avvolge sul periodo `4π`, quindi l'olonomia ### **deve** essere un "
      "multiplo intero di `4π`. ### **Scarto massimo misurato: `%s`.**"
      % (n4(max(sm)) if sm else "n/d"))
    A(">")
    dis = [((vv["misure"].get(str(k)) or {}).get("M3_C") or {}).get(
        "due_vie_segno_discorde") for k in passi_m]
    nn = [((vv["misure"].get(str(k)) or {}).get("M3_C") or {}).get(
        "olonomia_non_nulla") for k in passi_m]
    coppie = [(a_, b_) for a_, b_ in zip(dis, nn) if a_ is not None and b_ is not None]
    tutti = bool(coppie) and all(a_ == b_ and b_ > 0 for a_, b_ in coppie)
    A("> ### ⛔ **E IL SEGNO DELL'OLONOMIA NON E' DETERMINATO DAL GRAFO:** le due vie "
      "concordano sul ### **MODULO** e ### **discordano sul SEGNO**%s. ### **Due routine "
      "DEL SIMULATORE scelgono versi opposti sullo STESSO ciclo** — ed e' precisamente "
      "l'arbitrarieta' che l'obiezione `(a)` attribuisce all'opzione `C`."
      % (" su ### **TUTTI** i cicli con olonomia non nulla, a ### **ogni** passo misurato "
         "*(%s su %s)*" % (", ".join(n4(x) for x, _y in coppie),
                           ", ".join(n4(y) for _x, y in coppie))
         if tutti else
         " su %s cicli con olonomia non nulla *(su %s)*"
         % (", ".join(n4(x) for x in dis), ", ".join(n4(x) for x in nn))))
    A("")

    # ------------------------------------------------------------------ M4
    A("---")
    A("")
    A("## `M4` — **LE PLAQUETTE** *(l'opzione `P` di Luca)*")
    A("")
    A("**La plaquette:** un triangolo coi ### **tre archi presenti.** La circolazione sul "
      "cammino `u -> v -> w -> u` e' `tw[(u,v)] + tw[(v,w)] - tw[(u,w)]`, e ### **il meno "
      "c'e' perche' l'ultimo tratto va contro la convenzione `i < j`.**")
    A("")
    A("> ### ✔ **E IL SEGNO DI UNA SINGOLA PLAQUETTE E' ARBITRARIO, IL PRODOTTO COL "
      "VERSORE NO:** scambiando due vertici la circolazione cambia segno ### **e la "
      "normale anche**, quindi il prodotto ### **`(Σ tw) · n̂` e' INVARIANTE mentre "
      "ciascun fattore da solo NON LO E'.** ### **Per questo `(b)` misura il MODULO e "
      "`(c)` il VETTORE** — e ### **`R_k` resta un ASSE: l'invarianza non regala il "
      "segno.**")
    A("")
    A("### `(a)` **quante, e quanto costano**")
    A("")
    A("| passo | ### **plaquette** | conto ### **indipendente** | degeneri | "
      "archi `i > j` | cappi esclusi | nodi senza plaquette | `s` enumerazione | "
      "`s` controllo | MATERIA | BORDO | VUOTO |")
    A("|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|")
    for k in passi_m:
        m = pp["misure"].get(str(k))
        if not m:
            A("| `%d` |" % k + " n/d |" * 11)
            continue
        t = tab_classi(m["a_per_nodo_per_classe"], "mediana", 0)
        A("| `%d` | ### **%s** | %s | %s | ### **%s** | %s | %s | %s | %s | %s | %s | %s |"
          % (k, n4(m["a_plaquette_totali"]), n4(m["a_controllo_indipendente"]),
             n4(m["a_degeneri"]), n4(m.get("a_archi_i_maggiore_j")),
             n4(m.get("a_cappi_esclusi")), n4(m["a_nodi_senza_plaquette"]),
             n4(m["a_secondi"], 2), n4(m["a_secondi_controllo"], 2), t[0], t[1], t[2]))
    A("")
    A("*(Le tre colonne di classe sono la ### **MEDIANA delle plaquette per nodo**.)*")
    A("")
    ok_ind = all((pp["misure"].get(str(k)) or {}).get("a_plaquette_totali")
                 == (pp["misure"].get(str(k)) or {}).get("a_controllo_indipendente")
                 for k in passi_m if pp["misure"].get(str(k)))
    A("> ### %s **IL CONTO INDIPENDENTE:** %s. Per ogni arco il numero di ### **vicini "
      "comuni** e' il numero di triangoli che passano per quell'arco, e sommato sugli "
      "archi orientati ogni triangolo si conta ### **sei volte.** ### **Non passa da "
      "nessuna chiave**, quindi non condivide nessun difetto con l'enumerazione — e "
      "### ⛔ **in costruzione ha trovato un traboccamento `int32` che faceva sparire "
      "il `97 %%` dei triangoli IN SILENZIO.**"
      % (("✔", "coincide a tutti i passi") if ok_ind else
         ("⛔", "### **NON coincide**: la misura non vale")))
    A("")
    A("### `(b)` **`|Σ tw|` sulle plaquette**, per classe")
    A("")
    A("| passo | campione | q05 | q25 | ### **q50** | q75 | q95 | max | "
      "MATERIA *(media per nodo)* | BORDO | VUOTO |")
    A("|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|")
    for k in passi_m:
        m = pp["misure"].get(str(k))
        if not m:
            A("| `%d` |" % k + " n/d |" * 10)
            continue
        q = m["b_campione"].get("quantili") or [None] * 5
        t = tab_classi(m["b_modulo_medio_per_nodo_per_classe"], "mediana")
        A("| `%d` | %s | %s | %s | ### **%s** | %s | %s | %s | %s | %s | %s |"
          % (k, n4(m["b_campione"]["n"]), n4(q[0]), n4(q[1]), n4(q[2]), n4(q[3]),
             n4(q[4]), n4(m["b_campione"]["max"]), t[0], t[1], t[2]))
    A("")
    A("*(I quantili vengono da un sottocampione a ### **passo PRIMO fisso** `%s`: "
      "### **deterministico, nessun RNG, nessun seme da dichiarare.**)*"
      % pp.get("passo_campione"))
    A("")
    A("### `(c)` **LA COERENZA `|Σ v| / Σ |v|`** — `0` disordine, `1` stesso asse")
    A("")
    A("| passo | MATERIA | BORDO | VUOTO | MATERIA q25-q75 | VUOTO q25-q75 | "
      "nodi senza `R` definito |")
    A("|--:|--:|--:|--:|--:|--:|--:|")
    for k in passi_m:
        m = pp["misure"].get(str(k))
        if not m:
            A("| `%d` |" % k + " n/d |" * 6)
            continue
        c = m["c_coerenza_per_classe"]
        t = tab_classi(c, "mediana")
        mm = c.get("MATERIA") or {}
        vu = c.get("VUOTO") or {}
        A("| `%d` | ### **%s** | %s | ### **%s** | %s - %s | %s - %s | %s |"
          % (k, t[0], t[1], t[2], n4(mm.get("q25")), n4(mm.get("q75")),
             n4(vu.get("q25")), n4(vu.get("q75")),
             n4(m.get("a_nodi_senza_plaquette_non_degenere"))))
    A("")
    A("> ### ⚠ **E UN NODO SENZA NESSUNA PLAQUETTE NON DEGENERE HA COERENZA `NaN`, "
      "NON `0`:** un `0` li' vorrebbe dire *«disordine totale»* mentre la verita' e' "
      "*«non definita»*. ### **E' la famiglia di `CHI-TORS-ZERO-FALSO`, e il collaudo me "
      "l'ha trovato addosso.**")
    A("")
    A("### `(d)` **il coseno fra `R_k` e l'asse di Bloch `_nb`** — *e `P2` dipende da qui*")
    A("")
    A("**IL CASO NULLO E' ANALITICO, non simulato:** fra due assi indipendenti in `3D` il "
      "coseno e' ### **UNIFORME su `[-1,1]`**, quindi ### **media `0`** e ### **frazione "
      "con `|cos| > 0.5` pari a `0.5`.**")
    A("")
    A("| passo | media MATERIA | media BORDO | media VUOTO | "
      "`|cos|>0.5` MATERIA | BORDO | VUOTO | ### **atteso dal caso** |")
    A("|--:|--:|--:|--:|--:|--:|--:|--:|")
    for k in passi_m:
        m = pp["misure"].get(str(k))
        if not m:
            A("| `%d` |" % k + " n/d |" * 7)
            continue
        t = tab_classi(m["d_cos_con_nb_per_classe"], "media")
        f = tab_classi(m["d_frazione_oltre_mezzo_per_classe"], "media")
        A("| `%d` | %s | %s | %s | %s | %s | %s | media `%s`, frazione `%s` |"
          % (k, t[0], t[1], t[2], f[0], f[1], f[2],
             n4(m["d_caso_nullo"]["media_attesa"], 1),
             n4(m["d_caso_nullo"]["frazione_oltre_mezzo_attesa"], 1)))
    A("")
    A("### `(e)` **LA STABILITA': di quanto ruota `R_k` fra due passi**")
    A("")
    A("| passo | contro il passo | nodi | ### **angolo mediano (gradi)** MATERIA | BORDO | "
      "VUOTO | nodi senza `R` | ### **riferimento: `perc_geom` cambia** |")
    A("|--:|--:|--:|--:|--:|--:|--:|--:|")
    for k in passi_m:
        m = pp["misure"].get(str(k))
        e = (m or {}).get("e_stabilita")
        if not e:
            A("| `%d` |" % k + " n/d |" * 7)
            continue
        t = tab_classi(e["angolo_gradi_per_classe"], "mediana", 2)
        A("| `%d` | `%s` | %s | ### **%s** | %s | %s | %s | ### **%s** |"
          % (k, e["passo_precedente"], n4(e["nodi_confrontabili"]), t[0], t[1], t[2],
             n4(e["nodi_senza_R"]),
             pct(e.get("riferimento_perc_geom_frazione_cambiata"))))
    A("")
    A("> ### **L'ANGOLO E IL RIFERIMENTO MISURANO DUE COSE DIVERSE, e lo dico perche' non "
      "si confondano:** l'angolo e' ### **CONTINUO** *(di quanto ruota un asse)*, la "
      "frazione di `perc_geom` e' ### **DISCRETA** *(quanti nodi cambiano valore)*. "
      "### **Non sono la stessa grandezza e non si sottraggono** — stanno accanto perche' "
      "il mandato chiede il confronto, e ### **il confronto e' fra due letture, non fra "
      "due numeri.**")
    A("")

    # ------------------------------------------------------------------ le previsioni
    A("---")
    A("")
    A("## \u26a0 **LE MIE PREVISIONI, CONTRO I NUMERI** — *e le stampa lo script*")
    A("")
    A("Le previsioni sono fissate in `doc/TASK_HISTORY/2026-10-06_misura-verso-e-"
      "plaquette.md`, committato ### **prima della corsa** in `76b18ef`. ### **Qui le "
      "confronta il codice, non la mia buona volonta'** — e ### **il passo `1` non conta: "
      "era GIA' VISTO** *(il collaudo su `2` passi)*, quindi si guardano i passi "
      "### **oltre il primo.**")
    A("")
    # ### I PASSI CHE CONTANO: quelli della misura DOPO il primo, e solo se MISURATI.
    dopo = [k for k in passi_m if k > 1]
    def _m1(k):
        return (vv["misure"].get(str(k)) or {}).get("M1")
    def _m2(k):
        return (vv["misure"].get(str(k)) or {}).get("M2")
    def _m4(k):
        return pp["misure"].get(str(k))
    pr = []

    # --- 1. M1: chi-core inerte
    v = [_m1(k) for k in dopo]
    v = [x for x in v if x and x.get("stato") == "MISURATO"]
    if not v:
        pr.append(("`M1`", "### **`--chi-core` INERTE** per il dipolo",
                   "n/d", "### \u26a0 **NON DECIDIBILE**: nessun passo misurato"))
    else:
        ok = all(x["a_nodi_sopra_1"] == 0 and x["c_diversi_da_perc_geom"] == 0 for x in v)
        pr.append(("`M1`", "### **`--chi-core` INERTE** per il dipolo",
                   "`(a)` e `(c)` valgono `0` su %d passi su %d; il massimo del rapporto "
                   "sale da `%s` a `%s`"
                   % (len(v), len(dopo), n4(v[0]["b_rapporto_max"], 6),
                      n4(v[-1]["b_rapporto_max"], 6)),
                   "### \u2714 **CONFERMATA**" if ok else
                   "### \u26d4 **SMENTITA**"))

    # --- 2. M2: c_k separa MATERIA da VUOTO
    v = [_m2(k) for k in dopo]
    v = [x for x in v if x and x.get("auc_materia_vuoto") is not None]
    if not v:
        pr.append(("`M2`", "`c_k` ### **separa MATERIA da VUOTO**", "n/d",
                   "### \u26a0 **NON DECIDIBILE**"))
    else:
        au = [x["auc_materia_vuoto"] for x in v]
        pr.append(("`M2`", "`c_k` ### **separa MATERIA da VUOTO**",
                   "`AUC` fra `%s` e `%s` *(`0.5` = nessuna separazione)*"
                   % (n4(min(au)), n4(max(au))),
                   "### \u2714 **CONFERMATA**" if min(au) > 0.5 else
                   "### \u26d4 **SMENTITA**"))

    # --- 3. M3-A: i cambi di segno CALANO coi passi
    fr = []
    for k in dopo:
        r = righe.get(k)
        if r and r.get("cambi_A_grezza") is not None and r.get("nodi_confrontabili"):
            fr.append((k, float(r["cambi_A_grezza"]) / r["nodi_confrontabili"]))
    if len(fr) < 2:
        pr.append(("`M3-A`", "i cambi di segno ### **CALANO** coi passi", "n/d",
                   "### \u26a0 **NON DECIDIBILE**: servono almeno due passi misurati"))
    else:
        cala = all(fr[i + 1][1] <= fr[i][1] for i in range(len(fr) - 1))
        pr.append(("`M3-A`", "i cambi di segno ### **CALANO** coi passi",
                   "frazione per passo: %s"
                   % ", ".join("`%d` -> %s" % (k, pct(x)) for k, x in fr),
                   "### \u2714 **CONFERMATA**" if cala else
                   "### \u26d4 **SMENTITA**: non e' monotona"))

    # --- 4. M3-C: la base cambia molto quando cominciano le nascite
    cb = [((vv["misure"].get(str(k)) or {}).get("M3_C_cambio_base"), k) for k in dopo]
    cb = [(x, k) for x, k in cb if x]
    nati = [righe.get(k, {}).get("nodi_nuovi") for k in dopo]
    nati = [x for x in nati if x]
    if not cb:
        pr.append(("`M3-C`", "la base dei cicli ### **cambia molto** con le nascite",
                   "n/d", "### \u26a0 **NON DECIDIBILE**"))
    elif not nati:
        pr.append(("`M3-C`", "la base dei cicli ### **cambia molto** con le nascite",
                   "nessuna nascita nei passi confrontati, e la base cambia %s"
                   % ", ".join(pct(x["frazione_cambiata"]) for x, _k in cb),
                   "### \u26a0 **NON DECIDIBILE**: ### **la premessa non si e' "
                   "verificata** -- senza nascite `_grado()` non invalida la cache"))
    else:
        mx = max(x["frazione_cambiata"] for x, _k in cb)
        pr.append(("`M3-C`", "la base dei cicli ### **cambia molto** con le nascite",
                   "massimo cambiato: %s, con nascite" % pct(mx),
                   "### \u2714 **CONFERMATA**" if mx > 0 else
                   "### \u26d4 **SMENTITA**: non cambia"))

    # --- 5. M4(c): la coerenza e' BASSA
    co = []
    for k in dopo:
        m = _m4(k)
        if not m:
            continue
        for cl in CLASSI:
            x = (m["c_coerenza_per_classe"] or {}).get(cl) or {}
            if x.get("mediana") is not None:
                co.append(x["mediana"])
    if not co:
        pr.append(("`M4(c)`", "la ### **COERENZA e' BASSA**", "n/d",
                   "### \u26a0 **NON DECIDIBILE**"))
    else:
        # ### LA SOGLIA DI <<BASSA>> E' MIA, E LA DICHIARO: `0.5`, cioe' il PUNTO MEDIO
        #   dell'intervallo `[0, 1]`. ### **Non e' derivata da niente**, ed e' giusto che
        #   si veda che e' una mia convenzione e non una misura.
        pr.append(("`M4(c)`", "la ### **COERENZA e' BASSA**",
                   "mediane per classe fra `%s` e `%s` *(soglia di <<bassa>>: `0.5`, il "
                   "punto medio -- ### **e' una mia convenzione, DICHIARATA, non una "
                   "misura**)*" % (n4(min(co)), n4(max(co))),
                   "### \u2714 **CONFERMATA**" if max(co) < 0.5 else
                   "### \u26d4 **SMENTITA**"))

    # --- 6. M4(d): R_k e _nb SCORRELATI come il caso
    det = []
    for k in dopo:
        m = _m4(k)
        if not m:
            continue
        for cl in CLASSI:
            x = (m["d_cos_con_nb_per_classe"] or {}).get(cl) or {}
            f = (m["d_frazione_oltre_mezzo_per_classe"] or {}).get(cl) or {}
            n_ = x.get("n", 0) - x.get("n_non_definiti", 0)
            if x.get("media") is None or n_ <= 1:
                continue
            # ### LA TOLLERANZA E' DERIVATA, NON SCELTA: per un coseno UNIFORME su
            #   `[-1,1]` la varianza e' `1/3`, quindi l'errore standard della media e'
            #   `sqrt(1/3 / n)`; per una frazione attorno a `0.5` e' `0.5/sqrt(n)`.
            #   ### **Si confronta con DUE errori standard.**
            se_m = (1.0 / 3.0 / n_) ** 0.5
            se_f = 0.5 / (n_ ** 0.5)
            det.append((k, cl, x["media"], se_m, f.get("media"), se_f, n_))
    if not det:
        pr.append(("`M4(d)`", "`R_k` e `_nb` ### **SCORRELATI, come il caso**", "n/d",
                   "### \u26a0 **NON DECIDIBILE**"))
    else:
        peggio = max(abs(m_) / sm for _k, _c, m_, sm, _f, _s, _n in det)
        pf = [abs(fz - 0.5) / sf for _k, _c, _m, _s, fz, sf, _n in det if fz is not None]
        peggio_f = max(pf) if pf else None
        # ### ⛔ **LA SOGLIA DEVE TENER CONTO DI QUANTI CONFRONTI FACCIO, e la prima
        #   versione NON LO FACEVA:** con `2 sigma` fissi e ### **%d confronti** un
        #   massimo a `2.5 sigma` ### **e' quello che il caso produce da solo**, e
        #   dichiarare <<SMENTITA>> su quel massimo sarebbe ### **un artefatto di
        #   MOLTEPLICITA'** -- cioe' esattamente l'errore di prendere un numero vero e
        #   portarlo dove misura un'altra cosa. ### **Quindi la soglia si DERIVA da
        #   Bonferroni:** il quantile normale a due code per `0.05 / n_test`.
        n_test = len(det) + len(pf)
        z = float(_norm.isf(0.025 / max(n_test, 1)))
        dentro = (peggio <= z) and (peggio_f is None or peggio_f <= z)
        pr.append(("`M4(d)`", "`R_k` e `_nb` ### **SCORRELATI, come il caso**",
                   "scarto massimo dal caso nullo: la ### **media** del coseno a "
                   "### **%s sigma** dallo zero, la ### **frazione** `|cos| > 0.5` a "
                   "### **%s sigma** da `0.5`; tolleranza ### **%s sigma**, che e' "
                   "### **Bonferroni su %d confronti** e non un numero scelto *(`sigma` e' "
                   "### **DERIVATO**: per un coseno uniforme su `[-1,1]` la varianza e' "
                   "`1/3`, e per una frazione attorno a `0.5` e' `0.5/sqrt(n)`)*"
                   % (n4(peggio, 2), n4(peggio_f, 2), n4(z, 2), n_test),
                   "### \u2714 **CONFERMATA**" if dentro else
                   "### \u26d4 **SMENTITA**"))

    # --- 7. M4(e): R_k ruota DI MOLTO
    an = []
    for k in dopo:
        e = (_m4(k) or {}).get("e_stabilita")
        if not e:
            continue
        for cl in CLASSI:
            x = (e["angolo_gradi_per_classe"] or {}).get(cl) or {}
            if x.get("mediana") is not None:
                an.append(x["mediana"])
    if not an:
        pr.append(("`M4(e)`", "`R_k` ### **ruota DI MOLTO** fra due passi", "n/d",
                   "### \u26a0 **NON DECIDIBILE**"))
    else:
        # ### <<DI MOLTO>> E' MIO, E LO DICHIARO: `10` gradi per passo.
        pr.append(("`M4(e)`", "`R_k` ### **ruota DI MOLTO** fra due passi, cioe' "
                   "### **NON e' stabile**",
                   "angolo mediano fra `%s` e `%s` gradi *(soglia di <<molto>>: `10` "
                   "gradi -- ### **e' una mia convenzione, DICHIARATA**)*"
                   % (n4(min(an), 2), n4(max(an), 2)),
                   "### \u2714 **CONFERMATA**" if min(an) > 10.0 else
                   "### \u26d4 **SMENTITA**"))

    A("| | la previsione | il numero | esito |")
    A("|---|---|---|---|")
    for et, q, num, es in pr:
        A("| %s | %s | %s | %s |" % (et, q, num, es))
    A("")
    n_sm = sum(1 for _e, _q, _n, es in pr if "SMENTITA" in es)
    n_cf = sum(1 for _e, _q, _n, es in pr if "CONFERMATA" in es)
    n_nd = len(pr) - n_sm - n_cf
    A("> ### **%d confermate, %d SMENTITE, %d non decidibili.** ### **Le smentite sono il "
      "pezzo che vale:** una misura che conferma tutto quello che credevo "
      "### **non mi ha insegnato niente.**" % (n_cf, n_sm, n_nd))
    A("")
    A("> ### \u26a0 **E DUE SOGLIE DI QUESTA TAVOLA SONO MIE, non misurate:** "
      "### **<<bassa>> = `0.5`** per la coerenza e ### **<<di molto>> = `10` gradi** per "
      "la rotazione. ### **Le dichiaro perche' un esito che dipende da una soglia scelta "
      "da me DEVE dirlo** -- la tolleranza di `M4(d)`, invece, e' ### **DERIVATA** dalla "
      "varianza di una distribuzione uniforme.")
    A("")

    # ------------------------------------------------------------------ i limiti
    A("---")
    A("")
    A("## ⛔ **CHE COSA QUESTA MISURA NON DICE**")
    A("")
    A("| | |")
    A("|---|---|")
    A("| ### **non sceglie un'opzione** | lo vieta il mandato, e ### **le "
      "raccomandazioni restano quelle di `doc/GEOM_SENZA_VERSO.md`** |")
    A("| ### **non misura `f'`** | la quota di conteggi *(un arco sta in una frazione "
      "delle plaquette del nodo)* ### **NON e' la derivata**: `f'` dipende anche dalla "
      "normalizzazione di `chi_k` e dalla coerenza delle normali |")
    A("| ### **non prova la prova dello specchio** | `B` della Stella Polare resta "
      "### **NON FATTA**: il controllo che direbbe se il verso e' una chiralita' vera o un "
      "artefatto dell'orientamento del grafo |")
    A("| ### **non chiude `U1`** | `chiralita_core_locale` prende `rho_c` da "
      "`massa_critica_adattiva`, che chiama ### **la stessa** `massa_critica_collasso`: "
      "### **il ramo adattivo non sfugge a `U1`** — e se aprire `U1` per questa funzione "
      "e' una decisione di Luca |")
    A("| ### **non e' un braccio contro un braccio** | e' ### **un braccio solo**: dice "
      "come si comportano i candidati ### **oggi**, non che cosa cambierebbe una cura |")
    A("")
    avv = (vv.get("avvisi") or []) + (pp.get("avvisi") or [])
    A("**AVVISI DEGLI STRUMENTI:** %s"
      % ("### ✔ **nessuno**" if not avv else
         NL + NL.join("* " + x for x in avv)))
    A("")
    A("> ### ⛔ **LA SCELTA FRA `A`/`B`/`C`/`D`/`P`, FRA `P1`/`P2`/`P3` — cioe' se il "
      "verso e' un SEGNO o un ASSE — E SE APRIRE `U1` PER `chiralita_core_locale`, SONO "
      "DECISIONI DI LUCA.**")
    io.open(FUORI, "w", encoding="utf-8", newline=NL).write(NL.join(o) + NL)
    print("scritto %s (%d righe)" % (FUORI, len(o) + 1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
