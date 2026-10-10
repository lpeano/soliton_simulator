r"""**L'ARCHIVIO FREDDO SU `E:` — si COPIA, si VERIFICA, e solo allora si cancella.**

**Decisione di Luca, 2026-10-10:** *«SPOSTA SU `E:` (non cancellare) gli output RIGENERABILI e
NON TRACCIATI da git: i `.pkl`, `.gz` e `.npz` dentro `csv/` (e quelli di `db/` non tracciati).
Destinazione: `E:\archivio_soliton\2026-10-10\` con lo STESSO percorso relativo del repo. Prima
di cancellare l'originale: copia, verifica sha1 della copia contro l'originale, e solo se
coincide cancella l'originale. […] Se un file e' TRACCIATO da git, NON lo tocchi. Se `E:` non e'
collegato a meta' lavoro: ti fermi, niente a meta'.»*

> ## ⛔ **L'ORDINE DELLE TRE OPERAZIONI E' LA GARANZIA, non la prudenza.**
> **copia → `sha1` della COPIA contro l'ORIGINALE → e SOLO SE COINCIDE si cancella.**
> ### ⚠ **Un file per volta**, cosi' un'interruzione a meta' lascia **ogni singolo file in uno
> dei due stati buoni**: o nel repo, o su `E:` verificato. ### **Mai in nessuno dei due.**

**E CHI E' TRACCIATO NON SI TOCCA:** l'insieme dei tracciati esce da **`git ls-files`**, non dal
`.gitignore` — ### **<<ignorato>> e <<non tracciato>> sono due cose diverse**, e quella che conta
qui e' **la seconda**.

**NESSUN RUN, nessun simulatore.**
"""
# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Copia byte e confronta sha1.
import hashlib
import io
import os
import shutil
import subprocess
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
NL = chr(10)
MB = 1048576.0
GB = 1073741824.0

# ### ⛔ **LE TRE ESTENSIONI, DICHIARATE** -- e non <<tutto cio- che e- grosso>>: sono
# ### ### **le uscite dei run**, e `CLAUDE.md` par. `6` dice che ### **il dato E- il comando
# ### che lo produce.**
ESTENSIONI = (".pkl", ".gz", ".npz")
# ### ⚠ **E LE DUE RADICI, DICHIARATE:** `csv/` e `db/`. ### **`doc/` non c-e-**, e non e-
# ### una dimenticanza: la- i file ### **sono il lavoro**, non il suo scarto.
RADICI = ("csv", "db")

DESTINAZIONE = os.path.join("E:" + os.sep, "archivio_soliton", "2026-10-10")
MANIFEST = os.path.join(RADICE, "doc", "ARCHIVIO_E_2026-10-10.tsv")


