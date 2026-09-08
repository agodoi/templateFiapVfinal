# --- 1. BIBLIOTECAS (Com verificação automática) ---
if (!require("openxlsx")) install.packages("openxlsx")
if (!require("dplyr")) install.packages("dplyr")
if (!require("lubridate")) install.packages("lubridate")

library(openxlsx)
library(dplyr)
library(lubridate)

# --- 2. CONFIGURAÇÕES INICIAIS ---
data_inicio <- as.Date("2020-01-01")
data_fim    <- as.Date("2026-04-18")

# Criar sequência de datas
datas <- seq(data_inicio, data_fim, by = "day")

# --- 3. FUNÇÃO DE CÁLCULO (Equivalente ao Python) ---
calcular_parametros <- function(data) {
  # Idade em dias e extração do mês
  dias <- as.numeric(data - data_inicio)
  mes  <- month(data)
  
  # Inicialização de variáveis
  estagio <- ""
  cad     <- 0
  kc      <- 0
  
  # 1. Fase de Estabelecimento (0-6 meses)
  if (dias < 180) {
    estagio <- "Pós-Plantio / Estabelecimento"
    cad     <- 25
    kc      <- 0.5
  } 
  # 2. Crescimento Vegetativo (6 meses a 2 anos)
  else if (dias < 730) {
    estagio <- "Crescimento Vegetativo Jovem"
    cad     <- 45
    kc      <- 0.7
  } 
  # 3. Fase Adulta (Produção)
  else {
    cad <- 70
    
    # Sazonalidade da planta adulta
    if (mes %in% c(9, 10)) {
      estagio <- "Florada e Início de Expansão"
      kc      <- 1.05
    } else if (mes %in% c(11, 12, 1, 2, 3)) {
      estagio <- "Expansão e Enchimento de Grãos"
      kc      <- 1.20
    } else if (mes %in% c(4, 5, 6)) {
      estagio <- "Maturação dos Frutos"
      kc      <- 0.85
    } else {
      estagio <- "Repouso Vegetativo / Colheita"
      kc      <- 0.65
    }
  }
  
  # Evapotranspiração de referência média (ET0)
  # Verão/Primavera (Set-Mar): ~4.5 | Outono/Inverno: ~3.0
  if ((mes >= 9 && mes <= 12) || (mes >= 1 && mes <= 3)) {
    et0 <- 4.5
  } else {
    et0 <- 3.0
  }
  
  consumo <- round(et0 * kc, 2)
  
  return(list(estagio = estagio, cad = cad, consumo = consumo))
}

# --- 4. GERAÇÃO DOS DADOS ---
# Aplicar a função a todas as datas
resultados <- lapply(datas, calcular_parametros)

# Converter a lista em um DataFrame
df <- data.frame(
  Data = format(datas, "%d/%m/%Y"),
  Estagio_Desenvolvimento = sapply(resultados, function(x) x$estagio),
  CAD_Solo_mm = sapply(resultados, function(x) x$cad),
  Consumo_Agua_Estimado_mm_dia = sapply(resultados, function(x) x$consumo)
)

# --- 5. SALVAR ARQUIVO ---
write.xlsx(df, "manejo_irrigacao_cafe_franca_2020_2025.xlsx")

# Mensagem de confirmação
cat("Arquivo Excel gerado com sucesso!")



