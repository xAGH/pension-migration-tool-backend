from app.schemas.person import Person
from app.scripts.move_files import move_files


def move_files_job():
    source_folder = "./files/SolicitudesEntrantes"
    destination_folder = "./files/SolicitudesEnProcesamiento"
    error_folder = "./files/ErroresSolicitudes"
    entity = Person
    primary_key = "identificacion"
    move_files(source_folder, destination_folder, entity, primary_key, error_folder)
