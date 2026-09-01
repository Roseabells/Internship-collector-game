import os
import sys
from types import ModuleType

from pgzero.runner import prepare_mod, run_mod

GAME_FILE = "beta.py"

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), GAME_FILE)

with open(path) as f:
    src = f.read()

code = compile(src, os.path.basename(path), 'exec', dont_inherit=True)

name, _ = os.path.splitext(os.path.basename(path))
mod = ModuleType(name)
mod.__file__ = path
mod.__name__ = name
sys.modules[name] = mod

sys._pgzrun = True

prepare_mod(mod)
exec(code, mod.__dict__)
run_mod(mod)