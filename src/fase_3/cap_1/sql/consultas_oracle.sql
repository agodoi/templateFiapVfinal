-- SEQUENCIA DE SELECTS

-- 1. Validação de Integridade
-- Verifica se não há dados órfãos e se a distribuição das fazendas está correta.

SELECT ID_FAZENDA, COUNT(*) as TOTAL_DIAS
FROM SENSORES
GROUP BY ID_FAZENDA
ORDER BY ID_FAZENDA;

-- ********************************************************************************************

-- 2. Validação da Lógica de Nutrientes (N, P, K)
-- Mostra reposição de nutrientes no solo.

SELECT EXTRACT(YEAR FROM TO_DATE(DATA_LEITURA, 'YYYY-MM-DD')) as ANO,
       ID_FAZENDA,
       COUNT(*) as TOTAL_DIAS_COM_NUTRIENTE_ZERO
FROM SENSORES
WHERE N_STATUS = 0
GROUP BY EXTRACT(YEAR FROM TO_DATE(DATA_LEITURA, 'YYYY-MM-DD')), ID_FAZENDA
ORDER BY ANO, TOTAL_DIAS_COM_NUTRIENTE_ZERO DESC;

-- ********************************************************************************************

-- 3. Validação da Sazonalidade Hídrica
-- Demonstra que a irrigação está sendo acionada conforme a necessidade da cultura, variando ao longo do tempo.

-- Verifica a taxa de ativação da bomba por mês, ano e localiade (prova a sazonalidade)
SELECT 
    EXTRACT(YEAR FROM TO_DATE(s.DATA_LEITURA, 'YYYY-MM-DD')) as ANO,
    EXTRACT(MONTH FROM TO_DATE(s.DATA_LEITURA, 'YYYY-MM-DD')) as MES,
    f.ESTADO,
    COUNT(*) as TOTAL_IRRIGACOES
FROM SENSORES s
JOIN FAZENDAS f ON s.ID_FAZENDA = f.ID_FAZENDA
WHERE s.BOMBA_STATUS = 'LIGADA'
GROUP BY 
    EXTRACT(YEAR FROM TO_DATE(s.DATA_LEITURA, 'YYYY-MM-DD')),
    EXTRACT(MONTH FROM TO_DATE(s.DATA_LEITURA, 'YYYY-MM-DD')),
    f.ESTADO
ORDER BY ANO, MES, f.ESTADO;

-- ********************************************************************************************

-- 4. Comparativo entre Culturas
-- Valida que o modelo entende a diferença entre Soja e Café.

-- Compara o comportamento da bomba entre Soja e Café (join com a tabela de fazendas)
SELECT f.CULTURA,
       s.BOMBA_STATUS,
       COUNT(*) as QUANTIDADE
FROM SENSORES s
JOIN FAZENDAS f ON s.ID_FAZENDA = f.ID_FAZENDA
GROUP BY f.CULTURA, s.BOMBA_STATUS;

-- ********************************************************************************************

-- 5. Avaliar quantas vezes uma fazenda específica foi irrigada no período analisado

SELECT 
    f.MUNICIPIO,
    f.CULTURA,
    s.DATA_LEITURA,
    s.ID_FAZENDA,
    s.BOMBA_STATUS
FROM SENSORES s
JOIN FAZENDAS f ON s.ID_FAZENDA = f.ID_FAZENDA
WHERE s.BOMBA_STATUS = 'LIGADA'
  AND s.ID_FAZENDA = 1
ORDER BY s.DATA_LEITURA DESC;

-- ********************************************************************************************

-- 6. Avaliar quantas vezes uma fazenda específica teve reposição de nutrientes

SELECT 
    f.MUNICIPIO,
    f.CULTURA,
    s.DATA_LEITURA,
    s.ID_FAZENDA,
    'NITROGÊNIO' as NUTRIENTE,
    'REPOSIÇÃO' as STATUS
FROM SENSORES s
JOIN FAZENDAS f ON s.ID_FAZENDA = f.ID_FAZENDA
WHERE s.N_STATUS = 0 AND s.ID_FAZENDA = 1

UNION ALL

SELECT 
    f.MUNICIPIO,
    f.CULTURA,
    s.DATA_LEITURA,
    s.ID_FAZENDA,
    'FÓSFORO' as NUTRIENTE,
    'REPOSIÇÃO' as STATUS
FROM SENSORES s
JOIN FAZENDAS f ON s.ID_FAZENDA = f.ID_FAZENDA
WHERE s.P_STATUS = 0 AND s.ID_FAZENDA = 1

UNION ALL

SELECT 
    f.MUNICIPIO,
    f.CULTURA,
    s.DATA_LEITURA,
    s.ID_FAZENDA,
    'POTÁSSIO' as NUTRIENTE,
    'REPOSIÇÃO' as STATUS
FROM SENSORES s
JOIN FAZENDAS f ON s.ID_FAZENDA = f.ID_FAZENDA
WHERE s.K_STATUS = 0 AND s.ID_FAZENDA = 1
ORDER BY DATA_LEITURA DESC;