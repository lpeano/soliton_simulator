# 2026-10-28 — IL CUORE E L'ALONE DEL CONGELATO LUNGO *([[VUOTO-SUL-FONDO]], [[PROGETTO-MASSA-COLLETTIVA]]; la risposta di Luca delle `18:12` a `40061005`)*

> ### **LIVELLO: un'analisi dei dati gia' prodotti da `40061005`; nessuna corsa nuova, nessun file del nucleo.**
> *(Prima forma con i titoli nuovi, regola di Luca del `2026-10-28`: premesse, criteri, letture, motivazioni.)*

## 0. IL MANDATO

```
LA LETTURA DA PROVARE: il solitone non si disfa; si ASSESTA emettendo onde (la parte non esattamente stazionaria
dello stato di partenza) e respira (periodo 11.1). Il guardiano ritira la frase netta di 83daa823 "la deriva lunga
non viene dallo stato di partenza".
(a) dai jsonl, nel tempo: la norma del CUORE (entro w_in) e quella dell'ALONE (M meno la norma entro 3 w0), alle due taglie;
(b) la FWHM allo stato iniziale e finale;
(c) il profilo radiale medio allo stato iniziale e finale;
(d) il cuore finale contro il solitone del risolutore alla norma del cuore (stessa s): larghezza e picco.
LETTURE: cuore stabile + alone che cresce + FWHM che resta o cala = STABILE e irradia; cuore che cala senza fermarsi =
si svuota; (d) dice se il cuore e' gia' l'oggetto stazionario. Nessuna corsa nuova.
```

## 1. LE PREMESSE DAL CODICE

- **i punti** *(`doc/referti_l2/congelato_lungo/L<81|120>_<scena>_<t0>.jsonl`, `_congelato_lungo.punto`)*: ogni `10` tick
  `f_win` = frazione di `M` entro `w_in` dal baricentro, `f_3w0` = frazione entro `3 w0`, `picco` = `rho.max()` per nodo, `M`.
  Quindi **cuore = `f_win M`**, **alone = `(1 - f_3w0) M`**.
- `w_in = 6.6297` *(il secondo momento dello stato iniziale sul toro)*, `w0 = 6.6003` *(la larghezza del risolutore)*;
  `3 w0 = 19.8`.
- **gli stati:** l'iniziale si ricostruisce con `_congelato_lungo.iniziale(L, scena)`; il finale *(tick `10000`)* e' in
  `db/congelato_lungo/L<L>_<scena>.npz`, e si verifica con lo `sha_fine` del pezzo `08000`.
  **`uniforme` e `fondo` hanno gli `.npz` identici al byte** *(`cmp`)*: si analizza una scena per taglia, e si dichiara.
- **lo stato iniziale** *(`_energia_del_legame.stato`)*: `psi` = `u(r) sqrt(AREA_NODO)` del risolutore sul nodo, rinormalizzato a `N`;
  quindi `rho_nodo ~ u^2 AREA_NODO`, `AREA_NODO = sqrt(3)/2`, le posizioni nelle stesse unita' di `r` del risolutore.
- **il risolutore** *(`_deriva_congelato.prepara`)*: `MPS.largo(VC.FORMA, c, s, N)` con `MPS.LAM0 = STR.LAM0_TRI`; il profilo con
  `STR.profilo_u(forma, c, s, N, LAM0_TRI, w)`, che da' `(q, r, u)`, `q["larghezza"]` = secondo momento, `q["rho_centro"] = u(0)^2`.

## 2. I CRITERI

- **(a)** cuore e alone ogni `3` di tempo fisico; in tabella le medie per finestre di `500` e la pendenza per finestra.
- **(b), (c)** il profilo radiale medio: `rho` per nodo, media per anelli di larghezza `1` dal baricentro; la FWHM = `2 r_1/2`,
  `r_1/2` per interpolazione lineare dove il profilo scende a meta' del primo anello.
- **(d)** il risolutore a `N_cuore` = cuore finale, stessa `s`, stessa `c`: larghezza, `rho_centro AREA_NODO`, FWHM dal suo `u(r)`;
  contro il cuore finale: la FWHM, il picco, il profilo ai raggi `0..20`.
- **IL CONTROLLO DI SCALA** *(DEVE PASSARE)*: lo stato **iniziale** contro il risolutore a `N = M`: la FWHM e il picco entro il `2%`
  *(la discretizzazione sul nodo, non una manopola: e' lo stesso oggetto per costruzione)*. Se fallisce, **(d) non si legge**.
- **DEVE PASSARE:** lo stato finale caricato ha lo `sha1` = `sha_fine` del pezzo `08000`.
- **un limite dichiarato:** lo stato finale e' **un'istantanea** di un oggetto che respira *(ampiezza `0.02`-`0.04` in `w/w_in`)*.

## 3. LE LETTURE *(scritte prima dei numeri, senza soglie, come nel mandato)*

- cuore che si ferma + alone che cresce + FWHM che resta o cala → **STABILE, e irradia**;
- cuore che cala senza fermarsi → **si sta svuotando**;
- (d): FWHM e picco del cuore come quelli del risolutore a `N_cuore` → **il cuore e' gia' l'oggetto stazionario**;
  se no, si scrive di quanto e in che verso.

## 4. LE MOTIVAZIONI

- La larghezza come secondo momento pesa `r^2`: una piccola norma lontana la fa crescere anche se il centro non cambia.
  Il cuore, l'alone e la FWHM separano le due cose.

## 5. TODO

1. questo file, commit e push, da solo;
2. `csv/_cuore_e_alone.py`, commit e push prima di girarlo; l'INVENTARIO;
3. `--referto > doc/referti_l2/cuore_e_alone.txt`; la regola di forma in `doc/PATTERN_DI_PROVA.md`; la RELAZIONE; la MAPPA
   *(riga `4` della sezione `4`, riga nuova della sezione `1`)*; commit e push.
