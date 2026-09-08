# Definir biblioteca pessoal para instalação de pacotes
if (!dir.exists(Sys.getenv("R_LIBS_USER"))) {
  dir.create(Sys.getenv("R_LIBS_USER"), recursive = TRUE)
}
.libPaths(c(Sys.getenv("R_LIBS_USER"), .libPaths()))

# Carregar pacotes necessários (se ainda não estiverem instalados)
if (!require("dplyr")) install.packages("dplyr")
library(dplyr)

if (!require("ggplot2")) install.packages("ggplot2")
library(ggplot2)

# Leitura dos dados
# O CSV deve ter colunas: cultura, area, tipo_insumo, qnt_insumo
args <- commandArgs(trailingOnly = FALSE)
script_path <- grep("^--file=", args, value = TRUE)
if (length(script_path) == 0) {
  script_dir <- getwd()
} else {
  script_dir <- dirname(sub("^--file=", "", script_path))
}
dados <- read.csv(file.path(script_dir, "dados_plantio.csv"), stringsAsFactors = FALSE)

# Visualizar os dados
print("Dados de plantio:")
print(dados)

# Cálculo de estatísticas básicas para a área plantada e quantidade de insumos
# Estatísticas gerais:
media_area <- mean(dados$area, na.rm = TRUE)
desvio_area <- sd(dados$area, na.rm = TRUE)

media_qnt_insumo <- mean(dados$qnt_insumo, na.rm = TRUE)
desvio_qnt_insumo <- sd(dados$qnt_insumo, na.rm = TRUE)



dados_limpos <- dados %>%
  group_by(cultura, area) %>%
  summarise(
    lucro_total = max(lucro, na.rm = TRUE),
    peso_total = max(peso, na.rm = TRUE),
    metodo = first(na.omit(metodo))
  )

cores <- ifelse(dados_limpos$metodo == "Pulverizador Tratorizado", "slategray", "darkorange2")
modelo_drone <- lm(lucro_total ~ area, data = subset(dados_limpos, metodo_utilizado == "Drone Agrícola"))
modelo_trator <- lm(lucro_total ~ area, data = subset(dados_limpos, metodo_utilizado == "Pulverizador Tratorizado"))

plot(dados_limpos$area, dados_limpos$lucro_total,
main = "REGRESSÃO: ÁREA X LUCRO (METODOS DE COLHEITA)",
xlab = "area(m²)",
ylab = "lucro(r$)",
pch = 16,
col = "#9d9d9d")
abline(modelo_drone, col = cores, lwd = 2)
abline(modelo_trator, col = cores, lwd = 2)
egend("topleft", legend=c("Drone", "Trator"), col=cores, lty=1, lwd=2)
correl <- cor(dados_limpos$area, dados_limpos$lucro_total, use = "complete.obs")




# Agora sim a correlação funciona:
correl <- cor(dados_limpos$area, dados_limpos$lucro_total, use = "complete.obs")

cat("== Estatísticas Gerais ==\n")
cat("Média da área plantada:", round(media_area, 2), "m²\n")
cat("Desvio padrão da área plantada:", round(desvio_area, 2), "m²\n\n")
cat("Média da quantidade de insumos:", round(media_qnt_insumo, 2), "\n")
cat("Desvio padrão da quantidade de insumos:", round(desvio_qnt_insumo, 2), "\n\n")



# Caso queira ver as estatísticas separadas por cultura (Cafe e Soja)
estatisticas_por_cultura <- dados %>%
  group_by(cultura) %>%
  summarise(
    media_area = mean(area, na.rm = TRUE),
    desvio_area = sd(area, na.rm = TRUE),
    media_qnt_insumo = mean(qnt_insumo, na.rm = TRUE),
    desvio_qnt_insumo = sd(qnt_insumo, na.rm = TRUE),
  )

cat("== Estatísticas por Cultura ==\n")
print(estatisticas_por_cultura)