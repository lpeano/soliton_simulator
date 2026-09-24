# LA MAPPA DEL `4pi` -- **di chi e' la doppia copertura, punto per punto**

> **GENERATA** da `csv/_test_fork/_mappa_4pi.py`, che **riusa `_censimento_fasi.py`**
> (`Z118`). **Sola lettura, AST.** Stato effettivo dei flag: dal referto di configurazione del run `_g4_corto`, commit 757bc285.

## LE QUATTRO CLASSI

| classe | che cos'e' | che se ne fa l'architettura a un solo ponte |
|:--:|---|---|
| **`VERA`** | la doppia copertura **dello SPINORE**: un oggetto di spin 1/2 torna in se' dopo `4pi`. **E' fisica.** | **RESTA**, ed e' l'unico posto dove il `4pi` vive |
| **`DICHIARATA`** | il **dominio `[0, 4pi)` di `phi`**: una **convenzione del codice**, non una proprieta' misurata | **CADE**: `phi` diventa una lettura dello spinore, su `2pi` |
| **`EREDITATA`** | cio' che prende la sua **scala** da `phi` | **si RIDERIVA** dal trasporto degli spinori, non dalle differenze di `phi` |
| **`INVERSA`** | **il finto pilota il vero**: una grandezza ereditata SCRIVE una grandezza spinoriale | **si ABOLISCE**: e' il verso sbagliato del ponte |

**Precedenza dichiarata:** `INVERSA` > `VERA` > `DICHIARATA` > `EREDITATA`. Un sito che e' sia spinoriale sia scritto da `tw` e' **`INVERSA`**, perche' la domanda e' *dove il finto comanda il vero*.

## I PUNTI

