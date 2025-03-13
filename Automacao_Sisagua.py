from selenium.webdriver import Firefox
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import time
from selenium.webdriver.common.keys import Keys

inicio = time.time()

url = 'http://sisagua.saude.gov.br/sisagua/login.jsf'

options = webdriver.FirefoxOptions()

#! Dados a serem alimentados para o funcionamento da automação
login = '' # Inserir CPF ou email cadastrado entre os apóstrofos

senha = '' # Senha para acesso ao sistema

pocos_para_lancar = ['Morumbi','Nacoes','Village','Ubirama'] #* O nome de cada poço inserido nessa lista deve ser compatível com o nome do arquivo CSV para lançamento (NOME_DO_POCO.csv) e o nome que está cadastrado no sistema 

ano_lancamento = '2024' #* Inserir o ano a ser lançado

semestre = 1 #* Inserir qual o semestre a ser lançado

#* Login no sistema
driver = Firefox()
driver.get(url)
sleep(5)
login_input = driver.find_element(By.ID, "email")
sleep(1)
login_input.send_keys(login)
sleep(1)
password_input = driver.find_element(By.ID, "senha")
sleep(1)
password_input.send_keys(senha)
sleep(1)
botao = driver.find_element(By.ID, "btnEntrar")
botao.click()
sleep(1)

def preenchimento(parametro):
    # Esta função tem o objetivo de varrer todos os parâmetros fisico-químicos de uma seção do SISÁGUA, consultar o dataframe do resultado relatado em relatório e lançá-lo de acordo com seu resultado, obedecendo às regras de preenchimento do sistema. O argumento passado para ela é uma lista python com os parâmetros de um dos grandes blocos de lançamento do site (substâncias inorgânicas, orgânicas, agrotóxicos e organolépticos)

    for indice, item in enumerate(parametro):
        try:
            link = driver.find_element(By.XPATH, f"//a[contains(text(), '{item}')]")
            link.click()
            sleep(5)
            

            campo = driver.find_element(By.ID, f"accordionAnalise:{indice}:loopPA:0:loopCA:0:dataColeta_input")
            campo.send_keys("26012024"+Keys.TAB)
            sleep(5)
            
            campo = driver.find_element(By.ID, f"accordionAnalise:{indice}:loopPA:0:loopCA:1:dataAnalise_input")
            campo.send_keys(df.loc[df["Análise"].str.contains(item, na=False, case=False), "Data Análise"].values[0] + Keys.TAB)
            sleep(5)

            if df.loc[df["Análise"].str.contains(item, na=False, case=False), "Resultado"].values[0].split()[0] == "<":
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.TAB)
                sleep(5)
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ARROW_DOWN)
                sleep(5)

            else:
                campo = driver.find_element(By.ID, f"accordionAnalise:{indice}:loopPA:0:loopCA:2:campoResultado")
                campo.send_keys(df.loc[df["Análise"].str.contains(item, na=False, case=False), "Resultado"].values[0].split()[0])
                sleep(5)

            if 'Gosto' not in item:
                campo = driver.find_element(By.ID, f"accordionAnalise:{indice}:loopPA:0:loopCA:5:j_idt376")
                campo.send_keys(df.loc[df["Análise"].str.contains(item, na=False, case=False), "LQ"].values[0])
                sleep(5)

            botao = driver.find_element(By.ID, f"accordionAnalise:{indice}:j_idt389")
            botao.click()
            sleep(10)
            
        except Exception as e:
            print(f"Erro ao clicar no link '{item}': {e}")
            
    botao = driver.find_element(By.ID, "btnSalvarAnalise")
    botao.click()
    sleep(20)


