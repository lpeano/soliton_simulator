# -*- coding: utf-8 -*-
"""SIGILLO — `GRAV_BIFASE = False` SPEGNE SOLO `S09`, e nient'altro. [G3, prima della prova]

⚠ NON MODIFICA IL SIMULATORE NE' IL DRIVER. Imposta la costante SUL MODULO dalla rigiocata, che
  e' esattamente il modo in cui la prova di spegnimento la impostera'.

⚠ OGNI BRACCIO GIRA IN UN PROCESSO SEPARATO, e non e' un dettaglio di comodo: la prima versione di
  questo sigillo girava i quattro bracci nello STESSO processo ed e' FALLITA su `T0`
  (`REFERTO_FALLITO_T0.txt`, commit `b6f3c83`). **LA CAUSA, dal sorgente** (`avvia_test`, `:6465`):

      def _f(_=None):
          if test["nome"] == nome: ferma_test(); return

  **`avvia_test` e' un INTERRUTTORE A LEVETTA**: la seconda chiamata, con la scena ancora attiva,
  la **FERMA** e torna **senza seminare le masse** -- i bracci si alternavano `n=2480 / n=900`.
  E oltre alla levetta, **la rete stessa sopravvive** fra un braccio e l'altro.
  **Un processo per braccio toglie il problema alla radice invece di aggirarlo.**

COSA DEVE DIMOSTRARE, e sono tre cose diverse che NON si sostituiscono:
  1. che lo spegnimento **SPEGNE** (`S09` sparisce);
  2. che spegne **SOLO** quello (tutti gli altri scrittori di `d0` conservano le stesse
     invocazioni, e cio' che sta A MONTE resta BYTE-IDENTICO);
  3. che **la memoria del moto non e' toccata** (`mem_mot` identico bit per bit).

⚠ I SITI CHE CONCATENANO NON SI CONFRONTANO SOLO PER LUNGHEZZA (rilievo di Luca, 2026-09-22):
  due bracci possono allungare `d0` DELLA STESSA QUANTITA' con VALORI DIVERSI, e un criterio che
  guarda solo i conti li darebbe per identici. Si confrontano anche la **CODA NUOVA** (i valori
  oltre la vecchia lunghezza) e l'**INTERO `d0`** dopo la scrittura -- quest'ultimo perche' `S06`
  fa `concatenate([d0[keep], d0new])`, cioe' TOGLIE archi e poi appende: **la parte conservata
  NON e' un prefisso di `prima`**, e un cambiamento LI' non si vedrebbe guardando solo la coda.

⚠ IL CONFRONTO SI FA SU FIRME (`sha1` dei byte), NON SU `max|delta|`, ed e' un criterio PIU'
  FORTE: `max|delta| = 0` sopravvive a due `NaN` nello stesso posto e a `+0.0` contro `-0.0`,
  l'identita' dei byte no. Quando una firma differisce si stampano **cinque scalari** (somma,
  somma dei moduli, min, max, forma) cosi' chi legge vede **di quanto**, non solo **che**.

⚠ E UNA DISTINZIONE CHE VA FATTA E NON NASCOSTA, sulla COESIONE.
  L'ordine dei diciannove siti di scrittura di `d0`, VERIFICATO dal sorgente, e':
      S01 S02 S03 S04 P1 S05 P2 S06 S07 S08 P3 | S09 S10 P4 | S11 P5 S12 P6 P7
                                    a monte       GRAVITA'      a valle
  **`S12_coesione` sta A VALLE del blocco della gravita'.** Quindi, spenta la gravita', la
  coesione **vede un `d0` diverso** e i suoi incrementi **cambiano**. **Questo non significa che
  l'interruttore tocchi la LEGGE della coesione**, e il sigillo non lo afferma: afferma che
  **il numero di invocazioni e' lo stesso** e che **la legge non e' gated su `GRAV_BIFASE`**, e
  quest'ultima la dimostra **strutturalmente** (`T5`), non per campione.
  **Dire «la coesione non e' toccata» senza questa distinzione sarebbe FALSO.**

⚠ `P1-sexies`: i criteri sono collaudati PRIMA su casi a risposta nota, **e il piu' importante e'
  quello che DEVE fallire** -- uno spegnimento che tocca ANCHE un altro scrittore. Il caso che
  deve fallire e' girato **sul codice vero**, non simulato: `MEM_HEBB = False`, cioe' proprio lo
  spegnimento che il mandato VIETA di usare.
ASCII PURO.
"""
import ast
import hashlib
import io
import json
import os
import subprocess
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, RADICE)
DEST = os.path.join(_QUI, "_sig_spegni_grav")
OUT = os.path.join(DEST, "REFERTO.txt")

