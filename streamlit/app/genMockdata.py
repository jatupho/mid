import psycopg2
from psycopg2 import sql
import random

class PostgreSQLDB(object):
    def __init__(self, host='idap.eastus2.cloudapp.azure.com', port=5432, database_name="postgres", table_name="waterdata", user="cpe", password="Cpe@1234567!"):
        try:
            self._connection = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database_name
            )
            self._connection.autocommit = True
        except Exception as error:
            raise Exception(error)
        self._cursor = self._connection.cursor()

        self._table_name = table_name

        # ตรวจสอบหรือสร้างตาราง
        self._create_table()

    def _create_table(self):
        create_table_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {table} (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                date INT,
                month INT,
                year INT,
                water_data_front INT,
                water_data_back INT,
                water_drain_rate INT
            )
        """).format(table=sql.Identifier(self._table_name))
        self._cursor.execute(create_table_query)

    def insert(self, post):
        insert_query = sql.SQL("INSERT INTO {} (name, date, month, year, water_data_front, water_data_back, water_drain_rate) VALUES (%s, %s, %s, %s, %s, %s, %s)").format(sql.Identifier(self._table_name))
        self._cursor.execute(insert_query, (
            post['Name'],
            post['Date'],
            post['Month'],
            post['Year'],
            post['WaterDataFront'],
            post['WaterDataBack'],
            post['WaterDrainRate']
        ))

print('[*] Pushing data to PostgreSQL')
postgres_db = PostgreSQLDB()

# total days in every month during non leap years
M_DAYS = [0, 32, 29, 32, 31, 32, 31, 32, 32, 31, 32, 31, 32]

def isleap(year):
    """Return True for leap years, False for non-leap years."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
data_list = list()
for year in range(2024,2026,1):
    for month in range(1,13,1):
        for date in range(1,M_DAYS[month],1):
            data_list.append({'Name':'Huana','Date':date,'Month':month,'Year':year,'WaterDataFront':random.randrange(100,200,1),'WaterDataBack':random.randrange(90,180,1),'WaterDrainRate':random.randrange(90,150,2)})
        if month==2 and isleap(year):
            data_list.append({'Name':'Huana','Date':29,'Month':month,'Year':year,'WaterDataFront':random.randrange(100,200,1),'WaterDataBack':random.randrange(90,180,1),'WaterDrainRate':random.randrange(90,150,2)})

for collection in data_list:
    print('[!] Inserting - ', collection)
    postgres_db.insert(collection)
