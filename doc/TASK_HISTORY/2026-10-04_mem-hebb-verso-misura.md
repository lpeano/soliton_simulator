# `MEM-HEBB-VERSO`, passo (1) — **DECISIONE REGISTRATA E MISURA**

## STATO: NON INIZIATO - in coda dopo TETTO-CAUSALE passo (1)

*(Messo al sicuro nel repo su ordine di Luca del 2026-10-04, fine serata. **Nessun lavoro e'
stato fatto su questo mandato.** Il passo (1) di `TETTO-CAUSALE` e' chiuso col referto
`doc/REFERTO_tetto_causale_tempo_2026-10-04.md`, in `eeb54be`.)*

> ### ⛔ **LA SEZIONE `LA STELLA POLARE` NON E' QUI, E NON PER DIMENTICANZA:** si scrive
> **quando il lavoro parte**, non ora. ### **Scritta adesso sarebbe una risposta data prima
> di aver letto il codice, cioe' esattamente la ricostruzione che il par.8 esiste per
> impedire.**

> ### ⚠ **E IL TESTO QUI SOTTO E' COPIATO PAROLA PER PAROLA dalla conversazione, come Luca
> ha chiesto: non e' riassunto ne' riformulato.** Se una riga sembra ambigua, l'ambiguita' e'
> **nell'originale** e va risolta con Luca, non da me.

---

## IL MANDATO, verbatim

MANDATO: MEM-HEBB-VERSO, PASSO (1): DECISIONE REGISTRATA E MISURA. Il simulatore 0f060670 NON si tocca. Congelamento dell'infrastruttura (decisione di Luca, 2026-10-04): niente presidi, riordini o censimenti di igiene, salvo un difetto che falsi QUESTA misura. Se il mandato TETTO-CAUSALE passo (1) e' in coda prima di questo, fallo prima: sono due commit separati, in ordine.

DECISIONI DI LUCA (2026-10-04), da registrare in doc/INDICE_ID.tsv e nel task history. Le decisioni sono sue: non reinterpretarle. doc/ASSIOMI.md non si tocca.
(1) d0 (memoria_hebbiana_moto, :9035-9037 su 0f060670). Oggi proj = media(m_i*I_i, m_j*I_j)/Imed . dir(i->j): cambia segno invertendo il verso dell'arco, e una traslazione rigida cambia d0. FORMA DECISA: moto relativo, con peso d'arco:
    proj = 0.5*(I_i+I_j)/Imed * (m_j - m_i) . dir(i->j)
  E' invariante per scambio i<->j, nulla per traslazione rigida (tutte le m uguali), positiva se i nodi si allontanano. Il peso e' sull'ARCO, non sul nodo: con il peso per nodo, la traslazione rigida di masse diverse NON da' zero.
(2) Fase (:9409-9434). Tre difetti: solo l'estremo ii riceve; phi[ii]=... con indici ripetuti tiene l'ULTIMA scrittura; dir_laterale = (-y, x, 0) privilegia l'asse z del laboratorio, mentre i nodi stanno in 3D (:4843). DECISIONE: il sito si SPEGNE con un flag proprio (MEM_MOTO_TUTTO e MEM_MOTO restano come sono). Si apre la voce nuova FASE-TRASCINAMENTO-3D (aperta, difetto): serve un asse fisico locale al posto di z. E' legge nuova, non riparazione.

LA MISURA, sulla scena del driver (nmasse e sep dall'argv), seme 11, 72 e 150 passi, sul blob di oggi. Calcola le grandezze nuove a lato, senza scriverle:
(a) d0, forma vecchia contro forma decisa, su ogni arco e a ogni passo: distribuzione di |proj| prima del taglio (min, mediana, p99, max); frazione di archi SATURI al taglio passo_max = 0.01*mediana(d0) (:9050), per ciascuna forma; frazione di archi in cui il segno cambia fra le due forme; somma con segno di Delta d0 per passo, per ciascuna forma.
(b) Fase: nodi con piu' di un arco come primo estremo; contributi scartati da "l'ultimo vince" (numero e somma dei moduli scartati contro quella applicata); distribuzione di |shift|; frazione saturata dal taglio pi/4.
(c) Dichiara, dall'AST, se nella configurazione del driver il sito (2) gira davvero (MEM_MOTO_TUTTO e i gate a :9391/:9393).
CONTROLLI CHE POSSONO FALLIRE, da fissare e committare PRIMA di girare:
 - la tua forma vecchia, ricalcolata a lato, coincide AL BIT con il proj del simulatore, dopo il taglio, su ogni arco. Se no, misuri un'altra cosa: FERMATI;
 - forma decisa con mem_mot sostituita da un vettore costante (traslazione rigida): proj = 0 esatto su ogni arco. La forma vecchia sullo stesso ingresso deve dare un proj NON nullo. Se la vecchia da' zero, il caso non discrimina: FERMATI;
 - scambio i<->j su tutti gli archi: la forma decisa e' identica al bit, la vecchia cambia segno.
Solo numeri, nessun PASSA/FALLISCE fuori dai controlli. Dichiara la piattaforma.

Prima di girare: task history con LA STELLA POLARE (le cinque risposte) per la cura decisa, scritta ORA e non dopo. Nel task history scrivi anche i criteri del sigillo della cura, per i commit successivi:
 - (1): braccio 0; caso che DEVE fallire = traslazione rigida (vecchia != 0, nuova == 0); scambio del verso degli archi: identita' al bit della nuova legge;
 - (2): con il flag nuovo ACCESO, identita' al byte con il blob di oggi; con il flag spento, le differenze devono stare solo in phi e a valle.
Commit: strumento prima di girare, referto dopo, con i blob citati.

NON CHIUDERE IL TURNO A META': ti fermi solo con "FERMO: <motivo>" su un controllo fallito o su una decisione di Luca. Chiudi con "PUSHATO: <hash>". STOP.

---

## CHE COSA MANCA, PRIMA CHE QUESTO LAVORO POSSA PARTIRE

*(Nessuna di queste righe interpreta il mandato: sono **cose da fare** che il mandato stesso
elenca, messe in ordine perche' alla ripresa non si debba ri-leggerlo per capire da dove
cominciare.)*

1. **`LA STELLA POLARE`**, le cinque risposte per la cura decisa — **prima** di girare;
2. i **criteri del sigillo** per i commit successivi, come il mandato li detta;
3. le **due decisioni di Luca** registrate in `doc/INDICE_ID.tsv` e nel task history;
4. la **voce nuova `FASE-TRASCINAMENTO-3D`** *(aperta, difetto)*;
5. il **flag proprio** per spegnere il sito (2) — *decisione di Luca: `MEM_MOTO_TUTTO` e
   `MEM_MOTO` restano come sono*;
6. i **tre controlli che possono fallire**, fissati e **committati PRIMA di girare**;
7. lo **strumento** prima di girare, il **referto** dopo, **coi blob citati**.

### ⚠ **E UNA COSA CHE IL MANDATO DICE E CHE VA LETTA DUE VOLTE:** *«Le decisioni sono sue:
non reinterpretarle»*, e *«`doc/ASSIOMI.md` non si tocca»*.
### **Quindi la forma di `proj` NON si discute: si registra e si misura.**
