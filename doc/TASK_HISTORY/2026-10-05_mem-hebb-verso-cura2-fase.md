# `MEM-HEBB-VERSO`, passo (2) — **LA CURA DEL SITO DELLA FASE (lo SPEGNIMENTO)**, piu' **IL PROGRAMMA CONCORDATO**

## STATO: **NON INIZIATO** — in coda dopo `Z43` passo (1)

*(Messo al sicuro nel repo il **2026-10-05**, **mentre il mandato `Z43` passo (1) era in
corso**. ### **Nessun lavoro e' stato fatto su questo mandato.**)*

> ### ⛔ **PERCHE' NON PARTE SUBITO, e non e' una mia scelta: e' `L-UN-PROMPT`** — *«un
> prompt alla volta; i rilievi che arrivano durante un lavoro vanno in CODA, non lo
> interrompono»*. ### **E il mandato stesso lo dice:** *«Si esegue DOPO il mandato `Z43`
> passo (1), che e' in coda prima di questo»*.

> ### ⛔ **LA SEZIONE `LA STELLA POLARE` NON E' QUI, E NON PER DIMENTICANZA:** il mandato
> chiede *«task history PRIMA del codice, con `LA STELLA POLARE`»*, e si scrive **quando il
> lavoro parte**. ### **Scritta adesso sarebbe una risposta data prima di aver letto il
> codice, cioe' esattamente la ricostruzione che il par.8 esiste per impedire.**

> ### ⚠ **E IL TESTO QUI SOTTO E' COPIATO PAROLA PER PAROLA**, come per il mandato del
> 2026-10-04: **non e' riassunto ne' riformulato.** Se una riga sembra ambigua,
> l'ambiguita' e' **nell'originale** e va risolta con Luca, non da me.

---

## IL MANDATO, verbatim

MANDATO: MEM-HEBB-VERSO, PASSO (2): LA CURA DEL SITO DELLA FASE (lo SPEGNIMENTO), piu' IL PROGRAMMA CONCORDATO. Si esegue DOPO il mandato Z43 passo (1), che e' in coda prima di questo.

PARTE 1: IL PROGRAMMA, deciso da Luca il 2026-10-05, da scrivere nel "TODO ALLA RIPRESA" di doc/TASK_HISTORY/2026-10-04_mem-hebb-verso-misura.md e da collegare in doc/INDICE_ID.tsv (Z43, MEM-HEBB-VERSO, TETTO-CAUSALE-TEMPO-COORDINATO):
 1. Z43 passo (1), la misura del tempo proprio r (in coda prima di questo).
 2. MEM-HEBB-VERSO passo (2): lo spegnimento del sito della fase (questo mandato).
 3. Decisione di Luca sulla definizione di r, dopo il referto di Z43; poi la cura di r con il suo sigillo.
 4. TETTO-CAUSALE passo (2) e la cura (1) di MEM-HEBB-VERSO (la forma di proj), PENSATI INSIEME perche' toccano la stessa funzione, ma in commit separati, ciascuno col suo sigillo. L'idea da valutare allora: il taglio passo_max = 0.01*mediana(d0) (numero a mano, mediana globale, comanda sul 40-55% degli archi) sostituito dal limite causale c_s*dt_e dell'arco. DECISIONE DI LUCA, da prendere allora.
 IN SOSPESO, da scrivere tale e quale: la decisione (1) (proj = 0.5*(I_i+I_j)/Imed*(m_j-m_i).dir) va RICONFERMATA da Luca prima della sua cura, alla luce di due fatti emersi dopo: (a) mem_mot NON e' una velocita': rilassa verso grad_tw (:9130 su e2940b3c), quindi (m_j-m_i).dir e' circa la curvatura della torsione lungo l'arco, non un moto relativo (le simmetrie restano valide); (b) la forma decisa satura al taglio sul 55% degli archi e cambia la somma di Delta d0 da +6.7e3 a -9.2e4 (referto 2717308).
 Osservazione del guardiano, da registrare: dentro memoria_hebbiana_moto nessun passo usa il tempo proprio (mem_mot si aggiorna per passo senza dt, il taglio su d0 non ha tempo, i tetti usano DT). Va nella voce TETTO-CAUSALE-TEMPO-COORDINATO.

PARTE 2: LA CURA (2), decisione di Luca del 2026-10-04, confermata dal referto 2717308 (il sito scarta il 97.3% dei contributi, scartati/applicati = 36.2): il sito della fase in memoria_hebbiana_moto (phi[ii] = (phi[ii] + shift) % _dphi(), :9531 su e2940b3c, censiscilo dall'AST) si SPEGNE con un FLAG PROPRIO. MEM_MOTO_TUTTO e MEM_MOTO restano come sono, e mem_mot continua ad aggiornarsi.
 - Il flag nuovo, ACCESO, riproduce il comportamento di oggi; SPENTO, il sito non scrive phi. Il default del modulo e il driver lo tengono SPENTO: e' la fisica decisa. Rispetta le regole del repo sui flag (registro dei flag, configurazione dichiarata, P5).
 - FASE-TRASCINAMENTO-3D resta aperta: la legge in 3D NON si scrive ora.
 - Task history PRIMA del codice, con LA STELLA POLARE.
I CRITERI DEL SIGILLO, gia' fissati in b7e5a89 e qui precisati:
 - braccio 0: prima + patch committata = blob nuovo;
 - flag ACCESO: stato identico AL BYTE al blob e2940b3c su 150 passi, scena del driver, seme 11, lockstep su TUTTI gli attributi di net;
 - flag SPENTO: al primo passo le differenze stanno SOLO in phi (il sito e' l'ultima scrittura di memoria_hebbiana_moto, che e' l'ultima voce del passo). Se al passo 1 differisce altro, FERMATI. Dal passo 2 in poi le differenze si propagano: riportane la crescita per attributo, senza giudicarla;
 - CASO CHE DEVE FALLIRE: col flag spento phi DEVE differire al passo 1. Se non differisce, lo spegnimento non spegne niente: FERMATI.
Commit separati, in ordine: programma, task history, codice e strumento del sigillo, corsa e referto, con i blob citati.

NON CHIUDERE IL TURNO A META': ti fermi solo con "FERMO: <motivo>". Chiudi con "PUSHATO: <hash>". STOP.

---

## CHE COSA MANCA, PRIMA CHE QUESTO LAVORO POSSA PARTIRE

*(Nessuna di queste righe interpreta il mandato: sono **cose da fare** che il mandato stesso
elenca, messe in ordine perche' alla ripresa non si debba ri-leggerlo per capire da dove
cominciare.)*

1. ### **il commit del PROGRAMMA** — il `TODO ALLA RIPRESA` di
   `doc/TASK_HISTORY/2026-10-04_mem-hebb-verso-misura.md` e i **collegamenti** nelle tre
   voci d'indice *(`Z43`, `MEM-HEBB-VERSO`, `TETTO-CAUSALE-TEMPO-COORDINATO`)*;
2. **l'`IN SOSPESO` scritto TALE E QUALE:** la decisione `(1)` va ### **RICONFERMATA da
   Luca** prima della sua cura, coi **due fatti emersi dopo**;
3. **l'osservazione del guardiano** nella voce `TETTO-CAUSALE-TEMPO-COORDINATO`;
4. **il task history del passo (2)**, con `LA STELLA POLARE`, **prima del codice**;
5. il **censimento dall'AST** del sito `:9531`;
6. il **flag nuovo**, col **registro dei flag**, il **`README`** *(cosa fa, il **DEFAULT**,
   se e' byte-inerte)* e la **configurazione dichiarata** *(`P5`)*;
7. lo **strumento del sigillo** coi **quattro criteri**, e il **caso che deve fallire**;
8. la **corsa** e il **referto**, coi **blob citati**.

### ⚠ **DUE COSE DEL MANDATO CHE VANNO LETTE DUE VOLTE**

1. ### **IL DEFAULT E' SPENTO, ED E' UN RIBALTAMENTO:** *«il default del modulo e il driver
   lo tengono SPENTO: e' la fisica decisa»*. ### **Quindi il flag ACCESO riproduce oggi, ma
   il default lo SPEGNE** — e il par.6 ② pretende che, ### **nello stesso commit**, si
   cerchino **TUTTI i punti che ottenevano il vecchio comportamento per OMISSIONE.**
2. ### **`FASE-TRASCINAMENTO-3D` RESTA APERTA:** *«la legge in 3D NON si scrive ora»*.
   ### **Spegnere non e' curare**, e la voce non si chiude.

### 📌 **E UNA COSA CHE QUESTO MANDATO CAMBIA RISPETTO A IERI, da non perdere**

Il referto `2717308` chiudeva dicendo che restava a Luca la **riconferma** della decisione
`(1)`. ### **Qui Luca la mette in SOSPESO ESPLICITO, con due fatti nuovi** — e il secondo
*(`(a)`: `mem_mot` **non e' una velocita'**, rilassa verso `grad_tw`, quindi
`(m_j - m_i).dir` e' **circa la curvatura della torsione lungo l'arco**)* ### **non era nel
mio referto: e' una lettura del guardiano, e va registrata come sua.**
