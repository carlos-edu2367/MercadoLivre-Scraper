from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import sys
import random


def valorML(nome):
    # Configurações do navegador
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignora erros SSL
    # Executa em segundo plano (remova se quiser ver o navegador)
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Inicializa o navegador
    navegador = webdriver.Chrome(options=chrome_options)
    navegador.maximize_window()

    # Solicita o produto a ser pesquisado
    nome_produto = nome

    # Acessa o Mercado Livre
    navegador.get("https://www.mercadolivre.com.br/")
    time.sleep(random.uniform(2, 4))

    # Realiza a pesquisa
    navegador.find_element(
        By.CLASS_NAME, "nav-search-input").send_keys(nome_produto)
    time.sleep(random.uniform(1, 2))
    navegador.find_element(By.CLASS_NAME, "nav-search-btn").click()
    time.sleep(random.uniform(2, 4))

    # Coleta os produtos na página
    produtos = navegador.find_elements(By.CLASS_NAME, "poly-card__content")

    print(f"🔍 {len(produtos)} produtos encontrados!")

    # Inicializa variável para armazenar o produto mais barato
    valor = sys.float_info.max
    titulo_mais_barato = None
    link_mais_barato = None

    # Itera sobre os produtos
    for produto in produtos:
        try:
            # Obtém o título do produto
            titulo = produto.find_element(
                By.CLASS_NAME, "poly-component__title").text.strip()

            # Obtém o preço do produto
            preco_texto = produto.find_element(
                By.CLASS_NAME, "andes-money-amount__fraction").text
            # Remove separador de milhar e converte
            preco = float(preco_texto.replace(".", "").replace(",", "."))

            # Obtém o link do produto
            link = produto.find_element(
                By.CLASS_NAME, "poly-component__title").get_attribute("href")

            # Verifica se o título contém o nome do produto (ignorando maiúsculas/minúsculas)
            if nome_produto.lower() in titulo.lower():
                if preco < valor:  # Se for o mais barato, atualiza os valores
                    valor = preco
                    titulo_mais_barato = titulo
                    link_mais_barato = link

        except Exception as e:
            print(f"⚠ Erro ao processar um produto: {e}")

    # Exibe o resultado final
    if titulo_mais_barato and link_mais_barato:
        return titulo_mais_barato, link_mais_barato, valor
    else:
        return False

    # Fecha o navegador
    navegador.quit()
