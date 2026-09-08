# Rafael Bassani - RM569930 - Fase 2 - Capítulo 7
#Nádia Nakamura Vieira - rm568906 - Fase 2 - Capítulo 7
#Marco Antônio Rodrigues Siqueira - rm569975 - Fase 2 - Capítulo 7
#Heitor Exposito de Sousa - rm566013 - Fase 2 - Capítulo 7
#Vinicius Xavier da Silva - rm572108 - Fase 2 - Capítulo 7
# =========================
# 1. Pacotes
# =========================
if (!"readxl" %in% installed.packages()) {
  install.packages("readxl")
}

library(readxl)
# =========================
# 2. Importação da base
# =========================
dados <- read_excel("base_dados.xlsx")

# =========================
# 3. Conferência da base
# =========================
head(dados)
str(dados)
summary(dados)
nrow(dados)

# =========================
# 4. Padronização dos nomes das colunas
# =========================
names(dados) <- c(
  "ID",
  "Produto",
  "Safra",
  "Ano",
  "Producao_mil_ton",
  "Consumo_mil_ton",
  "Nivel_Producao"
)

# Conferir se ficou certo
names(dados)
str(dados)

# =========================
# 5. Escolha da variável quantitativa
# =========================
producao <- dados$Producao_mil_ton

# =========================
# 6. Medidas de tendência central
# =========================
media_producao <- mean(producao)
mediana_producao <- median(producao)

moda <- function(x) {
  ux <- unique(x)
  ux[which.max(tabulate(match(x, ux)))]
}
moda_producao <- moda(producao)

cat("\nMEDIDAS DE TENDÊNCIA CENTRAL\n")
cat("Média:", media_producao, "\n")
cat("Mediana:", mediana_producao, "\n")
cat("Moda:", moda_producao, "\n")

# =========================
# 7. Medidas de dispersão
# =========================
minimo_producao <- min(producao)
maximo_producao <- max(producao)
amplitude_producao <- maximo_producao - minimo_producao
variancia_producao <- var(producao)
desvio_padrao_producao <- sd(producao)
iqr_producao <- IQR(producao)

cat("\nMEDIDAS DE DISPERSÃO\n")
cat("Mínimo:", minimo_producao, "\n")
cat("Máximo:", maximo_producao, "\n")
cat("Amplitude:", amplitude_producao, "\n")
cat("Variância:", variancia_producao, "\n")
cat("Desvio padrão:", desvio_padrao_producao, "\n")
cat("Amplitude interquartil:", iqr_producao, "\n")

# =========================
# 8. Medidas separatrizes
# =========================
quartis_producao <- quantile(producao)
percentis_producao <- quantile(producao, probs = c(0.10, 0.25, 0.50, 0.75, 0.90))

cat("\nMEDIDAS SEPARATRIZES\n")
cat("Quartis:\n")
print(quartis_producao)

cat("\nPercentis (10%, 25%, 50%, 75%, 90%):\n")
print(percentis_producao)

# =========================
# 9. Análise gráfica da variável quantitativa
# =========================
hist(
  producao,
  main = "Histograma da Produção",
  xlab = "Produção (mil ton)",
  ylab = "Frequência"
)

boxplot(
  producao,
  main = "Boxplot da Produção",
  ylab = "Produção (mil ton)"
)

# =========================
# 10. Análise da variável qualitativa
# Escolha: Produto
# =========================
frequencia_produto <- table(dados$Produto)

cat("\nFREQUÊNCIA DA VARIÁVEL QUALITATIVA - PRODUTO\n")
print(frequencia_produto)

barplot(
  frequencia_produto,
  main = "Frequência por Produto",
  xlab = "Produto",
  ylab = "Quantidade"
)
producao_por_produto <- tapply(dados$Producao_mil_ton, dados$Produto, sum)
barplot(producao_por_produto,
        main = "Produção Total por Produto",
        xlab = "Produto",
        ylab = "Produção Total (mil ton)")


# =========================
# 11. Análise opcional da variável qualitativa ordinal
# =========================
frequencia_nivel <- table(dados$Nivel_Producao)

cat("\nFREQUÊNCIA DA VARIÁVEL QUALITATIVA ORDINAL - NÍVEL DE PRODUÇÃO\n")
print(frequencia_nivel)

barplot(
  frequencia_nivel,
  main = "Frequência por Nível de Produção",
  xlab = "Nível de Produção",
  ylab = "Quantidade"
)

# =========================
# 12. Gráfico complementar por cultura
# tipo controle com pontos + linha + média ± desvio padrão
# =========================

# Lista de culturas presentes na base
culturas <- unique(dados$Produto)

# Define layout para vários gráficos na mesma janela
par(mfrow = c(3, 2))  # ajuste se quiser outro arranjo

for (cultura in culturas) {
  
  dados_cultura <- subset(dados, Produto == cultura)
  
  producao_cultura <- dados_cultura$Producao_mil_ton
  anos_cultura <- dados_cultura$Ano
  
  media_cultura <- mean(producao_cultura)
  desvio_cultura <- sd(producao_cultura)
  
  plot(
    anos_cultura,
    producao_cultura,
    type = "b",
    pch = 16,
    main = paste("Produção por Ano -", cultura),
    xlab = "Ano",
    ylab = "Produção (mil ton)"
  )
  
  abline(h = media_cultura, lty = 1, lwd = 2)
  abline(h = media_cultura + desvio_cultura, lty = 2, lwd = 2)
  abline(h = media_cultura - desvio_cultura, lty = 2, lwd = 2)
}

# Voltar layout padrão
par(mfrow = c(1, 1))

# =========================
# 13. Resumo final para interpretação
# =========================
cat("\nRESUMO FINAL\n")
cat("Total de linhas da base:", nrow(dados), "\n")
cat("Quantidade de produtos analisados:", length(unique(dados$Produto)), "\n")
cat("Média da produção:", media_producao, "\n")
cat("Mediana da produção:", mediana_producao, "\n")
cat("Desvio padrão da produção:", desvio_padrao_producao, "\n")


