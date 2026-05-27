
from dao.conexion import DBConnection
from entidades.orden import Orden


class OrdenDAO:
    """DAO para la entidad Orden."""

    def guardar(self, orden: Orden) -> int:
        conn = DBConnection.get_connection()
        if not conn:
            return -1

        cursor = conn.cursor()

        sql = """
        INSERT INTO orden (cliente_id, fecha, tipo_orden, total)
        VALUES (%s, %s, %s, %s)
        """

        try:
            cursor.execute(
                sql,
                (
                    orden.cliente_id,
                    orden.fecha,
                    orden.tipo_orden,
                    orden.total
                )
            )

            conn.commit()
            orden.id = cursor.lastrowid
            return orden.id

        except DBConnection.error as err:
            return -1

        finally:
            cursor.close()
            conn.close()

    def buscar_por_id(self, orden_id: int) -> Orden | None:
        conn = DBConnection.get_connection()

        if not conn:
            return None

        cursor = conn.cursor(dictionary=True)

        sql = """
        SELECT id, cliente_id, fecha, tipo_orden, total
        FROM orden
        WHERE id = %s
        """

        try:
            cursor.execute(sql, (orden_id,))
            resultado = cursor.fetchone()

            if resultado:
                return Orden(
                    id=resultado['id'],
                    cliente_id=resultado['cliente_id'],
                    fecha=resultado['fecha'],
                    tipo_orden=resultado['tipo_orden'],
                    total=float(resultado['total'])
                )

            return None

        finally:
            cursor.close()
            conn.close()