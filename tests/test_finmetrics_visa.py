"""Golden tests anclados al taller de VISA (FY2025). Rellenar cuando exista fintarget/features/finmetrics.py."""
import pytest

VISA_FY2025_EXPECTED = {
    "current_ratio": 1.08,
    "roic": 0.475,
    "beta_regresion_60m": 0.76,
    "wacc_mercado": 0.079,
    "eva_usd_mm": 18535,
}

@pytest.mark.skip(reason="pendiente: extraer finmetrics.py del modelo VISA")
def test_visa_golden():
    ...
