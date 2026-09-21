import os, sys
os.chdir('C:\\Users\\lpeano\\soliton_simulator')
sys.path.insert(0, 'C:\\Users\\lpeano\\soliton_simulator')
sys.argv = ['soliton_simulator.py', '--test', 'N-MASSE', '--nmasse', '3', '--sep', '4.0', '--giri', '0', '--campo-spinoriale', '--spinore-vivo', '--spinore-corretto', '--chi-core', '--calore-scal', '--deparam-orologio', '--verlet', '--fork-su2', '--fork-su2-mem', '--cs-dinamico', '--tau-luce', '--rumore-colorato', '--pav-com', '--guscio-morbido', '--zeta-vir', '--chi-basc', '--chi-coop', '--scala-min', '--coes-adim', '--plast-din', '--viriale', '--olon-part']
import soliton_simulator as S
S.FERMA_DOPO_NSUB = True
a = S._cli(); S._applica_regime(a); S._applica_flag(a)
S._NMASSE_VIDEO['n'] = 3; S._NMASSE_VIDEO['sep'] = 4.0
S._NMASSE_VIDEO['size'] = None
S.avvia_test('N-MASSE')()
try:
    S.net.step()
except S.StopDopoNsub as e:
    d = S.net._g_nsub_stop
    print('STOP ok nsub=%d n1=%.0f ramo=%s msg=%s'
          % (d['nsub'], d['n1'], d['ramo'], e))
    raise SystemExit(0)
print('STOP NON ALZATO')
raise SystemExit(1)
