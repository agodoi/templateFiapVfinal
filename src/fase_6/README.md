# Fase 6 — O Despertar da Rede Neural

## Identificação

**Fase:** 6  
**Capítulo:** 1  
**Grupo:** H.M.N.R.V.  
**Entregáveis contemplados:** 1 e 2

---
## ATENÇÃO 🚨🚨
Para rodar o notebook na sua máquina, abra o arquivo "classificar.yaml" e substitua "CAMINHO AQUI" pelo caminho das pastas do seu *próprio drive*
## Descrição da Atividade

Este projeto aplica técnicas de **Visão Computacional e Deep Learning** para reconhecer objetos em imagens utilizando duas classes: **Copo** e **Taça**.

A solução foi organizada em um único notebook e contempla três abordagens:

1. **YOLOv5 customizada**, treinada especificamente para as classes do projeto;
2. **YOLOv5s pré-treinada no COCO**, utilizada sem customização;
3. **CNN criada do zero com TensorFlow/Keras**, utilizada para classificação das imagens.

O objetivo é comparar as abordagens em termos de desempenho, tempo de treinamento, tempo de inferência quando disponível e facilidade de integração, respeitando a diferença entre **detecção de objetos** e **classificação de imagens**.

> **Observação metodológica:** as métricas de YOLO e CNN não são diretamente equivalentes. A YOLO é avaliada principalmente por métricas de detecção, como `mAP`, enquanto a CNN é avaliada por `accuracy` e `loss`.

---

## Integrantes

- Heitor Exposito de Sousa — RM 566013
- Marco Antônio Rodrigues Siqueira — RM 569975
- Nádia Nakamura Vieira — RM 568906
- Rafael Bassani — RM 569930
- Vinicius Xavier da Silva — RM 572108

---

## Tecnologias e Bibliotecas

As principais tecnologias utilizadas no notebook são:

- **Python**
- **Google Colab**
- **Google Drive**
- **YOLOv5 / Ultralytics**
- **TensorFlow / Keras**
- **Pandas**
- **Matplotlib**
- **Seaborn**
- **Scikit-learn**
- **PyYAML**

---

# Estrutura Geral da Solução

A implementação foi dividida em quatro partes principais:

```text
PARTE A — YOLO customizada
    ├── Validação do dataset
    ├── Treinamento com 20 épocas
    ├── Validação do modelo
    ├── Treinamento com 40 épocas
    ├── Validação do modelo
    ├── Comparação de métricas
    └── Inferência no conjunto de teste

PARTE B — YOLO pré-treinada
    └── Inferência com yolov5s.pt treinada no COCO

PARTE C — CNN criada do zero
    ├── Preparação do dataset
    ├── Construção da arquitetura
    ├── Treinamento
    ├── Curvas de aprendizado
    ├── Avaliação no conjunto de teste
    └── Matriz de confusão

PARTE D — Comparação final
    ├── Comparação quantitativa
    ├── Comparação qualitativa
    └── Conclusões
```

---

# Dataset

## Dataset utilizado pela YOLO

O arquivo `classificar.yaml` contém duas classes:

```text
0 — Copo
1 — Taca
```

Na execução registrada no notebook, foram identificadas:

| Divisão | Total de imagens | Copo | Taça | Imagens sem rótulo |
|---|---:|---:|---:|---:|
| Treino | 72 | 36 | 36 | 0 |
| Validação | 8 | 4 | 4 | 0 |

Também foram encontrados **80 arquivos de anotação `.txt`** abaixo do diretório-base utilizado pela YOLO.

A pasta de teste foi configurada separadamente por meio de `TEST_PATH` e utilizada nas inferências dos modelos. O notebook confirma a existência dessa pasta, mas não registra em tabela a quantidade total de imagens presente nela.

### Organização esperada

```text
RedeNeuralYolo/
├── classificar.yaml
├── images/
│   ├── train/
│   └── val/
├── labels/
│   ├── train/
│   └── val/
└── test/
```

---

## Dataset utilizado pela CNN

Para a CNN foi utilizada uma estrutura própria de classificação, separada em diretórios por classe:

```text
CNN/
├── train/
│   ├── Classe0/
│   └── Classe1/
├── val/
│   ├── Classe0/
│   └── Classe1/
└── test/
    ├── Classe0/
    └── Classe1/
```

Na execução do notebook foram carregadas:

| Divisão | Quantidade de imagens |
|---|---:|
| Treino | 101 |
| Validação | 16 |
| Teste | 36 |

As imagens foram redimensionadas para **150 × 150 pixels**, com `batch_size=32`.

---

# Entrega 1 — YOLOv5 Customizada

A primeira abordagem utiliza a **YOLOv5s** com pesos `yolov5s.pt` como ponto de partida. Esses pesos são utilizados para inicialização, mas o modelo é treinado especificamente para as classes **Copo** e **Taça**.

Foram realizados dois experimentos mantendo os mesmos parâmetros principais e alterando o número de épocas.

## Experimento 1 — 20 épocas

Configuração principal:

```text
Modelo base: yolov5s.pt
Tamanho da imagem: 640
Épocas: 20
```

Tempo de treinamento registrado:

**1068,22 segundos**, aproximadamente **17,8 minutos**.

O modelo gerado foi posteriormente validado com `val.py`.

Tempo de validação:

**19,50 segundos**.

### Melhores métricas observadas no histórico

| Métrica | Resultado |
|---|---:|
| Precision máxima | 0,70886 |
| Recall máximo | 1,00000 |
| mAP@0.5 máximo | 0,78250 |
| mAP@0.5:0.95 máximo | 0,46053 |

---

## Experimento 2 — 40 épocas

O segundo treinamento manteve os mesmos parâmetros do primeiro e alterou somente a quantidade de épocas.

```text
Modelo base: yolov5s.pt
Tamanho da imagem: 640
Épocas: 40
```

Tempo de treinamento registrado:

**1987,35 segundos**, aproximadamente **33,1 minutos**.

Tempo de validação:

**19,81 segundos**.

### Melhores métricas observadas no histórico

| Métrica | Resultado |
|---|---:|
| Precision máxima | 0,97348 |
| Recall máximo | 1,00000 |
| mAP@0.5 máximo | 0,99500 |
| mAP@0.5:0.95 máximo | 0,62994 |

---

## Comparação dos treinamentos da YOLO

| Critério | 20 épocas | 40 épocas |
|---|---:|---:|
| Tempo de treinamento | 1068,22 s | 1987,35 s |
| Precision máxima | 0,70886 | 0,97348 |
| Recall máximo | 1,00000 | 1,00000 |
| mAP@0.5 máximo | 0,78250 | 0,99500 |
| mAP@0.5:0.95 máximo | 0,46053 | 0,62994 |

O experimento de **40 épocas apresentou os maiores valores de Precision, mAP@0.5 e mAP@0.5:0.95** registrados no notebook.

O ganho de desempenho veio acompanhado de maior custo de treinamento: o tempo passou de aproximadamente **17,8 minutos para 33,1 minutos**.

O notebook também gera e exibe, para os dois treinamentos:

- matriz de confusão;
- curva Precision-Recall;
- curva de Precision;
- curva de Recall;
- curva F1;
- evolução das principais métricas ao longo das épocas.

---

## Inferência no conjunto de teste

Os dois modelos customizados foram executados sobre a mesma pasta de teste.

Tempos totais registrados:

| Modelo | Tempo total de inferência |
|---|---:|
| YOLO customizada — 20 épocas | 18,92 s |
| YOLO customizada — 40 épocas | 9,00 s |

As execuções utilizam `detect.py` e salvam:

- imagens processadas;
- rótulos detectados;
- confiança das detecções.

> Os tempos acima correspondem ao tempo total registrado pelo notebook para cada execução e não representam, isoladamente, uma comparação normalizada de tempo médio por imagem.

---

# Entrega 2 — Comparação com Outras Abordagens

## YOLOv5s Pré-treinada no COCO

Para comparação, foi executada uma **YOLOv5s padrão**, utilizando diretamente os pesos `yolov5s.pt`, sem novo treinamento nas classes do projeto.

O objetivo desta etapa é observar o comportamento de um modelo genérico nas mesmas imagens utilizadas no teste.

Tempo total de inferência registrado:

**7,98 segundos**.

### Limitação observada

A YOLO pré-treinada reconhece somente as classes existentes no dataset **COCO**.

Consequentemente, ao processar as imagens do projeto, ela pode:

- reconhecer objetos por classes semanticamente próximas;
- não reconhecer uma das classes utilizadas no trabalho;
- identificar outros objetos presentes na cena.

Por esse motivo, o notebook trata essa abordagem principalmente de forma **qualitativa**, e não apresenta uma métrica numérica equivalente ao mAP dos modelos customizados.

---

# CNN Criada do Zero

A terceira abordagem foi construída com **TensorFlow/Keras**, sem utilização de uma arquitetura pré-treinada.

A rede implementada no notebook contém:

```text
Rescaling
↓
Conv2D
↓
MaxPooling
↓
Flatten
↓
Dense
↓
Dense
↓
Sigmoid
```

A camada `Rescaling` normaliza os pixels entre 0 e 1.

Como o problema é de classificação binária, a camada final utiliza ativação **sigmoid**.

## Configuração de treinamento

O modelo foi compilado com:

```text
Otimizador: Adam
Loss: binary_crossentropy
Métrica: accuracy
Máximo de épocas: 50
```

Também foi utilizado **EarlyStopping**, monitorando `val_accuracy`, com:

```text
patience = 5
restore_best_weights = True
```

Isso permite interromper o treinamento quando a acurácia de validação deixa de melhorar e restaurar os melhores pesos encontrados.

---

## Resultados da CNN

Tempo de treinamento registrado:

**212,22 segundos**, aproximadamente **3,5 minutos**.

No conjunto independente de teste:

| Métrica | Resultado |
|---|---:|
| Loss | 0,6140 |
| Accuracy | 0,7222 |
| Accuracy percentual | 72,22% |

O notebook também apresenta:

- curvas de acurácia de treino e validação;
- curvas de loss;
- previsões sobre o conjunto de teste;
- matriz de confusão.

Durante o treinamento registrado, a acurácia de validação apresentou oscilações entre as épocas, enquanto a acurácia de treinamento chegou a valores mais elevados em diferentes momentos. O uso de `EarlyStopping` foi adotado justamente para controlar o processo de treinamento com base no desempenho de validação.

---

# Comparação Final

## Comparação quantitativa registrada no notebook

| Abordagem | Treinada nas classes do projeto | Métrica principal | Resultado | Tempo de treinamento | Tempo total de inferência |
|---|---|---|---:|---:|---:|
| YOLO customizada — 20 épocas | Sim | mAP@0.5 | 0,78250 | 1068,22 s | 18,92 s |
| YOLO customizada — 40 épocas | Sim | mAP@0.5 | 0,99500 | 1987,35 s | 9,00 s |
| YOLOv5s pré-treinada (COCO) | Não | Análise qualitativa | N/A | 0 s | 7,98 s |
| CNN criada do zero | Sim | Accuracy | 0,72222 | 212,22 s | 3.3608 s |

> **Importante:** `mAP@0.5` e `accuracy` medem aspectos diferentes e não devem ser interpretados como se fossem a mesma métrica.

---

## Comparação qualitativa

| Abordagem | Vantagens observadas | Limitações observadas | Facilidade de integração |
|---|---|---|---|
| YOLO customizada — 20 épocas | Treinamento mais rápido entre os dois experimentos YOLO; detecta e localiza objetos | Apresentou métricas inferiores ao treinamento de 40 épocas | Alta |
| YOLO customizada — 40 épocas | Apresentou os maiores valores de Precision e mAP entre os treinamentos customizados | Exigiu maior tempo de treinamento | Alta |
| YOLOv5s pré-treinada | Não exige novo treinamento | Limitada às classes do COCO e não foi treinada especificamente para Copo e Taça | Muito alta |
| CNN criada do zero | Arquitetura controlada pela equipe e treinamento relativamente rápido | Resolve classificação, não localização; resultado de teste foi de 72,22% | Alta |

---

# Análise dos Resultados

## Efeito do aumento de épocas na YOLO customizada

O aumento de **20 para 40 épocas** elevou o tempo de treinamento de **1068,22 s para 1987,35 s**.

