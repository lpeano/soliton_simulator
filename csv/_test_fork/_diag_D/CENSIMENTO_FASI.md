# CENSIMENTO — **la famiglia «`4π` dichiarato, `2π` usato»**

> Generato da `csv/_test_fork/_censimento_fasi.py`. **Blob simulatore `3d91338e`.**
> **Sola lettura: nessuna cura, nessuna proposta in codice.**
>
> **LA REGOLA DI FONDO:** *lo spinore ha periodo `4π`; tutto ciò che si OSSERVA da lui ha periodo `2π`; un ACCUMULO non ha periodo.*

**PUNTI TROVATI: 52**, di cui **GRAVI: 38**.

| riga | funzione | tipo | **grave** | classe | flag che lo governa | che cosa |
|--:|---|:--:|:--:|:--:|---|---|
| `602` | `stato_crossover` | `OSS` | ⚠ **SÌ** | **`T`** | `—` | `phi` (4pi) dentro `exp` (periodo 2pi) |
| `2349` | `semina` | `W4` | no | **`T`** | `—` | ? |
| `2350` | `semina` | `W4` | no | **`T`** | `—` | ? |
| `2408` | `_registra_concorrenza` | `OSS` | ⚠ **SÌ** | **`T`** | `—` | `phi` (4pi) dentro `exp` (periodo 2pi) |
| `2447` | `aggiorna_pesi_concorrenza` | `OSS` | ⚠ **SÌ** | **`T`** | `—` | `phi` (4pi) dentro `exp` (periodo 2pi) |
| `2453` | `aggiorna_pesi_concorrenza` | `OSS` | ⚠ **SÌ** | **`T`** | `—` | `phi` (4pi) dentro `cos` (periodo 2pi) |
| `2456` | `aggiorna_pesi_concorrenza` | `OSS` | ⚠ **SÌ** | **`T`** | `—` | `phi` (4pi) dentro `exp` (periodo 2pi) |
| `2582` | `ritmo` | `W2` | no | **`T`** | `—` | OSSERVABILE (via `a`) |
| `2606` | `ritmo` | `W2` | no | **`T`** | `RITMO_WRAP_2PI` | OSSERVABILE (via `a`) |
| `2608` | `ritmo` | `W4` | ⚠ **SÌ** | **`T`** | `RITMO_WRAP_2PI` | OSSERVABILE (via `a`) |
| `2608` | `ritmo` | `A2P` | ⚠ **SÌ** | **`T`** | `RITMO_WRAP_2PI` | `+2pi` su una fase |
| `3109` | `_passo_spinoriale` | `OSS` | ⚠ **SÌ** | **`T`** | `DEPARAM_OROLOGIO` | `phi` (4pi) dentro `cos` (periodo 2pi) |
| `3357` | `calcola_psi` | `OSS` | ⚠ **SÌ** | **`T`** | `—` | `phi` (4pi) dentro `exp` (periodo 2pi) |
| `3367` | `calcola_psi` | `OSS` | ⚠ **SÌ** | **`T`** | `CAMPO_SPINORIALE` | `phi` (4pi) dentro `exp` (periodo 2pi) |
| `3423` | `_w4` | `W4` | no | **`T`** | `—` | ? |
| `3423` | `_w4` | `A2P` | ⚠ **SÌ** | **`T`** | `—` | `+2pi` su una fase |
| `4366` | `step` | `OSS` | ⚠ **SÌ** | **`T`** | `TEMPO_SEGNO` | `phi` (4pi) dentro `cos` (periodo 2pi) |
| `4375` | `step` | `OSS` | ⚠ **SÌ** | **`T`** | `SYNC_UPDATE` | `_phi_t` (4pi) dentro `exp` (periodo 2pi) |
| `4377` | `step` | `OSS` | ⚠ **SÌ** | **`T`** | `—` | `phi0` (4pi) dentro `cos` (periodo 2pi) |
| `4378` | `step` | `OSS` | ⚠ **SÌ** | **`T`** | `—` | `_phi_t` (4pi) dentro `exp` (periodo 2pi) |
| `4406` | `step` | `OSS` | ⚠ **SÌ** | **`T`** | `REPULS_LEGGE` | `_phi_t` (4pi) dentro `exp` (periodo 2pi) |
| `4416` | `step` | `OSS` | ⚠ **SÌ** | **`T`** | `REPULS_LEGGE` | `_phi_t` (4pi) dentro `cos` (periodo 2pi) |
| `4597` | `step` | `OSS` | ⚠ **SÌ** | **`T`** | `K_SYNC` | `_phi_t` (4pi) dentro `exp` (periodo 2pi) |
| `4599` | `step` | `OSS` | ⚠ **SÌ** | **`T`** | `K_SYNC` | `_phi_t` (4pi) dentro `sin` (periodo 2pi) |
| `4625` | `step` | `W4` | ⚠ **SÌ** | **`T`** | `—` | OSSERVABILE (via `delta_sync_phi`) |
| `4710` | `step` | `OSS` | ⚠ **SÌ** | **`T`** | `SYNC_UPDATE` | `phi` (4pi) dentro `exp` (periodo 2pi) |
| `4831` | `step` | `OSS` | ⚠ **SÌ** | **`T`** | `HAM_SRC` | `dph` (4pi) dentro `cos` (periodo 2pi) |
| `5289` | `mitosi` | `W4` | no | **`T`** | `MITOSI_DIR` | grandezza su 4pi (via `D`) |
| `5291` | `mitosi` | `W4` | no | **`T`** | `MITOSI_DIR` | grandezza su 4pi (via `D`) |
| `5311` | `mitosi` | `W4` | no | **`T`** | `ANTIFASE_ADD` | grandezza su 4pi (via `fm`) |
| `5311` | `mitosi` | `A2P` | ⚠ **SÌ** | **`T`** | `ANTIFASE_ADD` | `+2pi` su una fase |
| `5353` | `mitosi` | `W4` | no | **`T`** | `REGIME` | grandezza su 4pi |
| `5354` | `mitosi` | `W4` | no | **`T`** | `REGIME` | grandezza su 4pi |
| `5357` | `mitosi` | `W4` | no | **`T`** | `REGIME` | grandezza su 4pi |
| `5443` | `mitosi` | `W4` | ⚠ **SÌ** | **`T`** | `COPPIA_MIT,MAX_NODI` | OSSERVABILE (via `pick`) |
| `5443` | `mitosi` | `A2P` | ⚠ **SÌ** | **`T`** | `COPPIA_MIT,MAX_NODI` | `+2pi` su una fase |
| `5542` | `campo_spaziale` | `OSS` | ⚠ **SÌ** | **`T`** | `—` | `phi` (4pi) dentro `exp` (periodo 2pi) |
| `5894` | `memoria_hebbiana_moto` | `OSS` | ⚠ **SÌ** | **`T`** | `K_FRANGE` | `phi` (4pi) dentro `angle` (periodo 2pi) |
| `6105` | `memoria_hebbiana_moto` | `W4` | no | **`T`** | `MEM_MOTO_TUTTO` | grandezza su 4pi |
| `6118` | `diagnostica` | `OSS` | ⚠ **SÌ** | **`T`** | `—` | `phi` (4pi) dentro `exp` (periodo 2pi) |
| `8570` | `batch_condensazione` | `W2` | no | **`T`** | `—` | ? |
| `8587` | `batch_condensazione` | `OSS` | ⚠ **SÌ** | **`T`** | `—` | `phi` (4pi) dentro `angle` (periodo 2pi) |
| `8588` | `batch_condensazione` | `OSS` | ⚠ **SÌ** | **`T`** | `—` | `phi` (4pi) dentro `cos` (periodo 2pi) |
| `8678` | `batch_condensazione` | `OSS` | ⚠ **SÌ** | **`T`** | `—` | `phi` (4pi) dentro `exp` (periodo 2pi) |
| `8680` | `batch_condensazione` | `OSS` | ⚠ **SÌ** | **`T`** | `—` | `phi` (4pi) dentro `exp` (periodo 2pi) |
| `8741` | `batch_condensazione` | `OSS` | ⚠ **SÌ** | **`T`** | `—` | `phi` (4pi) dentro `exp` (periodo 2pi) |
| `8753` | `batch_condensazione` | `W2` | no | **`T`** | `—` | ? |
| `8868` | `batch_condensazione` | `OSS` | ⚠ **SÌ** | **`T`** | `—` | `phi` (4pi) dentro `angle` (periodo 2pi) |
| `8877` | `batch_condensazione` | `OSS` | ⚠ **SÌ** | **`T`** | `—` | `phi` (4pi) dentro `exp` (periodo 2pi) |
| `8891` | `batch_condensazione` | `OSS` | ⚠ **SÌ** | **`T`** | `—` | `phg` (4pi) dentro `exp` (periodo 2pi) |
| `8934` | `batch_condensazione` | `OSS` | ⚠ **SÌ** | **`T`** | `—` | `phi` (4pi) dentro `exp` (periodo 2pi) |
| `8969` | `batch_condensazione` | `OSS` | ⚠ **SÌ** | **`T`** | `—` | `phi` (4pi) dentro `exp` (periodo 2pi) |

