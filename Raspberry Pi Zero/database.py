#Cheslyn Williams
#WLLCHE013
#uComputer - Raspberry Pi - Raspberry Pi Zero
#Enter pregathered data into data base
#October 2022

#Database Imports
import psycopg2

#Connect to the postgres database
conn = psycopg2.connect("dbname=garden user=cheslyn")

#Open a cursor to perform database operations
cur = conn.cursor()

while True:
    plant = input("Plant \n")
    min_moist = input("Min Moisture \n")
    max_moist = input("Max Moisture \n")
    min_humid = input("Min Humidity \n")
    max_humid = input("Max Humidity \n")
    min_temp = input("Min Temperature \n")
    max_temp = input("Max Temperature \n")
    min_light = input("Min Light \n")
    max_light = input("Max Light \n")
    recommend1 = input("Recommend1 \n")
    recommend2 = input("Recommend2 \n")
    recommend3 = input("Recommend3 \n")

    doit = "INSERT INTO plants (plant, min_moist, max_moist, min_humid, max_humid, min_temp, max_temp, min_light, max_light, recommend1, recommend2, recommend3) VALUES ('" + plant + "', '" + min_moist + "', '" + max_moist + "', '" + min_humid + "', '" + max_humid + "', '" + min_temp + "', '" + max_temp + "', '" + min_light + "', '" + max_light + "', '" + recommend1 + "', '" + recommend2 + "', '" + recommend3 + "');"
    cur.execute(doit)

    #Make the changes to the database persistent
    conn.commit()
    print("Done")

cur.close()
conn.close()