PASSI = 3
BRACCIO = None
for _a in sys.argv[1:]:
    if _a.startswith("--passi="):
        PASSI = int(_a.split("=", 1)[1])
    if _a.startswith("--braccio="):
        BRACCIO = _a.split("=", 1)[1]

# LA CONFIGURAZIONE DELLA VALIDAZIONE, identica a quella di `G2`
ARGV = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
        "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
        "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
        "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
        "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--chi-coop",
        "--coes-adim", "--plast-din", "--viriale", "--olon-part",
        "--peq-esatto", "--peq-nascita-locale", "--scala-min-passo", "--coes-causale",
        "--anom-simm", "--invarianti=on"]

# L'ordine dei siti, VERIFICATO dal sorgente il 2026-09-22 (righe 2464..6030).
A_MONTE = ("S01_archi_nuovi", "S02_rilass_visco", "S03_diff_guscio", "S04_rilass_TAU_P",
           "P1_dopo_rilass", "S05_spinta_locale", "P2_dopo_spinta", "S06_mitosi",
           "S07_schwinger", "S08_proj", "P3_dopo_proj")
GRAVITA = ("S09_spinta_med", "S10_grav_med", "P4_dopo_grav")
A_VALLE = ("S11_flusso", "P5_dopo_flusso", "S12_coesione", "P6_dopo_coesione", "P7_dopo_4917")
# I SITI CHE CONCATENANO: cambiano la LUNGHEZZA di `d0`, quindi il delta elemento-per-elemento
# NON ESISTE. E' la stessa convenzione che in `Z102` li fa comparire con `n/d`.
# ⚠ Non si confrontano per FIRMA -- si confrontano per la COPPIA DI LUNGHEZZE. Trattarli come
#   "assenti" faceva fallire `T0` su un'assenza STRUTTURALE e ATTESA (2026-09-22).
CONCATENANO = ("S01_archi_nuovi", "S06_mitosi", "S07_schwinger")

# i quattro bracci: (nome, spegni_grav, spegni_hebb)
BRACCI = (("ON", False, False), ("ON-bis", False, False),
          ("OFF", True, False), ("HEBB", False, True))


# ------------------------------------------------------------------ I CRITERI, isolati
def firma(a):
    """La FIRMA di un array: `sha1` dei byte, piu' cinque scalari per dire DI QUANTO differisce.

    ⚠ Piu' forte di `max|delta| = 0`, che sopravvive a due `NaN` nello stesso posto e a `+0.0`
      contro `-0.0`. I cinque scalari servono a chi legge un FAIL: senza, saprebbe solo CHE.
    """
    if a is None:
        return None
    a = np.ascontiguousarray(np.asarray(a))
    fin = a[np.isfinite(a)] if a.size else a
    return {"sha1": hashlib.sha1(a.tobytes()).hexdigest()[:12],
            "forma": list(a.shape), "dtype": str(a.dtype),
            "somma": float(np.sum(fin)) if fin.size else 0.0,
            "somma_abs": float(np.sum(np.abs(fin))) if fin.size else 0.0,
            "min": float(np.min(fin)) if fin.size else 0.0,
            "max": float(np.max(fin)) if fin.size else 0.0,
            "n_non_finiti": int(a.size - fin.size)}


