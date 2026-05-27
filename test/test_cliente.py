# test_cliente.py
from datetime import date

import mysql

from unittest.mock import MagicMock
from entidades.cliente import Cliente
from dao.conexion import DBConnection
from dao.clienteDAO import ClienteDAO
from servicios.servicio import ClienteService

# ===== AGREGADO GUIA TDD =====
# Temporalmente usamos ClienteService hasta implementar el controlador real.
# Este comentario servirá para identificar el cambio en el informe.
# ===== FIN AGREGADO =====


# =========================================================
# PRUEBAS UNITARIAS (Aislando la Capa de Servicio)
# =========================================================

# Usamos la fixture 'mocker' proporcionada por pytest-mock
def test_guardar_cliente_unitario_exitoso(mocker):
    """
    Prueba unitaria para ClienteService.registrar_cliente().
    Aísla la capa de servicio 'mockeando' la capa DAO.
    """

    # 1. Preparación del Mock: Simular que ClienteDAO.guardar() retorna un ID (éxito)
    # Creamos un mock para el método guardar del DAO.

    # ===== CAMBIO GUIA TDD =====
    # Se corrige la ruta real del DAO.
    mock_dao_guardar = mocker.patch(
        'dao.clienteDAO.ClienteDAO.guardar',
        return_value=5
    )
    # ===== FIN CAMBIO =====

    # 2. Inicialización del servicio
    service = ClienteService()

    # 3. Ejecución
    # No necesitamos pasar una instancia de Cliente real, solo los datos.
    cliente_registrado = service.registrar_cliente("Test Mock", "123456789")

    # 4. Verificación (Asserts)

    # Aseguramos que el método 'guardar' del DAO fue llamado exactamente una vez
    mock_dao_guardar.assert_called_once()

    # Aseguramos que la función de servicio retorna un objeto Cliente válido
    assert cliente_registrado is not None
    assert cliente_registrado.nombre == "Test Mock"

    # El servicio no debe asignar el ID devuelto por el DAO a menos que se implemente buscar_por_id,
    # pero aquí validamos que retorna un objeto:
    assert isinstance(cliente_registrado, Cliente)


def test_guardar_cliente_unitario_fallido(mocker):
    """
    Prueba unitaria para ClienteService.registrar_cliente().
    Simula que el DAO falla al guardar (ej. teléfono duplicado).
    """

    # 1. Preparación del Mock: Simular que ClienteDAO.guardar() retorna -1 (fallo)

    # ===== CAMBIO GUIA TDD =====
    # Se corrige la ruta real del DAO.
    mock_dao_guardar = mocker.patch(
        'dao.clienteDAO.ClienteDAO.guardar',
        return_value=-1
    )
    # ===== FIN CAMBIO =====

    # 2. Inicialización del servicio
    service = ClienteService()

    # 3. Ejecución
    cliente_registrado = service.registrar_cliente("Test Fallo", "111222333")

    # 4. Verificación (Asserts)

    # Aseguramos que el método 'guardar' del DAO fue llamado
    mock_dao_guardar.assert_called_once()

    # El servicio debe retornar None si el DAO falló
    assert cliente_registrado is None


# =========================================================
# PRUEBAS DE INTEGRACIÓN (Controller, Service, DAO, DBConnection)
# =========================================================

# Nota: Esta prueba NO USA MOCKS para el DAO ni la BD,
# sino que usa un Mock para la función crítica DBConnection.get_connection()
# y simula una excepción en la base de datos para verificar el manejo de errores.

def test_registro_cliente_integracion_fallo_db(mocker):
    """
    Prueba de integración para ClienteService.
    Simula un fallo total de conexión a la BD para verificar que el flujo del
    Servicio maneje la excepción correctamente.
    """

    # 1. Preparación del Mock: Simular un fallo de conexión en la capa más baja

    # Creamos un objeto de excepción de MySQL simulado.
    mock_error = mysql.connector.Error(msg="Simulated DB Connection Error")

    # ===== CAMBIO GUIA TDD =====
    # Se corrige la ruta real de DBConnection.
    mock_conn = mocker.patch(
        'dao.conexion.DBConnection.get_connection',
        side_effect=mock_error
    )
    # ===== FIN CAMBIO =====

    # ===== AGREGADO GUIA TDD =====
    # Mientras se implementa el controlador solicitado por la guía,
    # se prueba el servicio directamente.
    service = ClienteService()
    # ===== FIN AGREGADO =====

    resultado = service.registrar_cliente(
        "Cliente Error",
        "999999999"
    )

    # 4. Verificación (Asserts)

    # El método de conexión debe haber sido llamado
    mock_conn.assert_called()

    # El servicio debe retornar None cuando la conexión falla
    assert resultado is None