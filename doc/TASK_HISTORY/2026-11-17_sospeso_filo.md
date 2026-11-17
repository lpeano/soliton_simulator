# IL FILO DELLA RICERCA MESSO IN SALVO E IN SOSPESO *(Luca `2026-11-17` `09:19`-`09:20`)*

> **Il mandato:** la verifica nella scatola giusta *(`doc/PIANO_VERIFICA_SCATOLA.md`)* e' **SOSPESA** e si rifara'; nessuna corsa si riprende stasera. **Prima di sospendere, tutto il filo di questi giorni in UN documento:** `doc/SOSPESO_2026-11-17_FILO_DELLA_RICERCA.md` *(parti `1`-`6`)*. **Il testo e' del guardiano; io lo porto nel documento CONTROLLANDO ogni numero contro il referto citato: se non torna NON lo cambio, scrivo accanto «il referto dice ...» e lo segnalo nel commit.**

## 1. LE PREMESSE DAL CODICE *(cosa credo prima di guardare; cosa NON so)*

- **Il documento e' di sola scrittura in `doc/`:** nessuna corsa, nessun file del nucleo, nessun file o stato cancellato. Le corse sono tutte ferme dalle `08:00` *(la carta notte, sez. `7`; `b8b1977a`)*.
- **I numeri delle parti `1`-`3` vengono da referti di giorni diversi**, molti sulle corse di `L 162` *(`doc/referti_l2/mattone/`)*. **NON so ancora** quanti si ritrovano tali e quali: alcuni sono stati scritti dal guardiano a memoria, o arrotondati, o di un'altra corsa. **Se un numero non lo trovo, lo scrivo «NON TROVATO»: non e' un errore, e' una provenienza mancante** (`L-NUMERI`).
- **La condizione di ripresa** *(parte `5`)*: «lo sha1 di `doc/NUCLEO_CONGELATO.md` di oggi». **Quel file dice lo STATO del congelamento, non i byte del nucleo:** accanto scrivo anche gli sha1 dei `12` file del nucleo che le voci del registro della notte hanno timbrato *(il campo `nucleo.sha1_byte`)*, perche' sono quelli che decidono se gli stati sono riprendibili.

## 2. PROGETTAZIONE DEL RAGIONAMENTO

1. **Il controllo dei numeri, per parte:** per ogni numero, il file e la riga *(o il commit)* dove sta. **Il controllo lo fanno due agenti in sola lettura** *(parti `1A`-`1D`; parti `1E`-`4`)*; **ogni «NON TORNA» lo ricontrollo io sul file** prima di scriverlo.
2. **Il documento:** il testo del guardiano **com'e'**; accanto a ogni numero che non torna «*(il referto dice ...)*»; accanto a ogni numero non trovato «*(la fonte: non trovata)*»; **la fonte di ogni parte.**
3. **Le righe che lo richiamano:** il piano di verifica e la ROTTA *(«SOSPESO per decisione di Luca 2026-11-17 09:19, da rifare»)*; R-SCATOLA al `5%` nella ROTTA *(ADOTTATA per il mattone singolo; per gli oggetti composti «da ridefinire», Q2)*; la relazione.
4. **Cosa mi farebbe FERMARE:** un numero che cambia una CONCLUSIONE *(per esempio una previsione scritta confermata che il referto dice fallita)*: **lo scrivo accanto e lo metto in testa al commit e al messaggio**, non lo correggo io.

## 3. TODO DEL NEXT STEP

1. questa carta: commit e push **prima** del documento;
2. il controllo dei numeri *(gli agenti; i miei ricontrolli)*;
3. il documento; il piano, la ROTTA, la relazione; commit e push;
4. **FERMO** *(fine del mandato)*.
