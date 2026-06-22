# 💧💻 Automação SISAGUA

## 📋 Descrição

Automação desenvolvida em Python para o lançamento de dados de qualidade da água potável no sistema **SISAGUA** (Sistema de Informação de Vigilância da Qualidade da Água para Consumo Humano), do Ministério da Saúde.

O script percorre automaticamente as seções do sistema e preenche os parâmetros físico-químicos e agrotóxicos a partir de arquivos CSV, dispensando a necessidade de input manual.

---

## 💡 Motivação

No contexto de monitoramento da qualidade da água distribuída a um município, os resultados analíticos eram recebidos em relatórios PDF emitidos por laboratórios terceiros. Após a extração e organização desses dados em planilhas CSV, o lançamento manual no SISAGUA consumia **várias horas de trabalho exclusivo** por ciclo semestral, devido ao alto volume de parâmetros por ponto de coleta.

Esta automação foi desenvolvida para eliminar esse gargalo, reduzindo drasticamente o tempo dedicado a essa tarefa e liberando horas para atividades de maior valor analítico.

---

## 🛠️ Tecnologias utilizadas

- [Python 3](https://www.python.org/)
- [Selenium](https://www.selenium.dev/) — automação do navegador
- [Pandas](https://pandas.pydata.org/) — leitura e manipulação dos dados CSV
- [Firefox WebDriver (geckodriver)](https://github.com/mozilla/geckodriver)

---

## ⚙️ Como usar

### Pré-requisitos

- Python 3 instalado
- Firefox instalado
- [geckodriver](https://github.com/mozilla/geckodriver/releases) instalado e no PATH

### Instalação

```bash
git clone https://github.com/doug-braz/automacao_sisagua.git
cd automacao_sisagua
pip install selenium pandas
```

### Configuração

No início do arquivo `Automacao_Sisagua.py`, preencha as variáveis obrigatórias:

```python
login = ''                      # CPF ou e-mail cadastrado no SISAGUA
senha = ''                      # Senha de acesso
pocos_para_lancar = []          # Lista com os nomes dos pontos de coleta
ano_lancamento = ''             # Ano de referência (ex: '2024')
semestre = 1                    # Semestre a ser lançado (1 para primeiro, 2 para segundo)
data_coleta_amostra = ''        # Data de coleta no formato DDMMYYYY (ex: '01012024')
```

### Arquivos CSV

Para cada ponto de coleta, é necessário um arquivo CSV na raiz do projeto. **O nome utilizado no arquivo CSV deve ser o mesmo inserido na lista `pocos_para_lancar`**, e esse mesmo trecho de nome deve estar contido no nome cadastrado para o poço no sistema — não precisa ser idêntico, mas o trecho precisa estar presente.

> **Exemplo:** o poço cadastrado no sistema como "Poço Brasil Centro" deve ser referenciado como `'Brasil'` na lista e ter seu arquivo nomeado como `Brasil.csv`.

Múltiplos poços podem ser adicionados à lista simultaneamente:

```python
pocos_para_lancar = ['Brasil', 'Chacara', 'Jardim']
```

O repositório inclui dois arquivos de referência:

- **`modelo_preenchido.csv`** — exemplo funcional com dados reais de entrada. Siga exatamente esse modelo ao preparar seus arquivos.
- **`modelo_vazio.csv`** — template para preenchimento. As colunas **`ordem`** e **`Análise`** não devem ser alteradas. Preencha apenas as colunas seguintes, observando as regras abaixo:

| Coluna | Formato | Exemplo |
|---|---|---|
| `Resultado` | Entre aspas. Quando o analito não é detectado (abaixo do LQ), usar `"< 0,005 mg/L"`. Quando detectado, informar apenas o valor e a unidade: `"0,20 mg/L"` | `"< 0,005 mg/L"` ou `"0,20 mg/L"` |
| `LQ` | Entre aspas | `"0,005"` |
| `Data Análise` | Sem aspas, formato DD/MM/AAAA | `01/01/2024` |

Exemplo de linhas preenchidas:

```csv
ordem,Análise,Resultado,LQ,Data Análise
1,Antimônio,"< 0,005 mg/L","0,005",01/01/2024
2,Arsênio,"< 0,005 mg/L","0,005",01/01/2024
3,Bário,"< 0,010 mg/L","0,010",01/01/2024
```

### Execução

```bash
python Automacao_Sisagua.py
```

Ao final, o terminal exibirá o tempo total de execução.

---

## ⚠️ Aviso

Este projeto foi desenvolvido para uso interno e depende de credenciais de acesso ao SISAGUA. O sistema não é de acesso público. Certifique-se de não versionar seus dados de login.

O uso desta ferramenta é de total responsabilidade do usuário. Recomenda-se conferir os dados lançados no sistema após a execução, a fim de garantir que não houve erros de preenchimento.
