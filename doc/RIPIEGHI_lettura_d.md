# I 43 CANDIDATI `(d)`, **LETTI A MANO** *(2026-09-28)*

> ### **Questo documento è SCRITTO A MANO, e la tabella generata è un'altra:**
> `doc/RIPIEGHI_classi.md`. ### **Le classi `(a)`–`(e)` le decide uno strumento; i verdetti qui sotto
> li decido io leggendo, e per questo stanno in un file separato.**
> *(Punto ① di `RIPIEGHI-ZERO`, mandato del guardiano: «leggi a mano tutti i `(d)` e per ciascuno
> scrivi cosa restituisce il ramo di scorta, se tocca tutti i nodi o solo i nuovi, se è mai scattato
> nei 72 passi della scena grande».)*

## ✅ **La terza domanda ha una risposta sola, e è GENERATA**

### **NESSUNO dei 43 è scattato nei 72 passi della scena grande.** Il giunto è col referto della
sonda *(`_ripieghi_len_n.json`, stesso blob `f7541d03`, quindi le righe combaciano)*: in tutta la
corsa — **otto** passi di nascita, Schwinger compreso — l'unico sito che ha preso il ramo di scorta è
**`_xi_rumore`**, che è classe `(b)`.

> ### ⚠ **E «mai scattato» NON vuol dire «innocuo»:** vuol dire **che quella scena non lo esercita.**
> `lambda_nodi` scattava **una volta su 44 passi**, e quella volta bastava a gonfiare il campo di
> tutta la rete del `62 %`.

---

# Le quattro famiglie, e la quarta la regola automatica **non poteva vederla**

## ① ### **RICALCOLO A METÀ PASSO — la famiglia del flash.** `len(psi) < n → calcola_psi()`

| riga | funzione |
|---|---|
| `:2525` | `chiralita_core_locale` |
| `:3600` | `_passo_spinoriale` |
| `:3715` | `_passo_spinoriale` |
| `:7002` | `memoria_hebbiana_moto` |

**Cosa restituisce:** `psi` **ricalcolata da zero**, sui pesi della `d` **corrente**.
**Chi tocca:** ### **TUTTI i nodi**, non i nuovi.
### ➜ **È ESATTAMENTE `lambda_nodi` prima della cura**, e la condizione è **fusa**
*(`not hasattr(psi) or len(psi) < n`)*: **inizializzazione in OR col ricalcolo**.
### **Va separata come in `lambda_nodi`: `len(psi) == 0` resta, `0 < len(psi) < n` solleva.**
*(Sono i quattro che il guardiano ha indicato.)*

## ② ### **SOSTITUZIONE DI UN VALORE A TUTTA LA RETE.** `full(n, …)` · `zeros(n)` · `stack([zeros…])`

| riga | funzione | il valore di scorta | che cosa spegne |
|---|---|---|---|
| `:3747` | `_passo_spinoriale` | `_cs_in = np.full(n, CS_M)` | ### **la `cs` dinamica, per tutti** |
| `:4145` | `_passo_spinoriale` | `_csn2 = np.full(n, CS_M)` | idem, **e non è contato** |
| `:5454` | `_tempo_luce_nodo` | `CS_M` *(contato: `_cs_fallback`)* | idem |
| `:7328` | `memoria_hebbiana_moto` | `np.full(sum(mask), CS_M)` *(contato)* | idem, sul sottoinsieme mascherato |
| `:5384` | `_tau_arco_causale` | ripiega su `CS_M` *(contato: `_tum_cs_salti`)* | idem |
| ### `:5280` | `_bloch_ritardato` | ### **`dt_n = np.full(n, DT)`** | ### **il TEMPO PROPRIO, per tutti** — `dt_n = DT·r` diventa `DT` |
| ### `:5344` | `_r_nodo_mitosi` | `r` a **uno** per tutti *(contato: `_tum_r_salti`)* | ### **il RITMO, per tutti** |
| `:4084` `:4086` | `_passo_spinoriale` | ### **`rho = np.zeros(n)`** | ### **la DENSITÀ a zero, per tutti** — e **non è contato** |
| `:7115` | `memoria_hebbiana_moto` | `_nb` **ricostruito** da `zeros(n)` | la **direzione di Bloch**, per tutti |