def identiche(fa, fb):
    """Due catture sono la stessa cosa?

    ⚠ TRE casi, e mescolarli e' stato un difetto vero (`T0` fallito il 2026-09-22):
      * due FIRME        -> identita' dei BYTE e della forma;
      * due CONCATENA    -> stessa coppia di lunghezze. L'assenza del delta e' STRUTTURALE e
                            ATTESA, non un dato mancante: sono i siti che allungano `d0`;
      * una di ciascuna, oppure un `None` -> **NON e' identita'**. Due ASSENZE non fanno
                            un'uguaglianza, e un sito che cambia natura fra i due bracci e' un
                            SEGNALE, non un pareggio.
    """
    if fa is None or fb is None:
        return False
    ca, cb = fa.get("concatena"), fb.get("concatena")
    if ca or cb:
        if not (ca and cb):
            return False
        # ⚠ LE LUNGHEZZE DA SOLE NON BASTANO -- rilievo di Luca, 2026-09-22. Due bracci possono
        #   allungare `d0` DELLA STESSA QUANTITA' con VALORI DIVERSI, e il criterio li avrebbe
        #   dati per identici. Si confrontano anche:
        #     `coda`  -- la firma dei valori OLTRE la vecchia lunghezza, cioe' la coda nuova;
        #     `tutto` -- la firma dell'INTERO `d0` dopo la scrittura.
        #   Servono ENTRAMBE: `coda` e' cio' che Luca ha nominato, ma `S06` fa
        #   `d0 = concatenate([d0[keep], d0new])`, cioe' TOGLIE archi e poi appende -- la parte
        #   conservata NON e' un prefisso di `prima`. `tutto` copre anche un cambiamento LI'.
        #   ⚠ se `d0` si ACCORCIA la coda non esiste in NESSUNO dei due, e li' l'assenza e'
        #     determinata dalla coppia di lunghezze, che e' gia' confrontata: due `None` valgono
        #     come uguali SOLO in questo caso, e solo perche' `da`/`a` coincidono gia'.
        _ka, _kb = fa.get("coda"), fb.get("coda")
        coda_ok = (_ka is None and _kb is None) or identiche(_ka, _kb)
        return (fa.get("da") == fb.get("da") and fa.get("a") == fb.get("a")
                and coda_ok and identiche(fa.get("tutto"), fb.get("tutto")))
    return fa["sha1"] == fb["sha1"] and fa["forma"] == fb["forma"]


def solo_quello(cnt_a, cnt_b, esenti):
    """I siti NON esenti hanno le stesse invocazioni nei due bracci? Ritorna i colpevoli.
    E' il criterio di `T2`, ed e' quello che il collaudo deve saper far fallire."""
    fuori = []
    for s in sorted(set(cnt_a) | set(cnt_b)):
        if s in esenti:
            continue
        if cnt_a.get(s, 0) != cnt_b.get(s, 0):
            fuori.append((s, cnt_a.get(s, 0), cnt_b.get(s, 0)))
    return fuori


def gate_unico(percorso):
    """`T5`, LA PROVA STRUTTURALE: quante RAMIFICAZIONI dipendono da `GRAV_BIFASE`?

    Non e' un campione: e' il sorgente. Si costruisce l'AST e si cercano TUTTI i nodi `If`/`IfExp`
    il cui TEST nomina `GRAV_BIFASE`. Se ce n'e' ESATTAMENTE UNO, **nessun'altra legge PUO' essere
    gated su quel nome**, e l'affermazione «spegne solo la gravita'» smette di dipendere
    da quanti passi si sono girati.
    """
    with io.open(percorso, encoding="utf-8") as f:
        albero = ast.parse(f.read(), percorso)
    rami, assegn, tutti = [], [], []
    for nodo in ast.walk(albero):
        if isinstance(nodo, (ast.If, ast.IfExp)):
            if any(isinstance(x, ast.Name) and x.id == "GRAV_BIFASE"
                   for x in ast.walk(nodo.test)):
                rami.append(nodo.lineno)
        elif isinstance(nodo, ast.Assign):
            for t in nodo.targets:
                if isinstance(t, ast.Name) and t.id == "GRAV_BIFASE":
                    assegn.append(nodo.lineno)
        elif isinstance(nodo, ast.Name) and nodo.id == "GRAV_BIFASE":
            tutti.append(nodo.lineno)
    return sorted(rami), sorted(assegn), sorted(set(tutti))


