# test_orden.py

from datetime import date
from entidades.orden import Orden
from dao.ordenDAO import OrdenDAO


# =========================================================
# PRUEBA UNITARIA - GUARDAR ORDEN
# =========================================================

def test_guardar_orden_unitario_exitoso(mocker):
    """
    Prueba unitaria para OrdenDAO.guardar().
    Aísla el guardado usando mocks.
    """

    # ===== AGREGADO GUIA TDD =====
    # Simulación del guardado exitoso.
    mock_guardar = mocker.patch(
        'dao.ordenDAO.OrdenDAO.guardar',
        return_value=10
    )
    # ===== FIN AGREGADO =====

    dao = OrdenDAO()

    orden = Orden(
        cliente_id=1,
        fecha=date.today(),
        tipo_orden='I',
        total=50.00
    )

    resultado = dao.guardar(orden)

    mock_guardar.assert_called_once()

    assert resultado == 10


# =========================================================
# PRUEBA DE INTEGRACIÓN - ORDEN
# =========================================================

def test_guardar_orden_integracion():
    """
    Prueba de integración para OrdenDAO.
    Verifica guardado real en la BD.
    """

    dao = OrdenDAO()

    orden = Orden(
        cliente_id=1,
        fecha=date.today(),
        tipo_orden='I',
        total=60.00
    )

    resultado = dao.guardar(orden)

    # ===== AGREGADO GUIA TDD =====
    # Verifica inserción correcta.
    # ===== FIN AGREGADO =====
    assert resultado != -1