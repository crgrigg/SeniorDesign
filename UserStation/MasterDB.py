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
        self.UpdateFlag = 0

    def __init__(self):
        self.dataInit()
        self.Database = sqlite3.connect(self.DBName)
        self.Cursor = self.Database.cursor()
        self.TempValue = []
        self.PressureValue = []
        self.ULValue = []
        self.URValue = []
        self.UBValue = []
        self.TimeValue = []
        #self.CreateIOTable()

    def Update_Present(self):
        if self.UpdateFlag == 1:
            return True
        return False
    #Create Table for Sensors
    def CreateIOTable(self):
        self.Cursor.execute('''CREATE TABLE SensorData(TimeStamp text,Temp real, Pressure real,UltrasonicLeft real,
        UltrasonicRight real,UltrasonicDown real)''')

    #Create Table for Images
    def CreateImgTable(self):
        self.Cursor.execute('''CREATE TABLE ImageData(TimeStamp text,DetectionStatus int,CenterMass real,Image blob)''')
     #Read Range of Sensor Data from Database
    def ReadIORange(self):
         #Data = self.Cursor.execute(''' SELECT * FROM SensorData 
         #                               WHERE  timestamp >= ((SELECT MAX(timestamp) FROM SensorData) - %d)''' % self.Range)
         String = "SELECT * FROM SensorData WHERE  timestamp >= ((SELECT MAX(timestamp) FROM SensorData) -" + str(self.Range) + ")"
         self.NewValues = pd.read_sql(String,self.Database)
         if self.NewValues.empty:
            self.NewValues = self.Values
         else:
            self.Values = self.NewValues
         return self.NewValues

    #Write Sensor Data to IO Table
    def WriteIO(self):
        Data = Global.MemMap
        if self.UpdateFlag == 0:
            self.Cursor.execute('''INSERT INTO SensorData VALUES(?,?,?,?,?,?)''',
                                   (time.time(),
                                    Data["DepthSensor"]["Depth"],
                                    Data["TempSensor"]["TempC"],
                                    Data["UltraSensor1"]["Distance"],
                                    Data["UltraSensor2"]["Distance"],
                                    Data["UltraSensor3"]["Distance"]))
        self.Database.commit()
    
    #Read Sensor Data (all)
    def ReadIO(self):
        Data = self.Cursor.execute('''SELECT * FROM SensorData''')
        return pd.DataFrame(Data.fetchall())

    #Read Sensor Latest Data Entry    
    def ReadLastIO(self):
        Data = self.Cursor.execute('''SELECT * FROM SensorData 
                                       WHERE timestamp = (SELECT MAX(timestamp) FROM SensorData)''')
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


#i = 0 
#Database = MasterDB()
#while i < 20:
#    Database.WriteIO()
#    Value = Database.ReadIORange()
#    i += 1
#    sleep(5)
#    print(Value.Temp.values.tolist())