## LE CLASSI, e la distinzione è il punto *(§S)*

| classe | che cos'è | che si fa |
|:--:|---|---|
| **`T`** | **avvolgimento di una FASE** *(topologia)* | **NON si leviga.** Il salto da `2π` a `0` è un artefatto della **coordinata**, non una discontinuità fisica: **levigarlo inventerebbe valori che non esistono.** La cura è **usare il periodo giusto** |
| **`L`** | soglia, tetto, `clip` di una **LEGGE** | **si leviga**, coi tre obblighi del corollario 7 di `A11` e la **larghezza DERIVATA**. *Una levigatura con larghezza scelta a mano è un parametro nuovo: peggio dello spigolo* |
| **`E`** | **evento discreto** | l'evento **resta discreto** *(il grafo è discreto)*, **ma la sua PROBABILITÀ o il suo TASSO dev'essere liscio** |

**⚠ TUTTI i punti di questo censimento sono di CLASSE `T`**: sono avvolgimenti e letture di fasi. **Le classi `L` ed `E` appartengono al censimento delle SCALE** *(`SCALE-TW`: soglia della mitosi, `discesa`, il punto di inversione, `tanh(3·…)`)*, **che è un lavoro diverso e non si fa qui.**

## IL CONTO PER TIPO

| tipo | che cos'è | gravi | non gravi |
|:--:|---|--:|--:|
| `OSS` | una grandezza a `4π` dentro una funzione a periodo `2π` | **31** | 0 |
| `W4` | un avvolgimento su `4π` | **3** | 10 |
| `W2` | un avvolgimento su `2π` | **0** | 4 |
| `A2P` | un `+2π` su una fase | **4** | 0 |

