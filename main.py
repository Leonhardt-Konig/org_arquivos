import os
import pathlib
from shutil import move
import argparse

#valores em outro idioma por preferência pessoal.
EXT_TO_CATEGORY = {
    "png": "Images",
    "jpg": "Images",
    "jpeg": "Images",
    "webp":"Images",
    "gif": "Images",
    "mp4": "Videos",
    "mov": "Videos",
    "avi": "Videos",
    "txt": "Documents",
    "pdf": "Documents",
    "doc": "Documents",
    "docx": "Documents",
    "no_extension": "Others"
}

def analyzeDir(target, dry_run=False, nsub=False):
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
                ext = file_type[1:] if file_type else "no_extension"  # Remove o ponto primeiro '.'
                if not nsub:
                    staging.setdefault(ext.upper(), []).append(file_path)
                else:
                    category = EXT_TO_CATEGORY.get(ext, "Others")
                    staging.setdefault(category.upper(), []).append(file_path)
    except Exception as e:
        print(f"Erro: {e}")
        return

    stageFolders(staging, target, dry_run, nsub)
    stageMove(staging, target, dry_run, nsub)

def stagingAnalysis(stagingDict, file_path, file_type):
    """Análise e separação de arquivos inicial."""
    if file_type:
        category = EXT_TO_CATEGORY.get(file_type.lower(), "Others")
    else:
        category = "Others"
    stagingDict.setdefault(category, []).append(file_path)

def stageFolders(stagingDict, path, dry_run=False, nsub=False):
    """Criar pastas para cada extensão."""
    if nsub: print("Operação sem sub-diretórios.")

    for key in stagingDict:
        folder_path = os.path.join(path, key)  

        if not dry_run and nsub and not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True) 
            print(f"Diretório {folder_path} criado")

        elif not dry_run and not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True) 
            print(f"Diretório {folder_path} criado.")

        elif dry_run:
            print(f"Irá criar diretório {folder_path}.")

        else:
            print(f"Diretório {folder_path} existente.")


def stageMove(stagingDict, dir_path, dry_run=False, nsub=False):
    """Mover arquivos para pastas correspondentes."""
    for extension, files in stagingDict.items():
        target_dir = os.path.join(dir_path, extension)

        if os.path.isdir(target_dir) or dry_run:
            
            for file in files:
                print(f"Arquivo: {file} movido para: {target_dir}.")
                dest_path = os.path.join(target_dir, os.path.basename(file))
                if dry_run:
                    print(f"Irá mover {file} para {dest_path}.")
                elif nsub:
                    try:
                        move(file, dest_path)
                        print(f"Arquivo {file} movido para {dest_path}.")
                    except PermissionError:
                        print(f"Erro: Permissão negada ao mover {file}.")
                    except Exception as e:
                        print(f"Erro inesperado movendo {file}: {e}.")
                else:
                    try:
                        move(file, dest_path)
                        print(f"Arquivo {file} será movido para {dest_path}.")
                    except PermissionError:
                        print(f"Erro: Permissão negada ao mover {file}.")
                    except Exception as e:
                        print(f"Erro inesperado movendo {file}: {e}.")
        else:
            print(f"Diretório {target_dir} não é válido.")
            break


def main():
    """Recebe os argumentos da linha de comando e executa o organizador de arquivos."""
    parser = argparse.ArgumentParser(description="Organize os arquivos por extensão.")
    parser.add_argument("directory", help="Diretório para organizar os arquivos.")
    parser.add_argument("--dry-run", action="store_true", help="Simula a organização sem mover os arquivos.")
    parser.add_argument("--nsub", action="store_true", help="Realiza a organização sem criar sub-pastas por extensão.")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Erro: {args.directory} não é um diretório válido")
        return
    analyzeDir(args.directory, args.dry_run, args.nsub)

if __name__ == "__main__":
    main()



