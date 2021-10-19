import requests
import pandas as pd
import collections
import sys

#Url com os resultados da lotofacil
#url = 'http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzcDbz8vTxNDRy9_Y2NQ13CDA0sTIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XMwtfQ0MPM2I02-AAzgaENIfrh-FqsQ9wBmoxN_FydLAGAgNTKEK8DkRrACPGwpyQyMMMj0VAcySpRM!/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK818G0K85260Q5OIRSC42046/res/id=historicoHTML/c=cacheLevelPage/=/'
#Colocando a url como parâmetro, pois caso ocorra mudança no endereço, não é necessário fazer alterações no código.
url = sys.argv[1]

#Chamada da url
r = requests.get(url)
r_text = r.text

#Identificando os dados no XML 
df = pd.read_html(r_text)
df = df[0].copy()

#Lista os números primos
nr_primos = [2,3,5,7,11,13,17,19,23]

#Categoriza os números
categ_num = {'pares': 0, 'impares': 0, 'primos': 0}

#Conta os números sorteados
cont_num = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0,
11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0,
19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0}

comb = []

#Lista os sorteados
lst_campos = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5',
'Bola6', 'Bola7', 'Bola8', 'Bola9', 'Bola10',
'Bola11', 'Bola12', 'Bola13', 'Bola14', 'Bola15']


for index, row in df.iterrows():
    v_pares = 0
    v_impares = 0
    v_primos = 0

    #Percorre a lista contando quandos foram sorteados
    for campo in lst_campos:
        #numeros pares 
        if (row[campo] % 2) == 0:
            categ_num['pares'] += 1
            v_pares += 1

        #números impares
        if (row[campo] % 2) != 0:
            categ_num['impares'] += 1
            v_impares += 1

        #números primos
        if (row[campo] in nr_primos):
            categ_num['primos'] += 1
            v_primos += 1

        for key in cont_num.keys():
            if key == row[campo]:
                cont_num[key] += 1

    comb.append(str(v_pares) + 'p-' + str(v_impares) + 'i-'+str(v_primos)+'np')

cont_num = [list(i) for i in cont_num.items()]

cont_num.sort(key=lambda cont_num: cont_num[1], reverse=True)

counter = collections.Counter(comb)
resultado = pd.DataFrame(counter.items(), columns=['Combinação', 'Frequencia'])
resultado['p_freq'] = (resultado['Frequencia'] / resultado['Frequencia'].sum()) 
resultado = resultado.sort_values(by=['p_freq'])

print('''
O número mais frequente é o: {}
O número menos frequente é o: {}
A combinação de Pares, Ímpares e Primos mais frequente é: {} com a frequencia de: {}%
'''.format(cont_num[0][0], cont_num[-1][0], resultado['Combinação'].values[-1], int((resultado['p_freq'].values[-1]*100)*100)/100)
)