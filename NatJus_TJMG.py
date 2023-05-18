#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

import re


# In[22]:


urls = [
    "https://bd.tjmg.jus.br/jspui/handle/tjmg/7735/browse?type=dateissued&sort_by=2&order=DESC&rpp=100&etal=-1&null=&offset=",
    "https://bd.tjmg.jus.br/jspui/handle/tjmg/7736/browse?type=dateissued&sort_by=2&order=DESC&rpp=100&etal=-1&null=&offset=0",
    "https://bd.tjmg.jus.br/jspui/handle/tjmg/7737/browse?type=dateissued&sort_by=2&order=DESC&rpp=100&etal=-1&null=&offset="
]

max_offsets = [2100, 0, 1700]

categorias = ["Nota Técnica", "Parecer Técnico", "Parecer Técnico"]

info_pareceres = []

for i, url_base in enumerate(urls):
    offset = 0
    categoria = categorias[i]

    while offset <= max_offsets[i]:
        print(f"Coletando dados da página {offset // 100 + 1} do link {i+1}")
        link = url_base + str(offset)
        pareceres = requests.get(link)
        pareceres_bs = bs(pareceres.content, "lxml")

        tabela = pareceres_bs.find('table', attrs={'class':'miscTable'})
        lista_de_tr = tabela.find_all('tr')

        if len(lista_de_tr) <= 1:
            break

        for tr in lista_de_tr[1:]:
            dados = tr.find_all('td')
            data = dados[1].text.strip()
            ano = int(data[-4:])
            titulo = dados[2].text.strip()
            link_tag = dados[2].find("a")
            link = "https://bd.tjmg.jus.br/" + link_tag.get("href").strip() if link_tag is not None else ""

            info_pareceres.append([ano, data, titulo, categoria, link])

        offset += 100


# In[24]:


pareceres_df = pd.DataFrame(info_pareceres)
pareceres_df.columns = ["Ano", "Data", "Título", "Tipo de Documento", "Link"]

pareceres_df.to_excel("tjmg1.xlsx")