for poco in pocos_para_lancar:
    driver.get('http://sisagua.saude.gov.br/sisagua/paginas/seguro/controleSaaSemestral/controleSaaSemestral.jsf?faces-redirect=true')

    ano = driver.find_element(By.ID, 'ano_label')
    ano.click()
    sleep(1)

    ano = driver.find_element(By.CSS_SELECTOR, f'li[data-label="{ano_lancamento}"]')
    ano.click()
    sleep(5)

    nome_poco = driver.find_element(By.ID, 'nomeSaa')
    nome_poco.send_keys(poco)

    botao = driver.find_element(By.ID, 'btConsultar')
    botao.click()

    sleep(5)

    botao = driver.find_element(By.ID, 'listaSaas:0:alterar')
    botao.click()
    sleep(5)

    if semestre == 2: #* Não é necessário clicar em nada caso o semestre a ser lançado é o primeiro
        link_parcial = driver.find_element(By.XPATH, "//a[contains(text(), '2° Semestre')]")
        link_parcial.click()
        sleep(5)

    botao = driver.find_element(By.ID, f'tabView:{"0" if semestre==1 else "1"}:listaEtas:0:detalharBTN')
    botao.click()
    sleep(10)

    import pandas as pd

    ARQUIVO_CSV = f'{poco}.csv'
    df = pd.read_csv(ARQUIVO_CSV)

    #!LANCAMENTO INORGANICOS
    INORGS = ['Antimônio', 'Arsênio', 'Bário', 'Cádmio', 'Chumbo', 'Cobre', 'Cromo', 'Mercúrio', 'Níquel', 'Nitrato', 'Nitrito', 'Selênio', 'Urânio']
    botao = driver.find_element(By.ID, f'tabView:{"0" if semestre==1 else "1"}:j_idt239:0:j_idt244')
    botao.click()
    sleep(5)

    preenchimento(INORGS)

    #! LANCAMENTO ORGANICOS
    ORGS = ['Dicloroetano', 'Acrilamida', 'Benzeno', 'pireno', 'Cloreto de Vinila', 'ftalato', 'Diclorometano', 'Dioxano', 'Epicloridrina', 'Etilbenzeno', 'Pentaclorofenol', 'Tetracloreto de Carbono', 'Tetracloroeteno', 'Tolueno', 'Tricloroeteno', 'Xilenos']
    botao = driver.find_element(By.ID, f'tabView:{"0" if semestre==1 else "1"}:j_idt239:1:j_idt244')
    botao.click()
    sleep(5)

    preenchimento(ORGS)

    #! LANCAMENTO AGROTOXICOS
    AGROTOX = ['2,4', 'Alaclor', 'Aldicarb', 'Aldrin', 'Ametrina', 'Atrazina', 'Carbendazim', 'Carbofurano', 'Ciproconazol', 'Clordano', 'Clorotalonil', 'Clorpirif', 'DDT', 'Difenoconazol', 'Dimetoato', 'Diuron', 'Epoxiconazol', 'Fipronil', 'Flutriafol', 'Glifosato', 'Hidroxi', 'Lindano', 'Malation', 'Mancozebe', 'Metamidofós', 'Metolacloro', 'Metribuzim', 'Molinato', 'Paraquate', 'Picloram', 'Profenof', 'Propargito', 'Proti', 'Simazina', 'Tebuconazol', 'Terbuf', 'Tiametoxam', 'Tiodicarbe', 'Tiram', 'Trifluralina']
    botao = driver.find_element(By.ID, f'tabView:{"0" if semestre==1 else "1"}:j_idt239:2:j_idt244')
    botao.click()
    sleep(5)

    preenchimento(AGROTOX)

    #! Lancamento - Organolepticos
    ORGANOLEP = ['1,2 Diclorobenzeno', '1,4 Diclorobenzeno', 'Alumínio', 'Amônia', 'Cloreto -', 'Dureza', 'Ferro', 'Gosto e odor', 'Manganês', 'Monoclorobenzeno', 'Sódio', 'Sólidos', 'Sulfato', 'Sulfeto de hidrogênio', 'Zinco']
    botao = driver.find_element(By.ID, f'tabView:{"0" if semestre==1 else "1"}:j_idt239:3:j_idt244')
    botao.click()
    sleep(5)

    preenchimento(ORGANOLEP)


fim = time.time()

tempo_decorrido = (fim - inicio)/60

print(f'Todos os poços lançados com sucesso! Tempo de execução: {tempo_decorrido:.2f} minutos')

