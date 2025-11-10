import psycopg
from fastapi import HTTPException
from modelos import Cliente, Compra, Juego

# --- Clase Base para la Lógica de Clientes ---
class ClienteRepository:
    """Maneja todas las operaciones CRUD y de saldo para la entidad Cliente."""
    
    def get_cliente_saldo(self, cliente_id: int, cursor: psycopg.Cursor) -> float:
        """Obtiene el saldo del cliente, o lanza 404 y BLOQUEA LA FILA (FOR UPDATE)."""
        saldo_res = cursor.execute(
            "SELECT saldo FROM cliente WHERE cliente_id = %s FOR UPDATE", 
            (cliente_id,)
        ).fetchone()
        
        if saldo_res is None:
            raise HTTPException(status_code=404, detail=f"Cliente con ID {cliente_id} no encontrado.")
        
        return saldo_res[0]

    def postcliente(self, cliente: Cliente, cursor: psycopg.Cursor) -> str:
        cursor.execute(
            "INSERT INTO cliente (nombre, saldo) VALUES (%s, %s)", (cliente.nombre, cliente.saldo)
        )
        return "Cliente/Comprador agregado con saldo inicial."
        
    def getcliente(self, cursor: psycopg.Cursor) -> list:
        res = cursor.execute(
            "SELECT cliente_id, nombre, saldo FROM cliente"
        ).fetchall() 
        return [{"id": row[0], "nombre": row[1], "saldo": row[2]} for row in res]
    
    def getcliente_by_id(self, id: int, cursor: psycopg.Cursor):
        res = cursor.execute(
            "SELECT cliente_id, nombre, saldo FROM cliente WHERE cliente_id = %s", (id,)
        ).fetchone()
        
        if res is None:
            raise HTTPException(status_code=404, detail=f"Cliente con ID {id} no encontrado.")

        return {"id": res[0], "nombre": res[1], "saldo": res[2]}
    
    def recargar_saldo(self, id: int, monto: float, cursor: psycopg.Cursor) -> str:
        self.get_cliente_saldo(id, cursor) 
        
        cursor.execute(
            "UPDATE cliente SET saldo = saldo + %s WHERE cliente_id = %s",
            (monto, id)
        )
        return f"Saldo recargado en ${monto:.2f}. Nuevo saldo aplicado."

# --- Clase Base para la Lógica de Juegos ---
class JuegoRepository:
    """Maneja todas las operaciones relacionadas con la entidad Juego (Catálogo)."""
    
    def get_juego_info(self, juego_id: int, cursor: psycopg.Cursor) -> tuple:
        """Obtiene el precio y el título de un juego, o lanza 404."""
        res = cursor.execute(
            "SELECT precio, titulo FROM juego WHERE juego_id = %s",
            (juego_id,)
        ).fetchone()
        
        if res is None:
            raise HTTPException(status_code=404, detail=f"Juego con ID {juego_id} no encontrado en el catálogo.")
        
        return res[0], res[1]
    
    def postjuego(self, juego: Juego, cursor: psycopg.Cursor):
        # VALIDACIÓN DE UNICIDAD
        existe = cursor.execute(
            "SELECT 1 FROM juego WHERE LOWER(titulo) = LOWER(%s)",
            (juego.titulo,)
        ).fetchone()
        
        if existe:
            raise HTTPException(
                status_code=409, 
                detail=f"Error: El juego con título '{juego.titulo}' ya existe en el catálogo."
            )

        cursor.execute(
            "INSERT INTO juego (titulo, precio, genero) VALUES (%s, %s, %s)",
            (juego.titulo, juego.precio, juego.genero)
        )
        return f"Juego digital de PS3 '{juego.titulo}' agregado al catálogo"
     
    def getjuego(self, cursor: psycopg.Cursor):
        res = cursor.execute(
            "SELECT juego_id, titulo, precio, genero FROM juego"
        ).fetchall()
        return [{"juego_id": row[0], "titulo": row[1], "precio": row[2], "genero": row[3]} for row in res]	

# --- Clase Base para la Lógica de Compras (Transacciones) ---
class CompraRepository:
    """Maneja la lógica transaccional y el historial de compras."""
    
    def __init__(self):
        self.cliente_repo = ClienteRepository()
        self.juego_repo = JuegoRepository()

    def postcompra(self, compra: Compra, cursor: psycopg.Cursor) -> str:
        juego_id = compra.juego_id
        cliente_id = compra.cliente_id
        
        # 1. Obtener información y Bloquear Fila
        precio_juego, titulo_juego = self.juego_repo.get_juego_info(juego_id, cursor)
        saldo_actual = self.cliente_repo.get_cliente_saldo(cliente_id, cursor)
        
        # 2. Verificar Saldo
        if saldo_actual >= precio_juego:
            
            nuevo_saldo = saldo_actual - precio_juego
            
            # A. Descontar Saldo
            cursor.execute(
                "UPDATE cliente SET saldo = %s WHERE cliente_id = %s",
                (nuevo_saldo, cliente_id)
            )
            
            # B. Registrar Compra
            cursor.execute(
                """
                INSERT INTO compra(juego_id, cliente_id, estado, monto_pagado) 
                VALUES (%s, %s, %s, %s)
                """,
                (juego_id, cliente_id, 'COMPLETADA', precio_juego)
            )
            
            return f"Compra exitosa: '{titulo_juego}'. Saldo restante: ${nuevo_saldo:.2f}."
            
        else:
            raise HTTPException(
                status_code=400, 
                detail=f"Saldo insuficiente. Se requieren ${precio_juego:.2f}, pero solo tienes ${saldo_actual:.2f}."
            )

    def getcompra(self, cursor: psycopg.Cursor) -> list:
         res = cursor.execute("""
              SELECT j.titulo, j.precio, c.nombre 
              FROM compra co
              INNER JOIN cliente c ON co.cliente_id = c.cliente_id 
              INNER JOIN juego j ON co.juego_id = j.juego_id
             """).fetchall()
         return [{"juego": row[0], "precio": row[1], "cliente": row[2]} for row in res]
    
    def getcompra_by_cliente(self, id: int, cursor: psycopg.Cursor) -> list:
        self.cliente_repo.get_cliente_saldo(id, cursor) 
        
        res = cursor.execute ("""
            SELECT j.titulo , j.precio
            FROM compra co
            INNER JOIN cliente c ON co.cliente_id = c.cliente_id
            INNER JOIN juego j ON co.juego_id = j.juego_id
            WHERE c.cliente_id = %s""", (id,)).fetchall()
        
        return [{"juego": row[0], "precio": row[1]} for row in res]