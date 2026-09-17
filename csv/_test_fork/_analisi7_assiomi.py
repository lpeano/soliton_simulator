# -*- coding: utf-8 -*-
"""(7) SOLO ANALISI -- quattro grandezze contro gli ASSIOMI. **NESSUN CABLAGGIO.**

  _tau        :2150-2151   TAU_A * max(_dens/median(_dens), 0.05)
  ZETA_LOC    :3185-3187   ZETA_M / (1 + max(rho/median(rho) - 1, 0))
  u_nodo      :2607        I / media_dei_vicini
  mediana r   :1939-1943   r / r_unit, con f normalizzato su median(|f|)

Per ognuna: (a) quale assioma tocca, (b) IL PUNTO FISSO -- cioe' se la grandezza puo' anche solo
in linea di principio muoversi dove sta la maggioranza (CLAUDE.md par.9, P4), (c) la frazione al
pavimento, dove c'e' (A3b).

E c'e' una domanda che questi quattro casi possono DECIDERE: doc/ASSIOMI.md, APERTO #2, si chiede
se **A3 sia un caso particolare di A2**. Basta un caso che soddisfi A2 e violi A3 per rispondere no.
Dati: i .pkl gia' committati. ASCII PURO. Nessun run.
"""
import sys as _sys_enc  # PRESIDIO ENCODING (CLAUDE.md): lo stdout di Windows e' cp1252 e
# uccide qualunque print con un carattere non-ASCII. E' successo SETTE volte, l'ultima allo
# script che stava CONTANDO le occorrenze. Il `# -*- coding: utf-8 -*-` NON basta: riguarda il
# SORGENTE, non lo STDOUT. Questa riga lo risolve alla radice.
try:
    _sys_enc.stdout.reconfigure(encoding="utf-8")
    _sys_enc.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import glob
import os
import pickle

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = sorted(glob.glob(os.path.join(HERE, "_vuoto_s2ON_s?.pkl")))
TAU_A = 50.0
ZETA_M = 1.0

print("=" * 118)
print("(7) ANALISI -- quattro grandezze contro A1/A2/A3. NESSUN CABLAGGIO.")
print("=" * 118)

tau_med, tau_pav, zl_med, zl_zero, u_med, u_sopra = [], [], [], [], [], []
_senza_filtro = []
for f in FILES:
    A = pickle.load(open(f, "rb"))["attrs"]
    I = np.abs(np.asarray(A["psi"])) ** 2
    n = len(I)
    i = np.asarray(A["i"], int); j = np.asarray(A["j"], int)

    # --- _tau : normalizzato sulla MEDIANA del proprio insieme, con pavimento 0.05
    dens = I[I > 1e-6]
    if len(dens):
        rif = max(float(np.median(dens)), 1e-6)
        t = TAU_A * np.maximum(I / rif, 0.05)
        tau_med.append(float(np.median(t)) / TAU_A)
        tau_pav.append(float(np.mean(I / rif <= 0.05)))
        _rif2 = max(float(np.median(I)), 1e-6)          # CONTROPROVA: mediana su TUTTI i nodi
        _senza_filtro.append("%.6f" % float(np.median(I / _rif2)))

    # --- ZETA_LOC : eccesso sulla mediana degli ARCHI
    rho = 0.5 * (I[i] + I[j])
    mr = max(float(np.median(rho)), 1e-9)
    ecc = np.maximum(rho / mr - 1.0, 0.0)
    zl = ZETA_M / (1.0 + ecc)
    zl_med.append(float(np.median(zl)))
    zl_zero.append(float(np.mean(ecc == 0.0)))

    # --- u_nodo : normalizzato sulla MEDIA DEI VICINI (locale!)
    deg = np.maximum(np.bincount(i, minlength=n) + np.bincount(j, minlength=n), 1)
    sv = np.bincount(i, I[j], minlength=n) + np.bincount(j, I[i], minlength=n)
    mv = sv / deg
    u = I / np.maximum(mv, 1e-9)
    u_med.append(float(np.median(u)))
    u_sopra.append(float(np.mean(u > 1.0)))

