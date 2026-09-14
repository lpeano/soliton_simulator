# PROFILAZIONE — dove va davvero il tempo nei run lenti?

> **Scritta per Claude web** e per chiunque debba decidere se e dove ottimizzare.
> Branch `fork-su2`, 2026-09-14. **`soliton_simulator.py` NON è stato toccato**: il lavoro è stato
> fatto su una **copia** (blob verificato identico all'originale prima di iniziare), perché due run
> stavano usando il file del repo.

---

## 1. IL VERDETTO IN UNA RIGA

> **Il collo di bottiglia NON è il loop CFL.** Le due ottimizzazioni autorizzate dal mandato
> (`cs_arco**2` e il numeratore di `beta_new`) varrebbero **qualche punto percentuale**.
> **Non le ho applicate**, come prescrive il mandato stesso: *"se il collo NON è il loop CFL,
> FERMATI e riporta"*.

---

## 2. COME È STATA FATTA

`cProfile` su **100 passi** con `--cs-dinamico --gamma-turbo 100`, cioè **il regime lento**
(`nsub` grande). Profilare il regime veloce direbbe poco su dove si spende quando fa male.
Aggiunto un timer attorno a `step()` per separare il passo fisico dal resto.

---

## 3. I NUMERI

Tempo totale **390.4 s**, di cui **323.7 s (83 %)** dentro `step()`. 406 chiamate a `step()`
(100 del batch + 300 del riscaldamento di `_applica_flag` + 6 di semina).

| funzione | chiamate | **tempo proprio** | cumulativo |
|---|---|---|---|
| `step` (contiene il loop CFL) | 406 | **38.3 s** | 322.7 s |
| **`_pesi`** | **6606** | **27.6 s** | 44.8 s |
| `scipy csr_matvec` | 12287 | **14.0 s** | 14.0 s |
| `_mat` | 9956 | **12.4 s** | 12.4 s |
| `_passo_spinoriale` | 406 | 8.6 s | **131.8 s** |
| `aggiorna_pesi_concorrenza` | 3 | 2.9 s | 3.1 s |

**`np.bincount` non compare nei primi 18.** Eppure il loop CFL ne fa **quattro per sottopasso**:
se fosse il collo, sarebbe in cima.

---

## 4. PERCHÉ I DUE HOIST NON VALGONO LA PENA

Entrambi vivono **dentro `step`**, che pesa **38.3 s su 390** (9.8 %). E dentro quei 38 s c'è
**tutto** il passo metrico, non solo il loop: le due moltiplicazioni sono una frazione di una
frazione.

Applicarli significherebbe mettere due modifiche nel repo — ognuna col suo sigillo di byte-identità,
ognuna un'occasione di sbagliare l'ordine delle operazioni e rompere l'ultimo bit — per un guadagno
che **il profiler non giustifica**. Meno tocchi, meglio è: era il principio guida del mandato, e
qui indica di non toccare.

---

## 5. DOVE VA IL TEMPO DAVVERO (fuori dal mandato — da decidere, non da fare)

> **`_pesi` è chiamato 6606 volte per 406 passi: SEDICI volte per passo.**

È il **primo hotspot per tempo proprio** dopo `step` stesso. Insieme a `_mat` + `csr_matvec`, che
ricostruiscono e applicano la matrice sparsa, fanno **54 s su 390 = il 14 %** — contro i 38 s di
*tutto* `step`.

Sedici ricalcoli per passo di una quantità che **nel passo non cambia** è il profilo tipico di un
valore ricalcolabile una volta e riusato. **Ma non è nella lista autorizzata, e non l'ho toccato.**
Se si decide di guardarlo, va fatto con lo **stesso sigillo di byte-identità** richiesto per i hoist:
`max|A − B| = 0.000e+00` esatto **e** stesso numero di nodi (uno zero con N diverso è *mancanza di
confronto*, non identità).

**Attenzione a una trappola:** `_pesi` potrebbe *non* essere invariante dentro il passo — dipende da
`self.eta`, `self.d`, `self.tw`, che **cambiano** durante `step()`. Se qualcuna delle 16 chiamate
legge uno stato aggiornato, cachearla **cambierebbe la fisica**. Va verificato **prima**, non
assunto: è esattamente il tipo di ottimizzazione che sembra gratuita e non lo è.

---

## 6. LA LEVA VERA NON È IL CODICE

Confermato dal profiler: anche azzerando i due hoist, il costo dominante non cambia.

> Il costo è **`nsub` × (bincount + matematica)**, e `nsub` è grande perché il forcing (K alto) rende
> `cs` basso → mezzo molle → escursioni grandi → il CFL chiede molti sottopassi.
> **Il taglio grosso è ridurre `nsub`, e `nsub` si controlla dalla SCALA** — K più basso, screening
> a K alto prima, N ridotto — **non dal codice.**

Un sottopasso più veloce × 200 resta lento. **Meno sottopassi** è la leva.

E c'è un corollario da tenere: **il costo È il segnale**. Forzare `cs` basso è caro *perché* è
lontano dal regime naturale del sistema.

---

## 7. COSA NON È STATO TOCCATO

`nsub` e le formule CFL; le `bincount` (cambiarle in CSR o riduzioni parallele cambierebbe l'ordine
di somma → non byte-identico → caos); l'ordine dei due mezzi-passi Verlet; `src` congelato a `t`;
`d0` aggiornato dopo il loop; le regolarizzazioni (`1e-9`, `1e-12`, `1e-6`, floor `d >= 0.05`).
E nessuna parallelizzazione.

**Il repo è intatto:** nessun commit tocca `soliton_simulator.py` per questo lavoro.