| riga | funzione | tipo | **di chi** | regola che l'ha deciso | flag | **EFFETTIVO nei run** |
|--:|---|:--:|:--:|---|---|:--:|
| `:410` | `(modulo)` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | - | **-** |
| `:602` | `stato_crossover` | `OSS` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | — | **-** |
| `:1517` | `__init__` | `SWEEP` | **`VERA`** | l'espressione contiene una grandezza SPINORIALE | - | **-** |
| `:1690` | `_aggiorna_lift_spinoriale` | `SWEEP` | **`VERA`** | l'espressione contiene una grandezza SPINORIALE | - | **-** |
| `:1700` | `_aggiorna_lift_spinoriale` | `SWEEP` | **`VERA`** | l'espressione contiene una grandezza SPINORIALE | - | **-** |
| `:1842` | `_eredita_spinore_figli` | `SWEEP` | **`VERA`** | l'espressione contiene una grandezza SPINORIALE | - | **-** |
| `:1843` | `_eredita_spinore_figli` | `SWEEP` | **`VERA`** | l'espressione contiene una grandezza SPINORIALE | - | **-** |
| `:1846` | `_eredita_spinore_figli` | `SWEEP` | **`VERA`** | l'espressione contiene una grandezza SPINORIALE | - | **-** |
| `:1876` | `olonomia_lift_ciclo` | `SWEEP` | **`VERA`** | l'espressione contiene una grandezza SPINORIALE | - | **-** |
| `:1881` | `olonomia_lift_ciclo` | `SWEEP` | **`VERA`** | l'espressione contiene una grandezza SPINORIALE | - | **-** |
| `:1951` | `_feedback_spinoriale_archi` | `SWEEP` | **`VERA`** | l'espressione contiene una grandezza SPINORIALE | - | **-** |
| `:1953` | `_feedback_spinoriale_archi` | `SWEEP` | **`VERA`** | l'espressione contiene una grandezza SPINORIALE | - | **-** |
| `:1961` | `_feedback_spinoriale_archi` | `SWEEP` | **`VERA`** | l'espressione contiene una grandezza SPINORIALE | - | **-** |
| `:2060` | `misura_spin_picco_massa` | `SWEEP` | **`VERA`** | l'espressione contiene una grandezza SPINORIALE | - | **-** |
| `:2095` | `misura_spin_picco_massa` | `SWEEP` | **`VERA`** | l'espressione contiene una grandezza SPINORIALE | - | **-** |
| `:2097` | `misura_spin_picco_massa` | `SWEEP` | **`VERA`** | l'espressione contiene una grandezza SPINORIALE | - | **-** |
| `:2098` | `misura_spin_picco_massa` | `SWEEP` | **`VERA`** | l'espressione contiene una grandezza SPINORIALE | - | **-** |
| `:2245` | `circolazione_topologica` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | - | **-** |
| `:2246` | `circolazione_topologica` | `SWEEP` | **`DICHIARATA`** | avvolgimento del DOMINIO di `phi` (convenzione, non misura) | - | **-** |
| `:2377` | `semina` | `SWEEP` | **`DICHIARATA`** | avvolgimento del DOMINIO di `phi` (convenzione, non misura) | - | **-** |
| `:2378` | `semina` | `SWEEP` | **`DICHIARATA`** | avvolgimento del DOMINIO di `phi` (convenzione, non misura) | - | **-** |
| `:2436` | `_registra_concorrenza` | `OSS` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | — | **-** |
| `:2475` | `aggiorna_pesi_concorrenza` | `OSS` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | — | **-** |
| `:2481` | `aggiorna_pesi_concorrenza` | `OSS` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | — | **-** |
| `:2484` | `aggiorna_pesi_concorrenza` | `OSS` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | — | **-** |
| `:2598` | `ritmo` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | TEMPO_SEGNO | **False** |
| `:2610` | `ritmo` | `W2` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | — | **-** |
| `:2634` | `ritmo` | `W2` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | RITMO_WRAP_2PI | **False** |
| `:2636` | `ritmo` | `A2P` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | RITMO_WRAP_2PI | **False** |
| `:2636` | `ritmo` | `W4` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | RITMO_WRAP_2PI | **False** |
| `:2856` | `_passo_spinoriale` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | SPIN_LARMOR | **False** |
| `:3095` | `_passo_spinoriale` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | TW_SPINORE | **False** |
| `:3095` | `_passo_spinoriale` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | TW_SPINORE | **False** |
| `:3097` | `_passo_spinoriale` | `SWEEP` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | TW_SPINORE | **False** |
| `:3098` | `_passo_spinoriale` | `SWEEP` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | TW_SPINORE | **False** |
| `:3098` | `_passo_spinoriale` | `SWEEP` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | TW_SPINORE | **False** |
| `:3099` | `_passo_spinoriale` | `SWEEP` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | TW_SPINORE | **False** |
| `:3099` | `_passo_spinoriale` | `SWEEP` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | TW_SPINORE | **False** |
| `:3100` | `_passo_spinoriale` | `SWEEP` | **`INVERSA`** | bersaglio spinoriale/Bloch, valore che discende da `tw` (via `_degt`, `_otw`, `omega_new`) | TW_SPINORE | **False** |
| `:3137` | `_passo_spinoriale` | `OSS` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | DEPARAM_OROLOGIO | **True** |
| `:3173` | `_passo_spinoriale` | `SWEEP` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | DEPARAM_OROLOGIO | **True** |
| `:3186` | `_passo_spinoriale` | `SWEEP` | **`VERA`** | sito dichiarato da Luca: _phc: la fase dell'orologio proprio, dove il 4pi e' dello spinore | DEPARAM_OROLOGIO | **True** |
| `:3186` | `_passo_spinoriale` | `SWEEP` | **`VERA`** | sito dichiarato da Luca: _phc: la fase dell'orologio proprio, dove il 4pi e' dello spinore | DEPARAM_OROLOGIO | **True** |
| `:3187` | `_passo_spinoriale` | `SWEEP` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | DEPARAM_OROLOGIO | **True** |
| `:3220` | `_passo_spinoriale` | `SWEEP` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | KURAMOTO_SU2 | **False** |
| `:3222` | `_passo_spinoriale` | `SWEEP` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | KURAMOTO_SU2 | **False** |
| `:3223` | `_passo_spinoriale` | `SWEEP` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | KURAMOTO_SU2 | **False** |
| `:3264` | `_passo_spinoriale` | `SWEEP` | **`INVERSA`** | bersaglio spinoriale/Bloch, valore che discende da `tw` (via `psi_sp_new`) | SPINORE_CORRETTO | **True** |
| `:3329` | `_pesi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | KERNEL_ALPHA | **1.0** |
| `:3385` | `calcola_psi` | `OSS` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | — | **-** |
| `:3395` | `calcola_psi` | `OSS` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | CAMPO_SPINORIALE | **True** |
| `:3466` | `_wphi` | `W2` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | FASE_2PI | **False** |
| `:3467` | `_wphi` | `A2P` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | — | **-** |
| `:3467` | `_wphi` | `W4` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | — | **-** |
| `:3470` | `_w4` | `A2P` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | — | **-** |
| `:3470` | `_w4` | `W4` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | — | **-** |
| `:4413` | `step` | `OSS` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | TEMPO_SEGNO | **False** |
| `:4422` | `step` | `OSS` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | SYNC_UPDATE | **False** |
| `:4424` | `step` | `OSS` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | — | **-** |
| `:4425` | `step` | `OSS` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | — | **-** |
| `:4453` | `step` | `OSS` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | REPULS_LEGGE | **True** |
| `:4463` | `step` | `OSS` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | REPULS_LEGGE | **True** |
| `:4545` | `step` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | CHI_CORE | **True** |
| `:4553` | `step` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | VERSO_CHI | **False** |
| `:4555` | `step` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | CHI_CORE | **True** |
| `:4644` | `step` | `OSS` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | K_SYNC | **1.0** |
| `:4646` | `step` | `OSS` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | K_SYNC | **1.0** |
| `:4672` | `step` | `SWEEP` | **`DICHIARATA`** | avvolgimento del DOMINIO di `phi` (convenzione, non misura) | - | **-** |
| `:4675` | `step` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | - | **-** |
| `:4694` | `step` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | POLO_MATURO | **False** |
| `:4696` | `step` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | POLO_MATURO | **False** |
| `:4698` | `step` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | TORS_4PI | **True** |
| `:4698` | `step` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | TORS_4PI | **True** |
| `:4699` | `step` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | TORS_4PI | **True** |
| `:4699` | `step` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | TORS_4PI | **True** |
| `:4702` | `step` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | TORS_4PI | **True** |
| `:4715` | `step` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | CHI_BASC,CHI_COOP,CHI_DA_SPINORE | **True** |
| `:4757` | `step` | `OSS` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | SYNC_UPDATE | **False** |
| `:4878` | `step` | `OSS` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | HAM_SRC | **0.0** |
| `:5153` | `mitosi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | FASE_2PI,TORS_4PI | **False** |
| `:5154` | `mitosi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | FASE_2PI,TORS_4PI | **False** |
| `:5154` | `mitosi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | FASE_2PI,TORS_4PI | **False** |
| `:5154` | `mitosi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | FASE_2PI,TORS_4PI | **False** |
| `:5156` | `mitosi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | FASE_2PI,TORS_4PI | **False** |
| `:5156` | `mitosi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | FASE_2PI,TORS_4PI | **False** |
| `:5166` | `mitosi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | - | **-** |
| `:5193` | `mitosi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | TORS_4PI | **True** |
| `:5196` | `mitosi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | TORS_4PI | **True** |
| `:5211` | `mitosi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | - | **-** |
| `:5225` | `mitosi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | - | **-** |
| `:5233` | `mitosi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | - | **-** |
| `:5234` | `mitosi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | - | **-** |
| `:5234` | `mitosi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | - | **-** |
| `:5235` | `mitosi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | - | **-** |
| `:5235` | `mitosi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | - | **-** |
| `:5235` | `mitosi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | - | **-** |
| `:5238` | `mitosi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | - | **-** |
| `:5238` | `mitosi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | - | **-** |
| `:5323` | `mitosi` | `SWEEP` | **`DICHIARATA`** | avvolgimento del DOMINIO di `phi` (convenzione, non misura) | - | **-** |
| `:5339` | `mitosi` | `SWEEP` | **`DICHIARATA`** | avvolgimento del DOMINIO di `phi` (convenzione, non misura) | MITOSI_DIR | **0.0** |
| `:5341` | `mitosi` | `SWEEP` | **`DICHIARATA`** | avvolgimento del DOMINIO di `phi` (convenzione, non misura) | MITOSI_DIR | **0.0** |
| `:5362` | `mitosi` | `SWEEP` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | ANTIFASE_ADD | **False** |
| `:5363` | `mitosi` | `SWEEP` | **`DICHIARATA`** | avvolgimento del DOMINIO di `phi` (convenzione, non misura) | ANTIFASE_ADD | **False** |
| `:5392` | `mitosi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | - | **-** |
| `:5399` | `mitosi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | REGIME | **deterministico** |
| `:5405` | `mitosi` | `SWEEP` | **`DICHIARATA`** | avvolgimento del DOMINIO di `phi` (convenzione, non misura) | REGIME | **deterministico** |
| `:5406` | `mitosi` | `SWEEP` | **`DICHIARATA`** | avvolgimento del DOMINIO di `phi` (convenzione, non misura) | REGIME | **deterministico** |
| `:5410` | `mitosi` | `SWEEP` | **`DICHIARATA`** | avvolgimento del DOMINIO di `phi` (convenzione, non misura) | REGIME | **deterministico** |
| `:5423` | `mitosi` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | PLAST_DIN | **True** |
| `:5455` | `mitosi` | `SWEEP` | **`DICHIARATA`** | avvolgimento del DOMINIO di `phi` (convenzione, non misura) | - | **-** |
| `:5456` | `mitosi` | `SWEEP` | **`DICHIARATA`** | avvolgimento del DOMINIO di `phi` (convenzione, non misura) | - | **-** |
| `:5499` | `mitosi` | `SWEEP` | **`DICHIARATA`** | avvolgimento del DOMINIO di `phi` (convenzione, non misura) | COPPIA_MIT,MAX_NODI | **1.0** |
| `:5564` | `mitosi` | `SWEEP` | **`DICHIARATA`** | avvolgimento del DOMINIO di `phi` (convenzione, non misura) | COPPIA_MIT,MAX_NODI | **1.0** |
| `:5565` | `mitosi` | `SWEEP` | **`DICHIARATA`** | avvolgimento del DOMINIO di `phi` (convenzione, non misura) | COPPIA_MIT,MAX_NODI | **1.0** |
| `:5598` | `campo_spaziale` | `OSS` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | — | **-** |
| `:5789` | `memoria_hebbiana_moto` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | GRAV_BIFASE | **True** |
| `:5872` | `memoria_hebbiana_moto` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | VIRIALE | **True** |
| `:5950` | `memoria_hebbiana_moto` | `OSS` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | K_FRANGE | **0.0** |
| `:6128` | `memoria_hebbiana_moto` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | - | **-** |
| `:6161` | `memoria_hebbiana_moto` | `SWEEP` | **`DICHIARATA`** | avvolgimento del DOMINIO di `phi` (convenzione, non misura) | MEM_MOTO_TUTTO | **True** |
| `:6174` | `diagnostica` | `OSS` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | — | **-** |
| `:6440` | `(modulo)` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | - | **-** |
| `:6660` | `_render_vista_rete_sola` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | - | **-** |
| `:6733` | `_render_vista_rete_sola` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | - | **-** |
| `:6980` | `update` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | - | **-** |
| `:7021` | `update` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | - | **-** |
| `:8296` | `batch_condensazione` | `SWEEP` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | - | **-** |
| `:8626` | `batch_condensazione` | `W2` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | — | **-** |
| `:8643` | `batch_condensazione` | `OSS` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | — | **-** |
| `:8644` | `batch_condensazione` | `OSS` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | — | **-** |
| `:8734` | `batch_condensazione` | `OSS` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | — | **-** |
| `:8736` | `batch_condensazione` | `OSS` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | — | **-** |
| `:8797` | `batch_condensazione` | `OSS` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | — | **-** |
| `:8809` | `batch_condensazione` | `W2` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | — | **-** |
| `:8924` | `batch_condensazione` | `OSS` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | — | **-** |
| `:8933` | `batch_condensazione` | `OSS` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | — | **-** |
| `:8947` | `batch_condensazione` | `OSS` | **`?`** | nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara | — | **-** |
| `:8990` | `batch_condensazione` | `OSS` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | — | **-** |
| `:9025` | `batch_condensazione` | `OSS` | **`EREDITATA`** | legge una grandezza che prende la sua scala da `phi` | — | **-** |

