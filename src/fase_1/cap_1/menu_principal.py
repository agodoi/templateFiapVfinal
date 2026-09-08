import math
import os
import subprocess
import shutil
from dataclasses import dataclass, field
from typing import Optional

import pandas as pd

# Caracteres ANSI para estilização no terminal
CYAN = "\033[96m"
VERDE = "\033[92m"
AMARELO = "\033[93m"
AZUL = "\033[94m"
VERMELHO = "\033[91m"
NEGRITO = "\033[1m"
RESET = "\033[0m"

#Solução e problemas

def find_rscript():
    """Encontra o caminho do Rscript automaticamente."""
    rscript = shutil.which("Rscript")
    if rscript:
        return rscript
    # Fallback para caminhos comuns
    common_paths = [
        r"C:\Program Files\R\R-4.5.3\bin\RScript.exe",
        r"C:\Program Files\R\R-4.4.0\bin\RScript.exe",
        r"C:\Program Files\R\R-4.3.0\bin\RScript.exe",
        r"C:\R\bin\RScript.exe"
    ]
    for path in common_paths:
        if os.path.exists(path):
            return path
    return None


@dataclass
class Insumos:
    adubo: float = 0.0
    agua: float = 0.0
    fosfato: float = 0.0
    herbicida: str = "N/A"
    pesticida: str = "N/A"
    fertilizante: str = "N/A"


@dataclass
class Financeiro:
    area_total: float = 0.0
    peso_total: float = 0.0
    lucro: float = 0.0
    gastos: float = 0.0
    metodo_aplicacao: str = "N/A"


@dataclass
class Cultura:
    cultura: Optional[str] = None
    area: float = 0.0
    insumos: Insumos = field(default_factory=Insumos)
    financeiro: Financeiro = field(default_factory=Financeiro)
    status_qualidade: str = "Não analisado"
    qual_col: str = RESET


@dataclass
class FarmData:
    culturas: list[Cultura] = field(default_factory=list)
    cultura_ativa_idx: Optional[int] = None

    @property
    def cultura_ativa(self) -> Optional[Cultura]:
        if self.cultura_ativa_idx is not None and 0 <= self.cultura_ativa_idx < len(self.culturas):
            return self.culturas[self.cultura_ativa_idx]
        return None


def validar_float(mensagem: str, minimo: float = 0.0) -> float:
    """Solicita um float validado ao usuário."""
    while True:
        try:
            valor = float(
                input(f"{AZUL}{mensagem}{RESET}").replace(",", ".").strip())
            if valor < minimo:
                raise ValueError(f"Valor deve ser >= {minimo}.")
            return valor
        except ValueError as exc:
            print(f"{VERMELHO}Entrada inválida: {exc}. Tente novamente.{RESET}")

def validar_int(mensagem: str, opcoes: Optional[list] = None) -> int:
    """Solicita um inteiro validado ao usuário."""
    while True:
        try:
            valor = int(input(f"{AZUL}{mensagem}{RESET}").strip())
            if opcoes and valor not in opcoes:
                raise ValueError(f"Escolha uma das opções: {opcoes}.")
            return valor
        except ValueError as exc:
            print(f"{VERMELHO}Entrada inválida: {exc}. Tente novamente.{RESET}")

def validar_area(area: float):
    minimo = 100
    maximo = 1.52e12 
    sim = ["S", "SI", "SIM", "SS"]
    nao = ["N", "NA", "NAO", "NN"]
    try:
        if area < minimo:
             raise ValueError(f"Valor deve ser maior ou igual a 100m².")
        elif area > maximo:
            confirm = input(f"{AZUL}O valor digitado está correto? [S]im, [N]ao{RESET}").strip().upper()
            if confirm in sim:
                return area
            elif confirm in nao:
                return None
            else:
                return None
        return area
    except ValueError as exc:
        print(f"{VERMELHO}Entrada inválida: {exc}. Tente novamente.{RESET}")

