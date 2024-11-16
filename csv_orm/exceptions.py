from typing import List


class HeaderMismatchError(Exception):
    def __init__(self, csv_headers: List[str], class_attributes: List[str]):
        message = f"The CSV headers ({csv_headers}) mismatch with the class attributes({class_attributes})."
        super().__init__(message)


class PrimaryKeyNotFound(Exception):
    def __init__(self, primary_key: str, fields: List[str]):
        message = f"The specified primary key({primary_key}) is not in the CSV headers ({fields})"
        super().__init__(message)


class EntityCreationError(Exception):
    def __init__(self, path: str, original_exc: str):
        message = f"The creation of entity in the file {path} failed.\nException: {original_exc}"
        super().__init__(message)
