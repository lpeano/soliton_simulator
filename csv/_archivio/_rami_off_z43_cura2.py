# -*- coding: utf-8 -*-
"""**IL RAMO DELLA FASE DI `ritmo()`, USCITO DAL SIMULATORE con la CURA (2) di `Z43`.**

*(Decisione di Luca, 2026-10-05: `r = cs_nodo / CS_M`. Il ramo esce, ma **non si perde**:
e' qui **COPIATO DAL SORGENTE**, non riscritto.)*

> ### UNA DIFFERENZA DALL'ARCHIVIO DELLA `CURA 2`, e va detta subito: **quello archiviava
> ### CODICE MORTO** *(rami `else` di un flag sempre acceso, byte-inerti per costruzione)*.
> ### **QUESTO ARCHIVIA CODICE VIVO:** il ramo qui sotto **girava a ogni passo** ed era
> ### **LA LEGGE DEL TEMPO PROPRIO**. Non e' una pulizia: e' **una legge che ne sostituisce
> ### un'altra**, e il sigillo serve a dire **che cosa cambia**.

> ### QUESTO FILE NON SI IMPORTA E NON GIRA. E' un ARCHIVIO.
> **Per rilanciare il simulatore com'era, si parte dal TAG:**
> ```
> git cat-file -p pre-z43-cura2-r-da-cs:soliton_simulator.py > sim_vecchio.py
> ```
> **scritto in BINARIO** *(`git checkout` riscriverebbe le newline: par.7)*.
> **Blob del simulatore al tag: `062172d3`** *(sha1 dei byte grezzi)*.

**CHE COSA USCIVA, riga per riga al tag:**

| righe al tag | che cosa facevano | perche' escono |
|--:|---|---|
| `:5296`-`:5301` | la docstring che descriveva il bottleneck `x/sqrt(1+x^2)` e la mediana come gauge | descrive una legge che non c'e' piu': **lasciarla sarebbe un commento scaduto**, e in questo repo lo sono stati |
| `:5316` | `_ritmo_chiamate`, il contatore delle chiamate | **non esce**: resta nella forma nuova |
| `:5317`-`:5322` | il ripiego su `_psi_prec` assente -> `r = 1`, piu' `_ritmo_sicurezza` | la forma nuova non legge `_psi_prec`: il ripiego diventa quello su `_cs_nodo_prev` |
| `:5323`-`:5324` | `f` dal campo SCALARE: `angle(psi) - angle(_psi_prec)`, diviso `DT` | **`r` non legge piu' la fase**: e' la decisione (2) di Luca |
| `:5329`-`:5344` | il guard `4pi` sul campo SPINORIALE, con `_ritmo_guard4pi_ko` e `_ritmo_snap_identico` | guardava gli snapshot di `psi_spin`, che la forma nuova non consuma |
| `:5345`-`:5354` | `f` dal campo SPINORIALE con il wrapping `2pi`/`4pi` (`RITMO_WRAP_2PI`) | idem: e' la fase |
| `:5355`-`:5357` | `TEMPO_PROPRIO_ORIENTATO`: `f` col SEGNO invece che in modulo | il segno della fase non entra piu' in `r` |
| `:5358`-`:5369` | i tre contatori della degenerazione di `f` (`f_tutto_nullo`, `f_mediana_nulla`, `med_sul_pavimento`) | contavano la degenerazione **di `f`**, che non c'e' piu' |
| `:5370`-`:5399` | **IL GAUGE**: `_med_f_ultimo`, `_med_f_prec`, `_ritmo_med_assente`, `_ritmo_med_identico` e la cura dell'anello istantaneo del 2026-09-18 | il gauge era la MEDIANA GLOBALE della fase: **esce con la fase** |
| `:5400`-`:5410` | `x = f/med`, il bottleneck `x/sqrt(1+x^2) + 1e-6`, la normalizzazione a `x=1` e `1 + TAU_LOC*(r_norm - 1)` | **e' la legge sostituita** |

**E UNA COSA CHE QUESTO ARCHIVIO CONSERVA E CHE NON E' CODICE:** il blocco `:5370`-`:5399`
contiene **la motivazione scritta della cura dell'anello istantaneo** *(2026-09-18)* --
perche' `ritmo()` **non** scriveva `_med_f_prec`, perche' lo promuoveva `step()`, e il
numero misurato `max|median(x) - 1| = 0.000e+00` su 122 passi. **Quella misura resta vera**:
diceva che il gauge istantaneo era un punto fisso ESATTO. La cura nuova non la smentisce,
**la rende inutile** -- e il ragionamento va conservato perche' **la stessa trappola puo'
ripresentarsi**: `cs -> r -> dt_e -> cs` e' un anello, e passa per la cache di UN PASSO
PRIMA proprio per la ragione scritta qui.

**CHE COSA *NON* ESCE, e va detto perche' il contrario sarebbe estendere la cura da soli:**
il ramo `TEMPO_SEGNO` *(`:5303`-`:5312`)* **RESTA**. Legge `tw`, non la fase, e **non e'
nominato** fra i rami che la decisione di Luca fa uscire. Oggi `TEMPO_SEGNO = False`, quindi
la scelta e' **byte-inerte**; se un giorno venisse acceso, le due letture possibili del
mandato darebbero `r` DIVERSI, e **quella sarebbe una decisione di Luca**
*(doc/TASK_HISTORY/2026-10-05_z43-cura2-r-da-cs.md)*.
"""

