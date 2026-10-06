# -*- coding: utf-8 -*-
"""LA PATCH DI **<<VIA IL `0.3`>>** — `MITOSI-SOGLIA-GRAD` esce.

*(Decisione di Luca del 2026-10-06, sul referto `27c10bd`. Il ragionamento e i criteri sono in
`doc/TASK_HISTORY/2026-10-06_via-il-03-mitosi-soglia-grad.md`, committato **prima** in
`e693993`.)*

### ⛔ **E' UNA RIMOZIONE, con ZERO CODICE NUOVO.** `soglia` e' **gia'**
### `np.full(len(avv), soglia0, float)`: il blocco della modulazione **la sovrascrive**.
### Togliere il blocco lascia **`soglia = soglia0` su ogni arco**, che e' esattamente cio' che
### il mandato chiede — e **`9-ter` e' soddisfatto nel modo piu' forte: una legge in meno e
### nemmeno una riga da scrivere.**

**TRE RIMOZIONI, ogni ancora CONTATA e UNICA** *(`P1-quater`)*:

1. il blocco della **modulazione** *(`if TORS_4PI and len(self.i) == len(avv):`)*;
2. **`_r_nodo_mitosi`**, che resta **senza chiamanti nel simulatore**;
3. e con lei i quattro contatori **`_tum_r_*`**, che vivono dentro quella funzione.

**PIU' UNA ANNOTAZIONE**, che e' l'unica cosa che si AGGIUNGE: la guardia `_g_tors4pi_*`
**resta** *(il mandato non chiede di toglierla)* ma dopo questa patch **non guarda piu'
niente**, e il codice lo deve dire.

# ESENTE-H-P8: il confronto col codice di prima lo fa IL SIGILLO, e lo prende dal PADRE. Qui
#   `HEAD` compare solo in questa riga di docstring, che spiega perche'.

USO:  python csv/_seal_fork/_mitosi_soglia_grad_via_patch.py            (sul simulatore)
      python csv/_seal_fork/_mitosi_soglia_grad_via_patch.py <src> <dst>  (per il SIGILLO)
"""
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
SIM = os.path.join(RADICE, "soliton_simulator.py")

# =============================================================== I TRE BLOCCHI CHE ESCONO
# ### ⛔ **SI SCRIVONO PER INTERO**, e l'ancora si pretende UNICA: un'ancora corta
#   prenderebbe anche le copie archiviate della stessa funzione.

VIA_MODULAZIONE = '''        if TORS_4PI and len(self.i) == len(avv):
            # gradiente di tempo proprio LUNGO l'arco: differenza del tempo proprio nodale
            # fra i due estremi. tau_nodo alto = tempo lento = materia. Dove il gradiente
            # e' forte, la soglia si abbassa (la mitosi e' agevolata verso il tempo lento).
            # [CURA 2 STRUTTURALE, 2026-09-27] IL RAMO `if TEMPO_UNICO_MITOSI:` E' STATO TOLTO: la legge e' SEMPRE questa.
            #   Il ramo `else` e' ARCHIVIATO in `csv/_archivio/rami_off_cura2.py` e si rilancia dal tag `pre-cura2-strutturale`.
            # [CURA 2] IL GRADIENTE DI TEMPO SI PRENDE DALL'OROLOGIO, non da `|tw|`.
            # Il commento qui sopra dice "gradiente di TEMPO PROPRIO", ma `tau_nodo` e'
            # `1 + mean(|tw|)/PHI_CRIT`, cioe' ESATTAMENTE la formula del ramo
            # `TEMPO_SEGNO` di `ritmo()` -- CHE NON GIRA (`TEMPO_SEGNO = False` in 9 run
            # su 11, `Z130`). Intenzione TEMPO, implementazione TORSIONE.
            # SI PRENDE `r` E NON `1/r`, e la ragione e' un conto, non una preferenza:
            #   r    in [1.4142e-6, 1.4142]  -> tanh(grad) <= 0.8884 -> la soglia MODULA
            #   1/r  in [0.707, 707107]      -> tanh(grad) -> 1 ESATTO -> la modulazione
            #                                   diventerebbe un RISCALAMENTO COSTANTE
            #                                   della soglia, cioe' un PARAMETRO NASCOSTO
            #                                   (`A1`), e `A11` cor.6 dice che un limite
            #                                   che satura e' un allarme.
            _rn = self._r_nodo_mitosi()
            # `grad_modula` qui e' il gradiente di `r`: IL TEMPO PROPRIO VERO.
            grad_modula = np.abs(_rn[self.i] - _rn[self.j])
            # modulazione limitata: la soglia scende di al piu' ~30% dove il gradiente e' forte
            soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_modula))
'''

