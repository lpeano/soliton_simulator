# IL PROGETTO DELLA DIVISIONE DEL VUOTO *(la parte 2 del mandato del 2026-10-26, 08:57)*

> **Il mandato:** di Luca, `2026-10-26` *([[PROGETTO-MITOSI]], [[CONTO-DEL-VUOTO]], [[D-BILANCIO-NASCITA]])*: ### **una sezione nuova di `doc/PROGETTO_MITOSI.md`, NIENTE scelte;** ### **i conti sulla carta con lo strumento di `C3`** *(`csv/_conto_del_vuoto.py`, importato)*: ### **lo script `csv/_divisione_vuoto.py`, il referto `doc/referti_l2/divisione_vuoto.{txt,jsonl}`.**
> ### **IL FATTO** *(`d999cca7`)*: ### **con `D7` anche per `phi` la nascita libera `8.548`** *(il vuoto `-8.483`)*; ### **il `-8.48` viene dalla regola di trasporto di `phi`, non dalla mitosi in se'.**

**LIVELLO:** un documento di progetto e un conto sulla carta.

## 0. LA STELLA POLARE

1. **`A14`:** ### **e' la domanda:** ### **una regola con `V` conservata e `Delta H_tot = 0`?** 2. **Il gradino:** ### **il trasporto di `phi` alla nascita.** 3. **Aggiunge un numero o una legge?** ### **No: descrive e misura regole possibili, nessuna scelta.** 4. **Tocca `rho`, `c_s` o il segno?** ### **Misura `Delta Lambda` e quindi `Delta cs`.** 5. **Emergente o imposto?** ### **Le regole sono candidate; la scelta e' di Luca.**

## 1. IL RAGIONAMENTO PRELIMINARE, DALLA FORMA *(prima dei numeri)*

- ### **`(a)` PERCHE' IL VUOTO UNIFORME E' IL MASSIMO:** ### **la parte del vuoto di `H_tot`** *(`energia_pesata.termini_di_h`)* ### **e' `-OMEGA_H [somma_nodi (|phi|^2 - |S phi|^2/d) + somma_archi |phi_0 - phi_1|^2/2] = -pi <phi|(I - P_u) + P_-|phi>`;** ### **`(I - P_u)` e `P_-` sono PROIETTORI, quindi la forma fra parentesi e' `>= 0`, e col segno `-pi` la parte del vuoto e' `<= 0`;** ### **vale `0` esattamente quando `phi` e' uniforme su ogni nodo** *(`P_u phi = phi`)* ### **e uguale ai due capi di ogni arco** *(`P_- phi = 0`)*: ### **cioe' il vuoto UNIFORME PER ESTREMITA', a qualunque ampiezza.** ### **QUINDI ogni regola che perturba il vuoto uniforme ne ABBASSA la parte quadratica:** ### **o la regola lascia il vuoto uniforme per estremita', o l'energia va altrove.**
- ### ⭐ **L'ALTROVE CHE C'E': IL LEGAME `N`.** ### **`N = rho ln(rho/(rho + Lambda))` ha `dN/dLambda = -rho/(rho + Lambda) < 0`:** ### **ABBASSARE `Lambda` dove c'e' materia ALZA `H_tot`.** ### **Quindi una regola con `V` conservata puo' pagare SOLO attraverso `N`** *(la parte quadratica non puo' salire sopra `0`)*: ### **diluendo il vuoto sotto la materia.** ### **Lo misuro, non lo assumo.**

## 2. LE REGOLE DI TRASPORTO DI `phi` ALLA NASCITA `(b1)` *(DICHIARATE QUI; `psi` resta come in `C3`: `D7` col padre `i`)*