# ESENTE-H-P5: e' un ARCHIVIO. Non importa il simulatore, non gira, non scrive referti.

TAG = "pre-z43-cura2-r-da-cs"
BLOB_AL_TAG = "062172d3"          # sha1 dei BYTE GREZZI del simulatore al tag
RIGHE_AL_TAG = (5296, 5301, 5313, 5410)


# ==============================================================================================
#  LA DOCSTRING di `ritmo()` -- righe `:5296`-`:5301` al tag `pre-z43-cura2-r-da-cs`
#  (blob 062172d3)
# ----------------------------------------------------------------------------------------------
#  COSA DICEVA:   la legge del bottleneck `x/sqrt(1+x^2)` ancorata alla mediana globale
#  PERCHE' ESCE:  descrive una legge sostituita. Un commento scaduto e' un difetto (par.2)
#  COME SI RILANCIA: git cat-file -p pre-z43-cura2-r-da-cs:soliton_simulator.py (in BINARIO)
# ==============================================================================================

#         """Ritmo del TEMPO PROPRIO locale, derivato dalla frequenza d'interferenza.
#         Privo di clipping artificiali: dilatazione e compressione del tempo proprio emergono da una
#         risposta analitica continua e liscia (bottleneck x/sqrt(1+x^2)), ancorata alla mediana
#         globale come gauge. Vicino a x=1 la risposta e' ~lineare; per x->inf satura sub-linearmente;
#         per x->0 decade dolcemente verso un pavimento infinitesimo, senza discontinuita'. Nessun
#         parametro libero: la scala e' dettata dalla transizione analitica."""


# ==============================================================================================
#  IL RAMO DELLA FASE di `ritmo()` -- righe `:5313`-`:5410` al tag `pre-z43-cura2-r-da-cs`
#  (blob 062172d3)
# ----------------------------------------------------------------------------------------------
#  COSA FACEVA:   `r` dalla FREQUENZA d'interferenza `f = Delta(angle psi)/DT`, normalizzata
#                 sulla MEDIANA GLOBALE di `|f|` del passo PRECEDENTE (il gauge), passata nel
#                 bottleneck `x/sqrt(1+x^2) + 1e-6` e riscalata a `1` al gauge `x = 1`.
#  PERCHE' ESCE:  decisione di Luca del 2026-10-05: `r = cs_nodo/CS_M`, esponente `p = 1`
#                 ("orologio a luce"). `r` NON legge piu' la fase.
#  COME SI RILANCIA: git cat-file -p pre-z43-cura2-r-da-cs:soliton_simulator.py (in BINARIO)
# ==============================================================================================

