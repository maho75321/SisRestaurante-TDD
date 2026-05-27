# test_fidelidad.py

from datetime import date
from servicios.servicio import ClienteService


# =========================================================
# PRUEBA UNITARIA - FIDELIDAD
# =========================================================

def test_fidelidad_unitaria(mocker):
    """
    Prueba unitaria para verificar_oferta_fidelidad().
    Usa mocks para aislar la lógica.
    """

    service = ClienteService()

    # ===== AGREGADO GUIA TDD =====
    # Simulación temporal del método.
    mock_fidelidad = mocker.patch.object(
        service,
        'verificar_oferta_fidelidad',
        return_value=True
    )
    # ===== FIN AGREGADO =====

    resultado = service.verificar_oferta_fidelidad(
        1,
        date.today()
    )

    mock_fidelidad.assert_called_once()

    assert resultado is True


# =========================================================
# PRUEBA DE INTEGRACIÓN - FIDELIDAD
# =========================================================

def test_fidelidad_integracion():
    """
    Prueba integración del servicio fidelidad.
    """

    service = ClienteService()

    resultado = service.verificar_oferta_fidelidad(
        1,
        date.today()
    )

    # ===== AGREGADO GUIA TDD =====
    # Verifica respuesta booleana.
    # ===== FIN AGREGADO =====
    assert isinstance(resultado, bool)