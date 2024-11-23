from pydantic import BaseModel


class BlackList(BaseModel):
    identificacion: str
    fecha_ingreso: str
