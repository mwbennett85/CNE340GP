#Matt Bennett
#Calvin Davis
#Alex Nikolaev
#CNE340 3/8/2023
#Create a script that pulls data from a file, uploads it to a mysql database and performs some analytics
#Extensively used the resources found at https://matplotlib.org/stable/index.html and https://pandas.pydata.org/docs/index.html


import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import matplotlib.pyplot as plt


# Install cryptography, pymysql, mysql-connector-python and sqlalchemy
hostname = "127.0.0.1"
uname = "root"
pwd = ""
dbname = "meteor"  # Will need to create a db named meteor in phpmyadmin

engine = create_engine(f"mysql+mysqlconnector://{uname}:{pwd}@{hostname}/{dbname}")

tables = pd.read_csv('https://data.nasa.gov/api/views/gh4g-9sfh/rows.csv') #using pandas to download and read the csv

tables.rename(columns = {'mass (g)':'massg'}, inplace=True) #changing mass (g) to massg for ease of use

connection = engine.connect()

tables.to_sql('mets', con = engine, if_exists = 'append')      #creates the mets table, adds tables data, appends if already exists
connection.execute(text('CREATE TABLE mets_2 Like mets'))      #creates a secondary table to put distinct info
connection.execute(text('INSERT INTO mets_2 SELECT DISTINCT * FROM mets'))
connection.execute(text('DROP TABLE mets'))                    #drops first table
connection.execute(text('ALTER TABLE mets_2 RENAME TO mets'))  #renames to first table

df = pd.read_sql_table('mets', connection) #https://pandas.pydata.org/docs/reference/api/pandas.read_sql_table.html
                                           #Pulls the data from the table we just created and returns it to pandas form

max = df.loc[df['massg'].idxmax()] #Isolating index of the row with the largest massg
                                   #https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html

print(f'''The largest meteorite in NASA's dataset is {max['name']}.
It fell in the year {int(max['year'])} at {max['reclat']} latitude and {max['reclong']} longitude.
It weighed {max['massg']} grams, or in approximate Freedom Units, {max['massg']//453.6} pounds.
Click this link to see it on Google Maps: https://www.google.com/maps/place/{max['reclat']}+{max['reclong']}.''')
print("\n")
print('For more information on meteorite classifications, please check out the resources at: https://curator.jsc.nasa.gov/education/classification.cfm')


#Figure 1 (Matt)
#Initiate the plot and size
fig, ax = plt.subplots(figsize=(10, 4)) #Altered the size of the figure for readability

#Provide the data desired and the axis labels
ax.scatter(df['reclong'], df['reclat'], s=1, alpha=0.1) #s is the size of the plot point, reduced from standard 10
ax.set_xlabel('Longitude')                              #alpha is the opacity of the plot points, reduced for readability
ax.set_ylabel('Latitude')
ax.set_title('Meteorite Landing Sites')

#Figure 2 (Calvin)
fig, ax = plt.subplots(figsize=(10, 4))

year = ['Before 1900', '1900-1925', '1925-1950', '1950-1975', '1975-2000', 'After 2000']
counts = [((df['year'] < 1900).sum()), ((df['year'] >= 1900) & (df['year'] < 1925)).sum(),
    ((df['year'] >= 1925) & (df['year'] < 1950)).sum(), ((df['year'] >= 1950) & (df['year'] < 1975)).sum(),
    ((df['year'] >= 1975) & (df['year'] < 2000)).sum(), ((df['year'] >= 2000).sum())]

year_colors = ['tab:blue', 'tab:red', 'tab:green', 'tab:orange', 'tab:purple', 'tab:gray']

ax.bar(year, counts, color=year_colors)
ax.set_ylabel('Number of meteorites')
ax.set_title('Years of meteorite falls')

#Figure 3 (Calvin)
fig, ax = plt.subplots(figsize=(8, 8))
top = df['recclass'].value_counts().nlargest(7)
other = df['recclass'].value_counts().sum() - top.sum()
top['Other'] = other

plt.pie(top, labels=top.index, autopct='%1.1f%%')
plt.title('Top 7 Meteorite Classes')

#Figure 4 (Alex)
fig, ax = plt.subplots(figsize=(10, 4))
masses = ['Under 100', '100 to 1000', '1000 to 100000', '100000+']

counts = [((df['massg'] < 100).sum()), ((df['massg'] >= 100) & (df['massg'] < 1000)).sum(),
          ((df['massg'] >= 1000) & (df['massg'] < 100000)).sum(), ((df['massg'] >= 100000).sum())]

year_color = ['tab:pink', 'tab:purple', 'tab:orange', 'tab:red']

ax.bar(masses, counts, color=year_color)
ax.set_ylabel('Number of Meteors')
ax.set_title('Size of Meteors')


plt.show()

connection.close() #Close extension to database
