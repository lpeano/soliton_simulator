# -*- coding: utf-8 -*-
"""LA PATCH DI `Z43` CURA (2): `r = cs_nodo / CS_M`, l'orologio a luce.

*(Il **braccio 0** del sigillo: applicata al blob di **prima** deve ridare il blob di
**oggi**, al byte.)*

### GLI HUNK VENGONO DAL DIFF VERO *(`difflib.SequenceMatcher`)*, non da cio' che credevo
di aver cambiato -- e il generatore ha **VERIFICATO la ricostruzione confrontando i blob
PRIMA di scrivere questo file**. E' la forma imparata dalla `CURA (1)`, dove due tentativi
<<a mano>> hanno dato `f8ce6859` invece di `062172d3`
*(`csv/_seal_fork/_z43_cura1_patch.py`)*.

### UNA DIFFERENZA DALLA PATCH DELLA `CURA (1)`, e conta: quella era **una riga in tre
### punti**. Questa **TOGLIE 98 RIGHE DI LEGGE VIVA** e ne mette 22. Non e' un ritocco:
### e' una legge del tempo proprio che sostituisce un'altra.

### ⚠ **IL *PRIMA* DI QUESTA PATCH NON E' IL BLOB DELLA `PARTE A`, ed e' una
### conseguenza di `H-REG-R`:** la cura toccava anche **un commento in `__init__`**, e
`__init__` **non ha una scheda** nel `REGISTRO_FISICA`. Le uscite erano aprire una scheda
*(decisione di struttura fuori dal mandato)* o dichiarare `[SENZA-FISICA]` **su un commit che
cambia la legge del tempo** *(falso)*. ### **Quindi il commento e' andato in un commit SUO,
e PRIMA** *(`19f9d68`, blob `ca3cdd8a`)*, cosi' **non esiste nessun commit in cui quel
commento sia falso**. ### **Il *prima* di questa patch e' QUELLO, non `062172d3`** -- e i due
differiscono **solo per quel commento**, quindi girano **identici**.

**CHE COSA CAMBIA, in ordine:** la **docstring** di `ritmo()` *(descriveva il bottleneck
`x/sqrt(1+x^2)` e la mediana globale come gauge: una legge che non c'e' piu')*; il **corpo**
di `ritmo()` *(la frequenza d'interferenza, il guard `4pi`, i tre contatori della
degenerazione di `f`, il gauge `_med_f_prec` e il bottleneck -> `cs_nodo_prev/CS_M`)*; la
**promozione del gauge** in `step()`; il **commento in `__init__`**, che altrimenti
resterebbe a dire che `ritmo()` scrive un registro che non scrive piu'.

**I rami che escono sono COPIATI** in `csv/_archivio/_rami_off_z43_cura2.py`. Il simulatore
della `PARTE A` si rilancia dal tag **`pre-z43-cura2-r-da-cs`** *(blob `062172d3`)*, e il *prima* di questa
patch dal commit **`19f9d68`** *(blob `ca3cdd8a`)*, con
`git cat-file -p <ref>:soliton_simulator.py` **in BINARIO** *(par.7)*.

USO:  python csv/_seal_fork/_z43_cura2_patch.py <partenza> <uscita>
"""

# ESENTE-H-P8: un FALSO POSITIVO, e lo nomino invece di riformularlo. L occorrenza di
#   `HEAD` sta DENTRO UN HUNK -- e' una riga del COMMENTO NUOVO del simulatore, che dice
#   che `_sigillo_anello.py` da oggi fallisce a `HEAD` e DEVE farlo. Questa patch NON
#   prende niente da `HEAD`: non legge git affatto, riceve i due file da `argv`, e il
#   *prima* lo estrae il SIGILLO, dal PADRE del commit che ha cambiato il simulatore.
#   Potevo cambiare la parola nel commento del simulatore e passare il controllo:
#   NON LO FACCIO -- sarebbe disarmare un presidio cambiando le parole, e quel commento
#   e' VERO e serve a chi trovera' quel sigillo rotto. E' la QUINTA volta per la stessa
#   ragione, e la quarta e' nel sigillo di questa stessa cura.
import hashlib
import io
import sys

NL = chr(10)
TAG = "pre-z43-cura2-r-da-cs"            # il tag della PARTE A (blob 062172d3)
DA = "19f9d68"             # il PADRE: il commit del solo commento di `__init__`
BLOB_PRIMA = "ca3cdd8a"
BLOB_DOPO = "f7237563"

