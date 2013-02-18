import re
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

executables = [
    Executable('Sudoku.py', 'Console')
]

setup(name='Sudoku',
      version = '1.0',
      description = 'Sudoku game written with pyQt',
      options = dict(build_exe = buildOptions),
      executables = executables)
