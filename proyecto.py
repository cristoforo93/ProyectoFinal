# %%
import pandas as pd
import numpy as np
import psycopg2
import boto3
import configparser
import seaborn as sb
import matplotlib.pyplot as plt

# %% [markdown]
# ## Configuración de la base de datos

# %%
config = configparser.ConfigParser()
config.read('proyecto.cfg')

# %% [markdown]
# ## Conexión a base de datos

# %%
import sql_queries

try:
    db_conn = psycopg2.connect(
        database = config.get('RDS', 'DB_NAME'),
        user = config.get('RDS', 'DB_USER'),
        password = config.get('RDS', 'DB_PASSWORD'),
        host = config.get('RDS', 'DB_HOST'),
        port = config.get('RDS', 'DB_PORT')
    )
    cursor = db_conn.cursor()
    cursor.execute(sql_queries.DDL_QUERY)
    db_conn.commit()
    print("Base de datos creada exitosamente.")
except Exception as ex:
    print("ERROR: Error al crear la base de datos.")
    print(ex)

# %% [markdown]
# ## Carga de datos

# %%
def insertDataToSQL(data_dict, table_name):
     postgres_driver = f"""postgresql://{config.get('RDS', 'DB_USER')}:{config.get('RDS', 'DB_PASSWORD')}@{config.get('RDS','DB_HOST')}:{config.get('RDS', 'DB_PORT')}/{config.get('RDS', 'DB_NAME')}"""    
     df_data = pd.DataFrame.from_records(data_dict)
     try:
          response = df_data.to_sql(table_name, postgres_driver, index=False, if_exists='append')
          print(f'Se han insertado {response} nuevos registros.' )
     except Exception as ex:
          print(ex)

# %%
import csv

sql_data = [*csv.DictReader(open('Video_Games_Sales_as_at_22_Dec_2016.csv'))]

insertDataToSQL(
    sql_data,
    'gamesales'
)

# %% [markdown]
# ## Análisis de los datos

# %%
sql_query = 'SELECT * FROM gamesales'
postgres_driver = f"""postgresql://{config.get('RDS', 'DB_USER')}:{config.get('RDS', 'DB_PASSWORD')}@{config.get('RDS','DB_HOST')}:{config.get('RDS', 'DB_PORT')}/{config.get('RDS', 'DB_NAME')}"""

#Carga de los datos a un dataframe
gamesales = pd.read_sql(sql_query, postgres_driver)
gamesales.info()

# %% [markdown]
# ### Ventas totales por región
# * Plataforma

# %%
#NA_Sales
plataforma = gamesales[['Platform','NA_Sales']]
plataforma['NA_Sales'] = plataforma['NA_Sales'].astype('float')
plataforma.groupby('Platform').sum().sort_values('NA_Sales',ascending=False)

# %%
#EU_Sales
plataforma = gamesales[['Platform','EU_Sales']]
plataforma['EU_Sales'] = plataforma['EU_Sales'].astype('float')
plataforma.groupby('Platform').sum().sort_values('EU_Sales',ascending=False)

# %%
#JP_Sales
plataforma = gamesales[['Platform','JP_Sales']]
plataforma['JP_Sales'] = plataforma['JP_Sales'].astype('float')
plataforma.groupby('Platform').sum().sort_values('JP_Sales',ascending=False)

# %%
#Other_Sales
plataforma = gamesales[['Platform','Other_Sales']]
plataforma['Other_Sales'] = plataforma['Other_Sales'].astype('float')
plataforma.groupby('Platform').sum().sort_values('Other_Sales',ascending=False)

# %%
#Global_Sales
plataforma = gamesales[['Platform','Global_Sales']]
plataforma['Global_Sales'] = plataforma['Global_Sales'].astype('float')
print(plataforma.groupby('Platform').sum().sort_values('Global_Sales',ascending=False))
plot = sb.scatterplot(data = plataforma.groupby('Platform').sum().sort_values('Global_Sales',ascending=False),
               x='Platform',
               y='Global_Sales')
plt.setp(plot.get_xticklabels(),rotation=90)

# %% [markdown]
# * Año de lanzamiento

# %%
#Global_Sales
año = gamesales[['Year_of_Release','Global_Sales']]
año['Global_Sales'] = año['Global_Sales'].astype('float')
print(año.groupby('Year_of_Release').sum().sort_values('Global_Sales',ascending=False))
plot = sb.scatterplot(data = año.groupby('Year_of_Release').sum().sort_values('Global_Sales',ascending=False),
               x='Year_of_Release',
               y='Global_Sales')
plt.setp(plot.get_xticklabels(),rotation=90)

# %% [markdown]
# * Género

# %%
#Global_Sales
genero = gamesales[['Genre','Global_Sales']]
genero['Global_Sales'] = genero['Global_Sales'].astype('float')
print(genero.groupby('Genre').sum().sort_values('Global_Sales',ascending=False))
plot = sb.scatterplot(data = genero.groupby('Genre').sum().sort_values('Global_Sales',ascending=False),
               x='Genre',
               y='Global_Sales')
plt.setp(plot.get_xticklabels(),rotation=90)

# %% [markdown]
# * Publisher

# %%
#Global_Sales
publisher = gamesales[['Publisher','Global_Sales']]
publisher['Global_Sales'] = publisher['Global_Sales'].astype('float')
print(publisher.groupby('Publisher').sum().sort_values('Global_Sales',ascending=False))
plot = sb.scatterplot(data = publisher.groupby('Publisher').sum().sort_values('Global_Sales',ascending=False).iloc[:10],
               x='Publisher',
               y='Global_Sales')
plt.setp(plot.get_xticklabels(),rotation=90)

# %% [markdown]
# ## Mejor plataforma
# Como vimos anteriormente, el PS2 es la consola con mejores ventas globales a la fecha de los datos.

# %%
ps2 = gamesales.loc[gamesales['Platform']=='PS2']
print(
    ps2['Global_Sales'].isnull().values.any()
)
ps2 = ps2.loc[ps2['Critic_Score'] != '']
ps2['Critic_Score'] = ps2['Critic_Score'].astype('float')

# %% [markdown]
# * Juego con las mejores ventas

# %%
ps2 = ps2.loc[ps2['Critic_Score'].sort_values(ascending=False)>=80]
plot = sb.scatterplot(data=ps2.iloc[:10],
               x='Name',
               y='Critic_Score')
plt.setp(plot.get_xticklabels(),rotation=90)

# %%
ps2 = gamesales.loc[gamesales['Platform']=='PS2']
print(
    ps2['Global_Sales'].isnull().values.any()
)
ps2 = ps2.loc[ps2['User_Score'] != '']
ps2['User_Score'] = ps2['User_Score'].astype('float')

# %%
ps2 = ps2.loc[ps2['User_Score'].sort_values(ascending=False)>=8]
plot = sb.scatterplot(data=ps2.iloc[:10],
               x='Name',
               y='User_Score')
plt.setp(plot.get_xticklabels(),rotation=90)


