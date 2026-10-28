# 2026-10-28 — LA GOBBA DEL VUOTO E IL SEGNO DELLA GRAVITA': UNA DOMANDA NELLA LISTA IN ATTESA *([[MAPPA-DEL-LAVORO]], [[PROGETTO-MASSA-COLLETTIVA]], [[VUOTO-SUL-FONDO]], [[PUNTO-FISSO-CS-SOLITONE]], [[CANALE-CS-SECONDA-SORGENTE]]; il mandato breve di Luca delle `10:40`)*

> ### **LIVELLO: una voce dell'indice e una riga della mappa; nessuna corsa, nessun file del nucleo.**
> ### **Le corse della rampa** *(`csv/_solitone_con_la_buca.py`, `327e5ad8`)* ### **girano e non si fermano:** ### **nessun file del loro percorso si tocca.**

## 0. IL MANDATO DELLE `10:40`, PER INTERO

```
MANDATO BREVE (2026-10-28 10:40) -- UNA DOMANDA NELLA LISTA IN ATTESA: LA GOBBA DEL VUOTO E IL SEGNO
DELLA GRAVITA' (da fare mentre girano le corse della rampa, senza fermarle)

LIVELLO: una voce dell'indice e una riga della mappa; nessuna corsa, nessun file del nucleo.

DECISIONE DI LUCA (2026-10-28 10:40): si registra nella lista in attesa di doc/MAPPA.md (sezione 4) la
domanda qui sotto; una voce dell'indice DOMANDA-GOBBA-SEGNO-GRAVITA (classe DOMANDA), legata a
PROGETTO-MASSA-COLLETTIVA, VUOTO-SUL-FONDO, PUNTO-FISSO-CS-SOLITONE (o il nome della voce del punto
fisso di cs), CANALE-CS-SECONDA-SORGENTE, al task history del solitone con la sua buca (3617ae6b,
327e5ad8), a 76eecbf5 e a 15df5c63.

IL FATTO (una lettura della prova breve, NON ancora una misura): dal vuoto UNIFORME la materia scava
il vuoto (Lambda per estremita' al centro da 1 a 0.08-0.22, 74f99039, 15df5c63); dal vuoto del FONDO
lo raccoglie: una GOBBA, Lambda 4.30 al centro contro 0.97 lontano (la prova breve dello script della
rampa, taglia piccola, pochi tick). E' lo stesso capovolgimento del verso dell'energia (76eecbf5),
visto nella forma del vuoto.

LA DOMANDA: la gravita' del modello viene da cs = Lambda/(Lambda + Lambda_c): piu' vuoto, cs piu'
alto, orologi piu' veloci. Con la BUCA, vicino a una massa gli orologi rallentano (come nella
relativita' generale); con la GOBBA accelererebbero (il contrario). Con cs acceso e il vuoto del
fondo, la massa crea attorno a se' un pozzo o una collina di cs? E la materia di prova CADE verso la
massa o se ne allontana? (Il verso della caduta nel gradiente di cs va preso dalle misure gia' fatte,
7daa8840 e la caduta da cs di 43c3a298, non assunto.)

LA MISURA, QUANDO SI APRE (descritta ora): (1) dal referto della rampa: la gobba resta, quanto e'
grande, si stabilizza? (2) il profilo di cs che la gobba darebbe (il conto, senza dinamica); (3) un
pacchetto di prova lento nel profilo di cs di un solitone sul vuoto del fondo: verso dove accelera.
La condizione: dopo il referto della rampa, e dopo la voce del punto fisso di cs col solitone (che
oggi impedisce di accendere cs con la materia densa).

LE POSSIBILI CONSEGUENZE, da scrivere come possibilita': il vuoto del fondo risolve il verso
dell'energia ma rovescia il segno della gravita'; oppure va rivista la dipendenza di cs da Lambda;
oppure la gobba con cs acceso non c'e'.

FORMA: la voce, la riga della MAPPA, un paragrafo nella RELAZIONE; FILE CAMBIATI esatto. Le corse
della rampa non si fermano.
```

## 1. RAGIONAMENTO PRELIMINARE

- ### **Che cosa credo:** ### **la gobba e' un fatto di POCHI tick, alla taglia piccola, da una prova** *(`614` tick di rampa tanh a `T_r 25`, `10` dopo)*: ### **non so se resta.** ### **La domanda e' ben posta solo se resta;** ### **per questo la misura `(1)` e' il referto della rampa.**
- ### **Un fatto nuovo, dalle corse di oggi, che pesa sulla condizione:** ### **alla taglia piccola** *(`N 1e5`, `L 48`)* ### **il congelato si rompe a `s 0.075`** *(tick `2200`, tempo fisico `165`; anche a `r = 0`)*. ### **La prova breve della gobba era a quella taglia:** ### **la gobba va riletta alla taglia grande.**
- ### **Che cosa NON so:** ### **il verso della caduta nel gradiente di `cs`** *(il mandato lo vieta come assunto: va preso da `7daa8840` e da `43c3a298`)*; ### **se `CAMM-FASE-VUOTO` con `cs` acceso cambi la gobba;** ### **la causa della gobba.**

## 2. PROGETTAZIONE DEL RAGIONAMENTO

1. ### **la voce** `DOMANDA-GOBBA-SEGNO-GRAVITA` ### **con `crea-lotto`:** ### ⚠ **la classe `DOMANDA` NON C'E' nel vocabolario chiuso:** ### **`DECISIONE`, stato `AGENDA`, come `DOMANDA-CHIRALITA` e le due domande sulla carica** *(dichiarato, non scelto di nascosto)*; ### **collegata alle quattro voci del mandato.**
2. ### **la riga `12` della lista in attesa** *(sezione `4` di `doc/MAPPA.md`)*.
3. ### **un paragrafo nella RELAZIONE.**
- ### **Cosa mi farebbe fermare:** ### **un ID collegato che non esiste** *(controllato: esistono tutti e quattro)*; ### **un presidio che rifiuta per un file che le corse stanno scrivendo** *(la via d'uscita dichiarata `SENZA-NON-TRACCIATI`, a run aperto)*.

## 3. TODO DEL NEXT STEP

1. ### **questo task history, committato e pushato da solo;**
2. ### **la voce, la riga `12` della MAPPA, la RELAZIONE, in un commit;**
3. ### **poi si torna alle corse della rampa.**
