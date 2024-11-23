import os
import shutil
from typing import Optional, Type, TypeVar

from csv_orm.orm import CsvOrm

T = TypeVar("T")


def move_files(
    source_folder: str,
    destination_folder: str,
    entity: Type[T],
    primary_key: str,
    error_folder: Optional[str] = None,
) -> bool:
    path = os.path.abspath(source_folder)

    for csv in os.listdir(source_folder):
        path = os.path.abspath(os.path.join(source_folder, csv))
        orm = CsvOrm(entity, primary_key, path)
        has_error_folder = isinstance(error_folder, str)
        valid = orm.validate()

        if not valid and not has_error_folder:
            return False

        folder = destination_folder if valid else error_folder
        dest = os.path.abspath(os.path.join(folder, csv))
        print(path)
        print(dest)
        if os.path.isfile(path):
            shutil.move(source_folder, dest)
