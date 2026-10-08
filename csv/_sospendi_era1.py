# -*- coding: utf-8 -*-
"""LA SOSPENSIONE DELLE VOCI DELL'ERA `1` — **dall'indice, NON a memoria**.

### ⛔ **CHE COSA FA, e che cosa NON fa:**

* ogni voce ### **aperta / in coda / da-decidere** e di ### **FISICA** riceve lo stato
  **`SOSPESA-ERA-1`**, con lo ### **stato originale conservato** nella colonna nuova
  `stato_era_1` e ### **a quale legge o variabile si riferisce** in `si_riferisce_a`;
* ### **NESSUNA VOCE SI CANCELLA**, e il `--collaudo` lo ### **asserisce** contando le righe
  prima e dopo;
* ### ⛔ **ECCEZIONE: le LEZIONI DI METODO NON si sospendono** — valgono anche nell'era `2`.

### ⚠ **LA CLASSIFICAZIONE FISICA/METODO E' UN'EURISTICA, e si dichiara:** `tipo` in
*(`presidio`, `standard`, `assioma`)* e un elenco di ### **parole del metodo** nel titolo o
nello `stato_da`. ### ➜ **L'elenco delle `METODO` si da' a LUCA perche' lo CONFERMI**, e il
file lo scrive in `doc/SOSPENSIONE_era1_METODO.md`.

Gira con:  python csv/_sospendi_era1.py --collaudo     *(non scrive: conta)*
           python csv/_sospendi_era1.py --applica
"""
import io
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Legge e riscrive un TSV.
TSV = os.path.join(RADICE, "doc", "INDICE_ID.tsv")
ELENCO = os.path.join(RADICE, "doc", "SOSPENSIONE_era1_METODO.md")
NL = chr(10)
TAB = chr(9)

COL13 = ["id", "alias", "titolo_breve", "fonte_principale", "stato", "blocca_run_base",
         "tipo", "famiglia", "stato_da", "avanzamento", "revisione", "motivo", "nota"]
NUOVE = ["stato_era_1", "si_riferisce_a"]
SOSPESA = "SOSPESA-ERA-1"

# ### I TIPI che sono METODO per costruzione: un presidio, uno standard e un assioma NON sono
# ### leggi di fisica -- sono regole SU COME si lavora, e l'era 2 le eredita.
TIPI_METODO = ("presidio", "standard", "assioma")

# ### LE PAROLE DEL METODO. ### ⚠ **E' un'euristica**, e per questo l'elenco va a Luca.
PAROLE_METODO = (
    "falso zero", "falso-zero", "falso positivo", "falso negativo", "falso uno",
    "falso-uno", "byte-inerzia", "byte inerzia", "identita' al byte", "identico al bit",
    "pavimento calcolato", "pavimento derivato", "default del modulo", "argv del driver",
    "dai default", "finestra", "provenienza", "riproducibil", "ricopiat",
    "non e' un controllo", "senza contrasto", "a vuoto", "controllo positivo",
    "caso che deve fallire", "non si rigira", "non e' piu' ri-girabile", "inventario",
    "numeri di riga", "shiftat", "commento scaduto", "commento stale",
    "sigillo che non", "misura mancante", "criterio non decidibile", "p3",
)

# ### LE GRANDEZZE E LE LEGGI a cui una voce puo' riferirsi: si cercano NEL TESTO della voce.
VARIABILI = (
    "phivel", "phi0", "phi_s", "phi", "psi_spin", "psi_spinor", "psi", "peq", "mem_mot",
    "omega_s", "perc_chi", "perc_geom", "perc_tw", "conc_nodi", "twp_dip", "twp", "tw",
    "d0", "vd", "eta", "pos", "lambda_nodi", "_rep", "_nb_ret", "_nb_prec", "_nb",
    "_spinor_lift", "_cs_nodo_prev", "rho_spin", "xi_termo", "dt_e", "dt_n", "tau",
)
LEGGI = (
    "K_SYNC", "sincronizzazione", "termostato", "scuoti_vuoto", "scuotimento",
    "mitosi", "schwinger", "_allaccia", "memoria_hebbiana_moto", "_smorza",
    "massa_critica", "coppia", "repuls", "SPIN_FEEDBACK", "FRAME_DRAG", "frame-drag",
    "chiralita", "torsione", "coesione", "gravita", "POZZO_D", "GRAV_BIFASE", "VIRIALE",
    "ZETA_VIR", "LAM", "rilassa_disegno", "calcola_psi", "_passo_spinoriale",
    "verlet", "step", "nascita", "divisione",
)


def leggi_tsv():
    righe = io.open(TSV, encoding="utf-8").read().split(NL)
    while righe and righe[-1] == "":
        righe.pop()
    testa = righe[0].split(TAB)
    corpo = [r.split(TAB) for r in righe[1:]]
    return testa, corpo