def escolher_cultura(state: FarmData) -> None:
    """Define a cultura escolhida no estado."""
    if state.culturas:
        print(f"{AZUL}Culturas existentes:{RESET}")
        for i, c in enumerate(state.culturas):
            print(f"{i+1} - {c.cultura or 'Não definida'} (Área: {c.area:.2f} m²)")
        opcao = validar_int(
            f"{AZUL}Escolher cultura existente [1-{len(state.culturas)}] ou 0 para nova: {RESET}", list(range(0, len(state.culturas)+1)))
        if opcao == 0:
            # Nova cultura
            pass  # Continua para escolher tipo
        else:
            state.cultura_ativa_idx = opcao - 1
            print(f"{VERDE}Cultura ativa: {state.cultura_ativa.cultura}{RESET}")
            return

    # Escolher tipo de cultura
    opcao = input(
        f"{AZUL}Escolha a cultura [C]afé / [S]oja: {RESET}").strip().upper()
    if opcao == "C":
        cultura_nome = "cafe"
    elif opcao == "S":
        cultura_nome = "soja"
    else:
        print(f"{VERMELHO}Opção inválida. Use C ou S.{RESET}")
        return

    # Criar nova cultura
    nova_cultura = Cultura(cultura=cultura_nome)
    state.culturas.append(nova_cultura)
    state.cultura_ativa_idx = len(state.culturas) - 1
    print(f"{VERDE}Nova cultura criada: {cultura_nome}{RESET}")

def calcular_area(state: FarmData) -> None:
    """Calcula a área plantada com base na cultura."""
    if not state.cultura_ativa:
        print(f"{VERMELHO}Nenhuma cultura ativa selecionada.{RESET}")
        return

    cultura = state.cultura_ativa
    if cultura.cultura == "cafe":
        comprimento = validar_float("Comprimento (m): ", 0.01)
        largura = validar_float("Largura (m): ", 0.01)
        area_calculada = comprimento * largura
        area_validade = validar_area(area_calculada)
        if area_validade is not None:
            cultura.area = area_validade
        else:
            print(f"{VERMELHO}Gravação cancelada. Insira os dados novamente.{RESET}")
        print(f"{VERDE}Área do café (retângulo): {cultura.area:.2f} m²{RESET}")
    elif cultura.cultura == "soja":
        raio = validar_float("Raio (m): ", 0.01)
        cultura.area = math.pi * (raio ** 2)
        print(f"{VERDE}Área da soja (círculo): {cultura.area:.2f} m²{RESET}")
    else:
        print(f"{VERMELHO}Defina uma cultura antes de calcular área.{RESET}")


def calcular_insumos(state: FarmData) -> None:
    """Calcula insumos a partir da área e cultura."""
    if not state.cultura_ativa:
        print(f"{VERMELHO}Nenhuma cultura ativa selecionada.{RESET}")
        return

    cultura = state.cultura_ativa
    if cultura.area <= 0:
        print(f"{VERMELHO}Área não definida. Não é possível calcular insumos.{RESET}")
        return

    if cultura.cultura == "cafe":
        cultura.insumos.adubo = 200 * cultura.area
        cultura.insumos.agua = 3.0 * cultura.area
        cultura.insumos.fosfato = 10 * cultura.area
    else:
        cultura.insumos.adubo = 150 * cultura.area
        cultura.insumos.agua = 2.5 * cultura.area
        cultura.insumos.fosfato = 5 * cultura.area

    print(f"{VERDE}Insumos calculados com sucesso.{RESET}")


def definir_herbicida(state: FarmData) -> None:
    """Seleciona herbicida conforme tipo de ervas daninhas."""
    if not state.cultura_ativa:
        print(f"{VERMELHO}Nenhuma cultura ativa selecionada.{RESET}")
        return
    print(f"{AZUL}Escolha o tipo de ervas daninhas:{RESET}")
    tipo = validar_int(
        "[1] Grama rasteira, [2] Grama de folha larga: ", [1, 2])
    state.cultura_ativa.insumos.herbicida = "Glifosato" if tipo == 1 else "2,4-D"
    print(f"Herbicida: {state.cultura_ativa.insumos.herbicida}")


