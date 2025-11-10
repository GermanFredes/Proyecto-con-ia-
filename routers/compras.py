from fastapi import APIRouter, Depends
import psycopg
from modelos import Compra 
from manager import CompraRepository
from database import getCursor

router = APIRouter(
    prefix="/compra",
    tags=["Transacciones Digitales"]
)

compra_repo = CompraRepository()

@router.post("/finalizar")
def finalizar_compra(compra: Compra, cursor: psycopg.Cursor = Depends(getCursor)):
    res=compra_repo.postcompra(compra, cursor)
    return {"msg": res}

@router.get("/todas")
def ver_compras(cursor: psycopg.Cursor = Depends(getCursor)):
    res = compra_repo.getcompra(cursor)
    return res

@router.get("/{cliente_id}/biblioteca")
def ver_biblioteca_por_cliente(cliente_id: int, cursor: psycopg.Cursor = Depends(getCursor)):
    res = compra_repo.getcompra_by_cliente(cliente_id,cursor)
    return res