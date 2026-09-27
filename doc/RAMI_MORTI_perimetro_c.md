# I RAMI MORTI COL DRIVER, dentro il perimetro della cura (c) — **121**

> **Mandato di Luca (2026-09-27):** *«Su `(b)3` LIMITA il perimetro: archivia SOLO i rami
> morti col driver che stanno nelle righe che la cura `(c)` di `ETC-PASSO` dovra'
> riscrivere (le cinque leggi del passo pieno e cio' che chiamano). Prima dimmi quanti
> sono, in una tabella (sito, perche' e' morto, flag coinvolti), poi STOP.»*
>
> ### 🛑 **QUESTO E' SOLO IL RILIEVO. Nessun ramo e' stato archiviato.**
> ### **Blob del simulatore `7439d5c3`, prima e dopo.**

**Strumento:** `csv/_test_fork/_etc_rami_morti.py`, referto `_etc_rami_morti.json`.
**Perimetro:** le **cinque leggi** del passo pieno e cio' che chiamano = **57 funzioni**.

## Il criterio, e perche' NON e' il campionamento

| | |
|---|---|
| un ramo **MORTO** | la sua condizione dipende **solo da flag di modulo** e, coi valori dell'argv del driver, **non puo' essere raggiunto**. E' una proprieta' della **configurazione** |
| un ramo **NON ESERCITATO** | in `N` passi non e' girato **ma potrebbe**. ### **Non e' morto**, e archiviarlo sarebbe un errore |

### **Un conteggio fatto sui soli 3 passi non distinguerebbe le due cose.**
**Test NON DECIDIBILI** *(dipendono da valori di runtime)*: **319** — e **non entrano**
nell'elenco.

## La corroborazione, e i due errori che ha trovato

**172 righe ESCLUSIVE** dei rami morti, e in 3 passi pieni ### **ZERO hanno eseguito.**

> **⚠ E ci sono arrivato in tre giri, perche' la RIGA non e' l'unita' giusta:**
> **①** al primo giro **37 righe <<morte>> avevano eseguito**: in un ternario e in un
> `if F: y` su una riga il ramo morto **condivide la riga con quello vivo**;
> **②** corretto quello, ne restava **UNA**, `:5272` — un ternario su due righe
> *(`chi_core = (... if CHI_COOP else ...)`)* dove **il test sta sulla riga del ramo
> morto** mentre `n.lineno` e' la precedente.
> **Si corrobora solo sulle righe ESCLUSIVE**, e i **61** rami che non ne hanno
> *(ternari e `if` di una riga)* sono **dichiarati non corroborabili per riga**, non
> spacciati per verificati.

## Le 121, in quattro famiglie

| famiglia | rami | righe | che farne |
|---|---|---|---|
| **① DIAGNOSTICI SWITCHABILI** | **41** | **41** | **NON si archiviano**: esistono per essere ACCESI |
| **② RAMI DI CONTROLLO di cure GIA' PROMOSSE** | **43** | **111** | il candidato NATURALE: e' la stessa forma di `tempo-unico-mitosi` e `SYNC_UPDATE` |
| **③ ESPERIMENTI SPENTI** | **17** | **70** | sono **ALTERNATIVE**, non doppioni: archiviarli e' una decisione di TEORIA |
| **④ DA GUARDARE UNO A UNO** | **20** | **21** | non entrano in una famiglia netta |

### ⚠ **E DUE COSE CHE NON VANNO ARCHIVIATE, e le dico subito**

**①** i **41 diagnostici** *(`TRACCIA_D0` da sola ne fa **37**, piu' `TRACCIA_VD`,
`TRACCIA_PEQ`, `INVARIANTI`)*: **sono spenti PERCHE' sono strumenti**, e archiviarli
vorrebbe dire **perdere lo strumento**. E' `A8`: la strumentazione deve esistere.

**②** ### `:5696` e `:5742` sono **LA PRECEDENZA CHE HAI APPENA CHIESTO DI RIPRISTINARE**
*(`if SCALA_MIN and not SCALA_MIN_PASSO`)*. Col driver sono morti **per costruzione** —
`SCALA_MIN` e' spento — **ma archiviarli cancellerebbe la correzione di stamattina.**
**E' l'esempio che mostra perche' <<morto col driver>> non basta come criterio.**

---

# LA TABELLA INTERA, per famiglia

## ② RAMI DI CONTROLLO di cure GIA' PROMOSSE — 43 rami, 111 righe

| riga | dentro | tipo | righe | perche' e' morto | flag = valore |
|---|---|---|---|---|---|
| `:5170` | `step` | else | 15 | il test e' VERO coi flag del driver: muore l'else | `REPULS_LEGGE`=`True` |
| `:5668` | `step` | else | 13 | il test e' VERO coi flag del driver: muore l'else | `VERLET`=`True` |
| `:5642` | `step` | else | 9 | il test e' VERO coi flag del driver: muore l'else | `VERLET`=`True` |
| `:3624` | `_passo_spinoriale` | else | 7 | il test e' VERO coi flag del driver: muore l'else | `TAU_LUCE`=`True` |
| `:3659` | `_passo_spinoriale` | else | 7 | il test e' VERO coi flag del driver: muore l'else | `SPINORE_CORRETTO`=`True` |
| `:5550` | `step` | else | 5 | il test e' VERO coi flag del driver: muore l'else | `TAU_LOCALI`=`True` |
| `:6241` | `mitosi` | else | 5 | il test e' VERO coi flag del driver: muore l'else | `PLAST_DIN`=`True` |
| `:3678` | `_passo_spinoriale` | else | 4 | il test e' VERO coi flag del driver: muore l'else | `DEPARAM_OROLOGIO`=`True` |
| `:6710` | `memoria_hebbiana_moto` | else | 4 | il test e' VERO coi flag del driver: muore l'else | `VIRIALE`=`True` |
| `:5755` | `step` | else | 3 | il test e' VERO coi flag del driver: muore l'else | `TAU_LOCALI`=`True` |
| `:5412` | `step` | ternario | 2 | muore il ramo `else`: il test e' True coi flag del driver | `CHI_CORE`=`True` |
| `:5444` | `step` | else | 2 | il test e' VERO coi flag del driver: muore l'else | `CHI_COOP`=`True` |
| `:5489` | `step` | else | 2 | il test e' VERO coi flag del driver: muore l'else | `CS_DINAMICO`=`True` |
| `:6215` | `mitosi` | else | 2 | il test e' VERO coi flag del driver: muore l'else | `REGIME`=`deterministico` |
| `:6530` | `pozzo_grafo` | else | 2 | il test e' VERO coi flag del driver: muore l'else | `POZZO_D`=`True` |
| `:6945` | `memoria_hebbiana_moto` | else | 2 | il test e' VERO coi flag del driver: muore l'else | `COES_ADIM`=`True` |
| `:3072` | `ritmo` | else | 1 | il test e' VERO coi flag del driver: muore l'else | `RITMO_WRAP_2PI`=`True` |
| `:3189` | `_passo_spinoriale` | else | 1 | il test e' VERO coi flag del driver: muore l'else | `RUMORE_COLORATO`=`True` |
| `:3629` | `_passo_spinoriale` | else | 1 | il test e' VERO coi flag del driver: muore l'else | `TAU_A_LOCALE`=`True` |
| `:3793` | `_passo_spinoriale` | else | 1 | il test e' VERO coi flag del driver: muore l'else | `SPINORE_CORRETTO`=`True` |
| `:5271` | `step` | ternario | 1 | muore il ramo `else`: il test e' True coi flag del driver | `CHI_COOP`=`True` |
| `:5280` | `step` | ternario | 1 | muore il ramo `else`: il test e' True coi flag del driver | `CHI_COOP`=`True` |
| `:5290` | `step` | else | 1 | il test e' VERO coi flag del driver: muore l'else | `REGIME`=`deterministico` |
| `:5305` | `step` | else | 1 | il test e' VERO coi flag del driver: muore l'else | `CS_DINAMICO`=`True` |
| `:5409` | `step` | ternario | 1 | muore il ramo `else`: il test e' True coi flag del driver | `CHI_COOP`=`True` |
| `:5412` | `step` | ternario | 1 | muore il ramo `else`: il test e' True coi flag del driver | `CHI_COOP`=`True` |
| `:5414` | `step` | ternario | 1 | muore il ramo `else`: il test e' True coi flag del driver | `CHI_COOP`=`True` |
| `:5425` | `step` | ternario | 1 | muore il ramo `else`: il test e' True coi flag del driver | `TAU_LOCALI`=`True` |
| `:5429` | `step` | ternario | 1 | muore il ramo `else`: il test e' True coi flag del driver | `TAU_LOCALI`=`True` |
| `:5556` | `step` | else | 1 | il test e' VERO coi flag del driver: muore l'else | `PEQ_ESATTO`=`True` |
| `:5562` | `step` | else | 1 | il test e' VERO coi flag del driver: muore l'else | `PEQ_ESATTO`=`True` |
| `:5571` | `step` | else | 1 | il test e' VERO coi flag del driver: muore l'else | `ANOM_SIMM`=`True` |
| `:5596` | `step` | ternario | 1 | muore il ramo `else`: il test e' True coi flag del driver | `CS_DINAMICO`=`True` |
| `:5608` | `step` | ternario | 1 | muore il ramo `else`: il test e' True coi flag del driver | `CS_DINAMICO`=`True` |
| `:5610` | `step` | ternario | 1 | muore il ramo `else`: il test e' True coi flag del driver | `CS_DINAMICO`=`True` |
| `:5666` | `step` | ternario | 1 | muore il ramo `else`: il test e' True coi flag del driver | `SCALA_MIN_PASSO`=`True` |
| `:5708` | `step` | ternario | 1 | muore il ramo `else`: il test e' True coi flag del driver | `CS_DINAMICO`=`True` |
| `:5710` | `step` | ternario | 1 | muore il ramo `else`: il test e' True coi flag del driver | `CS_DINAMICO`=`True` |
| `:5806` | `step` | ternario | 1 | muore il ramo `else`: il test e' True coi flag del driver | `CS_DINAMICO`=`True` |
| `:6336` | `mitosi` | ternario | 1 | muore il ramo `else`: il test e' True coi flag del driver | `PEQ_NASCITA_LOCALE`=`True` |
| `:6595` | `memoria_hebbiana_moto` | else | 1 | il test e' VERO coi flag del driver: muore l'else | `MEM_MOTO_TUTTO`=`True` |
| `:6718` | `memoria_hebbiana_moto` | else | 1 | il test e' VERO coi flag del driver: muore l'else | `OLON_PART`=`True` |
| `:6891` | `memoria_hebbiana_moto` | else | 1 | il test e' VERO coi flag del driver: muore l'else | `COES_CAUSALE`=`True` |

## ③ ESPERIMENTI SPENTI — 17 rami, 70 righe

| riga | dentro | tipo | righe | perche' e' morto | flag = valore |
|---|---|---|---|---|---|
| `:6172` | `mitosi` | if | 13 | il test e' FALSO coi flag del driver | `ANTIFASE_ADD`=`False` |
| `:3284` | `_passo_spinoriale` | if | 8 | il test e' FALSO coi flag del driver | `SPIN_LARMOR`=`False` |
| `:6153` | `mitosi` | if | 7 | il test e' FALSO coi flag del driver | `MITOSI_DIR`=`0.0` |
| `:3638` | `_passo_spinoriale` | if | 6 | il test e' FALSO coi flag del driver | `TW_SPINORE`=`False` |
| `:5416` | `step` | if | 6 | il test e' FALSO coi flag del driver | `POLO_MATURO`=`False` |
| `:6304` | `mitosi` | if | 6 | il test e' FALSO coi flag del driver | `COPPIA_DENSITA`=`False` |
| `:5604` | `step` | if | 4 | il test e' FALSO coi flag del driver | `ZETA_LOC`=`False` |
| `:5647` | `step` | if | 4 | il test e' FALSO coi flag del driver | `FERMA_DOPO_NSUB`=`False` |
| `:5657` | `step` | if | 4 | il test e' FALSO coi flag del driver | `FERMA_DOPO_NSUB`=`False` |
| `:3605` | `_passo_spinoriale` | if | 3 | il test e' FALSO coi flag del driver | `COPPIA_RECIPROCA`=`False` |
| `:6248` | `mitosi` | if | 2 | il test e' FALSO coi flag del driver | `PLAST_MIT`=`0.0` |
| `:6665` | `memoria_hebbiana_moto` | if | 2 | il test e' FALSO coi flag del driver | `SCALA_P_MEDIANA`=`False` |
| `:3587` | `_passo_spinoriale` | if | 1 | il test e' FALSO coi flag del driver | `GRAV_AMPIEZZA`=`False` |
| `:4070` | `_wphi` | if | 1 | il test e' FALSO coi flag del driver | `FASE_2PI`=`False` |
| `:5369` | `step` | if | 1 | il test e' FALSO coi flag del driver | `KURAMOTO_SU2`=`False` · `SYNC_FASE_OROLOGIO`=`False` · `SYNC_SPINORE`=`False` |
| `:5707` | `step` | if | 1 | il test e' FALSO coi flag del driver | `ZETA_LOC`=`False` |
| `:5769` | `step` | if | 1 | il test e' FALSO coi flag del driver | `TAU_USA_D0`=`False` |

## ④ DA GUARDARE UNO A UNO — 20 rami, 21 righe

| riga | dentro | tipo | righe | perche' e' morto | flag = valore |
|---|---|---|---|---|---|
| `:2122` | `_feedback_spinoriale_archi` | if | 2 | il test e' FALSO coi flag del driver | `SPIN_FEEDBACK`=`True` |
| `:597` | `massa_critica_collasso` | ternario | 1 | muore il ramo `if`: il test e' False coi flag del driver | `COMPAT_CHI`=`False` · `TORS_4PI`=`True` |
| `:1997` | `_eredita_spinore_figli` | if | 1 | il test e' FALSO coi flag del driver | `CAMPO_SPINORIALE`=`True` · `SPINORE_CORRETTO`=`True` |
| `:3018` | `_lam_archi` | if | 1 | il test e' FALSO coi flag del driver | `SCHERMATURA`=`True` |
| `:3030` | `ritmo` | if | 1 | il test e' FALSO coi flag del driver | `TAU_LOC`=`1.0` |
| `:3081` | `ritmo` | ternario | 1 | muore il ramo `if`: il test e' False coi flag del driver | `TEMPO_PROPRIO_ORIENTATO`=`False` |
| `:3842` | `_tempo_rampa` | if | 1 | il test e' FALSO coi flag del driver | `SEMINA_MATURA`=`True` |
| `:4062` | `_dphi` | ternario | 1 | muore il ramo `if`: il test e' False coi flag del driver | `FASE_2PI`=`False` |
| `:4407` | `_smp_chiudi` | if | 1 | il test e' FALSO coi flag del driver | `SCALA_MIN_PASSO`=`True` |
| `:5543` | `step` | ternario | 1 | muore il ramo `else`: il test e' True coi flag del driver | `DIFF_RES`=`0.0` |
| `:5548` | `step` | ternario | 1 | muore il ramo `else`: il test e' True coi flag del driver | `DIFF_RES`=`0.0` |
| `:5567` | `step` | else | 1 | il test e' VERO coi flag del driver: muore l'else | `HAM_SRC`=`0.0` |
| `:5597` | `step` | ternario | 1 | muore il ramo `else`: il test e' True coi flag del driver | `ALPHA_NAT`=`0.0` |
| `:5602` | `step` | if | 1 | il test e' FALSO coi flag del driver | `ZETA_M`=`0.75` |
| `:5696` | `step` | if | 1 | il test e' FALSO coi flag del driver | `SCALA_MIN`=`False` · `SCALA_MIN_PASSO`=`True` |
| `:5705` | `step` | if | 1 | il test e' FALSO coi flag del driver | `ZETA_M`=`0.75` |
| `:5742` | `step` | if | 1 | il test e' FALSO coi flag del driver | `SCALA_MIN`=`False` · `SCALA_MIN_PASSO`=`True` |
| `:5884` | `mitosi` | else | 1 | il test e' VERO coi flag del driver: muore l'else | `FASE_2PI`=`False` · `TORS_4PI`=`True` |
| `:6123` | `mitosi` | ternario | 1 | muore il ramo `else`: il test e' True coi flag del driver | `MITMAX`=`0` |
| `:6462` | `rilassa_disegno` | ternario | 1 | muore il ramo `if`: il test e' False coi flag del driver | `L_CONSERVA`=`False` |

## ① DIAGNOSTICI SWITCHABILI — 41 rami, 41 righe

| riga | dentro | tipo | righe | perche' e' morto | flag = valore |
|---|---|---|---|---|---|
| `:4257` | `verifica_invarianti` | if | 1 | il test e' FALSO coi flag del driver | `INVARIANTI`=`True` |
| `:5555` | `step` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_PEQ`=`False` |
| `:5561` | `step` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_PEQ`=`False` |
| `:5677` | `step` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_VD`=`False` |
| `:5842` | `step` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:5844` | `step` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:5853` | `step` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:5855` | `step` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:5857` | `step` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:5859` | `step` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:5861` | `step` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:5862` | `step` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6115` | `mitosi` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6117` | `mitosi` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6118` | `mitosi` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6120` | `mitosi` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6267` | `mitosi` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6270` | `mitosi` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6378` | `mitosi` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6381` | `mitosi` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6621` | `memoria_hebbiana_moto` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6623` | `memoria_hebbiana_moto` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6624` | `memoria_hebbiana_moto` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6625` | `memoria_hebbiana_moto` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6767` | `memoria_hebbiana_moto` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6769` | `memoria_hebbiana_moto` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6773` | `memoria_hebbiana_moto` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6775` | `memoria_hebbiana_moto` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6776` | `memoria_hebbiana_moto` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6777` | `memoria_hebbiana_moto` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6795` | `memoria_hebbiana_moto` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6797` | `memoria_hebbiana_moto` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6798` | `memoria_hebbiana_moto` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6799` | `memoria_hebbiana_moto` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6943` | `memoria_hebbiana_moto` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6944` | `memoria_hebbiana_moto` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6950` | `memoria_hebbiana_moto` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6951` | `memoria_hebbiana_moto` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6952` | `memoria_hebbiana_moto` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6998` | `memoria_hebbiana_moto` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |
| `:6999` | `memoria_hebbiana_moto` | if | 1 | il test e' FALSO coi flag del driver | `TRACCIA_D0`=`False` |

---

# CHE COSA PROPONGO, e la decisione e' di Luca

### **Il candidato e' la famiglia ②: 43 rami, 111 righe.**
Sono i **percorsi vecchi di cure gia' promosse** — la stessa forma di
`tempo-unico-mitosi` e di `SYNC_UPDATE`, e la stessa che ha appena superato due sigilli.

**Le altre tre restano voce aperta di `CLIP-INVENTARIO`:** i ① sono strumenti, i ③ sono
**alternative di teoria** *(archiviarle e' una scelta, non una pulizia)*, i ④ vanno
guardati **uno per uno** — e fra loro c'e' la precedenza di stamattina.

> ### 🛑 **STOP. La priorita' resta (c).**

## LE VOCI D'INDICE CHE QUESTO DOCUMENTO TOCCA

`CLIP-INVENTARIO` · `ETC-PASSO` · `ARCH-SYNC` · `ARCH-PAVIMENTI` · `A8` · `A9`
