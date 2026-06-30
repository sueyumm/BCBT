import builtins
import sys

sys.path.insert(0, 'D:\\ANONYMOUS_USER\\pycharm\\BCBT\\scientific_calculation\\2DJacobiPoissonSolver')
import example as _example

for _name in dir(_example):
    if _name.startswith('_'):
        continue
    setattr(builtins, _name, getattr(_example, _name))
