import sqlite3
import numpy
import Global
from time import sleep
import time
import pandas as pd

class MasterDB():
    
    def dataInit(self):
        self.DBName = 'Data.db'
        self.BackUpDBName = 'BkUpData.db'
        self.Range = 10

    def __init__(self):
        self.dataInit()
        self.Database = sqlite3.connect('Data.db')
        self.Cursor = self.Database.cursor()
    

    #Create Table for Sensors
    def CreateIOTable(self):
        self.Cursor.execute('''CREATE TABLE SensorData(TimeStamp text,Temp real, Pressure real,UltrasonicLeft real,
        UltrasonicRight real,UltrasonicDown real)''')

    #Create Table for Images
    def CreateImgTable(self):
        self.Cursor.execute('''CREATE TABLE ImageData(TimeStamp text,DetectionStatus int,CenterMass real,Image blob)''')
    
    #Write Sensor Data to IO Table
    def WriteIO(self):
        Data = Global.MemMap
        self.Cursor.execute('''INSERT INTO SensorData VALUES(?,?,?,?,?,?)''',
                               (time.time(),
                                Data["DepthSensor"]["Depth"],
                                Data["TempSensor"]["Temp"],
                                Data["UltraSensor1"]["Distance"],
                                Data["UltraSensor2"]["Distance"],
                                Data["UltraSensor3"]["Distance"]))
    
    #Read Sensor Data (all)
    def ReadIO(self):
        Data = self.Cursor.execute('''SELECT * FROM SensorData''')
        return pd.DataFrame(Data.fetchall())

    #Read Sensor Latest Data Entry    
    def ReadLastIO(self):
        Data = self.Cursor.execute('''SELECT * FROM SensorData 
                                       WHERE timestamp = (SELECT MAX(timestamp) FROM SensorData)''')
        return pd.DataFrame(Data.fetchall())

    #Read Range of Sensor Data from Database
    def ReadIORange(self):
         Data = self.Cursor.execute(''' SELECT * FROM SensorData 
                                        WHERE  timestamp >= ((SELECT MAX(timestamp) FROM SensorData) - %d)''' % self.Range)
         return pd.DataFrame(Data.fetchall())

     #Max Timestamp
    def MaxTime(self):
        Data = self.Cursor.execute(''' SELECT timestamp FROM SensorData 
                                        WHERE  timestamp = (SELECT MAX(timestamp) FROM SensorData)''')
        return Data.fetchall()

    #Set Range for Graphing
    def setRange(self,NewRange):
        self.Range = NewRange

    def ClearIOTable(self):
        self.Cursor.execute('''DELETE * FROM SensorData''')

    def __del__(self):
        self.Database.commit()
