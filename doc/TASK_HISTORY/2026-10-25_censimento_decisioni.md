# IL CENSIMENTO DELLE DECISIONI DI LUCA: QUALI SONO NEL NUCLEO, QUALI SOLO NEGLI STRUMENTI, QUALI SOLO NEI DOCUMENTI

> **Il mandato:** di Luca, `2026-10-25` *(«abbiamo gia' regole che dovrebbero essere embeddate direttamente nel simulatore e che invece sono ancora in memoria», `15:52`)*. ### **SOLA LETTURA:** ### **nessun file del nucleo, degli strumenti o dell'indice cambiato, tranne il documento `doc/CENSIMENTO_DECISIONI.md`, questo task history, la relazione e la voce del censimento.** ### **Il caso verificato dal guardiano: [[DECISIONE-SOLO-TRIANGOLI]] NON e' nel nucleo.**

**LIVELLO:** un censimento in sola lettura.

## 0. LA STELLA POLARE

1. **`A14`:** ### **non si applica** *(nessuna legge cambia: e' un censimento)*.
2. **Il gradino:** ### **non si applica** *(nessun risultato di fisica)*.
3. **Aggiunge un numero o una legge?** ### **No.** ### **Il censimento DICE dove manca una legge, non la aggiunge.**
4. **Tocca `rho`, `c_s` o il segno?** ### **No.**
5. **Emergente o imposto?** ### **Non si applica.**

## 1. IL RAGIONAMENTO PRELIMINARE

- ### **LE FONTI** *(fissate qui)*: ### **`(F1)` le voci di classe `DECISIONE` dell'indice** *(`python csv/indice.py cerca --classe DECISIONE`: `93` voci, di cui `16` `CHIUSA`)*; ### **`(F2)` i nodi dell'albero con `presa: true`** *(`doc/ALBERO_era2.yaml`, letto con `yaml`: `6` su `15`)*; ### **`(F3)` le decisioni scritte nei task history dal `2026-10-08`** *(`66` file su `125` nominano «decisione di Luca»)*; ### **`(F4)` il registro della fisica** *(`doc/REGISTRO_FISICA.md`: `83` righe)*.
- ### ⚠ **LA TRAPPOLA CHE VEDO GIA':** ### **lo `stato` di una voce `DECISIONE` NON dice se Luca ha deciso** *(`DECISIONE-SOLO-TRIANGOLI` e' `AGENDA` ma e' decisa; molte `DOMANDA-...` sono di classe `DECISIONE` ma sono domande aperte)*: ### **la classe dice «serve una decisione», non «c'e' una decisione».** ### **Quindi il censimento legge la descrizione di ogni voce e la fonte, e CLASSIFICA a mano** *(decisa / aperta / superata)*, ### **dichiarandolo** *(e un programma non potrebbe farlo: `DECISIONE-VUOLE-UN-CAMPO`)*.
- ### **LE CATEGORIE di dove sta una decisione** *(fissate qui)*: ### **NEL NUCLEO** *(`primo_ordine/` e `leggi.yaml`: file e riga)*; ### **SOLO NEGLI STRUMENTI** *(`csv/`, in memoria)*; ### **SOLO NEI DOCUMENTI**; ### **DA NESSUNA PARTE.** ### **E il giudizio:** ### **GIUSTO** *(una regola di prova nei documenti di metodo; una legge non decisa in memoria)* ### **o MANCANZA.**
- ### **NON so** ### **quante delle decisioni nei task history siano gia' voci dell'indice** *(le duplicazioni si contano una volta, dichiarandolo)*.

## 2. LA PROGETTAZIONE

1. ### **le query e i file, scritti nel documento** *(il numero visto per fonte)*;
2. ### **una riga per decisione:** la data e le parole di Luca; che cosa chiede al simulatore *(una legge, una scena, un parametro, una regola di prova, un principio, niente)*; dove sta, con file e riga; giusto o mancanza;
3. ### **per ogni mancanza:** i file, il sigillo di riduzione al bit, la suite, se cambia l'impronta `2e7f795d2a52fbe7`, da quale decisione aperta dipende;
4. ### **la tabella riassuntiva in testa e l'ordine proposto** *(una proposta)*;
5. ### **il caso dei triangoli:** `primo_ordine/scena_l2.py`, `primo_ordine/driver.py`, `csv/_triangoli.py`.
- ### **Mi FERMO se** ### **una fonte non si lascia contare** *(lo scrivo come tale, e conto cio' che si conta)*.

## 3. TODO DEL NEXT STEP

1. questo task history, da solo, controllato leggendo tutta l'uscita;
2. `doc/CENSIMENTO_DECISIONI.md`, la voce dell'indice, la relazione.
