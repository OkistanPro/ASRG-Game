import sys
from cx_Freeze import setup, Executable

# Les dépendances sont automatiquement détectées, mais il peut être nécessaire de les ajuster.
build_exe_options = {
    "excludes": ["tkinter", "unittest"],
    "zip_include_packages": ["encodings", "PySide6"],
    "include_files" : ["fonts", "images", "levelfiles", "music"]
}

# base="Win32GUI" devrait être utilisé uniquement avec l’app Windows GUI 
base = "Win32GUI" if sys.platform == "win32" else "gui"

setup(
    name="A Simple Rhythm Game",
    version="0.1",
    description="Jeu de rythme - Projet CMI L1 2024",
    options={"build_exe": build_exe_options},
    executables=[Executable(
        "mainloop.py", 
        base=base,
        target_name="asrg",
        icon="logo.ico")],
)