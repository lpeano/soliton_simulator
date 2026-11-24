# 2026-11-22 -- L'ANEMOMETRO: IL BORDO PORTA LA MASSA? IL VENTO CHE SPINGE E IL VENTO CHE INFORMA *(il mandato di Luca [M1052], fase 3, [M1052-G], e l'aggiunta [M1052-I] delle `10:59`)* [[PROGETTO-MITOSI]]

> **Le regole di questo file:** cio' che dicono Luca e il guardiano e' scritto come LORO; le premesse non si riscrivono, si annotano; **SOLA LETTURA** *(nessuna corsa, un processo breve)*; i file sono nuovi. **Scritta PRIMA del codice `doc/referti_l2/anemometro.py` e dei numeri.**

## 1. I MANDATI *(copiati)*

> «[M1052-G] Sugli stati di chi-mattone-v2 (k 2000, 6000, 10000 e l'ultimo) e di caduta V1: il flusso radiale di χ (c²·f·∂χ/∂r integrato sull'anello, con l'inerzia f), il flusso di impulso della materia e |φ − φ0| medio, attraverso anelli di raggio 20, 25, 30, 40, 60 attorno al baricentro; il confronto con la Yukawa 2D di portata v/m ≈ 61 (K1(r/61), normalizzata a r 30). Il caso noto: su χ statico calcolato a mano per una sorgente puntiforme, il flusso ridà K1 entro l'1%. Referto doc/referti_l2/anemometro.txt.»

> «[M1052-I] Due grandezze per anello e per stato, accanto al flusso di impulso già previsto: (a) L'AGGANCIO DI FASE [...] Γ(r) = |Σ_anello w·e^{i(θ_anello − θ_mattone)}| / Σ w, con θ la fase del vuoto φ (e, a parte, della materia ψ dove ρ > 1e-6), θ_mattone la fase media pesata con ρ entro r 15, w il peso |φ − φ0| (dichiarato). (b) IL FLUSSO DI AGGANCIO: dΓ/dt fra stati salvati successivi, per anello. (c) Il confronto: per ogni anello e per ogni variante della caduta (V1, V2, V3, V4) e per chi-mattone-v2, il rapporto fra il flusso di impulso e Γ, e fra il flusso di impulso e dΓ/dt [...]. IL CASO NOTO: sul vuoto F3 puro Γ = 0 entro il rumore e il flusso di impulso = 0; IL DEVE-FALLIRE: con le fasi dell'anello mescolate a caso (seme fisso) Γ scende sotto 0,05 anche dove senza mescolare è alto. Dichiarato: Γ è un indicatore di informazione, non l'informazione di Shannon.»

**Le previsioni del guardiano** *(copiate)*: **P-S4:** fuori dal mattone il flusso di χ segue K1 entro il `10%` fra r `25` e `60` (χ porta la massa come una Yukawa). `70%`. **P-I1:** Γ cala con il raggio come l'alone del vuoto (circa `0,1` a r `30-40` nella scala di |φ − φ0|). `60%`. **P-I2:** il rapporto fra flusso di impulso e dΓ/dt è costante entro il `30%` fra gli anelli `25-60`, ma non fra le varianti V1-V4. `40%`.

## 2. LE PREMESSE DAL CODICE

- **Gli stati:** `chi-mattone-v2` *(`CHI/mattone_v2`, `L 186`, la scena `convergenza.scena_L(186, ...)` come `t4_sblocco`; **CON il bordo sorbente** `R_A = 50` del `meta`: ### ⚠ **l'anello di `r 60` sta DENTRO il bordo che assorbe, e li' `phi` e' tirato a `phi0`: dichiarato**)*; la caduta *(`CHI/caduta/<V>`, S162, senza bordo, `chi` IMPOSTO: ### ⚠ **il flusso di `chi` della caduta NON e' quello del mattone, e' il seno imposto: lo stampo, ma non dice niente su P-S4**)*.
- **Quali stati:** `chi-mattone-v2` a `k 2000, 6000, 10000` e l'ultimo salvato quando lo script parte, **ciascuno col suo precedente** `k - 250` *(per `dGamma/dt` «fra stati salvati successivi»)*; la caduta: tutti gli stati `0 ... 2000` di V0, V1, V2, V3, V4, V1m.
- **Il centro degli anelli:** il baricentro di `rho` dello stato *(`toro.centro`)*; **gli anelli** `|r - R| < 0.5`, `R = 20, 25, 30, 40, 60`.
- **`|phi - phi0|`:** `porto.dphi_nodi(Z, t0 + k)` *(lo strumento delle mappe del 15/11: per nodo `sqrt(somma_6 |phi - c(t) F3|^2)`; `t0 = G2.T0`, come `chi_mattone_v3`)*; **la media sull'anello.**
- **Il flusso di `chi`:** `Phi_chi(R) = c2 f 2 pi R dchi/dr`, `dchi/dr = (chi(R + 1) - chi(R - 1))/2` dalle medie sugli anelli; `c2`, `f` dal `meta`. **La Yukawa 2D:** `chi ~ K0(r/lambda)`, quindi `dchi/dr ~ K1(r/lambda)` e **il flusso `~ r K1(r/lambda)`**; ### ⚠ **il mandato dice «K1, normalizzata a r 30»: confronto il CAMPO `dchi/dr` con `K1` e il FLUSSO con `r K1`, tutte e due normalizzate a `r 30`.** **La portata** dai numeri del codice: `lambda = sqrt(3/2 c2 / m2)` *(il `3/2` del laplaciano del reticolo a triangoli nel continuo)* `= 61.24` con `c2 0.25`, `m2 1e-4`.
- **Il flusso di impulso della materia:** `J` per nodo *(lo strumento di [M0908-M]: `spostamento_trasporto` a `0.5`, col `cs` e la fase dello stato)*; ### ⚠ **lo strumento da' la DENSITA' d'impulso, non il tensore dello sforzo: per «il flusso di impulso attraverso l'anello» uso `Phi_J(R) = 2 pi R <J . r_hat>_anello`** *(la corrente radiale sull'anello)*: **dichiarato, da confermare da Luca.**
- **L'aggancio `Gamma`:** la fase del vuoto per nodo `theta_v = arg somma_6 conj(phi0) phi`; la fase della materia `theta_m` = la componente di `psi_h` del primo semiarco con la norma piu' grande *(`girandola_chi_v3.fase_dei_nodi`)*, solo dove `rho > 1e-6`; **`theta_mattone = arg somma_{r < 15} rho e^{i theta}`** *(la «fase media pesata con rho»)*, per il vuoto e per la materia; **`w = |phi - phi0|`** per tutte e due *(dichiarato, il mandato)*. **`dGamma/dt = (Gamma(k) - Gamma(k - 250))/250`.**
- **Il confronto (c):** `Phi_J/Gamma` e `Phi_J/(dGamma/dt)` per anello e per variante; **il coefficiente di variazione** *(`std/|media|`)* fra gli anelli `25-60` e fra le varianti V1-V4 a parita' di anello: **«costante» se sotto il `30%`** *(la soglia di P-I2)*.

## 3. I CASI NOTI

- **(G)** su S162: `chi = (c2 L + m2)^{-1} delta` *(il solutore del codice, `chi_tick.Laplaciano.statico`, una sorgente in un nodo)*: **il flusso misurato col MIO operatore, normalizzato a `r 30`, contro lo stesso operatore applicato al campo del continuo `somma_immagini K0(|x - x_i|/lambda)`** *(le immagini del toro `L (k1 A1 + k2 A2)`, `|k| <= 2`)*, a `r 20, 25, 40, 60`: **entro l'`1%`**. ### ⚠ **Non contro `r K1` nudo:** sul toro di `162` le immagini a `r 60` pesano parecchio *(`K1(102/61)/K1(60/61)` non e' piccolo)*; **stampo anche lo scarto da `r K1` nudo.** **Il deve-fallire:** contro il campo senza massa *(il flusso costante)* lo scarto a `r 60` supera l'`1%`.
- **(I)** il vuoto F3 puro, UN tick del tick U *(`gravita_due_corpi.tick_U`, `psi = 0`)*: **`w` e' rumore di arrotondamento**, quindi **`Gamma <= 3/sqrt(n_anello)`** *(fasi a caso)*, e **`Phi_J = 0` esatto** *(`psi = 0`)*. **Il deve-fallire** *(il mandato)*: sullo stato `k 2000` di V1, con le fasi dell'anello mescolate *(il seme `11`)*, `Gamma < 0.05` dove senza mescolare e' sopra `0.2`. ### ⚠ **Se nessun anello ha `Gamma > 0.2`, il deve-fallire non ha materia: lo stampo, non lo conto.**

## 4. LE PREVISIONI *(mie, accanto)*

- P-S4 `55%` *(il mattone con `chi` ha anche `c0`, lo sfondo: il flusso fuori puo' cambiare segno)*; P-I1 `45%`; P-I2 `25%`.

## 5. TODO

- [ ] committare questa carta e `anemometro.py`; girarlo quando c'e' un posto *(un processo breve)*; il referto, commit, la relazione nel ramo principale.
