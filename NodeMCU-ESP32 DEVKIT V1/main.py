#Cheslyn Williams
#WLLCHE013
#Sensor Node Code For WSN Home Gardening
#October 2022

#Socket Programming
from socket import *

serverName = '10.0.0.14'
serverPort = 12000

#Sensor Data
#Import Functions
#NodeMCU pin management
from machine import Pin, I2C

#Delays
from time import sleep

#Soil Sensor Functionality
from stemma_soil_sensor import StemmaSoilSensor

#Humidity Sensor Functionality
from dht import DHT22

#Light Sensor Functionality
from bh1750 import BH1750

#Soil Sensor Setup
i2c0 = I2C(1)
ss = StemmaSoilSensor(i2c0)

#Humidity Sensor Setup
hs = DHT22(Pin(14))

#Light Sensor Setup
i2c1 = I2C(0)
ls = BH1750(i2c1)

while True:
  #Attempt to take Readings from Sensors and Print them
  try:
    #Delay
    sleep(2)

    #Read Moisture Level 
    moist = ss.get_moisture()

    #Read Temperature Level (Soil Sensor)
    tempS = ss.get_temp()
    
    #Measure Readings from Humidity Sensor
    hs.measure()

    #Read Humidity Level
    humid = hs.humidity()

    #Read Temperature Level (Humidity Sensor)
    tempH = hs.temperature()

    #Read Light Level
    light = ls.luminance(BH1750.ONCE_HIRES_1)

    #Print Readings to Screen
    print("Moisture: " + str(moist) +  " TemperatureS: " + str(tempS) + "\u00b0C")
    print("Humidity: " + str(humid) + "%" + " TemperatureH: " + str(tempH) + "\u00b0C")
    print("Light: " + str(light) + " lux")
    print("\n")
    
    #Send Readings to Raspberry Pi
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    sleep(1)
    clientSocket.send(str(moist).encode())
    sleep(1)
    clientSocket.send(str(tempS).encode())
    sleep(1)
    clientSocket.send(str(humid).encode())
    sleep(1)
    clientSocket.send(str(tempH).encode())
    sleep(1)
    clientSocket.send(str(light).encode())
    sleep(1)
    clientSocket.close()
  
  #Notify of Errors and Continue
  except OSError as e:
    print("Failed to read sensors")
    
  #KeyboardInterrupt
  except KeyboardInterrupt:
    print("keyboardInterrupt Error Caught")
    
  #Delay
  sleep(2)