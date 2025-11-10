from fastapi import APIRouter, Depends, HTTPException, Header
import psycopg
from modelos import Juego 
from manager import JuegoRepository
from database import getCursor

router = APIRouter(
    prefix="/catalogo",
    tags=["Juegos Digitales"]
)

juego_repo = JuegoRepository()

# --- CLAVE SECRETA DE ADMINISTRACIÓN ---
ADMIN_API_KEY = "TOKEN_SECRETO_ADMIN123" 

# --- FUNCIÓN DE DEPENDENCIA DE SEGURIDAD ---
async def verificar_api_key(x_api_key: str = Header(..., description="Clave de administrador requerida")):
    """Verifica si el token proporcionado en el encabezado X-API-Key es válido."""
    if x_api_key != ADMIN_API_KEY:
        # Retorna 401 Unauthorized si la clave no coincide
        raise HTTPException(
            status_code=401,
            detail="Acceso no autorizado. Token de API de administración inválido."
        )
    return x_api_key

# --- ENDPOINT PROTEGIDO con Depends(verificar_api_key) ---
@router.post("/agregar_juego")
def agregar_juego(
    juego: Juego, 
    cursor: psycopg.Cursor = Depends(getCursor),
    # Aplica la dependencia para forzar la verificación del token
    admin_key: str = Depends(verificar_api_key) 
):
    res = juego_repo.postjuego(juego, cursor)
    return {"msg": res}

@router.get("/juegos")
def ver_juegos(cursor: psycopg.Cursor = Depends(getCursor)):
    res = juego_repo.getjuego(cursor)
    return res