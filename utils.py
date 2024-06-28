import requests
from bs4 import BeautifulSoup
import re

def get_kabum_promotions():
    domain = 'https://www.kabum.com.br'
    url = f'{domain}/hardware/kit-hardware/kit-upgrade?page_number=1&page_size=100&facet_filters=&sort=offer_price'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.google.com',
    }

    site = requests.get(url, headers=headers)
    if site.status_code != 200:
        print(f"Erro ao acessar o site da Kabum: {site.status_code}")
        return []

    soup = BeautifulSoup(site.content, 'html.parser')

    produtos = soup.find_all('article', class_=re.compile('productCard'))
    if not produtos:
        print("Nenhum produto encontrado na Kabum.")

    promotions = []

    for produto in produtos:
        try:
            marca = produto.find('span', class_=re.compile('nameCard')).get_text(strip=True)
            preco = produto.find('span', class_=re.compile('priceCard')).get_text(strip=True)
            link = produto.find('a')['href']
            link = f"{domain}{link}"
            promotions.append(f"{marca} - {preco}\n{link}")
        except AttributeError:
            print("Erro ao processar um produto.")
            continue

    return promotions

def kabum_teste():
    import math
    import re
    import requests
    from bs4 import BeautifulSoup

    domain = 'https://www.kabum.com.br'
    url = f'{domain}/hardware/placa-de-video-vga/placa-de-video-nvidia'
    headers = {'User-Agent': 'Mozilla/5.0'}

    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    qtd_itens = soup.find('div', id='listingCount').get_text().strip()

    index = qtd_itens.find(' ')
    qtd = qtd_itens[:index]

    ultima_pagina = math.ceil(int(qtd) / 20)

    dic_produtos = {'marca': [], 'preco': []}

    for i in range(1, ultima_pagina + 1):
        domain = 'https://www.kabum.com.br'
        url_pag = f'{domain}/hardware/placa-de-video-vga/placa-de-video-nvidia?page_number={i}&page_size=20&facet_filters=&sort=offer_price'
        site = requests.get(url_pag, headers=headers)
        soup = BeautifulSoup(site.content, 'html.parser')

        produtos = soup.find_all('article', class_=re.compile('productCard'))

        for produto in produtos:
            marca = produto.find('span', class_=re.compile('nameCard'))
            marca_texto = marca.get_text(strip=True) if marca else ''
            print(marca_texto)
            dic_produtos['marca'].append(marca_texto)