from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

from socket import *

serverName = '10.0.0.14'
serverPort = 12000
plant = ''

class Menu(Screen):
    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.option = 0
        self.option1 = 0
        self.monitor = ['', '']
        self.moist = [int(0), int(0)]
        self.humid = [float(0), float(0)]
        self.temp = [float(0), float(0)]
        self.light = [float(0), float(0)] 
        self.plant = ['', '']
        self.ideal_min_moist = [int(150), int(150)]
        self.ideal_max_moist = [int(2050), int(2050)]
        self.ideal_min_humid = [float(0), float(0)]
        self.ideal_max_humid = [float(100), float(100)]
        self.ideal_min_temp = [float(-40), float(-40)]
        self.ideal_max_temp = [float(70), float(70)]
        self.ideal_min_light = [float(0), float(0)]
        self.ideal_max_light = [float(10000), float(10000)]
        self.recommend_1 = ['', '']
        self.recommend_2 = ['', '']
        self.recommend_3 = ['', '']
        self.consistent()
        Clock.schedule_interval(lambda dt: self.consistent(), 30)

    def update(self):
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        clientSocket.send(str(self.option).encode())
        response = clientSocket.recv(1024).decode()
        data = response[1:-1].split(", ")
        clientSocket.close()
        self.monitor[self.option] = data[0][1:-1] 
        self.moist[self.option] = int(data[1][1:-1])
        self.humid[self.option] = float(data[3][1:-1])
        self.temp[self.option] = float(data[4][1:-1])
        self.light[self.option] = float(data[5][1:-1])
    
    def switch(self):
        if self.option == 0:
            self.option = 1
        else:
            self.option = 0
        self.update()

    def switch1(self):
        if self.option1 == 0:
            self.option1 = 1
        else:
            self.option1 = 0

    def consistent(self):
        self.switch()
        self.switch()

class CurrentConditions(Screen):
    def __init__(self, **kwargs):
        super(CurrentConditions, self).__init__(**kwargs)
        self.readings = manager.get_screen('menu')
        self.read()
        Clock.schedule_interval(lambda dt: self.read(), 30)
    
    def refresh(self):
        self.readings.update()
        self.read()
    
    def switch_device(self):
        self.readings.switch()
        self.read()

    def read(self):
        self.lbl0.text = "Monitoring Area: " + str(self.readings.option+1) + " [IP = " + self.readings.monitor[self.readings.option] + "]"
        self.lbl1.text = "Moisture: " + str(self.readings.moist[self.readings.option])
        self.lbl2.text = "Humidity: " + str(self.readings.humid[self.readings.option]) + "%" 
        self.lbl3.text = "Temperature: " + str(self.readings.temp[self.readings.option]) + "\u00b0C"
        self.lbl4.text = "Light Level: " + str(self.readings.light[self.readings.option]) + " lux"

