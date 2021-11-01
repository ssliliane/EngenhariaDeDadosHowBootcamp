import requests
import pandas as pd
import json
import time
from bs4 import BeautifulSoup as bs
from os import lin, sep
from typing import AsyncIterable

##Definindo a URL de busca
url = 'https://glue-api.vivareal.com/v2/listings?addressCity=Uberlândia&addressLocationId=BR>Minas Gerais>NULL>Uberlandia&addressNeighborhood=&addressState=Minas Gerais&addressCountry=Brasil&addressStreet=&addressZone=&addressPointLat=-18.912775&addressPointLon=-48.275523&business=SALE&facets=amenities&unitTypes=HOME&unitSubTypes=CONDOMINIUM&unitTypesV3=CONDOMINIUM&usageTypes=RESIDENTIAL&listingType=USED&parentId=null&categoryPage=RESULT&includeFields=search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount),page,seasonalCampaigns,fullUriFragments,nearby(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount)),expansion(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount)),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,phones),developments(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount)),owners(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones),medias,accountLink,link)),totalCount))&size=300&from={}&q=&developmentsSize=5&__vt=&levels=CITY,UNIT_TYPE&ref=/venda/minas-gerais/uberlandia/condominio_residencial/&pointRadius='

##Criando os parâmetros de chamada
headersList = {
    "Accept" : "*/*",
    "User-Agent" : "Thunder Client (https://www.thunderclient.io",
    "x-domain" : "www.vivareal.com.br"
}

payload = ""

##Criando função para retorno dos dados
def get_json(url, i, headersList, payload):
    ret = requests.request("GET", url.format(i), data=payload, headers=headersList)
    soup = bs(ret.text, 'html.parser')
    return json.loads(soup.text)

##Criando o dataFrame com as colunas que deseja
df = pd.DataFrame(
    columns=[
        'descricao',
        'endereco',
        'area',
        'quartos',
        'suites',
        'wc',
        'garagem',
        'valor',
        'condominio',
        'wlink'
    ]
)

##Percorrendo as páginas e coletando os dados que deseja
imovel_id = 0
json_data = get_json(url, imovel_id, headersList, payload)
while len(json_data['search']['result']['listings']) > 0:
    qtd = len(json_data['search']['result']['listings'])
    print(f"Qtd de imóveis: {qtd} | total: {imovel_id}")
    for i in range(0,qtd):
        try:
            descricao = json_data['search']['result']['listings'][i]['listing']['title']
        except:
            descricao = '-'

        try:
            try:
                endereco = json_data['search']['result']['listings'][i]['listing']['address']['street']+", "+json_data['search']['result']['listings'][i]['listing']['address']['streetNumber']
            except:
                endereco = json_data['search']['result']['listings'][i]['listing']['address']['street']        
        except:
            endereco = '-'

        try:
            area = json_data['search']['result']['listings'][i]['listing']['totalArea'] 
        except:
            area = '-'

        try:
            quartos = json_data['search']['result']['listings'][i]['listing']['bedrooms']
        except:
            quartos = '-'

        try:
            suites = json_data['search']['result']['listings'][i]['listing']['suites']
        except:
            suites = '-'

        try:
            wc = json_data['search']['result']['listings'][i]['listing']['bathrooms']
        except:
            wc = '-'

        try:
            garagem = json_data['search']['result']['listings'][i]['listing']['parkingSpaces']
        except:
            garagem = '-'

        try:
            valor = json_data['search']['result']['listings'][i]['listing']['priceInfos'][0]['price']
        except:
            valor = '-'

        try:
            condominio = json_data['search']['result']['listings'][i]['listing']['priceInfos'][0]['monthlyCondoFee']
        except:
            condominio = '-'

        try:
            wlink = 'https://www.vivareal.com.br' + json_data['search']['result']['listings'][i]['link']['href']
        except:
            wlink = '-'


        df.loc[df.shape[0]] = [
            descricao,
            endereco,
            area,
            quartos,
            suites,
            wc,
            garagem,
            valor,
            condominio,
            wlink
        ]
    ##incrementa a quantidade de imoveis lidos
    imovel_id = imovel_id + qtd
    ##Só carrega 10000 imoveis, para evitar erro, se atingir a quantidade para a leitura
    if imovel_id > 10000:
        break
    time.sleep(1) ##para evitar erro 429 - muitas requisições ao servidor
    json_data = get_json(url, imovel_id, headersList, payload)

##Exportando os dados para um arquivo .csv
df.to_csv('banco_de_imoveis.csv', sep=";", index=False)