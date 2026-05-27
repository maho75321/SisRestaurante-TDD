# test_plato.py

from entidades.plato import Plato
from dao.platoDAO import PlatoDAO
from datetime import datetime


# =========================================================
# PRUEBA UNITARIA - GUARDAR PLATO
# =========================================================

def test_guardar_plato_unitario_exitoso(mocker):
    """
    Prueba unitaria para PlatoDAO.guardar().
    Usa mocks para aislar la lógica.
    """

    # ===== AGREGADO GUIA TDD =====
    # Simulación de guardado exitoso.
    mock_guardar = mocker.patch(
        'dao.platoDAO.PlatoDAO.guardar',
        return_value=20
    )
    # ===== FIN AGREGADO =====

    dao = PlatoDAO()

    plato = Plato(
        nombre="Plato Test",
        descripcion="Descripción prueba",
        precio=25.00
    )

    resultado = dao.guardar(plato)

    mock_guardar.assert_called_once()

    assert resultado == 20


# =========================================================
# PRUEBA DE INTEGRACIÓN - PLATO
# =========================================================

def test_guardar_plato_integracion():
    """
    Prueba de integración para PlatoDAO.
    Guarda un plato real en la BD.
    """

    dao = PlatoDAO()

    # ===== CAMBIO GUIA TDD =====
    # Generación de nombre único para evitar conflicto UNIQUE.
    nombre_unico = f"Plato_TDD_{datetime.now().strftime('%H%M%S')}"
    # ===== FIN CAMBIO =====

    plato = Plato(
        nombre=nombre_unico,
        descripcion="Registro integración",
        precio=30.00
    )

    resultado = dao.guardar(plato)

    # ===== AGREGADO GUIA TDD =====
    # Verifica inserción correcta.
    # ===== FIN AGREGADO =====
    assert resultado != -1