class GardenProperties(Screen):
    def __init__(self, **kwargs):
        super(GardenProperties, self).__init__(**kwargs)
        self.readings = manager.get_screen('menu')
        self.lbl1.text = "Monitoring Area: " + str(self.readings.option1+1) + " [IP = " + self.readings.monitor[self.readings.option1] + "]"

    def set_plant(self):
        self.readings.plant[self.readings.option1] = self.inpt.text.lower()
        if not self.readings.plant[self.readings.option1] == '':
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((serverName, serverPort))
            clientSocket.send(self.readings.plant[self.readings.option1].encode())
            response = clientSocket.recv(1024).decode()
            if response  == "Not Avaliable":
                self.readings.plant[self.readings.option1] = 'Not Found'
                self.nothing()
                clientSocket.close
            else:
                data = response[1:-1].split(", ")
                self.readings.ideal_min_moist[self.readings.option1] = int(data[0][1:-1])
                self.readings.ideal_max_moist[self.readings.option1] = int(data[1][1:-1])
                self.readings.ideal_min_humid[self.readings.option1] = float(data[2][1:-1])
                self.readings.ideal_max_humid[self.readings.option1] = float(data[3][1:-1])
                self.readings.ideal_min_temp[self.readings.option1] = float(data[4][1:-1])
                self.readings.ideal_max_temp[self.readings.option1] = float(data[5][1:-1])
                self.readings.ideal_min_light[self.readings.option1] = float(data[6][1:-1])
                self.readings.ideal_max_light[self.readings.option1] = float(data[7][1:-1])
                self.readings.recommend_1[self.readings.option1] = data[8][1:-1]
                self.readings.recommend_2[self.readings.option1] = data[9][1:-1]
                self.readings.recommend_3[self.readings.option1] = data[10][1:-1]
                clientSocket.close()
        else:
            self.nothing()
        self.read()
        self.inpt.text = ''

    def switch_device(self):
        self.readings.switch1()
        self.read()
    
    def read(self):
        if not self.readings.plant[self.readings.option1] == '' and not self.readings.plant[self.readings.option1] == 'Not Found':
            self.lbl0.text = "Currently Monitored Plant: " + self.readings.plant[self.readings.option1].upper()
            self.lbl1.text = "Monitoring Area: " + str(self.readings.option1+1) + " [IP = " + self.readings.monitor[self.readings.option1] + "]"
            self.lbl2.text = "Ideal Moisture: " + str(self.readings.ideal_min_moist[self.readings.option1]) + " - " + str(self.readings.ideal_max_moist[self.readings.option1])
            self.lbl3.text = "Ideal Humidity: " + str(self.readings.ideal_min_humid[self.readings.option1]) + "% - " + str(self.readings.ideal_max_humid[self.readings.option1]) + "%"
            self.lbl4.text = "Ideal Temperature: " + str(self.readings.ideal_min_temp[self.readings.option1]) + "\u00b0C - " + str(self.readings.ideal_max_temp[self.readings.option1]) + "\u00b0C"
            self.lbl5.text =  "Ideal Light Level: " + str(self.readings.ideal_min_light[self.readings.option1]) + " lux - " + str(self.readings.ideal_max_light[self.readings.option1]) + " lux"
        else:
            self.lbl0.text = self.readings.plant[self.readings.option1]
            self.lbl1.text = "Monitoring Area: " + str(self.readings.option1+1) + " [IP = " + self.readings.monitor[self.readings.option1] + "]"
            self.lbl2.text = ''
            self.lbl3.text = ''
            self.lbl4.text = ''
            self.lbl5.text = '' 

    def nothing(self):
        self.readings.ideal_min_moist[self.readings.option1] = 150
        self.readings.ideal_max_moist[self.readings.option1] = 2050
        self.readings.ideal_min_humid[self.readings.option1] = 0
        self.readings.ideal_max_humid[self.readings.option1] = 100
        self.readings.ideal_min_temp[self.readings.option1] = -40
        self.readings.ideal_max_temp[self.readings.option1] = 70
        self.readings.ideal_min_light[self.readings.option1] = 0
        self.readings.ideal_max_light[self.readings.option1] = 10000
        self.readings.recommend_1[self.readings.option1] = ''
        self.readings.recommend_2[self.readings.option1] = ''
        self.readings.recommend_3[self.readings.option1] = ''   
        
class Recomendations(Screen):
    def __init__(self, **kwargs):
        super(Recomendations, self).__init__(**kwargs)

class Advice(Screen):
    def __init__(self, **kwargs):
        super(Advice, self).__init__(**kwargs)

