#Cheslyn Williams
#WLLCHE013
#uComputer - Raspberry Pi - Raspberry Pi Zero
#Retrieve Sensor Data from NodeMCU via TCP Socket and Store in Database
#October 2022

#Database Imports
import psycopg2
import datetime

#Connect to the postgres database
conn = psycopg2.connect("dbname=garden user=cheslyn")

#Open a cursor to perform database operations
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS testing;")
cur.execute("CREATE TABLE testing (IP TEXT, Moisture TEXT, TemperatureS TEXT, Humidity TEXT, TemperatureH TEXT, Light TEXT, Timestamp Text);")

#Socket Programming
from socket import *
serverPort = 11000

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen()

print("The server is ready to receive")

while True:
    connectionSocket, addr = serverSocket.accept()
    
    data = connectionSocket.recv(1024).decode()
    
    #Track time the data was received
    timing = datetime.datetime.now()
    timestamp = timing.strftime("%c")
    
    data = data[1:-1]

    broken = data.split(", ")

    moist = int(broken[0][1:-1])
    
    tempS = float(broken[1][1:-1])
    
    humid = float(broken[2][1:-1])
    
    tempH = float(broken[3][1:-1])
    
    light = float(broken[4][1:-1])
    
    print(str(addr))
    
    print("Moisture: " + str(moist) +  " TemperatureS: " + str(tempS) + "\u00b0C")
    print("Humidity: " + str(humid) + "%" + " TemperatureH: " + str(tempH) + "\u00b0C")
    print("Light: " + str(light) + " lux")
    print("\n")
    
    # Execute a query
    query = "INSERT INTO testing (IP, Moisture, TemperatureS, Humidity, TemperatureH, Light, Timestamp) VALUES ('" + str(addr[0]) + "', '" + str(moist) + "', '" + str(tempS) + "', '" + str(humid) + "', '" + str(tempH) + "', '" + str(light) + "', '" + timestamp + "');"
    cur.execute(query)

    #Make the changes to the database persistent
    conn.commit()
    connectionSocket.close()    

cur.close()
conn.close()