**Conteggio per classe:** **?** 27 . **DICHIARATA** 17 . **EREDITATA** 76 . **INVERSA** 2 . **VERA** 17

> **!! `27` punti NON CLASSIFICATI**, e restano `?`: nessuna regola ha attaccato. **Non li forzo in una classe**, perche' una classe assegnata a forza e' peggio di una cella vuota.

### !! COME SI LEGGE UNA `INVERSA`, e il limite e' dichiarato

**Il contagio da `tw` e' INSENSIBILE AL FLUSSO: ignora i gate.** Quindi una `INVERSA` dice *"la catena ESISTE nel codice"*, **non** *"gira adesso"*. Per sapere se gira si guarda la colonna **EFFETTIVO**.

**Le due `INVERSA` trovate stanno sulla STESSA catena**, ed e' quella di `TW_SPINORE`:

```
  tw  --> _twh = tw/(2*PHI_CRIT)        :3095
      --> np.add.at(_otw, ii, _axis*_twh)   :3098-3099   (mutazione IN PLACE)
      --> omega_new = omega_new + _otw/...  :3100        *** INVERSA ***
      --> psi_sp_new  (integra omega_new)
      --> self._psi_spinor = psi_sp_new     :3264        *** INVERSA (conseguenza) ***
```

> **`:3100` e' il PONTE SBAGLIATO** *(la torsione che scrive `omega_s`, cioe' lo spinore)*, **e `:3264` e' la sua CONSEGUENZA**: il commit atomico dello spinore. **`:3264` non e' un difetto in se'** -- diventa un ponte inverso **solo** se `:3100` ha scritto.
> **E OGGI NESSUNA DELLE DUE GIRA: `TW_SPINORE = False`.** La catena e' **in codice e spenta**, e l'architettura a un solo ponte deve dire **se puo' esistere affatto**.

