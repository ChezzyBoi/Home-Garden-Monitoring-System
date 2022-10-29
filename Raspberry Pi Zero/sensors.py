#Cheslyn Williams
#WLLCHE013
#uComputer - Raspberry Pi - Raspberry Pi Zero
#Retrieve Sensor Data from NodeMCU via TCP Socket and Store in Files
#October 2022

#Socket Programming
from socket import *
serverPort = 11000

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen()

file = open("result0.txt", "w")
file.write(str("['N/A', '0', '0', '0', '0', '0']"))
file.flush()
file.close

file = open("result1.txt", "w")
file.write(str("['N/A', '0', '0', '0', '0', '0']"))
file.flush()
file.close

#Keep track of devices connected
number = 0
devices = []
print("The server is ready to receive")

while True:
    connectionSocket, addr = serverSocket.accept()
    
    data = connectionSocket.recv(1024).decode()
        
    data = data[1:-1]

    broken = data.split(", ")

    if not str(addr[0]) in devices:
        devices.append(str(addr[0]))
        number += 1
        #Update number of connected devices
        file = open("number.txt", "w")
        file.write(str(number))
        file.flush()
        file.close

        #Update Devices IP Address
        file = open("devices", "w")
        file.write(str(devices))
        file.flush()
        file.close
    
    #Write data to specific file
    option = "result" + str(devices.index(str(addr[0]))) + ".txt"
    file = open(option, "w")

    moist = int(broken[0][1:-1])
    
    tempS = float(broken[1][1:-1])
    
    humid = float(broken[2][1:-1])
    
    tempH = float(broken[3][1:-1])
    
    light = float(broken[4][1:-1])
    
    arr = [str(addr[0]), str(moist), str(tempS), str(humid), str(tempH), str(light)]
    file.write(str(arr))
    file.flush()
    file.close

    print(str(addr))
    print("Moisture: " + str(moist) +  " TemperatureS: " + str(tempS) + "\u00b0C")
    print("Humidity: " + str(humid) + "%" + " TemperatureH: " + str(tempH) + "\u00b0C")
    print("Light: " + str(light) + " lux")
    print("\n")
    
    connectionSocket.close()   