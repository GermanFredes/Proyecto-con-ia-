from pydantic import BaseModel, Field 

class Cliente(BaseModel):
	nombre: str
	saldo: float = Field(default=0.0, ge=0, description="Saldo del monedero. Debe ser positivo.")

class Compra(BaseModel):
	juego_id: int = Field(ge=1)
	cliente_id: int = Field(ge=1)
	
class Juego(BaseModel):
	titulo: str 
	precio: float = Field(gt=0, description="Precio del juego. Debe ser mayor que cero.")
	genero: str = None