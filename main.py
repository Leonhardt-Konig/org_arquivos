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

    stageFolders(staging, target, dry_run)
    

def stagingAnalysis(stagingDict, file_path, file_type):
    """Análise e separação de arquivos inicial."""
    if file_type:
        category = EXT_TO_CATEGORY.get(file_type.lower(), "Sonstige")
    else:
        category = "Sonstige"
    stagingDict.setdefault(category, []).append(file_path)

def stageFolders(stagingDict, path, dry_run=False):
    """Criar pastas para cada extensão."""
    for key in stagingDict:
        folder_path = os.path.join(path, key)  
        if not dry_run and not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True) 
            print(f"Diretório {folder_path} criado")
        elif dry_run:
            print(f"Irá criar diretório {folder_path}")
        else:
            print(f"Diretório {folder_path} existente")
def main():
    """Recebe os argumentos da linha de comando e executa o organizador de arquivos."""
    parser = argparse.ArgumentParser(description="Organize os arquivos por extensão.")
    parser.add_argument("directory", help="Diretório para organizar os arquivos.")
    parser.add_argument("--dry-run", action="store_true", help="Simula a organização sem mover os arquivos.")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Erro: {args.directory} não é um diretório válido")
        return
    analyzeDir(args.directory, args.dry_run)