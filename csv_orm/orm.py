import csv
import ntpath
import os
import shutil
from dataclasses import asdict, dataclass, fields, is_dataclass
from io import TextIOWrapper
from typing import Any, Generic, List, Optional, Type, TypeVar

from csv_orm.exceptions import (
    EntityCreationError,
    HeaderMismatchError,
    PrimaryKeyNotFound,
)
from csv_orm.utils import to_snake_case

T = TypeVar("T")


class CsvOrm(Generic[T]):

    path: str
    primary_key: str

    __entity: Type[T]

    @property
    def entity(self):
        return self.__entity

    def __init__(
        self,
        entity: Type[T],
        primary_key: Optional[str] = None,
        csv_path: Optional[str] = None,
    ):
        self.__entity = entity if is_dataclass(entity) else dataclass(entity)

        if not isinstance(csv_path, str):
            class_name = to_snake_case(self.entity.__name__)
            cwd = os.getcwd()
            csv_path = os.path.join(cwd, f"{class_name}.csv")

        self.path = csv_path
        self.primary_key = primary_key
        if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
            self.__create_file(csv_path)
        print(self.path)
        self.__ensure_fields()
        self.__ensure_primary_key()

    def __ensure_fields(self):
        with open(self.path, mode="r") as f:
            reader = csv.reader(f)
            csv_headers = next(reader)
        class_attributes = [f.name for f in fields(self.entity)]

        if set(csv_headers) != set(class_attributes):
            raise HeaderMismatchError(csv_headers, class_attributes)

    def __ensure_primary_key(self):
        with open(self.path, mode="r") as f:
            reader = csv.reader(f)
            fields = next(reader)

        if self.primary_key is not None:
            if self.primary_key not in fields:
                raise PrimaryKeyNotFound(self.primary_key, fields)
            return

        self.primary_key = fields[0]

    def __create_file(self, path: str):
        with open(path, mode="w", newline="") as file:
            fieldnames = [field.name for field in fields(self.entity)]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    def __writer(self, file: TextIOWrapper):
        entity = self.entity
        return csv.DictWriter(file, fieldnames=[field.name for field in fields(entity)])

    def validate(self) -> bool:
        with open(self.path, mode="r") as file:
            reader = csv.DictReader(file)
        for row in reader:
            try:
                self.entity(**row)
            except:
                return False
        return True

    def get_all(self) -> List[T]:
        instances = []
        with open(self.path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    obj = self.entity(**row)
                except Exception as e:
                    raise EntityCreationError(self.path, str(e))
                instances.append(obj)
        return instances

    def create(self, instance: Type[T]) -> T:
        with open(self.path, mode="a", newline="") as file:
            writer = self.__writer(file)
            writer.writerow(asdict(instance))
        return instance

    def get_one(self, primary_key: Any) -> Optional[T]:
        with open(self.path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if str(row[self.primary_key]) == str(primary_key):
                    return self.entity(**row)
        return None

    def update(self, uid: int, **kwargs) -> bool:
        updated = False
        records = []
        with open(self.path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row["uid"]) == uid:
                    row.update(kwargs)
                    updated = True
                records.append(row)

        if updated:
            with open(self.path, mode="w", newline="") as file:
                writer = self.__writer(file)
                writer.writeheader()
                writer.writerows(records)

        return updated

    def delete(self, uid: int) -> bool:
        deleted = False
        records = []
        with open(self.path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row["uid"]) != uid:
                    records.append(row)
                else:
                    deleted = True

        if deleted:
            with open(self.path, mode="w", newline="") as file:
                writer = self.__writer(file)
                writer.writeheader()
                writer.writerows(records)

        return deleted

    def move_to(self, new_path: str):
        directory = new_path

        if os.path.isfile(new_path):
            directory = os.path.dirname(new_path)
            new_file_path = new_path
        else:
            head, tail = ntpath.split(self.path)
            filename = tail or ntpath.basename(head)
            new_file_path = os.path.join(new_path, filename)

        os.makedirs(directory, exist_ok=True)
        try:
            shutil.move(self.path, directory)
        except Exception:
            pass
        self.path = new_file_path