# Ogni hunk: (etichetta, il VECCHIO testo, il NUOVO). Il vecchio e' ASSERITO UNICO a ogni
# applicazione (`P1-quater`), e il CONTESTO accanto a ciascuno e' quanto e' bastato per
# renderlo unico -- non una scelta, una MISURA del generatore.
HUNK = [
    ("hunk 1 (replace), contesto 0 righe",
     NL.join([
    '        """Ritmo del TEMPO PROPRIO locale, derivato dalla frequenza d\'interferenza.',
    '        Privo di clipping artificiali: dilatazione e compressione del tempo proprio emergono da una',
    '        risposta analitica continua e liscia (bottleneck x/sqrt(1+x^2)), ancorata alla mediana',
    "        globale come gauge. Vicino a x=1 la risposta e' ~lineare; per x->inf satura sub-linearmente;",
    "        per x->0 decade dolcemente verso un pavimento infinitesimo, senza discontinuita'. Nessun",
    '        parametro libero: la scala e\' dettata dalla transizione analitica."""',
     ]),
     NL.join([
    '        """Ritmo del TEMPO PROPRIO locale: r = cs_nodo / CS_M, la velocita\' delle onde metriche',
    '        nel nodo divisa per quella del vuoto. Esponente p = 1 ("orologio a luce"): un tic e\' il',
    '        TEMPO DI ATTRAVERSAMENTO, la stessa legge del tempo-luce tau = d/cs -- quindi r e tau',
    '        vengono ora dalla STESSA grandezza, e non da due costruzioni diverse.',
    '        [Z43 CURA (2), decisione di Luca del 2026-10-05] PRIMA r veniva dalla FREQUENZA',
    "        d'interferenza della fase, normalizzata sulla MEDIANA GLOBALE di |f| del passo precedente",
    "        e passata in un bottleneck x/sqrt(1+x^2). Il ramo e' COPIATO in",
    '        csv/_archivio/_rami_off_z43_cura2.py, e si rilancia dal tag pre-z43-cura2-r-da-cs.',
    "        r STA IN (0, 1], e la ragione NON e' il `np.minimum(cs_floor, CS_M)`: quello limita il",
    "        PAVIMENTO, non il risultato. La ragione e' che `_cs_nodo` restituisce",
    '        `cs_floor + (CS_M - cs_floor)*transizione` con',
    '        `transizione = 0.5*(1 + tanh(1 - u_nodo))` e `u_nodo = I/media_vicini >= 0`, quindi',
    '        `1 - u_nodo <= 1` e `transizione <= 0.5*(1 + tanh(1)) = 0.880797`: la transizione NON',
    "        PUO' ARRIVARE A 1. Da cui `cs < CS_M` STRETTAMENTE dove `cs_floor < CS_M`, e",
    "        `cs = CS_M` -- cioe' `r = 1` ESATTO -- SOLO dove `I = 0`, perche' li' il pavimento",
    "        vale gia' CS_M. IN UNA RETE DI MATERIA NON ESISTONO NODI CON r = 1: il tempo proprio",
    "        e' PIU' LENTO di quello coordinato OVUNQUE ci sia qualcosa, ed e' il verso giusto.",
    "        ⚠ E `r <= 1` E' ARITMETICA, non algebra: `a + (b-a)*t` con `t < 1` potrebbe in",
    '        principio superare `b` di un ulp. MISURATO su 2e6 campioni casuali: ZERO superamenti,',
    '        e il margine resta ~1e-06 sotto. Il sigillo lo RIMISURA sul simulatore vero invece di',
    '        fidarsi di questa riga.',
    "        TAU_LOC NON E' PIU' L'AMPIEZZA della dilatazione: resta solo l'INTERRUTTORE (0 = orologio",
    "        globale). A TAU_LOC = 1.0 la forma vecchia era 1 + 1.0*(x - 1) = x, cioe' un PASSANTE:",
    "        questa cura non toglie un'ampiezza in uso, toglie una manopola che valeva 1 (A1).",
    "        E DUE FLAG PERDONO QUI IL LORO UNICO CONSUMATORE FISICO, e non li tolgo io perche'",
    '        sarebbe estendere la cura: RITMO_WRAP_2PI (la cura D34, che avvolgeva su 2pi la',
    '        differenza di np.angle) e TEMPO_PROPRIO_ORIENTATO (il segno di f). Dopo questa cura r',
    "        NON LEGGE LA FASE, quindi non c'e' piu' niente da avvolgere ne' da orientare: entrambi",
    "        restano accettati dal CLI e INERTI nella fisica, e la loro sorte e' una decisione di",
    '        Luca. CAMPO_SPINORIALE invece conserva i suoi altri consumatori."""',
     ])),
    ("hunk 2 (replace), contesto 0 righe",
     NL.join([
    '        # [A8 - Z33, 2026-09-18] SOLO CONTATORI, nessuna logica toccata. Questo ramo restituisce',
    "        # `r = 1` per TUTTI: la dilatazione temporale sparisce in quel passo. E' legittimo -- non",
    '        # esiste uno stato precedente con cui confrontarsi -- ma finora non lo diceva NESSUNO.',
     ]),
     NL.join([
    '        # [Z43 CURA (2), 2026-10-05] IL CONTATORE DELLE CHIAMATE RESTA: dei dodici contatori del',
    "        # ramo vecchio e' l'UNICO che non dipendeva dalla fase, quindi sopravvive alla cura (A8).",
     ])),
    ("hunk 3 (replace), contesto 0 righe",
     NL.join([
    '        if self._psi_prec is None or len(self._psi_prec) != self.n:',
    '            self._ritmo_sicurezza = getattr(self, "_ritmo_sicurezza", 0) + 1',
    '            self._ritmo_sicurezza_shape = (',
    '                -1 if self._psi_prec is None else len(self._psi_prec), self.n)',
    '            self._psi_prec = self.psi.copy() if len(self.psi) == self.n else np.ones(self.n, complex)',
     ]),
     NL.join([
    "        # LA CACHE DI `cs` DEL PASSO PRECEDENTE. La convenzione del ripiego NON e' nuova: e'",
    "        # quella GIA' USATA DUE VOLTE in questo file (`_tempo_luce_nodo` e il gemello",
    "        # dell'inerzia) -- cache assente o piu' corta di `n` -> si cade sul VUOTO, dove",
    "        # `cs = CS_M`, cioe' `r = 1`. Ed e' anche la convenzione che QUESTO STESSO metodo",
    '        # usava quando `_psi_prec` mancava (`np.ones`). Si CONTA (A8).',
    "        # E SUCCEDE DAVVERO, non e' un ramo teorico: `_cs_nodo_prev` e' scritto solo con",
    '        # `CS_DINAMICO` e solo se `FORK_SU2_MEM or STEP2_OROLOGIO`, e AL PASSO 0 NON ESISTE.',
    "        # E' la famiglia di difetti `A8b` misurata all'80 % proprio su questa cache: qui non",
    "        # puo' restare invisibile perche' il contatore registra ANCHE la forma.",
    '        _csp = getattr(self, "_cs_nodo_prev", None)',
    '        if _csp is None or len(_csp) < self.n:',
    '            self._ritmo_cs_assente = getattr(self, "_ritmo_cs_assente", 0) + 1',
    '            self._ritmo_cs_forma = (-1 if _csp is None else len(_csp), self.n)',
     ])),
    ("hunk 4 (replace), contesto 0 righe",
     NL.join([
    '        a = np.angle(self.psi) - np.angle(self._psi_prec)',
    '        signed = ((a + np.pi) % (2 * np.pi) - np.pi) / DT',
    "        # [FASE 5] TEMPO PROPRIO dal CAMPO SPINORIALE (batte sull'OTTO, 4pi) invece del campo scalare.",
    '        # COERENZA (magnitudine): nel limite psi_spin[:,0]=self.psi e |dphi|<pi -> ritmo IDENTICO. Il segno',
    "        # non entra nel ritmo (magnitudine); il legame orologio-segno vive nel de Broglie SU(2) (gia' 4pi,",
    '        # TW_SPINORE = tw/4pi). Snapshot t-1 (Jacobi): psi_spin del passo precedente, _psi_spin_prec aggiornato in step.',
    '        _ps = getattr(self, "psi_spin", None); _psp = getattr(self, "_psi_spin_prec", None)',
    '        # [A8 - Z33] il guard 4pi: se fallisce si cade sul ramo SCALARE 2pi, e nessuno lo dice.',
    "        # E' la stessa guardia che fu inerte nel 95.33 % delle chiamate PER MESI (C11).",
    '        if CAMPO_SPINORIALE:',
    '            if _ps is None or _psp is None or len(_ps) != self.n or len(_psp) != self.n:',
    '                self._ritmo_guard4pi_ko = getattr(self, "_ritmo_guard4pi_ko", 0) + 1',
    '                self._ritmo_guard4pi_shape = (-1 if _ps is None else len(_ps),',
    '                                              -1 if _psp is None else len(_psp), self.n)',
    '            elif _ps is _psp or np.array_equal(_ps, _psp):',
    "                # LO SNAPSHOT E' LO STESSO OGGETTO (o identico): `f` sara' ZERO per ogni nodo.",
    "                # Non e' un errore -- significa che `psi_spin` non e' cambiato dall'ultimo snapshot --",
    "                # ma senza questo contatore la degenerazione e' INVISIBILE.",
    '                self._ritmo_snap_identico = getattr(self, "_ritmo_snap_identico", 0) + 1',
    '        if CAMPO_SPINORIALE and _ps is not None and _psp is not None and len(_ps) == self.n and len(_psp) == self.n:',
    '            a = np.angle(_ps[:, 0]) - np.angle(_psp[:, 0])',
    '            if RITMO_WRAP_2PI:',
    '                # [D34, 2026-09-22] IL PERIODO GIUSTO. `np.angle` ha periodo `2pi`, quindi `a`',
    '                # sta in (-2pi, 2pi] e una differenza di OSSERVABILI si avvolge su `2pi`.',
    "                # E' LA STESSA FORMA del ramo scalare otto righe sopra.",
    '                signed = ((a + np.pi) % (2 * np.pi) - np.pi) / DT',
    '            else:',
    "                signed = ((a + 2 * np.pi) % (4 * np.pi) - 2 * np.pi) / DT   # wrapping su 4pi (l'otto)",
    '        # FLAG 4 (--tempo-proprio-orientato): f mantiene il SEGNO (tempo proprio orientato);',
    '        # off = modulo, byte-identico al comportamento storico. La scala gauge resta positiva.',
    '        f = signed if TEMPO_PROPRIO_ORIENTATO else np.abs(signed)',
    '        # [A8 - Z33] LA FIRMA DEL DIFETTO: `f` identicamente nullo -> `x = 0` -> `r ~ 1.414e-06`,',
    "        # cioe' IL TEMPO PROPRIO SI FERMA PER TUTTI in quel passo. E il caso piu' debole:",
    '        # `median(|f|) = 0` con qualche `f` non nullo -> `med` cade sul PAVIMENTO e quelli ESPLODONO.',
    '        # Sono due regimi OPPOSTI e si contano separatamente.',
    '        _fa = np.abs(f)',
    '        if _fa.size:',
    '            if float(np.max(_fa)) == 0.0:',
    '                self._ritmo_f_tutto_nullo = getattr(self, "_ritmo_f_tutto_nullo", 0) + 1',
    '            elif float(np.median(_fa)) <= 0.0:',
    '                self._ritmo_f_mediana_nulla = getattr(self, "_ritmo_f_mediana_nulla", 0) + 1',
    '            if float(np.median(_fa)) <= 1e-9:',
    '                self._ritmo_med_sul_pavimento = getattr(self, "_ritmo_med_sul_pavimento", 0) + 1',
    "        # [CURA DELL'ANELLO ISTANTANEO, 2026-09-18 - categoria D del par.10: NESSUN FLAG]",
    '        # IL DIFETTO: `med` era `median(|f|)` DELLO STESSO ISTANTE, e veniva usato SU `f`. Due',
    '        # assiomi nella stessa riga: A6 (nessuna funzione istantanea di X agisce dinamicamente su X:',
    "        # `f` e `r` si determinavano a vicenda DENTRO il passo) e A3 (`median(x) = 1` per IDENTITA').",
    '        # MISURATO PRIMA DELLA CURA (`csv/_test_fork/_anello_sfasato.txt`, blob f8f46683):',
    '        #   `max|median(x) - 1| = 0.000e+00` su 122 passi -- il punto fisso non era "circa": era',
    '        #   ESATTO A MACCHINA. Col `med` sfasato di uno diventa 2.1097 / 0.9108 / 1.1727.',
    '        # LA CURA: si legge il `med` del passo PRECEDENTE. Il RIFERIMENTO non cambia (resta',
    '        # `median(|f|)`): cambia QUANDO lo si legge. Nessun gauge nuovo, nessun numero tarato.',
    '        #',
    "        # PERCHE' `ritmo()` NON SCRIVE `_med_f_prec`, ed e' il presidio che regge tutto: questo",
    '        # metodo ha TRE call-site, e DUE SONO DIAGNOSTICI (`:3124` la fisica, `_diag_completa` e il',
    '        # terzo). Se lo snapshot avanzasse qui, ogni chiamata diagnostica farebbe avanzare lo stato',
    '        # fisico -- par.2.3 (purezza pure-read) violato, e sarebbe il QUINTO difetto di questa',
    '        # famiglia. Quindi: qui si LEGGE e si REGISTRA; **`step()` PROMUOVE**, a `:3129-3131`,',
    '        # accanto a `_psi_prec` e `_psi_spin_prec`, che sono gli altri due snapshot consumati da qui.',
    "        # La contaminazione da diagnostico e' chiusa PER COSTRUZIONE: `step()` chiama `ritmo()`",
    "        # PRIMA di promuovere, quindi il valore promosso e' sempre quello della chiamata FISICA.",
    '        #',
    "        # PERCHE' UNO SCALARE E NON L'ARRAY `f`: uno scalare NON HA LUNGHEZZA, quindi l'intera",
    '        # classe A8b (cache cross-passo da estendere a ogni punto di crescita: mitosi, `semina`,',
    "        # `nuova_massa`) SPARISCE PER COSTRUZIONE. E' il presidio piu' forte disponibile, ed e' la",
    "        # ragione per cui `_cs_nodo_prev` e `_psi_spin_prec` hanno fatto difetto e questo non puo'.",
    "        # A3c/A8b (quarto livello): `med_prec` e `f` sono ENTRAMBI `Delta_angle/DT`, cioe' `[1/T]` -",
    '        # confrontabili, non solo presenti.',
    '        _med_corrente = max(float(np.median(np.abs(f))), 1e-9)',
    '        self._med_f_ultimo = _med_corrente             # REGISTRO, non snapshot: lo promuove step()',
    '        _medp = getattr(self, "_med_f_prec", None)',
    '        if _medp is None:',
    "            # NON ESISTE UN PRIMA. Si riusa la convenzione gia' presente in questo stesso metodo",
    '            # (`:2021-2026`, `_psi_prec` assente -> `np.ones`), NON se ne inventa una nuova: "nessun',
    '            # passato" significa "nessuna dilatazione", e si CONTA (A8).',
    "            # ⚠ E il fallback NON e' `median(|f|)` corrente: sarebbe il difetto stesso, al passo 1.",
    '            self._ritmo_med_assente = getattr(self, "_ritmo_med_assente", 0) + 1',
    '            return np.ones(self.n)',
    '        med = float(_medp)',
    '        if med == _med_corrente:',
    "            # il gauge non si e' mosso fra i due passi: legittimo, ma invisibile senza contatore",
    "            # (e' la forma che `Z33` prende qui).",
    '            self._ritmo_med_identico = getattr(self, "_ritmo_med_identico", 0) + 1',
    '        x = f / med',
    '        r = x / np.sqrt(1.0 + x**2) + 1.0e-6           # bottleneck liscio, satura a 1 per x->inf',
    '        r_unit = 1.0 / np.sqrt(2.0) + 1.0e-6           # valore al gauge x=1',
    '        r_normalized = r / r_unit                       # x=1 -> fattore unitario',
    '        return 1.0 + TAU_LOC * (r_normalized - 1.0)',
     ]),
     NL.join([
    "        # NESSUN PAVIMENTO su `cs`, e il perche' e' `A11`: i due gemelli hanno",
    "        # `np.maximum(cs, 1e-12)` perche' LI' `cs` DIVIDE (`tau = d/cs`). Qui MOLTIPLICA, quindi",
    "        # una divisione per zero e' IMPOSSIBILE e un pavimento proteggerebbe da NIENTE.",
    '        # Copiarlo "per simmetria" sarebbe scrivere un clip senza errore da cui proteggere.',
    "        # E non c'e' nemmeno un tetto: `cs <= CS_M` non e' un clip, e' una PROPRIETA' della",
    "        # forma di `_cs_nodo` -- l'unico modo di violarlo e' cambiare quella legge.",
    '        return np.asarray(_csp, float)[:self.n] / CS_M',
     ])),
    ("hunk 5 (replace), contesto 0 righe",
     NL.join([
    "            # [CURA DELL'ANELLO ISTANTANEO, 2026-09-18] LA PROMOZIONE del gauge di `ritmo()`, QUI e",
    "            # non dentro `ritmo()`: questo e' l'UNICO call-site FISICO (gli altri due sono",
    '            # diagnostici), quindi solo qui lo snapshot deve avanzare. Sta accanto a `_psi_prec` e',
    "            # `_psi_spin_prec` perche' e' la stessa cosa: uno snapshot CONSUMATO da `ritmo()`, e si",
    "            # promuove DOPO il consumo -- che e' cio' che fa valere A6 (misurato in `680d069`:",
    "            # promuoverlo PRIMA confronterebbe lo stato con se' stesso, `f = 0` per costruzione).",
    "            # ⚠ NON SI PROMUOVE UN `med` CHE STA SUL PAVIMENTO `1e-9`: quel valore non e' una",
    "            # misura, e' la protezione da divisione per zero. Promuoverlo renderebbe la",
    '            # REGOLARIZZAZIONE il gauge del passo dopo -- e la misura dice quanto costerebbe: il',
    "            # rapporto `med_t/med_(t-1)` ha `max = 4.81e+07`, ed e' ESATTAMENTE il passo che segue",
    '            # un gauge degenere (`Z33`). Senza questo ramo la degenerazione non sparirebbe: si',
    '            # ROVESCEREBBE, da "tutti sul pavimento" a "tutti in saturazione". Contato (A8).',
    '            _mu = getattr(self, "_med_f_ultimo", None)',
    '            if _mu is not None:',
    '                if _mu > 1e-9:',
    '                    self._med_f_prec = _mu',
    '                else:',
    '                    self._ritmo_med_non_promosso = getattr(self, "_ritmo_med_non_promosso", 0) + 1',
     ]),
     NL.join([
    "            # [Z43 CURA (2), 2026-10-05] LA PROMOZIONE DEL GAUGE DI `ritmo()` E' USCITA DA QUI.",
    '            # Era `_med_f_prec = _med_f_ultimo` con il ramo che NON promuoveva un `med` sul',
    "            # pavimento `1e-9`. Esce perche' il gauge ERA LA MEDIANA GLOBALE DELLA FASE, e",
    "            # `r = cs_nodo/CS_M` non legge piu' la fase: non c'e' piu' niente da promuovere.",
    "            # Il blocco e' COPIATO in `csv/_archivio/_rami_off_z43_cura2.py` con la sua",
    '            # motivazione del 2026-09-18 e il numero misurato (`max med_t/med_(t-1) = 4.81e+07`),',
    '            # che resta vero: diceva quanto costava promuovere una regolarizzazione.',
    '            # DUE COSE NON LE TOLGO IO, e le dichiaro invece di nasconderle:',
    '            #  (1) `self._med_f_prec` e `self._med_f_ultimo` restano DICHIARATI a `None` in',
    '            #      `__init__` (A7b) e da oggi NESSUNO LI SCRIVE. Sono due registri morti, non',
    "            #      stato: toglierli e' una pulizia a se', non questa cura (lo stesso criterio",
    "            #      con cui `r_node` e' rimasto nella CURA (1)).",
    '            #  (2) `csv/_seal_fork/_sigillo_anello.py` ASSERISCE che `step()` promuova il',
    '            #      gauge: da questo commit quel sigillo FALLISCE a `HEAD`, e deve farlo --',
    "            #      sigilla una legge che non c'e' piu'. Si rigira AL SUO COMMIT (par.6).",
     ])),
]


def applica(t):
    """Ogni hunk si asserisce UNICO (`P1-quater`), uno alla volta."""
    for et, vecchio, nuovo in HUNK:
        n = t.count(vecchio)
        if n != 1:
            raise SystemExit("[FERMO] %s compare %d volte, non 1." % (et, n))
        t = t.replace(vecchio, nuovo, 1)
    return t


def main(argv):
    src, dst = argv[1], argv[2]
    b = hashlib.sha1(io.open(src, "rb").read()).hexdigest()[:8]
    print("  partenza: %s  (atteso %s)" % (b, BLOB_PRIMA))
    out = applica(io.open(src, encoding="utf-8").read())
    io.open(dst, "w", encoding="utf-8", newline=NL).write(out)
    bd = hashlib.sha1(io.open(dst, "rb").read()).hexdigest()[:8]
    print("  uscita:   %s  (atteso %s)   %s"
          % (bd, BLOB_DOPO, "COINCIDE" if bd == BLOB_DOPO
             else "### NON COINCIDE"))
    return 0 if bd == BLOB_DOPO else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