def collaudo(W):
    """`P1-sexies`. I criteri si collaudano su casi a risposta NOTA, PRIMA di usarli."""
    W("COLLAUDO DEI CRITERI su casi a RISPOSTA NOTA (`P1-sexies`), PRIMA di sigillare\n")
    W("-" * 100 + "\n")
    e = []
    base = {"S08_proj": 3, "S09_spinta_med": 3, "S11_flusso": 3, "S12_coesione": 3}
    esenti = set(GRAVITA)

    bene = dict(base); bene["S09_spinta_med"] = 0
    f1 = solo_quello(base, bene, esenti)
    ok1 = (len(f1) == 0)
    W("K1 spegnimento CHIRURGICO (solo `S09` sparisce) -> atteso NESSUN colpevole\n")
    W("     colpevoli: %s  -> %s\n"
      % (f1 if f1 else "nessuno", "OK" if ok1 else "*** FALSO ALLARME ***"))
    e.append(ok1)

    # IL CASO CHE DEVE FALLIRE, e non e' quello catastrofico: e' quello CHIRURGICO SBAGLIATO.
    male = dict(base); male["S09_spinta_med"] = 0; male["S11_flusso"] = 0
    f2 = solo_quello(base, male, esenti)
    ok2 = any(s == "S11_flusso" for s, _a, _b in f2)
    W("K2 IL CASO CHE DEVE FALLIRE: lo spegnimento tocca ANCHE `S11_flusso`\n")
    W("     colpevoli: %s\n" % f2)
    W("     atteso: `S11_flusso` segnalato -> %s\n"
      % ("OK: il criterio VEDE uno spegnimento troppo largo"
         if ok2 else "*** CIECO: direbbe `spegne solo S09` senza saperlo ***"))
    e.append(ok2)

    extra = dict(base); extra["S09_spinta_med"] = 0; extra["S05_spinta_locale"] = 7
    f3 = solo_quello(base, extra, esenti)
    ok3 = any(s == "S05_spinta_locale" for s, _a, _b in f3)
    W("K3 un sito che COMPARE invece di sparire -> atteso segnalato\n")
    W("     colpevoli: %s  -> %s\n" % (f3, "OK" if ok3 else "*** NON LO VEDE ***"))
    e.append(ok3)

    # --- la FIRMA: tre casi, e il secondo e' quello che un criterio su `max|delta|` SBAGLIEREBBE
    a = np.linspace(0.0, 1.0, 50)
    ok4 = identiche(firma(a), firma(a.copy()))
    W("K4 FIRMA: due array identici -> stessa firma  -> %s\n"
      % ("OK" if ok4 else "*** NON RICONOSCE L'IDENTITA' ***"))
    e.append(ok4)

    z1 = np.array([0.0, 1.0]); z2 = np.array([-0.0, 1.0])
    max_delta = float(np.max(np.abs(z1 - z2)))
    ok5 = (not identiche(firma(z1), firma(z2))) and (max_delta == 0.0)
    W("K5 IL CASO CHE UN CRITERIO SU `max|delta|` SBAGLIEREBBE: `+0.0` contro `-0.0`\n")
    W("     max|delta| = %.3e  (un criterio su max|delta| direbbe IDENTICI)\n" % max_delta)
    W("     le firme: %s  -> %s\n"
      % ("DIVERSE" if not identiche(firma(z1), firma(z2)) else "uguali",
         "OK: la firma e' PIU' STRETTA" if ok5 else "*** la firma non e' piu' stretta ***"))
    e.append(ok5)

    ok6 = (not identiche(firma(np.ones(5)), firma(np.ones(7))))
    W("K6 FORME DIVERSE -> firme diverse, MAI identita' per mancanza di confronto -> %s\n"
      % ("OK" if ok6 else "*** LO ZERO SAREBBE AMBIGUO ***"))
    e.append(ok6)

    def _cc(da, a, coda, tutto):
        return {"concatena": True, "da": da, "a": a,
                "coda": firma(np.asarray(coda, dtype=float)),
                "tutto": firma(np.asarray(tutto, dtype=float))}

    cc1 = _cc(100, 104, [1.0, 2.0, 3.0, 4.0], np.arange(104, dtype=float))
    cc2 = _cc(100, 104, [1.0, 2.0, 3.0, 4.0], np.arange(104, dtype=float))
    cc3 = _cc(100, 106, [1.0, 2.0, 3.0, 4.0, 5.0, 6.0], np.arange(106, dtype=float))
    # IL CASO DI LUCA: STESSE LUNGHEZZE, CONTENUTO DELLA CODA DIVERSO.
    cc4 = _cc(100, 104, [1.0, 2.0, 3.0, 9.0], np.arange(104, dtype=float))
    # e il suo gemello: coda uguale, ma cambia qualcosa NELLA PARTE CONSERVATA.
    _t5 = np.arange(104, dtype=float); _t5[7] = -1.0
    cc5 = _cc(100, 104, [1.0, 2.0, 3.0, 4.0], _t5)
    ok8 = identiche(cc1, cc2)
    ok9 = (not identiche(cc1, cc3))
    ok10 = (not identiche(cc1, firma(np.ones(4))))
    W("K8 i siti che CONCATENANO: stessa coppia di lunghezze -> IDENTICI -> %s\n"
      % ("OK" if ok8 else "*** un'assenza STRUTTURALE e ATTESA farebbe fallire T0 ***"))
    W("K9 lunghezze DIVERSE (100->104 contro 100->106) -> NON identici -> %s\n"
      % ("OK" if ok9 else "*** non vedrebbe una mitosi diversa ***"))
    W("K10 un CONCATENA contro una FIRMA -> NON identici -> %s\n"
      % ("OK" if ok10 else "*** un sito che cambia NATURA passerebbe per uguale ***"))
    ok11 = (not identiche(cc1, cc4))
    ok12 = (not identiche(cc1, cc5))
    W("K11 IL CASO DI LUCA: STESSE LUNGHEZZE (100->104), CODA DIVERSA -> NON identici -> %s\n"
      % ("OK" if ok11 else
         "*** due code DIVERSE passerebbero per uguali: il criterio guarderebbe solo i CONTI ***"))
    W("K12 stesse lunghezze e stessa coda, ma cambia la parte CONSERVATA -> NON identici -> %s\n"
      % ("OK" if ok12 else "*** un cambiamento dentro `d0[keep]` sfuggirebbe ***"))
    e += [ok8, ok9, ok10, ok11, ok12]

    ok7 = (not identiche(None, None))
    W("K7 due ASSENZE non sono un'identita' -> %s\n"
      % ("OK" if ok7 else "*** due `None` passerebbero per uguali ***"))
    e.append(ok7)

    ok = all(e)
    W("-" * 100 + "\n")
    W("  -> i criteri %s\n\n"
      % ("PASSANO: si sigilla" if ok else "*** NON PASSANO: NON sigillo ***"))
    return ok