## IL GRAFO DELLE DIPENDENZE

```
  SPINORE (4pi VERO)
      |  _phc / phivel / omega_clk
      v
    phi  (4pi DICHIARATO -- la convenzione)
      |  dph = _wphi(phi[i] - phi[j])   :4675
      v
  twp, tw  (EREDITATO)                  :4698-4699
      |                |            |              |
      v                v            v              v
   MITOSI          SCHWINGER    REPULSIONE       TEMPI
   soglia,         antifase,    max compress.    ritmo, tau_pp
   campana         prob_coppia  (S05)            d/cs

  E IL VERSO SBAGLIATO, che l'architettura deve abolire:
    tw  ---- TW_SPINORE ---->  omega_s  (lo SPINORE)     *** INVERSA ***
```

| da | a | come | classe |
|---|---|---|:--:|
| SPINORE `psi_spinor` | `phi` | `_phc` / `phivel` / `omega_clk`: l'orologio proprio nasce dalla fase dello spinore | `VERA -> DICHIARATA` |
| `phi` | `dph` | `dph = _wphi(phi[i] - phi[j])` (`:4675`) | `DICHIARATA -> EREDITATA` |
| `dph` | `twp`, `tw` | `tw += _w8(dph + twist_dip - twp)` (`:4698-4699`) | `EREDITATA` |
| `tw` | MITOSI | `avv = |tw|`, soglia `PHI_CRIT + twist_max`, campana fino a `TW_TETTO` | `EREDITATA` |
| `tw` | SCHWINGER | `eccesso_torsione` -> `prob_coppia`, e l'antifase `fm + dphi/2` | `EREDITATA` |
| `tw` | REPULSIONE / `d0` | il termine di massima compressione (`S05`) | `EREDITATA` |
| `tw` | TEMPI | `ritmo()` ramo `TEMPO_SEGNO` (`r = 1 + mean|tw|/PHI_CRIT`) e `tau_pp` | `EREDITATA` |
| `phi` | TEMPI | `ritmo()` ramo VIVO: `signed` da `np.angle(psi_spin)`, gauge, bottleneck | `DICHIARATA -> EREDITATA` |
| `tw` | SPINORE | `TW_SPINORE`: `_otw` sommato a `omega_new` (`:2149-2154`) | `*** INVERSA ***` |

> **!! COSA QUESTA MAPPA NON FA: non decide.** Dice **di chi** e' il `4pi` in ogni punto e **se quel punto gira**. La proposta e' una **scheda a parte**.