| | la regola | `V` | locale? |
|---|---|---|---|
| `(v1)` | ### **`D7` anche per `phi`** *(la regola di `C3`, misurata)* | conservata | si' |
| `(v2)` | ### **le estremita' NUOVE al valore uniforme `VUOTO_PER_ESTREMITA`; il padre NON dimezzato** *(il vuoto resta uniforme per estremita')* | ### **CRESCE di `6`** *(contro `DEC-QC-CONSERVATA`: lo dico)* | si' |
| `(v3)` | ### **come `(v2)`, poi TUTTO il vuoto del toro moltiplicato per `sqrt(V/(V + 6))`** *(uniforme ovunque)* | conservata | ### **NO: ogni estremita' del toro cambia** |
| `(v4)` | ### **il vuoto dei nodi della mossa e dei loro vicini a un passo** *(`n, i, j, k, l`)* ### **ridistribuito UNIFORME fra le loro estremita'** *(`24` prima, `30` dopo: il valore `sqrt(24/30)`)* | conservata | si' *(un'isometria locale)* |
| `(v5)` | ### **il MASSIMO della parte quadratica del vuoto sulle estremita' di `S`** *(i nodi della mossa e i vicini a un passo, il resto fisso)* ### **alla norma conservata** *(l'estremo esatto di `C3`, `estremi_sfera`)* | conservata | si' |

- ### **PER CIASCUNA:** ### **`Delta H_vuoto`, `Delta H_tot`** *(materia, vuoto, legame)*, ### **`V`, `Lambda` per estremita' sui nodi `n, i, j, k, l`, e `Delta cs` per nodo e per estremita'** *(`Lambda_c/Lambda_6` in `0.1, 1, 10`)*; ### **e la rotazione di `C3` sul cerchio massimo** *(con `N` incluso)* ### **che porterebbe `Delta H_tot` a `0`, se esiste** *(`conto` di `_conto_del_vuoto`, applicato alla regola)*.
- ### **IL FLIP:** ### **nessuna estremita' nasce: il trasporto di `phi` e' la permutazione di `C3`, e TUTTE le `(v)` coincidono con `(v1)`** *(lo script lo verifica)*.
- ### **`(c)` LA DOMANDA DI FONDO:** ### **esiste una `(v)` con `V` conservata e `Delta H_tot = 0` per la nascita?** ### **Se si', `Delta cs`** *(il legame tempo-spazio contro `gamma = 1`, sezione `3(d)`)*; ### **se no, sulla famiglia provata.**
- ### **`(d)` L'ALBERO:** ### **`D6f`** *(`DEC-D6F-FORME-VUOTO`, presa)* ### **e `DEC-QC-CONSERVATA`** *(le norme esatte, `H_tot` al secondo ordine)*: ### **nel documento.**

## 3. I CRITERI

| | il criterio | il tipo |
|---|---|---|
| `1` | ### **`(v1)` ridà i numeri di `d999cca7` AL BIT** *(`Delta H_tot`, le tre parti, `M`, `V`, a `L 24` e `36`, letti dal jsonl di `C3`)* | DEVE |
| `2` | ### **il flip: `(v2)`, `(v3)`, `(v4)` coincidono con `(v1)` AL BIT; `(v5)` entro `1e-12`** *(l'estremo della sfera e' un conto numerico)* | DEVE |
| `3` | ### **le norme: `V` conservata entro `1e-14` relativo per `(v1)`, `(v3)`, `(v4)`, `(v5)`; `(v2)` cresce di `6` esatto** | DEVE |
| `4` | ### **esiste una `(v)` con `V` conservata e `|Delta H_tot| < 1e-10`** *(con la rotazione di `C3`, se serve)* | PUO' FALLIRE |

### **Mi FERMO** ### **se `1`, `2` o `3` fallisce.**

## 3-bis. ANNOTAZIONE, PRIMA DEL COMMIT DELLO SCRIPT *(una prova di costruzione a `L 6`, NON il referto)*

