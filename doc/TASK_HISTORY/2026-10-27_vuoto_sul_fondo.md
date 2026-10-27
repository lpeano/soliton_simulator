# IL VUOTO SUL FONDO, SULLA CARTA *(la parte 2 del mandato dopo `15df5c63`)*

> **Il mandato:** ### **`(a)` lo SPETTRO del generatore del vuoto** *(la sua energia come in `energia_pesata.termini_di_h`, con lo zero simmetrico e con quello di oggi)* ### **sul toro a triangoli: dove sta il vuoto uniforme, dove sta il FONDO, com'e' fatto lo stato del fondo** *(quale `k`, quali fasi sulle estremita', uniforme in modulo o no)*; ### **`(b)` IL SEGNO: il vuoto uniforme e' il massimo per la FORMA, per lo zero o per il segno di `H`?** ### **Dal generatore; e che cosa cambierebbe per la materia;** ### **`(c)` SE esiste un vuoto sul fondo ammissibile** *(la stessa norma `V`, uniforme in modulo per estremita' come `VUOTO_PER_ESTREMITA`)*: ### **`(i)` la sua energia; `(ii)` la nascita `b1` con le regole `v1`-`v5` di `f7ee87a9` da QUEL vuoto; `(iii)` il solitone `S1` col vuoto del fondo** *(congelato e poi col tick intero, `N 1e6` `L 81`, `2000` tick, lo zero simmetrico; per pezzo e per regione: lo strumento del libro dei conti)*. ### **Le previsioni del guardiano:** ### **DEVE `(a)`: il vuoto uniforme e' un autostato;** ### **PUO' FALLIRE: e' l'autovalore MASSIMO;** ### **PUO' FALLIRE `(c-ii)`: dal fondo la nascita ha un `Delta H_tot` che il vuoto puo' assorbire;** ### **PUO' FALLIRE `(c-iii)`: col fondo e il tick intero il solitone vive oltre `1280` tick e il vuoto PRENDE energia dalla materia.** ### **Se il fondo non e' uniforme in modulo, mi fermo dopo `(b)`.** *([[PROGETTO-MASSA-COLLETTIVA]], [[ENERGIA-DEL-LEGAME]], [[LIBRO-DEI-CONTI]])*
> ### **Nessuna scelta sulle forme del vuoto** *(`D6f`)*: ### **si misura, non si sceglie.**

**LIVELLO:** una misura sulla carta, in tre passi *(`a`-`b`-`c-i`; poi `c-ii`; poi `c-iii`)*, ### **ognuno col suo script committato prima.**

## 0. LA STELLA POLARE

1. **`A14`:** ### **il vuoto nella fisica e' lo stato di energia MINIMA; qui si misura dove sta.** 2. **Il gradino:** ### **la lettura del guardiano** *(un vuoto al massimo puo' solo cedere: i due problemi insieme)*. 3. **Aggiunge un numero o una legge?** ### **No.** 4. **Tocca `rho`, `c_s` o il segno?** ### **Il segno si LEGGE, non si cambia.** 5. **Emergente o imposto?** ### **Si misura.**

## 1. CHE COSA CREDO PRIMA DI GUARDARE *(una derivazione sulla carta, da verificare dal codice)*, E CHE COSA NON SO

- ### **LA FORMA, letta da `energia_pesata.termini_di_h`** *(la materia a zero)*: ### **per nodo `-pi (nrm_phi - pu_phi)`, per arco `-pi (|f0|^2 + |f1|^2 - 2 Re f0* f1)/2`.** ### **Cioe' `H_vuoto = -pi [(I - P_u) + (I - P_s)]`,** ### **`P_u` il proiettore sugli stati UNIFORMI in ogni nodo** *(`nrm - pu = <phi|(I - P_u)|phi>`)*, ### **`P_s` quello sugli stati UGUALI ai due capi di ogni arco** *(`|f0 - f1|^2/2 = <phi|(I - P_s)|phi>`)*.
- ### **QUINDI CREDO:** ### **`H_vuoto <= 0`** *(meno `pi` per due complementi di proiettori, semidefiniti positivi)*; ### **il MASSIMO `0` e' raggiunto solo da uno stato uniforme in ogni nodo E uguale ai capi di ogni arco: su un grafo connesso, IL VUOTO UNIFORME.** ### **Il minimo `-2 pi` per unita' di norma, da uno stato ortogonale a tutti e due:** ### **ANTISIMMETRICO su ogni arco e a SOMMA NULLA in ogni nodo** *(un flusso senza divergenza)*, ### **degenere** *(la dimensione dei cicli del grafo)*. ### **UNIFORME IN MODULO: un flusso COSTANTE per ognuna delle tre direzioni del reticolo** *(ogni nodo ha un arco uscente e uno entrante per direzione)*: ### **le estremita' `+-c_d`, e la TORSIONE `pi` su ogni arco.**
- ### **IL SEGNO `(b)`:** ### **il vuoto uniforme e' il massimo per la FORMA** *(il `-pi` davanti a forme positive)*; ### **lo zero e' una costante** *(`+ 2 pi lambda` per unita' di norma: sposta tutto lo spettro, non l'ordine)*; ### **il segno GLOBALE di `H`** *(il verso del tempo: tutti i pezzi applicano `-s` volte la derivata della loro energia, `b04ec0d3`)* ### **lo porterebbe al fondo, e capovolgerebbe anche lo spettro della materia.**
- ### ⚠ **NON SO:** ### **se il fondo uniforme in modulo e' un autostato del TICK** *(credo di si': ogni pezzo e' una funzione di `P_u` o di `P_s`, e lo stato e' nel nucleo di tutti e due)*; ### **dove sta lo stato uniforme della MATERIA nel suo spettro** *(`e_K(0) = -4.71`)*; ### **e se la nascita e il solitone dal fondo sono possibili: `(c-ii)` e `(c-iii)` vengono dopo.**

