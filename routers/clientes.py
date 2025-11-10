from fastapi import APIRouter, Depends , HTTPException
import psycopg
from modelos import Cliente 
from manager import ClienteRepository
from database import getCursor


router = APIRouter(
    prefix="/cliente",
    tags=["Clientes (Compradores)"]
)

cliente_repo = ClienteRepository()

@router.post("/registrar")
def agregar_cliente(cliente: Cliente, cursor: psycopg.Cursor = Depends(getCursor)):
    res = cliente_repo.postcliente(cliente, cursor)
    return {"msg" : res}

@router.get("/todos")
def ver_cliente(cursor: psycopg.Cursor = Depends(getCursor)):
    res = cliente_repo.getcliente(cursor)
    return res

@router.get("/{cliente_id}")
def getclienteporid(cliente_id: int, cursor: psycopg.Cursor = Depends(getCursor)):
    res = cliente_repo.getcliente_by_id(cliente_id, cursor) 
    return res

@router.post("/recargar_saldo/{cliente_id}")
def recargar_saldo(cliente_id: int, monto: float, cursor: psycopg.Cursor = Depends(getCursor)):
    if monto <= 0:
        raise HTTPException(status_code=400, detail="El monto de recarga debe ser positivo.")
        
    res = cliente_repo.recargar_saldo(cliente_id, monto, cursor)
    return {"msg": res}

@router.put("/actualizar/{cliente_id}")
def actualizarCliente(cliente_id: int, actualizarCliente: Cliente, cursor: psycopg.Cursor = Depends(getCursor)):
    return {"msg": "Funcionalidad PUT pendiente de implementación en ClienteRepository."}

@router.delete("/eliminar/{cliente_id}")
def eliminarcliente(cliente_id: int, cursor: psycopg.Cursor = Depends(getCursor)):
    return {"msg": "Funcionalidad DELETE pendiente de implementación en ClienteRepository."}