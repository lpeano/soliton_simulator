# -*- coding: utf-8 -*-
"""**PUNTO 7 DEL CHECKPOINT: le TRE VOCI NUOVE di `T3`** *(3b, 3c, 3d del mandato di Luca)*
**piu' l'ATTRIBUZIONE della strada (a) in `MITOSI-NON-DIVISA`.**

**Perche' uno script:** `L-NUMERI` e `P1-quater`, come per `_indice_decisioni_6.py`. Qui in piu'
ogni voce nuova **fallisce se l'id esiste gia'** e **asserisce il tetto di 100 caratteri** del
`titolo_breve` *(il validatore lo imporrebbe comunque, ma un errore chiaro vale piu' di un rifiuto
del `pre-commit`)*.

LE TRE VOCI, e sono i punti 3b/3c/3d dell'ultimo messaggio di Luca:
  - **3b `TORS-SPINTA`**: la spinta repulsiva di torsione e' una LEGGE DINAMICA nascosta dentro
    `mitosi()`, e porta TRE NUMERI NON DERIVATI. **Nessuna cura ora: dopo `T3`.**
  - **3c `MAX-NODI-FERMA`**: `MAX_NODI` e' una GUARDIA DI MEMORIA che oggi cambia la FISICA in
    silenzio. **Deve FERMARE il run con un errore esplicito, mai troncare.**
  - **3d `MITOSI-SOGLIA-GRAD`**: la soglia di mitosi si abbassa col gradiente di tempo proprio,
    con ampiezza `0.3` e forma `tanh` **scelte a mano**. **Dopo `T3`.**

⚠ TUTTE E TRE SONO REGISTRAZIONI, NON CURE: il mandato di Luca dice *«da registrare per la fisica,
NON ora»*. Nessun numero si tocca in questo commit, e il simulatore non cambia di un byte.

COMANDO:  python csv/_archivio/_indice_t3_punto7.py
USCITA:   0 se tutto attacca, 1 se una sola cosa non attacca (e allora NON scrive).
"""
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)

TSV = os.path.join(RADICE, "doc", "INDICE_ID.tsv")
TAB = chr(9)
NL = chr(10)
OGGI = "2026-09-28"
TITOLO_MAX = 100

RIGHE = [l.rstrip(NL).split(TAB) for l in io.open(TSV, encoding="utf-8")]
H = RIGHE[0]
ESISTONO = {r[0] for r in RIGHE[1:]}
TITOLI = {r[H.index("titolo_breve")].strip() for r in RIGHE[1:]}
FATTE = []


def nuova(vid, **campi):
    """AGGIUNGE una voce, e FALLISCE se l'id o il titolo esistono gia'."""
    if vid in ESISTONO:
        raise SystemExit("[GIA' FATTO] la voce `%s` esiste: non si sovrascrive" % vid)
    t = campi.get("titolo_breve", "")
    if len(t) > TITOLO_MAX:
        raise SystemExit("[TITOLO] `%s`: %d caratteri, il tetto e' %d" % (vid, len(t), TITOLO_MAX))
    if t in TITOLI:
        raise SystemExit("[TITOLO] `%s`: titolo_breve DUPLICATO" % vid)
    r = [""] * len(H)
    r[0] = vid
    for k, v in campi.items():
        if TAB in v or NL in v:
            raise SystemExit("[FORMA] `%s`.%s: un campo non contiene TAB ne' NEWLINE" % (vid, k))
        r[H.index(k)] = v
    RIGHE.append(r)
    ESISTONO.add(vid)
    TITOLI.add(t)
    FATTE.append((vid, "NUOVA", len(t)))


def aggiungi(vid, colonna, testo):
    q = [k for k, r in enumerate(RIGHE) if k and r[0] == vid]
    if len(q) != 1:
        raise SystemExit("[ANCORA] la voce `%s` compare %d volte, non 1" % (vid, len(q)))
    r = RIGHE[q[0]]
    c = H.index(colonna)
    if testo in r[c]:
        raise SystemExit("[GIA' FATTO] `%s`.%s contiene gia' il testo" % (vid, colonna))
    r[c] = (r[c] + " " + testo) if r[c] else testo
    FATTE.append((vid, "ACCODATO a " + colonna, len(r[c])))


