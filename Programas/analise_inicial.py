import pandas as pd
import fiona
import geopandas as gpd


sanepar = gpd.read_file('Bacia_de_Mananciais_Ativos.shp')
shapes = fiona.listlayers('/Users/arlan/Downloads/REDE_Hidrografica_OTTOCODIFICADA_PR.gdb')
areas_drenagem = shapes[0]
trech_drenagem = shapes[1]
ottobac = gpd.read_file('/Users/arlan/Downloads/REDE_Hidrografica_OTTOCODIFICADA_PR.gdb', \
            layer=areas_drenagem)


def eh_exutorio(codigo_exutorio, codigo_bacia):
    codigo_exutorio = list(codigo_exutorio)
    codigo_bacia    = list(codigo_bacia)

    # 1 - identificacao do "trailing", que eh a parte do codigo a direita distinta entre ambos os codigos
    k = []
    for i in range(0,len(codigo_exutorio)):
        try:
            if codigo_bacia[i] != codigo_exutorio[i]:
                k.append(i)
                break
        except:
            continue

    # 2a - procedimentos para o caso em que nao tenham sido detectadas diferencas
    if not k:
        if len(codigo_bacia) == 0: # bacia inconsistente (codigo vazio, por ex.)
            return False
        else: # eh o proprio codigo da bacia (ou um pedaco dele)
            return True

    # 2b - procedimentos para o caso em que foram detectadas diferencas
    trailing_exutorio = codigo_exutorio[k[0]:]
    trailing_bacia    = codigo_bacia[k[0]:]

    # 3 - para ser outlet duas condicoes devem ser satisfeitas:
    # c1 :: somente digitos impares em trailing_exutorio
    c1 = all(int(n) % 2 == 1 for n in outlet_trailing)
    # c2 :: primeiro digito de trailing_exutorio menor do que o primeiro digito de trailing_bacia
    c2 = trailing_exutorio[0] < trailing_bacia[0]
    if c1 & c2:
        return True
    else:
        return False