# ### la RIGA che resta al suo posto, e che la patch NON tocca: e' lei a rendere la
#   rimozione sufficiente.
RESTA = "        soglia = np.full(len(avv), soglia0, float)" + NL

ANNOTA_VIA = (
 "        # [MITOSI-SOGLIA-GRAD VIA, 2026-10-06, decisione di Luca] LA MODULAZIONE DELLA" + NL
 + "        #   SOGLIA E' USCITA. `soglia` resta `soglia0` su OGNI arco, ed e' la riga qui"
 + NL
 + "        #   sopra a farlo: la modulazione la SOVRASCRIVEVA, e toglierla basta." + NL
 + "        #   IL PERCHE', MISURATO (referto 27c10bd, 1000 passi, due bracci):" + NL
 + "        #     R = 0.1616 sulle divisioni e 0.3417 sulla popolazione nella finestra," + NL
 + "        #     quindi la crescita NON era creata dalla modulazione;" + NL
 + "        #     e SENZA di lei la crescita e' STABILE (48-150 nascite ogni 100 passi)," + NL
 + "        #     mentre CON lei ACCELERA fino a 1044. Non una differenza di quantita':" + NL
 + "        #     UNA DIFFERENZA DI FORMA." + NL
 + "        #   Il ramo che esce e' ARCHIVIATO in `csv/_archivio/_rami_off_mitosi_soglia"
 + "_grad.py`" + NL
 + "        #   e si rilancia dal tag `pre-mitosi-soglia-grad-via`." + NL
 + "        #   LA SOGLIA 3pi NON E' TOCCATA: `soglia0 = PHI_CRIT + twist_max`. Il `pi` di" + NL
 + "        #   dipolo che in questa scena non esiste e' una DECISIONE SEPARATA di Luca." + NL)

VIA_FUNZIONE = '''    def _r_nodo_mitosi(self):
        """L'OROLOGIO per NODO, per il gradiente di tempo della mitosi. Guardia CONTATA (`A8`).

        Il fallback e' `1` = "nessuna dilatazione", **la stessa convenzione che `ritmo()` usa
        quando non c'e' un passato** (`np.ones`): non una convenzione nuova.
        `_r_corrente` e' un array PER NODO attraversato da un punto di crescita, cioe' la
        classe `A8b` di `_cs_nodo_prev` (71.88 %) e `_psi_spin_prec` (95.33 %): si contano
        QUATTRO cose, non una -- invocazioni, salti, la FORMA al fallimento, e QUANDO.
        """
        n = self.n
        self._tum_r_tot = getattr(self, "_tum_r_tot", 0) + 1
        r = getattr(self, "_r_corrente", None)
        if r is None or len(r) < n:
            self._tum_r_salti = getattr(self, "_tum_r_salti", 0) + 1
            self._tum_r_forma = (-1 if r is None else len(r), n)
            self._tum_r_quando = self._tum_r_tot
            return np.ones(n)
        return np.asarray(r, dtype=float)[:n]

'''

ANNOTA_GUARDIA = (
 "        # [MITOSI-SOGLIA-GRAD VIA, 2026-10-06] ATTENZIONE: questa guardia CONTAVA i salti"
 + NL
 + "        #   DELLA MODULAZIONE, che e' USCITA -- quindi dopo quella cura NON GUARDA PIU'"
 + NL
 + "        #   NIENTE. Nessuno strumento vivo la legge (censito col comando). NON la tolgo"
 + NL
 + "        #   perche' il mandato non lo chiede, e fare piu' di quello che un mandato chiede"
 + NL
 + "        #   e' il modo in cui una cura diventa due: TOGLIERLA E' UNA DECISIONE DI LUCA."
 + NL)
ANCORA_GUARDIA = "        self._g_tors4pi_tot = getattr(self, \"_g_tors4pi_tot\", 0) + 1" + NL

# ### il commento che nominava la variabile RIMOSSA: si corregge, non si lascia.
VECCHIO_COMMENTO = (
 "        # massima alla SOGLIA LOCALE (soglia critica emergente, pilotata da `grad_modula`:"
 " il gradiente di" + NL
 + "        # `r` a flag acceso, della torsione a flag spento -- `D32`), e si SPEGNE al tetto"
 " 4pi. Tra i due, la" + NL)
