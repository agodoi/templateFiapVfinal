# --- 1. BIBLIOTECAS ---
if (!require("dplyr")) install.packages("dplyr")
if (!require("lubridate")) install.packages("lubridate")
if (!require("ggplot2")) install.packages("ggplot2")
if (!require("tidyr")) install.packages("tidyr")
library(dplyr)
library(lubridate)
library(ggplot2)
library(tidyr)

# --- 2. CARREGAMENTO E TRATAMENTO DE DADOS ---
df_cafe <- read.csv("Dataset - 2026.04.19 19h07.csv", sep = ";", dec = ".")
df_cafe$Data_Formatada <- as.Date(df_cafe$Data, origin = "2000-01-01")
df_cafe$Ano <- year(df_cafe$Data_Formatada)
df_cafe$Mes <- month(df_cafe$Data_Formatada)

# --- 3. FUNÇÃO DE BALANÇO HÍDRICO ---
calcular_balanco <- function(dados, tipo_modelo) {
  n <- nrow(dados)
  estoque_ini <- numeric(n); consumo_dia <- numeric(n); saldo_dia_pos <- numeric(n)
  irrigacao_vol <- numeric(n); irrigou_dia <- logical(n); saldo_final <- numeric(n)
  est_atual <- NULL 
  
  for (i in 1:n) {
    if (dados$Data_Formatada[i] == as.Date("2020-01-01")) { est_atual <- 30 }
    if (is.null(est_atual)) { est_atual <- 30 }
    
    estoque_ini[i] <- est_atual
    consumo_dia[i] <- dados$ET0[i] * dados$KC[i]
    soma_limitada_cad <- min(estoque_ini[i] + dados$Precipitacao[i], dados$CAD_Max[i])
    saldo_dia_pos[i] <- soma_limitada_cad - consumo_dia[i]
    
    gatilho <- if(tipo_modelo == "Estresse") dados$CAD_Estresse[i] else dados$CAD_Otimizado[i]
    
    if (saldo_dia_pos[i] < (gatilho - 0.01)) {
      alvo <- dados$CAD_Max[i] * 0.9
      irrigacao_vol[i] <- max(0, alvo - max(0, saldo_dia_pos[i]))
      irrigou_dia[i] <- TRUE
    } else {
      irrigacao_vol[i] <- 0; irrigou_dia[i] <- FALSE
    }
    saldo_final[i] <- min(max(0, saldo_dia_pos[i] + irrigacao_vol[i]), dados$CAD_Max[i])
    est_atual <- saldo_final[i]
  }
  return(data.frame(Data = dados$Data_Formatada, Ano = dados$Ano, Mes = dados$Mes, 
                    Estagio = dados$Estagio, Precipitacao = dados$Precipitacao, 
                    Consumo = consumo_dia, Estoque_Inicial = estoque_ini, 
                    Saldo_Pos = saldo_dia_pos, Irrigou = irrigou_dia, 
                    Vol = irrigacao_vol, Saldo_Final = saldo_final))
}

# --- 4. PROCESSAMENTO ---
df_otimizado <- calcular_balanco(df_cafe, "Otimizado")
df_estresse  <- calcular_balanco(df_cafe, "Estresse")

# --- 5. CRIAÇÃO DO RESUMO ANUAL FINAL ---
resumo_mensal <- df_estresse %>%
  group_by(Ano, Mes, Estagio) %>%
  summarise(Precip = sum(Precipitacao), Consumo = sum(Consumo),
            Irrig_Est_mm = sum(Vol), Vezes_Est = sum(Irrigou), .groups = 'drop') %>%
  left_join(df_otimizado %>% group_by(Ano, Mes, Estagio) %>%
              summarise(Irrig_Oti_mm = sum(Vol), Vezes_Oti = sum(Irrigou), .groups = 'drop'),
            by = c("Ano", "Mes", "Estagio"))

resumo_anual_base <- resumo_mensal %>%
  group_by(Ano) %>%
  summarise(Precip = sum(Precip), Consumo = sum(Consumo),
            Irrig_Est_mm = sum(Irrig_Est_mm), Vezes_Est = sum(Vezes_Est),
            Irrig_Oti_mm = sum(Irrig_Oti_mm), Vezes_Oti = sum(Vezes_Oti), .groups = 'drop') %>%
  mutate(Dif_Vol = Irrig_Oti_mm - Irrig_Est_mm, Dif_Vezes = Vezes_Oti - Vezes_Est)

total_geral_row <- resumo_anual_base %>%
  summarise(Ano = "TOTAL GERAL", Precip = sum(Precip), Consumo = sum(Consumo),
            Irrig_Est_mm = sum(Irrig_Est_mm), Vezes_Est = sum(Vezes_Est),
            Irrig_Oti_mm = sum(Irrig_Oti_mm), Vezes_Oti = sum(Vezes_Oti),
            Dif_Vol = sum(Dif_Vol), Dif_Vezes = sum(Dif_Vezes))

resumo_anual_final <- rbind(as.data.frame(resumo_anual_base), as.data.frame(total_geral_row))

# --- 6. GRÁFICO COMPARATIVO ---
# Usamos os dados base do relatorio anual (sem a linha total geral para não distorcer a proporção do gráfico)
df_graph <- resumo_anual_final %>% filter(Ano != "TOTAL GERAL")
df_graph$Ano <- as.numeric(as.character(df_graph$Ano))

# Coeficiente para o segundo eixo (Vezes)
coeff <- max(df_graph$Irrig_Oti_mm) / max(df_graph$Vezes_Oti)

plot_comparativo <- ggplot(df_graph, aes(x = factor(Ano))) +
  # Barras de Volume (mm)
  geom_bar(aes(y = Irrig_Est_mm, fill = "Estresse"), stat = "identity", position = position_nudge(x = -0.2), width = 0.2) +
  geom_bar(aes(y = Irrig_Oti_mm, fill = "Otimizado"), stat = "identity", position = position_nudge(x = 0), width = 0.2) +
  geom_bar(aes(y = Dif_Vol, fill = "Diferença"), stat = "identity", position = position_nudge(x = 0.2), width = 0.2) +
  # Linhas de Frequência (Vezes)
  geom_line(aes(y = Vezes_Est * coeff, color = "Estresse", group = 1), size = 1.2) +
  geom_point(aes(y = Vezes_Est * coeff, color = "Estresse"), size = 3) +
  geom_line(aes(y = Vezes_Oti * coeff, color = "Otimizado", group = 1), size = 1.2) +
  geom_point(aes(y = Vezes_Oti * coeff, color = "Otimizado"), size = 3) +
  geom_line(aes(y = Dif_Vezes * coeff, color = "Diferença", group = 1), linetype = "dashed", size = 1) +
  # Cores e Eixos
  scale_fill_manual(values = c("Estresse" = "blue", "Otimizado" = "purple", "Diferença" = "gray60")) +
  scale_color_manual(values = c("Estresse" = "blue", "Otimizado" = "purple", "Diferença" = "gray60")) +
  scale_y_continuous(name = "Volume Irrigado (mm)", sec.axis = sec_axis(~./coeff, name = "Quantidade de Vezes")) +
  labs(title = "Comparativo Anual dos Sistemas de Irrigação de Conforto e Estresse Hídrico",
       x = "Ano", fill = "Volume (Barras)", color = "Frequência (Linhas)") +
  theme_minimal() +
  theme(legend.position = "bottom")

# --- 7. EXIBIÇÃO ---
print(resumo_anual_final)
print(plot_comparativo)