def definir_pesticida(state: FarmData) -> None:
    """Seleciona pesticida conforme tipo de inseto."""
    if not state.cultura_ativa:
        print(f"{VERMELHO}Nenhuma cultura ativa selecionada.{RESET}")
        return
    print(f"{AZUL}Escolha o tipo de insetos:{RESET}")
    tipo = validar_int("[1] Insetos vagens, [2] Insetos sugadores: ", [1, 2])
    state.cultura_ativa.insumos.pesticida = "Carbaryl" if tipo == 1 else "Imidacloprido"
    print(f"Pesticida: {state.cultura_ativa.insumos.pesticida}")


def definir_fertilizante(state: FarmData) -> None:
    """Seleciona fertilizante conforme condição do solo."""
    if not state.cultura_ativa:
        print(f"{VERMELHO}Nenhuma cultura ativa selecionada.{RESET}")
        return
    print(f"{AZUL}Escolha a condição do solo:{RESET}")
    tipo = validar_int("[1] pH < 6, [2] baixa fixação biológica: ", [1, 2])
    state.cultura_ativa.insumos.fertilizante = "Calcário" if tipo == 1 else "Inoculante Rhizobium"
    print(f"Fertilizante: {state.cultura_ativa.insumos.fertilizante}")


def definir_meio_aplicacao(state: FarmData) -> None:
    """Seleciona método de aplicação e atualiza gastos."""
    if not state.cultura_ativa:
        print(f"{VERMELHO}Nenhuma cultura ativa selecionada.{RESET}")
        return
    print(f"{AZUL}Escolha o método de aplicação:{RESET}")
    tipo = validar_int("[1] Pulverizador tratorizado, [2] Drone: ", [1, 2])
    if tipo == 1:
        state.cultura_ativa.financeiro.metodo_aplicacao = "Pulverizador Tratorizado"
        state.cultura_ativa.financeiro.gastos = 225000
    else:
        state.cultura_ativa.financeiro.metodo_aplicacao = "Drone Agrícola"
        state.cultura_ativa.financeiro.gastos = 15000
    print(
        f"Método de aplicação: {state.cultura_ativa.financeiro.metodo_aplicacao}")


def calcular_financeiro(state: FarmData) -> None:
    """Calcula produção e lucro estimado."""
    if not state.cultura_ativa:
        print(f"{VERMELHO}Nenhuma cultura ativa selecionada.{RESET}")
        return

    cultura = state.cultura_ativa
    if cultura.area <= 0:
        print("Área inválida para cálculo financeiro.")
        return

    hectares = cultura.area / 10000.0
    cultura.financeiro.area_total = cultura.area
    if cultura.cultura == "cafe":
        produtividade = 1.5  # ton/ha (valor médio simplificado)
    elif cultura.cultura == "soja":
        produtividade = 3.2  # ton/ha
    else:
        produtividade = 0.0

    receita = 6300 * hectares
    cultura.financeiro.peso_total = produtividade * hectares
    cultura.financeiro.lucro = receita - cultura.financeiro.gastos

    print(f"Peso estimado: {cultura.financeiro.peso_total:.2f} ton")
    print(f"Lucro estimado: R$ {cultura.financeiro.lucro:.2f}")


def exibir_dados(state: FarmData) -> None:
    """Exibe o estado atual configurado."""
    if not state.cultura_ativa:
        print(f"{VERMELHO}Nenhuma cultura ativa selecionada.{RESET}")
        return

    cultura = state.cultura_ativa
    print(f"\n{VERDE}{NEGRITO}=== Perfil de Plantio ==={RESET}")
    print(f"{AZUL}Cultura: {cultura.cultura or 'N/A'}{RESET}")
    print(f"{AZUL}Área: {cultura.area:.2f} m²{RESET}")
    print(f"{VERDE}--- Insumos ---{RESET}")
    print(f"{AZUL}Adubo: {cultura.insumos.adubo:.2f} g{RESET}")
    print(f"{AZUL}Água: {cultura.insumos.agua:.2f} L{RESET}")
    print(f"{AZUL}Fosfato: {cultura.insumos.fosfato:.2f} g{RESET}")
    print(f"{AZUL}Herbicida: {cultura.insumos.herbicida}{RESET}")
    print(f"{AZUL}Pesticida: {cultura.insumos.pesticida}{RESET}")
    print(f"{AZUL}Fertilizante: {cultura.insumos.fertilizante}{RESET}")
    print(f"{VERDE}--- Financeiro ---{RESET}")
    print(f"{AZUL}Área total: {cultura.financeiro.area_total:.2f}{RESET}")
    print(f"{AZUL}Peso total (ton): {cultura.financeiro.peso_total:.2f}{RESET}")
    print(f"{AZUL}Lucro: R$ {cultura.financeiro.lucro:.2f}{RESET}")
    print(f"{AZUL}Gastos: R$ {cultura.financeiro.gastos:.2f}{RESET}")
    print(f"{AZUL}Meio aplicação: {cultura.financeiro.metodo_aplicacao}{RESET}")
    print(f"{VERDE}--- Qualidade ---{RESET}")
    print(f"{cultura.qual_col}--- {cultura.status_qualidade} ---{RESET}")


