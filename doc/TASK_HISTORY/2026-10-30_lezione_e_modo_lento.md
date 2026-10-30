# 2026-10-30 — LA LEZIONE GENERALE DELLE BANDE PIATTE E IL MODO LENTO A `r 1.5247`, CON LE CONSERVAZIONI NEL DECADIMENTO *(UNA DIAGNOSI IN `csv/`, NESSUNA MODIFICA AL NUCLEO; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; i mandati di Luca delle `09:09` e delle `09:16`)*

> **LA CODA** *(`PRECEDENZA-IN-CODA`, l'ordine registrato)*: `08:52` *(la regola dei tre incroci: tre punti)* -> **`09:09`** *(niente taratura dei pesi; la lezione; una sola misura)* -> **`09:16`** *(il chiarimento: vale `09:09`; delle `08:52` solo il punto `1`, che e' il punto `2` delle `09:09`; i punti `2` e `3` delle `08:52` in lista d'attesa; l'aggiunta `2bis`)*.
> **Che cosa era gia' fatto delle `08:52`:** **solo il task history** *(`doc/TASK_HISTORY/2026-10-30_tre_incroci.md`, `085ffb27`)*. **Nessuno script, nessuna corsa:** la corsa lunga a `r 0.69` **non e' partita**, non c'e' niente da fermare. Quel file resta come premesse *(le sue sezioni `1` valgono anche qui)*, ed e' annotato come superato.
> **LA DECISIONE DI LUCA DELLE `09:09`:** **non si tarano i pesi del nodo e dell'arco per stabilizzare `S1`** *(dipenderebbe da `mu`, dalla forma, da `N`: una taratura)*; **la strada (B) esce dal menu come cura, resta come diagnosi.**

## 1. LE PREMESSE DAL CODICE

### Gia' scritte e committate in `085ffb27` *(e valgono qui)*

