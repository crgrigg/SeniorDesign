# lets make the client code
import socket, pickle, struct
import XboxControllerPWM
import threading
import client
import Global
#import MasterDB
import time

# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '169.254.253.85' # paste your server ip address here
port = 8002

client_socket.connect((host_ip,port)) # a tuple


myThread = threading.Thread(target=XboxControllerPWM.get_signals)
myComputer = threading.Thread(target = client.computer_visual)
myThread.start()
myComputer.start()
data = 0
while True:
    data = pickle.dumps(Global.ControllerMap)
  
    client_socket.sendall(data)
    value = client_socket.recv(8192)
    value = pickle.loads(value)
    seconds = time.time()
    local_time = time.ctime(seconds)

 
client_socket.close()