# ------------------------------------------------------------------ IL BRACCIO (processo figlio)
def braccio(nome):
    """Una rigiocata dalla semina, in un processo TUTTO SUO. Scrive la cattura in JSON."""
    _sp = dict((n, (g, h)) for n, g, h in BRACCI)
    spegni_grav, spegni_hebb = _sp[nome]
    os.chdir(RADICE)
    sys.argv = list(ARGV)
    import soliton_simulator as S
    S.TRACCIA_D0 = False                    # ⚠ spenta DURANTE la semina: senno' i contatori
    a = S._cli(); S._applica_regime(a); S._applica_flag(a)   # conterebbero le calibrazioni
    S.GRAV_BIFASE = (not spegni_grav)       # <- IMPOSTATA SUL MODULO, come fara' la prova
    S.MEM_HEBB = (not spegni_hebb)
    np.random.seed(20260922)                # vedi la nota nel referto
    S._NMASSE_VIDEO["n"] = 3; S._NMASSE_VIDEO["sep"] = 4.0; S._NMASSE_VIDEO["size"] = None
    S.avvia_test("N-MASSE")()
    net = S.net
    S.stato["nframe"] = 0

    cnt, primo = {}, {}
    stato = {"passo": 0}

    def traccia(self, sito, prima, pavimento=None):
        cnt[sito] = cnt.get(sito, 0) + 1
        if stato["passo"] == 1 and sito not in primo:
            dopo = np.asarray(self.d0, dtype=float)
            pri = np.asarray(prima, dtype=float)
            if len(pri) == len(dopo):
                primo[sito] = firma(dopo - pri)
            else:
                # ⚠ il delta elemento-per-elemento non esiste, ma il CONTENUTO va confrontato
                #   lo stesso: lunghezze uguali con valori diversi devono risultare DIVERSE.
                primo[sito] = {"concatena": True, "da": len(pri), "a": len(dopo),
                               "coda": firma(dopo[len(pri):]) if len(dopo) > len(pri) else None,
                               "tutto": firma(dopo)}
    S.Rete._traccia_d0 = traccia
    S.TRACCIA_D0 = True

    PPF = int(S.PASSI_PER_FRAME)
    mm1 = d01 = None
    for k in range(1, PASSI + 1):
        stato["passo"] = k
        if (k - 1) % PPF == 0:
            S.passo_test()
        S.scuoti_vuoto(net); net.step(); net.mitosi()
        net.rilassa_disegno(); net.memoria_hebbiana_moto()
        if k == 1:
            mm1 = firma(np.asarray(net.mem_mot, dtype=float))
            d01 = firma(np.asarray(net.d0, dtype=float))
    cap = {"nome": nome, "grav": bool(S.GRAV_BIFASE), "hebb": bool(S.MEM_HEBB),
           "n": int(net.n), "archi": int(len(net.i)), "passi": PASSI,
           "cnt": cnt, "primo": primo, "mem_mot": mm1, "d0": d01}
    with io.open(os.path.join(DEST, "cap_%s.json" % nome), "w", encoding="utf-8") as f:
        f.write(json.dumps(cap, indent=1))
    print("[braccio %s] n=%d archi=%d siti=%d" % (nome, net.n, len(net.i), len(cnt)))
    return 0


