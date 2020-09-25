### Observacoes
# 1 - para rodar eh preciso ter o geopandas e o fiona; no caso, ativar o geo_env
# 2 - considera a base hidrografica ottocodificada do Parana, disponib. pelo IAT

# para rodar tem que ativar o gen_env
# Dados de entrada
#   coexutorio - codigo da ottobacia contendo a secao exutoria
#   achs - shape contendo as Areas de Contribuicao Hidrograficas (ottobacias)

# Procedimentos..
# 1 - Encontrar a posicao do ultimo digito PAR contido em coexutorio e capturar
# todos os digitos ate essa posicao em "coesquerda"
# 2 - Filtrar o GDF: todos os codigos das ottobacias de montante devem comecar
# com "coesqueda"
# 3 - Antes de mais nada, algumas definicoes
#   coexutorio_dir = parte do codigo do exutorio que eh diferente de coesquerda
#   cobacia_dir    = parte do codigo da ottobacia que eh diferente de coesquerda
# 4 - Encontrar o primeiro digito distinto entre cobacia_dir e
# coexutorio_dir. Obs: iterar ao longo de cobaciar_dir ate encontrar um
# digto diferente, pois nunca vai ter um cobacia_dir com comprimento maior
# do que coexutorio_dir ao longo de uma string com digitos iguais
# Iterar no cobacia_dir que pode ser menor, igual ou maior que o coexutorio
# dar o break antes de ultrapassar o tamanho!
# 1


import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import itertools as iter


def ottobacias_montante(coexutorio, achs):
    if not coexutorio in achs['cobacia'].values:
        print('ERRO: coexutorio nao encontrado no shape de ACHs')
        return 0
    # 1
    pos = 0
    for i, dig_str in enumerate(coexutorio):
        dig = int(dig_str)
        if ((dig%2)==0) or (dig==9):
            pos = i
    # 2
    gdf = achs.loc[achs['cobacia'].str.startswith(coexutorio[:(pos+1)])]
    # 3
    total = len(gdf)
    count = 0
    for index, cobacia in gdf['cobacia'].items():
        count += 1
        print('Processamento {:.2f} %'.format(count/total*100))
        for i in range(pos, len(cobacia)):
            dig_bac = int(cobacia[i])
            dig_ext = int(coexutorio[i])
            if dig_bac != dig_ext:
                if dig_bac < dig_ext:
                    gdf = gdf.drop([index], axis=0)
                break
    return gdf

achs = gpd.read_file('/Users/arlan/Projetos/hidrografia-pr/REDE_Hidrografica_OTTOCODIFICADA_PR.gdb', layer=0)
# tdrs = gpd.read_file('/Users/arlan/Projetos/hidrografia-pr/REDE_Hidrografica_OTTOCODIFICADA_PR.gdb', layer=1)
coexutorio = '8642354135'
gdf = ottobacias_montante(coexutorio, achs)
