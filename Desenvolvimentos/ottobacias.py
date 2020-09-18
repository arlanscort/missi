# para rodar tem que ativar o gen_env

import pandas as pd
import fiona
import geopandas as gpd



#sanepar = gpd.read_file('Bacia_de_Mananciais_Ativos.shp')
shapes = fiona.listlayers('/Users/arlan/Arquivos-Fixos/REDE_Hidrografica_OTTOCODIFICADA_PR.gdb')
achs = shapes[0] # Areas de Contribuição Hidrográfica
ottobac_IAT = gpd.read_file('/Users/arlan/Arquivos-Fixos/REDE_Hidrografica_OTTOCODIFICADA_PR.gdb', \
            layer=achs)

# Teste para o reservatorio de Fiu
coexutorio = '8642354535'



# Procedimentos
# 1 - Encontrar a posicao do ultimo digito par contido em codigo_exutorio
pos = 0
for i,dig in enumerate(coexutorio):
    if (int(dig)%2) == 0:
        pos = i
coesquerda = coexutorio[:(pos+1)]
gdf1 = ottobac_IAT.loc[ottobac_IAT['cobacia'].str.startswith(coesquerda)]

# 2 -
coexutorio_dir = coexutorio[(pos+1):]
for index, cobacia in gdf1['cobacia'].items():
    cobacia_dir = cobacia[(pos+1):]

    # 2 - Dropar as cobacias cujo primeiro digito da parte codigo a direita eh
    # menor que o digito correspondente do codigo do exutorio
    for pos, dig in enumerate(coexutorio_dir):
        if int(cobacia_dir[pos]) < int(dig):
            gdf2 = gdf1.drop([index], inplace=True)
            break
        if int(cobacia_dir[pos]) > int(dig):
            break



# C1 - nao tem digitos diferentes - NAO FAZ NADA (JA ESTA SELECIONADO)
# C2 - o primeiro diferente eh maior - NAO FAZ NADA (JA ESTA SELECIONADO)
# C3 - o primeiro diferente eh menor - DROPA











# Explicacao
# Explicar as duas condicoes
# ...
# Se o ultimo digito par for o ultimo digito do codigo do exutorio, significa # QUESTION:
# a propria bacia



# def eh_exutorio(codigo_exutorio, codigo_bacia):
#     codigo_exutorio = list(codigo_exutorio)
#     codigo_bacia    = list(codigo_bacia)
#
#     # 1 - identificacao do "trailing", que eh a parte do codigo a direita distinta entre ambos os codigos
#     k = []
#     for i in range(0,len(codigo_exutorio)):
#         try:
#             if codigo_bacia[i] != codigo_exutorio[i]:
#                 k.append(i)
#                 break
#         except:
#             continue
#
#     # 2a - procedimentos para o caso em que nao tenham sido detectadas diferencas
#     if not k:
#         if len(codigo_bacia) == 0: # bacia inconsistente (codigo vazio, por ex.)
#             return False
#         else: # eh o proprio codigo da bacia (ou um pedaco dele)
#             return True
#
#     # 2b - procedimentos para o caso em que foram detectadas diferencas
#     trailing_exutorio = codigo_exutorio[k[0]:]
#     trailing_bacia    = codigo_bacia[k[0]:]
#
#     # 3 - para ser outlet duas condicoes devem ser satisfeitas:
#     # c1 :: somente digitos impares em trailing_exutorio
#     c1 = all(int(n) % 2 == 1 for n in outlet_trailing)
#     # c2 :: primeiro digito de trailing_exutorio menor do que o primeiro digito de trailing_bacia
#     c2 = trailing_exutorio[0] < trailing_bacia[0]
#     if c1 & c2:
#         return True
#     else:
#         return False
