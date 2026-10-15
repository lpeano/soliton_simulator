# LA PROVA CHE IL PRESIDIO FERMA UN COMMIT VERO -- 2026-10-15

## COME E' STATA FATTA

Su un ramo USA-E-GETTA (`prova-presidio-tp`, poi buttato), partendo da `8bf0ded`:
rimesso il Grover dello spinore A TICK FISSO (tre righe marcate `PROVA DEL PRESIDIO`
in `primo_ordine/motore.py`), `git add -A`, e `git commit`.

## IL RISULTATO

    IL COMMIT E' TORNATO: 1
    E HEAD E' RIMASTO 8bf0ded, cioe' IL COMMIT NON E' ATTERRATO.

E non e' lo script che torna 1: e' IL COMMIT che non si fa. La differenza e' tutta,
ed e' l'errore che avevo fatto il 15 ottobre -- avevo misurato che lo script torna 1
e avevo scritto che fermava un commit, mentre il collaudo NON ERA NEL HOOK.

## IL PEZZO DECISIVO DELL'OUTPUT DEL HOOK

```
    LO SCHEMA DELLA CAMMINATA: 25 su 25   ### TUTTI PASSATI
    ====================================================================================================
    [TIMBRO] _collauda_tempo_proprio.py  sha1-BYTE 037a71f3  committato e pulito
    ================================================================================================
    IL CONTROLLO DEL TEMPO PROPRIO: quali pezzi EVOLVONO COL TICK invece che col dtau
    ================================================================================================
      CAMM-SATURAZIONE           frazione 0.5   |psi(dtau) - psi(dtau/2)| = 9.871e-02   dipende dal tempo proprio
      CAMM-MONETA-SPIN           frazione 0.5   |psi(dtau) - psi(dtau/2)| = 1.591e-01   dipende dal tempo proprio
      CAMM-GROVER                frazione 0.5   |psi(dtau) - psi(dtau/2)| = 0.000e+00   ### IGNORA dtau: VIOLA `TEMPO-PROPRIO-LOCALE`
      CAMM-SPOSTAMENTO           frazione 0.5   |psi(dtau) - psi(dtau/2)| = 5.095e-01   dipende dal tempo proprio
      CAMM-GROVER-VUOTO          frazione 0.5   |psi(dtau) - psi(dtau/2)| = 6.255e-01   dipende dal tempo proprio
      CAMM-SPOSTAMENTO-VUOTO     frazione 0.5   |psi(dtau) - psi(dtau/2)| = 6.236e-01   dipende dal tempo proprio
      CAMM-SPOSTAMENTO-VUOTO     frazione 0.5   |psi(dtau) - psi(dtau/2)| = 6.236e-01   dipende dal tempo proprio
      CAMM-GROVER-VUOTO          frazione 0.5   |psi(dtau) - psi(dtau/2)| = 6.255e-01   dipende dal tempo proprio
      CAMM-SPOSTAMENTO           frazione 0.5   |psi(dtau) - psi(dtau/2)| = 5.095e-01   dipende dal tempo proprio
      CAMM-GROVER                frazione 0.5   |psi(dtau) - psi(dtau/2)| = 0.000e+00   ### IGNORA dtau: VIOLA `TEMPO-PROPRIO-LOCALE`
      CAMM-MONETA-SPIN           frazione 0.5   |psi(dtau) - psi(dtau/2)| = 1.591e-01   dipende dal tempo proprio
      CAMM-SATURAZIONE           frazione 0.5   |psi(dtau) - psi(dtau/2)| = 9.871e-02   dipende dal tempo proprio
    ------------------------------------------------------------------------------------------------
      ### (1) i violatori sono ESATTAMENTE quelli attesi       ### FALLISCE   visti ('CAMM-GROVER',)
      ### (2) DEVE DIPENDERE: la moneta di spin e la saturazio PASSA   senza questo il braccio (1) passerebbe anche con TUTTO fermo
      ### (3) e sono 0 violatori su 12 pezzi, tutti guardati   ### FALLISCE   1 violatori su 12 pezzi, e 12 pezzi guardati
    ================================================================================================
      1 su 3
    ### ✅ E IL CENSIMENTO DICE CHE ZERO PEZZI VIOLANO `TEMPO-PROPRIO-LOCALE`:
    ###   la strada (B) e' stata fatta il 2026-10-15, e questo file da CRITERIO
    ###   DI ACCETTAZIONE e' diventato UN PRESIDIO: un pezzo che tornasse a
    ###   evolvere col tick FA FALLIRE il pre-commit, e la prova che fallisce
    ###   davvero e' stata fatta rimettendo un pezzo a tick fisso.
    ================================================================================================
```

## E POI LA PROVA E' STATA TOLTA

Il ramo e' stato cancellato (`git branch -D prova-presidio-tp`) e `motore.py` non
contiene nessuna traccia di `PROVA DEL PRESIDIO`: il collaudo, sul ramo vero, torna 0.
