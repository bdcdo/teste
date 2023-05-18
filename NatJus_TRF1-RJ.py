#!/usr/bin/env python
# coding: utf-8

# In[7]:


import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


# In[23]:


def extrair_pareceres_do_ano(ano):
    url = f"https://www10.trf2.jus.br/comite-estadual-de-saude-rj/nat-jus/pareceres/pareceres-{ano}/"
    pagina = requests.get(url, verify=False)
    pagina_bs = bs(pagina.content, "html.parser")
    info_pareceres = []
    tabela = pagina_bs.find('dl')
    lista_de_dt = tabela.find_all('dt')
    lista_de_dd = tabela.find_all('dd')
    
    
    for i in range(len(lista_de_dt)):
        titulo = lista_de_dt[i].text.strip()
        
        link = lista_de_dt[i].find('a').get("href").strip()
        if link.startswith(('http', '//')):
            link = link.replace('//', 'https://')
        else:
            link = "https://www10.trf2.jus.br/" + link
       
        descricao = lista_de_dd[i].text.strip()
        info_pareceres.append([titulo, ano, link, descricao])
        
    pareceres_df = pd.DataFrame(info_pareceres, columns=["Título", "Ano", "Link", "Descricao"])
    return pareceres_df


# In[26]:


anos = range(2017, 2024) # de 2017 a 2023 - tem que colocar um ano a mais
pareceres_df = pd.concat([extrair_pareceres_do_ano(ano) for ano in anos])


# In[27]:


pareceres_df.to_excel("trfrj1.xlsx")