def atualizar_dados(state: FarmData) -> None:
    """Atualiza os dados de cultura, área e insumos do plantio."""
    if not state.culturas:
        print(f"{VERMELHO}Nenhuma cultura cadastrada.{RESET}")
        return

    print("\n=== Atualização de Dados ===")
    print("Culturas disponíveis:")
    for i, c in enumerate(state.culturas):
        print(f"{i+1} - {c.cultura or 'Não definida'} (Área: {c.area:.2f} m²)")

    idx = validar_int("Escolha a cultura para atualizar: ",
                      list(range(1, len(state.culturas)+1))) - 1
    state.cultura_ativa_idx = idx
    cultura = state.culturas[idx]

    print("\n1 - Alterar cultura")
    print("2 - Alterar área")
    print("3 - Alterar insumos")
    print("0 - Voltar")

    opcao = validar_int("Escolha opção de atualização: ", [0, 1, 2, 3])

    if opcao == 1:
        escolher_cultura(state)  # Isso vai sobrescrever a cultura ativa
    elif opcao == 2:
        calcular_area(state)
        calcular_insumos(state)
    elif opcao == 3:
        definir_herbicida(state)
        definir_pesticida(state)
        definir_fertilizante(state)
        definir_meio_aplicacao(state)
    else:
        print(f"{AZUL}Retornando ao menu principal.{RESET}")


def consultar_dados(state: FarmData) -> None:
    """Exibe todas as culturas cadastradas."""
    if not state.culturas:
        print(f"{VERMELHO}Nenhuma cultura cadastrada.{RESET}")
        return

    print(f"\n{VERDE}{NEGRITO}=== Consulta de Dados ==={RESET}")
    for i, cultura in enumerate(state.culturas):
        print(f"\n{AMARELO}--- Cultura {i+1} ---{RESET}")
        print(f"{AZUL}Cultura: {cultura.cultura or 'Não definida'}{RESET}")
        print(f"{AZUL}Área: {cultura.area:.2f} m²{RESET}")
        print(f"{VERDE}--- Insumos ---{RESET}")
        print(f"{AZUL}Herbicida: {cultura.insumos.herbicida}{RESET}")
        print(f"{AZUL}Pesticida: {cultura.insumos.pesticida}{RESET}")
        print(f"{AZUL}Fertilizante: {cultura.insumos.fertilizante}{RESET}")
        print(f"{AZUL}Adubo (g): {cultura.insumos.adubo:.2f}{RESET}")
        print(f"{AZUL}Água (L): {cultura.insumos.agua:.2f}{RESET}")
        print(f"{AZUL}Fosfato (g): {cultura.insumos.fosfato:.2f}{RESET}")


def zerar_dados(state: FarmData) -> None:
    """Permite deletar culturas específicas ou todas."""
    if not state.culturas:
        print(f"{VERMELHO}Nenhuma cultura cadastrada.{RESET}")
        return

    print("\n=== Deletar Dados ===")
    print("Culturas disponíveis:")
    for i, c in enumerate(state.culturas):
        print(f"{i+1} - {c.cultura or 'Não definida'} (Área: {c.area:.2f} m²)")

    print(f"{len(state.culturas)+1} - Deletar todas as culturas")
    print("0 - Voltar")

    opcao = validar_int("Escolha opção: ", list(
        range(0, len(state.culturas)+2)))

    if opcao == 0:
        print(f"{AZUL}Retornando ao menu principal.{RESET}")
    elif opcao == len(state.culturas) + 1:
        state.culturas.clear()
        state.cultura_ativa_idx = None
        print(f"{VERDE}Todas as culturas deletadas.{RESET}")
    else:
        idx = opcao - 1
        cultura_removida = state.culturas.pop(idx)
        print(f"{VERDE}Cultura '{cultura_removida.cultura}' deletada.{RESET}")
        if state.cultura_ativa_idx == idx:
            state.cultura_ativa_idx = None
        elif state.cultura_ativa_idx and state.cultura_ativa_idx > idx:
            state.cultura_ativa_idx -= 1


