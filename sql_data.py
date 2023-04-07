import csv

#lista con todos los datos a ingresar a la base de datos

sql_data = [*csv.DictReader(open('ProyectoFinal\Video_Games_Sales_as_at_22_Dec_2016.csv'))]