- ### **I NUMERI GIA' VISTI** *(la nascita, `L 6`)*: ### **`(v1)` `-8.548`; `(v2)` `-0.144`** *(`V` `216 -> 222`; il legame `-0.079`)*; ### **`(v3)` `-0.0466`** *(il legame `+0.018`: la diluizione sotto la materia PAGA, come previsto dalla forma, ma non abbastanza contro la materia `-0.065`)*; ### **`(v4)` `-0.301`; `(v5)` `-0.233`.** ### **Il flip: le cinque coincidono** *(`-0.2603`)*. ### **Le soglie del §3 restano.**

## 4. TODO

1. questo task history, da solo; 2. lo script, committato prima della corsa; 3. la corsa; 4. il referto; 5. la sezione di `PROGETTO_MITOSI`, la relazione, l'indice.

## 5. IL RISULTATO *(dopo `aac33f2f`)*

### **IL REFERTO:** `doc/referti_l2/divisione_vuoto.{txt,jsonl}` *(`csv/_divisione_vuoto.py` al commit `aac33f2f`; il task history `273cf8bc`)*. ### **`3/4`, nessun DEVE fallito; la PUO' FALLIRE `4` FALLISCE.**

| la regola | `Delta H_tot` *(`L 36`)* | materia | vuoto | legame | `V` | `Lambda` per estremita' su `n, i, k` |
|---|---|---|---|---|---|---|
| `(v1)` `D7` anche per `phi` | `-8.548214` | `-0.064801` | `-8.483412` | `~1e-13` | conservata | `0.75`, `0.50`, `0.857` |
| `(v2)` le nuove uniformi | `-0.143587` | `-0.064801` | `0` | `-0.078786` | ### **`+6`** | `1`, `1`, `1` |
| `(v3)` la diluizione globale | `-0.045264` *(`-0.045311` a `L 24`)* | `-0.064801` | `0` | ### **`+0.019537`** | conservata | `0.99923` ovunque |
| `(v4)` uniforme su `S` | `-0.300804` | `-0.064801` | `-0.245105` | `+0.009102` | conservata | `0.8` su `S` |
| `(v5)` il massimo su `S` | `-0.233405` | `-0.064801` | `-0.177546` | `+0.008942` | conservata | `0.697`, `0.808`, `0.823` |

- ### **`(v1)` RIDA' `d999cca7` AL BIT** *(il DEVE `1`)*; ### **il flip: le cinque regole COINCIDONO** *(`-0.260303`, tutto materia: nessuna estremita' nasce; il DEVE `2`)*; ### **le norme come dichiarato** *(il DEVE `3`)*.
- ### ⭐ **IL LEGAME PAGA, COME PREVISTO DALLA FORMA, MA NON BASTA:** ### **`(v3)` e' la migliore** *(`-0.0453`)*: ### **la diluizione del vuoto sotto la materia ALZA `N` di `+0.0195`,** ### **contro la materia `-0.0648` che nessuna regola di `phi` tocca** *(e' `D7` su `psi`)*. ### **E il guadagno del legame NON svanisce con `L`:** ### **diluire `6` di vuoto su tutto il toro alza `N` di circa `6 rho/(rho + Lambda) = 0.098` in tutto, a ogni `L`** *(il resto e' il `-0.079` di `(v2)`)*.
- ### **NESSUNA ROTAZIONE di `C3` porta il conto a `0`** *(per nessuna regola: il verso, come in `C3`)*.
- ### **`cs`** *(`Lambda_c/Lambda_6 = 1`)*: ### **`(v1)` `-33%` al nodo nuovo e al padre** *(per nodo e per estremita' al padre)*; ### **`(v3)` per estremita' `-0.04%` ovunque, per nodo `-20%` al nodo nuovo e `+7.7%` ai nodi a `7`** *(e' il grado)*; ### **`(v4)` per estremita' `-11%` su tutto `S`.**

### **La sezione `3(f)` di `doc/PROGETTO_MITOSI.md` porta la lettura.**
