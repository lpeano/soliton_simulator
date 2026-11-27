# [M-GM] IL W DI WEYL SUL MODELLO INTERO: A DINAMICO (LA FASE SUGLI ARCHI) CON LA GRAVITA' ACCESA — DA ESEGUIRE SOLO AL «VIA» DI LUCA

CORRETTO il 2026-11-27 22:20 (ERRORE DEL GUARDIANO n.261): Theta sommato su un giro chiuso è identicamente zero (telescopico: ogni nodo entra una volta col più e una col meno); Theta NON è un'olonomia del tempo e la mitosi non scatta da un giro. Il W con la scala solo nel tempo (chi scalare) è integrabile: NESSUN secondo effetto di orologio, l'obiezione di Einstein a Weyl non si applica; e da questo W NON viene nessun gravitomagnetismo (per g_0i serve un pezzo misto tempo-spazio che il modello non ha). P4 e P5 della versione precedente sono TOLTE. Restano P1-P3: l'elettromagnetismo (A dinamico, sorgente la corrente di psi) sopra il modello con la gravità accesa.

Categoria: ATTESA DI LUCA (scritto il 2026-11-27 22:00). Diventa DECISIONE DI LUCA (hh:mm) con l'ora del «via», che Luca dà in chat o con una lettera. Fino ad allora: non si esegue, non si scrive codice.

PRIMA: git log --all --grep "[M-GM" ; se un pezzo è già fatto, non rifarlo.

PREMESSE
- Il modello intero resta acceso in tutto: chi e N = exp(-kappa chi), F0, il vuoto phi, toro, g_e = 0, la composizione palindroma. L'unico interruttore nuovo è A: la parte di fase di U diventa dinamica. R (la parte di spin di U) resta fissa in questo mandato.
- L'idea (stella polare H10): un solo oggetto per collegamento, W = exp(-kappa chi) sul collegamento temporale (modulo: la gravità, non si compensa, grande scala) e exp(iA) sull'arco spaziale (fase: si compensa, piccola scala). La sorgente di A è la CORRENTE DI psi sugli archi (J, la stessa del vento), con una costante propria e_A (da scrivere nella carta) e il segno dell'elettromagnetismo: correnti parallele si attraggono, cariche uguali (stesso giro di fase) si respingono. E' la forza di U, non la gravità: la gravità resta chi.
- Il W ha la scala (exp(-kappa chi), chi scalare) solo nel tempo: integrabile, nessun secondo effetto di orologio. Un oggetto che fa un giro torna con lo stesso omega: cambia il tempo trascorso, non il ritmo. L'obiezione di Einstein a Weyl non si applica. Theta non entra in questo mandato.
- Ramo nuovo «u-dinamica» da lapse-u. Nucleo intatto: se la dinamica di A richiede un pezzo nella tabella delle leggi (CAMM-U), è la stessa via di CAMM-MONETA-SPIN: una legge in leggi.yaml con il suo termine, il presidio del nucleo, e DECISIONE DI LUCA per il tocco al nucleo. Carta prima del codice; stati ogni 250; coda_m1446.py dalla cartella nuova; tetto 10, freno 4 GB.

PEZZO 0, A COSTO ZERO (si fa PRIMA, sugli stati che ci sono, con chi acceso): sui due triangoli «tre sfasate» (destro e sinistro) e sul triangolo in fase: il numero di vortice (il giro della fase di psi attorno al centro, in unità di 2 pi), la corrente circolante J_theta per anello, Theta sommato sul giro attorno al centro. Se nessun triangolo ha giro di fase intero, il resto del mandato si ferma e si dichiara.

LE SCELTE (da confermare al «via»)
- S1. La dinamica di A: salto di rana come chi_tick (E avanza con il rotore del flusso attraverso i triangoli meno la sorgente; A avanza con E), mezzo passo prima e mezzo dopo CAMM-SPOSTAMENTO nel palindromo; Gauss resta il vincolo, verificato ogni OGNI_GAUSS. c_A = la c della materia (0,085 nodi/tick) dichiarata; nessun termine di massa.
- S2. La sorgente: la corrente di psi sugli archi (J), costante e_A, segno dell'elettromagnetismo. Scritta nella carta con la sua forma esatta PRIMA del codice.
- S3. Il ritorno su chi: la sorgente u include 1/2 (E^2 + B^2) sul reticolo.
- S4. Casi noti: (K1) vuoto puro: A resta zero al bit per 1000 tick; (K2) Gauss conservato a 1e-9; (K3) H + H_A conservata entro la deriva di fondo su 6000 tick; (K4) kappa_A = 0 e A = 0 -> il tick di oggi al bit (la tenuta del giro 3 di [M0414]).

LE PROVE (ciascuna una corsa <= 6000 tick, in quest'ordine; ogni corsa si ferma se la precedente scarta l'idea)
- P1 la quantizzazione: il triangolo sfasato destro, dal suo punto fisso, con A acceso: il flusso di B attraverso il centro va a 2 pi n con n intero (entro il 5%) e l'olonomia di exp(iA) lungo i tre lati lo misura. Se il flusso non è quantizzato: FERMO, l'oggetto non è un vortice.
- P2 i due segni: destro-destro e destro-sinistro a 40 nodi: la forza (a dal fit di d(k)) opposta in segno fra le due coppie, oltre il controllo con A spento.
- P3 Eötvös con gli aggregati: destro+sinistro (carica totale zero) accanto a un oggetto M, nel pozzo DIPINTO (seno): stessa accelerazione all'1% sulla prima finestra. Se fallisce: van der Waals gravitazionale, l'idea è sbagliata rispetto al mondo, si dichiara.

CRITERI: le soglie sono di Luca (5% su P1, 1% su P3) e si confermano al «via»; nessun verdetto senza i controlli con A spento; ogni numero con il k e la finestra.

PREVISIONI DEL GUARDIANO (scritte il 27/11 alle 22:00)
- Pezzo 0: le tre sfasate hanno giro di fase n = +-1 (70%).
- P1 passa (55%): la saturazione può rompere il giro di fase al centro.
- P2 passa (75%). P3 passa (70%).

FINE: commit, push dopo ogni pezzo. Poi FERMO.
