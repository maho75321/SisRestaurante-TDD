from dao.conexion import DBConnection
from entidades.plato import Plato
import mysql.connector


class PlatoDAO:
    """DAO para la entidad Plato."""

    def guardar(self, plato: Plato) -> int:
        conn = DBConnection.get_connection()
        if not conn:
            return -1

        cursor = conn.cursor()
        sql = "INSERT INTO plato (nombre, descripcion, precio) VALUES (%s, %s, %s)"

        try:
            cursor.execute(
                sql,
                (plato.nombre, plato.descripcion, plato.precio)
            )

            conn.commit()
            plato.id = cursor.lastrowid
            return plato.id

        # ===== CAMBIO GUIA TDD =====
        # Se corrige captura de excepción MySQL.
        except mysql.connector.Error:
            return -1
        # ===== FIN CAMBIO =====

        finally:
            cursor.close()
            conn.close()

    def buscar_por_id(self, plato_id: int) -> Plato | None:
        conn = DBConnection.get_connection()

        if not conn:
            return None

        cursor = conn.cursor(dictionary=True)
        sql = "SELECT id, nombre, descripcion, precio FROM plato WHERE id = %s"

        try:
            cursor.execute(sql, (plato_id,))
            resultado = cursor.fetchone()

            if resultado:
                return Plato(
                    id=resultado['id'],
                    nombre=resultado['nombre'],
                    descripcion=resultado['descripcion'],
                    precio=float(resultado['precio'])
                )

            return None

        finally:
            cursor.close()
            conn.close()