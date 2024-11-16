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
    for csv in os.listdir(source_folder):
        source_path = os.path.join(source_folder, csv)
        orm = CsvOrm(entity, primary_key, csv)
        has_error_folder = isinstance(error_folder, str)
        valid = orm.validate()

        if not valid and not has_error_folder:
            return False

        folder = destination_folder if valid else error_folder
        dest = os.path.join(folder, csv)

        if os.path.isfile(source_path):
            shutil.move(source_path, dest)

        return True
