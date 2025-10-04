import os
import pathlib
from shutil import move
import argparse

#valores em outro idioma por preferência pessoal.
EXT_TO_CATEGORY = {
    ".png": "Bild",
    ".jpg": "Bild",
    ".jpeg": "Bild",
    ".gif": "Bild",
    ".mp4": "Videos",
    ".mov": "Videos",
    ".avi": "Videos",
    ".txt": "Unterlagen",
    ".pdf": "Unterlagen",
    ".doc": "Unterlagen",
    ".docx": "Unterlagen",
    "no_extension": "Sonstige"
}

def analyzeDir(target, dry_run=False):
    """Função base para a análise de diretórios."""
    staging = {}  # Dicionário Local
    try:
        for root, _, files in os.walk(target):
            for file in files:
                if file.startswith("."):  # Ignore arquivos ocultos
                    continue
                file_path = os.path.join(root, file)
                file_type = pathlib.Path(file_path).suffix.lower()
                # Lidar Com Extensões Vazias 
                ext = file_type[1:] if file_type else "no_extension"  # Remove o ponto '.'
                staging.setdefault(ext.upper(), []).append(file_path)
    except Exception as e:
        print(f"Erro: {e}")
        return