- **Le premesse del guardiano, rilette dal disco: confermate.** `|w - w0|` lungo `lunga_r1.52`: `7.3e-08` *(450)*, `1.08e-06` *(480)*, `5.74e-05` *(540)*, `2.71e-03` *(600)*, `2.79e-02` *(660)*. La coppia per anello col SUO stato a `r 1.5247`: `+0.70727` all'anello `12`, `-0.69613` al `13`.
- **Due errori miei:** in `ea8ace8f` ho scritto «`13`-`14`» *(il profilo di `r 1`)* per lo stato di `r 1.5247` *(`12`-`13`)*; e «nessun modo sopra `0.039`» presupponeva un seme pari al residuo di Newton, **che il modo non aveva** *(il seme era molto piu' piccolo)*.
- **Lo stato del tick e' solo `psi_h`** *(`phi` rimesso a `phi0` a fine tick)*: le analisi in corsa si fanno salvando e rimettendo `psi_h`; **il controllo e' il confronto al bit coi punti di `lunga_r1.52`**.

### Per la lezione *(punto `1`, sulla carta)*

Con il legame scalare per nodo `alpha` da `0` *(coda)* a `alpha_max` *(cuore)*, e un oggetto legato a `K` con `mu = A(K) + alpha_max + d = -mu0 + alpha_max + d` *(`d` piccolo: l'energia cinetica del legato)*:

- **la coppia nel cuore** *(`alpha = alpha_max`)*: `P0 + Ppi + 2 alpha_max - 2 mu = -a_n + 2 mu0 - 2 d`. **A `r = 1` e' `-2 d`, QUALUNQUE sia `alpha_max`:** il legame sposta di `alpha_max` sia l'oggetto sia la coppia, e l'oggetto ne prende due. **E' la ragione per cui la risonanza di `r 1` non si toglie cambiando il legame.** Da `dfb5ab7e` *(`S1`, `s 0.15`)*: `mu -0.566022365`, quindi `2 - pi - 2 mu = -0.0095`, `d = mu + pi/2 - 1 = +0.0048` *(col `mu0` del primo ordine; letti dal disco in questa sessione con `_modo_al_variare_di_s.carica`)*.
- **fuori da `r = 1`**, ciascuna delle tre condizioni scorre lungo il profilo per un tratto lungo `alpha_max` *(la coppia `2 alpha_max`)*: **evitarle tutte vuole che i pesi siano scelti rispetto a `alpha_max` e a `d`**, cioe' rispetto a `mu`, alla forma, a `N`: **la taratura che Luca esclude.** Il caso misurato: `r 0.69` *(nessun incrocio, c1 su `P0` a `+0.019` nella coda)* e' esattamente una fettina tarata.
- **Lo scrivo come REGOLA DA VERIFICARE, non come legge:** «incrocia» non e' ancora «decade». **I casi misurati:** `r 1` *(la coppia nel cuore; il modo in `P0 + Ppi`, `5f06dbfb`)*; `r 0.65` *(c1 su `P0` agli anelli `14`-`15`; `D` in `P0` li', `ea8ace8f`)*; `r 1.5247` *(la coppia agli anelli `12`-`13`; il modo: il punto `2`)*.
- **Quello che la regola NON dice, e lo scrivo:** sulla carta, a pesi liberi, esistono punti dove nessuna incrocia *(`085ffb27`, sez. `1`: `a_n 5`, `b_a 3`)*; **sono tarature** nel senso della decisione delle `09:09`, e la loro verifica e' in lista d'attesa.

### Per le conservazioni *(punto `2bis`)*, dal codice

| la grandezza | conservata dal tick? | da dove |
|---|---|---|
| `M = N_su + N_giu` | **si'**, esatta | ogni pezzo e' unitario; il legame e' una fase per nodo |
| **`Q_S = N_su - N_giu`** *(`sigma_z = diag(1, -1, ...)` sulle `12` componenti)* | **si', a `eps 0`** *(tutte le scene di `S1`)* | `doc/PROGETTO_U1.md`: ogni pezzo commuta con `sigma_z` *(Grover uguale sulle due, il legame con `rho` di tutte e due, `U` diagonale, la moneta identita' a `eps 0`)*; `3.2e-15` col tick intero. **Quindi `N_su` e `N_giu` SEPARATAMENTE.** **Lo ricontrollo lungo la corsa** *(DEVE PASSARE)* |
| **la quasi-energia** *(mod `2 pi/s`)* | **per il linearizzato attorno allo stato fermo, si'** *(la mappa e' periodica nel tempo: Floquet)* | una coppia `u`, `v` di Bogoliubov ruota con frequenze opposte: `E_1 + E_2 = 2 mu`. **E' la condizione della coppia stessa**; si misura dalle rotazioni delle componenti `P0` e `Ppi` di `D` |
| **il quasi-impulso** | **NO come grandezza conservata** *(la mappa non e' lineare)*; **si' come regola di selezione** del linearizzato **solo attorno a uno stato invariante per traslazione**, e lo stato fermo non lo e' | il tick commuta con le traslazioni del reticolo *(`DV.matrice` costruisce `A(k)` da un impulso: lo presuppone)*. **Quello che si puo' misurare:** due quanti a `K` hanno impulso `2K = K'` *(`3K = 0`)*; con `u` a `k1` e `v` a `k2`, `k1 + k2 = 2K`; **in `D` la parte `v` compare coniugata, a `-k2 = k1 - 2K = k1 + K`.** Le valli di `P0` e `Ppi` in `D` vanno quindi confrontate **con lo spostamento `+K` o `-K`** *(non so quale delle due piatte sia `u`)* |
| le rotazioni del reticolo | per il linearizzato attorno a uno stato simmetrico | **non la misuro** *(lo dichiaro)*: le armoniche di `D` si stampano come in `5f06dbfb`, senza lettura di conservazione |

### Due fatti di metodo, scritti PRIMA

- **Il campionamento:** alla risonanza della coppia, le parti `P0` e `Ppi` di `D` ruotano a `-(P0 + alpha* - mu)` e `-(Ppi + alpha* - mu)` per unita' di tempo, con `alpha* = mu - (P0 + Ppi)/2`: **a `r 1.5247` circa `±1.79`** *(`alpha* ~0.60`)*, **a `r 1` circa `±pi/2`**. **Ogni `10` tick a `s 0.15` *(`1.5`)* e ogni `10` a `s 0.3` *(`3.0`, `5f06dbfb`)* sono troppo radi:** a `r 1` il campionamento di `5f06dbfb` **sta sotto Nyquist** *(`pi/2 * 3 = 4.7 > pi`)*: **il «periodo `10.91`» di `5f06dbfb` potrebbe essere un alias.** Qui: **ogni `5` tick** a `r 1.5247` *(`0.75`)*, **ogni `2`** a `r 1` *(`0.6`)*.
- **I `D` di `5f06dbfb` NON sono salvati** *(si calcolavano in memoria)*. Il mandato dice «nessuna corsa nuova»: **li RIGENERO con gli stessi `600` tick, controllati AL BIT coi punti di `26300537`** *(lo stesso controllo di `5f06dbfb`)*. **Non e' una corsa nuova: e' lo stesso dato** *(«il dato E' il comando che lo produce», `CLAUDE.md` par.`6`)*. **Lo dichiaro; se Luca lo considera una corsa nuova, la parte `r 1` del `2bis` si toglie.**

### Cosa NON so

- se il modo di `r 1.5247` e' **uno**;
- quale delle due piatte sia la `u` e quale la `v`;
- se le valli dello stato fermo sono `K` sola o `K` e `K'` *(lo misuro: e' la premessa del test d'impulso)*;
- se la finestra lineare esiste sotto `1e-2` con abbastanza campioni *(dai punti del guardiano: `480`-`630`)*.

## 2. I CRITERI

| il punto | il criterio *(fissato qui)* |
|---|---|
| `1`, la lezione | **nessuna corsa:** il conto delle tre condizioni ai due estremi del profilo *(`alpha` della coda e del cuore, dal profilo di ogni stato)* per `r 1`, `0.65`, `1.5247`, e `r 0.69` **etichettato come la fettina tarata**; con `_strada_b_lati.conto`; scritto in `doc/BANDE_PIATTE.md` come **regola da verificare** |
| `2`, la corsa | `4400` tick da `fermo_r1.52` col cammino di `lunga` *(`CL.avanza`, `VC.FORMA`, `DC.ZERO`, i pesi in memoria)*; **DEVE PASSARE: i punti ogni `10` tick = `lunga_r1.52`, AL BIT**; **DEVE PASSARE: `Q_S` e `M` conservate entro `1e-10` relativo** |
| `2`, `D` | `D(t) = e^{i mu s t} psi(t) - psi0`; `|D|/|psi0|` ogni `5` tick dall'inizio; `D` intero ogni `5` tick fra il tick `3000` e il `4400` *(tempo `450`-`660`)*, salvato in `db/tre_incroci/` *(non committato)*; un `.json` coi numeri derivati, committato |
| `2`, la finestra | da `10` volte la deriva lineare della corsa breve *(`c + v tau` di `forma_r1.52.json`)* a `1e-2`; **il tasso** = la pendenza di `ln|D|` nella finestra, lo scarto massimo dalla retta; **accanto, il tasso di `|D|` nelle sole piatte** *(fuori dalla banda `A` dove sta la deriva)*, nella stessa finestra |
| `2`, il periodo | come `5f06dbfb`: i cambi di segno di `Re<D(t_rif), D(t)>`, `t_rif` l'ultimo campione della finestra; **e le rotazioni per banda:** `arg<D_b(t), D_b(t + 5)>` per unita' di tempo, per `P0` e `Ppi` |
| `2`, la forma | **a tre istanti: il primo, quello di mezzo e l'ultimo campione della finestra**: le bande, i tre anelli maggiori e il profilo di `|D|^2` per anello, le armoniche `m 0..12` di `drho` e della fase *(`MI.per_nodo`, `MI.armoniche`)* |
| `2bis`, `Q_S` | sugli stessi `D` salvati: `q(X) = <X, sigma_z X>/<X, X>` per `X` = `psi0`, la parte `A` di `psi0`, `D`, `D_P0`, `D_Ppi`, `D_P0 + D_Ppi`, `D_A` *(le parti dai proiettori di banda di `DV.autovettori`: un gruppo intero di bande, quindi indipendente dalla base dentro il gruppo)* |
| `2bis`, le valli | i pesi in `K`, `K'`, «altrove» *(la valle `Gamma` di `DV.geometria`)* di `psi0` *(la sua parte `A`)*, di `D_P0`, di `D_Ppi`; **il confronto delle valli di `D_Ppi` con quelle di `D_P0` spostate di `0`, `+K`, `-K`** *(la differenza assoluta dei tre pesi)* |
| `2bis`, la quasi-energia | `rot_P0 + rot_Ppi` *(le rotazioni per banda)*, e `alpha*` ricavato da ciascuna *(`alpha* = mu - P0 - rot_P0`... col segno della convenzione `-arg/s`)* contro `alpha` agli anelli dove la coppia si incrocia |
| `2bis`, `r 1` | i `600` tick di `5f06dbfb` rigenerati con `MI.Mappa` *(`s 0.3`, `L 81`)*; **DEVE PASSARE: i punti ogni `10` tick = `26300537`, AL BIT**; `D` ogni `2` tick nella finestra di `5f06dbfb` *(da `1e3` volte il residuo a `1e-2`)*; le stesse grandezze |

## 3. LE LETTURE *(di Luca, scritte prima, senza soglie)*

- **Punto `2`:** **(m1)** `D` nelle piatte `P0 + Ppi` agli anelli `12`-`13`: la coppia locale, **la regola del punto `1` confermata**; **(m2)** altrove *(dove)*: **la regola non basta.** **Come si legge, scritto qui:** (m1) se, ai tre istanti, `P0 + Ppi` pesa piu' di `A + B` **e** l'anello maggiore di `|D|^2` e' il `12` o il `13`; altrimenti (m2), col dove.
- **Punto `2bis`:** **(n1)** tutte tornano: il decadimento e' permesso dalle conservazioni del modello *(come un atomo eccitato)*; **(n2)** una non torna: quale, e perche' il decadimento avviene lo stesso. **Come si legge, scritto qui:** `Q_S` torna se `q(D_P0 + D_Ppi)` e' uguale a `q(psi0)` entro la dispersione fra i tre istanti; la quasi-energia torna se `rot_P0 + rot_Ppi` e' zero entro la stessa dispersione; **l'impulso non e' una conservazione** *(vedi sopra)*: le valli si riportano, e si dice quale spostamento le accoppia, senza farne una lettura (n1)/(n2).

## 4. LE MOTIVAZIONI

La decisione delle piatte fra **(A)** *(tenerle come fisica: il solitone stabile e' lo stato che respira)* e **(C)** *(un legame diverso sulle piatte, per una ragione di principio)*, **di Luca, dopo il punto `2`**. Se la regola regge, ogni oggetto legato a `K` con un legame scalare sente le piatte: la domanda non e' piu' «quali pesi» ma «le piatte sono fisica o no». Il `2bis` dice se il decadimento e' **lecito** nel modello *(un atomo eccitato che decade)* o se viola qualcosa *(un difetto)*.

## 5. TODO

1. Questo file e l'annotazione su `2026-10-30_tre_incroci.md`, committati **DA SOLI**.
2. `csv/_modo_lento.py` *(`--modo`, `--uno`, `--referto`)* e la sua riga nell'inventario, committati **prima** di girare.
3. `--modo` *(r 1.5247)*: il `.json`, committato.
4. `--uno` *(r 1, i `D` di `5f06dbfb` rigenerati)*: il `.json`, committato.
5. `--referto` in `doc/referti_l2/modo_lento.txt`.
6. `doc/BANDE_PIATTE.md`: la sezione della lezione; la strada (B) fuori dal menu come cura.
7. `RELAZIONE_PER_CLAUDE.md`; `doc/MAPPA.md`: la riga `d`; la lista d'attesa *(i punti `2`-`3` delle `08:52`, tolti come taratura; la decisione sulle piatte `(A)`/`(C)`)*; l'errore `n.83` del guardiano; la decisione delle `09:09`; la sostituzione `08:52` -> `09:09` e l'aggiunta `2bis`.
8. La sezione `6` qui; il checkpoint; la coda.

## 6. ANNOTAZIONE DOPO IL REFERTO *(`doc/referti_l2/modo_lento.txt`; lo script `sha1-BYTE 36ff91ba`, `a3e7100d`; `8/8`)*

| il punto | l'esito |
|---|---|
| `1`, la lezione | il conto lungo il profilo *(nessuna corsa)*: `r 1` la coppia `-2.0095 -> -0.0096` *(tocca lo zero nel cuore, a `-2 d`)*; `r 0.65` c1 su `P0` fra `14`-`15`; `r 1.5247` la coppia fra `12`-`13`; `r 0.69` nessun incrocio *(la fettina tarata, c1 su `P0` a `+0.019`)*. In `doc/BANDE_PIATTE.md` sez. `5`, **come regola da verificare** |
| `2`, il modo lento | al bit con `lunga_r1.52` *(`440` confronti)*; `Q_S` e `M` entro `1.2e-12`; la finestra `377`-`621`; **il tasso `0.0331`** *(le piatte `0.0310`)*; le rotazioni `P0 +1.821`, `Ppi -1.783`; `alpha*` `0.638`/`0.604` contro `0.602`; a `450` e `535.5` `P0 + Ppi` `0.92`/`0.90`, anelli `12`-`13`; **a `621` `A` `0.507`** -> **ALLA LETTERA `(m2)`** *(il criterio chiedeva i tre istanti)* |
| `2bis` | `Q_S`: `psi0` tutto spin su, **banale**; alla lettera TORNA a `r 1.5247`, **NON TORNA a `r 1` per un artefatto del proiettore** *(`Ppi`/`A` in `Gamma`, `~1e-6`; `q(D) - 1 <= 8e-9`)*. **La quasi-energia TORNA** *(`+0.037 ± 0.11`, `-0.013 ± 0.066`)*. Le valli: non distinguono a `r 1.5247` |
| `r 1` *(i `D` di `5f06dbfb`)* | al bit con `26300537` *(`60` confronti)*; il tasso `0.13901` *(`5f06dbfb` `0.13870`)*; **il periodo `4.07`-`4.10`, non `10.91`: un alias del campionamento ogni `3`** *(il conto `11.20`-`11.39`; vale anche per l'`11.45` di `de411167`)* |

- **Una premessa corretta PRIMA dei numeri** *(nel commit dello script, `1eb344e6`)*: in un modo di Bogoliubov le due componenti di `D` portano direttamente i due quanti *(`k_Ppi = 2K - k_P0`, una riflessione)*, non uno spostamento di `±K`; lo script ha confrontato tutte e cinque le mappe.
- **Due righe AGGIUNTE DOPO I NUMERI** *(`a50ab539`, `a3e7100d`)*: `q - 1` a precisione piena, `alpha*` dalle rotazioni, e il periodo che si vede campionando ogni `3`. **Nessun criterio cambiato.**
- **Il mio errore:** dopo la prima di quelle due modifiche, il commit e' stato **rifiutato** *(`H-NON-TRACCIATI`: il referto precedente sul disco)*, ma il referto e' girato lo stesso, perche' `| tail` nascondeva il codice d'uscita del commit *(la trappola gia' scritta in memoria)*. **Quel referto, timbrato «MODIFICATO rispetto a HEAD», e' stato cancellato senza committarlo; il referto valido e' quello rigirato dopo `a3e7100d`.**
- **Il criterio di `Q_S` era mal fatto:** la dispersione fra tre istanti non e' una barra per un artefatto di `1e-6`. Dichiarato, non cambiato.