# ------------------------------------------------------------------ il GENITORE
def main():
    try:
        os.makedirs(DEST)
    except OSError:
        pass
    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    W = o.write
    W("# SIGILLO -- `GRAV_BIFASE = False` SPEGNE SOLO `S09`\n")
    W("# prima della prova di spegnimento `G3`. Nessuna modifica a simulatore ne' driver.\n")
    W("# %d passi dalla semina per braccio, configurazione della validazione.\n" % PASSI)
    W("# ⚠ OGNI BRACCIO IN UN PROCESSO SEPARATO: `avvia_test` e' un interruttore a LEVETTA\n")
    W("#   (`:6465`), e in-process il secondo braccio nasceva SENZA MASSE. Vedi\n")
    W("#   `REFERTO_FALLITO_T0.txt` e il commit `b6f3c83`.\n#\n")
    if not collaudo(W):
        o.close(); print(io.open(OUT, encoding="utf-8").read()); return 1

    import hashlib as _h
    blob = _h.sha1(
        open(os.path.join(RADICE, "soliton_simulator.py"), "rb").read()).hexdigest()[:8]
    W("blob simulatore (sha1 byte grezzi) %s\n\n" % blob)

    t0 = time.time()
    W("I QUATTRO BRACCI, ciascuno in un processo suo:\n")
    cap = {}
    for nome, _g, _hh in BRACCI:
        p = os.path.join(DEST, "cap_%s.json" % nome)
        if os.path.exists(p):
            os.remove(p)
        r = subprocess.run([sys.executable, os.path.abspath(__file__),
                            "--braccio=%s" % nome, "--passi=%d" % PASSI],
                           cwd=RADICE, capture_output=True, text=True)
        if not os.path.exists(p):
            W("  *** il braccio %s NON ha prodotto la cattura. uscita=%d ***\n"
              % (nome, r.returncode))
            W("  %s\n" % (r.stderr or "")[-2000:])
            o.close(); print(io.open(OUT, encoding="utf-8").read()); return 1
        with io.open(p, encoding="utf-8") as f:
            cap[nome] = json.load(f)
        c = cap[nome]
        W("  %-8s GRAV_BIFASE=%-5s MEM_HEBB=%-5s  n=%-6d archi=%-7d siti=%d\n"
          % (nome, c["grav"], c["hebb"], c["n"], c["archi"], len(c["cnt"])))
    W("  (%.1f s)\n\n" % (time.time() - t0))

    ON, ONB, OFF, HEBB = cap["ON"], cap["ON-bis"], cap["OFF"], cap["HEBB"]
    esiti = []

    def esito(nome, ok, riga):
        esiti.append((nome, ok))
        W("%-5s %-4s %s\n" % (nome, "PASS" if ok else "FAIL", riga))

    W("=" * 100 + "\nI CRITERI\n" + "=" * 100 + "\n")

    # ---- T0: senza questo, uno zero non significa niente
    f0 = solo_quello(ON["cnt"], ONB["cnt"], set())
    div = [s for s in ON["primo"] if not identiche(ON["primo"][s], ONB["primo"].get(s))]
    ok0 = (len(f0) == 0 and not div
           and identiche(ON["mem_mot"], ONB["mem_mot"])
           and identiche(ON["d0"], ONB["d0"]) and ON["n"] == ONB["n"])
    esito("T0", ok0, "RIPRODUCIBILITA': due bracci ON separati coincidono? invocazioni "
                     "diverse=%d, siti con firma diversa=%d, n %d==%d, mem_mot %s, d0 %s"
                     % (len(f0), len(div), ON["n"], ONB["n"],
                        "=" if identiche(ON["mem_mot"], ONB["mem_mot"]) else "DIVERSO",
                        "=" if identiche(ON["d0"], ONB["d0"]) else "DIVERSO"))
    if not ok0:
        W("\n*** T0 FALLISCE: i due bracci ON NON coincidono, quindi QUALUNQUE differenza\n")
        W("    misurata sotto sarebbe indistinguibile dalla deriva. IL SIGILLO SI FERMA. ***\n")
        if div:
            W("    siti con firma diversa: %s\n" % div[:10])
        o.close(); print(io.open(OUT, encoding="utf-8").read()); return 1

    # ---- T1: lo spegnimento SPEGNE
    on9 = ON["cnt"].get("S09_spinta_med", 0)
    off9 = OFF["cnt"].get("S09_spinta_med", 0)
    off10 = OFF["cnt"].get("S10_grav_med", 0)
    off4 = OFF["cnt"].get("P4_dopo_grav", 0)
    ok1 = (on9 > 0) and (off9 == 0) and (off10 == 0) and (off4 == 0)
    esito("T1", ok1, "LO SPEGNIMENTO SPEGNE: S09 ON=%d -> OFF=%d ; S10 OFF=%d ; P4 OFF=%d"
                     % (on9, off9, off10, off4))

    # ---- T2: spegne SOLO quello
    f2 = solo_quello(ON["cnt"], OFF["cnt"], set(GRAVITA))
    ok2 = (len(f2) == 0)
    esito("T2", ok2, "SPEGNE SOLO QUELLO: siti (non gravita') con invocazioni diverse = %d %s"
                     % (len(f2), f2 if f2 else ""))

    # ---- T3: byte-identita' A MONTE, al primo passo
    fuori = [s for s in A_MONTE
             if s in ON["primo"] and not identiche(ON["primo"][s], OFF["primo"].get(s))]
    ok3 = (len(fuori) == 0)
    esito("T3", ok3, "BYTE-IDENTITA' A MONTE al passo 1: siti confrontati=%d, con firma "
                     "DIVERSA=%d %s"
                     % (len([s for s in A_MONTE if s in ON["primo"]]), len(fuori),
                        fuori if fuori else ""))
    for s in A_MONTE:
        fa = ON["primo"].get(s)
        if fa is None:
            W("      %-20s non invocato al passo 1\n" % s)
            continue
        ug = "IDENTICO" if identiche(fa, OFF["primo"].get(s)) else "*** DIVERSO ***"
        if fa.get("concatena"):
            # ⚠ i siti che CONCATENANO non hanno un delta: si mostra la COPPIA DI LUNGHEZZE.
            #   Stamparli come firme faceva SCHIANTARE il referto su `KeyError: 'sha1'` DOPO che
            #   T0..T3 erano gia' passati -- un crash nella STAMPA, non in un criterio.
            fb = OFF["primo"].get(s) or {}
            _ka = (fa.get("coda") or {}).get("sha1", "-")
            _kb = (fb.get("coda") or {}).get("sha1", "-")
            _ta = (fa.get("tutto") or {}).get("sha1", "-")
            _tb = (fb.get("tutto") or {}).get("sha1", "-")
            W("      %-20s CONCATENA ON %s->%s OFF %s->%s  coda %s/%s  tutto %s/%s  %s\n"
              % (s, fa.get("da"), fa.get("a"), fb.get("da"), fb.get("a"),
                 _ka, _kb, _ta, _tb, ug))
        else:
            W("      %-20s sha1 %s  forma %s  somma %+.6e  %s\n"
              % (s, fa["sha1"], fa["forma"], fa["somma"], ug))

    # ---- T4: la MEMORIA DEL MOTO non e' toccata
    ok4 = identiche(ON["mem_mot"], OFF["mem_mot"])
    esito("T4", ok4, "MEMORIA DEL MOTO intatta: mem_mot ON sha1 %s forma %s  vs OFF sha1 %s -> %s"
                     % (ON["mem_mot"]["sha1"], ON["mem_mot"]["forma"],
                        OFF["mem_mot"]["sha1"], "IDENTICO" if ok4 else "DIVERSO"))

    # ---- T5: la prova STRUTTURALE
    rami, assegn, tutti = gate_unico(os.path.join(RADICE, "soliton_simulator.py"))
    ok5 = (len(rami) == 1)
    esito("T5", ok5, "GATE UNICO (AST): ramificazioni che dipendono da GRAV_BIFASE = %d, righe %s"
                     % (len(rami), rami))
    W("      assegnamenti: righe %s ; tutte le occorrenze del NOME: righe %s\n" % (assegn, tutti))
    W("      -> se la ramificazione e' UNA SOLA, nessun'altra legge PUO' essere gated su quel\n")
    W("         nome, e l'affermazione non dipende piu' da quanti passi si sono girati.\n")

    # ---- T6: IL CASO CHE DEVE FALLIRE, sul codice VERO
    f6 = solo_quello(ON["cnt"], HEBB["cnt"], set(GRAVITA))
    ok6 = (len(f6) > 0)
    esito("T6", ok6, "IL CASO CHE DEVE FALLIRE -- `MEM_HEBB=False`: siti toccati OLTRE la "
                     "gravita' = %d" % len(f6))
    for s, a_, b_ in f6:
        W("      %-20s ON=%-4d HEBB=%-4d\n" % (s, a_, b_))
    W("      -> `T2` su questo braccio FALLISCE, come deve. Se `T2` lo desse per buono, direbbe\n")
    W("         \"spegne solo S09\" SENZA POTERLO SAPERE. Ed e' anche la prova, SUL CODICE VERO,\n")
    W("         di perche' il mandato VIETA `MEM_HEBB=False` come prova di spegnimento.\n")

    # ---- la DISTINZIONE sulla coesione, dichiarata e non nascosta
    W("\n" + "-" * 100 + "\n")
    W("LA COESIONE: cosa il sigillo AFFERMA e cosa NO\n")
    W("-" * 100 + "\n")
    c_on = ON["cnt"].get("S12_coesione", 0); c_off = OFF["cnt"].get("S12_coesione", 0)
    s12on = ON["primo"].get("S12_coesione"); s12off = OFF["primo"].get("S12_coesione")
    W("  `S12_coesione` sta A VALLE del blocco della gravita' (ordine verificato dal sorgente).\n")
    W("  invocazioni ON=%d OFF=%d -> %s\n"
      % (c_on, c_off, "UGUALI" if c_on == c_off else "DIVERSE"))
    if s12on and s12off and "somma" in s12on and "somma" in s12off:
        W("  al passo 1: somma ON %+.6e  OFF %+.6e   firme %s\n"
          % (s12on["somma"], s12off["somma"],
             "UGUALI" if identiche(s12on, s12off) else "DIVERSE"))
    elif s12on and s12off:
        W("  al passo 1: e' un sito che CONCATENA, quindi niente somma: %s\n"
          % ("coppie di lunghezze UGUALI" if identiche(s12on, s12off) else "DIVERSE"))
    else:
        W("  al passo 1: non invocato in almeno uno dei due bracci (ON=%s OFF=%s)\n"
          % (s12on is not None, s12off is not None))
    W("  -> IL SIGILLO AFFERMA: la coesione gira lo STESSO NUMERO DI VOLTE, e la sua legge NON e'\n")
    W("     gated su `GRAV_BIFASE` (`T5`: la ramificazione e' UNA SOLA).\n")
    W("  -> IL SIGILLO NON AFFERMA che i suoi incrementi siano identici: NON LO SONO, e NON\n")
    W("     DEVONO esserlo. La coesione vede un `d0` diverso perche' la gravita' non lo ha\n")
    W("     spostato. E' FISICA CHE PROPAGA, non l'interruttore che la tocca.\n")
    W("     Dire \"la coesione non e' toccata\" senza questa distinzione sarebbe FALSO.\n")

    n_ok = sum(1 for _n, k in esiti if k)
    W("\n" + "=" * 100 + "\nESITO: %d/%d\n" % (n_ok, len(esiti)) + "=" * 100 + "\n")
    if n_ok == len(esiti):
        W("*** SIGILLO PASSATO: `GRAV_BIFASE = False` spegne SOLO la gravita' bifase.\n")
        W("    La prova di spegnimento `G3` puo' partire. ***\n")
    else:
        W("*** SIGILLO FALLITO: la prova di spegnimento NON parte. ***\n")
    W("\nLIMITI: %d passi per braccio, UN seme, UNA scena. `T2` e' un confronto di CONTEGGI su\n"
      % PASSI)
    W("  pochi passi; cio' che rende il sigillo conclusivo NON e' il numero di passi ma `T5`,\n")
    W("  che e' STRUTTURALE e non campionario.\n")
    W("NOTA: `np.random.seed()` e' rimesso identico in ogni braccio. Il generatore e' PER-RETE\n")
    W("  (`self.rng = np.random.default_rng(seed)`, `:1430`), quindi in teoria non serve; se un\n")
    W("  percorso usasse quello GLOBALE, senza non sarebbero confrontabili. `T0` e' cio' che lo\n")
    W("  verifica invece di darlo per scontato.\n")
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0 if n_ok == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(braccio(BRACCIO) if BRACCIO else main())