# ============ 3b: LA SPINTA REPULSIVA DI TORSIONE ==========================================
nuova("TORS-SPINTA",
      titolo_breve="la spinta repulsiva di torsione: legge DINAMICA dentro mitosi(), con tre "
                   "numeri non derivati",
      fonte_principale="doc/REGOLE_composizione_T3.md",
      stato="aperto", blocca_run_base="DA-DECIDERE", tipo="difetto", famiglia="?",
      avanzamento="IN CODA",
      stato_da="APERTA il " + OGGI + " su mandato di Luca (punto 3b). titolo_breve INTERO: la "
               "spinta repulsiva di torsione su `d0` e' una LEGGE DINAMICA a tutti gli effetti, "
               "nascosta dentro `mitosi()` -- che nel registro del passo e' dichiarata AMBIGUA -- "
               "e porta TRE NUMERI CHE NON SONO DERIVATI. Da registrare per la fisica, non da "
               "curare ora: la decisione di Luca e' di affrontarla DOPO `T3`, quando diventa una "
               "legge a se'.",
      nota="I SITI, letti dal codice sul blob 1fc9235f: :6307 `spinta = 0.02 * self.d0 * "
           "_rep_mem` e :6309 `self.d0 = self.d0 + self._sd0(spinta)`. E' una scrittura di `d0`, "
           "cioe' DINAMICA, dentro una funzione che il registro dichiara AMBIGUA: per questo la "
           "separazione di `T3` la fa uscire allo scoperto. I TRE NUMERI NON DERIVATI: (1) il "
           "`0.02` di :6307, e LO DICE IL CODICE STESSO -- il commento sopra la riga scrive `A1` "
           "RESTA VIOLATO, E VA DETTO: il 0.02 e' un numero SCELTO, non derivato; (2) la "
           "PENDENZA `3.0` di :6179 `segno = -np.tanh(3.0 * (pos_torsione - centro))`, che decide "
           "quanto ripida e' l'inversione fra creazione e repulsione; (3) il PUNTO DI INVERSIONE "
           "di :6177 `centro = 0.5 * (pos_soglia + pos_tetto)`, che con soglia 3 pi e tetto 4 pi "
           "cade a 3.5 pi: il valore E' derivato (e' il punto medio), ma LA SCELTA DEL PUNTO "
           "MEDIO non lo e'. DUE COSE CHE NON SONO IL DIFETTO: la spinta e' MOLTIPLICATIVA in "
           "`d0` (scala LOCALE dell'arco), e questo e' GIA' CURATO -- la versione vecchia usava "
           "`median(self.d0)`, una statistica GLOBALE dentro un termine dichiarato Locale pura "
           "(`A2`, `A3`), e la cura di S05 e' del 2026-09-17; il gemello sull'altra spinta e' "
           "`S09-MEDIANA`, ANCORA APERTO. E la spinta va in UNA SOLA DIREZIONE: allarga `d0` e "
           "non lo restringe mai (la famiglia di `D31`). DECISIONE DI LUCA del " + OGGI + ": "
           "NESSUNA CURA ORA. Dopo `T3` si portano le OPZIONI, e sono tre -- i numeri si "
           "DERIVANO, oppure diventano PARAMETRI DICHIARATI, oppure la spinta si esprime in "
           "UNITA' DI `LAM` (che e' la scala di Planck del sistema, `A13`).")

# ============ 3c: MAX_NODI ==================================================================
nuova("MAX-NODI-FERMA",
      titolo_breve="MAX_NODI e' una guardia di MEMORIA che oggi cambia la FISICA in silenzio: "
                   "deve FERMARE il run",
      fonte_principale="doc/REGOLE_composizione_T3.md",
      stato="aperto", blocca_run_base="NO", tipo="cura", famiglia="?", avanzamento="IN CODA",
      stato_da="APERTA il " + OGGI + " su mandato di Luca (punto 3c). titolo_breve INTERO: "
               "`MAX_NODI` e' dichiarata dal codice stesso una GUARDIA DI MEMORIA e non di "
               "fisica, ma i tre siti che la leggono CAMBIANO LA FISICA IN SILENZIO invece di "
               "fermarsi: e' la forma di `A8` -- un ramo che salta senza dirlo e' un "
               "comportamento sconosciuto. La cura decisa da Luca e' UN controllo dello "
               "schedulatore che FERMA il run con un errore esplicito, MAI troncare.",
      nota="I TRE SITI, letti dal codice sul blob 1fc9235f: :6058 `if self.n >= MAX_NODI or not "
           "len(self.tw): return 0` -- la mitosi restituisce ZERO NASCITE e il run continua come "
           "se la fisica avesse deciso di non far nascere niente; :2924 `n = (MAX_NODI - self.n) "
           "if _sat else max(0, min(n, MAX_NODI - self.n))` -- la semina si TRONCA al numero che "
           "ci sta; :6481 `if COPPIA_MIT > 0.0 and self.n < MAX_NODI` -- il canale di Schwinger "
           "si spegne. E IL CODICE SA GIA' CHE E' SBAGLIATO: il commento di :1851 dice `se lo "
           "fosse, la misura e' da rifare con piu' memoria, non da troncare`. L'intenzione e' "
           "scritta e il codice fa l'opposto: e' esattamente la forma che `A8` esiste per "
           "impedire. PERCHE' `blocca_run_base = NO`: il default e' 4000000 nodi e le corse reali "
           "non ci arrivano (il pilota sta attorno a 12800 nodi), quindi oggi il run base non "
           "viene toccato. IL DIFETTO E' LA SILENZIOSITA', NON IL LIMITE. DECISIONE DI LUCA del "
           + OGGI + ": CONFERMATA la cura -- un controllo dello schedulatore che FERMA il run con "
           "un errore esplicito, MAI troncare, COL SUO CASO CHE DEVE FALLIRE; e in futuro "
           "`MAX_NODI` VA ELIMINATO.")

