#Goniotape GUI
#Johnathan Schiede
#Rowan University Electrical & Computer Engineering class of 2025



# Import Functionality
import pygame as pg
import random
import serial
import sys
import numpy as np
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QTimer, Qt, QObject
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QComboBox
from PySide6.QtGui import QPalette, QColor


#Create Widget 
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        #Initialize variables
        self.fName = ""
        self.precaution = False
        self.caution = False

        #Initialize Serial Port Connection
        self.ser = serial.Serial('COM9', 9600) 

        

        #Text for Data Display
        self.text = QLabel("Goniotape V1",
                                     alignment=Qt.AlignCenter)
        
        
        
        #Create Save Button 
        self.savebutton = QPushButton()
        self.savebutton.setText("Save")
        self.savebutton.clicked.connect(self.fileSave)
        
       
        #Intialize Arrays for Data Collection
        self.timeData = np.array([])
        self.angleData = np.array([])
        self.data = np.array([0,0])


        #Initialize Timer to Acquire Data
        # Call every .1 seconds 100/1000 = .1s
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.dataSend)
        self.text.setText("Hello Welcome Press Start to Begin Data Collection")
        self.text.setStyleSheet("background-color: blue; color: black;font-size: 24px;")
        pg.mixer.init()
        self.sound = pg.mixer.Sound("beep-01a.mp3")
        
        
        #Joint Injury Selection Box
        self.injury = QComboBox(self)
        self.injury.setPlaceholderText(" ")
        self.injury.addItems(["Hip","Shoulder"])
        



        #Start/Stop Button
        self.startbutton = QPushButton()
        self.startbutton.setText("Start")
        self.startbutton.setStyleSheet("background-color: green")
        self.startStop = True
        self.startbutton.clicked.connect(self.startBut)
        
        #Reset Button 
        self.resetbutton = QPushButton()
        self.resetbutton.setText("Reset")
        self.resetbutton.setStyleSheet("background-color: red")
        self.resetbutton.clicked.connect(self.resetBut)

        #Create Layout on QApplication and Add Widgets to layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.injury)
        self.layout.addWidget(self.startbutton)
        self.layout.addWidget(self.savebutton)
        self.layout.addWidget(self.resetbutton)


        
        
        
        
    ## Implementation of Functionality 
   

    #Retrieve, Store, and Display Accelerometer Data  
    def dataSend(self):
            #Get Data From Serial Port
            data = self.ser.readline().decode().split(",")
            time = data[0]
            angle = data[1]

            #Add current data to total Data
            self.timeData = np.append(self.timeData, time)
            self.angleData = np.append(self.angleData, angle)

            
            #Display Data
            self.text.setText(f"Angle Degrees = {angle}, Time = {time}")

            #Precaution Detection
            if self.injury.currentText() == "Hip":
                 caution = 90>=float(angle)>=0
                 precaution = 110>=float(angle)>90
            elif self.injury.currentText() == "Shoulder":
                 caution = float(angle)>140
                 precaution = 140>=float(angle)>90
            else:
                 caution = False
                 precaution = False
            self.sound.stop()


            #Changes Made based on the current precaution status
            if (precaution):
                self.text.setStyleSheet("background-color: yellow; color: black; font-size: 24px;")
                sound_file = "beep-01a.mp3"
                self.sound = pg.mixer.Sound(sound_file)
                self.sound.play()
                self.text.setText(f"Caution You are approaching a precaution\nAngle = {angle}")
                
            elif(caution):
                self.text.setStyleSheet("background-color: red; color: black; font-size: 24px;")
                sound_file = "beep-13.mp3"
                self.sound = pg.mixer.Sound(sound_file)
                self.sound.play()
                self.text.setText(f"CAUTION Your Movement is Outside ofthe Restriction\nAngle = {angle}")
                
            else:
                self.text.setStyleSheet("background-color: blue; color: black; font-size: 24px;")
                 
            
                 
                 
            



    
    #Saves a .txt text File of the Angle and Time Data
    def fileSave(self):
        file, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text files (*.txt);;All files (*.*)")
        if file:
            try:
                with open(file, "w") as f:
                    # Replace this with the actual data you want to save
                    for i in range(0,len(self.angleData)-1):
                            f.write(f"Iteration = {i} Angle = {self.angleData[i]}  Time = {self.timeData[i]} Injury = {self.injury.currentText()}\n")
                    f.close()
            except Exception as e:
                print(f"Error saving file: {e}")
        
       

    #Starts and Stops QTimer
    def startBut(self):
         
        if (self.startStop):
              self.startbutton.setText("Stop")
              self.startbutton.setStyleSheet("background-color: red")
              self.timer.start(100)
              self.startStop = False
        else:
            self.startbutton.setText("Start")
            self.startbutton.setStyleSheet("background-color: green")
            self.timer.stop()
            self.startStop = True
            self.sound.stop()

    #Reset Data
    def resetBut(self):
        self.startbutton.setText("Start")
        self.startbutton.setStyleSheet("background-color: green")
        self.timer.stop()
        self.startStop = True
        self.sound.stop()
        self.timeData = np.array([])
        self.angleData = np.array([])
        self.text.setText("Hello Welcome Press Start to Begin Data Collection")
        self.text.setStyleSheet("background-color: blue; color: black; font-size: 24px;")

    

        

    
              


#Main Function to Launch Application
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    style = 'Fusion'
    app.setStyle(style)
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()
    widget.setWindowTitle("Goniotape")
    sys.exit(app.exec())