> **⚠ IL NUMERO CHE DECIDE `B1`: `31` punti in cui `phi` (che vive su `[0, 4π)`) entra in una funzione a periodo `2π`.**
> **In tutti e `31`, la doppia copertura di `phi` E' INVISIBILE alla fisica:** `exp(i(phi + 2π)) = exp(i phi)`.
> **Non è un'opinione sul modello: è un conto.** È la domanda §`B1` — *che cos'è `phi`?* — e **questa tabella è la sua evidenza.**

## ⚠ I FALSI POSITIVI, dichiarati invece che lasciati da scoprire

- **`_w4` (`:3423`) segnalato `A2P`:** quella riga *è* la **definizione** di un avvolgimento su `4π` — `(a + 2π) %% (4π) - 2π` — e il `+2π` fa parte della **costruzione del wrap**, non è un'antifase. **Il rilevatore `A2P` non può distinguerli guardando la riga**, e chiamarlo difetto sarebbe un errore. *(`_w4` resta comunque da classificare: **su che cosa viene applicato** decide se il periodo è giusto, e quello si vede dai suoi CHIAMANTI, non da qui.)*
- **`fonte = ?`:** lo strumento **non ha saputo** dire da dove viene il valore avvolto. **Si scrive `?`, non si indovina.**
- **`flag = —`** non significa «sempre attivo»: significa **nessun `if <FLAG>` che racchiude quella riga**. Il ramo può essere governato più in alto, o da una guardia che non è un flag.

## CHE COSA QUESTO STRUMENTO NON FA

**Non decide.** Ogni punto esce con la sua classe e col flag che lo governa; **la proposta è un lavoro a parte**, e per i punti non capiti si scrive `DA DECIDERE`.
**E non distingue ATTIVO da DORMIENTE da solo:** riporta **il flag**, e il default si legge dal sorgente. *(Un flag `False` non garantisce che il ramo non giri: il driver ne accende molti — è il fatto che la sezione `CURE VERIFICATE` ha reso visibile.)*