class Ideal(Screen):
    def __init__(self, **kwargs):
        super(Ideal, self).__init__(**kwargs)
        self.look = ''

    def search(self):
        self.look = self.inpt.text.lower()
        if not self.look == '':
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((serverName, serverPort))
            clientSocket.send(self.look.encode())
            response = clientSocket.recv(1024).decode()
            if response  == "Not Avaliable":
                self.lbl0.text = "Not Found" 
                self.naked()
                clientSocket.close()
            else:
                data = response[1:-1].split(", ")
                self.lbl0.text = "Plant: " + self.look.upper()  
                self.lbl1.text = "Ideal Moisture: " + data[0][1:-1] + " - " + data[1][1:-1]
                self.lbl2.text = "Ideal Humidity: " + data[2][1:-1] + "% - " + data[3][1:-1] + "%"
                self.lbl3.text = "Ideal Temperature: " + data[4][1:-1] + "\u00b0C - " + data[5][1:-1] + "\u00b0C"
                self.lbl4.text =  "Ideal Light Level: " + data[6][1:-1] + " lux - " + data[7][1:-1] + " lux"
                self.lbl5.text =  data[8][1:-1]
                self.lbl6.text =  data[9][1:-1]
                self.lbl7.text =  data[10][1:-1]
                clientSocket.close()
        else:
            self.lbl0.text = ''
            self.naked()
        self.inpt.text = ''

    def naked(self):
        self.lbl1.text = ''
        self.lbl2.text = ''
        self.lbl3.text = ''
        self.lbl4.text = ''
        self.lbl5.text = ''
        self.lbl6.text = ''
        self.lbl7.text = ''

