# LA SCOMPOSIZIONE DELL'ENERGIA A RIPOSO DEL SOLITONE *(la parte 2 del mandato del 2026-10-27; la misura `(e)`)*

> **Il mandato:** di Luca, `2026-10-27` *([[SOLITONE-VUOTO-CONGELATO]], [[PROGETTO-MASSA-COLLETTIVA]], [[INDIRIZZO-MASSA-COLLETTIVA]])*: ### **sull'oggetto stabile della parte `1`** *(il solitone `S1`, `N 1e6`, col vuoto congelato: stabile fino a `2000` tick alle due taglie, `74f99039`)*: ### **l'energia a riposo totale, la parte `N mu0`** *(la massa dei costituenti, fissa in archi)*, ### **la parte del legame col vuoto, la parte cinetica** *(la curvatura dell'inviluppo)*; ### **la frazione del legame.** ### **La risposta di Luca `(3)` delle `00:58`: questa misura va PRIMA della relazione energia-impulso.**
> ### **L'ipotesi di Luca delle `09:08`** *(la massa come autointerazione)* ### **e' cio' che questa misura mette alla prova sull'oggetto di oggi.**
> ### **Lo script `csv/_scomposizione_solitone.py`, il referto `doc/referti_l2/scomposizione_solitone.{txt,jsonl}`.**

**LIVELLO:** un conto d'energia su uno stato misurato.

## 0. LA STELLA POLARE

1. **`A14`:** ### **le norme si conservano** *(il vuoto congelato).* 2. **Il gradino:** ### **la massa di un oggetto composto.** 3. **Aggiunge un numero o una legge?** ### **No.** 4. **Tocca `rho`, `c_s` o il segno?** ### **No.** 5. **Emergente o imposto?** ### **Quanto della massa e' dei costituenti e quanto dell'interazione: e' la misura.**

## 1. LE GRANDEZZE *(fissate qui)*

- ### **LO STATO:** ### **quello della parte `1`** *(il profilo del risolutore sul toro a triangoli, `L 81` e `120`, il vuoto uniforme `1` per estremita')*, ### **a `t = 0` e dopo `2000` tick col vuoto CONGELATO** *(il tick con i pezzi del vuoto saltati e `phi` rimesso)*. ### **IL CONTROLLO: la larghezza e la frazione iniziali uguali al referto `74f99039` al bit** *(lo stesso stato)*.
- ### **LE PARTI, da `energia_pesata.termini_di_h`** *(a forma spenta, `cs = None` per la lettura)*: ### **la MATERIA QUADRATICA `E_mat = H(psi, phi = 0)`** *(Grover, spostamento, moneta su `psi`)*; ### **il VUOTO `H(0, phi)`** *(uniforme: `0`)*.
- ### ⚠ **IL LEGAME, DA RICALCOLARE:** ### **`termini_di_h` scrive `N = rho ln(rho/(rho + Lambda))`, la forma `S3` del nucleo, NON quella accesa in memoria;** ### **per `S1` l'energia del legame e' `N_1 = Lambda F_1(x)`, `F_1(x) = x - arctan x`, `x = rho/Lambda`** *(coerente con `alpha_1 = F_1'(x) = x^2/(1 + x^2)` di `_screening_forme_s3`)*: ### **`E_legame = somma_k Lambda_k F_1(rho_k/Lambda_k)`.** ### **Il controllo della forma: `F_1'` per differenze contro `alpha_1` di `_screening_forme_s3.pezzi_di("S1")` entro `1e-8`.**
- ### **I COSTITUENTI `N e_K`:** ### **`e_K` = l'energia quadratica PER UNITA' DI NORMA dello stato UNIFORME del ramo della coppia del solitone** *(il ramo basso di `_triangoli_forza.coppia_K(0, s)`, lo stesso vettore `Q`, `e^{i K.r}`, sullo stesso toro)*: ### **`e_K = H(psi_K, 0)/|psi_K|^2`;** ### **`N e_K` e' cio' che avrebbero `N` costituenti fermi a `K`.**
- ### **LA PARTE CINETICA: `E_cin = E_mat - N e_K`** *(il costo della curvatura dell'inviluppo)*.
- ### **L'ENERGIA A RIPOSO: `E_0 = E_mat + E_legame`** *(rispetto al vuoto: la sua parte quadratica e' `0` prima e dopo)*.
- ### **LE FRAZIONI: `N e_K / E_0`, `E_cin / E_0`, `E_legame / E_0`; e il legame per costituente `E_legame/N` contro `mu` del risolutore** *(`+0.2983`)* ### **e contro `e_K`.**

