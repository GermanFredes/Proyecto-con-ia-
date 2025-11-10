from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import clientes, catalogo, compras 

app = FastAPI(
    title="PS3 Digital Store API",
    description="API para la compra digital de juegos de PS3, con lógica transaccional y Repositorios.",
)

# --- Configuración Global: CORS ---
origins = ["*"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     
    allow_methods=["*"],       
    allow_headers=["*"],       
    allow_credentials=True,    
)

# --- Montaje de Routers ---
app.include_router(clientes.router)
app.include_router(catalogo.router)
app.include_router(compras.router)