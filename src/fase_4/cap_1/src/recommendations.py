"""Simple recommendation rules for the demo assistant.

This module implements a lightweight rule-based recommender used by the
`Assistente Agrícola` page. It is deliberately simple to keep the demo
explainable; replace with ML-based logic if needed.
"""

from typing import Dict


def recommend(umidade_solo: float, temperatura: float, nutrientes_N: float, volume_estimado: float, cultura: str = None) -> Dict:
    """Return a dictionary with irrigation and management recommendations.

    The function returns keys: `recomendacao_irrigacao`, `recomendacao_manejo`,
    `nivel_risco`, and `explicacao` for display in the UI.
    """
    risk = 'Baixo'
    advice_irrig = 'Não é necessária irrigação imediata.'
    advice_fert = 'Manter práticas atuais.'

    if umidade_solo < 30:
        risk = 'Alto'
        advice_irrig = f'Recomenda-se irrigação. Volume estimado: {volume_estimado:.1f} unidades.'
    elif umidade_solo < 45:
        risk = 'Médio'
        advice_irrig = 'Monitorar e avaliar frequência de irrigação.'

    if nutrientes_N < 100:
        advice_fert = 'Aplicar fertilizante nitrogenado conforme recomendação técnica.'
        if risk == 'Baixo':
            risk = 'Médio'

    explanation = f"Umidade solo {umidade_solo:.1f}%, temperatura {temperatura:.1f}°C, nutrientes N {nutrientes_N:.1f}."
    return {
        'recomendacao_irrigacao': advice_irrig,
        'recomendacao_manejo': advice_fert,
        'nivel_risco': risk,
        'explicacao': explanation
    }