### ➜ **Sono la stessa famiglia del flash**, e due di loro *(`:4145`, `:4084`/`:4086`)* ### **non
hanno nemmeno un contatore**: se scattassero, **non lo saprebbe nessuno.**

## ③ **USA LA CACHE COSÌ COM'È, e su una cache corta viene FUORI UN ARRAY CORTO**

| riga | funzione | il ramo di scorta |
|---|---|---|
| `:4138` | `_passo_spinoriale` | `np.where(perc_chi[:n] >= 0, 1, -1)` |
| `:5754` | `step` | `self.psi` |
| `:6960` | `pozzo_grafo` | `np.abs(psi[:n])**2` |
| `:7394` | `memoria_hebbiana_moto` | `np.abs(psi[:n])**2` |
| `:5750` `:5799` `:5868` `:6000` | `step` | `median(d0[:n])` · `phivel[:n]` · `_deg[:n]` · `abs(_pv_src[:n])` |

**Cosa restituisce:** la cache **tagliata a `n`** — ma se è **più corta di `n`**, `x[:n]` restituisce
### **tutto quello che c'è, cioè un array più corto.**
### ⚠ **E qui NON SO dire cosa succede a valle:** o un errore di forma, o un **broadcast silenzioso**.
### **Non lo indovino: serve una misura, e non l'ho fatta.** *(La dichiaro come domanda aperta invece
di metterla in una classe.)*

## ④ ### **SOLO UN CONTATORE, e poi SI SALTA IL BLOCCO — e la mia regola non poteva vederla**

| riga | funzione | il ramo di scorta |
|---|---|---|
| `:2153` | `_aggiorna_lift_spinoriale` | `return` |
| `:2478` | `_feedback_spinoriale_archi` | conta `_sfb_lift_corto` e la forma |
| `:3680` `:5715` `:5722` | `_passo_spinoriale`, `step` | contano *(`_g_chicore_passo_salti`)* o ricalcolano un ramo alternativo |
| `:5477` `:5587` `:5588` `:5592`×2 `:5730` `:5852` `:5885` `:5911` `:5912` `:5917` `:5918` `:6225` | `step`, `_coppia_interferenza` | ### **«nessun else: si continua dopo l'`if`»** |

> ### 📌 **Per questi il ramo di scorta NON SCRIVE NIENTE: l'effetto è che IL BLOCCO PROTETTO VIENE
> SALTATO.** Quindi l'effetto va letto su ### **ciò che NON viene fatto**, non su ciò che viene
> scritto. ### **La mia regola automatica guardava solo il valore restituito: questa famiglia le era
> INVISIBILE per costruzione.**
>
> ### ⚠ **E sono la maggioranza dei 43.** Non li classifico: dico che ### **vanno letti uno per uno
> guardando il blocco che salta**, e che quello è un lavoro a sé — non una regola.

---

# ➜ **Che cosa propongo, e non faccio**

| | |
|---|---|
| **①** | la famiglia ① *(4 siti)*: ### **stessa cura di `lambda_nodi`** — condizione separata, `0 < len < n` solleva. **È la più chiara e la più grave** |
| **②** | la famiglia ② *(9 siti)*: ### **stessa cura**, e **prima** un **contatore** dove manca *(`:4145`, `:4084`, `:4086`)* — perché oggi, se scattassero, **non lo saprebbe nessuno** |
| **③** | la famiglia ③ *(8 siti)*: ### **prima una MISURA**, non una cura: cosa fa a valle un array più corto di `n` |
| **④** | la famiglia ④ *(22 siti)*: ### **lettura uno per uno del blocco che salta.** Un lavoro a sé |

### **Non ne curo nessuno in questo giro:** il mandato dice *«nessun codice»*, e la famiglia ④ da
sola è più grande di tutto il resto.
