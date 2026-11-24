# La delega (il perimetro della posta)

Decisione di Luca, 2026-11-24, 23:46 ([M2345]), sul perimetro proposto dal guardiano alle 23:43. Luca può restringerla o revocarla con una riga in chat, in qualunque momento; il guardiano la riporta qui con l'ora.

Ogni mandato in `posta/` dichiara in testa una delle tre categorie:

- **DELEGA**: il Cantiere esegue senza chiedere. Rientrano: letture su stati già salvati; documentazione (sagoma, carta, relazione, MAPPA) che registra numeri senza giudizio; corse entro il tetto: al più 5 per mandato, ≤ 6000 tick ciascuna, dentro i vincoli della macchina (10 processi a un filo, freno 4 GB, CPU < 90%), con stati ogni 250, su scene e script già esistenti, senza file nuovi nel nucleo e senza gestione nuova.
- **DECISIONE DI LUCA (hh:mm)**: Luca ha deciso in chat; il guardiano riporta l'ora e le parole. Il Cantiere esegue.
- **ATTESA DI LUCA**: il guardiano propone; il Cantiere NON esegue finché Luca non ratifica in chat (il guardiano aggiorna il file dell'INDICE con l'ora della ratifica). Rientrano sempre: soglie e criteri che decidono un verdetto; scene o semine nuove; il nucleo (primo_ordine/); i lanciatori, le code, i presidi, le attività pianificate; le forme della non linearità; lo zero del vuoto; qualunque merge.

Il guardiano non è un secondo comandante: la posta toglie a Luca il copia-incolla, non la decisione.
