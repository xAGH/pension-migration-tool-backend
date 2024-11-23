from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel


class Person(BaseModel):
    identificacion: str
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    genero: Literal["M", "H"]
    fecha_de_nacimiento: date
    ciudad_de_residencia: str
    ciudad_de_nacimiento: str
    semanas_cotizadas: int
    fondo_actual: str
    pre_pensionado: bool
    institucion_publica: Optional[str] = None
    numero_hijos: int
    condecoracion: bool
    tiene_hijos_inpec: bool
    tiene_familia_policia: bool
    observaciones_disciplinarias: str
