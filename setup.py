"""Build Windows executable using cx_freeze.
"""

from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
includes = ["OpenGL.platform.win32", "platform", "OpenGL.arrays",
            "OpenGL.arrays.ctypesarrays", "OpenGL.arrays.numpymodule",
            "OpenGL.arrays.lists", "OpenGL.arrays.numbers",
            "OpenGL.arrays.strings"]

includefiles = ["README.txt", "LICENSE.txt", "images", "fonts"]

build_exe_options = {"packages": ["os"],
        "includes": includes,
        "excludes": ["tkinter"],
        "include_files": includefiles
        }

exe = Executable(
        script="wikigame.py",
        base="Win32GUI"
        )

setup(
        name = "WikiGame",
        version = "1.0",
        description = "Escape from Wikipedia",
        author = "Aaron Graham-Horowitz",
        options = {"build_exe": build_exe_options},
        executables = [exe]
        )
