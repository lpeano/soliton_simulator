# [M2351] IL MATTONE DEL FONDO: K-T v2 E LA SUITE 5b-5f *(il mandato di Luca; la carta `doc/CARTA_torneo_nonlinearita.md`, sez. 13)* [[PROGETTO-MITOSI]]

> **Scritto e committato PRIMA del codice.**

## 1. LE PREMESSE DAL CODICE *(cosa credo, e cosa NON so)*

- **Gli stati a `k 1500` ci sono** *(`E:\soliton_simulator\controllo\M1631\tenuta_v2\L-1_proiezione_Gamma` e `...\tenuta\S1_cima`, ogni `250`, col campo `A`, `E`)*: **la partenza della suite si legge dal disco, non si rifa'.**
- **`massa_calcio` partiva dallo STAMPO** *(`caduta_libera.prepara`)* **e ricalcolava il campo con Gauss**; qui si parte da uno stato evoluto: **il campo si prende dal file.** **Non so** se F0 da `k 1500` *(contratto: `w 7.8` contro `15.5` dello stampo)* ridia m* `-19.26` entro il `2%`: **se no, il caso noto cade e lo dico per primo** *(l'oggetto dopo il transitorio non e' quello dello stampo)*.
- **La banda piatta:** se l'oggetto del fondo e' fatto di stati della banda piatta, `v` puo' essere sotto il rumore; ma `omega` e' **fuori** dalla banda *(`-0.599`, `0.117` sotto il fondo)*: **non so** quanto pesa.
- **L'orologio, la caduta e le coppie** *(5c-5e)* hanno ognuno un suo strumento di oggi *(`orologio_mattone_v2`, `caduta_libera`, `gravita_due_corpi_d`)* che parte dallo stampo: **li leggo prima di scrivere 5c-5e**, e le definizioni vanno nella carta prima del loro codice.

## 2. PROGETTAZIONE DEL RAGIONAMENTO

- **(R1)** `doc/referti_l2/torneo_kt_v2.py`: le sei tenute e (a) rilette con K-T v2 *(sola lettura)*; i DEVE: F0, FH, FT, L+0.5, L+0.25 REGGE; L0 NON REGGE *(il controllo negativo)*.
- **(R2)** `doc/referti_l2/fondo_suite.py calcio`: 5b come nella carta sez. 13; le corse in coda a priorita' `0`; `lettura_calcio`.
- **(R3)** **se m* del fondo e' misurabile:** le definizioni di 5c, 5d, 5e nella carta, poi il codice, poi le corse; **se no: FERMO** *(il mandato)*.
- **COSA MI FA FERMARE:** il controllo negativo L0 che regge con K-T v2; m* del fondo sotto il rumore; il caso noto di F0 fuori dal `2%` *(lo dico, e non e' un FERMO del mandato: e' un caso noto che cade, e chiedo)*.

## 3. TODO

1. commit di questo file, della sez. 13, di `doc/SAGOMA.md` *(DANNO)* e della relazione;
2. R1: codice, commit, lettura, referto;
3. R2: codice, commit, voci in coda, il dispatcher; a corse chiuse la lettura;
4. R3 secondo m*.