NUOVO_COMMENTO = (
 "        # massima alla SOGLIA `soglia0` (= `PHI_CRIT + twist_max` = 3pi), e si SPEGNE al"
 " tetto 4pi." + NL
 + "        # [MITOSI-SOGLIA-GRAD VIA, 2026-10-06] QUI C'ERA SCRITTO <<pilotata da"
 " `grad_modula`>>," + NL
 + "        #   e `grad_modula` NON ESISTE PIU'. La soglia non e' piu' pilotata da niente:"
 " e'" + NL
 + "        #   `soglia0` su ogni arco. Tra i due, la" + NL)


def patcha(t):
    """Applica le tre rimozioni e le due annotazioni. ### **Ogni ancora si CONTA.**"""
    fatte = []

    def uno(et, a, b):
        nonlocal t
        k = t.count(a)
        if k != 1:
            raise SystemExit("[FERMO] l'ancora di `%s` compare %d volte, non 1." % (et, k))
        t = t.replace(a, b)
        fatte.append(et)

    uno("A: VIA il blocco della MODULAZIONE", VIA_MODULAZIONE, "")
    uno("B: l'annotazione sotto la riga che RESTA", RESTA, RESTA + ANNOTA_VIA)
    uno("C: VIA `_r_nodo_mitosi` (e con lei i quattro `_tum_r_*`)", VIA_FUNZIONE, "")
    uno("D: l'annotazione sulla guardia che non guarda piu' niente",
        ANCORA_GUARDIA, ANNOTA_GUARDIA + ANCORA_GUARDIA)
    # ### ⛔ **E IL COMMENTO CHE NOMINAVA `grad_modula` SI CORREGGE, non si lascia:**
    #   dopo la rimozione quella variabile ### **non esiste piu'**, e un commento che la
    #   nomina e' ### **esattamente un commento scaduto** -- la classe che questo repo si e'
    #   gia' trovata addosso (`H-P7`). ### **L'ha trovato la patch stessa**, contando le
    #   citazioni rimaste nel file patchato.
    uno("E: il commento che nominava `grad_modula`", VECCHIO_COMMENTO, NUOVO_COMMENTO)
    return t, fatte


def main(argv):
    src = argv[1] if len(argv) > 2 else SIM
    dst = argv[2] if len(argv) > 2 else SIM
    t = io.open(src, encoding="utf-8", newline="").read()
    t2, fatte = patcha(t)
    io.open(dst, "w", encoding="utf-8", newline="").write(t2)
    print("=" * 96)
    print("LA PATCH DI <<VIA IL 0.3>>: %s -> %s" % (os.path.basename(src),
                                                    os.path.basename(dst)))
    print("=" * 96)
    for f in fatte:
        print("   %s" % f)
    print()
    print("   righe prima %d, dopo %d  (### %+d)"
          % (len(t.split(NL)), len(t2.split(NL)),
             len(t2.split(NL)) - len(t.split(NL))))
    # ### i controlli che la patch fa SU SE STESSA, e che si leggono nell'uscita
    # ### ⛔ **SI CONTA SUL CODICE, NON SUL FILE:** il commento che SPIEGA la rimozione
    #   nomina `grad_modula` apposta, e contarlo come una citazione viva sarebbe
    #   ### **un autocontrollo che fallisce per la ragione sbagliata.** ### **Il collaudo
    #   della patch me l'ha fatto vedere: diceva <<atteso 0>> e ne trovava 2, tutte e due
    #   nella riga che dice che la variabile NON ESISTE PIU'.**
    def _nel_codice(testo, nome):
        return sum(1 for L in testo.split(NL)
                   if nome in L and not L.lstrip().startswith("#"))

    for nome in ("grad_modula", "_r_nodo_mitosi", "_tum_r_"):
        nc, nt = _nel_codice(t2, nome), t2.count(nome)
        print("   %-18s nel CODICE %d   (nel file %d, il resto sono commenti)   %s"
              % (nome, nc, nt, "OK" if nc == 0 else "### ATTESO 0 NEL CODICE"))
    print("   %-18s resta %d volte  (la guardia, ANNOTATA e non tolta)"
          % ("_g_tors4pi_", t2.count("_g_tors4pi_")))
    import ast
    ast.parse(t2)
    print("   ### la sintassi del file patchato: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