def e_metodo(v):
    """### `True` se la voce e' una LEZIONE DI METODO. Restituisce anche IL PERCHE'."""
    if v.get("tipo") in TIPI_METODO:
        return True, "tipo `%s`" % v["tipo"]
    testo = " ".join([v.get("titolo_breve", ""), v.get("stato_da", ""),
                      v.get("nota", "")]).lower()
    for p in PAROLE_METODO:
        if p in testo:
            return True, "la parola *«%s»*" % p
    return False, ""


# ### ⭐ **LA SPIEGAZIONE LUNGA STA IN `doc/STATO_RUN.md`, non nell'indice** *(par.9: «la
# ### spiegazione lunga in `doc/STATO_RUN.md` CON LO STESSO ID»)*. Senza di essa il campo
# ### `si_riferisce_a` restava vuoto nel `77 %` dei casi, e NON perche' le voci non abbiano un
# ### soggetto: perche' `titolo_breve` e' troncato a `100` caratteri.
_STATO_RUN = None


def testo_lungo(idv):
    """### Le righe di `doc/STATO_RUN.md` che citano QUESTO id."""
    global _STATO_RUN
    if _STATO_RUN is None:
        p2 = os.path.join(RADICE, "doc", "STATO_RUN.md")
        _STATO_RUN = io.open(p2, encoding="utf-8").read().split(NL) if os.path.exists(p2)             else []
    return " ".join(r for r in _STATO_RUN if idv in r)


def riferimenti(v):
    """### A quale legge o variabile si riferisce: si cerca NEL TESTO della voce."""
    # ### ⚠ **L'`id` SI CERCA ANCHE LUI, e non e' un dettaglio:** `titolo_breve` e'
    # ### troncato a `100` caratteri, e in molte voci il soggetto sta ### **nell'id**
    # ### *(`PHI0-CONGELATA`, `SCHW-SOTTO-LAM`, `M-LEGAMI`)*. Senza l'id il campo restava
    # ### vuoto nel `77 %` dei casi.
    testo = " ".join([v.get("id", "").replace("-", " "), v.get("titolo_breve", ""),
                      v.get("stato_da", ""), v.get("fonte_principale", ""),
                      v.get("nota", ""), testo_lungo(v.get("id", ""))])
    fuori = []
    for n in VARIABILI:
        if re.search(r"\b" + re.escape(n) + r"\b", testo):
            fuori.append(n)
    for n in LEGGI:
        if re.search(re.escape(n), testo, re.I) and n not in fuori:
            fuori.append(n)
    return fuori[:6]


