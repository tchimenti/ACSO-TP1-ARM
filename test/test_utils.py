from parse_dumpsim import parse_dumpsim
from pathlib import Path

def get_name_test(type_of_test):
    # Configura tu ruta aquí
    ruta_carpeta = Path(f'inputs/asm')
    if type_of_test == "extra":
        ruta_carpeta = Path(f'inputs/extra_asm')
    if type_of_test == "custom":
        ruta_carpeta = Path(f'inputs/custom_asm')
    # Verificamos si la carpeta existe para evitar errores
    if ruta_carpeta.is_dir():
        # Listamos solo archivos
        return [archivo.stem for archivo in ruta_carpeta.iterdir() if archivo.is_file()]
        
    else:
        print("La ruta especificada no es una carpeta válida.")
        return []

def build_testdata(type_of_test):
    tests_names = get_name_test(type_of_test)
    result = []
    for test in tests_names:
       result.append(
           (parse_dumpsim(f'{type_of_test}_dumpsim/dumpsim_ref_{test}'),
            parse_dumpsim(f'{type_of_test}_dumpsim/dumpsim_user_{test}')
           )
       )
    return result, tests_names
