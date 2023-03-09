#Matt Bennett
#CNE340 3/8/2023
#Create a script that pulls data from a file, uploads it to a mysql database and performs some analytics
#Extensively used the resources found at https://matplotlib.org/stable/index.html


import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import matplotlib.pyplot as plt


# install cryptography
hostname="127.0.0.1"
uname="root"
pwd=""
dbname="meteor"  # Will need to create a db named meteor in phpmyadmin

# install pymysql and sqlalchemy
engine = create_engine(f"mysql+mysqlconnector://{uname}:{pwd}@{hostname}/{dbname}")

tables = pd.read_csv('https://data.nasa.gov/api/views/gh4g-9sfh/rows.csv') #using pandas to download and read the csv

tables.rename(columns = {'mass (g)':'massg'}, inplace=True) #changing mass (g) to massg for ease of use

connection = engine.connect()

tables.to_sql('mets', con = engine, if_exists = 'append')      #creates the mets table, appends if already exists
connection.execute(text('CREATE TABLE mets_2 Like mets'))      #creates a secondary table to put distinct info
connection.execute(text('INSERT INTO mets_2 SELECT DISTINCT * FROM mets'))
connection.execute(text('DROP TABLE mets'))                    #drops first table
connection.execute(text('ALTER TABLE mets_2 RENAME TO mets'))  #renames to first table

df = pd.read_sql_table('mets', connection) #https://pandas.pydata.org/docs/reference/api/pandas.read_sql_table.html
                                           #Pulls the data from the table we just created and returns it to pandas form

#Initiate the plot and size
fig, axs = plt.subplots(figsize=(10, 4)) #Altered the size of the figure for readability

#Provide the data desired and the axis labels
axs.scatter(df['reclong'], df['reclat'], s=1, alpha=0.1) #s is the size of the plot point, reduced from standard 10
axs.set_xlabel('Longitude')                              #alpha is the opacity of the plot points, reduced for readability
axs.set_ylabel('Latitude')
axs.set_title('Meteorite Landing Sites')


plt.show()

connection.close() #Close extension to database