## 2. I CRITERI

| | il criterio | il tipo |
|---|---|---|
| `1` | ### **lo stato a `t = 0` = quello della parte `1`** *(la larghezza e la frazione al bit col jsonl di `74f99039`)* | DEVE |
| `2` | ### **la forma del legame: `F_1'` = `alpha_1` entro `1e-8`** | DEVE |
| `3` | ### **le norme: `M` e `V` dopo `2000` tick entro `1e-10`** | DEVE |
| `4` | ### **la convergenza: le frazioni alle due taglie entro l'`1%`** | DEVE |

### **LA LETTURA, nessuna soglia:** ### **la frazione del legame: e' la massa un'autointerazione** *(l'ipotesi di Luca)* ### **o la somma dei costituenti?** ### **Mi FERMO** ### **se `1`, `2` o `3` fallisce.**

## 2-bis. ANNOTAZIONE, PRIMA DEL COMMIT DELLO SCRIPT *(una prova a `t = 0`, `L 81`, da una cartella pulita: NON il referto)*

- ### **Lo stato coincide con la parte `1`** *(la larghezza `6.629698`, la frazione `1.0`)*; ### **`e_K = -4.710543` per unita' di norma; `E_mat = -4.715062e6`, `N e_K = -4.710543e6`, la cinetica `-4.5e3`; il legame `+9.933e5`** *(per `S1` a `x >> 1` quasi `+1` per costituente)*; ### **`E0 ~ -3.72e6`: il legame ne e' circa il `-27%`** *(di segno opposto ai costituenti)*. ### **Le soglie restano.**

## 3. TODO

1. questo task history, da solo; 2. lo script, committato prima della corsa; 3. la corsa; 4. il referto, la relazione, l'indice.

## 4. IL RISULTATO *(dopo `dc4a1437`)*

### **IL REFERTO DELLA SCOMPOSIZIONE:** `doc/referti_l2/scomposizione_solitone.{txt,jsonl}` *(`csv/_scomposizione_solitone.py` al commit `dc4a1437`, «committato e pulito»; il task history `6c6b5ef0`)*. ### **`4/4`.**

- ### **I CONTROLLI:** ### **lo stato a `t 0` = quello di `74f99039` al bit; la forma del legame `F_1' = alpha_1` a `8.2e-11`; `M`, `V` dopo `2000` tick a `2.6e-13`; le frazioni alle due taglie entro `2.4e-5`.**
- ### ⭐ **LA SCOMPOSIZIONE** *(`S1`, `N 1e6`, `L 81` e `120`, a `t 0`)*: ### **`E0 = -3.721753e6` = i COSTITUENTI `N e_K = -4.710543e6`** *(`e_K = -4.71054` per unita' di norma, lo stato uniforme dello stesso ramo)* ### **+ la CINETICA `-4.52e3` + il LEGAME `+9.933e5`.** ### **Le frazioni: i costituenti `+1.2657`, la cinetica `+0.0012`, il legame `-0.2669`.** ### **Dopo `2000` tick col vuoto congelato: `+1.2657`, `-0.0001`, `-0.2656`** *(il legame `+0.9885` per costituente)*.
- ### **LA LETTURA** *(nessuna soglia)*: ### **l'energia a riposo di QUESTO oggetto e' DOMINATA DAI COSTITUENTI** *(`127%`)*; ### **il legame col vuoto e' `+0.99` per costituente** *(per `S1` a `x >> 1`: `F_1 ~ x`)* ### **e la RIDUCE di circa un quarto; la cinetica e' trascurabile.** ### **Non e' ancora la massa come autointerazione dell'ipotesi di Luca delle `09:08`:** ### **coi costituenti di oggi** *(la coppia con `mu0` fisso in archi)* ### **la massa resta la loro somma, corretta dal legame** *(la nota di Luca: la sua strada sono i costituenti SENZA massa, `(f)` e `(g)` del progetto)*.
- ### **UN'AVVERTENZA INNOCUA del referto:** ### **lo stato uniforme ha `phi = 0`, e il suo legame `rho/Lambda` da' `NaN`** *(non usato: dello stato uniforme serve solo la parte quadratica)*.
