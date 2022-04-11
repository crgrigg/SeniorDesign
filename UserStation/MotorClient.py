# lets make the client code
import socket, pickle, struct
import XboxControllerPWM
import threading
#import client
import Global
from time import sleep
import time
import MasterDB

def motor_client():
    # create socket
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = '169.254.253.85' # paste your server ip address here
    port = 8000
    client_socket.connect((host_ip,port)) # a tuple
   
   
    data = 0
    while True:
        data = pickle.dumps(Global.ControllerMap)
        client_socket.sendall(data)
        value = client_socket.recv(8192)
        Global.MemMap = pickle.loads(value)
        print(Global.MemMap)
    client_socket.close()