# ============ 3d: LA SOGLIA DI MITOSI ======================================================
nuova("MITOSI-SOGLIA-GRAD",
      titolo_breve="la soglia di mitosi si abbassa col gradiente di tempo proprio: ampiezza 0.3 "
                   "e tanh a mano",
      fonte_principale="doc/REGOLE_composizione_T3.md",
      stato="aperto", blocca_run_base="DA-DECIDERE", tipo="difetto", famiglia="?",
      avanzamento="IN CODA",
      stato_da="APERTA il " + OGGI + " su mandato di Luca (punto 3d). titolo_breve INTERO: la "
               "soglia critica della mitosi non e' costante: si ABBASSA dove il tempo proprio "
               "cambia piu' in fretta lungo l'arco, ed e' questo che dovrebbe far traslare il "
               "baricentro lungo la geodetica (il principio di equivalenza). La LEGGE e' "
               "interessante e la MODULAZIONE non e' derivata: ampiezza `0.3` e forma `tanh` sono "
               "scelte a mano.",
      nota="IL SITO, letto dal codice sul blob 1fc9235f: :6132 `soglia = soglia0 * (1.0 - 0.3 * "
           "np.tanh(grad_modula))`, con :6130 `grad_modula = np.abs(_rn[self.i] - _rn[self.j])` e "
           ":6128 `_rn = self._r_nodo_mitosi()`. COSA E' DERIVATO E COSA NO, e la distinzione e' "
           "il punto: `soglia0 = PHI_CRIT + pi = 3 pi` E' DERIVATA (quanto di olonomia piu' "
           "twist dipolare massimo, e se cambiano gli ingredienti si aggiorna da se'); l'AMPIEZZA "
           "`0.3` e la FORMA `tanh` NON LO SONO -- il commento del codice le dichiara come "
           "`modulazione limitata: la soglia scende di al piu' ~30%`, che e' una scelta, non una "
           "derivazione. UNA COSA GIA' CURATA, e non va ricontata come difetto: il gradiente si "
           "prende da `r` (il tempo proprio VERO) e non da `1/r` ne' da `|tw|` -- e' `CURA 2`, e "
           "il conto sta nel commento (`1/r` farebbe saturare il `tanh` a 1 esatto, cioe' un "
           "RISCALAMENTO COSTANTE della soglia, un parametro nascosto: `A1`, e `A11` cor.6 dice "
           "che un limite che satura e' un allarme). E ATTENZIONE AL NOME: la posizione sull'asse "
           "della torsione `1 + |tw|/PHI_CRIT` NON E' un tempo proprio, e si chiamava `tau_pp`: "
           "lo ha rinominato `D32`. DECISIONE DI LUCA del " + OGGI + ": si affronta DOPO `T3`. "
           "Nessuna cura ora.")

# ============ L'ATTRIBUZIONE: la strada (a) e' una DECISIONE DI LUCA =======================
aggiungi("MITOSI-NON-DIVISA", "nota",
         "ATTRIBUZIONE, e va scritta perche' l'avevo sbagliata: LA STRADA (a) -- la mitosi resta "
         "UNA voce AMBIGUA in `T2` e si separa in `T3` -- E' UNA DECISIONE DI LUCA DEL " + OGGI
         + ", NON MIA. In 3ba317f mi ero FERMATO ad aspettarla, come il mandato chiede; in "
         "5ac5150 l'ho considerata scelta e ho chiuso `T2` SENZA che Luca avesse risposto. Nel "
         "merito Luca la CONFERMA, ma la forma era sbagliata, e la regola che ho violato la "
         "scrive lui: UNA SCELTA LASCIATA A LUCA NON SI PRENDE AL SUO POSTO, NEMMENO QUANDO E' "
         "QUELLA RACCOMANDATA.")

io.open(TSV, "w", encoding="utf-8", newline=NL).write(
    NL.join(TAB.join(r) for r in RIGHE) + NL)

print("doc/INDICE_ID.tsv -- %d operazioni" % len(FATTE))
print("")
print("  %-20s %-22s %s" % ("voce", "come", "caratteri"))
for vid, come, n in FATTE:
    print("  %-20s %-22s %d" % (vid, come, n))
print("")
print("voci nell'indice: %d" % (len(RIGHE) - 1))