def exportar_csv(state: FarmData) -> None:
    """Exporta dados de plantio e insumos para CSV."""
    if not state.culturas:
        print(
            f"{VERMELHO}Não há dados válidos para exportação. Cadastre culturas.{RESET}")
        return

    registros = []
    for cultura in state.culturas:
        if cultura.cultura and cultura.area > 0:
            registros.extend([
                #ADUBO
                {"cultura": cultura.cultura, "area": cultura.area,
                    "tipo_insumo": "adubo", "qnt_insumo": cultura.insumos.adubo},
                #AGUA
                {"cultura": cultura.cultura, "area": cultura.area,
                    "tipo_insumo": "agua", "qnt_insumo": cultura.insumos.agua},
                #FOSFATO
                {"cultura": cultura.cultura, "area": cultura.area,
                    "tipo_insumo": "fosfato", "qnt_insumo": cultura.insumos.fosfato},
                #QUALIDADE
                {"cultura": cultura.cultura, "area": cultura.area,
                    "qualidade": cultura.status_qualidade, "cor": cultura.qual_col},
                #LUCRO E GASTOS
                {"cultura": cultura.cultura, "area": cultura.area,
                    "lucro": cultura.financeiro.lucro, "gastos": cultura.financeiro.gastos},
                {"cultura": cultura.cultura, "area": cultura.area,
                    "metodo": cultura.financeiro.metodo_aplicacao, "peso": cultura.financeiro.peso_total}
                    
            ])

    if not registros:
        print(f"{VERMELHO}Não há dados válidos para exportação.{RESET}")
        return

    df = pd.DataFrame(registros)
    nome_arquivo = "dados_plantio.csv"
    df.to_csv(nome_arquivo, index=False, encoding="utf-8-sig")
    print(f"{VERDE}CSV exportado: {nome_arquivo}{RESET}")


def executar_estatisticas_r() -> None:
    """Executa script estatisticas_basicas.r com dados exportados."""
    arquivo = "dados_plantio.csv"
    if not os.path.exists(arquivo):
        print(
            f"{VERMELHO}Arquivo dados_plantio.csv não encontrado. Exporte antes.{RESET}")
        return

    rscript_path = find_rscript()
    if not rscript_path:
        print(
            f"{VERMELHO}Rscript não encontrado. Instale R ou adicione ao PATH.{RESET}")
        return

    try:
        resultado = subprocess.run(
            [rscript_path, "estatisticas_basicas.r"], capture_output=True, text=True, check=True)
        print(f"{VERDE}== Estatísticas (R) =={RESET}")
        print(resultado.stdout)
    except subprocess.CalledProcessError as exc:
        print(f"{VERMELHO}Erro ao executar R: {exc.stderr}{RESET}")
    except FileNotFoundError:
        print(f"{VERMELHO}Rscript não encontrado.{RESET}")


def consultar_previsao_tempo() -> None:
    """Executa o script previsao_do_tempo.r com cidade escolhida pelo usuário."""
    cidade = input(
        f"{AZUL}Digite o nome da cidade para consulta do tempo: {RESET}").strip()
    if not cidade:
        print(f"{AMARELO}Cidade não informada. Usando São Paulo como padrão.{RESET}")
        cidade = "São Paulo"

    rscript_path = find_rscript()
    if not rscript_path:
        print(
            f"{VERMELHO}Rscript não encontrado. Instale R ou adicione ao PATH.{RESET}")
        return

    try:
        resultado = subprocess.run(
            [rscript_path, "previsao_do_tempo.r", cidade], capture_output=True, text=True, check=True)
        print(f"{VERDE}== Previsão do tempo (R) =={RESET}")
        print(resultado.stdout)
    except subprocess.CalledProcessError as exc:
        print(f"{VERMELHO}Erro ao executar R: {exc.stderr}{RESET}")
    except FileNotFoundError:
        print(f"{VERMELHO}Rscript não encontrado.{RESET}")

