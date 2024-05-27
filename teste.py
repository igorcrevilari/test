#importando arquivos
import pyautogui
from time import sleep
import pandas as pd
from urllib.parse import quote
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

relatorio = pd.read_excel('phishing.xlsx') #importa o arquivo

#Tratando link 
for linha in relatorio.index:
    url_hash = "http://testefieb.meusite.space/?rid="
    hashId = str(relatorio.loc[linha, "link"])
    url_hash = url_hash + hashId
    relatorio.loc[linha, "link"] = url_hash

#Iniciando navegador para LOGIN no WhatsApp Web
navegador = webdriver.Chrome()
navegador.get("https://web.whatsapp.com/")

# esperar a tela do whatsapp carregar -> espera um elemento que só existe na tela já carregada aparecer
while len(navegador.find_elements(By.ID, 'side')) < 1: # -> lista for vazia -> que o elemento não existe ainda
    sleep(1)

#iteração para ler linha por linha
for linha in relatorio.index:
    #linha[x] - o "x" se refere a coluna lida na linha
    telefone = relatorio.loc[linha, "whatsapp"]
    nome = relatorio.loc[linha, "nome"]
    link = relatorio.loc[linha, "link"]

    mensagem = (f"Olá, {nome}! Atualize o seu e-mail corporativo, com as novas regras de atualizações você poderá perder o acesso a conta.\n"
        f"Acesse o link abaixo para a atualização do Teams:\n"
        f"{link}")
    url_whatsapp = f"https://web.whatsapp.com/send?phone={telefone}=&text={quote(mensagem)}" #o método quote irá criptografar o conteúdo da variável mensagem

    #Para funcionar, o WhatsApp Web deverá estar logado
    navegador.get(url_whatsapp)
    sleep(15)

    # esperar a tela do whatsapp carregar -> espera um elemento que só existe na tela já carregada aparecer
    while len(navegador.find_elements(By.ID, 'side')) < 1: # -> lista for vazia -> que o elemento não existe ainda
        sleep(1)
    sleep(2)

 # você tem que verificar se o número é inválido
    if len(navegador.find_elements(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]')) < 1:
        # enviar a mensagem
        navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span').click()
        print("Número encontrado!")
    elif len(navegador.find_elements(By.XPATH,'//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div')) < 1:
        navegador.find_elements(By.XPATH,'//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/button/div/div').click()
        print("Número não encontrado!")
    sleep(10)
