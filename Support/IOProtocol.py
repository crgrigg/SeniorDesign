from bitarray import bitarray



#Author: Charles Griggs, Jay Franko
#Date:  February 18, 2022
#
#
# User Connection Signals
#  The first byte of communication will be a control command
# INIT - 0x10   Initialize on board data and send to user. Master will then intialize data based on this input
#           -Formatted Set of all data
# UPDATE - 0x20 Update output signals from Master to Slave
# GET   - 0x30  Retrieve Inputs Data from Slave and send to Master
# ESTOP - 0x00   Emergency Stop all process  ## Can you Stop process?
# CLOSE - 0xF0   End Communication
# 

class IOProtocol:




    ########Constants

    #Communication Constraints
    MAX_LENGTH = 64000
    COMMAND_LENGTH = 8      # Command ID from Master to Slave 
    OBJECT_ID_LENGTH = 8    # Object ID number Length
    ATTRIBUTE_ID_LENGTH = 8 #Attribute ID number Length

    #ROV STATUS OBJECT
    OBJ_ROV = 0X00

    ATT_AUTO = 0X00
    ATT_AUTO_SIZE = 4

    ATT_ROV_RESERVE = 0X01
    ATT_ROV_RESERVE_SIZE = 20

    #ROV FAULTS OBJECT
    OBJ_FAULT = 0XFF
    OBJ_FAULT_SIZE = 32

    ATT_FAULT_RESERVE_ID = 0X00
    ATT_FAULT_RESERVER_SIZE = 24

    #MOTOR OBJECT
    OBJ_MOTOR = 0X0A
    OBJ_MOTOR_SIZE = 96

    ATT_MOTOR_ID = 0X00
    ATT_MOTOR_ID_SIZE = 8

    ATT_MOTOR_ON = 0X01
    ATT_MOTOR_ON_SIZE = 4

    ATT_MOTOR_SPEED = 0X02
    ATT_MOTOR_SPEED_SIZE = 32

    ATT_MOTOR_SPEED_ACK = 0X03
    ATT_MOTOR_SPEED_ACK_SIZE = 32
    
    ATT_MOTOR_RESERVE = 0X04
    ATT_MOTOR_RESERVE_SIZE = 14

    
    #CAMERA CONTROL OBJECT
    OBJ_CAM_CONTROL = 0X0B
    OBJ_CAM_CONTROL_SIZE = 64

    ATT_CAM_CONTROL_ON = 0X00
    ATT_CAM_CONTROL_ON_SIZE = 2

    ATT_CAM_CONTROL_RESERVE = 0X01
    ATT_CAM_CONTROL_RESERVE_SIZE = 54

    #ULTRASONIC SENSOR OBJECT
    OBJ_US_SENSOR = 0X11
    OBJ_US_SENSOR_SIZE = 32

    ATT_US_SENSOR_ON = 0X00
    ATT_US_SENSOR_ON_SIZE = 4

    ATT_US_SENSOR_DATA = 0X01
    ATT_US_SENSOR_DATA_SIZE = 32

    ATT_US_SENSOR_RESERVE = 0X02
    ATT_US_SENSOR_RESERVE_SIZE = 14


    #DEPTH SENSOR OBJECT
    OBJ_DEPTH_SENSOR = 0X12
    OBJ_DEPTH_SENSOR_SIZE = 72

    ATT_DEPTH_SENSOR_ON = 0X00
    ATT_DEPTH_SENSOR_ON_SIZE = 4

    ATT_DEPTH_SENSOR_DATA = 0X01
    ATT_DEPTH_SENSOR_DATA_SIZE =32

    ATT_DEPTH_SENSOR_RESERVED = 0X02
    ATT_DEPTH_SENSOR_RESERVED_SIZE = 14


    #TEMP SENSOR OBJECT
    OBJ_TEMP_SENSOR = 0X13
    OBJ_TEMP_SENSOR_SIZE = 72

    ATT_TEMP_SENSOR_ON = 0X00
    ATT_TEMP_SENSOR_ON_SIZE = 4

    ATT_TEMP_SENSOR_DATA = 0X01
    ATT_TEMP_SENSOR_DATA_SIZE =32

    ATT_TEMP_SENSOR_RESERVED = 0X02
    ATT_TEMP_SENSOR_RESERVED_SIZE = 14

    

  