def exibir_comparativo() -> None:
    print(f"\n{NEGRITO}{AMARELO}=== TABELA COMPARATIVA DE MODELO ==={RESET}")

    # Bloco MANUAL
    print(f"\n{NEGRITO}[1]Irrigação Inteligente:{RESET}")
    print(f"Eficiência             : {CYAN}95% de precisão{RESET}")
    print(f"Custo                  : {CYAN}R$45.000{RESET}")
    print(f"Perda Estimada (R$)    : {VERDE}R$230 por safra {RESET}")
    print(f"Perda Estimada (kg)    : {VERDE}96kg/ha{RESET}")
    
    print(f"-" * 40)

    # Bloco MECÂNICA
    print(f"\n{NEGRITO}[2]Irrigação Atual:{RESET}")
    print(f"Eficiência             : {CYAN}60% de precisão{RESET}")
    print(f"Custo                  : {CYAN}R$N/A{RESET}")
    print(f"Perda Estimada (R$)    : {VERDE}R$1152 por safra {RESET}")
    print(f"Perda Estimada (kg)    : {VERDE}480kg/ha{RESET}")

    print(f"{AMARELO}{'-' * 40}{RESET}\n")

def solution(state: FarmData) -> None:
    """Definir gargalos e soluções."""
    if not state.cultura_ativa:
        print(f"{VERMELHO}Nenhuma cultura ativa selecionada.{RESET}")
        return

    if state.cultura_ativa.cultura == "cafe":
        print(f"\n{NEGRITO}Solução Sugerida:{RESET}")
        print(f"* Revisar processo de secagem em terreiros ou secadores.")
        print(f"* Implementar peneiramento e separação eletrônica de grãos pretos/ardidos.")
        print(f"{AMARELO} QUALIDADE AUMENTOU DE RUIM -> BOM{RESET}")
        state.cultura_ativa.status_qualidade = "BOM"
        state.cultura_ativa.qual_col = AMARELO
    elif state.cultura_ativa.cultura == "soja":
        exibir_comparativo()
        escolha = validar_int("[1]IRRIGAÇÃO INTELIGENTE, [2] MODELO ATUAL: ", [1, 2])
        if escolha == 1:
            custo_implementacao = 4500000
            state.cultura_ativa.financeiro.gastos += custo_implementacao
            calcular_financeiro(state)
            state.cultura_ativa.status_qualidade = "EXCELENTE"
            state.cultura_ativa.qual_col = VERDE
            print(f"{VERDE} QUALIDADE AUMENTOU DE BOM -> EXCELENTE!{RESET}")




        # Você pode adicionar aqui a lógica de janela de plantio
    else:
        print(f"{VERMELHO}Cultura desconhecida.{RESET}")

