import os
import tarfile
from datetime import datetime

def excluir_venvs(tar, directorio_raiz):
    for root, dirs, files in os.walk(directorio_raiz):
        # Evitar ingresar en carpetas .venv
        if '.venv' in dirs:
            dirs.remove('.venv')  # no descender en .venv

        for file in files:
            ruta_completa = os.path.join(root, file)
            ruta_relativa = os.path.relpath(ruta_completa, directorio_raiz)
            tar.add(ruta_completa, arcname=ruta_relativa)
            print(f"Añadiendo: {ruta_relativa}")

if __name__ == "__main__":
    directorio_raiz = '.'  # Directorio base
    nombre_archivo = f"backup_sin_venv_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"

    with tarfile.open(nombre_archivo, "w:gz") as tar:
        excluir_venvs(tar, directorio_raiz)

    print(f"\n✅ Backup creado sin .venv: {nombre_archivo}")
