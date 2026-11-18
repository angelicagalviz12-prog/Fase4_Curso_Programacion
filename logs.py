# Importo las herramientas necesarias para configurar el registro de eventos.
import logging
from pathlib import Path

# Defino la ubicación de la carpeta donde guardaré los registros.
CARPETA_LOGS = Path(__file__).parent / "registros"

# Creo la carpeta de registros si todavía no existe.
CARPETA_LOGS.mkdir(exist_ok=True)

# Defino la ubicación del archivo de registro.
ARCHIVO_LOGS = CARPETA_LOGS / "sistema.log"

# Configuro el registro general de eventos del sistema.
def configurar_logs():
    
    # Establezco el formato de los mensajes de registro.
    formato = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    
    # Configuro el registro en archivo y en consola.
    logging.basicConfig(
        level=logging.INFO,
        format=formato,
        handlers=[
            logging.FileHandler(ARCHIVO_LOGS, encoding="utf-8"),
            logging.StreamHandler()
        ],
        force=True)

    # Registro el inicio de la configuración.
    logging.getLogger(__name__).info("Configuración de registros iniciada correctamente.")


# Obtengo un registrador para utilizarlo en otros módulos.
def obtener_logger(nombre):

    # Devuelvo el registrador correspondiente al módulo.
    return logging.getLogger(nombre)