print("""
--- (a) `_tau` (:2150-2151)  TAU_A * max(dens/median(dens), 0.05) ---
  ASSIOMI: A2 (median globale su percorso fisico) + A3 (normalizzata sulla PROPRIA mediana)
           + A3b (pavimento 0.05).""")
print("  tau_mediano / TAU_A  per seme: %s" % ["%.4f" % x for x in tau_med])
print("  frazione AL PAVIMENTO (dens/rif <= 0.05): %s   media %.2f %%"
      % (["%.2f %%" % (100 * x) for x in tau_pav], 100 * float(np.mean(tau_pav))))
print("  CONTROPROVA -- la stessa quantita' con la mediana su TUTTI i nodi: %s" % _senza_filtro)
print("""
  !! DUE COSE CHE AVEVO SCRITTO E CHE LA MISURA SMENTISCE. LA SECONDA CORREGGE CLAUDE.md par.9.

  (1) "il pavimento e' il comportamento di quasi tutti i nodi": FALSO a 300 passi. Misurato
      19.58 % in media (8.8 % - 45.3 %). E' una frazione grande, non la maggioranza. La voce di
      par.9 che parla del pavimento riguarda la SECONDA META' di un run, ed e' un'altra misura:
      non si trasporta a questa senza dirlo.

  (2) IL PUNTO FISSO DI `_tau` NON SI FORMA, e par.9 dice che si forma. La voce dice:
      "poiche' il riferimento e' la MEDIANA, per il nodo mediano dens/dens_rif ~ 1 SEMPRE ...
       e' un PUNTO FISSO auto-normalizzante".
      MISURATO: 0.3698 / 0.0629 / 0.8024 / 0.7475 -- un fattore 13 fra semi, non 1.
      PERCHE', ed e' visibile nella riga :2150: il riferimento NON e' la mediana dell'insieme,
      e' la mediana di un SOTTOINSIEME -- `median(_dens[_dens > 1e-6])`, cioe' il 78-88 % dei nodi.
      Numeratore e denominatore vivono su popolazioni DIVERSE, ed e' esattamente la condizione che
      il punto fisso di C12 richiede e che qui manca (la stessa distinzione che A3 chiama
      "errore di popolazione", qui con segno opposto: qui SALVA invece di rompere).
      LA CONTROPROVA SOPRA LO DIMOSTRA: togliendo il filtro il rapporto vale 1.000000 ESATTO su
      4 semi su 4. Il filtro e' l'unica cosa che separa i due casi.
      COSA RESTA VERO E COSA NO: il punto fisso ESATTO non c'e'. Ma il rapporto resta confinato
      entro un fattore ~16, non libero su ordini di grandezza: l'ancoraggio e' ATTENUATO, non
      abolito. E la conseguenza operativa di par.9 -- "far maturare il sistema non puo', PER
      COSTRUZIONE, accorciare la memoria del nodo tipico" -- NON E' PIU' SOSTENUTA DA QUESTO
      ARGOMENTO. Non sto affermando il contrario: non l'ho misurato. Sto dicendo che la
      DIMOSTRAZIONE su cui poggiava non regge, e serve una misura a tempi diversi.""")

print("""
--- (b) `ZETA_LOC` (:3185-3187)  ZETA_M / (1 + max(rho/median(rho) - 1, 0)) ---
  ASSIOMI: A2 (median globale) + A3 (propria mediana) -- ma la POPOLAZIONE e' corretta:
           `rho` e `median(rho)` vivono ENTRAMBI sugli archi. Cfr. il difetto di
           `fattore_elasticita`, dove NON era cosi'.""")
print("  zeta_loc mediano per seme: %s   (ZETA_M = %.1f)" % (["%.4f" % x for x in zl_med], ZETA_M))
print("  frazione con eccesso ESATTAMENTE 0 (zeta_loc = ZETA_M): %s   media %.2f %%"
      % (["%.2f %%" % (100 * x) for x in zl_zero], 100 * float(np.mean(zl_zero))))