def main(argv):
    applica = "--applica" in argv
    testa, corpo = leggi_tsv()
    n_prima = len(corpo)
    assert testa[:13] == COL13, "la testa del TSV non e' quella attesa: %r" % testa[:13]
    gia = testa[13:] == NUOVE
    larg = 13 + len(NUOVE)

    def voce(r):
        r = list(r) + [""] * (larg - len(r))
        return dict(zip(COL13 + NUOVE, r[:larg]))

    vv = [voce(r) for r in corpo]
    print("=" * 104)
    print("LA SOSPENSIONE DELLE VOCI DELL'ERA 1 -- dall'indice, NON a memoria")
    print("=" * 104)
    print("  voci: %d   colonne: %d %s"
          % (n_prima, len(testa), "(le due nuove CI SONO GIA')" if gia else ""))

    da_sospendere, metodo, intatte = [], [], []
    for v in vv:
        in_gioco = (v["stato"] in ("aperto", "da-decidere")
                    or v["avanzamento"] == "IN CODA")
        if v["stato"] == SOSPESA:
            intatte.append(v)          # ### gia' sospesa: non si tocca due volte
            continue
        if not in_gioco:
            intatte.append(v)
            continue
        m, perche = e_metodo(v)
        if m:
            v["_perche_metodo"] = perche
            metodo.append(v)
        else:
            da_sospendere.append(v)

    bloccanti = [v for v in da_sospendere if v["blocca_run_base"] == "SI"]
    print("  in gioco (aperto / da-decidere / IN CODA): %d"
          % (len(da_sospendere) + len(metodo)))
    print("      -> DA SOSPENDERE (FISICA):            %d" % len(da_sospendere))
    print("      -> NON si sospendono (METODO):        %d" % len(metodo))
    print("      di cui BLOCCANTI fra le sospese:      %d" % len(bloccanti))
    print("  intatte (chiuso / teoria / non-difetto / gia' sospese): %d" % len(intatte))
    senza_rif = [v for v in da_sospendere if not riferimenti(v)]
    print("  sospese SENZA nessun riferimento trovato: %d   ### (il censimento e' per DIFETTO)"
          % len(senza_rif))

    if not applica:
        print()
        print("  --collaudo: NON HO SCRITTO NIENTE. Per applicare: --applica")
        print()
        print("  I TIPI delle METODO:")
        per_tipo = {}
        for v in metodo:
            per_tipo.setdefault(v["tipo"], []).append(v["id"])
        for k in sorted(per_tipo, key=lambda x: -len(per_tipo[x])):
            print("      %-18s %3d" % (k, len(per_tipo[k])))
        return 0

    # ---------------------------------------------- SI APPLICA
    for v in da_sospendere:
        v["stato_era_1"] = v["stato"]
        v["stato"] = SOSPESA
        rif = riferimenti(v)
        v["si_riferisce_a"] = ",".join(rif) if rif else "(non trovato)"

    fuori = [TAB.join(COL13 + NUOVE)]
    for v in vv:
        fuori.append(TAB.join(v.get(c, "") for c in COL13 + NUOVE))
    io.open(TSV, "w", encoding="utf-8", newline=NL).write(NL.join(fuori) + NL)

    # ### IL CONTROLLO CHE NESSUNA VOCE E' SPARITA
    _t2, c2 = leggi_tsv()
    assert len(c2) == n_prima, ("VOCI PERSE: %d prima, %d dopo -- e NESSUNA VOCE SI CANCELLA"
                               % (n_prima, len(c2)))
    print("  ### scritto il TSV: %d voci prima, %d dopo -- NESSUNA PERSA" % (n_prima, len(c2)))

    # ---------------------------------------------- l'elenco per Luca
    E = []
    E.append("# LE LEZIONI DI METODO — **NON si sospendono, e Luca lo confermi**")
    E.append("")
    E.append("> ### ⛔ **Le voci qui sotto NON hanno ricevuto `%s`:** sono "
             "### **lezioni di METODO**, e valgono anche nell'era `2`." % SOSPESA)
    E.append(">")
    E.append("> ### ⚠ **LA CLASSIFICAZIONE E' UN'EURISTICA, e per questo l'elenco e' qui:** "
             "`tipo` in *(`%s`)* oppure una ### **parola del metodo** nel titolo o nello "
             "`stato_da`. ### ➜ **Luca lo conferma o lo corregge.**"
             % ", ".join("`%s`" % x for x in TIPI_METODO))
    E.append("")
    E.append("| | |")
    E.append("|---|--:|")
    E.append("| voci dell'indice | `%d` |" % n_prima)
    E.append("| in gioco *(aperto / da-decidere / `IN CODA`)* | `%d` |"
             % (len(da_sospendere) + len(metodo)))
    E.append("| ### **SOSPESE** *(fisica)* | ### **`%d`** |" % len(da_sospendere))
    E.append("| ### **NON sospese** *(metodo)* | ### **`%d`** |" % len(metodo))
    E.append("| ### ⛔ **bloccanti fra le SOSPESE** | ### **`%d`** |" % len(bloccanti))
    E.append("")
    E.append("## **L'ELENCO, da confermare**")
    E.append("")
    E.append("| id | tipo | ### **perche' METODO** | titolo |")
    E.append("|---|---|---|---|")
    for v in sorted(metodo, key=lambda x: (x["tipo"], x["id"])):
        E.append("| `%s` | `%s` | %s | %s |"
                 % (v["id"], v["tipo"], v.get("_perche_metodo", ""),
                    v["titolo_breve"][:92].replace("|", "/")))
    E.append("")
    E.append("## ⛔ **E LE BLOCCANTI CHE HO SOSPESO: Luca le guardi**")
    E.append("")
    E.append("### **Una voce bloccante sospesa NON e' una voce risolta:** blocca le corse "
             "### **dell'era `1`**, che non si fanno piu'. ### ⚠ **Ma se una di queste e' in "
             "realta' una lezione di METODO, l'era `2` la perderebbe.**")
    E.append("")
    E.append("| id | stato prima | si riferisce a | titolo |")
    E.append("|---|---|---|---|")
    for v in sorted(bloccanti, key=lambda x: x["id"]):
        E.append("| `%s` | `%s` | `%s` | %s |"
                 % (v["id"], v["stato_era_1"], v["si_riferisce_a"],
                    v["titolo_breve"][:84].replace("|", "/")))
    E.append("")
    E.append("## ⚠ **E LE SOSPESE SENZA RIFERIMENTO: `%d`**" % len(senza_rif))
    E.append("")
    E.append("### **Il campo `si_riferisce_a` si riempie cercando NEL TESTO della voce** i nomi "
             "delle variabili di stato e delle leggi. ### ⛔ **Dove non trova niente scrive "
             "`(non trovato)`, e NON inventa:** il censimento e' ### **per DIFETTO**, e queste "
             "sono le voci che al triage ### **vanno lette a mano.**")
    io.open(ELENCO, "w", encoding="utf-8", newline=NL).write(NL.join(E) + NL)
    print("  ### scritto %s (%d righe)" % (ELENCO, len(E)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
