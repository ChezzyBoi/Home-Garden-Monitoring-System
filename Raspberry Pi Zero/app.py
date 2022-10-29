#Cheslyn Williams
#WLLCHE013
#uComputer - Raspberry Pi - Raspberry Pi Zero
#App Querry Handling
#October 2022

#Socket Programming
from socket import *

from psycopg2.sql import NULL

serverPort = 12000

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen()

#Database Imports
import psycopg2

#Connect to the postgres database
conn = psycopg2.connect("dbname=garden user=cheslyn")

#Open a cursor to perform database operations
cur = conn.cursor()

devices = open("number.txt", "r")
number = int(devices.readline())
devices.close

print("The server is ready to receive")

while True:
    connectionSocket, addr = serverSocket.accept()
    
    data = connectionSocket.recv(1024).decode()

    option = 4

    if data.isdigit():
        option = int(data)

    if option == 0:
        devices = open("result0.txt", "r")
        data = str(devices.readline())
        devices.close
        connectionSocket.send(data.encode())
        connectionSocket.close()  

    elif option == 1:
        devices = open("result1.txt", "r")
        data = str(devices.readline())
        devices.close
        connectionSocket.send(data.encode())
        connectionSocket.close()   
    
    else:
        querry = "SELECT * FROM plants WHERE plant = '" + data + "';"
        cur.execute(querry)
        data = cur.fetchone()
        if data is None:
            connectionSocket.send(str("Not Avaliable").encode())
            connectionSocket.close
        else:
            broken = str(data)[1:-1].split(", ")
            fixed = [broken[1][1:-1], broken[2][1:-1], broken[3][1:-1], broken[4][1:-1], broken[5][1:-1], broken[6][1:-1], broken[7][1:-1], broken[8][1:-1], broken[9][1:-1], broken[10][1:-1], broken[11][1:-1]]
            connectionSocket.send(str(fixed).encode())
            connectionSocket.close

cur.close()
conn.close()   