print("""  LETTURA: per meta' degli archi lo smorzamento "locale" vale ESATTAMENTE il valore
  globale ZETA_M -- e' il 50 % per DEFINIZIONE di mediana, non un fatto misurato. Su quella meta'
  la legge non e' locale: e' la costante. NB: ZETA_LOC e' OFF di default (:250), quindi questo
  NON tocca nessun run committato -- e' un difetto DORMIENTE.""")

print("""
--- (c) `u_nodo` (:2607)  I / media_dei_VICINI  -- IL CASO CHE DECIDE UNA DOMANDA APERTA ---
  ASSIOMI: A2 SODDISFATTO (la media e' sui vicini topologici: nessuna scorciatoia globale).
           A3 VIOLATO (e' una statistica di POSIZIONE del proprio intorno, e A3 nomina
           esplicitamente "media dei primi vicini").""")
print("  u_nodo mediano per seme: %s" % ["%.4f" % x for x in u_med])
print("  frazione sopra 1       : %s" % ["%.4f" % x for x in u_sopra])
print("""  LETTURA -- E' LA RISPOSTA ALLA DOMANDA "APERTO #2" DI doc/ASSIOMI.md:
  la domanda era se **A3 sia un caso particolare di A2**. `u_nodo` SODDISFA A2 e VIOLA A3.
  Quindi NO: A3 e' INDIPENDENTE da A2, e un solo controesempio basta a stabilirlo.
  !!  MA `u_nodo` NON e' percio' un difetto da correggere: sta dentro `_cs_nodo`, cioe' dentro cio'
  che DEFINISCE la struttura causale, e A4 dice che quel livello si giudica a parte. Inoltre la
  mediana misurata NON e' 1 (il punto fisso di A3 non si forma, perche' la media dei vicini non e'
  una statistica dello stesso insieme cui `I` appartiene). **Serve a decidere una questione sugli
  assiomi, non a giustificare una modifica.**""")

print("""
--- (d) mediana di `r` in `ritmo()` (:1939-1943) ---
  ASSIOMI: A2 (`med = median(|f|)` globale) + A3 (punto fisso).
  NON MISURABILE DAI .pkl: `f` e' la frequenza d'interferenza, interna al passo, e non e' salvata.
  MA IL PUNTO FISSO E' ALGEBRICO, non statistico, ed e' GIA' STABILITO (par.9, presidio C12):
  `x = f/median(|f|)` e `r_normalized = r/r_unit` con `r_unit` il valore a `x = 1` implicano
  `median(r) = 1.0 ESATTAMENTE`, con qualunque orologio. Il sigillo S4 della cura di
  `_psi_spin_prec` confronto' proprio quelle due mediane e diede `z = 0.00`: NON "nessun effetto",
  ma NESSUNA MISURA.
  NON SERVE UN RUN PER CONFERMARLO, e farne uno sarebbe il test vuoto che P4 vieta.""")

print("\n" + "=" * 118)
print("""SINTESI -- quattro casi, TRE esiti diversi, e la differenza conta:

  _tau      DIFETTO ATTIVO      A2 (mediana globale) + A3b (pavimento al 19.6 %). MA il PUNTO
                                FISSO di A3 NON si forma, contro quanto par.9 afferma: il filtro
                                `_dens > 1e-6` salva la legge per caso. Vedi (a). Percorso VIVO.
  ZETA_LOC  DIFETTO DORMIENTE   A2+A3, meta' degli archi al valore globale per definizione.
                                Flag OFF di default: nessun run committato ne risente.
  u_nodo    NON UN DIFETTO      viola A3 ma soddisfa A2 ed e' dentro `_cs_nodo` (A4).
                                Il suo valore e' METODOLOGICO: dimostra che A3 NON discende da A2.
  median r  GIA' STABILITO      punto fisso ALGEBRICO. Non serve misurarlo; misurarlo e' il test
                                vuoto che P4 vieta.

NESSUNA DI QUESTE E' STATA CABLATA. (7) era analisi, e resta analisi.""")
