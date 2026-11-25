# Lo stato in volo (per una sessione nuova del guardiano)

Aggiornato: 2026-11-24, 23:50.

## Dove siamo
- Rami del Cantiere: `lapse-u` (nucleo ricongelato il 22/11; l'oggetto al fondo a K) e `mitosi` (lapse-u fuso dentro il 24/11, 13:40). Nucleo: 5 file su lapse-u, 9 su mitosi (vedi SKILL.md).
- L'oggetto al fondo a K (il punto fisso del giro 4, [M1932], respiro 6,8%, w 10,9, m* +18,9 in tre misure): orologio come N in V2; caduta VERSO il tempo lento; la legge a = −∇ω/m* vale all'1% nella prima finestra (gradiente pesato, convenzione della cima), per l'oggetto compatto e per quello fermo largo 11; K cala nel tempo (1,00 → 0,89 → 0,77) uguale per forme, scale, velocità; la rampa lo attenua (0,83) ma non lo toglie; le onde di ritorno di ψ NON lo spiegano (norma lontana 3e-4).
- Il vento del vuoto ([M2245], 22:59): in V2 il vuoto φ (ω −0,471) cade nel gradiente di N con v_φ = ω_φ k ⟨dN/dy⟩ entro il 7% (28,8σ), 7–14 volte la velocità dell'oggetto; non si ammassa. Nel seno dipinto. Nel modello intero (χ dalla materia) è in corsa: [M2330] due oggetti del fondo con χ vero (d1), senza (d2), uno solo con χ (d3), 6000 tick, stati ogni 250; previsioni nel mandato.
- Lo specchio è chiuso (V3 etichetta, 5σ). E(p): newtoniano fino a un terzo di c, poi si spezza. Eötvös: 0,11 sull'intera corsa, 0,01–0,02 nella prima finestra.
- Idee in attesa (stella polare, MAPPA sez. 6): H1 elemento/aggregato; H2 somma di configurazioni; H3 mitosi come assorbitore; H4 la fiammata delle nascite come scarica del toro. Condizione per tutte: prima il freno.

## Decisioni di Luca in vigore
Un solo lanciatore (coda_m1446.py); nessuna gestione nuova senza «DECISIONE DI LUCA (hh:mm)»; F0 predefinita; niente era 3; il bordo assorbente spento (toro, g_e = 0); il guardiano scrive solo sul ramo `guardiano` ([M2345]); la diagnosi delle retroazioni si fa nel modello intero, non sul seno (24/11, 23:27).

## Pendenti
- [M2330] in corsa (fine ~01:00): leggere d1/d2/d3.
- La decisione sullo zero del vuoto (V2 fa cadere il vuoto; lo zero vero no): rimandata a dopo [M2330].
- Le schede [M1751] (cadute quattro volte): contesto pulito, prova a secco.
- [M1739-E2] la deriva dell'energia senza nascite: mandato a parte.
- Il post Itaca «Il Big Bang era un gong» (scritto, non so se pubblicato); il documento «La materia al fondo a K» nel progetto Claude (artefatto Docs, aggiornato al 24/11 sera).

## Aggiornamento 2026-11-25 01:40
- [M2330] chiuso: d1 si avvicina (63,46 -> 8,47), d2 no; vento radiale verso l'oggetto cresce; ma la coppia era a 63,46 in diagonale (A2) e chi partiva fuori equilibrio (-9,4 -> -150, oscilla), respiro 0,90: numeri non quantitativi.
- [M0105] eseguito via posta (137baaf9) e portato su lapse-u (33737d2d): la posta funziona.
- [M0137] in posta (DECISIONE DI LUCA 01:37): punto fisso con chi acceso, poi coppia a (+24,+48) = 41,57 lungo y; criterio C 10%/10%/3 giri.
- Il coordinatore in Python: progetto a parte, Luca lo vedra' poi.

## Aggiornamento 2026-11-25 09:25 (sospensione)
- [M0414] fatto: l'oggetto con chi esiste (w 4,5, omega 0,0833, pozzo -102 +-4), con un modo normale Omega_b = 2 pi / 2500 (D). Cinque previsioni su cinque dalla parte giusta.
- La coppia dal giro 3 NON si compone: il vuoto del giro 3 non e' a phi_v (|a| 0,019, residuo 52; chi lontano -24). Via decisa da Luca (09:25): psi e chi dal giro 3, phi FRESCO; d3' controllo; lettura solo sulle finestre con w, omega entro 5% del giro 3.
- [M0237] mitosi: H cala lungo la fiammata e va nelle nascite (H + E_persa costante); K3, K4 falliti, pezzi 3-4 fermi (D1: provenienza di MITOSI; D2: residuo senza rho).
- Le corse della rampa [M0137] pezzo 6 (d1', d2', d3' in rampa, chiuse 05:23) esistono ma sono fuori mandato: non lette.
- Repo: 4860 commit, 1,07 GB su GitHub, RELAZIONE 27.500 righe: un mandato di gestione (binari fuori da git, RELAZIONE per mese) da proporre a coda vuota.
- Il postino non interrompe: il «leggi la posta» viene eseguito a fine passo (la rampa e' partita 1 minuto dopo il comando).