Ao mesmo tempo, foram observadas melhorias nas métricas máximas:

- `Precision`: **0,70886 → 0,97348**
- `mAP@0.5`: **0,78250 → 0,99500**
- `mAP@0.5:0.95`: **0,46053 → 0,62994**

O `Recall` máximo chegou a **1,0** nos dois experimentos.

Dentro dos resultados registrados no notebook, o modelo de **40 épocas apresentou o melhor desempenho entre os dois treinamentos customizados**, embora tenha demandado aproximadamente o dobro do tempo de treinamento.

---

## YOLO customizada versus YOLO pré-treinada

A YOLO customizada foi treinada especificamente para reconhecer **Copo** e **Taça**.

A YOLO padrão utilizada na comparação foi treinada no COCO e não passou por treinamento específico para essas duas classes.

Por isso, a YOLO padrão foi utilizada como referência qualitativa. O notebook não atribui a ela um mAP específico para o problema do projeto.

Essa diferença demonstra a importância da customização quando o objetivo envolve classes específicas que não correspondem diretamente às categorias disponíveis no modelo genérico.

---

## YOLO versus CNN

As abordagens solucionam problemas diferentes.

### YOLO

A YOLO realiza:

```text
Detecção = classificação + localização
```

Ela identifica a classe e também informa onde o objeto está presente na imagem por meio de bounding boxes.

### CNN

A CNN implementada realiza:

```text
Classificação = classe da imagem
```

Ela determina a qual classe a imagem pertence, mas não fornece a localização do objeto.

Por isso, comparar diretamente o `mAP` da YOLO com a `accuracy` da CNN não seria metodologicamente adequado.

O resultado da CNN no conjunto de teste foi de **72,22% de acurácia**, enquanto a YOLO customizada de 40 épocas registrou **mAP@0.5 máximo de 0,995** no histórico de treinamento.

Esses valores devem ser interpretados dentro das respectivas tarefas.

---

# Pontos Fortes da Solução

Com base na execução registrada no notebook, destacam-se:

- utilização de duas classes;
- separação entre treinamento, validação e teste;
- validação automática da estrutura do dataset YOLO;
- confirmação da existência das anotações `.txt`;
- dois experimentos controlados de treinamento da YOLO;
- coleta de métricas de Precision, Recall e mAP;
- geração de curvas e matrizes de confusão;
- inferência sobre imagens de teste;
- comparação com YOLO pré-treinada;
- implementação de uma CNN do zero;
- uso de Early Stopping;
- avaliação da CNN em conjunto de teste independente;
- comparação quantitativa e qualitativa das abordagens.

---

# Limitações Identificadas

A própria estrutura e os resultados registrados no notebook evidenciam algumas limitações que devem ser consideradas:

1. **As métricas máximas da YOLO são extraídas do histórico de treinamento.**  
   Precision, Recall e mAP apresentados na tabela correspondem aos maiores valores encontrados nas respectivas colunas de `results.csv`.

2. **O conjunto de teste da YOLO é utilizado na inferência, mas sua quantidade total de imagens não é exibida na tabela de validação do dataset.**

3. **YOLO e CNN trabalham com estruturas de dados diferentes.**  
   A YOLO usa imagens com bounding boxes, enquanto a CNN utiliza imagens organizadas por classe.

4. **mAP e accuracy não são diretamente comparáveis.**  
   Portanto, a análise entre YOLO e CNN deve considerar também a natureza da tarefa executada por cada modelo.

5. **A YOLO pré-treinada não foi treinada nas classes do projeto.**  
   Assim, sua avaliação é qualitativa e limitada às categorias aprendidas no COCO.



---

# Conclusão

Foram avaliadas três abordagens de Visão Computacional: **YOLOv5 customizada**, **YOLOv5s pré-treinada no COCO** e **CNN construída do zero**.

Na YOLO customizada, o aumento de 20 para 40 épocas elevou o tempo de treinamento de aproximadamente **17,8 para 33,1 minutos**, mas também aumentou as principais métricas registradas.

O modelo de 20 épocas atingiu:

```text
Precision máxima: 0,70886
Recall máximo: 1,00000
mAP@0.5 máximo: 0,78250
mAP@0.5:0.95 máximo: 0,46053
```

Já o modelo de 40 épocas atingiu:

```text
Precision máxima: 0,97348
Recall máximo: 1,00000
mAP@0.5 máximo: 0,99500
mAP@0.5:0.95 máximo: 0,62994
```

Entre os dois treinamentos customizados executados, **40 épocas apresentou os melhores resultados registrados**, em troca de maior tempo de processamento.

A YOLOv5s pré-treinada foi executada diretamente nas imagens de teste e apresentou tempo total de inferência de **7,98 segundos**, porém sua análise é limitada pelo fato de o modelo reconhecer as classes do COCO e não ter sido customizado especificamente para Copo e Taça.

A CNN criada do zero foi treinada em aproximadamente **3,5 minutos** e atingiu **72,22% de acurácia no conjunto de teste**, com `loss` de **0,6140**.

A comparação evidencia que a escolha da arquitetura depende do problema a ser resolvido:

- a **YOLO customizada** é adequada quando é necessário identificar **qual objeto está presente e onde ele se encontra**;
- a **CNN** é adequada para cenários de **classificação**, nos quais a imagem deve ser associada a uma classe;
- a **YOLO pré-treinada** oferece alta facilidade de uso, porém fica limitada às classes aprendidas anteriormente no COCO quando não há customização.

Dentro dos experimentos realizados no notebook, a **YOLO customizada com 40 épocas apresentou o melhor desempenho de detecção entre os modelos customizados avaliados**.

---

# Como Executar o Notebook

O notebook foi desenvolvido para execução no **Google Colab** e utiliza dados armazenados no Google Drive.

## 1. Organize os dados no Google Drive

O caminho-base utilizado pela YOLO é:

```text
/content/drive/MyDrive/Cap 1 - O despertar da Rede Neural/RedeNeuralYolo
```

O notebook utiliza:

```text
classificar.yaml
images/train
images/val
labels/train
labels/val
test
```

A CNN utiliza uma estrutura própria dentro da pasta correspondente ao conjunto de classificação.

## 2. Abra o notebook no Google Colab

Notebook principal:

`MarcoSiqueira_rm569975_pbl_fase6_entrega1&2_unificada.ipynb`

[**Acessar notebook no Google Colab**](https://colab.research.google.com/drive/1Y-jDRm9pqECWsGKeNOTVH8ZvC7s0NgoW?usp=sharing)

## 3. Ative a GPU

No Google Colab:

```text
Ambiente de execução
→ Alterar tipo de ambiente de execução
→ GPU
```

## 4. Execute as células em sequência

O notebook:

1. monta o Google Drive;
2. instala o YOLOv5 e dependências;
3. valida a configuração do dataset;
4. treina e valida os modelos YOLO;
5. executa os testes;
6. executa a YOLO pré-treinada;
7. treina e avalia a CNN;
8. gera a comparação final.

---

# Vídeo Demonstrativo

O vídeo contempla **as Entregas 1 e 2**, apresentando o funcionamento e os principais resultados do projeto.

[**Assistir ao vídeo demonstrativo no YouTube**](https://youtube.com/watch?v=v5UiTAw8Jhc&feature=youtu.be)

---

# Arquivo Principal

```text
MarcoSiqueira_rm569975_pbl_fase6_entrega1&2_unificada.ipynb
```

O notebook concentra o desenvolvimento das duas entregas, os experimentos, as métricas, as avaliações e as conclusões apresentadas neste README.

---

## Resumo dos Resultados

| Modelo | Resultado principal | Treinamento | Inferência |
|---|---:|---:|---:|
| YOLO customizada — 20 épocas | mAP@0.5 = 0,78250 | 17,8 min | 18,92 s |
| YOLO customizada — 40 épocas | mAP@0.5 = 0,99500 | 33,1 min | 9,00 s |
| YOLOv5s pré-treinada | Análise qualitativa | Não aplicável | 7,98 s |
| CNN do zero | Accuracy = 72,22% | 3,5 min |3.3608 s  |

---

**FarmTech Solutions — FIAP | Fase 6 — Visão Computacional e Redes Neurais**