#         # [A8 - Z33, 2026-09-18] SOLO CONTATORI, nessuna logica toccata. Questo ramo restituisce
#         # `r = 1` per TUTTI: la dilatazione temporale sparisce in quel passo. E' legittimo -- non
#         # esiste uno stato precedente con cui confrontarsi -- ma finora non lo diceva NESSUNO.
#         self._ritmo_chiamate = getattr(self, "_ritmo_chiamate", 0) + 1
#         if self._psi_prec is None or len(self._psi_prec) != self.n:
#             self._ritmo_sicurezza = getattr(self, "_ritmo_sicurezza", 0) + 1
#             self._ritmo_sicurezza_shape = (
#                 -1 if self._psi_prec is None else len(self._psi_prec), self.n)
#             self._psi_prec = self.psi.copy() if len(self.psi) == self.n else np.ones(self.n, complex)
#             return np.ones(self.n)
#         a = np.angle(self.psi) - np.angle(self._psi_prec)
#         signed = ((a + np.pi) % (2 * np.pi) - np.pi) / DT
#         # [FASE 5] TEMPO PROPRIO dal CAMPO SPINORIALE (batte sull'OTTO, 4pi) invece del campo scalare.
#         # COERENZA (magnitudine): nel limite psi_spin[:,0]=self.psi e |dphi|<pi -> ritmo IDENTICO. Il segno
#         # non entra nel ritmo (magnitudine); il legame orologio-segno vive nel de Broglie SU(2) (gia' 4pi,
#         # TW_SPINORE = tw/4pi). Snapshot t-1 (Jacobi): psi_spin del passo precedente, _psi_spin_prec aggiornato in step.
#         _ps = getattr(self, "psi_spin", None); _psp = getattr(self, "_psi_spin_prec", None)
#         # [A8 - Z33] il guard 4pi: se fallisce si cade sul ramo SCALARE 2pi, e nessuno lo dice.
#         # E' la stessa guardia che fu inerte nel 95.33 % delle chiamate PER MESI (C11).
#         if CAMPO_SPINORIALE:
#             if _ps is None or _psp is None or len(_ps) != self.n or len(_psp) != self.n:
#                 self._ritmo_guard4pi_ko = getattr(self, "_ritmo_guard4pi_ko", 0) + 1
#                 self._ritmo_guard4pi_shape = (-1 if _ps is None else len(_ps),
#                                               -1 if _psp is None else len(_psp), self.n)
#             elif _ps is _psp or np.array_equal(_ps, _psp):
#                 # LO SNAPSHOT E' LO STESSO OGGETTO (o identico): `f` sara' ZERO per ogni nodo.
#                 # Non e' un errore -- significa che `psi_spin` non e' cambiato dall'ultimo snapshot --
#                 # ma senza questo contatore la degenerazione e' INVISIBILE.
#                 self._ritmo_snap_identico = getattr(self, "_ritmo_snap_identico", 0) + 1
#         if CAMPO_SPINORIALE and _ps is not None and _psp is not None and len(_ps) == self.n and len(_psp) == self.n:
#             a = np.angle(_ps[:, 0]) - np.angle(_psp[:, 0])
#             if RITMO_WRAP_2PI:
#                 # [D34, 2026-09-22] IL PERIODO GIUSTO. `np.angle` ha periodo `2pi`, quindi `a`
#                 # sta in (-2pi, 2pi] e una differenza di OSSERVABILI si avvolge su `2pi`.
#                 # E' LA STESSA FORMA del ramo scalare otto righe sopra.
#                 signed = ((a + np.pi) % (2 * np.pi) - np.pi) / DT
#             else:
#                 signed = ((a + 2 * np.pi) % (4 * np.pi) - 2 * np.pi) / DT   # wrapping su 4pi (l'otto)
#         # FLAG 4 (--tempo-proprio-orientato): f mantiene il SEGNO (tempo proprio orientato);
#         # off = modulo, byte-identico al comportamento storico. La scala gauge resta positiva.
#         f = signed if TEMPO_PROPRIO_ORIENTATO else np.abs(signed)
#         # [A8 - Z33] LA FIRMA DEL DIFETTO: `f` identicamente nullo -> `x = 0` -> `r ~ 1.414e-06`,
#         # cioe' IL TEMPO PROPRIO SI FERMA PER TUTTI in quel passo. E il caso piu' debole:
#         # `median(|f|) = 0` con qualche `f` non nullo -> `med` cade sul PAVIMENTO e quelli ESPLODONO.
#         # Sono due regimi OPPOSTI e si contano separatamente.
#         _fa = np.abs(f)
#         if _fa.size:
#             if float(np.max(_fa)) == 0.0:
#                 self._ritmo_f_tutto_nullo = getattr(self, "_ritmo_f_tutto_nullo", 0) + 1
#             elif float(np.median(_fa)) <= 0.0:
#                 self._ritmo_f_mediana_nulla = getattr(self, "_ritmo_f_mediana_nulla", 0) + 1
#             if float(np.median(_fa)) <= 1e-9:
#                 self._ritmo_med_sul_pavimento = getattr(self, "_ritmo_med_sul_pavimento", 0) + 1
#         # [CURA DELL'ANELLO ISTANTANEO, 2026-09-18 - categoria D del par.10: NESSUN FLAG]
#         # IL DIFETTO: `med` era `median(|f|)` DELLO STESSO ISTANTE, e veniva usato SU `f`. Due
#         # assiomi nella stessa riga: A6 (nessuna funzione istantanea di X agisce dinamicamente su X:
#         # `f` e `r` si determinavano a vicenda DENTRO il passo) e A3 (`median(x) = 1` per IDENTITA').
#         # MISURATO PRIMA DELLA CURA (`csv/_test_fork/_anello_sfasato.txt`, blob f8f46683):
#         #   `max|median(x) - 1| = 0.000e+00` su 122 passi -- il punto fisso non era "circa": era
#         #   ESATTO A MACCHINA. Col `med` sfasato di uno diventa 2.1097 / 0.9108 / 1.1727.
#         # LA CURA: si legge il `med` del passo PRECEDENTE. Il RIFERIMENTO non cambia (resta
#         # `median(|f|)`): cambia QUANDO lo si legge. Nessun gauge nuovo, nessun numero tarato.
#         #
#         # PERCHE' `ritmo()` NON SCRIVE `_med_f_prec`, ed e' il presidio che regge tutto: questo
#         # metodo ha TRE call-site, e DUE SONO DIAGNOSTICI (`:3124` la fisica, `_diag_completa` e il
#         # terzo). Se lo snapshot avanzasse qui, ogni chiamata diagnostica farebbe avanzare lo stato
#         # fisico -- par.2.3 (purezza pure-read) violato, e sarebbe il QUINTO difetto di questa
#         # famiglia. Quindi: qui si LEGGE e si REGISTRA; **`step()` PROMUOVE**, a `:3129-3131`,
#         # accanto a `_psi_prec` e `_psi_spin_prec`, che sono gli altri due snapshot consumati da qui.
#         # La contaminazione da diagnostico e' chiusa PER COSTRUZIONE: `step()` chiama `ritmo()`
#         # PRIMA di promuovere, quindi il valore promosso e' sempre quello della chiamata FISICA.
#         #
#         # PERCHE' UNO SCALARE E NON L'ARRAY `f`: uno scalare NON HA LUNGHEZZA, quindi l'intera
#         # classe A8b (cache cross-passo da estendere a ogni punto di crescita: mitosi, `semina`,
#         # `nuova_massa`) SPARISCE PER COSTRUZIONE. E' il presidio piu' forte disponibile, ed e' la
#         # ragione per cui `_cs_nodo_prev` e `_psi_spin_prec` hanno fatto difetto e questo non puo'.
#         # A3c/A8b (quarto livello): `med_prec` e `f` sono ENTRAMBI `Delta_angle/DT`, cioe' `[1/T]` -
#         # confrontabili, non solo presenti.
#         _med_corrente = max(float(np.median(np.abs(f))), 1e-9)
#         self._med_f_ultimo = _med_corrente             # REGISTRO, non snapshot: lo promuove step()
#         _medp = getattr(self, "_med_f_prec", None)
#         if _medp is None:
#             # NON ESISTE UN PRIMA. Si riusa la convenzione gia' presente in questo stesso metodo
#             # (`:2021-2026`, `_psi_prec` assente -> `np.ones`), NON se ne inventa una nuova: "nessun
#             # passato" significa "nessuna dilatazione", e si CONTA (A8).
#             # ⚠ E il fallback NON e' `median(|f|)` corrente: sarebbe il difetto stesso, al passo 1.
#             self._ritmo_med_assente = getattr(self, "_ritmo_med_assente", 0) + 1
#             return np.ones(self.n)
#         med = float(_medp)
#         if med == _med_corrente:
#             # il gauge non si e' mosso fra i due passi: legittimo, ma invisibile senza contatore
#             # (e' la forma che `Z33` prende qui).
#             self._ritmo_med_identico = getattr(self, "_ritmo_med_identico", 0) + 1
#         x = f / med
#         r = x / np.sqrt(1.0 + x**2) + 1.0e-6           # bottleneck liscio, satura a 1 per x->inf
#         r_unit = 1.0 / np.sqrt(2.0) + 1.0e-6           # valore al gauge x=1
#         r_normalized = r / r_unit                       # x=1 -> fattore unitario
#         return 1.0 + TAU_LOC * (r_normalized - 1.0)