class Notifications(Screen):
    def __init__(self, **kwargs):
        super(Notifications, self).__init__(**kwargs)
        self.readings = manager.get_screen('menu')
        self.check()
        Clock.schedule_interval(lambda dt: self.check(), 30)
    
    def clear(self):
        self.lbl0.text = ''
        self.lbl1.text = ''
        self.lbl2.text = ''
        self.lbl3.text = ''
        self.lbl4.text = ''
        self.lbl5.text = ''
        self.lbl6.text = ''
    
    def move(self):
        self.lbl6.text = self.lbl5.text
        self.lbl5.text = self.lbl4.text
        self.lbl4.text = self.lbl3.text
        self.lbl3.text = self.lbl2.text
        self.lbl2.text = self.lbl1.text
        self.lbl1.text = self.lbl0.text
    
    def check(self):
        if self.readings.moist[0] < self.readings.ideal_min_moist[0] and not self.readings.monitor[0] == "N/A":
            prepare = self.readings.plant[0].upper() + " requires more moisture"
            if not prepare == self.lbl0.text and not prepare == self.lbl1.text and not prepare == self.lbl2.text and not prepare == self.lbl3.text and not prepare == self.lbl4.text and not prepare == self.lbl5.text and not prepare == self.lbl6.text:
                self.move()
                self.lbl0.text = prepare
        if self.readings.moist[1] < self.readings.ideal_min_moist[1] and not self.readings.monitor[1] == "N/A":
            prepare = self.readings.plant[1].upper() + " requires more moisture"
            if not prepare == self.lbl0.text and not prepare == self.lbl1.text and not prepare == self.lbl2.text and not prepare == self.lbl3.text and not prepare == self.lbl4.text and not prepare == self.lbl5.text and not prepare == self.lbl6.text:
                self.move()
                self.lbl0.text = prepare
        if self.readings.moist[0] > self.readings.ideal_max_moist[0] and not self.readings.monitor[0] == "N/A":
            prepare = self.readings.plant[0].upper() + " requires less moisture"
            if not prepare == self.lbl0.text and not prepare == self.lbl1.text and not prepare == self.lbl2.text and not prepare == self.lbl3.text and not prepare == self.lbl4.text and not prepare == self.lbl5.text and not prepare == self.lbl6.text:
                self.move()
                self.lbl0.text = prepare
        if self.readings.moist[1] > self.readings.ideal_max_moist[1] and not self.readings.monitor[1] == "N/A":
            prepare = self.readings.plant[1].upper() + " requires less moisture"
            if not prepare == self.lbl0.text and not prepare == self.lbl1.text and not prepare == self.lbl2.text and not prepare == self.lbl3.text and not prepare == self.lbl4.text and not prepare == self.lbl5.text and not prepare == self.lbl6.text:
                self.move()
                self.lbl0.text = prepare

        if self.readings.humid[0] < self.readings.ideal_min_humid[0] and not self.readings.monitor[0] == "N/A":
            prepare = self.readings.plant[0].upper() + " requires more humidity"
            if not prepare == self.lbl0.text and not prepare == self.lbl1.text and not prepare == self.lbl2.text and not prepare == self.lbl3.text and not prepare == self.lbl4.text and not prepare == self.lbl5.text and not prepare == self.lbl6.text:
                self.move()
                self.lbl0.text = prepare
        if self.readings.humid[1] < self.readings.ideal_min_humid[1] and not self.readings.monitor[1] == "N/A":
            prepare = self.readings.plant[1].upper() + " requires more humidity"
            if not prepare == self.lbl0.text and not prepare == self.lbl1.text and not prepare == self.lbl2.text and not prepare == self.lbl3.text and not prepare == self.lbl4.text and not prepare == self.lbl5.text and not prepare == self.lbl6.text:
                self.move()
                self.lbl0.text = prepare
        if self.readings.humid[0] > self.readings.ideal_max_humid[0] and not self.readings.monitor[0] == "N/A":
            prepare = self.readings.plant[0].upper() + " requires less humidity"
            if not prepare == self.lbl0.text and not prepare == self.lbl1.text and not prepare == self.lbl2.text and not prepare == self.lbl3.text and not prepare == self.lbl4.text and not prepare == self.lbl5.text and not prepare == self.lbl6.text:
                self.move()
                self.lbl0.text = prepare
        if self.readings.humid[1] > self.readings.ideal_max_humid[1] and not self.readings.monitor[1] == "N/A":
            prepare = self.readings.plant[1].upper() + " requires less humidity"
            if not prepare == self.lbl0.text and not prepare == self.lbl1.text and not prepare == self.lbl2.text and not prepare == self.lbl3.text and not prepare == self.lbl4.text and not prepare == self.lbl5.text and not prepare == self.lbl6.text:
                self.move()
                self.lbl0.text = prepare

        if self.readings.temp[0] < self.readings.ideal_min_temp[0] and not self.readings.monitor[0] == "N/A":
            prepare = self.readings.plant[0].upper() + " requires higher temperature"
            if not prepare == self.lbl0.text and not prepare == self.lbl1.text and not prepare == self.lbl2.text and not prepare == self.lbl3.text and not prepare == self.lbl4.text and not prepare == self.lbl5.text and not prepare == self.lbl6.text:
                self.move()
                self.lbl0.text = prepare
        if self.readings.temp[1] < self.readings.ideal_min_temp[1] and not self.readings.monitor[1] == "N/A":
            prepare = self.readings.plant[1].upper() + " requires higher temperature"
            if not prepare == self.lbl0.text and not prepare == self.lbl1.text and not prepare == self.lbl2.text and not prepare == self.lbl3.text and not prepare == self.lbl4.text and not prepare == self.lbl5.text and not prepare == self.lbl6.text:
                self.move()
                self.lbl0.text = prepare
        if self.readings.temp[0] > self.readings.ideal_max_temp[0] and not self.readings.monitor[0] == "N/A":
            prepare = self.readings.plant[0].upper() + " requires lower temperature"
            if not prepare == self.lbl0.text and not prepare == self.lbl1.text and not prepare == self.lbl2.text and not prepare == self.lbl3.text and not prepare == self.lbl4.text and not prepare == self.lbl5.text and not prepare == self.lbl6.text:
                self.move()
                self.lbl0.text = prepare
        if self.readings.temp[1] > self.readings.ideal_max_temp[1] and not self.readings.monitor[1] == "N/A":
            prepare = self.readings.plant[1].upper() + " requires lower temperature"
            if not prepare == self.lbl0.text and not prepare == self.lbl1.text and not prepare == self.lbl2.text and not prepare == self.lbl3.text and not prepare == self.lbl4.text and not prepare == self.lbl5.text and not prepare == self.lbl6.text:
                self.move()
                self.lbl0.text = prepare

        if self.readings.light[0] < self.readings.ideal_min_light[0] and not self.readings.monitor[0] == "N/A":
            prepare = self.readings.plant[0].upper() + " requires more light"
            if not prepare == self.lbl0.text and not prepare == self.lbl1.text and not prepare == self.lbl2.text and not prepare == self.lbl3.text and not prepare == self.lbl4.text and not prepare == self.lbl5.text and not prepare == self.lbl6.text:
                self.move()
                self.lbl0.text = prepare
        if self.readings.light[1] < self.readings.ideal_min_light[1] and not self.readings.monitor[1] == "N/A":
            prepare = self.readings.plant[1].upper() + " requires more light"
            if not prepare == self.lbl0.text and not prepare == self.lbl1.text and not prepare == self.lbl2.text and not prepare == self.lbl3.text and not prepare == self.lbl4.text and not prepare == self.lbl5.text and not prepare == self.lbl6.text:
                self.move()
                self.lbl0.text = prepare
        if self.readings.light[0] > self.readings.ideal_max_light[0] and not self.readings.monitor[0] == "N/A":
            prepare = self.readings.plant[0].upper() + " requires less light"
            if not prepare == self.lbl0.text and not prepare == self.lbl1.text and not prepare == self.lbl2.text and not prepare == self.lbl3.text and not prepare == self.lbl4.text and not prepare == self.lbl5.text and not prepare == self.lbl6.text:
                self.move()
                self.lbl0.text = prepare
        if self.readings.light[1] > self.readings.ideal_max_light[1] and not self.readings.monitor[1] == "N/A":
            prepare = self.readings.plant[1].upper() + " requires less light"
            if not prepare == self.lbl0.text and not prepare == self.lbl1.text and not prepare == self.lbl2.text and not prepare == self.lbl3.text and not prepare == self.lbl4.text and not prepare == self.lbl5.text and not prepare == self.lbl6.text:
                self.move()
                self.lbl0.text = prepare

