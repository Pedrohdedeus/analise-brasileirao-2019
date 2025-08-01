# %%
import pandas as pd

# Importando o arquivo csv com os dados das partidas

df = pd.read_csv("../dados_transformados_sql/partidas.csv", sep=',')
df


# %%
# Filtrando apenas as partidas do brasileirão de 2019  

df['data'] = pd.to_datetime(df['data'])

df_brasileiro_2019 =  df[df['data'].dt.year == 2019]  
df_brasileiro_2019

# %%

# Função que irá somar todos os gols de um time como mandante, visitante. Além de somá-los para obter a quantidade total de gols

def calcular_gols_times(df, nome_time):
    gols_mandante = df[df['mandante'] == nome_time]['mandante_placar'].sum()

    gols_visitante = df[df['visitante'] == nome_time]['visitante_placar'].sum()
    
    gols_totais = gols_mandante + gols_visitante

    return gols_mandante, gols_visitante, gols_totais


# %%

# Coletando o nome de todos os times em uma lista utilizando o tolist
# Unique para não repetir os valores.

list_times = pd.unique(df_brasileiro_2019['mandante'].tolist())
list_times 

# %%

# Criando o dicionário que ira unir o time, e a quantidade de gols. Utilizando o for para correr a lista com o nome dos times.

gols_por_time = {times: calcular_gols_times(df_brasileiro_2019, times) for times in list_times} 
gols_por_time 

# %%

# transformando o dicionario, em um data frame.
# E utilizando o items() para separar em duas colunas (times, gols) cada atributo.

df_gols_por_time = pd.DataFrame(gols_por_time.items(),columns=['Time', 'Gols'])

# %%

# Separando a tupla da coluna 'Gols' em colunas individuais.

df_gols_por_time[['Gols Como Mandante', 'Gols Como Visitante', 'Total']] = pd.DataFrame(df_gols_por_time['Gols'].tolist())
df_gols_por_time

# %%

"""
Excuindo a coluna (Gols), por não ter mais utilidade,
ordenando os valores pelo total, do maior para o menor,
Resetando o índice,
Retirando a coluna 'index' que continha os índices anteriormente.
"""

df_gols_por_time = (df_gols_por_time
                    .drop(columns='Gols')
                    .sort_values(by='Total', ascending=False)
                    .reset_index()
                    .drop(columns='index'))
df_gols_por_time

# %%

# Exportando a nova tabela para um arquivo csv.

df_gols_por_time.to_csv("../BrasileiraoAnalise/dados_transformados_python/gols_por_time.csv",sep= ';', index=False)