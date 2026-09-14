# REPERTO — `_pesi()` non è ricalcolato 16 volte: è **ricorsivo**

> Branch `fork-su2`, 2026-09-14. **FASE A del mandato: sola lettura, nessuna modifica.**
> `soliton_simulator.py` **non è stato toccato**.

---

## 1. PERCHÉ MI FERMO PRIMA DELLA FASE B

Il mandato della FASE B assume che le **16 chiamate per passo** di `_pesi()` siano *ricalcoli
ridondanti dello stesso valore da parte di `calcola_psi()`*, e che quindi basti calcolarlo una
volta e passarlo. **La misura dice che la premessa è falsa.**

> Le chiamate da `calcola_psi()` sono il **12.8 %**. L'**80.9 %** viene da `stato_crossover()`,
> raggiunto attraverso `massa_critica_adattiva()`. E **il 43.6 % del totale è `_pesi()` che chiama
> se stesso**, un livello più in basso.

Ottimizzare il bersaglio sbagliato non è neutro: è una modifica al file con il suo rischio di
rottura dell'ultimo bit, per un guadagno che non c'è. Riporto e mi fermo, come da mandato.

---

## 2. IL CENSIMENTO (misurato, non letto)

Strumentazione per **monkeypatch in-process** su un run corto (20 passi + 300 di riscaldamento +
6 di semina = **326 chiamate a `step()`**). Non tocca il file, non altera la fisica: conta e
delega all'originale.

**5239 chiamate totali → 16.1 per passo** — coerente col profiler (`doc/PROFILAZIONE_costo_run.md`,
6606 chiamate / 406 passi).

| chiamante | chiamate | quota |
|---|---|---|
| **`stato_crossover:424`** (via `massa_critica_adattiva`) | **4240** | **80.9 %** |
| `calcola_psi:2172` | 673 | 12.8 % |
| `step:2571` | 326 | 6.2 % |

E la catena dominante, da sola quasi metà di tutto:

| catena | chiamate | quota |
|---|---|---|
| `_pesi` → `_lam_archi` → `lambda_nodi` → `massa_critica_adattiva` → `stato_crossover` → **`_pesi`** | **2284** | **43.6 %** |
| `chiralita_core_locale` → `lambda_nodi` → … → `_pesi` | 652 | 12.4 % |
| `calcola_psi` ← `step` | 600 | 11.5 % |
| `chiralita_core_locale` ← `step` / ← `_passo_spinoriale` | 326 + 326 | 12.4 % |
| `_passo_spinoriale` → `massa_critica_adattiva` → … | 326 | 6.2 % |

---

## 3. COSA SIGNIFICA — è un **ciclo**, non una ridondanza

```
_pesi()  ->  _lam_archi()  ->  lambda_nodi()  ->  massa_critica_adattiva()
                                                       |
                                              stato_crossover()  ->  _pesi()   [un livello sotto]
```

Il ciclo **non è infinito** perché `lambda_nodi()` ha già una guardia esplicita
(`self._calcolo_schermatura`), che nel ramo rientrante **restituisce `LAM` costante** invece della
schermatura vera. Il commento nel codice lo dice: «Nel ramo ricorsivo si usa LAM: il crossover resta
dinamico senza loop infinito.»

Quindi **le due `_pesi()` della ricorsione calcolano cose DIVERSE**: quella esterna usa
`_lam_archi()` schermata, quella interna `LAM` piatta. **Non sono lo stesso valore, e cachearne una
per l'altra cambierebbe la fisica** — non l'ultimo bit: la schermatura.

Ogni `_pesi()` esterna **costa una `_pesi()` interna**: il costo è ~2× per costruzione, ed è il
prezzo della guardia anti-ricorsione, non uno spreco da togliere.

---

## 4. LA TRAPPOLA GIÀ SEGNALATA, ORA PIÙ CONCRETA

`doc/PROFILAZIONE_costo_run.md` §5 avvertiva: `_pesi` dipende da `self.eta`, `self.d`, `self.tw`,
che **cambiano durante `step()`**. Ora si vede anche **dove**: `step:2571` fa `w = self._pesi()`
e **subito dopo** `self.eta += dt_n`. Ogni `_pesi()` chiamata **dopo** quella riga legge un `eta`
diverso. Non sono lo stesso valore neppure nel tempo.

---

## 5. TRE STRADE, PER LA DECISIONE DI LUCA (non dell'esecutore)

1. **Non fare nulla.** Il profiler dice che `_pesi` + `_mat` + `csr_matvec` sono il 14 % del tempo,
   e la leva vera è `nsub`, cioè la **scala**, non il codice (`PROFILAZIONE` §6). Resta la scelta
   coerente col principio «meno tocchi, meglio è».
2. **Cachare solo il ramo interno**, cioè memoizzare `_pesi` **quando `_calcolo_schermatura` è
   attivo** — lì `_lam_archi` restituisce `LAM` costante, quindi il valore è davvero lo stesso
   entro il passo *se* `eta/d/tw` non sono cambiati. Taglierebbe fino al 43.6 %. **Ma richiede di
   dimostrare l'invarianza, non di assumerla**, con il sigillo pieno: `max|A−B| = 0.000e+00`
   **e stesso numero di nodi** (uno zero con N diverso è mancanza di confronto, non identità).
3. **Ridurre le chiamate a `massa_critica_adattiva()`**, che è la vera sorgente: la chiamano
   `lambda_nodi`, `chiralita_core_locale`, `_passo_spinoriale`, `step`. È una quantità **globale**
   per passo. Più efficace e più rischiosa: tocca una legge di stato, non un dettaglio.

**Io non ho scelto e non ho toccato niente.** La FASE B, come scritta, ottimizzerebbe il 12.8 %
credendo di ottimizzare il tutto.

---

## 6. COSA NON È STATO TOCCATO

Nulla. Nessuna modifica a `soliton_simulator.py`. La strumentazione è vissuta in un processo
separato, per monkeypatch, e non ha scritto sul file né sul repo.
