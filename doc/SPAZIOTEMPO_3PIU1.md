# LO SPAZIO-TEMPO 3+1: LE IDEE, I FATTI, LE PROVE DA FARE

> ### 💡 **La discussione di Luca col guardiano del `2026-10-23`, `18:37`-`19:39`** *([[SPAZIOTEMPO-3PIU1]], collegata a [[PIANO-2D-3D]], [[DECISIONE-SOLO-TRIANGOLI]], [[DOMANDA-D9-GEOMETRIA]])*.
> ### ⛔ **NESSUNA RIGA E' UNA DECISIONE.** ### **Ogni riga ha un'etichetta:** ### **`[FATTO MATEMATICO]`, `[FATTO, dal codice]`, `[IDEA DI LUCA]`, `[VALUTAZIONE DEL GUARDIANO]`, `[PROVA DA
> FARE]`, `[MISURATO, commit]`.** ### **Dove il mandato e il repo non coincidono, ⚠ e il testo del repo.** ### **Il piano corrente resta `doc/PIANO_2D_3D.md`.**

## A. LO SPAZIO-TEMPO DEL SIMULATORE

- **`[FATTO, dal codice e dalle decisioni]`** ### **Il tempo e' la successione dei tick** *(tempo coordinato)* ### **e ogni nodo vive il suo tempo proprio `dtau cs`.** ### **I triangoli sono `2+1`, la FCC
  sara' `3+1`:** ### **le quattro dimensioni di spazio-tempo arrivano da se', non vanno aggiunte.** ### **Le fonti:** ### **`a9b764a9`** *(`2026-10-02`, `23:59`)*: «il tick globale e' solo la coordinata»;
  ### **la voce `TEMPO-PROPRIO-LOCALE`** *(«la MONETA ... avanza nel TEMPO PROPRIO del nodo: `d tau_k = r_k dt`»)*; ### **`flussi_parziali.py`: l'angolo per nodo e' `dtau x cs`.**
- **`[MISURATO, 8781162c, cbcb99c7]`** ### **Nelle misure della forza lo SPAZIO era PIATTO** *(griglia regolare, toro piatto: una REGOLA DI VICINANZA, condizioni al contorno periodiche, non una
  figura)* ### **e il TEMPO curvo per costruzione** *(`cs(x)` imposto a mano: il ritmo degli orologi che cambia da un punto all'altro e' la parte tempo-tempo della metrica, quella della gravita'
  debole)*; ### **nessuna retroazione della materia** *(il canale di `cs` e' chiuso)*.
- **`[PROVA DA FARE]`** ### **Se la metrica efficace** *(l'orologio E la velocita' per tick: `s` entra in entrambi)* ### **ha la forma giusta: una strada per il fattore `a/a_RG(v_max)` `1.63`-`1.68`**
  *(`cbcb99c7`: non viene dalla velocita' usata in `a_RG`)*.

## B. IL 2D E IL 3D *(il resto e' in `doc/PIANO_2D_3D.md`, sezioni `A` e `B`)*

- **`[FATTO MATEMATICO]`** ### **La propagazione netta di un lampo** *(il principio di Huygens forte)* ### **vale solo nelle dimensioni spaziali dispari:** ### **in 2D un impulso lascia una coda nel continuo,
  in 3D no.**
- **`[FATTO]`** ### **Nel modello la luce NON e' ancora definita** *(la voce `LUCE-VINCOLO-LAMPI-GAMMA`, `FRONTE`, `AGENDA`)*: ### **la coda in 2D NON e' una proprieta' misurata del simulatore** ### **-- ERRORE DEL
  GUARDIANO `n.54`: l'aveva scritta come se lo fosse.**

## C. LA FCC E LE QUATTRO DIREZIONI

- **`[FATTO MATEMATICO]`** ### **La FCC e' il reticolo `A3`** *(il nome della teoria dei reticoli e dei gruppi di radici: ⚠ NON l'assioma `A3` di `doc/ASSIOMI.md`, che e' un'altra cosa)*: ### **i punti di `Z^4` a somma nulla.** ### **I `12` vicini sono `e_i - e_j`, `i != j` in `{1, 2, 3, 4}`** *(`4 x 3 = 12`)*. ### **Le quattro direzioni
  sono quelle dal centro di un tetraedro ai vertici; la somma nulla le lega, e restano TRE dimensioni indipendenti.**
- **`[FATTO MATEMATICO]`** ### **Fissato `i`, i tre vettori `e_i - e_j` formano un triedro che genera lo spazio:** ### **i `12` vicini sono QUATTRO TRIEDRI, uno per direzione del tetraedro,
  equivalenti per la simmetria del tetraedro.**
- **`[IDEA DI LUCA]`** ### **Tre livelli di torsione sui tre assi `x`, `y`, `z`, e uno che rappresenta il tempo** *(`12 / 3 = 4`)*.
- **`[VALUTAZIONE DEL GUARDIANO, non decisione]`** ### **Nella forma «uno dei quattro triedri e' il tempo» l'idea rompe la simmetria del tetraedro** *(i quattro sono equivalenti)* ### **e non
  distingue il tempo dallo spazio** *(ogni triedro genera gia' `x`, `y`, `z`; il tempo ha segno opposto nell'intervallo)*; ### **nella forma algebrica** *(sezione `D`)* ### **«uno piu' tre» e'
  matematica esatta.** ### **Quale forma tenere e' una decisione APERTA di Luca.**

## D. LA TORSIONE E LA FIRMA DI MINKOWSKI

- **`[FATTO MATEMATICO]`** ### **Ogni matrice `2 x 2` si scrive con `I` e le tre di Pauli: uno piu' tre.** ### **Per `X = t I + x sigma_x + y sigma_y + z sigma_z` vale `det X = t^2 - x^2 - y^2 - z^2`,
  l'intervallo di Minkowski;** ### **le trasformazioni che lo conservano, `SL(2, C)`, sono le trasformazioni di Lorentz** *(in copertura doppia, come `SU(2)` per le rotazioni)*. ### **Il tempo e'
  la componente identita', lo spazio le tre di Pauli, senza direzioni scelte a mano.**
- **`[FATTO, dal codice]`** ### **Il trasporto sull'arco `U = cos(chi/2) I - i sin(chi/2) m.sigma`** *(`doc/BUSSOLA_TECNICA_dev-spinoriale.md`, `§4.0`, l'ERA `1`)* ### **ha la divisione scalare +
  vettore, ma e' UNITARIO: descrive le ROTAZIONI** *(`S^3`, euclideo)*; ### **la firma di Minkowski viene dalle matrici HERMITIANE, cioe' dai BOOST, che oggi nel modello NON ci sono.**
  ⚠ *(nell'ERA `2` la `U` dell'arco non si costruisce da `chi` e `m`: `primo_ordine/motore.py` `Geometria` accetta ogni `U` `2 x 2` e asserisce solo `U^dagger U = I`; la scena di
  riferimento ha `U = I`, alcune prove una `U` casuale di `SU(2)`, `corrente.py` di `U(2)`. La forma `cos a I - i sin a sigma.n` nell'era `2` e' quella della MONETA, `motore._moneta_spin`.
  La conclusione non cambia: NESSUN elemento non unitario, nessun boost.)*
- **`[PROVA DA FARE]`** ### **LA PROVA DI LORENTZ:** ### **se la camminata fa emergere i boost** *(la parte che mescola tempo e spazio)* ### **oltre alle rotazioni: un oggetto in moto deve vedere orologi
  rallentati e lunghezze contratte nella misura giusta**, ### **come in D'Ariano-Perinotti, dove la relativita' emerge approssimata a bassa energia.** *(Collegata: la voce `LORENTZ-MATERIA-INTERFERENZA`.)*

## E. LA MITOSI E LE TRE DIMENSIONI

- **`[IDEA DI LUCA]`** ### **La torsione costruisce il 3D:** ### **nell'era `1` la soglia della mitosi era sulla torsione** *(anche nella variante a doppia copertura `4 pi`, `TORS_4PI`)*, ### **e con
  la plasticita' dinamica** *(`PLAST_DIN`)* ### **la torsione sciolta alla nascita generava volume.**
  ⚠ *(nel repo «genera volume» e' un'IPOTESI, mai un risultato: `fork-su2:soliton_simulator.py`, il commento di `PLAST_MIT`, «Ipotesi: la suddivisione GENERA spazio invece di comprimerlo ... Da
  MISURARE, non imporre», e la tabella di `INTERPRETAZIONE_campagna_spinore_vivo_plastdin.md` resta a «?»; il documento di fondazione dice il contrario, «La mitosi non altera la geometria: ne
  cambia la risoluzione». E `TORS_4PI` ha il commento «default off» col valore `True`: `doc/CENSIMENTO_intenzioni.md`, `A2`.)*
- **`[VALUTAZIONE DEL GUARDIANO]`** ### **A favore, un argomento di principio:** ### **la torsione vive in `SU(2)`, copertura doppia delle rotazioni del 3D; le reti di spin `SU(2)` della gravita'
  quantistica a loop descrivono geometrie tridimensionali.**
- **`[PROVA DA FARE]`** ### **Una rete che cresca per mitosi nell'era `2` SENZA POSIZIONI**, ### **con la dimensione misurata dalle SOLE relazioni uguale a `3`** *(per esempio la crescita del numero dei
  nodi con la distanza, o la dimensione spettrale)*, ### **circa `12` vicini, triangoli e tetraedri chiusi.** ### **Oggi l'era `2` non ha la mitosi** *(`DEC-D7-DIVISIONE` aspetta `DEC-FC-COESIONE`)*.
- **`[IDEA DI LUCA]`** ### **L'ipersfera `x^2 + y^2 + z^2 + w^2 = R^2` come lettura del tempo cosmico:** ### **lo spazio che cresce con la mitosi** *(`D9`)* ### **come freccia del tempo, il tick come
  tempo locale.** ### **Non tradotta nel codice.** ⚠ *(nel repo NON ce n'e' traccia: nessuna «ipersfera», nessun `x^2 + y^2 + z^2 + w^2`, in nessuno dei `9` rami. I vicini: `FASCE-TAU` in
  `doc/STATO_RUN.md`, «l'analogo delle ipersuperfici a tempo cosmico costante di Friedmann», Luca `2026-09-22`; `doc/FONDAZIONE_3+1.md`, la quarta coordinata del tempo proprio accumulato;
  la voce `SPAZIO-TRIANGOLAZIONE-SENZA-POSIZIONI`, «la sfera che serve puo' stare nel BERSAGLIO, non nello spazio».)*

## F. LA VERIFICA DEL `3.08` DELL'ERA `1` *(sola lettura; la misura NON si rifa')*

### **LA FONTE TROVATA:** ### **`doc/leggi_del_sistema_solitoni .docx`** *(uno spazio prima di `.docx`)*, ### **«Le leggi fisiche del sistema dei solitoni relazionali — Documento di fondazione», datato
nel testo «4 luglio 2026».** ### **Identico nei rami `fork-su2`, `dev-spinoriale`, nel tag `era-1-secondo-ordine` e in `primo-ordine`:** ### **blob git `c1070f92` / sha1-BYTE `b7a81473`** *(le due
convenzioni: git `hash-object` e i byte grezzi)*. ### **Entrato in `8a3ab3e0`** *(`2026-08-28`, «Add documentation file for soliton system», col nome senza spazio)*, ### **rinominato e allargato in
`397b82dc`** *(stessa data)*; ### **il repo comincia il `2026-08-28`: il `4 luglio` sta solo nel testo.** ### ⚠ **Un `docx` non si cerca con `git grep`: per questo una ricerca di `3.08` non lo trova.**

1. **IL METODO** ### **`[FATTO, dal documento]`:** ### **«dimensione spettrale del random walk sulla rete `d_s = 3,08 +- 0,10`»** *(la Legge I, «Relazionalita' dello spazio»; e la tabella delle costanti:
   «`d_s` | `3,08 +- 0,10` | dimensione spettrale dello spazio relazionale»)*. ### **Nello stesso paragrafo: le geodetiche di grafo contro le distanze euclidee `r = 0,998`, e la ricostruzione delle
   posizioni dalle lunghezze relazionali `l_ij = -lambda ln|A_ij|` con «gap spettrale di fattore 23 dopo esattamente tre direzioni».** ### **La rete e' la matrice `A_ij = exp(-d_ij/lambda) cos(phi_i -
   phi_j)`, `lambda = 0,8`.** ### **LO STRUMENTO NON C'E' NEL REPO:** ### **nessun codice calcola `d_s`** *(cercati «spettral», «random walk», «return prob», «heat kernel» nel simulatore di allora e
   nei `.py` e `.md` di `fork-su2`)*.
2. **LE POSIZIONI IN 3D: SI'.** ### **`[FATTO, dal codice]`:** ### **la rete era seminata in una PALLA 3D** *(`semina`: `self.pos = np.vstack([self.pos, p])`, `p` uniforme in una palla)*, ### **gli archi per
   RAGGIO in 3D** *(`_allaccia`: `cKDTree(self.pos)`, `sparse_distance_matrix`)*, ### **i pesi `exp(-d/lambda)` della distanza 3D** ### **e i figli della mitosi nel punto medio** *(`pos_figlio = 0.5 (pos[a] +
   pos[b])`; al tag `(1 - FRAZ_NASCITA) pos[a] + FRAZ_NASCITA pos[b]`, `FRAZ_NASCITA = 0.5`)*. ### **Il documento stesso:** ### **«Le diciotto leggi precedenti sono verificate con posizioni FISSE».**
   ### **`[VALUTAZIONE DEL GUARDIANO]` LA DIMENSIONE E' EREDITATA DALL'IMMERSIONE, NON EMERSA:** ### **`d_s` era misurata «sul solo grafo», ma il grafo era un grafo geometrico casuale costruito da
   posizioni 3D fisse.** ### **Il repo lo ammette:** ### **`era-1-secondo-ordine:doc/ASSIOMI.md`, «la DIMENSIONE 3 e' FISICAMENTE RILEVANTE: `_allaccia` cerca per RAGGIO»; `doc/RAMIFICAZIONI.md`, `Z47`,
   «`pos` e' l'unico SFONDO rimasto».**
3. **RITRATTATA? NO, NON ESPLICITAMENTE; SUPERATA, SI'.** ### **Nessuna riga «RITRATTAZIONE» nomina `d_s` o la Legge I:** ### **le ritrattazioni del documento riguardano altro** *(il pozzo misurato sul
   dito; il rapporto `3,06` «non e' fidato, e la coincidenza era tautologica» -- attenzione all'omonimo `3,06`/`3,08`; la dilatazione del tempo proprio)*. ### **Superata nell'era `2`** *(`RELAZIONE_PER_CLAUDE.md`)*:
   ### **la dimensione spettrale DIPENDE DALLA TAGLIA** *(«cubico `L = 12` `3.090`; casuale `n = 120` `2.363`; casuale `n = 2000` `3.927`»; «la stessa (i) passa da `2.578` a `n = 1728` a `2.92` a `n = 4000`»)*:
   ### **un `d_s` senza la taglia non e' un dato.**
4. **IL VALORE E IL BLOB:** ### **`d_s = 3,08 +- 0,10`; il documento blob git `c1070f92`, sha1-BYTE `b7a81473`.**

## G. LE PROVE PER IL 3+1, IN ORDINE *(nessuna e' fatta)*

1. **`[PROVA DA FARE]`** ### **le proprieta' locali del passo sopravvivono al 3D** *(lo zero simmetrico, il segno su un reticolo non bipartito, la violazione `O(s^2)`)*;
2. **`[PROVA DA FARE]`** ### **la materia produce `cs` con la legge giusta** *(in 3D `1/r`)*;
3. **`[PROVA DA FARE]`** ### **la prova di Lorentz** *(i boost)*;
4. **`[PROVA DA FARE]`** ### **la mitosi costruisce un 3D SENZA POSIZIONI** *(e il `3.08` dell'era `1` NON lo prova: sezione `F`)*.
