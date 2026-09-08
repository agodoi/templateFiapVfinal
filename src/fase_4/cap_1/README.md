# FarmTech Solutions - Protótipo Assistente Agrícola Inteligente

Projeto acadêmico (FIAP - Fase 4) que demonstra um protótipo de assistente agrícola com Streamlit, integração Oracle e pipeline de Machine Learning.

Principais componentes:
- Interface Streamlit em `app.py` e páginas em `pages/`
- Camada de dados e integração Oracle em `src/database.py`
- Pipeline de ML em `src/models.py` e pré-processamento em `src/preprocessing.py`
- Recomendações em `src/recommendations.py`

Configuração rápida:
1. Copie `.env.example` para `.env` e preencha as variáveis.
2. Instale dependências: `pip install -r requirements.txt`
3. Rode: `streamlit run app.py`

Arquitetura e detalhes de uso estão descritos nos módulos `src/`.

## Modelagem e integridade dos dados

- **CS_FAZENDAS**: dimensão principal contendo informações da fazenda (identificador, nome, cidade, UF, área, cultura).
- **CS_CLIMA**: histórico climático por fazenda (temperatura, umidade relativa do ar, velocidade do vento, data_hora).
- **CS_SENSORES_IOT**: leituras simuladas de sensores de solo geradas a partir de `CS_CLIMA`. Contém `UMIDADE_SOLO` (umidade do solo), `TEMPERATURA_SOLO`, `NUTRIENTES_N`, `SCORE_NECESSIDADE_IRRIGACAO`, `VOLUME_IRRIGACAO_ESTIMADO` e `ACAO_IRRIGACAO`.
- **CS_CLIMA_EVENTOS**: eventos climáticos por cidade/UF/data, agregados por fazenda por meio da view `VW_EVENTOS_CLIMATICOS_FAZENDA`.

## Vídeo com as entregas
[https://youtu.be/ddQ8wB-jk9U](https://www.youtube.com/watch?v=ddQ8wB-jk9U)


Observações importantes:

- `UMIDADE_AR` (em `CS_CLIMA`) e `UMIDADE_SOLO` (em `CS_SENSORES_IOT`) são variáveis distintas: correlacionadas porém não idênticas.
- As views `VW_EVENTOS_CLIMATICOS_FAZENDA` e `VW_DADOS_AGRICOLAS_ML` consolidam eventos por fazenda e fornecem a base final para modelos de Machine Learning.
- Nunca coloque credenciais reais no repositório. Use `.env` local (não comitar).

## Vídeos das Entregas

- `Entrega 1 - [Entrega 1](https://www.youtube.com/watch?v=pPbfUXVtBOI)
- `Entrega 2 -  [Entrega 2](https://www.youtube.com/watch?v=VYf7oJ9xeoM)
- `Entrega 3 -  [Entrega 3](https://www.youtube.com/watch?v=QiJ5etScl1A)
- `Entrega 4 -  [Entrega 4](https://www.youtube.com/watch?v=OC5e83rR1Zo)
- `Todas as entregas - [Clique aqui para assistir à entrega completa!](https://www.youtube.com/watch?v=ddQ8wB-jk9U) 
  

Scripts criados:

- `scripts/rebuild_sensores_iot.py`: reconstrói `CS_SENSORES_IOT` com backup automático, geração sintética de leituras e criação das views necessárias. Pede confirmação textual `CONFIRMAR` antes de recriar a tabela.
- `scripts/validate_database_integrity.py`: gera um relatório básico de integridade (contagens, sensores sem fazenda, sensores sem clima correspondente, distribuição de ação de irrigação e métricas agregadas).

Uso rápido:

```bash
python scripts/rebuild_sensores_iot.py --sample-every 24
python scripts/validate_database_integrity.py
```