manager = ScreenManager()

class MainApp(App):
    def build(self):
        self.title = "Home Garden Monitoring App"
        manager.add_widget(Menu(name='menu'))
        manager.add_widget(CurrentConditions(name='currentconditions'))
        manager.add_widget(GardenProperties(name='gardenproperties'))
        manager.add_widget(Recomendations(name='recomendations'))
        manager.add_widget(Advice(name='advice'))
        manager.add_widget(Ideal(name='ideal'))
        manager.add_widget(Notifications(name='notifications'))
        return manager

    def advice(self):
        self.readings = manager.get_screen('menu')
        self.recommends = manager.get_screen("advice")
        self.recommends.lbl0.text = "Plant: " + self.readings.plant[0].upper()
        self.recommends.lbl5.text = "Plant: " + self.readings.plant[1].upper()
        self.recommends.lbl1.text = "Area: 1 [" + self.readings.monitor[0] + "]"
        self.recommends.lbl6.text = "Area: 2 [" + self.readings.monitor[1] + "]"
        self.recommends.lbl2.text = self.readings.recommend_1[0]
        self.recommends.lbl7.text = self.readings.recommend_1[1]
        self.recommends.lbl3.text = self.readings.recommend_2[0]
        self.recommends.lbl8.text = self.readings.recommend_2[1]
        self.recommends.lbl4.text = self.readings.recommend_3[0]
        self.recommends.lbl9.text = self.readings.recommend_3[1]
    
if __name__ == '__main__':
    app = MainApp()
    app.run()