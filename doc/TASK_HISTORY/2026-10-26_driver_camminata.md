# IL PROGETTO DEL DRIVER DELLA CAMMINATA *(la parte 3 del mandato del 2026-10-26, 08:57)*

> **Il mandato:** di Luca, `2026-10-26`, con la decisione `(1)` delle `08:57`: ### **la lettura `(ii)` di `2026-10-25_driver_triangoli.md`: il driver fara' girare la CAMMINATA** *(`tick.tick` sulla scena a triangoli)*; ### **PRIMA un documento di progetto, nessun codice** *([[DOMANDA-DRIVER-CAMMINATA]], [[DECISIONE-SOLO-TRIANGOLI]], [[SUITE-NEL-COMMIT]])*.
> ### **Il documento: `doc/PROGETTO_DRIVER_CAMMINATA.md`.**

**LIVELLO:** un documento di progetto.

## 0. LA STELLA POLARE

1. **`A14`:** ### **non si applica.** 2. **Il gradino:** ### **il programma che fa girare la fisica.** 3. **Aggiunge un numero o una legge?** ### **No.** 4. **Tocca `rho`, `c_s` o il segno?** ### **No.** 5. **Emergente o imposto?** ### **Uno strumento.**

## 1. LE FONTI *(lette per nome)*

- ### **`primo_ordine/driver.py`** *(`grafo`, `termini_attivi`, `osservatori_attivi`, `gira`, `main`)*; ### **`primo_ordine/config/schema_config.py`** *(`CAMPI`, `SCENE`, `INTEGRATORI`, `valida`, `carica`, `impronta`)*; ### **`primo_ordine/timbro.py`** *(`timbro`, `conto_leggi`, `impronta_generati`, `righe_timbro`, `salva`, `riprendi`)*; ### **`primo_ordine/tick.py`** *(`tick`, `percorri_tick`)*; ### **`primo_ordine/scena_l2.py`** *(`scena_toro`, `GRIGLIA_DEL_MODELLO`)*; ### **`primo_ordine/composizione.py`** *(`ORDINE`, `IMPRONTA`)*; ### **i collaudi che usano il driver o `config/prova.yaml`** *(`_collauda_determinismo`, `_collauda_grafo`, `_collauda_simmetrie`, `_collauda_passo`, `_collauda_cs`)*.

## 2. LA PROGETTAZIONE

### **Le sezioni: che cosa e' oggi; che cosa diventa; le opzioni** *(una seconda pipeline nello stesso driver, contro un driver nuovo)*; ### **lo schema della configurazione; il timbro; il sigillo; le domande per Luca, numerate.** ### **Nessuna scelta.**

## 3. TODO

1. questo task history, da solo; 2. il documento, la relazione, l'indice.

## 4. IL RISULTATO

### **`doc/PROGETTO_DRIVER_CAMMINATA.md`: sette sezioni, sette domande per Luca; nessuna scelta.** ### **Una correzione mentre scrivevo:** ### **avevo elencato `_collauda_motore` fra chi chiama `tick`; non lo importa** *(lo importano `_collauda_tempo_proprio`, `_collauda_cs`, `_collauda_cs_centro`, `_collauda_cs_l1`, `_collauda_deriva`, `_collauda_scala`)*.