def problemas(state: FarmData) -> None:
    """Definir gargalos e soluções."""
    if not state.cultura_ativa:
        print(f"{VERMELHO}Nenhuma cultura ativa selecionada.{RESET}")
        return

    if state.cultura_ativa.cultura == "cafe":
        tabela_defeito = {
            "preto": 1,
            "ardido": 2,
            "verde": 5,
        }
        print(f"{CYAN}Calculo de defeito em amostra de 300g {RESET}")
        qtd_preto = validar_float(f"{AZUL}Quantidade de grãos pretos{RESET}",1)
        qtd_ardido = validar_float(f"{AZUL}Quantidade de grãos ardidos{RESET}",1)
        qtd_verde = validar_float(f"{AZUL}Quantidade de grãos verdes{RESET}",1)

        media_preto = (qtd_preto / tabela_defeito["preto"])
        media_ardido = (qtd_ardido / tabela_defeito["ardido"])
        media_verde = (qtd_verde / tabela_defeito["verde"])

        total_defeito = media_ardido + media_preto + media_verde
        if total_defeito <= 4:
            print(f"Classificação: {VERDE}Tipo 2 (Excelente Qualidade){RESET}")
            state.cultura_ativa.status_qualidade = "EXCELENTE"
            state.cultura_ativa.qual_col = VERDE
        elif total_defeito <= 26:
            print(f"Classificação: {AMARELO}Tipo 4 (Boa Qualidade){RESET}")
            state.cultura_ativa.status_qualidade = "BOM"
            state.cultura_ativa.qual_col = AMARELO
        else:
            print(f"Classificação: {VERMELHO}Tipo 7 ou inferior (Baixa Qualidade){RESET}")
            state.cultura_ativa.status_qualidade = "RUIM"
            state.cultura_ativa.qual_col = VERMELHO
            solution(state)



    elif state.cultura_ativa.cultura == "soja":
        print(f"{CYAN}Calculo de defeito da soja (umidade) {RESET}")
        umidade = validar_int(f"{AZUL}Digite a umidade do solo em (%){RESET}")
        umidade = umidade/100

        if umidade < 20:
            status = f"{VERMELHO}CRÍTICO: Solo muito seco. Risco de perda de sementes.{RESET}"
            state.cultura_ativa.status_qualidade = "RUIM"
            state.cultura_ativa.qual_col = VERMELHO
            solution(state)
        elif umidade >= 20 and umidade <25:
            status = f"{AMARELO}ATENÇÃO: Umidade no limite do aceitável.{RESET}"
            state.cultura_ativa.status_qualidade = "BOM"
            state.cultura_ativa.qual_col = AMARELO
        else:
            status = f"{VERDE}FAVORÁVEL: Condições ideais para o início da semeadura.{RESET}"
            state.cultura_ativa.status_qualidade = "EXCELENTE"
            state.cultura_ativa.qual_col = VERDE
        print(f"\n{NEGRITO}Parecer Técnico:{RESET}")
        print(f"Status: {status}")

        # Você pode adicionar aqui a lógica de janela de plantio
    else:
        print(f"{VERMELHO}Cultura desconhecida.{RESET}")

def menu() -> int:
    """Exibe o menu principal e retorna opção."""
    print(f"\n{VERDE}{NEGRITO}=== MENU PRINCIPAL ==={RESET}")
    print("1 - Dados de Plantio")
    print("2 - Manipulação de Insumos (Herbicida/Pesticida/Fertilizante/Aplicação)")
    print("3 - Financeiro")
    print("4 - Estatísticas Básicas (R)")
    print("5 - API Meteorológica (R)")
    print("6 - Exportar CSV")
    print("7 - Exibir Perfil")
    print("8 - Consultar Dados")
    print("9 - Atualização de Dados")
    print("10 - Deletar de Dados")
    print("11 - Solução de problemas")
    print(f"12 - Sair{RESET}")
    return validar_int(f"{AZUL}Selecione a opção: {RESET}", list(range(1, 13)))


def main() -> None:
    state = FarmData()

    while True:
        opcao = menu()
        if opcao == 1:
            escolher_cultura(state)
            if state.cultura_ativa and state.cultura_ativa.area == 0:
                calcular_area(state)
                calcular_insumos(state)
        elif opcao == 2:
            if not state.cultura_ativa:
                print(
                    f"{VERMELHO}Defina uma cultura ativa antes de configurar insumos.{RESET}")
                continue
            definir_herbicida(state)
            definir_pesticida(state)
            definir_fertilizante(state)
            definir_meio_aplicacao(state)
        elif opcao == 3:
            if not state.cultura_ativa:
                print(
                    f"{VERMELHO}Defina uma cultura ativa antes de calcular financeiro.{RESET}")
                continue
            calcular_financeiro(state)
            exibir_dados(state)
        elif opcao == 4:
            executar_estatisticas_r()
        elif opcao == 5:
            consultar_previsao_tempo()
        elif opcao == 6:
            exportar_csv(state)
        elif opcao == 7:
            exibir_dados(state)
        elif opcao == 8:
            consultar_dados(state)
        elif opcao == 9:
            atualizar_dados(state)
        elif opcao == 10:
            zerar_dados(state)
        elif opcao == 11:
            problemas(state)
        elif opcao == 12:
            print(f"{VERDE}Encerrando aplicação. Até breve!{RESET}")
            break


if __name__ == "__main__":
    main()