## 2. LA PROGETTAZIONE DEL PASSO `a`-`b`-`c-i` *(lo script `csv/_vuoto_sul_fondo.py`)*

1. ### **LA MATRICE DEL GENERATORE, DAL CODICE:** ### **su tori a triangoli `L 6` e `L 12`** *(`scena_l2.scena_toro`, `2m = 216` e `864` estremita')*, ### **`H_ij` per polarizzazione di `E(phi) = sum per_nodo(..., "psi_h")`** *(la materia a zero)*, ### **sulle coppie di estremita' dello stesso nodo o dello stesso arco** *(il supporto della forma)*; ### **IL CONTROLLO: `E(phi)` del codice = `phi^+ H phi` su stati CASUALI** *(se la forma avesse termini fuori dal supporto, qui si vede)*.
2. ### **LO SPETTRO** *(`eigvalsh`)*: ### **il massimo, il minimo, le loro molteplicita'** *(entro `1e-9`)*; ### **il vuoto uniforme: il quoziente di Rayleigh e il residuo `||H phi - E phi||/||phi||`;** ### **IL FONDO UNIFORME IN MODULO costruito** *(il flusso costante per direzione)*: ### **il quoziente e il residuo;** ### **le sue fasi e la torsione.** ### **Per lo zero simmetrico lo spettro e' spostato di `+pi`** *(`2 pi lambda`, `lambda 1/2`)*.
3. ### **IL TICK:** ### **il tick del vuoto** *(la materia a zero, `cs` spento, `conv("simm")` e `"oggi"`)* ### **sul vuoto uniforme e sul fondo: il residuo da autostato e la fase per tick contro `-s (E/V + 2 pi lambda)`.**
4. ### **IL SEGNO `(b)`:** ### **lo spettro del termine di nodo e di quello d'arco SEPARATI** *(ognuno in `[-pi, 0]`)*; ### **lo spettro della MATERIA** *(`H_cam(psi)`, il vuoto a zero, `eps 0`, sulla stessa scena)* ### **e dove cade lo stato uniforme della materia** *(`_scomposizione_solitone.stato_uniforme`)*: ### **la sua posizione nello spettro e quella con il segno capovolto.**
5. ### **`(c-i)`:** ### **l'energia del fondo e dell'uniforme a `L 48`** *(dal codice, i due stati costruiti)*, ### **per unita' di norma e totale.**

| | il criterio | il tipo |
|---|---|---|
| `t` | ### **la matrice ridà l'energia del codice su `5` stati casuali entro `1e-12` relativo** | DEVE |
| `a` | ### **il vuoto uniforme e' un autostato del generatore: il residuo `<= 1e-12`** *(la previsione del guardiano)* | DEVE |
| `m` | ### **il vuoto uniforme e' l'autovalore MASSIMO** *(entro `1e-9`)* | PUO' FALLIRE |
| `f` | ### **ESISTE un fondo uniforme in modulo: il flusso costante per direzione ha il quoziente = il minimo dello spettro e residuo `<= 1e-12`** *(se NO: mi fermo dopo `(b)`)* | PUO' FALLIRE |

- ### **LE LETTURE:** ### **le molteplicita'; la torsione del fondo; il tick sui due stati; il segno** *(i due termini separati, la materia)*; ### **`(c-i)` a `L 48`.**

### **Mi FERMO** ### **se `t` o `a` fallisce, o se `f` fallisce** *(come dice il mandato)*.

## 3. TODO

1. questo task history, da solo; 2. `csv/_vuoto_sul_fondo.py`, committato prima della corsa; 3. la corsa e il referto; 4. se `f` passa: `(c-ii)`, la nascita dal fondo *(con lo strumento di `f7ee87a9`, `csv/_divisione_vuoto.py`; un'annotazione qui prima)*; 5. `(c-iii)`, il solitone dal fondo *(lo strumento del libro dei conti)*.