def sha1(p):
    """### `sha1` dei ### **byte grezzi**, a blocchi: i file arrivano a `53` MB."""
    h = hashlib.sha1()
    with io.open(p, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def tracciati():
    """### L-insieme dei percorsi ### **TRACCIATI**, da `git ls-files`."""
    r = subprocess.run(["git", "ls-files"], cwd=RADICE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return set(x.strip().replace("/", os.sep) for x in (r.stdout or "").split(NL)
               if x.strip())


def candidati():
    """### `[(rel, byte)]` ordinati, ### **solo i NON tracciati.**"""
    tr = tracciati()
    fuori, saltati = [], []
    for base in RADICI:
        for qui, _sub, nomi in os.walk(os.path.join(RADICE, base)):
            for nm in nomi:
                if not nm.endswith(ESTENSIONI):
                    continue
                f = os.path.join(qui, nm)
                rel = os.path.relpath(f, RADICE)
                if rel in tr:
                    saltati.append(rel)
                    continue
                try:
                    fuori.append((rel, os.path.getsize(f)))
                except OSError:
                    continue
    return sorted(fuori), sorted(saltati)


def _liberi(dove):
    try:
        return shutil.disk_usage(dove).free
    except Exception:
        return -1


def esegui(prova=True):
    lista, saltati = candidati()
    tot = sum(s for _r, s in lista)
    c_prima = _liberi(RADICE)
    e_prima = _liberi("E:" + os.sep)

    print("=" * 100)
    print("L-ARCHIVIO FREDDO SU E:   --   %s" % ("PROVA (non scrive niente)" if prova
                                                 else "ESECUZIONE"))
    print("=" * 100)
    print("  da spostare: %d file, %.2f GB" % (len(lista), tot / GB))
    print("  TRACCIATI, quindi NON toccati: %d" % len(saltati))
    print("  C: liberi prima: %.2f GB      E: liberi prima: %.2f GB"
          % (c_prima / GB, e_prima / GB))
    print("  destinazione: %s" % DESTINAZIONE)
    print("-" * 100)

    if not lista:
        print("  ### NIENTE DA SPOSTARE")
        return 0

    # ### ⛔ **SI CONTROLLA LO SPAZIO PRIMA DI COMINCIARE:** <<niente a meta->> vuol dire
    # ### ### **non partire**, non <<accorgersene a meta->>.
    if e_prima >= 0 and e_prima < tot * 1.05:
        print("  ### \u26d4 FERMO: su E: ci sono %.2f GB e servono %.2f GB"
              % (e_prima / GB, tot * 1.05 / GB))
        return 1

    if prova:
        print("  i primi 5, per vedere la forma:")
        for rel, s in lista[:5]:
            print("     %8.1f MB  %s" % (s / MB, rel.replace(os.sep, "/")))
        print("  ### PROVA: non ho scritto niente. Per farlo: --esegui")
        return 0

    righe, fatti, byte = [], 0, 0
    t0 = time.perf_counter()
    for rel, s in lista:
        src = os.path.join(RADICE, rel)
        dst = os.path.join(DESTINAZIONE, rel)
        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            h = sha1(src)
            # ### ⚠ **SE LA DESTINAZIONE C-E- GIA-, non si sovrascrive alla cieca:** si
            # ### confronta, e ### **se differisce SI FERMA.**
            if os.path.exists(dst):
                if sha1(dst) != h:
                    print("  ### \u26d4 FERMO su %s: la copia su E: ESISTE e DIFFERISCE"
                          % rel.replace(os.sep, "/"))
                    break
            else:
                shutil.copy2(src, dst)
            hc = sha1(dst)
            if hc != h:
                print("  ### \u26d4 FERMO su %s: sha1 DIVERSO (%s contro %s)"
                      % (rel.replace(os.sep, "/"), hc[:12], h[:12]))
                break
            os.remove(src)
            righe.append((rel.replace(os.sep, "/"), dst, s, h))
            fatti += 1
            byte += s
            if fatti % 25 == 0:
                print("     %d/%d   %.2f GB   %.0f s"
                      % (fatti, len(lista), byte / GB, time.perf_counter() - t0))
        except Exception as e:
            print("  ### \u26d4 FERMO su %s: %s" % (rel.replace(os.sep, "/"), e))
            break

    # ### ✅ **IL MANIFEST SI SCRIVE ANCHE SE CI SI E- FERMATI:** quello che e- stato
    # ### spostato ### **va scritto**, altrimenti sarebbe irrintracciabile.
    testa = [
        "# CONGELATO -- questo e- un REPERTO: la fotografia di una operazione IRREVERSIBILE,",
        "# fatta il 2026-10-10. Generato da `python csv/_archivia_su_e.py --esegui`.",
        "# Ogni riga: il file e- STATO SPOSTATO, e lo sha1 e- quello VERIFICATO sulla copia.",
        "percorso_nel_repo\tpercorso_su_E\tbyte\tsha1",
    ]
    corpo = ["%s\t%s\t%d\t%s" % r for r in righe]
    dati = (NL.join(testa + corpo) + NL).encode("utf-8")
    io.open(MANIFEST, "wb").write(dati)

    c_dopo = _liberi(RADICE)
    print("-" * 100)
    print("  SPOSTATI: %d file su %d, %.2f GB, in %.0f s"
          % (fatti, len(lista), byte / GB, time.perf_counter() - t0))
    print("  C: liberi PRIMA %.2f GB   ->   DOPO %.2f GB   (guadagnati %.2f GB)"
          % (c_prima / GB, c_dopo / GB, (c_dopo - c_prima) / GB))
    print("  manifest: %s (%d righe)"
          % (os.path.relpath(MANIFEST, RADICE).replace(os.sep, "/"), len(righe)))
    print("=" * 100)
    return 0 if fatti == len(lista) else 1


if __name__ == "__main__":
    sys.exit(esegui(prova="--esegui" not in sys.argv))
